/* bsp.c -- board support for the zan rv32 kit on QEMU riscv32 'virt'.
 *
 * Freestanding except newlib headers: newlib supplies libc (printf,
 * memcpy, setjmp) and libgcc supplies soft-float + lock-based __atomic_*
 * for rv32imc. This file is everything board-specific:
 *   - NS16550A UART console (newlib retarget: _write/_read/...)
 *   - CLINT mtime as the zan timer clock (overrides the weak
 *     zan_timer_now_ms from rt_timer.c) and as the await sleep source:
 *     poll() arms mtimecmp and wfi's -- the timer interrupt wakes the
 *     scheduler, so Task.Delay idles instead of spinning
 *   - exit()/abort(): report stack high-water, then finish QEMU via the
 *     sifive_test device
 */
#include <stdint.h>
#include <stddef.h>
#include <sys/stat.h>
#if defined(__has_include)
#if __has_include(<stdio.h>)
#include <stdio.h>             /* FILE / FDEV_SETUP_STREAM: console wiring */
#endif
#endif

/* ---- QEMU 'virt' memory map ---------------------------------------- */
#define UART0_BASE   0x10000000u /* NS16550A, byte-wide registers */
#define UART_THR     0u
#define UART_LSR     5u
#define UART_LSR_THRE 0x20u
#define CLINT_BASE   0x2000000ull
#define CLINT_MTIMECMP (CLINT_BASE + 0x4000)
#define CLINT_MTIME    (CLINT_BASE + 0xbff8)
#define TIMEBASE_HZ  10000000ull  /* virt's CLINT ticks at 10 MHz */
#define TEST_FINISHER 0x100000u   /* sifive_test: QEMU exits here */
#define FINISHER_PASS 0x5555u
#define FINISHER_FAIL 0x3333u

extern unsigned char __stack_bottom[], __stack_top[];

static volatile uint8_t *const uart = (volatile uint8_t *)UART0_BASE;

static void uart_putc(char c) {
    while (!(uart[UART_LSR] & UART_LSR_THRE)) { }
    uart[UART_THR] = (uint8_t)c;
}

static void uart_write(const char *s, unsigned len) {
    for (unsigned i = 0; i < len; i++) {
        if (s[i] == '\n') uart_putc('\r');   /* CRLF for the monitor */
        uart_putc(s[i]);
    }
}

/* ---- CLINT time ------------------------------------------------------ */

#if defined(__has_include)
#if __has_include(<stdio.h>)
/* picolibc tinystdio ships no stdout object: the board provides the
 * console FILE backed by the UART. */
static int zan_stdout_putc(char c, FILE *f) {
    (void)f;
    if (c == '\n') uart_putc('\r');
    uart_putc(c);
    return (unsigned char)c;
}
static FILE zan_stdout_file = FDEV_SETUP_STREAM(zan_stdout_putc, 0, 0,
                                                _FDEV_SETUP_WRITE);
FILE *const stdout = &zan_stdout_file;
#endif
#endif

static uint64_t mtime_read(void) {
    uint32_t hi, lo;
    do {
        hi = *(volatile uint32_t *)(CLINT_MTIME + 4);
        lo = *(volatile uint32_t *)CLINT_MTIME;
    } while (hi != *(volatile uint32_t *)(CLINT_MTIME + 4));
    return ((uint64_t)hi << 32) | lo;
}

/* Overrides the weak zan_timer_now_ms from rt_timer.c (-DZAN_BARE_METAL). */
long long zan_timer_now_ms(void) {
    return (long long)(mtime_read() / (TIMEBASE_HZ / 1000));
}

/* ---- rv32imc atomics: no A-extension, so shield with the IRQ lock ----
 * The zan runtime's reference counts and timer state use LLVM atomic
 * intrinsics, which lower to __atomic_* libgcc calls on rv32im; libgcc's
 * lock-based variants need an OS lock object, so the bare-metal kit
 * provides the ones the zan object actually references. Single hart:
 * clearing MIE is a sufficient exclusive section. */
static inline unsigned long zan_irq_lock(void) {
    unsigned long f;
    asm volatile ("csrrc %0, mstatus, %1" : "=r"(f) : "rK"(0x8) : "memory");
    return f;
}
static inline void zan_irq_unlock(unsigned long f) {
    if (f & 0x8) asm volatile ("csrs mstatus, %0" :: "rK"(0x8) : "memory");
}

uint32_t __atomic_exchange_4(void *p, uint32_t v, int m) {
    (void)m;
    unsigned long f = zan_irq_lock();
    uint32_t old = *(volatile uint32_t *)p;
    *(volatile uint32_t *)p = v;
    zan_irq_unlock(f);
    return old;
}

