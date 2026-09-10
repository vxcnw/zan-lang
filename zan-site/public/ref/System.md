# System

> 源码: `stdlib/System/Audio.zan`, `stdlib/System/Binding.zan`, `stdlib/System/ConsoleColor.zan`, `stdlib/System/DateTime.zan`, `stdlib/System/Exception.zan`, `stdlib/System/Guid.zan`, `stdlib/System/IDisposable.zan`, `stdlib/System/Interop.zan`, `stdlib/System/ListExtensions.zan`, `stdlib/System/NativeMemory.zan`, `stdlib/System/Random.zan`, `stdlib/System/RandomNumberGenerator.zan`, `stdlib/System/Stopwatch.zan`, `stdlib/System/StringExtensions.zan`, `stdlib/System/TaskJoin.zan`, `stdlib/System/TimeSpan.zan`, `stdlib/System/ZanVersion.zan`


## ArgumentException (class)

当传给方法的参数无效时抛出。

- public ArgumentException(string message)
  - 以描述参数无效原因的消息构造。


## Audio (class)

原生音频设备：一次打开，之后所有声音都混到这一个设备上。

零依赖原生实现（WASAPI 先行），取代原 SDL3 的音频桥。
`AudioClip` 是解码好的采样（WAV/OGG），
`AudioVoice` 是它的一次播放；同一个 clip 可以同时起多个
voice（叠加音效），混音由运行时后台线程完成。

- static bool Open()
  - 打开默认播放设备（已打开时直接返回 true）。

- static bool IsOpen()
  - 播放设备已打开时为真。

- static void SetVolume(double volume)
  - 主音量（0..1，可放大到 1 以上）。对已经在响的声音同样
    生效，所以静音/淡出立即听得到。

- static double Volume()
  - 当前主音量（0..1）。

- static string DriverName()
  - 原生音频后端名（Windows 上是 "wasapi"；其他平台的
    原生后端尚未落地，返回空串）。

- static int ActiveVoices()
  - 还在响的声音数：一次性音效播完即回收，不用调用方登记。

- static void StopAll()
  - 立刻停掉所有声音（切场景/退出时用）。

- static void Close()
  - 关闭设备，并停掉设备上剩下的声音。

- static string LastError()
  - 最近一次失败的原因（设备打开失败/解码失败等）；
    没有失败记录时为空串。


## AudioClip (class)

加载到内存的采样（s16 PCM）。`Play` 每次返回
一个新的 `AudioVoice`，所以同一个 clip 可以叠着响。

- nint handle;

- static AudioClip LoadWav(string path)
  - 加载 WAV 文件（PCM 8/16/24/32 位与 32 位浮点，含
    WAVE_FORMAT_EXTENSIBLE）。失败时返回的对象 IsValid() 为 false
    （原因见 <c>Audio.LastError()</c>），不返回 null。

- static AudioClip LoadOgg(string path)
  - 加载 OGG Vorbis 文件（背景音乐）。失败时返回的对象
    IsValid() 为 false，不返回 null。

- static AudioClip LoadWavFromMem(string data, int len)
  - 从内存字节解析 WAV。<paramref name="data"/> 是完整的
    WAV 文件字节（如从加密资源包解密出来的内容），全程不落盘。
    字节只在本次调用内同步读取（PCM 会被拷出），返回后即可释放
    缓冲区，不转移所有权。失败时返回的对象 IsValid() 为 false
    （原因见 <c>Audio.LastError()</c>），不返回 null。

- static AudioClip LoadOggFromMem(string data, int len)
  - 从内存字节解码 OGG Vorbis（背景音乐）。字节只在本次
    调用内同步读取（PCM 会被拷出），返回后即可释放缓冲区。
    失败时返回的对象 IsValid() 为 false。

- bool IsValid()
  - 加载成功时为真（失败时为假对象，不返回 null）。

- int Frequency()
  - 采样率（Hz）。

- int Channels()
  - 声道数（1 单声道、2 立体声）。

- int DurationMs()
  - 时长（毫秒）。

- AudioVoice Play()
  - 用默认音量播一次。

- AudioVoice Play(double gain, int loop)
  - 播一次。<paramref name="gain"/> 是这一个声音的音量，
    <paramref name="loop"/> 非 0 表示循环（背景音乐）。

- AudioVoice PlayLooping(double gain)
  - 循环播放，直到 `AudioVoice.Stop`。

- void Close()
  - 释放采样，并停掉还在读它的声音。


## AudioNative (class)

zan_audio 原生桥（音频随 zan_gui 运行时导出）。

- [DllImport("zan_gui")]static extern int zan_audio_open();

- [DllImport("zan_gui")]static extern void zan_audio_close();

- [DllImport("zan_gui")]static extern int zan_audio_is_open();

- [DllImport("zan_gui")]static extern void zan_audio_set_volume(double volume);

- [DllImport("zan_gui")]static extern double zan_audio_volume();

- [DllImport("zan_gui")]static extern string zan_audio_driver_name();

- [DllImport("zan_gui")]static extern int zan_audio_active_voices();

- [DllImport("zan_gui")]static extern void zan_audio_stop_all();

- [DllImport("zan_gui")]static extern string zan_audio_last_error();

- [DllImport("zan_gui")]static extern nint zan_audio_load_wav(string path);

- [DllImport("zan_gui")]static extern nint zan_audio_load_ogg(string path);

- [DllImport("zan_gui")]static extern nint zan_audio_load_wav_mem(string data, int len);

- [DllImport("zan_gui")]static extern nint zan_audio_load_ogg_mem(string data, int len);

- [DllImport("zan_gui")]static extern void zan_audio_free_clip(nint clip);

- [DllImport("zan_gui")]static extern int zan_audio_clip_frequency(nint clip);

- [DllImport("zan_gui")]static extern int zan_audio_clip_channels(nint clip);

- [DllImport("zan_gui")]static extern int zan_audio_clip_duration_ms(nint clip);

- [DllImport("zan_gui")]static extern long zan_audio_play(nint clip, double gain, int loop);

