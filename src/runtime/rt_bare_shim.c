/* rt_bare_shim.c -- freestanding shim for zanc's bare-metal targets.
 *
 * Not built by zan's CMake: compile this file with the TARGET SDK's C
 * compiler and link it with the object zanc emits (`zanc app.zan --target
 * riscv32 -o app.o`). It covers the POSIX-ish surface the emitted code
 * references when there is no OS underneath. On ESP-IDF you do not need
 * this file -- the IDF adapter (examples/esp32_hello) uses IDF's newlib,
 * pthread and vfs components instead, which behave better than these
 * stubs wherever both exist.
 *
 * What this file provides (strong definitions: if your libc also defines
 * one, the libc's archive member is simply never pulled in):
 *   malloc/calloc/free/realloc  deterministic pool allocator below
 *                               (-DZAN_BARE_HEAP_BYTES=... to size it)
 *   poll                        always "nothing ready" -- the scheduler's
 *                               pump falls through to its timer dispatch,
 *                               so awaits busy-wait (correct, power-hungry)
 *   pthread_mutex_lock/unlock   no-ops, pthread_self -> 1 (single thread
 *                               is the bare-metal contract)
 *   getenv                      NULL
 *   zan_w32_snprintf            snprintf with a long-long size parameter;
 *                               the compiler routes IR snprintf calls here
 *                               on 32-bit targets because an i64 in the
 *                               middle of the ilp32 argument list shifts
 *                               the register-pair alignment of everything
 *                               after it
 *
 * What must come from your toolchain (a riscv32 libc + libgcc, e.g.
 * picolibc or newlib-nano; NOT provided here):
 *   printf/setvbuf/stdout (Console output), exit, memcpy/memset/strlen,
 *   _setjmp/longjmp (try/throw lower onto them), __atomic_*_8 (rv32imc
 *   has no A extension -- libgcc's lock-based fallbacks are fine).
 */
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#if defined(__has_include)
#if __has_include(<stdio.h>)
#include <stdio.h>
#define ZAN_SHIM_HAVE_STDIO 1
#endif
#endif
#ifndef ZAN_SHIM_HAVE_STDIO
/* headerless rv32 toolchain (no sysroot): declare just what we call */
typedef __builtin_va_list zan_va_list;
int vsnprintf(char *s, unsigned long n, const char *fmt, zan_va_list ap);
#define va_list zan_va_list
#endif

/* Stub symbols are weak so a board bring-up (QEMU kit, Arduino core, ...)
 * can override them with strong definitions while still linking this file
 * for the allocator. */
#if defined(__ELF__)
#define ZAN_SHIM_WEAK __attribute__((weak))
#else
#define ZAN_SHIM_WEAK
#endif

/* ---- deterministic pool allocator -----------------------------------
 * First fit with a free list, 8-byte aligned (rv32 long long / double).
 * Out of pool: returns NULL -- the runtime's call sites treat that as a
 * soft failure (the timer heap drops the delay and readies the frame, the
 * string builder reports OOM) rather than aborting. */

#ifndef ZAN_BARE_HEAP_BYTES
#define ZAN_BARE_HEAP_BYTES (64 * 1024)
#endif

union zan_shim_block {
    struct {
        size_t size;             /* payload bytes, free blocks only */
        union zan_shim_block *next;
    } hdr;
    /* guarantees the payload is 8-byte aligned and at least word sized */
    long long align_min;
    unsigned char align_bytes[16];
};

static unsigned char zan_shim_pool[ZAN_BARE_HEAP_BYTES]
    __attribute__((aligned(8)));
static union zan_shim_block *zan_shim_free = NULL;
static int zan_shim_pool_ready;

static void zan_shim_pool_init(void) {
    union zan_shim_block *b = (union zan_shim_block *)zan_shim_pool;
    size_t bytes = sizeof(zan_shim_pool);
    if (bytes < sizeof(*b)) return;
    b->hdr.size = bytes - sizeof(*b);
    b->hdr.next = NULL;
    zan_shim_free = b;
    zan_shim_pool_ready = 1;
}

void *malloc(size_t n) {
    if (!zan_shim_pool_ready) zan_shim_pool_init();
    if (n == 0) n = 1;
    n = (n + 7u) & ~(size_t)7u;
    union zan_shim_block **prev = &zan_shim_free;
    for (union zan_shim_block *b = zan_shim_free; b; b = b->hdr.next) {
        if (b->hdr.size < n) { prev = &b->hdr.next; continue; }
        size_t rest = b->hdr.size - n;
        if (rest >= sizeof(*b)) {
            /* split: hand out the front, keep the tail on the free list */
            union zan_shim_block *tail =
                (union zan_shim_block *)((unsigned char *)b + sizeof(*b) + n);
            tail->hdr.size = rest - sizeof(*b);
            tail->hdr.next = b->hdr.next;
            *prev = tail;
        } else {
            *prev = b->hdr.next;
        }
        b->hdr.size = n;         /* free() reads this back */
        return (unsigned char *)b + sizeof(*b);
    }
    return NULL;
}

void free(void *p) {
    if (!p) return;
    union zan_shim_block *b =
        (union zan_shim_block *)((unsigned char *)p - sizeof(*b));
    b->hdr.next = zan_shim_free;
    zan_shim_free = b;
}

void *calloc(size_t count, size_t size) {
    size_t total = count * size;
    void *p = malloc(total);
    if (p) {
        unsigned char *q = (unsigned char *)p;
        for (size_t i = 0; i < total; i++) q[i] = 0;
    }
    return p;
}

void *realloc(void *p, size_t n) {
    if (!p) return malloc(n);
    if (!n) { free(p); return NULL; }
    union zan_shim_block *b =
        (union zan_shim_block *)((unsigned char *)p - sizeof(*b));
    size_t old = b->hdr.size;
    void *np = malloc(n);
    if (!np) return NULL;
    unsigned char *src = (unsigned char *)p;
    unsigned char *dst = (unsigned char *)np;
    for (size_t i = 0; i < (old < n ? old : n); i++) dst[i] = src[i];
    free(p);
    return np;
}

/* ---- single-thread stubs -------------------------------------------- */

ZAN_SHIM_WEAK int poll(void *fds, unsigned long nfds, int timeout) {
    (void)fds; (void)nfds; (void)timeout;
    return 0;                    /* nothing ready: pump falls to timers */
}

ZAN_SHIM_WEAK int pthread_mutex_lock(void *m) { (void)m; return 0; }
ZAN_SHIM_WEAK int pthread_mutex_unlock(void *m) { (void)m; return 0; }
ZAN_SHIM_WEAK unsigned long pthread_self(void) { return 1; }

ZAN_SHIM_WEAK char *getenv(const char *name) { (void)name; return NULL; }

/* ---- snprintf ABI wrapper ------------------------------------------- */

#ifdef ZAN_SHIM_HAVE_STDIO
int zan_w32_snprintf(char *s, long long n, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    int r = vsnprintf(s, (size_t)n, fmt, ap);
    va_end(ap);
    return r;
}
#else
/* rv32ilp32: long long is a register pair either way; forward by ABI */
int zan_w32_snprintf(char *s, long long n, const char *fmt, ...) {
    __builtin_va_list ap;
    __builtin_va_start(ap, fmt);
    int r = vsnprintf(s, (unsigned long)n, fmt, ap);
    __builtin_va_end(ap);
    return r;
}
#endif
