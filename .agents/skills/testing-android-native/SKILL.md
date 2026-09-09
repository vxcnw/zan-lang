---
name: testing-android-native
description: Zan GUI 的 Android NativeActivity 实机验证仪式——probe APK 构建（zanc --emit-apk 的 driver/dex 来源）、Gboard 拼音/emoji/组词全链路驱动、模拟器慢帧节奏。凡是要在 Android 模拟器上验证 stdlib/Gui 或 gui_runtime 改动（输入法、字体、触控、渲染）、排查"改动静默不生效/屏幕不刷新"时使用。
---

# Android NativeActivity 实机验证（Zan GUI）

## 构建链路：产物从哪来（踩坑：改了代码，APK 里跑的还是旧的）

- `zanc --emit-apk` 从 **`--stdlib-path` 指定的 stdlib 目录**下解析
  `Gui/drivers/android-<arch>/static/libzan_gui.a`，不是仓库 stdlib。
  用 scratch 副本（`_scratch/gallery-demo-stdlib`）编译 probe 时，重编
  驱动后必须把新 `.a` 也拷进 scratch 副本的 drivers 目录。
  为什么：entry.sh 只 staged 到仓库 `stdlib/Gui/drivers/`；一次遗漏就是
  "符号在、日志无、新逻辑全部静默失效"——APK 能编过，因为旧 `.a` 里
  符号也在，只有内容是旧的。验证手段：解包 APK 里的 libmain.so，
  `grep -a "新增日志字符串"`，搜不到就是链路错了。
- classes.dex 同理双处同步：`toolchain/apk-shell/`（提交用）和
  `build/apk-shell/`（zanc 从 **exe 同目录**的 apk-shell 读，main.c
  硬编码 `<zanc.exe dir>/apk-shell`）。dex 重编要一次编译全部三个
  Java 源（ZanApp + ZanIme + ZanWeb），只编一个出的小 dex 装上就
  "Failed to register native method"。
- 驱动重建：`_scratch/anw/entry.sh`（两个 ABI，gui_runtime.c +
  freetype 合并成 libzan_gui.a）。改了 `src/runtime/gui_runtime*.c`
  后必须重跑，再同步 scratch，再重打 APK。

## 事件契约：绕过事件环的状态变化必须推 kind-14（踩坑：屏幕永不刷新）

- App.RunLoop 空闲时阻塞在 WaitEvent；IME 组合期间按键全被输入法
  消费，事件环上一个事件都没有。任何"native 缓冲态"（组词预览、
  剪贴板回读等）变化后，必须 `aq_push_locked(14, ...)` 唤醒重绘，
  否则 Zan 层永远读不到新值——不是崩溃，是"输入了但界面纹丝不动"。
- 诊断顺序：先看屏幕上的帧计数（probe 自画 frames），分清"循环死了"
  还是"循环活着但没事件"；再看 logcat（`-s ZanIme zanShell`）。JNI
  侧 RegisterNatives 绑定结果、写入/读出两端都要留一次性日志。

## 实机驱动（Gboard 全链路）

- adb 在 `C:\Users\QQ\AppData\Local\Android\Sdk\platform-tools\adb.exe`；
  probe 包名 `dev.zan.probe2`，activity `android.app.NativeActivity`。
- 模拟器约 0.4-1fps：每次交互（tap/swipe/截图）间隔 4-6 秒，判定前
  多等几秒再截图，别把旧帧当结果。
- **模拟器截屏会拍到壁纸/启动器的"假游戏帧"**（踩坑：金色高亮全无、
  四色签名几乎全零）：桌面被 Home 回退后 Launcher 挡在最上，screencap
  拍的是壁纸，不是游戏。判定渲染前先 `dumpsys window | grep
  mCurrentFocus` 确认游戏窗口在前台、`pidof` 确认进程活着——APK 装上
  ≠能启动，`am start` 后必须 `pidof` 复核（v3 APK dlopen 缺符号秒退，
  桌面全绿毫无征兆；`logcat -d | grep LoadNativeLibrary` 看真实死因）。
- **截图视觉判断不可靠时用数值扫描收口**：PowerShell LockBits
  Format24bppRgb 按已知绘制色签名扫描（灯/绳/钢的 RGB ±容差），数
  像素数与质心、跨帧对比。竖屏构图 x/y 要按真实方向读——screencap
  竖屏回 1080x2400，扫描循环 y 走到 h、x 走到 w 别写反。坑出处：
  三帧"看起来一样"实为一帧渲染重复，视觉无法分辨伸/收；绳像素的
  spanY 跨伸→收从 310→1075 一眼定案。
- 截图 1080x2400 原生分辨率，Read 显示约 880 宽——显示坐标 ×1.2273
  才是 `input tap` 的原生坐标。算错两次打错键的教训：打字前先截一张
  键盘图，按当前布局算键位。
- 拼音链路：Input 聚焦 → Gboard 悬浮条上**长按**语言键（单点是切换
  中英文）→ 菜单"显示屏幕键盘"→ 打拼音 → 点候选词上屏。Gboard 的
  "Inline composing"（设置→语言→中文(简体)）默认关，不开就不调
  setComposingText，组词链路无从谈起——先查这个开关。
- 验证收口看三处：probe 屏幕上的状态行（text/composing 读出）、
  输入框内渲染、logcat commit/store 日志；三者一致才算过。