- [DllImport("zan_gui")]static extern int zan_audio_voice_playing(long voice);

- [DllImport("zan_gui")]static extern void zan_audio_voice_stop(long voice);

- [DllImport("zan_gui")]static extern void zan_audio_voice_set_gain(long voice, double gain);


## AudioVoice (class)

一次播放（voice）。

句柄带世代号：声音播完后句柄失效，`IsPlaying` 老实返回
false、`Stop` 什么也不做，因此一个存活时间比声音长的
AudioVoice 变量是安全的，不会碰到被回收的槽位。

- long handle;

- static AudioVoice Of(long handle)
  - 包装一个原生 voice 句柄；0 表示没起来的声音，此时对象
    依然可用（IsPlaying 为 false），调用方不需要判空。

- bool IsValid()
  - 声音是否成功起播（设备没开、voice 池满时为 false）。

- bool IsPlaying()
  - 声音仍在响时为真；播完或已 Stop 即 false（句柄按世代号失效）。

- void SetGain(double gain)
  - 这一个声音的音量（会再乘上主音量）。

- void Stop()
  - 停掉这一个声音并使句柄失效；对已失效句柄无操作。


## Binding (class)

到类型 T 值的双向数据绑定。

组件作者将可绑定属性声明为 `Binding<T>` 字段。
将字段左值赋给这类属性时，编译器会将其降级为
实时绑定（Get 读取字段，Set 回写）；赋
其他表达式则生成存储值的常量绑定。

class User { string name; }
input.data = user.name;   // 实时：model <-> UI
input.data = "hello";     // 常量：固定值，仍可设置

每次 Set 都会使 `version` 递增，控件可低成本检测写入。

- object target;

- BindGet<T> getter;

- BindSet<T> setter;

- bool live;

- T constVal;

- int version;

- T Get()
  - 绑定字段的当前值（live）或存储值（const）。

- void Set(T v)
  - 通过绑定写回（live 绑定时为 UI -> model）。

- int Version()
  - 通过此绑定执行的写入次数。

- bool IsLive()
  - 绑定到模型字段时为 true（区别于常量值）。


## Com (class)

无需 C shim 的 COM：接口指针即地址，方法存在于
对象的 vtable 中，槽位通过
delegate 转换变为可调用对象。

nint shell = Com.Create("00021401-0000-0000-C000-000000000046",
"00000000-0000-0000-C000-000000000046");
Com.Call1(shell, 5, argument);   // vtable 槽位 5，`shell` 作为 `this`
Com.Release(shell);

用 Zan 实现的 COM 对象（异步 COM API 的完成处理器都需要它）
通过 ComVtbl 构建：将回调地址写入 vtable
（从 `(nint)handler` 获取），并把对象交还回去。

- static nint Ole()
  - ole32 在运行时解析而非链接时解析：
    从不接触 COM 的程序既不会加载也不依赖它。

- static nint ole;
  - 已解析的 ole32.dll 句柄（0 为未加载）。

- static int comTls=Com.AllocComTls();
  - 保存"本线程 COM 已初始化"的 TLS 槽号；-1 表示分配失败。

- static int AllocComTls()
  - 分配记录 COM 初始化状态的 TLS 槽；失败返回 -1。

- static int ComTls()
  - 记录"本线程 COM 已初始化"的 TLS 槽号（-1 表示分配失败）。

- static bool ComInitialized()
  - 当前线程是否已通过本类初始化过 COM。

- static bool SetComInitialized(bool initialized)
  - 设置本线程的 COM 初始化标志；TLS 不可用时返回 false。

- static int CoInit(nint reserved, int flags)
  - CoInitializeEx 包装；入口缺失返回 -1。

- static void CoUninit()
  - CoUninitialize 包装；入口缺失时忽略。

- static int CoCreate(nint clsid, nint outer, int ctx, nint iid, nint result)
  - CoCreateInstance 包装；入口缺失返回 -1。

- static void TaskFree(nint p)
  - CoTaskMemFree 包装；入口缺失时忽略。

- static int SlotQueryInterface()
  - IUnknown vtable 布局，所有 COM 接口共用。

- static int SlotAddRef()
  - IUnknown vtable 槽位 1：AddRef（引用计数 +1）。

- static int SlotRelease()
  - IUnknown vtable 槽位 2：Release（引用计数 -1，归零自毁）。

- static int Apartment()
  - COINIT_APARTMENTTHREADED——UI/WebView2 对象所需的模式。

- static int InProc()
  - CLSCTX_INPROC_SERVER.

- static bool Ok(int hr)
  - HRESULT 是否成功（非负即成功，含 S_FALSE）。

- static int Initialize()
  - 在调用线程上初始化 COM。S_FALSE 表示成功，且
    与一次 Shutdown 配对；apartment 模式变更仍视为失败。

- static void Shutdown()
  - 在调用线程上平衡本类成功的 Initialize。

- static nint Guid(string text)
  - 将 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 解析为新建的
    16 字节 GUID（前三个字段为小端，符合 COM 预期）。

- static int Hex(string s, int off, int len)
  - 取 s 中 off 起 len 个十六进制字符的整数值（非法字符按 0）。

- static int Digit(string ch)
  - 单个十六进制字符的数值；非法字符按 0。

- static void FreeGuid(nint g)
  - 释放 Guid() 分配的 16 字节。

- static nint Create(string clsid, string iid)
  - 使用文本 GUID 调用 CoCreateInstance；类不可用时返回 0。

- static nint Slot(nint iface, int index)
  - 接口指针 vtable 槽位 `index` 处方法的地址。

- static int Call0(nint iface, int index)
  - 调用 vtable 槽位 `index`，以接口指针作为 `this`。
    槽位为空时返回 E_FAIL，缺失的方法会像调用失败一样
    优雅降级，而不是跳到地址零。

- static int Call1(nint iface, int index, nint a)
  - 同 Call0，多一个指针参数；槽位为空返回 E_FAIL。

