# aardio 能力迁移到 Zan 标准库 — 分析与任务清单

分析对象：`D:\aardio\lib`（840 个 `.aardio` 文件，48 个顶层库）与 `D:\aardio\tools`。
对照对象：`d:\project\zan-lang\stdlib`（`System/*`、`Gui/*`、`Platform/Runtime.zan`）。

本文只做「该迁什么、迁成什么样、按什么顺序」的规划，不含实现代码，供分派给其他智能体逐项落地。

---

## 1. 现状盘点

### Zan 已具备（不需要迁移，只可能补细节）

| 能力域 | Zan 现有位置 |
| --- | --- |
| 文件/目录/流 | `System/IO/*`（File、Directory、Path、FileStream、MemoryStream、StreamReader/Writer、ByteBuffer） |
| 进程启动/管道 | `System/Diagnostics/Process.zan`（popen、CreateProcess、RunCapture、RunDetached） |
| 网络 | `System/Net/*`（Sockets、Http、Https、WebSocket、Mqtt、Modbus、Ntp、Rpc、Sip、Coap、Tls、Sse） |
| 数据库 | `System/Data/*`（Sqlite、MySql、Postgres、SqlServer、Firebird、TDengine、Redis、Orm、ZanDb） |
| 加密/编码 | `System/Security/Cryptography/*`（AES、RSA、SM2/3/4、SHA、MD5、HMAC、HKDF、Base64、Hex、BigInt） |
| JSON / 正则 / 编码 | `System/Json/*`、`System/Text/RegularExpressions/*`、`System/Text/Encoding.zan` |
| 线程/并发 | `System/Threading/*`（Gate、AsyncGate、AsyncRwLock） |
| GUI 框架与绘图 | `Gui/*`（自绘控件体系、Skin、Layout、Render、Chart、CodeEditor、DataTable、WebView） |
| Windows 窗口消息层 | `Gui/Backend/Win32Shell.zan`（窗口创建、消息循环、剪贴板文本、拖放） |
| Web 服务端 | `System/Web/*`（Router、Controller、View、WebApp/WebHost） |

### Zan 明显缺失（aardio 有成熟实现）

- **输入模拟**：鼠标/键盘发送、组合键、坐标移动轨迹。
- **全局钩子与热键**：`WH_KEYBOARD_LL` / `WH_MOUSE_LL`、系统热键、按键串（key macro）。
- **系统与硬件信息**：CPU（CPUID/主频/厂商）、内存、磁盘/卷、显示器与分辨率、电源、计算机名/用户名、已安装软件、设备管理。
- **注册表**：读写、枚举、删除、Wow64 重定向。
- **窗口自动化**：查找/等待/枚举窗口与控件、取文本、点击控件、菜单、置顶/前台、坐标换算。
- **UI 自动化（无障碍）**：IAccessible / UIAutomation 元素查找与操作。
- **剪贴板扩展**：文件列表、位图/PNG、HTML/RTF 格式，格式枚举与监听。
- **托盘图标与气泡通知**。
- **屏幕相关**：截屏、区域选取、取色、多显示器信息、DPI。
- **进程增强**：枚举、CPU/内存占用、挂起/恢复/终止、提权运行（runas）、令牌与 SID、句柄与模块枚举。
- **服务 / 计划任务**。
- **文件系统增强**：目录变更监听、INI、快捷方式(lnk)、已知文件夹、驱动器信息、内存映射、路径与 glob、mime、硬链接/junction。
- **压缩**：zip / 7z / tar / gzip。
- **实用字符串/表工具**：CSV、UUID、模板、文本表格、拼音、模糊匹配、命令行解析、glob。
- **时间**：高精度计时、定时器、农历/节气、时区、NTP（NTP 已有）。

---

## 2. 迁移原则

1. **语义照原版，写法归 Zan**。aardio 源码只当 API 清单与行为规格用，实现一律用 Zan 的现有能力写（标准库集合/字符串/线程/`async`、强类型类、`#if` 平台分支），禁止逐行直译 aardio 的表驱动、全局函数、弱类型传值风格——直译等于把旧语言的形状整体搬进来，之后每个模块都顺着旧形状继续长歪。下文的「不移植 aardio 运行时」「命名对齐 .NET」「强类型化」都是这条的具体化。
2. **走 DllImport 直连 Win32，不移植 aardio 运行时**。Zan 已支持 `[DllImport("user32", EntryPoint="...")]`（见 `Gui/Backend/Win32Shell.zan`、`System/Diagnostics/Process.zan`），aardio 的 `::User32.xxx` 调用可以一对一映射。
3. **公共 API 跨平台，实现按平台分支**。用 `#if WINDOWS / #elif MACOS / #else` 分支（`Platform/Runtime.zan` 已是这个写法）。Windows 先落地，Linux/macOS 至少给出可编译的空实现或 X11/AppKit 实现，不要让接口只在 Windows 存在。
4. **命名空间对齐 .NET 风格**，与现有 `System.*` 保持一致，不照搬 aardio 的小写命名：
   - `System.Input.Mouse` / `System.Input.Keyboard` / `System.Input.Hotkey` / `System.Input.Hook`
   - `System.Management.SystemInfo` / `Cpu` / `Memory` / `Storage` / `Display` / `Power` / `Battery`
   - `System.Management.Registry`（Windows）
   - `System.Diagnostics.ProcessList` / `ProcessUsage` / `Privileges`
   - `System.Automation.Window` / `UiElement`（窗口与 UI 自动化）
   - `System.Windows.Clipboard` / `System.Windows.TrayIcon` / `System.Windows.Screen`
   - `System.IO.Compression.*`、`System.IO.DirectoryWatcher`、`System.IO.IniFile`、`System.IO.Shortcut`
