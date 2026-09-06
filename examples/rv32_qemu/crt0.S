/* crt0.S -- bare-metal entry for the zan rv32 kit (QEMU riscv32 'virt').
 *
 * Boots in M-mode with -bios none: paint the stack guard, clear .bss,
 * arm the trap vector, disarm the CLINT comparator (mtimecmp == 0 asserts
 * MTIP from boot), then enter the zan object's main. */

    .section .init.enter, "ax", @progbits
    .globl _start
_start:
    /* gp first: picolibc objects use gp-relative addressing */
.option push
.option norelax
    la   gp, __global_pointer$
.option pop
    la   sp, __stack_top

    /* guard-paint the whole stack region so exit() can report the
     * high-water mark */
    la   t0, __stack_bottom
    la   t1, __stack_top
    li   t2, 0xABABABAB
1:  bgeu t0, t1, 2f
    sw   t2, 0(t0)
    addi t0, t0, 4
    j    1b

    /* clear .bss */
2:  la   t0, __bss_start
    la   t1, __bss_end
3:  bgeu t0, t1, 4f
    sw   zero, 0(t0)
    addi t0, t0, 4
    j    3b

    /* trap vector + CLINT comparator disarm (write hi word first) */
4:  la   t0, zan_irq_timer
    csrw mtvec, t0
    li   t0, -1
    li   t1, 0x2004
    slli t1, t1, 12          /* mtimecmp @ 0x2004000 */
    sw   t0, 4(t1)
    sw   t0, 0(t1)

    /* picolibc startup: constructors bring stdio (stdout, ...) up */
    call __libc_init_array
    call main
    /* main returned: report usage and stop QEMU (exit lives in bsp.c) */
    call exit
5:  wfi
    j    5b

/* The only interrupt ever enabled is the machine timer (MTIE), so the
 * handler just pushes the comparator deadline to +infinity (clears MTIP)
 * and resumes. Poll() re-arms it for the next await. */
    .balign 4
    .globl zan_irq_timer
zan_irq_timer:
    addi sp, sp, -16
    sw   t0, 0(sp)
    sw   t1, 4(sp)
    li   t0, -1
    li   t1, 0x2004
    slli t1, t1, 12
    sw   t0, 4(t1)
    sw   t0, 0(t1)
    lw   t1, 4(sp)
    lw   t0, 0(sp)
    addi sp, sp, 16
    mret