- static int Call2(nint iface, int index, nint a, nint b)
  - 同 Call0，多两个指针参数；槽位为空返回 E_FAIL。

- static int Call3(nint iface, int index, nint a, nint b, nint c)
  - 同 Call0，多三个指针参数；槽位为空返回 E_FAIL。

- static int Call4(nint iface, int index, nint a, nint b, nint c, nint d)
  - 同 Call0，多四个指针参数；槽位为空返回 E_FAIL。

- static int Call5(nint iface, int index, nint a, nint b, nint c, nint d, nint e)
  - 同 Call0，多五个指针参数；槽位为空返回 E_FAIL。

- static int Fail()
  - E_FAIL.

- static nint Get(nint iface, int index)
  - 调用单个参数为 out 指针的槽位，返回
    被调用者存入的值（失败时返回 0）——所有 COM getter 的通用形式。

- static string GetString(nint iface, int index)
  - 返回 CoTaskMemAlloc 分配宽字符串的 getter，封送后释放。

- static int GetInt(nint iface, int index)
  - 通过 out 指针返回 32 位值（BOOL、枚举、计数）的 getter。

- static nint Query(nint iface, string iid)
  - 以文本 IID 调用 QueryInterface；不支持时返回 0。

- static nint Keep(nint iface)
  - 对借用的接口指针（即回调收到的）
    持有引用，使其在调用结束后依然存活。

- static void Release(nint iface)
  - 平衡 Keep/Query/Create 得到的引用：调用 IUnknown.Release 槽位。

- static void Free(nint p)
  - 释放被调用者用 CoTaskMemAlloc 分配的缓冲区（字符串
    出参的常用约定）。

- static string TakeString(nint p)
  - 读取 CoTaskMemAlloc 分配的宽字符串出参并释放。


## ComVtbl (class)

用 Zan 实现的 COM 对象：`Add` 按 vtable 顺序追加方法地址
（从三个 IUnknown 槽位开始），`Build` 返回
可供原生代码回调的接口指针。

ComVtbl v = ComVtbl.Create(4);
v.Add((nint)Handler.QueryInterface);
v.Add((nint)Handler.AddRef);
v.Add((nint)Handler.Release);
v.Add((nint)Handler.Invoke);
nint handler = v.Build();

对象为 `{ vtable, state }`：`State()` 为调用者提供一个槽位，
用于存放其关联 id，静态 handler 可从中
通过传入的 `self` 指针读回。

- nint vtbl;
  - vtable 内存。

- nint obj;
  - Build() 分配的对象指针（0 为未构建）。

- int slots;
  - vtable 容量（槽数）。

- int count;
  - 已填充的槽数。

- static ComVtbl Create(int slots)
  - 创建可容纳 slots 个条目的 vtable。

- ComVtbl Add(nint method)
  - 追加下一个 vtable 条目；超过 `slots` 的多余条目会被忽略。

- nint Build()
  - 分配对象（vtable 指针 + 一个状态字）并返回
    接口指针。

- void SetState(int v)
  - 由调用者持有、随对象携带的状态字。

- static int State(nint self)
  - 静态 handler 侧：从回调收到的 self 指针读回 SetState 写入的
    状态字。

- void Destroy()
  - 释放对象与 vtable 内存（Build 之后调用才有效）。


## DateTime (class)

UTC 时刻，精度为 1 秒，存储为
Unix 纪元（1970-01-01 00:00:00 UTC）以来的秒数。

日历字段由 civil-from-days 算法推导，因此
该类完全跨平台，仅需 libc <c>time()</c> 来获取
当前时刻。`Now` 与 `UtcNow` 都返回 UTC；
本机时区的墙钟时间由 `LocalNow` /
`ToLocalTime` 给出，偏移取自 libc 的时区库
（`LocalOffsetMinutes`），因此含夏令时。

- [DllImport("crt")]static extern long time(nint ptr);

- [DllImport("crt", EntryPoint="localtime")]static extern nint plat_localtime(nint tptr);
  - 本机时区换算全部交给 libc 的时区库：localtime 把纪元秒展开成本地
    墙钟字段，再用 timegm（Windows 上是 _mkgmtime）把这组字段当作 UTC
    折回纪元秒，两者之差就是该时刻的实际偏移（自带夏令时）。

- [DllImport("crt", EntryPoint="_mkgmtime")]static extern long plat_timegm(nint tm);

- [DllImport("crt", EntryPoint="localtime")]static extern nint plat_localtime(nint tptr);

- [DllImport("crt", EntryPoint="timegm")]static extern long plat_timegm(nint tm);

- long epoch;
  - 自 1970-01-01T00:00:00Z 以来的秒数。

- int year;
  - 年。

- int month;
  - 月，1..12。

- int day;
  - 日，1..31。

- int hour;
  - 时，0..23。

- int minute;
  - 分，0..59。

- int second;
  - 秒，0..59。

- int dayOfWeek;
  - 星期几，0=星期日 .. 6=星期六。

- DateTime(long unixSeconds)
  - 根据 Unix 时间戳（秒，UTC）构造时刻。

- static DateTime UtcNow()
  - 当前时刻（UTC）。

- static DateTime Now()
  - `UtcNow` 的别名；不应用本地时区偏移。

- static int LocalOffsetMinutesAt(long unixSeconds)
  - 本机时区在 <paramref name="unixSeconds"/> 这一时刻相对 UTC 的偏移
    （分钟，东为正，如东八区 480），含该时刻是否处于夏令时。
    时区信息不可用时返回 0（等同 UTC）。

- static int LocalOffsetMinutes()
  - 本机时区当前相对 UTC 的偏移（分钟，东为正）。

- DateTime ToLocalTime()
  - 同一时刻的本地墙钟表示：年月日时分秒都是本机时区读数。
    注意它的 `ToUnixSeconds` 已被偏移，不再是纪元秒；
    需要纪元秒请用原来的 UTC 时刻。

- static DateTime LocalNow()
  - 本机时区的当前墙钟时间（见 `ToLocalTime`）。

