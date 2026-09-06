# rv32 裸机 QEMU 套件（体积 / 内存 / CPU 实测）

在 `qemu-system-riscv32 -M virt` 上把 `zanc --target riscv32` 的产物真正
**跑起来**的全套裸机件：M-mode `-bios none` 启动、UART 控制台、CLINT 定时器、
`Task.Delay` 真睡眠、退出时自动报告栈高水位并让 QEMU 自动结束。也是量化
Zan 裸机程序的体积 / 内存 / CPU 三项成本的标尺。

与 `examples/esp32_hello`（ESP-IDF 工程，上真机）互补：这里不需要 ESP-IDF，
只要一台装了 QEMU 的 Linux（或 WSL），就能验证 rv32 产物 + 裸机适配层的
行为与成本。

## 文件

| 文件 | 作用 |
|---|---|
| `hello.zan` | 被测程序：5 个 tick，`Task.Delay(1000)` 间隔，然后退出 |
| `crt0.S` | `_start`：装载 gp、卫兵涂写 32 KiB 栈、清 bss、装 mtvec、预清 CLINT 比较器，`__libc_init_array` 后进 `main`，返回即 `exit`；`zan_irq_timer` 只做"比较器推到 +∞"（清 MTIP） |
| `bsp.c` | 板级：NS16550A UART 控制台（picolibc tinystdio 不带 stdout 对象，这里用 `FDEV_SETUP_STREAM` 提供）；CLINT mtime 覆写 weak `zan_timer_now_ms`；`poll()` 装 mtimecmp + MTIE + `wfi`——定时器中断唤醒调度器；rv32imc 无 A 扩展，zan 对象引用的 4 个 `__atomic_*` 用关中断临界区实现；`exit()` 打印 `[zan] exit code` 与栈高水位，写 sifive_test finisher（PASS/FAIL）后 QEMU 自动退出 |
| `link.ld` | RAM @ 0x80000000（QEMU `-kernel` 的装载地址）；`.init_array` 保留给 picolibc stdio 构造器；栈区在 bss 之后（卫兵扫描报告用，不计入 bss） |
| `build.sh` / `run.sh` | 一键构建 / 运行 |

## 构建与运行

Ubuntu/Debian（或 Windows 上走 WSL，脚本对 `zanc.exe` 自动做 wslpath 转换）：

```bash
apt-get install -y gcc-riscv64-unknown-elf picolibc-riscv64-unknown-elf \
                   qemu-system-misc
ZANC=/path/to/zanc bash build.sh     # --publish --target riscv32 出 .o，再链成 ELF
bash run.sh                          # qemu-system-riscv32 -M virt -nographic -bios none -kernel …
```

预期输出（墙钟 ≈ 4.1 s，QEMU 自动退出，无需超时杀）：

```
tick 0
tick 1
tick 2
tick 3
tick 4

[zan] exit code: 0
[zan] stack high-water: 112 of 32768 bytes
```

## 实测数字（hello.zan，`--publish` = Os 体积优化）

| 维度 | 数值 | 说明 |
|---|---|---|
| **flash 载荷** | **4,608 B** | objcopy 二进制；Berkeley text 4,504 + data 96。libc/libgcc 侧大头是整数 printf 与 `__udivdi3`/`__umoddi3`（64 位除法） |
| **静态 RAM** | 65,632 B (bss) | 其中 **64 KiB 是垫片确定性堆池**（`-DZAN_BARE_HEAP_BYTES=` 可调，剩余静态仅 96 B）；对照 ESP32-C3 的 400 KiB SRAM |
| **栈** | 预留 32 KiB，**实测高水位 112 B** | crt0 用 `0xABABABAB` 涂满栈区，`exit()` 扫描第一个被覆盖的卫兵字，随程序复杂度增长、每次退出自动打印 |
| **CPU** | 墙钟 4.106 s（= 4×1 s 延时 + 启动），QEMU 进程主机 CPU ≈ 45 ms（≈1%） | `poll()` 用 mtimecmp+MTIE+`wfi` 睡眠，定时器中断唤醒——`Task.Delay` 不忙等；tick 精度即 CLINT mtime（10 MHz）精度 |

复测命令：

```bash
riscv64-unknown-elf-size build/zan_hello.elf          # text/data/bss
riscv64-unknown-elf-objcopy -O binary build/zan_hello.elf /tmp/z.bin && stat -c %s /tmp/z.bin
time bash run.sh                                       # 墙钟 + 主机 CPU（wfi 睡眠证据）
```

## 边界（照实说）

- **ISA**：QEMU virt 的核是 rv32imac，本套件按该多库链接；zanc 产物仍是
  rv32imc（ESP32-C3/C6 的无 FPU 核画像）。真机上用 ESP-IDF 工具链，见
  `examples/esp32_hello`。
- **libc**：picolibc（Ubuntu 无 newlib 包）。它的 tinystdio 归档不提供
  `stdout` 对象——由 `bsp.c` 提供控制台 FILE；printf 链的是整数版
  （浮点会换 vfprintf 变体并增大 text，属预期）。
- **原子**：只实现 hello 实际引用的 4 个（`__atomic_load_8` /
  `__atomic_fetch_add_8` / `__atomic_fetch_sub_8` / `__atomic_exchange_4`）。
  宽程序按 `examples/esp32_hello/README.md` 的符号契约表补齐（同款关中断
  临界区写法）。
- **单核单线程**：`ZAN_BARE_METAL` 的既定模型；poll/pthread 桩在
  `src/runtime/rt_bare_shim.c`（weak，可被板卡覆盖）。