uint64_t __atomic_load_8(const void *p, int m) {
    (void)m;
    unsigned long f = zan_irq_lock();
    uint64_t v = *(volatile uint64_t *)p;
    zan_irq_unlock(f);
    return v;
}

uint64_t __atomic_fetch_add_8(void *p, uint64_t v, int m) {
    (void)m;
    unsigned long f = zan_irq_lock();
    volatile uint64_t *q = (volatile uint64_t *)p;
    uint64_t old = *q;
    *q = old + v;
    zan_irq_unlock(f);
    return old;
}

uint64_t __atomic_fetch_sub_8(void *p, uint64_t v, int m) {
    (void)m;
    unsigned long f = zan_irq_lock();
    volatile uint64_t *q = (volatile uint64_t *)p;
    uint64_t old = *q;
    *q = old - v;
    zan_irq_unlock(f);
    return old;
}

/* ---- awaits sleep: arm the comparator, wfi, timer irq wakes us ------ */

int poll(void *fds, unsigned long nfds, int timeout) {
    (void)fds; (void)nfds;
    if (timeout == 0) return 0;            /* nothing to wait for */
    uint64_t slice = (timeout < 0) ? 10u   /* no deadline: short slice */
                                   : (uint64_t)timeout;
    uint64_t deadline = mtime_read() + slice * (TIMEBASE_HZ / 1000);
    *(volatile uint32_t *)(CLINT_MTIMECMP + 4) = (uint32_t)(deadline >> 32);
    *(volatile uint32_t *)CLINT_MTIMECMP = (uint32_t)deadline;
    asm volatile ("csrs mie, %0" :: "r"(0x80));   /* MTIE */
    asm volatile ("csrsi mstatus, 0x8");          /* MIE */
    asm volatile ("wfi");                         /* wakes on MTIP */
    asm volatile ("csrci mstatus, 0x8");
    asm volatile ("csrc mie, %0" :: "r"(0x80));
    return 0;   /* scheduler dispatches due timers, then calls again */
}

/* ---- newlib syscalls ------------------------------------------------- */

int _write(int fd, const char *buf, unsigned len) {
    if (fd == 1 || fd == 2) { uart_write(buf, len); return (int)len; }
    return -1;
}

int _read(int fd, char *buf, unsigned len) {
    (void)buf; (void)len; (void)fd;
    return -1;                             /* no stdin on the board */
}

int _open(const char *path, int flags, int mode) {
    (void)path; (void)flags; (void)mode;
    return -1;   /* no filesystem: rt_timer's soft-log fopen degrades to
                    a single stderr line, by design */
}
int _close(int fd) { (void)fd; return -1; }
int _lseek(int fd, int off, int whence) { (void)fd; (void)off; (void)whence; return 0; }
int _unlink(const char *p) { (void)p; return -1; }

int _fstat(int fd, struct stat *st) {
    (void)fd;
    st->st_mode = S_IFCHR;                 /* console is a char device */
    return 0;
}
int _isatty(int fd) { return (fd == 1 || fd == 2); }

void *_sbrk(int inc) { (void)inc; return (void *)-1; }  /* zan uses the
                                    deterministic pool in rt_bare_shim.c */
int _getpid(void) { return 1; }
int _kill(int pid, int sig) { (void)pid; (void)sig; return -1; }

/* ---- shutdown: report, then finish QEMU ------------------------------ */

static void uart_print_dec(long long v) {
    char buf[24];
    int i = 0;
    unsigned long long u = v < 0 ? (unsigned long long)-(v + 1) + 1
                                 : (unsigned long long)v;
    do { buf[i++] = (char)('0' + u % 10); u /= 10; } while (u);
    if (v < 0) uart_putc('-');
    while (i) uart_putc(buf[--i]);
}

void __attribute__((noreturn)) exit(int code) {
    /* stdout is a write-through UART stream, so there is nothing to
     * flush; the report below goes straight out the same line. */
    /* stack high-water: first guard-violating word since boot */
    const volatile uint32_t *p = (const volatile uint32_t *)__stack_bottom;
    while (p < (const volatile uint32_t *)__stack_top && *p == 0xABABABABu)
        p++;
    unsigned long used = (unsigned long)__stack_top - (unsigned long)p;

    uart_write("\n[zan] exit code: ", 18);
    uart_print_dec(code);
    uart_write("\n[zan] stack high-water: ", 25);
    uart_print_dec((long long)used);
    uart_write(" of ", 4);
    uart_print_dec((long long)(__stack_top - __stack_bottom));
    uart_write(" bytes\n", 7);

    uint32_t finisher = code ? (FINISHER_FAIL | ((uint32_t)code << 16))
                             : FINISHER_PASS;
    *(volatile uint32_t *)TEST_FINISHER = finisher;
    for (;;) { asm volatile ("wfi"); }
}

void abort(void) { exit(134); }            /* 128 + SIGABRT convention */