- static DateTime FromUnixSeconds(long seconds)
  - 根据 Unix 时间戳（自纪元起的秒数）构造时刻。

- static DateTime FromDate(int year, int month, int day)
  - 给定日历日期当天的 UTC 午夜零点。

- static DateTime FromParts(int year, int month, int day, int hour, int minute, int second)
  - 给定的日历日期和墙上时钟时间，按 UTC 处理。

- static int DaysFromCivil(int year, int month, int day)
  - 公历日期到 Unix 纪元的天数——与构造器所用的
    civil-from-days 算法互为逆运算。
    1970 年之前的日期为负。

- static int DaysInMonth(int year, int month)
  - <paramref name="year"/> 年 <paramref name="month"/> 月的天数。

- static bool IsLeapYear(int year)
  - <paramref name="year"/> 是否为公历闰年。

- int Year()
  - 年。

- int Month()
  - 月（1..12）。

- int Day()
  - 日（1..31）。

- int Hour()
  - 时（0..23）。

- int Minute()
  - 分（0..59）。

- int Second()
  - 秒（0..59）。

- int DayOfWeek()
  - 星期几，0=星期日 .. 6=星期六。

- long ToUnixSeconds()
  - Unix 纪元以来的秒数（UTC）。

- DateTime AddSeconds(long n)
  - 加 n 秒。

- DateTime AddMinutes(long n)
  - 加 n 分钟。

- DateTime AddHours(long n)
  - 加 n 小时。

- DateTime AddDays(long n)
  - 加 n 天。

- TimeSpan Subtract(DateTime other)
  - 此时刻与 <paramref name="other"/> 之间的间隔。

- bool Equals(DateTime other)
  - 同一时刻（纪元秒相等）。

- bool IsBefore(DateTime other)
  - 早于 other。

- bool IsAfter(DateTime other)
  - 晚于 other。

- string ToString()
  - 类 ISO 文本："YYYY-MM-DD HH:MM:SS"。

- string ToDateString()
  - 仅日期："YYYY-MM-DD"。

- string ToTimeString()
  - 仅时间："HH:MM:SS"。

- static DateTime ParseDate(string value)
  - 解析严格的 "YYYY-MM-DD" 为当天 00:00:00；长度、分隔符或
    取值非法（月 1..12、日不超过当月天数）返回 null。年份须
    四位数字，供文本输入与属性面板回传使用。

- static int ParseDigits(string s, int at, int count)
  - 解析 `at` 起 `count` 位十进制数字；含非数字返回 -1。

- static int Digit(string c)
  - 十进制数字字符的值，非数字返回 -1。

- static string Pad2(long n)
  - 将 0..99 的值补零到两位。

- static long FloorDivL(long a, long b)
  - 对 64 位秒数做向下取整的整数除法。

- static int FloorDiv(int a, int b)
  - 向下取整的整数除法（向负无穷取整）。

- static int FloorMod(int a, int b)
  - 向下取整的模运算；结果符号与除数一致。


## Exception (class)

所有异常的基础类型，携带人类可读的消息，通过
<c>throw new Exception("...")</c> 抛出，并由 <c>catch (Exception e)</c> 捕获。

- public string Message;
  - 人类可读的异常消息。

- public Exception(string message)
  - 以人类可读的消息构造异常。

- public string ToString()
  - 消息文本即字符串形式。


## FileNotFoundException (class)

当必须存在的文件无法打开时抛出。

- public FileNotFoundException(string message)
  - 以描述缺失文件的消息构造。


## Guid (class)

UUID（GUID）的生成与解析。

string id = Guid.New();          // e.g. "f47ac10b-58cc-4372-a567-0e02b2c3d479"
Guid g = Guid.Parse(id);         // round-trips
bool same = Guid.Equals(g, g2);

- static string ToString(Guid g)
  - `g` 的规范形式：36 字符小写（"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"）。

- static Guid Parse(string text)
  - 解析 36 字符的规范 GUID（允许连字符，不区分大小写）。
    文本不是合法的 GUID 时返回 null。

- static Guid NewV4()
  - 使用操作系统 CSPRNG 生成 version-4（随机）UUID：
    122 个随机位，版本号 0100，变体位 10。
    仅当操作系统 RNG 失败时才返回 null。

- static string New()
  - 快捷方法：返回新的随机 GUID 字符串，RNG 失败时返回 ""。

- static bool Equals(Guid a, Guid b)
  - 两个 GUID 相等时返回 true（可安全处理 null）。

- static string Format(byte[]b)
  - 将 16 字节格式化为规范 GUID 字符串。

- static int CodeOf(string ch)
  - 首字符的字节值；空串返回 0。

- public string text;
  - 规范的小写 36 字符文本形式。


## HttpRequestException (class)

当 HTTP 请求无法发送或完成时抛出
（连接失败、TLS 握手失败）。

- public HttpRequestException(string message)
  - 以描述请求失败原因的消息构造。


## IOException (class)

当 I/O 操作（打开、读取、写入、复制）失败时抛出。

- public IOException(string message)
  - 以描述 I/O 失败原因的消息构造。


## Interop (class)

动态原生链接：在运行时解析库及其入口点，
并通过 delegate 调用，而不声明 `[DllImport]`
（加载时即需存在）。

nint user32 = Interop.Load("user32.dll");
nint addr   = Interop.Symbol(user32, "MessageBoxW");
MessageBoxW box = (MessageBoxW)addr;      // 地址 -> 可调用
box(0, Wide.Of("hi"), Wide.Of("zan"), 0);

`(Delegate)address` 转换及其逆操作 `(nint)handler` 是编译器的
原语，因此可选依赖（一个可能未安装的运行时）
无需 C shim：先探测，缺失时回退即可。

- [DllImport("kernel32", EntryPoint="LoadLibraryA")]static extern nint WinLoad(string name);

- [DllImport("kernel32", EntryPoint="GetProcAddress")]static extern nint WinSymbol(nint mod, string name);

- [DllImport("kernel32", EntryPoint="FreeLibrary")]static extern int WinUnload(nint mod);