5. **结构体用类 + 显式字段**，返回值用强类型对象（如 `MemoryStatus`、`MonitorInfo`、`ProcessEntry`），不要返回字符串或字典 —— 仓库规范禁止 `Any`/动态取属性。
6. **每个模块配一个 `tests/` 用例和 `examples/` 最小示例**，可自动跑的（信息读取类）优先做断言，需交互的（钩子、热键）做手动示例。
7. **不迁**：aardio 的 COM/`dotNet`/`java`/`golang`/`nodeJs` 互操作层、`web/layout` 的 HTML UI 体系、`ide/*`（aardio IDE 自身）、`autos/skills`（Office/PS 自动化，依赖 COM）、`protobuf`/`bencode` 等小众协议。这些要么与 Zan 自绘 GUI 路线冲突，要么投入产出比低，需要时再单独立项。

---

## 3. 迁移清单（按优先级分批）

难度：S = 半天内，M = 1~2 天，L = 3 天以上。

### 进度总览（2026-08 更新）

已完成并带 conformance 测试/示例的条目：

| # | 模块 | 落地位置 | 测试 |
| --- | --- | --- | --- |
| 1+2 | `System.Input.Mouse` / `Keyboard` | `stdlib/System/Input/{Mouse,Keyboard}.zan` | `input_*_smoke` |
| 3 | `System.Input.Hook` | `stdlib/System/Input/Hook.zan` | `input_hook_smoke` |
| 4 | `System.Input.Hotkey` | `stdlib/System/Input/Hotkey.zan` | `input_hotkey_smoke` |
| 5~10 | `System.Management` 信息族 | `stdlib/System/Management/{Cpu,Memory,SystemInfo,Storage,Display,Power}.zan` | `sysinfo_smoke` |
| 11 | `System.Management.Registry` | `stdlib/System/Management/Registry.zan` | `registry_roundtrip` |
| 14 | `System.Diagnostics.ProcessList` | `stdlib/System/Diagnostics/ProcessList.zan` | `process_list_smoke` |
| 15+16 | `Privileges` / `ProcessControl` | `stdlib/System/Diagnostics/{Privileges,ProcessControl}.zan` | `process_control_smoke` |
| 18+19 | `System.Windows.TrayIcon` / `Screen` | `stdlib/System/Windows/{TrayIcon,Screen}.zan` | `win_tray_screen_smoke` |
| 20 | `System.ServiceProcess` | `stdlib/System/ServiceProcess/ServiceProcess.zan` | `win_serviceprocess_smoke` |
| 21 | `System.Management.TaskScheduler` | `stdlib/System/Management/TaskScheduler.zan` | `win_taskscheduler_smoke` |
| 12 | `System.Automation.Window` | `stdlib/System/Automation/Window.zan` | `win_automation_smoke` |
| 13 | `System.Automation.UiElement` | `stdlib/System/Automation/UiElement.zan` | `win_uielement_smoke` |
| 23 | `System.IO.Compression` | `stdlib/System/IO/Compression/{Deflate,Crc32,GZip,Zip,Tar}.zan` | `win_compression_smoke` |
| 33 | `System.Guid` | `stdlib/System/Guid.zan` | `guid_*` |
| 36 | `Stopwatch` | `stdlib/System/Stopwatch.zan`（2026-08-27 从 `Diagnostics/` 移到根命名空间，见 TASKS A56） | `stopwatch_*` |
| 37 | `System.Globalization.Lunar` | `stdlib/System/Globalization/Lunar.zan` | `lunar_*` |
| 17 | `System.Windows.Clipboard` | `stdlib/System/Windows/Clipboard/Clipboard.zan` | `clipboard_roundtrip` |
| 22 | `System.IO.Watch.DirectoryWatcher` | `stdlib/System/IO/Watch/DirectoryWatcher.zan`（2026-08-27 独立命名空间，见 TASKS A56） | `dir_watcher` |
| 24~29 | `System.IO` 实用工具 | `stdlib/System/IO/{IniFile,Shortcut,KnownFolders,PathEx,FileInfoEx,MemoryMappedFile}.zan` | `ini_csv_roundtrip` / `shortcut_roundtrip` / `known_folders` / `path_ex` / `fileinfoex_mmap` |
| 30~32 | `Csv` / `Template` / `TextTable` | `stdlib/System/Text/{Csv,Template,TextTable}.zan` | `ini_csv_roundtrip` / `text_template` |
| 34+35 | `Pinyin` / `FuzzyMatching` / `Bm25Index` | `stdlib/System/Text/{Pinyin,FuzzyMatching,Bm25Index}.zan` | `tryget_pinyin` / `fuzzy_bm25` |
| 可选 | `Ping` / `NetworkInterface` | `stdlib/System/Net/{Ping,NetworkInterface}.zan` | `win_ping_network` |
| 可选 | `System.Drawing.Printing` / `System.Management.Device` | `stdlib/System/Drawing/Printing/Printing.zan` / `stdlib/System/Management/Device.zan` | `win_printing_smoke` / `win_device_smoke` |
| 可选 | `Otp` / `Jwt` | `stdlib/System/Security/Cryptography/{Otp,Jwt}.zan` | `otp_vectors` / `jwt_hs256` / `jwt_rs256` |
| 可选 | `System.Net.WebDav` / `System.Text.Markdown` | `stdlib/System/Net/WebDav/WebDavClient.zan` / `stdlib/System/Text/Markdown.zan` | `webdav_parse` / `markdown_parse` |

