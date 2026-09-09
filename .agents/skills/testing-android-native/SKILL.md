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
- **gui_runtime 新增 DllImport 后 APK 全体秒退的定式**（踩坑：
  gui 3D 落地 zan_gui_mesh_create 后，7 个已装游戏全部
  `dlopen failed: cannot locate symbol` 秒退，Splash 一闪即回桌面）：
  libmain 把 stdlib/Gui 编进去，运行时 DLLImport 按符号从
  libzan_gui.a 解析；提交了 gui_runtime.c 新导出但没重跑 entry.sh
  时，drivers/android-<arch>/static/libzan_gui.a 还是旧符号表，
  zanc 照常出包（静态链接时缺符号只在 dlopen 才爆）。
  诊断一击必杀：`adb logcat -d | grep -E "LoadNativeLibrary|dlopen"`
  看 "cannot locate symbol X"，`nm -D libmain.so | grep "UND X"`
  确认引用，`nm libzan_gui.a | grep "T X"` 确认驱动缺定义；
  重跑 entry.sh 后用 `strings|grep`/`nm -D` 复核新 so 再装机。
  build/zanc 不重编 stdlib 的 Gui（Zan 源），但驱动 .a 是外部产物，
  任何 gui_runtime.c 改动都等于驱动改动——与 classes.dex 双处同步
  同级别的纪律。

## 游戏素材烘焙：APK 里 assets 从哪来（踩坑：7 个 APK 全部烘空成纯色块）

- `--publish`/`--emit-apk` 只在 **irgen.uses_embed_api**（代码里出现
  `zan_embed_*` DllImport）且 assets 候选存在时才自动嵌入
  `<proj>/assets/`；素材打进 `lib/arm64-v8a/libmain.so` 的嵌入表
  （zlib 压缩），验证：`unzip -p dist/<g>-arm64.apk
  lib/arm64-v8a/libmain.so | strings | grep -c "^assets/"`，
  计数应与模板 assets 目录文件数一一相符。
- **路径候选坑**：assets 候选含「输入源目录的父目录」
  （`<proj>/src` 的父 = `<proj>`，即 src/ 与 assets/ 并排布局）。
  为什么：从项目内以裸相对路径 `src/main.zan` 起编时
  resolve_package_project_root 会落到 `.`，看不见兄弟 assets/——
  不报错、不警告，APK 照常产出但素材为空，只有上机看到纯色块才
  暴露。所以构建必须从仓库根以路径前缀形式调用
  （`build/zanc.exe templates/game/<g>/src/main.zan --auto-stdlib
  --publish ...`），不要 cd 进模板目录再编。
- 运行期解码走 `zan_embed_rawlen`/`zan_embed_decode`
  （src/runtime/zan_inflate.c + vendored miniz，CMakeLists zan_inflate
  配方）；uses_inflate 由 `zan_embed_decode/rawlen` 引用触发链接。
- **新素材 git status 看不见的陷阱**：.gitignore 有全局 `*.png`
  （截图防误提交），模板素材 PNG 必须逐个显式 `git add <path>` 或
  在 .gitignore 加 `!templates/game/<g>/assets/**/*.png` 白名单——
  否则本地 APK 烘得好好的，仓库里素材缺失，别人重建即烘空。
- 素材回填配方：从原版 exe 的嵌入表逐字节提取（_scratch/dump_embed.py
  模式：定位嵌入表 → 解 zlib → 按 (名,数据) 落盘），比外部找图可靠
  （网上原图是未处理的 1024px 色键版，尺寸/抠图都与发行版不符）。

## 逐游戏截图验证纪律（踩坑：相邻两次 screencap 字节级相同，误判成渲染缺陷）

- **每次截图必须 md5 存档比对**。模拟器慢帧下 sleep 太短时，
  screencap 会拍到同一帧旧画面：曾出现 breakout/weiqi/xiangqi 三张
  截图 md5 完全相同、gomoku==snake（各自换了游戏拍的！），加长间隔
  重拍后 md5 全部互异——是截图竞速不是渲染 bug。
- 可靠节奏：`am force-stop <pkg>` → `am start -n <pkg>/
  android.app.NativeActivity` → `sleep 10` → `screencap` → 
  `force-stop`，一个游戏一轮，绝不批量连拍。md5 相同先怀疑竞速，
  换更长间隔重拍再下结论。
- 判定画面是否真的在贴图（而非纯色块兜底）：PIL 按画面横带切条算
  ImageStat stddev——有纹理的带 35-100+，纯色兜底块 stddev≈0；
  中带裁剪（`im.crop((0, h*0.20, w, h*0.80))`）缩放后人工复核。

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