- [DllImport("kernel32", EntryPoint="GetLastError")]static extern int WinLastError();

- [DllImport("crt", EntryPoint="dlopen")]static extern nint PosixLoad(string name, int flags);

- [DllImport("crt", EntryPoint="dlsym")]static extern nint PosixSymbol(nint mod, string name);

- [DllImport("crt", EntryPoint="dlclose")]static extern int PosixUnload(nint mod);

- [DllImport("crt", EntryPoint="dlerror")]static extern string PosixError();

- static int RtldNowLocal()
  - RTLD_NOW | RTLD_LOCAL 的整数值：Linux/musl 上 RTLD_LOCAL 为 0
    （RTLD_NOW=2），Darwin 上 RTLD_LOCAL=4（RTLD_NOW=2），所以
    不能只写一次硬编码常量。

- static string lastError="";
  - 最近一次 Load/Symbol 失败的原因文本。

- static string LastError()
  - 上次失败加载的原生加载器错误文本（dlerror / Win32 错误码）；
    没有失败时为空字符串。

- static nint Load(string name)
  - 按名称或路径加载共享库；不存在时返回 0。

- static nint Symbol(nint mod, string name)
  - 导出入口点的地址；库中没有时返回 0
    （一种以 ABI 兼容方式探测新运行时特性的做法）。

- static void Unload(nint mod)
  - 卸载共享库；句柄为 0 时忽略。

- static nint Entry(string name, string entry)
  - 一步加载 `name` 并解析 `entry`；任一失败返回 0。

- static extern string getenv(string name);

- static string EnvVar(string name)
  - 从活动进程块读取环境变量，未设置时返回
    空字符串。


## InvalidOperationException (class)

当操作对对象当前
状态无效时抛出（例如对空序列调用 First()）。

- public InvalidOperationException(string message)
  - 以描述无效操作原因的消息构造。


## JsonException (class)

当 JSON 文本格式错误时抛出（JsonValue.Parse）。

- public JsonException(string message)
  - 以描述 JSON 格式错误的消息构造。


## ListExtensions (class)

编译器不会原生降低的 List<T> 操作。

以扩展方法（`this List<T>` 接收方）的形式编写，以便
像成员一样调用：`items.Remove(x)`。此前这些调用会被编译成
常量 0 / 静默空操作，把普通的 Remove 或 Sort 变成
一个没有诊断信息的 bug。

- static bool Remove<T>(this List<T> src, T item)
  - 移除第一个等于 `item` 的元素；返回是否
    确实移除了某个元素。

- static List<T> GetRange<T>(this List<T> src, int start, int count)
  - 从 `start` 开始的 `count` 个元素的副本。范围会
    被限制在列表范围内。

- static void Sort(this List<int> src)
  - 原地升序排序整数。

- static void Sort(this List<double> src)
  - 原地升序排序数值。

- static void Sort(this List<string> src)
  - 原地按序数升序排序字符串。


## NativeMemory (class)

二进制 IO 用的堆外原始内存（ByteBuffer、数据库页、网络
组帧）。地址是普通 nint，不进入 ARC 对象
机制，因此热路径的字节级循环开销与等效的 C 代码相同。

这里每个方法都是编译器内建函数：这些声明是为了
让检查器能对调用做类型检查（ARC 也能跟踪 GetString 返回的字符串），
但 irgen 将每个调用降低为单个 libc 调用——所命名的
库实际上从未被调用或链接。

标量访问是 <c>Span<T></c> 的职责：<c>new Span<int>(p, n)</c>
将原始地址视图化，并以小端、无对齐要求的
类型化读写进行索引。

安全约定：地址必须来自 `Alloc`（或
ByteBuffer.Raw() 之类的固定缓冲区），并且不能在
`Free` 之后继续使用。偏移/长度不做边界检查——由调用方
负责边界，与任何 FFI 缓冲区一样。

- [DllImport("crt")]static extern nint Alloc(int size);
  - 分配 `size` 字节并清零；返回其地址。

- [DllImport("crt")]static extern void Free(nint p);
  - 释放从 Alloc 获得的地址。释放 0 为无操作。

- [DllImport("crt")]static extern void Copy(nint dst, nint src, int n);
  - 将 n 字节从 src 复制到 dst（允许重叠，memmove 语义）。

- [DllImport("crt")]static extern void Fill(nint p, int v, int n);
  - 用 v 的低 8 位填充 p 处的 n 字节。

- [DllImport("crt")]static extern int Compare(nint a, nint b, int n);
  - memcmp：a 与 b 前 n 字节的比较序 <0 / 0 / >0。

- [DllImport("crt")]static extern int Find(nint p, int off, int b, int n);
  - memchr：在 p+off 起的 n 字节内查找字节 b（取低 8 位），
    命中返回相对 p 的偏移，未命中返回 -1。

- [DllImport("crt")]static extern string GetString(nint p, int off, int len);
  - 将 p+off 处的 len 字节复制为新的 ARC 托管字符串。

- [DllImport("crt")]static extern void PutString(nint p, int off, string s, int len);
  - 将 s 的前 len 字节复制到 p+off（不写 NUL 终止符）。

- [DllImport("crt")]static extern int Crc32(nint p, int len);
  - p 处 len 字节的 CRC-32（IEEE，poly 0xEDB88320）。


## PlatformNotSupportedException (class)

当跨平台 API 在当前平台
没有实现时抛出。接口在所有平台都存在，因此代码各处都能编译运行；
不支持的那一半会显式报错，而不是静默
不做事。

- public PlatformNotSupportedException(string message)
  - 以描述平台不支持原因的消息构造。


## Pump (class)

嵌套的 Win32 消息循环。异步 COM 完成以投递消息的形式
到达调用（apartment）线程，因此等待完成就需要
泵消息：同步包装器通过 `Pump.Until(flag, 5000)` 等待
回调而不死锁 UI 线程。

- static nint user32;
  - 惰性解析出的 user32.dll 句柄与四个入口地址（0 为未加载/失败）。