实现要点（记录在案，供后续条目复用）：

- **命令封装策略**：`ServiceProcess` / `TaskScheduler` 走 `sc.exe` / `schtasks.exe`
  文本输出而非原始 SCM COM 枚举——SCM 的 `EnumServicesStatusExW` 缓冲区布局在
  64 位系统上版本敏感（实测 301 条里有 215 条指针错位），文本接口稳定且免管理员。
- **输出编码归一**：`Process.WinCapture` 现在自动识别 UTF-16LE BOM 与 ANSI/GBK
  （`schtasks` 重定向输出 UTF-16、`sc` 输出 GBK），统一转 UTF-8 再 `SplitLines`。
  中英文系统字段名都解析（如 `Task To Run:` / `要运行的任务:`）。
- **TrayIcon 自包含**：自带隐藏宿主窗口 + 独立线程消息循环，不依赖 Gui 框架；
  任务栏重建（`TaskbarCreated`）后自动重挂图标。
- **Screen 取色走 BitBlt**：GDI `GetPixel` 在 DWM 合成桌面不可靠，1x1 BitBlt 一致。
- **Compression 纯手写**：`Deflate` 是 RFC 1951 完整实现（fixed + dynamic Huffman、
  stored block、LZ77 哈希链），不依赖 zlib；`Crc32` 查表法；`GZip`(RFC 1952)、
  `Zip`(PKZIP stored/deflate + 中央目录)、`Tar`(POSIX ustar 长路径 prefix) 均与
  Python zipfile/tarfile/gzip、.NET、Info-ZIP 双向互操作验证过。Huffman 码按
  RFC 1951 要求 MSB-first 打包（`WriteBitsMsb`），extra 位 LSB-first。
- **Window 自动化直连 Win32**：`Window` 覆盖 winex 的查找/等待/文本/菜单/坐标/
  样式/状态/进程线程全套，全部走 `user32` 直调；跨进程读文本用
  `SendMessageTimeoutW`+`SMTO_ABORTIFHUNG`（无响应返回空串不卡调用方）；
  `ClickMenu` 按 `File/Open` 路径逐级 `GetSubMenu`+`GetMenuStringW` 匹配后
  `PostMessage(WM_COMMAND)`；conformance 自建弹窗+子控件+菜单全量断言。
- **非 Windows 分支**：所有模块 `#else` 抛 `PlatformNotSupportedException`。

### P0 — 用户明确要的：输入模拟 + 系统信息

