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

## 画面冻结排查定式（踩坑：40 分钟截图 md5 恒等，进程/EGL 全正常）

- **"画面冻在第一帧"先查整窗帧声明转发，再怀疑渲染**（2026-09
  3D demo 实锤）：进程活着、`app_time_stats` 每秒都在刷（eglSwapBuffers
  正常提交）、md5 却恒等。根因=`stdlib/Gui/Backend/Native.zan` 的
  `PresentFull()` 只有 `#if WINDOWS` 一臂，非 Windows 上 App.PresentFrame
  的整窗声明被静默丢成空操作，上传范围落到 shell 的脏矩形差分队列；
  修法=补 `#else zan_gui_present_full()`（OHOS/Android/X11/wasm 四后端
  均已导出：清空本帧排队矩形=整窗上传）。任何"声明性 API 只写了
  Windows 分支"都要当坑查一遍——不报错、不崩、只是永远不生效。
- **冻结≠死循环的判别三板斧**：①`logcat --pid=<pid> | grep -c
  app_time_stats` 持续增长=EGL 提交活着；②`/proc/<pid>/task/<tid>/stat`
  的 utime 两次采样在涨=线程在跑；③此时截图 md5 恒等=提交的帧内容
  不变——三者合起来把根因锁定在"上传/声明层"而不是渲染层。
- **帧计数走字是"循环活着"的最低标准，不是"画面在动"的证明**：
  数值收口用三帧像素差分（间隔 5s，`screencap`×3 后逐帧 abs 差分），
  修好后三张 md5 各异、帧间差分约 2 万像素且 8x6 分带矩阵显示变化
  集中在动画区（立方体）而非整屏噪声；修复前差分恒 0。
  视觉上暗色主题 + 线框 + 模拟器慢帧，肉眼根本看不出动没动。

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

## 鸿蒙 OHOS 侧验证（踩坑：__ANDROID__ 独守的块在 OHOS musl 里落进 fontconfig/Xlib）

- **OHOS 条件编译守卫丢失模式**：OHOS clang 预定义 `__OHOS__` 和
  `__linux__`，但**不**定义 `__ANDROID__`；且 OHOS musl sysroot 没有
  fontconfig/X11 头。凡 `#if defined(__ANDROID__)` 独守的块，在 OHOS
  编译时不跳过、落进 Linux 分支的 fontconfig/Xlib 代码，而头文件又被
  外层排除守卫挡掉 → 20+ 编译错一齐爆。修法=逐处补
  `|| defined(__OHOS__)` / `&& !defined(__OHOS__)`（gui_runtime 的
  font.c 字体探测 /tray.c/gl_context.c 三处实锤），顺手把
  `/system/fonts/HarmonyOS_Sans.ttf` 放进 prim_paths 首位（OHOS 设备
  字体布局与 Android 同构：/system/etc/fonts.xml + /system/fonts）。
  证据链收口：llvm-nm 看驱动 —— 旧 .a `grep -E " U (Fc|X)"` 零引用
  =旧驱动根本没编那段代码；新 .a 里 `T zan_gui_draw3d`/
  `T zan_gui_present_full` 等新导出在位才算重编成功。
- **DevEco Emulator 必须 CLI 启停**（踩坑：双击图标与
  `Start-Process -ArgumentList` 都静默失败，不报错也不启动）：
  `powershell "& 'C:\Program Files\Huawei\DevEco Studio\tools\emulator\Emulator.exe' -start 'MateBook Pro'"`
  成功；`-list` 列实例（Mate X7/MateBook Pro/MatePad Pro 13/Pura 90
  Pro/Pura X View），`-stop '<实例名>'` 停止。hdc 在
  `.../sdk/default/openharmony/toolchains/hdc.exe`，目标 127.0.0.1:5555。
- **hdc file recv 用 cwd 相对路径**（Git Bash）：绝对 POSIX 路径
  `/data/...` 会被改写成 `C:/Program Files/Git/data/...`；recv 目标
  写 `oh1-3.jpeg` 这类相对名即可。
- **hilog 探针**：`hilog -r`（清日志）在 Git Bash 管道里挂死——避免，
  用 `hilog -x | grep`。"EGL 提交活着"的探针=DGLES 的
  `d_eglSwapBuffers_special` 持续 ~1 条/秒（OHOS 版 app_time_stats）。
- **HAP 跨模拟器重启持久免重装**：模拟器重启后 com.zan.hapshell 仍在。
  冷启定式：`hdc shell "aa force-stop com.zan.hapshell"` → `aa start`
  → 等 ~20s → `pidof` 确认 + isForeground。画面冻结判别沿用三板斧
  （hilog 提交探针 + 进程存活 + 三帧截图 md5 互异 + PIL 像素差分），
  但 2in1 模拟器（MateBook Pro，3120x2080@dpi304）应用是浮动窗口
  （约 515..2604 x 351..2048），先按窗口裁剪再差分/判读，整屏差分会
  混进桌面噪声。
- **OHOS 2in1 窗口 resize 三环链**（2026-09-11，gui_3d_demo snap 最大化
  黑带实锤）：2in1（MateBook Pro）拖拽/最大化**不销毁重建** XComponent
  surface，三处必须都在位，缺一环画面就停在旧尺寸：
  ①壳 `OnSurfaceChanged` 查 `OH_NativeXComponent_GetXComponentSize` 后
  **必须转发 attach**（只记日志不转发=驱动永远不知道窗口变了）；
  ②驱动 present 的重建判据必须认**同指针尺寸变化**：只比 `surf_nw != nw`
  （旋转用）在 2in1 resize 下永不触发——struct 记 surf_w/surf_h，
  指针或尺寸任一不符即销毁重建 EGL surface；
  ③**记账必须记实际值，不是预期值**：snap 最大化是单次大尺寸跳变
  （2090→3120），重建瞬间原生窗口 buffer geometry 可能未落定，
  `eglCreateWindowSurface` 实际拿到旧尺寸 surface；若记账记 attach 的
  预期值 w->w，账面"吻合"永不再重建、黑带永驻（连续小尺寸拖拽因最后
  一次事件在 geometry 落定后到来而侥幸全对，极具迷惑性）。修法=
  创建后 `eglQuerySurface(EGL_WIDTH/HEIGHT)` 记实际值，落定竞态由
  下一帧判据自愈。**验证仪式**：`uitest uiInput drag <标题栏x> 355
  <标题栏x> 5` 触发 snap 最大化（点系统 caption 按钮无效），
  `hidumper -s WindowManagerService -a '-a'` 看窗口 rect，
  hilog 等 "surface changed"，snapshot 后收紧深藏青区间判读
  （宽松区间会把合成器黑边当内容）；还原=从顶边 drag 回下方。
- **OHOS/Android 3D 性能定性**（用户问"复杂动画是否 CPU GPU 内存爆表"）：
  `gui_gl_context.c` 平台臂只有 WGL/GLX/Metal，Android/OHOS 落 #else
  空 stub——GPU 后端永不安装，3D=CPU 软件光栅 + 每帧整幅上传
  （2090x1324 约 11 MB/帧，60fps 即 0.7 GB/s 带宽）。模拟器实测：
  应用 ~35% 单核 + render_service ~63%，PSS 98 MB 不涨，帧 median 15ms。
  GPU 臂缺失已挂 TASKS.md A267，另案补 EGL 臂。