- static nint peek;
  - PeekMessageW 入口。

- static nint translate;
  - TranslateMessage 入口。

- static nint dispatch;
  - DispatchMessageW 入口。

- static nint sleep;
  - kernel32 Sleep 入口。

- static void Resolve()
  - 惰性解析 user32/kernel32 的入口（只做一次）。

- static void Drain()
  - 排空当前线程上所有已排队的消息。

- static bool Until(PumpGate gate, int timeoutMs)
  - 泵消息直到 `gate` 报告完成或超过 `timeoutMs`；
    闸门打开时返回 true。


## PumpGate (class)

回调设置、Pump.Until() 等待的完成标志。

- bool done;

- PumpGate()

- void Signal()
  - 标记完成。

- bool IsDone()
  - 是否已完成。

- void Reset()
  - 复位为未完成。


## Random (class)

通用（非加密）伪随机数生成器。
使用 64 位线性同余序列（Knuth MMIX 常数）；
速度快，可由种子复现，但绝不能用于安全用途——参见
<c>System.RandomNumberGenerator</c>。

- [DllImport("crt")]static extern long time(nint ptr);

- long state;
  - LCG 状态（构造与 Seeded 都保证非 0）。

- Random()
  - 以当前时间作为种子。

- static Random Seeded(long seed)
  - 用显式种子创建生成器（可复现）。

- long NextRaw()
  - 推进状态并返回原始 64 位结果。

- int Next()
  - 非负伪随机整数。

- int NextBelow(int bound)
  - [0, bound) 区间内的非负整数。

- int Between(int lo, int hi)
  - [lo, hi) 区间内的整数。

- double NextDouble()
  - [0.0, 1.0) 区间内的 double。

- bool NextBool()
  - 伪随机布尔值。


## RandomNumberGenerator (class)

跨平台的加密安全随机字节。
Windows 使用系统 CSPRNG（RtlGenRandom / SystemFunction036）；POSIX 从
/dev/urandom 读取（Linux、macOS、BSD）。无弱回退：请求
N 字节却得到更少字节的调用方会收到明确失败（null / 字节数不足），
绝不会返回可预测或未初始化的数据。

- [DllImport("advapi32")]static extern int SystemFunction036(string buf, int len);

- [DllImport("crt", EntryPoint="fopen")]static extern nint urandOpen(string path, string mode);

- [DllImport("crt", EntryPoint="fread")]static extern long urandRead(string buf, long size, long count, nint fp);

- [DllImport("crt", EntryPoint="fclose")]static extern int urandClose(nint fp);

- static int Fill(string buf, int n)
  - 用安全随机数据填充 buf 的前 n 字节。
    返回实际写入的字节数（成功时为 n，失败时更少）。

- static byte[]GetBytes(int n)
  - 分配含 n 个安全随机字节的缓冲区（n+1 字节，末尾的
    零字节使其可在期望 NUL 结尾字符串的场景中使用）。
    若系统 CSPRNG 无法提供 n 字节，则返回 null。


## RegexBudgetException (class)

当正则匹配用尽回溯步骤预算时抛出。病态模式
（`(a+)+$` 之类）在某些输入上代价会爆炸，引擎宁可报错也不把
超时伪装成"无匹配"。

- public RegexBudgetException(string message)
  - 以描述预算耗尽的消息构造。


## SocketException (class)

当套接字操作失败时抛出（创建、绑定、监听、
连接失败），消息携带平台错误码（Windows 的
WSAGetLastError / POSIX 的 errno）。<paramref name="code"/> 以
数值形式携带同一错误码，供程序检查而非解析消息文本。

- public int code;
  - 平台错误码（Windows 的 WSAGetLastError / POSIX 的 errno）。

- public SocketException(int code, string message)
  - 以平台错误码与消息构造。


## Stopwatch (class)

高分辨率计时器。Windows 上使用 QueryPerformanceCounter，
POSIX 上使用 clock_gettime(CLOCK_MONOTONIC) —— 两者都不受墙钟时间
变化（NTP 同步、手动改时）影响，计时结果保持准确。

Stopwatch sw = new Stopwatch();
sw.Start();
... work ...
sw.Stop();
long ms = sw.ElapsedMilliseconds();

- [DllImport("kernel32", EntryPoint="QueryPerformanceFrequency")]static extern int PlatQueryPerformanceFrequency(nint freq);

- [DllImport("kernel32", EntryPoint="QueryPerformanceCounter")]static extern int PlatQueryPerformanceCounter(nint count);

- [DllImport("crt", EntryPoint="zan_monotonic_ns")]static extern long ZanMonotonicNs();

- long startTicks;
  - 最近一次 Start 时的单调时钟读数（频率单位）。

- long accumulated;
  - Start 与 Stop 之间的 tick 数（频率单位）

- bool running;
  - 计时进行中。

- static Stopwatch StartNew()
  - 开始（或继续）计时，可安全重复调用。

- void Start()
  - 开始（或继续）计时。

- void Stop()
  - 停止计时；多次 Start/Stop 的耗时会累加。

- void Reset()
  - 重置累计时间（运行中则同时停止）。

- void Restart()
  - 重新开始：清零并启动。

- double ElapsedMilliseconds()
  - 总耗时（毫秒，双精度）。
    计时器可能仍在运行；读数包含当前累计值。

- double ElapsedSeconds()
  - 总耗时（秒，双精度）。

- long ElapsedTicks()
  - 以原始频率单位表示的耗时（参见 `Frequency`）。

- bool IsRunning()
  - 计时器运行中返回 true。

- static long Frequency()
  - 高分辨率时钟每秒的 tick 数。

- static long GetMicroseconds()
  - 单调微秒读数。不分配内存，能分辨单个请求，因此可用在请求
    处理路径上（超时、截止时间比较）。

- static long GetMilliseconds()
  - 单调毫秒读数。语义同 `GetMicroseconds`。