| # | 目标 Zan 模块 | aardio 来源 | 需覆盖的 API | 依赖 | 难度 |
| --- | --- | --- | --- | --- | --- |
| 1 | `System.Input.Mouse` | `mouse\_.aardio` | `GetPos/SetPos`、`Move/MoveTo(带步进轨迹)`、`Down/Up/Click/DoubleClick`（左中右）、`Drag`、`Wheel`、`State`、`MoveToWindow`（窗口相对坐标） | `user32!SendInput`、`GetCursorPos`、`GetSystemMetrics` | M |
| 2 | `System.Input.Keyboard` | `key\_.aardio`、`key\VK.aardio` | `Send(字符串宏，如 "{Ctrl}{C}")`、`SendText(Unicode 直发)`、`Press/Down/Up/Repeat`、`Combine`、`GetState/SetState`、`CapsLock/NumLock/ScrollLock`、`VK 名称<->码`、`Block(屏蔽输入)`、`WaitUp/Wait` | `user32!SendInput`、`MapVirtualKey`、`GetKeyState` | M |
| 3 | `System.Input.Hook` | `key\hook.aardio`、`mouse\hook.aardio` | 低级键鼠钩子：安装/卸载、回调（vk、scancode、是否注入、时间戳）、回调返回值可吞掉事件 | `SetWindowsHookEx(WH_KEYBOARD_LL/WH_MOUSE_LL)`、需消息循环 | L |
| 4 | `System.Input.Hotkey` | `key\hotkey\_.aardio` | 注册全局热键（组合键与按键串两种）、注销、冲突检测、从配置表批量加载 | `RegisterHotKey` 或基于 #3 的钩子 | M |
| 5 | `System.Management.Cpu` | `sys\cpu.aardio` | `Vendor/Brand/Frequency/Isa`（CPUID）、逻辑核数、用量百分比 | CPUID 内联或 `GetSystemInfo` + `NtQuerySystemInformation` | M |
| 6 | `System.Management.Memory` | `sys\mem.aardio` | `GetStatus()` → 物理/虚拟/页面文件 总量·可用·占用率 | `kernel32!GlobalMemoryStatusEx` | S |
| 7 | `System.Management.SystemInfo` | `sys\_.aardio`、`sys\info.aardio`、`win\version.aardio` | 计算机名/用户名、开机时间与运行时长、OS 版本与位数、`IsX64`、锁屏/注销/关机/重启/休眠 | `kernel32`、`advapi32`、`user32!ExitWindowsEx` | S |
| 8 | `System.Management.Storage` | `sys\volume.aardio`、`sys\storage.aardio`、`fsys\drives.aardio` | 驱动器枚举与类型、卷标、总量/可用空间、物理设备与是否 USB | `GetLogicalDrives`、`GetDiskFreeSpaceEx`、`DeviceIoControl` | M |
| 9 | `System.Management.Display` | `sys\monitor.aardio`、`sys\display.aardio` | 多显示器枚举（工作区/分辨率/主屏/DPI）、按窗口或坐标取所在显示器、分辨率切换 | `EnumDisplayMonitors`、`GetMonitorInfo`、`ChangeDisplaySettingsEx`、`GetDpiForMonitor` | M |
| 10 | `System.Management.Power` | `sys\power\_.aardio` | 电池状态与剩余电量、交流/电池、电源方案查询与切换、屏幕超时设置 | `GetSystemPowerStatus`、`powrprof` | S |

### P1 — 自动化与系统集成

| # | 目标 Zan 模块 | aardio 来源 | 需覆盖的 API | 难度 |
| --- | --- | --- | --- | --- |
| 11 | `System.Management.Registry` | `win\reg.aardio`、`sys\reg.aardio`、`util\registry.aardio` | 打开/创建/删除键、枚举子键与值、各类型值读写（DWORD/QWORD/SZ/EXPAND_SZ/MULTI_SZ/BINARY）、递归删除、Wow64 视图、导入导出 | M |
| 12 | `System.Automation.Window` | `winex\_.aardio`、`win\_.aardio` | 枚举/查找/等待窗口与子控件（类名+标题+ID 多条件、超时）、取/设文本、点击控件与菜单、显示/隐藏/置顶/前台/最大化、坐标与客户区换算、进程与线程 ID、是否无响应 | L |
| 13 | `System.Automation.UiElement` | `winex\accObject\*`、`System\Windows\Automation\*` | 从窗口/坐标取无障碍元素、遍历子元素、按条件查找、取名称/角色/值/矩形、Invoke/Select/SetValue | L |
| 14 | `System.Diagnostics.ProcessList` | `process\list.aardio`、`process\wmi.aardio`、`process\usage.aardio` | 枚举进程（PID/名称/路径/父进程/内存/线程数）、按名称或 PID 查找、CPU 与内存占用采样、模块与线程枚举 | M |
| 15 | `System.Diagnostics.Privileges` | `process\admin.aardio`、`process\token.aardio` | 是否管理员、UAC 提权运行（runas，可等待退出码）、降权运行、令牌用户与 SID、启用特权 | M |
| 16 | `System.Diagnostics.ProcessControl` | `process\_.aardio` 子集 | 挂起/恢复/终止、等待退出、优先级、亲和性、Job 对象随父进程退出、等待主窗口 | M |
| 17 | `System.Windows.Clipboard` | `win\clip\*` | 在现有文本剪贴板基础上补：文件列表、位图/PNG、HTML、RTF、格式枚举、清空、变更监听 | M |
| 18 | `System.Windows.TrayIcon` | `win\util\tray.aardio` | 托盘图标增删改、气泡通知、左右键与双击回调、任务栏重建自恢复 | M |
| 19 | `System.Windows.Screen` | `win\clip\screen.aardio`、`mouse\screenArea.aardio`、`gdip\snap.aardio` | 全屏/窗口/区域截图到位图或文件、交互式框选区域、屏幕取色 | M |
| 20 | `System.ServiceProcess` | `service\_.aardio` | 服务枚举、状态查询、启停、安装/卸载 | M |
| 21 | `System.Management.TaskScheduler` | `win\taskScheduler.aardio` | 计划任务创建/删除/查询（开机自启、定时运行） | M |

### P2 — 文件系统、压缩与实用工具

| # | 目标 Zan 模块 | aardio 来源 | 需覆盖的 API | 难度 |
| --- | --- | --- | --- | --- |
| 22 | `System.IO.DirectoryWatcher` | `fsys\dirWatcher.aardio`、`fsys\watch.aardio` | 目录变更监听（增删改名、递归、过滤），回调或异步迭代 | M |
| 23 | `System.IO.Compression` | `zlib\zip/unzip`、`sevenZip\lzma\*`、`fsys\tar.aardio` | zip 压缩/解压（含目录与密码）、gzip 流、tar、7z（可后置） | L |
| 24 | `System.IO.IniFile` | `fsys\ini.aardio`、`string\ini.aardio` | INI 读写、节与键枚举、内存 INI | S |
| 25 | `System.IO.Shortcut` | `fsys\lnk.aardio`、`fsys\shortcut.aardio` | 创建/解析 .lnk（目标、参数、工作目录、图标） | S |
| 26 | `System.IO.KnownFolders` | `fsys\knownFolder.aardio`、`fsys\environment.aardio` | 桌面/文档/AppData/临时目录等已知路径、环境变量读写与展开 | S |
| 27 | `System.IO.PathEx` | `fsys\path.aardio`、`fsys\safepath.aardio`、`string\glob.aardio` | 路径规范化、相对/绝对互转、安全路径校验、glob 匹配与递归枚举 | S |
| 28 | `System.IO.FileInfoEx` | `fsys\fileInfo.aardio`、`fsys\version.aardio`、`fsys\mime.aardio` | 文件版本信息、图标提取、MIME 猜测、时间戳读写、硬链接/junction | M |
| 29 | `System.IO.MemoryMappedFile` | `fsys\mmap\_.aardio` | 内存映射读写与跨进程共享 | M |
| 30 | `System.Text.Csv` | `string\csv.aardio` | CSV 读写（引号转义、自定义分隔符、表头映射） | S |
| 31 | `System.Text.Template` | `string\template.aardio` | 简单模板替换（与 `System/Web/View` 打通） | S |
| 32 | `System.Text.TextTable` | `string\textTable.aardio`、`console\table.aardio` | 控制台表格对齐输出（CLI 工具会常用） | S |
| 33 | `System.Guid` | `string\uuid.aardio`、`win\guid.aardio` | UUID v4/v7 生成与解析、GUID 字符串互转 | S |
| 34 | `System.Text.Pinyin` | `string\conv\pinyin.aardio` | 汉字转拼音/首字母（IDE 搜索、排序会用到） | M |
| 35 | `System.Text.FuzzyMatching` | `string\fuzzyMatching.aardio`、`string\bm25.aardio` | 模糊匹配打分、BM25（IDE 文件与符号搜索直接受益） | M |
| 36 | `System.Diagnostics.Stopwatch` + `System.Threading.Timer` | `time\performance.aardio`、`time\timer.aardio` | 高精度计时（QueryPerformanceCounter）、周期定时器 | S |
| 37 | `System.Globalization.Lunar` | `time\lunar.aardio`、`time\ganzhi.aardio`、`time\festival.aardio` | 农历、干支、节气、节假日（国内业务常用） | M |

### 可选 / 低优先（已完成）

- `icmp\ping.aardio` → `System.Net.Ping`；`inet\adapter.aardio` → `System.Net.NetworkInterface`。
- `sys\printer.aardio` → `System.Drawing.Printing`（枚举、默认打印机、RAW 文档）。
- `sys\device.aardio` → `System.Management.Device`（SetupAPI 只读枚举）。
- `crypt\otp.aardio` → `System.Security.Cryptography.Otp`（RFC 4226/6238）。
- `crypt\jwt/jws/jwk` → `System.Security.Cryptography.Jwt`（HS256/RS256、claims 校验）。
- `web\dav\*` → `System.Net.WebDav` 客户端（PROPFIND/MKCOL/GET/PUT/DELETE/COPY/MOVE）。
- `string\markdown\_.aardio` → `System.Text.Markdown`（安全紧凑 HTML 输出）。

---

## 4. 建议的任务拆分方式

给其他智能体分派时，按下面粒度切，一个任务一个 PR：

1. **任务 1**：`System.Input.Mouse` + `System.Input.Keyboard`（清单 1、2）。这两个共用 `INPUT` 结构与 `SendInput`，必须一起做。
2. **任务 2**：`System.Input.Hook` + `System.Input.Hotkey`（3、4）。依赖任务 1 的 VK 表。
3. **任务 3**：`System.Management` 信息族（5~10）。彼此独立、可并行内部完成，接口风格要统一。
4. **任务 4**：`System.Management.Registry`（11）。独立。
5. **任务 5**：`System.Automation.Window`（12）。独立，体量最大。
6. **任务 6**：`System.Automation.UiElement`（13）。依赖任务 5 的窗口句柄类型。
7. **任务 7**：进程族（14~16）。基于现有 `System/Diagnostics/Process.zan` 扩展，不要另起炉灶。
8. **任务 8**：`Clipboard` + `TrayIcon` + `Screen`（17~19）。都要和 `Gui/Backend/Win32Shell.zan` 的窗口与消息循环协作，放一起避免冲突。
9. **任务 9**：文件系统族（22、24~29）。
10. **任务 10**：压缩（23）。单独，因为要引入或实现 deflate/lzma。
11. **任务 11**：文本工具族（30~35）。纯算法，最容易并行，也最适合新手智能体。
12. **任务 12**：时间族（36、37）。

### 每个任务的验收要求