- static long MonoScaled(long unit)
  - tick 数换算到每秒 `unit` 份的单位。先除后乘：Windows 的 QPC 频率是
    10MHz 量级，直接 `ticks * 1000000` 在机器开机约 11 天后就会溢出 i64。

- static long NowTicks()
  - 当前单调时钟读数（频率单位）。


## StringExtensions (class)

编译器不会原生简化的字符串操作。

它们是扩展方法（`this string` 接收者），因此调用起来
与普通成员一样：`name.PadLeft(8)`。这里的每个名字以前都会编译成
常量 0（该成员根本不存在），所以 C# 风格的代码
会静默产生垃圾结果；把它们实现为真正的 Zan 代码，可以让
编译器、IDE 和语言服务器共用同一套实现。

- static bool IsNullOrEmpty(this string s)
  - 与 C# 的 `string.IsNullOrEmpty` 一致：字符串为 null 或
    长度为 0 时返回 true。先判 null（对 null 的引用比较是安全的），
    因此对 null 字符串调用它不会解引用，也就不会崩溃。用它替代
    `s == ""`——后者会在原生层对空指针做字符串比较直接崩溃。

- static bool IsNullOrWhiteSpace(this string s)
  - 与 C# 的 `string.IsNullOrWhiteSpace` 一致：null、空串或
    仅由空白字符组成时返回 true。

- static string PadLeft(this string s, int width)
  - 在 `width` 个空格宽的字段中右对齐字符串。

- static string PadLeft(this string s, int width, string pad)
  - 右对齐字符串，用 `pad` 填充（取其第一个
    字符；`pad` 为空时原样返回字符串）。

- static string PadRight(this string s, int width)
  - 在 `width` 个空格宽的字段中左对齐字符串。

- static string PadRight(this string s, int width, string pad)
  - 左对齐字符串，用 `pad` 填充（取其第一个
    字符；`pad` 为空时原样返回字符串）。

- static string TrimStart(this string s)
  - 返回去掉前导空白字符的副本。

- static string TrimEnd(this string s)
  - 返回去掉尾部空白字符的副本。

- static string Insert(this string s, int index, string text)
  - 在 `index` 处插入 `value` 的副本。越界的索引
    会被钳制到字符串两端。

- static string Remove(this string s, int start)
  - 返回删除自 `start` 起全部字符的副本。

- static string Remove(this string s, int start, int count)
  - 返回从 `start` 处删除 `count` 个字符的副本。

- static int CompareTo(this string s, string other)
  - 序号比较：返回负数、0 或正数，同 C# 的
    string.CompareTo。

- static bool EqualsOrdinal(this string s, string other)
  - 序号相等比较（字符串的 `==` 本身也按值比较；
    此方法是为了让 C# 风格的代码继续可用）。

- static List<string> ToCharList(this string s)
  - 把字符串拆成单字符字符串列表。Zan 没有
    char[] 值类型，因此这是 C# ToCharArray 的
    List<string> 等价实现。

- static int CountOf(this string s, string needle)
  - `needle` 不重叠出现的次数。


## TaskJoin (class)

扇出汇合（fan-out join）：<c>Task.WhenAll</c> / <c>Task.WhenAny</c> 的
实现。两者不是编译器内建——解析器只把接收者 <c>Task</c> 改写为
<c>TaskJoin</c>（见 parser.c 的 desugar_task_join），因此汇合本身就是
普通的 async 标准库代码，像其他被 await 的调用一样挂起与恢复。

List<long> hs = new List<long>();
hs.Add(Task.Spawn(Work(1)));
hs.Add(Task.Spawn(Work(2)));
int n = await Task.WhenAll(hs);      // 全部完成后返回句柄个数
int i = await Task.WhenAny(hs);      // 最先完成者的下标

完成性由 <c>Task.IsDone(handle)</c> 观察（协程完成或被取消后为真），
等待期间用 <c>Task.Delay</c> 让出：汇合方挂起到 reactor，不占线程、
也不忙等。轮询间隔从 1 毫秒起指数退避到 4 毫秒——短任务几乎立即
汇合，长任务不会每毫秒都唤醒一次。

- static int MAX_BACKOFF=4;
  - 轮询退避上限（毫秒）。

- static async int WhenAll(List<long> handles)
  - 挂起直到 `handles` 中每个句柄都已完成（或被取消），
    返回汇合的句柄个数。空列表立即返回 0，已完成的批次
    不会挂起。

- static async int WhenAny(List<long> handles)
  - 挂起直到 `handles` 中任一句柄完成，返回其下标；
    同一轮里多个都已完成时返回最小下标。空列表返回 -1。
    其余协程继续运行——需要一起收尾就先
    `CancelAll` 再 `WhenAll`。

- static void CancelAll(List<long> handles)
  - 请求取消每个句柄（已完成的句柄无副作用）。取消是
    协作式的：协程在下一个挂起点观察到请求，因此取消后通常
    紧跟一次 <c>WhenAll</c> 等它们真正收尾。

- static int DoneCount(List<long> handles)
  - `handles` 中已完成的句柄个数（不挂起）。


## TimeSpan (class)

一秒精度的时间间隔，以带符号的
总秒数存储。由 `DateTime.Subtract` 或
<c>From*</c> 工厂方法产生。

- long total;
  - 带符号的总秒数。

- TimeSpan(long seconds)
  - 从带符号的秒数构造一个时间间隔。

- static TimeSpan FromSeconds(long s)
  - 从秒数构造：`FromSeconds(90)` = 1 分 30 秒。

- static TimeSpan FromMinutes(long m)
  - 从分钟数构造。

- static TimeSpan FromHours(long h)
  - 从小时数构造。

- static TimeSpan FromDays(long d)
  - 从天数构造。

- long TotalSeconds()
  - 整个间隔的秒数（带符号，精度无损）。

- long TotalMinutes()
  - 整分钟数，向零截断：90 秒 = 1。

- long TotalHours()
  - 整小时数，向零截断。

- long TotalDays()
  - 整天数，向零截断。

- int Days()
  - 天分量（日历式拆分，恒非负）：
    -1.5 天 = Days 1 + 负号（见 TotalSeconds）。