- 公共 API 有 `///` 文档注释，命名与 `System.*` 现有风格一致。
- 非 Windows 平台可编译（用 `#if` 分支，未实现的抛明确异常而不是静默返回错误值）。
- `tests/` 下有可自动运行的用例（信息读取类断言字段非空且合理；交互类给 `examples/` 手动示例）。
- 结构化返回值用类，不用字符串拼装。
- 通过 `scripts/build_ide.ps1`（或对应构建脚本）编译。

---

## 5. 风险与注意事项

- **钩子与热键需要消息循环**：`SetWindowsHookEx` 的低级钩子回调在安装线程的消息队列上派发，Zan 侧要么复用 `Gui/Backend/Win32Shell.zan` 的循环，要么起独立线程跑自己的 `GetMessage` 循环，这一点要在任务 2 里先定方案再写代码。
- **回调函数指针**：多个模块（钩子、`EnumWindows`、`EnumDisplayMonitors`、目录监听）都需要把 Zan 函数作为 C 回调传出去。先确认 Zan 当前对回调/函数指针的支持程度，如果不支持，需要在运行时（`src/runtime`）补一层 trampoline —— 这是整批迁移最大的技术前置项，建议**先做一个最小验证**（用 `EnumWindows` 打通），再排后面的任务。
- **UAC 与权限**：提权运行、服务安装、注册表 HKLM 写入在非管理员下会失败，API 要返回明确错误而不是崩溃。
- **DPI**：显示器与截图相关 API 必须声明 per-monitor DPI 感知，否则在缩放屏上坐标会错位（IDE 已有缩放体系，注意别双重缩放）。
- **aardio 是 GBK 源码**：读取参考实现时注意编码；迁移过来的字符串常量统一 UTF-8。

---

## 6. 第二期清单（2026-09 盘点）：跨平台封装，语义参考 aardio、实现走 Zan

> 这一轮盘点只回答一个问题：`D:\aardio\lib` 里还有哪些能力值得进 Zan 标准库，
> 且能**跨平台**落地。纪律沿用迁移原则第 1 条：aardio 源码只当行为规格与
> API 清单（拿来确认语义细节，如 mDNS 的组播地址、STUN 的 magic cookie、
> WOL 的魔术包格式），实现一律用 Zan 现有底座（Sockets、HttpClient、Zip、
> ARC 类、`async/await`），禁止逐行直译表驱动风格。
> 已被现有 stdlib 覆盖或明确不迁的（COM/`dotNet`/python/php 嵌入、gdip 整族、
> aardio 的 HTML UI 布局体系、`web.rest`/`chrome` 自动化）不再重复列。

### 6.1 A 档 — 通用价值高、Zan 有现成底座、优先做

| 目标模块 | aardio 参考 | 覆盖范围 | Zan 底座 | 难度 |
| --- | --- | --- | --- | --- |
| `System.Xml` | `string/xml.aardio`（849 行：实体表、eachChild 遍历、queryEles 查询） | 解析（DOM 树 + 实体反转义）、序列化、按标签名/属性查询；XPath 可后置 | 纯算法，零依赖 | M |
| `System.Net.Ftp` | `inet/ftp.aardio`（WinInet 封装：下载/上传/列目录/建删目录，被动模式） | FTP 客户端，语义对齐：List/Download/Upload/MkDir/Delete/Rename | `Sockets`/`TcpClient` + `async`（协议本身要自己实现控制+数据双连接） | M |
| `System.Diagnostics.Log` 增强：控制台进度条 | `console/progress.aardio`（单行刷新、颜色、完成态） | 终端单行进度条（`\r` 重绘、百分比、消息行），非 TTY 时降级为逐条打印 | `Console` 内建（Write/ForegroundColor） | S |
| `System.IO.NamedPipe` | `fsys/namedPipe.aardio` + `fsys/stream.aardio` | 命名管道服务端/客户端（Windows `\\.\pipe\`，POSIX FIFO），父子进程 IPC | 已有 `MemoryMappedFile` 同族的句柄封装套路；驱动层需补 `CreateNamedPipe`/`ConnectNamedPipe`/`open(FIFO)` | M |
| 跨进程命名互斥体（`Mutex.OpenNamed`） | `process/mutex.aardio`（单实例检测：Open→conflict 判定） | 命名互斥体：单实例守护、跨进程资源锁 | `System.Threading.Mutex` 已有 Windows `CreateMutexA` 与 POSIX pthread 两条分支，补命名语义即可（POSIX 侧用文件锁） | S |
| `System.Text.Base32` | `string/base32.aardio`（96 行，RFC 4648） | encode/decode（含 padding 开关） | 纯算法；顺手给 `Otp` 的 secret 输入接上（RFC 6238 标准就是 Base32） | S |
| `System.Text.Patch` | `string/patch.aardio`（Aider 风格 SEARCH/REPLACE 块，530 行，版本号 2026.07.19.0） | 文本补丁应用（多块 SEARCH/REPLACE、唯一性校验）——AI 编码工具链直接受益 | 纯算法 | S |
| `System.Text.EditorOps` | `string/editor.aardio`（EOL 探测/统一/计数） | 换行风格探测（CRLF/LF/CR）、统一、行数统计 | 纯算法；`CodeEditor` 组件是现成消费方 | S |

### 6.2 B 档 — 值得做，但要么依赖面稍宽、要么使用面较窄

| 目标模块 | aardio 参考 | 说明 | 难度 |
| --- | --- | --- | --- |
| `System.Net.NetworkDiscovery`（mDNS/SSDP/WOL/STUN 四合一或分四个小类） | `wsock/udp/{mdnsClient,ssdpClient,wolClient,stunClient}.aardio` | UDP 组播/广播三件套 + STUN 公网地址探测；IoT/局域网工具高频 | M（需要补 `Socket` 组播 `IP_ADD_MEMBERSHIP` 选项封装） |
| `System.Cryptography.Certificate`（X.509 只读子集） | `crypt/cert.aardio`（666 行：PEM/DER 加载、subject/issuer/有效期/指纹读取） | 证书解析只读（列出字段），签名校验走已有 `Rsa`/`Sha*`；`RsaKey.zan` 已有 PEM/DER TLV 解析层可复用 | M |
| `System.Cryptography.Des`（DES/3DES）+ `Rc4` | `crypt/des.aardio`、`crypt/rc4.aardio` | 纯为遗留系统互通（老协议、老文件格式解密）；新代码禁用，类注释写明"仅遗留互操作" | M |
| `System.Cryptography.ProtectData`（DPAPI） | `crypt/protectData.aardio`（CryptProtectData/UnprotectData） | 用户级凭据加密落盘。Windows 直调 Crypt32；跨平台语义=本用户可解密，POSIX 用 libsecret/文件权限+密钥派生降级实现，文档写明强度差异 | S（Windows 侧）/ L（全平台对齐） |
| `System.Text.Html`（实体表 + 极简解析） | `string/html.aardio`、`web/entities` | 只做：HTML 实体反转义、剥标签取纯文本、元信息提取；不做完整 DOM（那是浏览器引擎的事，CEF 已覆盖） | S |
| `System.Text.Tfidf` | `string/tfidf.aardio` | 词频-逆文档频率打分；`Bm25Index` 已是同族（同一作者语义参照），补 TF-IDF 凑齐检索打分全家桶 | S |
| `System.Time.SunTimes` | `time/sun.aardio` + `time/julianDay.aardio`（Delta T 数据表、节气时刻） | 日出日落/儒略日/节气精确时刻。注意：`Lunar` 已覆盖"当天是哪个节气"，本条补的是**时刻计算**（天文历表照搬） | M |
| `System.Time.Period`（周期时间表达式） | `time/period.aardio`（22 行）+ `time/zone.aardio` | 相对时间窗口（"本周/上月/最近7天"）解析与求值——报表/筛选高频；时区转换目前 `DateTime` 只有本机时区，跨时区显式转换可并入 | S |
| `System.IO.LatestFile` | `fsys/latest.aardio` | 目录里取最新匹配文件（下载目录轮询场景） | S |
| `System.Text.ArgsTable`（命令行参数表） | `string/args.aardio`（131 行：键值对 ↔ 命令行文本双向序列化，dash-case 与引号转义规则齐全） | 内部工具把配置拼成命令行传给子进程的标准做法；`Environment.ArgAt` 只有裸数组，解析/拼接两端都缺 | S |
| `System.Text.CmdLine`（argv 切分） | `string/cmdline.aardio`（Windows `CommandLineToArgvW` 语义：引号、反斜杠转义） | 把一条命令行文本按平台规则切成 argv；纯算法实现即可（不调 Shell32，跨平台一致） | S |
| `System.Text.IntSegments` | `string/intSegments.aardio` | "1,3,5-8" ↔ 整数列表双向转换（分页/行号选择高频） | S |

### 6.3 判定不迁（有证据）

| aardio 库 | 不迁理由 |
| --- | --- |
| `gdip`/`gdi` 整族 | Zan GUI 已有自己的 `System.Drawing.Graphics` 自绘栈，GDI+ 只会是第二套绘图后端 |
| `dotNet`/`com`/`java`/`golang`/`nodeJs`/`py2`/`py3` 嵌入 | 与"Zan 自成体系"路线冲突（一期已判，维持） |
| `chrome`/`web.view`/`web.layout` | CEF 驱动（`Gui.Component.CefBrowser`）已覆盖内嵌浏览器 |
| `web.rest`/`soapClient`/`feishu`/`npm` 等在线服务族 | 业务 API 包装不属于标准库；OAuth 等通用机制已由 HttpClient/CookieJar 承接 |
| `string/regex.aardio`、`string/glob.aardio` | 已有 `System.Text.RegularExpressions`、`PathEx.Glob` |
| `string/xml.aardio` 之外的 markdown 族 | 已有 `System.Text.Markdown` |
| `sqlite`/`sqlServer`/`access`(OLE DB) | `System.Data` 已覆盖（access 仅 Windows OLE DB，跨平台无解，不迁） |
| `console/_.aardio` 大部（Windows INPUT_RECORD 级别的控制台输入） | `Console` 内建已覆盖 CLI 常规需求；Win32 控制台 buffer 级操作不值得跨平台封装 |
| `thread.works`/`thread.dlManager` | Zan 有真线程 + `async/await` + `BlockingQueue`，并发下载用 `async` 任务组实现更自然；aardio 的 fiber 工作线程模型是旧语言的妥协，不照搬 |
| `fsys/media.aardio`（MCI 播放）、`fonts/`、`color/table.aardio`（色表） | 音频走 `System.Audio`（WASAPI）；字体/颜色是 Gui 皮肤层的事 |
| `process/ffmpeg`/`process/git` 等外部工具包装 | 属于应用层，不值得进 stdlib（`Process.WinCapture` 已够用） |

### 6.4 本期方法论要点（同上一轮验证）

- **先探针再动手**：A 档里 `NamedPipe`、组播 socket 要先写最小探针确认驱动层
  现状（`src/runtime` 是否已有/缺哪个调用），探针进 `_scratch/`，结论记这里。
- **发现手搓重复实现的存货**：盘点发现 WebDAV 的 Multi-Status 解析、Xlsx 的
  XML 转义都是手写字符串扫描——`System.Xml`（A 档第 1 条）落地后应回头把
  这两处收敛到标准 XML 解析上，"影子解析器"只允许活到正式库落地为止。
- **aardio 的协作式并发模型不迁**：`coroutine`/`thread.works` 那套 fiber +
  共享表通信是 aardio 单线程 GUI 的历史产物；Zan 用 `async/await` +
  线程安全集合表达同样的语义，这是"写法归 Zan"最典型的一处。

### 6.5 补充档（第二轮排查补漏，2026-09-10）

逐项对照后确认仍是真缺口的：

| 目标模块 | aardio 参考 | 说明 | 难度 |
| --- | --- | --- | --- |
| `Encoding` 补 GBK/GB18030/Big5 转换 | `string/encoding.aardio`（codepage 注册表查询）、`fsys/codepage.aardio`（按 BOM/名称转码读文件） | 现状：`Encoding` 只有 UTF-8 一族，GBK 解码散落在 `Process.WinCapture` 的 `#if WINDOWS` 分支里。中文生态读写老文件/老协议必需，跨平台走 iconv 或内置表。`Process` 已示范 kernel32 直调，非 Windows 需 runtime 补一层 | M |
| `System.Net.Uri`（宽松 URL 解析） | `inet/urlpart.aardio`（scheme/host/user/pass/port/query 分段） | 现状只有 `ExternalTarget.Parse`——那是**安全严格**的解析器（拒绝 userinfo/百分号等），不能当通用解析用。通用解析允许 userinfo/片段/任意 scheme，HttpClient 与 WebSocket 都将受益 | S |
| `DateTime` 格式化/解析增强 | `time/util.aardio`（`%Y-%m-%d %H:%M:%S` 式 format/parse） | 现状 `ParseDate` 只认严格 `YYYY-MM-DD`。补：格式串 format/parse 双向、`TimeSpan` 文本化——报表、日志、CSV 导入高频 | M |
| `System.Text.ChineseNumber` | `string/chineseNumber.aardio`（216 行：数字↔中文大小写、金额、日期时间中文化，简繁两套） | 财务/票据/发票场景刚需；简繁两套字符表照搬，实现纯算法 | S |
| Zip 读写支持传统加密（ZipCrypto） | `zlib/zip.aardio`（minizip 带 password 参数） | 现状 `Zip` 明写"无加密"。老软件导出的 zip 全是 ZipCrypto；解密只需 CRC32（已有）+ 密钥流，读侧价值高于写侧 | M |
| `System.IO.HostsFile` | `fsys/hosts.aardio`（读改写 hosts + 刷新 DNS 缓存） | 网络调试/内网映射工具常用。跨平台：hosts 路径 Windows/POSIX 各一个常量，刷新 DNS 缓存 Windows 走 `DnsFlushResolverCache`、POSIX 无操作 | S |
| `System.IO.BatchRename`（批量文件操作框架） | `fsys/batch.aardio` | 按通配符批量遍历+改名/转码；`Directory` 已有遍历，缺的是"批量预览+应用"骨架。价值边际，可与 LatestFile 合并成一个"文件工具"小族 | S |

顺带确认过、已有等价物或价值不足的：`inet/mac.aardio`（`NetworkInterface`
已有 macAddress）、`inet/conn.aardio`（WinInet 代理设置，仅 Windows 且
HttpClient 不走系统代理，语义不适用）、`string/res.aardio`（PE 资源字符串，
仅 Windows）、`string/fontRanges.aardio`（GDI 字体覆盖查询，Gui 自绘栈不适用）、
`string/stream.aardio`/`fsys/table.aardio`（持久化 KV 配置——`ZanDb.KvStore`
是更完整的同类）、`string/fencedCodeBlock.aardio`、`string/html.minify`、
`string/lrc.aardio`（歌词解析，应用层）、`string/oct.aardio`（八进制转义，
`Encoding` 可扩一方法解决）、`crypt/bin.aardio`（Hex/Base64 已有）。