- int Hours()
  - 小时分量（0-23，恒非负）。

- int Minutes()
  - 分钟分量（0-59，恒非负）。

- int Seconds()
  - 秒分量（0-59，恒非负）。

- bool IsNegative()
  - 时间间隔为负时返回 true。

- TimeSpan Add(TimeSpan other)
  - 两间隔相加。

- TimeSpan Subtract(TimeSpan other)
  - 本间隔减 other。

- TimeSpan Negate()
  - 取反（正变负）。

- string ToString()
  - 文本格式为 "[-][D.]HH:MM:SS"。


## Wide (class)

针对 Win32/COM 宽字符（`W`）接口的 UTF-16 封送。
Zan 字符串是 UTF-8，因此宽字符参数是显式持有的缓冲区：

nint w = Wide.Of("https://example.com");
nav(webview, w);
Wide.Free(w);

- [DllImport("kernel32", EntryPoint="MultiByteToWideChar")]static extern int ToWide(int page, int flags, nint mb, int mbLen, nint wide, int wideLen);

- [DllImport("kernel32", EntryPoint="WideCharToMultiByte")]static extern int ToMulti(int page, int flags, nint wide, int wideLen, nint mb, int mbLen, nint defChar, nint usedDef);

- static int Utf8()
  - 代码页 CP_UTF8（65001）。

- static nint Of(string s)
  - 分配 `s` 的 NUL 结尾 UTF-16 副本。用 Free() 释放。

- static string Read(nint p)
  - 将 NUL 结尾的 UTF-16 缓冲区复制回 Zan 字符串。

- static int Length(nint p)
  - 宽字符缓冲区中 NUL 终止符前的 UTF-16 码元数量。

- static void Free(nint p)
  - 释放 Of() 分配的缓冲区（即 NativeMemory.Free）。


## ZanVersion (class)

本标准库随附的工具链版本，程序可直接打印
它（服务启动横幅、关于对话框、`--version`
输出）而无需查询构建系统。

- static string Text()
  - 点分格式的发布版本字符串，例如 "0.2.0"。


## T (delegate)

双向数据绑定背后的存取器对：读取/写入
`target` 的某个字段。当字段左值被赋给 `Binding<T>` 类型的槽时，
编译器会合成匹配的函数（如 `input.data = user.name;`）。

`delegate T BindGet<T>(object target);`


## int (delegate)

GetEnvironmentVariableW 的调用形式（name/buf 为宽字符指针，
size 为缓冲区的 UTF-16 码元容量，返回写入的码元数）。

`delegate int GetEnvironmentVariableWFn(nint name, nint buf, int size);`


## int (delegate)

PeekMessageW 的调用形式（remove 非 0 时从队列取走消息）。

`delegate int PeekMessageFn(nint msg, nint hwnd, int min, int max, int remove);`


## int (delegate)

TranslateMessage 的调用形式。

`delegate int TranslateMessageFn(nint msg);`


## int (delegate)

Win32 Sleep 的调用形式（毫秒）。

`delegate int SleepFn(int ms);`


## int (delegate)

vtable 方法的调用形式：每个 COM 方法都把接口
指针作为第一个参数并返回 HRESULT，宽于
寄存器的参数（RECT、结构体出参）以地址传递。
ComCall0Fn 到 ComCall5Fn 依次带 0 到 5 个指针参数。

`delegate int ComCall0Fn(nint self);`


## int (delegate)

1 个指针参数的 COM 方法形式。

`delegate int ComCall1Fn(nint self, nint a);`


## int (delegate)

2 个指针参数的 COM 方法形式。

`delegate int ComCall2Fn(nint self, nint a, nint b);`


## int (delegate)

3 个指针参数的 COM 方法形式。

`delegate int ComCall3Fn(nint self, nint a, nint b, nint c);`


## int (delegate)

4 个指针参数的 COM 方法形式。

`delegate int ComCall4Fn(nint self, nint a, nint b, nint c, nint d);`


## int (delegate)

5 个指针参数的 COM 方法形式。

`delegate int ComCall5Fn(nint self, nint a, nint b, nint c, nint d, nint e);`


## int (delegate)

CoInitializeEx 的调用形式（返回 HRESULT）。

`delegate int CoInitializeExFn(nint reserved, int flags);`


## int (delegate)

TlsAlloc 的调用形式（返回 TLS 槽号）。

`delegate int TlsAllocFn();`


## int (delegate)

TlsSetValue 的调用形式（成功返回非 0）。

`delegate int TlsSetValueFn(int index, nint data);`


## int (delegate)

CoCreateInstance 的调用形式（返回 HRESULT）。

`delegate int CoCreateInstanceFn(nint clsid, nint outer, int ctx, nint iid, nint result);`


## nint (delegate)

DispatchMessageW 的调用形式。

`delegate nint DispatchMessageFn(nint msg);`


## nint (delegate)

TlsGetValue 的调用形式。

`delegate nint TlsGetValueFn(int index);`


## void (delegate)

`delegate void BindSet<T>(object target, T v);`


## void (delegate)

CoUninitialize 的调用形式。

`delegate void CoUninitializeFn();`


## void (delegate)

CoTaskMemFree 的调用形式。

`delegate void CoTaskMemFreeFn(nint p);`


## ConsoleColor (enum)

16 种标准控制台颜色，顺序（0..15）与 C# 的
System.ConsoleColor 一致。可赋给 Console.ForegroundColor 或
Console.BackgroundColor；运行时将其映射为 ANSI SGR 转义序列。

- Black

- DarkBlue

- DarkGreen

- DarkCyan

- DarkRed

- DarkMagenta

- DarkYellow

- Gray

- DarkGray

- Blue

- Green

- Cyan

- Red

- Magenta

- Yellow

- White


## IDisposable (interface)

标准释放契约：持有原生资源的对象实现它，`using` 语句
在作用域结束时调用 `Dispose`。

- void Dispose();
  - 释放对象持有的资源。
