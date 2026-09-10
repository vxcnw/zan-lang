---
name: zan-compiler-internals
description: zanc 编译器内部（parser/checker/irgen）的实测定式与坑——Dict 内建布局契约（插入序 keys/values + 惰性哈希索引 + Remove 整体失效）、LLVM select 两臂都求值导致的死臂分配泄漏（用 branch+phi）、delegate 两形态与 wasm32 函数表索引撞 ZAN_CLOSURE_TAG 的根修定式（形状按 target_is_wasm32 条件化）、ARC 所有权判定内建优先于 extern 借用（GetString 误判=每 HTTP 请求泄一条请求头）、looks_like_var_decl 的内建关键字分派契约（rank specifier 必须容忍逗号）、stdlib 按需拉入的四坑（扩展宿主关键字接收者/方法名撞类名/泛型委托假名 T/#if 区域必须带宏扫描）、交叉工具链 .o 重出配方（zig cc + build/ 暂存副本不会自动刷新）、可空值类型在字符串位的解包形状、编译器调试的 scratch 卫生（bisect 用 worktree 即用即删、A/B 对照复用固定目录名）。做或改 src/compiler/*、交叉运行时对象、conformance golden 时使用。
---

# zanc 编译器内部定式与坑

> 提炼自 standard 层存量挂账清零批（2026-09-09：int[,] 回归、Dict.Remove
> 保序、string+可空拼接、交叉 rt 对象重出）。每条都实测踩过。

## Dict 内建（irgen.c 布局注释 = 契约）

- 布局 8 字段：`{i64 count, i64 capacity, i8** keys, i64* values, i64* index,
  i64 index_capacity, i64 indexed_count, ...}`。**keys/values 并行缓冲保持
  插入序**（枚举序与 ARC 释放序都依赖它），`index` 是开地址哈希索引（存
  entry+1，0=空），由 `__zan_dict_find` 惰性重建——重建判据
  `indexed_count != count` 或 `index_capacity==0`。
- **Remove 必须保插入序**：swap-remove（末项搬进洞）曾让 Keys/Values 离开
  插入序，违反布局契约、偏离 C# 可观察行为。正确形状 = memmove 下移洞上
  方全部条目（键 1 词、值 value_words 词）+ **索引整体失效
  （indexed_count=0）**——洞上方条目全部重编号后任何增量索引修复都不可能，
  find 的 stale 判据天然触发全量重建。Remove 变 O(n) 与 shift 同阶，可接受。
- find 的 append 快路径（只索引新追加的键）有 `kept = icnt > 0` 守卫，
  icnt=0 不会误入快路径——整体失效与增量追加逻辑兼容。
- tail 槽清零不能省（ARC 不得见脏引用）；memset 按 libc 真身
  `(ptr,i32,i64)->ptr` 调（get_libc_fn 按名字取先到声明，签名不一致
  verifier 直接拒）。

## LLVM 陷阱

- **`LLVMBuildSelect` 两臂都求值**。字符串化之类会分配的辅助（itoa64 的
  数字缓冲）放进 select 死臂就是泄漏——leakcheck 孪生测试当场抓。要用
  branch+phi：两块各算各的，merge 处 phi 合流。
- 返回 NULL 字符串是合法的空串形状：emit_str_concat 有 NULL→""、
  zan_rt_str_release 有 NULL 守卫，全链路安全。

## delegate 两形态与 wasm32 的 tag 碰撞（2026-09-10）

- **形态契约（zan_abi.h）**：delegate 值一个指针两形态，bit 0 区分——偶数
  =裸 fn 指针（静态方法组/无捕获 lambda），奇数=tag 过的堆 closure 记录
  `{fn,dtor,target,<captures>}`，invoke 是 `fn(rec, args...)`（rec-first）。
  runtime 侧 store-family（rt_sync 的 dispatch 队列、gui_runtime_wasm 的
  wdisp）用 `v & ZAN_CLOSURE_TAG` tag-test 收纳两形态，retain 打
  `rec-16` 的 rc 槽。
- **wasm32 没有真实函数指针**：裸 fn 是 wasm 函数表索引（小整数，奇偶皆
  有），奇数索引撞 tag 位 → irgen 把表索引解引用成记录，fn 槽读到索引处
  内存 → 浏览器报 `null function at <调用帧>`。**修法是形状按目标条件化
  （irgen_expr.c `target_is_wasm32(g)` 门控），native/wasm 各自复现历史
  契约**：native 全裸形状零变化；wasm32 全走 tagged record——静态方法组
  造 `__zan_mg_<method>` thunk 记录（thunk 丢 rec 调 target），thunk 同放
  fn+target 双槽保 `E+=M;E-=M` 相等性语义（equality 按 target 槽比对），
  dtor/retain 跳过 target 槽（是函数非对象）；无捕获 lambda 也走 rec-first
  （`is_closure || target_is_wasm32`）。C 回调 cast `(nint)M` 走裸 fn 指针
  路径（emit_raw_fn_for_cb_cast），与记录互不干扰。
- **根修兜底（2026-09-11）：wasm 链接加 `--table-base=2`（main.c wasm-ld
  命令行）**。lld 默认表基址 1，地址取函数的表索引奇偶皆有——任何漏网
  的裸 fn delegate（如 `inp.Size = vm.x` 合成 Binding 访问器曾是裸指针，
  `emit_binding_acc_delegate` 已按 mg 形状收口）都会撞 tag：索引 N 被当
  tagged 记录 untag 成 N-1，间接调用恰好落进相邻函数（实测 Canvas_DrawGlyph
  落进 getenv）。表基址挪到 2 后裸索引恒为偶，native 的「偶数才合法」
  假设在 wasm 上成立，整族漏网点一次性免疫。
- **教训**：中间层用「指针低位 tag」复用值位时，必须审计目标平台上"这个
  位模式是否真的不可能出现"——函数表索引/句柄/压缩指针都可能撞 tag。
  新 target 落地时对"native 偶数才合法"的隐含假设逐个显式化。

- **跨调用保活 delegate 必须 retain，线程入口必须 tag-test（A70/A261，
  2026-09-11）**：`Thread.Start(job.Run)`（实例方法组 = tagged closure 记录）
  此前在 native `zan_thread_start` 里被原样当裸 `void(*)()` 调用 → 启动瞬间
  SIGSEGV；同形的 `Thread.Start(() => {...})`（捕获 lambda）一样崩，裸静态
  方法组却正常（checker 不拦，编译期无诊断）。native 两路（Win32
  CreateThread / POSIX pthread_create）与 wasm 版、UI 派发队列同构化：
  trampoline 先 `v & ZAN_CLOSURE_TAG` 判形态（带 tag 就卸 tag 取记录 fn 槽按
  `fn(rec, ...)` rec-first 调；裸指针才直接调），`zan_thread_start` 侧
  `zan_delegate_retain(body)`、trampoline 收尾 `zan_delegate_release(arg)`。
  **retain 是必需的，不是保险**：调用方在 `Thread.Start(...)` 语句结束就释放
  自己的临时量，工作线程可能还没跑（实测去掉 retain 后 `-g` 下即段错误）。
  **通则：任何把 delegate 存下来留给"另一次调用 / 另一线程"执行的 runtime
  入口，都要对到达时的那个值补 retain、在真正的执行点补 release**——这正是
  zan_abi.h store-family 契约的要求。

## wasm32 局部数爆炸：V8 每函数 5 万局部硬上限（2026-09-11）

- **症状**：浏览器 `WebAssembly.instantiate` 报 `Compiling function #N:"X"
  failed: local count too large`。V8 上限 50,000 局部/函数；gui_gallery 的
  RenderPreviewEx（1.1 万行 IR）在默认档发出 116,222 个局部。
- **根因**：默认档（ZAN_OPT_NONE）走 `fast_codegen`→`LLVMCodeGenLevelNone`，
  wasm 后端零 stackify，几乎每条 IR 中间值都落成一个 wasm local（11.3 万
  IR 行 ≈ 11.6 万局部，一比一）。wasm32 上跳过 `fast_codegen`（main.c
  `if (!irgen.target_is_wasm) irgen.fast_codegen = true;`）后同一函数 731
  局部，全模块 max 731，编译 60s 可接受。**诊断工具**：解析 wasm code
  section 的 ULEB local 声明即可按函数计数（`_scratch` 里现成
  wasmlocals.py/wasmname.py 思路：导入函数计数偏移 + 每函数 `count×valtype`
  对求和）。
- **DLLImport nint 的坑**：`map_type` 对 TYPE_NINT 恒发 i64（所有 target）。
  embedres.c 往 File.zan 的 `nint zan_embed_bytes` 声明里塞函数体时，返回
  值必须按声明的实际返回类型 coerce（ptrtoint）；x64 宽度撞对掩盖了非法
  IR，wasm32 的 32 位指针立刻 `type error in return[0] (expected i64, got
  i32)`。凡「编译器合成的函数体装进 DllImport 声明」都要查这一层。
- **wasi-libc getenv 在 zan shim 下崩**：libc 惰性 environ 初始化走 zan
  WASI shim 的空 environ 契约，strncmp 读野指针 OOB（只在分配压力大、
  渲染中途首次 getenv 时炸，启动时探针复现不了）。H5 无环境变量——
  rt_sync_wasm.c 直接 stub `getenv→NULL`（显式 .o 优先于 libc.a 档案）。
- **stdlib 快照坑**：wasm gallery 构建用 `--stdlib-path _scratch/h5gui/
  stdlib_min`（带 WASI 分支的裁剪快照），**repo stdlib 的修复必须镜像进
  快照**（Effects.zan TakeDamage 首帧 null 守卫），否则构建用的还是旧代码。

## 泛型实例化定长表：第 64 个起静默丢弃（A78-3，2026-09-11）

- `irgen_emit.c` 里两张"按实例逐份"的表曾用定长栈数组：`variants[64]`
  （每实例一份方法体）与 `insts[64]`（泛型类静态字段的按实例初始化器）。
  `variants` 有一槽留给擦除版，循环守卫 `nvar < 64` 只装得下 **63** 个具体
  实例化：第 64 个实例化的专用体 `Wrap_Show$T63` 从未发射，调用点
  `route_generic_method` 查 `find_generic_fn` 落空后**静默退回擦除版**，而擦除
  版的体就是 `call abort(); unreachable` → 程序无输出、退出码 3。同族的
  `insts` 从第 65 个起静默丢弃，那些实例化的静态字段停在 0。
- **触发条件是"体的发射需要按实例特化"**（体里用到类型参数，如 `Wrap<T>` 的
  `Show()` 调 `item.Name()`）。只靠擦除形态就够的实例化（类实参、体不碰 T）
  到 100 个也正常——所以早期记录把它误判成"≥64 个实例化堆损坏、非确定性、
  ASLR 相关"，实际是**确定性的运行期 abort**，只跟"需要几份专用体"有关。
- **修法**：两张表改按需倍增的堆数组。**任何容量上限都不许静默截断**——截断
  等于悄悄改变行为，且症状与原因相隔极远。
- **诊断定式**：`ZANC_TRACE=1` 下 `discover_generic_insts` 报实例化总数、
  `route_generic_method` 在"具体实例化找不到专用体而退回擦除版"时报
  `route miss: Type.Method argc=..`——见到 `route miss` 就是这张表漏了实例。
- **回归**：`tests/conformance/generic_inst_count_70.zan`（70 个实例化，同时
  覆盖 64 边界的专用体与 65 边界的静态初始化器）输出 `2485/70`。

## 调用形状：接收者槽必须按静态性判定（A270，2026-09-11）

- `obj.Method(args)` 在 irgen_call.c 里按接收者形态走**两条互不相交的分支**：
  局部变量接收者（`local.Method(...)`）与表达式接收者（`expr.Method(...)`，`if (recv_cls)`）。
  两条都必须先判 `method_sym` 的 MOD_STATIC：静态方法签名里没有接收者槽，契约是
  「不传接收者」（另一分支的注释明写 `expr.StaticMethod(args)` is legal；C# 会 CS0176
  拒绝、Java 允许，Zan 选了允许）。
- 局部变量那条曾**无条件** `argc = args.count + 1`、把接收者塞进 slot 0、参数整体后移
  一位 → 静态方法调用生成 3 参 call 打 2 参函数，LLVM 校验报
  `Incorrect number of arguments passed to called function!`；报错点离调用点很远，调用者
  只看得到一个参数个数不符的 call。触发面就是 `d.StaticMethod()` 这一种写法
  （`tests/gui/compref_designer_test.zan` 曾长期挂在 standard 档）。
- **定式**：新增或改动任何 call 发射分支，先问三件事——接收者槽要不要（静态性）、
  参数索引用不用偏移（`recv_off`）、`emit_dispatch_call` 的类参数要不要传（静态方法
  没有 vtable，传 NULL 走直接调用）。三者是一组，漏一个就是形状错配。
- **归属定式**：这类"参数个数不符"报错不明说谁多传了，定位靠最小探针 + 逐一遍历接收者
  形态（局部 / 字段 / 临时 / 类型名）；并用**旧编译器快照**证明是既有缺陷而非本轮引入
  （本次用 `_scratch/zanc_head.exe`，2026-09-03 构建，同探针同样复现）。

## parser：looks_like_var_decl 的分派契约

- 内建类型关键字开头的语句要在「声明」（`int x = 3`、`int[] a`）与
  「表达式语句」（`int.Parse(s)`）之间分派，实现是裸源码扫描找 `.`。
  **扫 `[` 档位时必须容忍空白+逗号**——`int[,]`/`int[,,]`/`int[][,]` 的
  rank specifier 里是逗号，只认 `]` 就把整个语句误判成表达式
  （cs_b08_arrays 回归的根因）。混合档 `int[][,]` 也要过。
- 单行多声明符 `int a = 0, b = 2;` 走 pending_stmts 队列 + 三个语句收集点
  splice；comma 循环只吃 `IDENT [= expr]`。

## 字符串位的可空值类型

- C# 语义：`"a=" + int?` 合法，null 拼空串。checker
  type_is_concatable 对 TYPE_NULLABLE 递归放行元素可拼的；
  irgen emit_to_cstr_of 对 `zan.nullable.<payload>` 命名结构解包——
  has ? cstr(payload) : NULL（branch+phi，见上）。无符号元素
  （uint?/ulong?）要传 emit_to_cstr_u 的 unsigned 旗标。
- `Convert.ToString(int?)` 与 `.ToString()` 直接调至今会炸 verifier
  （nullable 结构按值进了 itoa64 形参）——拼接路径能走是因为有解包；
  直接调用是另一个待修缺口。

## 交叉运行时对象（toolchain/*/*.o）重出配方

- 源头 scripts/build_cross_rt.cmd 用 zig cc（本机无安装时：
  C:/Users/QQ/Downloads/zig-x86_64-windows-0.15.1.zip 解包即用；
  NDK 块要 ANDROID_NDK，OHOS 块要 OHOS_NDK）。
- **build/ 里的暂存副本不会自动刷新**：zanc 链接后处理的「自包含工具链
  打包」对已存在的 build/macos/ 等目录直接 skip——重出 toolchain/*.o 后
  必须手动 cp 进 build/<target>/，否则链接（--emit-lib、交叉 exe）用的
  还是旧对象，测试照样挂。
- ELF so 链接容忍未定义符号（运行期才炸），Mach-O dylib 链接期即拒——
  运行时新符号没进交叉对象时，只有 macos dylib 测试会报警，别被
  「只有 mac 挂」误导成 mac 特有问题。
- toolchain/** 的 *.o 命中 gitignore，提交要 `git add -f`。

## win-arm64 交叉 rt：setjmp 降层与 rt_crash 架构门（实测踩坑 2026-09）

- **生成的 `_setjmp` 在 aarch64-windows 链不上**：ARM64 的 msvcrt.dll 根本
  没有 `_setjmp` 导出（mingw setjmp.h 原话 "ARM64 msvcrt.dll lacks _setjmp,
  only has _setjmpex"），x64 那套「两参调用形状逼 LLVM 生成 rdx=返回地址
  前导」也是 x64 专属。irgen_builtins.c `emit_eh_setjmp/emit_eh_longjmp`
  已按目标降层：aarch64-windows 发静态对 `__mingw_setjmp(buf)`（入口 Lr
  即返回地址，无需前导）+ `__mingw_longjmp`，两端布局一致，libmingwex.a
  里就有；x64 路径一字未动。
- **rt_crash.h 的 guard 恢复是 x64 专属**：`__builtin_setjmp/longjmp` 在
  aarch64-windows 没有后端，CONTEXT 字段名也分架构（x64 Rsp/Rip，ARM64
  Sp/Pc，用 ZAN_CTX_SP/PC 宏）。恢复机（guard_recoverable/rip_recoverable/
  guard_resume/guard_log_deferred + setjmp 帧）整体收进 `#if x64` 门；
  非 x64 的 `zan__guard_call` 保留一次性崩溃记录器安装后直通执行——崩溃
  照常有 first-chance 记录，只是不做恢复续跑。头注释里写明这个降级。
- **ohos 交叉链接的两个暗坑**：(1) 链接行强制要求 toolchain\ohos-<arch>\
  zap_main.o（XComponent 壳适配），缺了报「sysroot subset not found」，
  但源 zap_main.c 只在 ohos-x64 目录里跟踪、.o 两架构都不跟踪也没脚本造
  ——build_cross_rt.cmd ohos 块现已补 zap_main.o + libEGL/libGLESv3 空占位
  so（scripts/ohos_stub.c）的构建配方；(2) `-shared` 默认容忍未定义符号，
  ohos 链接成功≠符号齐——要 `llvm-nm -D` 看未定义表再去 OHOS libc.a 里
  对（musl 有 `_setjmp`/`_longjmp`/`longjmp`，加载期可解析）。
- 重出对象名是 `zanrt_*.o` 前缀（build_win_rt.sh 协议），别把裸 `rt_*.o`
  拷进 toolchain/。OHOS NDK clang 15.0.4 在 DevEco Studio 安装目录的
  native/ 下。

## conformance 处置四分法

挂的测试先归因再动手：「stale golden」（重生成，逐行核对 C# 拼写）、
「实现违约」（修实现——布局注释/文档注释就是契约，「注释与实现打架时
先查 git 考古谁先谁后」）、「测试源不合法」（C# 也拒绝的写法改测试源，
如无约束 T 的 string 拼接改 .ToString()）、「真回归」（git 考古最后
通过点定位元凶提交修编译器）。混着处置就会把行为改错。

## ARC 契约：DllImport 的 string 返回值是借用指针，永不释放（内建除外！）

- **内建优先于 extern 借用规则（A262，2026-09-10）**：`NativeMemory.GetString`
  是编译器内建（emit_native_memory_call，irgen_expr.c 用 emit_string_alloc_rc
  建真 ARC 串、memcpy、NUL 收尾，交调用方 +1），`[DllImport]` 声明只为
  checker 提供类型。extern 借用判定必须先给内建开白名单
  （`is_call_to(e,"NativeMemory","GetString") && args==3` → return 1），
  否则所有消费点（实参临时/丢弃/局部捕获/返回）各泄一条串——stdlib 里
  ByteBuffer.Str → HttpFramer.Head/Slice/ReadBody 等约百处调用全中招，
  服务端每 HTTP 请求泄一份原始请求头，RSS 线性上涨（WSL 3×60s 登录压测
  13.7→313 MB；修复后 10.3→13.1 MB 趋平）。诊断定式：**泄漏报告的分配点
  不是泄漏原因**（报在消费点，根因在所有权判定）；**RSS 随请求数线性
  上涨=每请求泄漏，段间恒定=有界设计成本**；async frame 对 `this` 的
  receiver-retain（防 fluent 接收者 use-after-free）是设计内所有权，
  leakcheck 残余 1 条非缺陷。
- **新内建必须同步借用白名单（A264）**：白名单按内建名逐个枚举，
  nm_sha256_fn（NativeMemory.Sha256）落地时 expr_yields_owned_rc_value
  同步补 `is_call_to(e,"NativeMemory","Sha256") && args==2`——**加内建
  不加白名单 = A262 的复刻**，且泄漏只在真实调用方出现，编译器自身
  测试照绿。
- **expr_yields_owned_rc_value 对 extern 调用必须返回 0**（irgen_generics.c）：
  声明返回 `string` 的 bodyless [DllImport] 返回的是裸 `char*`——extern 内存
  或**调用方传入的缓冲**，没有 rc 头。通用丢弃路径（AST_EXPR_STMT）把所有
  AST_CALL 结果当 owned(+1) 去 release，就会把别人的内存放掉：stdlib 的
  `getcwd(b, 4096)` 返回指针落在调用方 `byte[]` 上，release 经
  zan_rt_str_release 的数组转发臂把数组引用减到 0 → free → musl mallocng
  把整组 16KB unmap → 随后 b[n] 扫描读已卸载页 SIGSEGV。Windows 分支不走
  getcwd 所以模板只在 Linux 上崩（诊断时先看平台分支差异）。修法是给
  expr_yields_owned_rc_value 的 AST_CALL 分支加 extern 判定
  （extern_check_callee_sym + sym_declares_extern + method_ret_type_at），
  void/string 返回一律借用。conformance 用例
  tests/conformance/extern_borrowed_string_result（getcwd 三次全读）。
- **platform-defining DllImport 会被 irgen 内建短路**：`Directory.\
  GetCurrentDirectory`/`SetCurrentDirectory` 在 irgen_call.c 有内建降层
  （!zan_type_defines 才生效）——探针里自己写 Directory 类会静默走 stdlib
  版本，写别的名字才有效。
- **musl 静态链内存布局速查**：cross 链接带 zanrt_mem.o + --wrap 时
  ≤2048B 走 zan 槽位分配器（1MiB 对齐 slab，指针 & ~0xFFFFF 可判归属），
  >2048B（如 4096 的 getcwd byte[]）落 musl mallocng 的 mmap 堆
  （0x7ffff7xxxxxx 段）；崩溃地址落在 mallocng 元数据检查
  （__malloc_allzerop）且 RSS 平台化后不重现，优先怀疑高压竞争而非
  Zan 侧 UAF——先用低速率复跑分型。

- **消费方要留引用时，拥有所有权的临时接收者必须释放（A269，2026-09-11）**：
  委托绑定（`Action a = new Job(i).Run;`）与 retained 字段读一样，会让闭包
  记录 retain 接收者（`emit_closure_record(..., retain_target=true)`），但方法组
  这条路径原先没有像 `finish_member_of_temp` 那样把"临时量自带的那一份 +1"
  释放掉 → 每次 `new Job(i).Run` 恒定泄漏一个 `Job`（20000 次循环泄漏 20000
  个；`--check-leaks` 报的分配点是那行 `new`，一眼看像"新对象泄漏"）。修法：
  把判据抽成 `receiver_is_owned_temp`（`obj_val && is_rc_managed_type(obj_type)
  && !expr_is_local_ident(object) && expr_yields_owned_rc_value(g, object)`），
  字段读与方法组绑定共用；**局部变量接收者不释放**（它不拥有 +1，释放会提前
  free）。诊断定式：**泄漏报告的分配点是"被泄漏的对象"，不是"忘记 release 的
  那条路径"**——按"谁 retain 了它"反查消费点（这里是 emit_closure_record 的
  retain_target），别只盯着 new。

## 字节串 ABI 契约（stdlib crypto EVP 换装踩坑，2026-09-10）

- **byte[] 按 string 形参传入时 `.Length` = strlen**：共享的是 payload
  指针，没有数组头，长度按 0x00 截断——Hex.Decode 产物首字节为 0 时
  `.Length==0`。stdlib 旧 crypto 从不读缓冲参数的 `.Length`、只索引；
  新代码加 `.Length` 门禁会把合法密钥/密文判空（Aes.zan:127 报
  "list index out of bounds" 的根源）。缓冲参数只判 null。
- **GetString 产物不能写字节**：`s[i]=x` 触发长度缓存失效
  （emit_string_len_invalidate），之后按 strlen 重 derive，NUL 开头的
  内容坍缩成长度 1，第二次写就越界。GCM tag 这类含 NUL 的编组必须走
  `byte[]`，仅在 extern 调用边界 `string tagBuf = tagB` 零拷转换。
- **同符号异形参用 EntryPoint 别名**：`[DllImport("crypto",
  EntryPoint="EVP_EncryptUpdate")] static extern int EVP_EncryptUpdateS(...)`
  ——发明不存在的符号名链接期才炸；string 形态做零拷输入（CBC 2→196
  MiB/s 的差额全在这一次字节拷贝）。
- **EVP 单块 ECB 两方向都要 `set_padding(0)`**：解密侧 PKCS#7 默认把
  末块扣在 Final 里，Update 返回 0 块（表现为"解密全零"）；SM4 微信
  无 pad 语义同款。EncryptCbc 返回精确长度数组（golden 断言 ct.Length，
  多给的 len+32 破档）；调用方对 outLen `List<int>` 预 `Add(0)`（空表
  写 [0] 是 fail-soft：报错但继续，错误会漂到别处爆）。
- **Zan 逐字节循环 ~130 MiB/s（1 MiB≈8ms），热路径字节过 native 边界
  进出两个方向都必须零拷贝**：进=byte[]→string 形参直传（上一条）；
  出=native 写进**精确长度预分配**的 byte[] 原样返回（CBC 加密 PKCS#7
  长度加密前确定 `(len/16+1)*16`；GCM 流式等长；仅解密剥填充会缩——
  未缩原样返回、缩则一次 `EntryPoint="memcpy"` 收缩，byte[] 形参直传
  载荷指针，File.EmbedCopyIn 同款）。坑：A264 只零拷了输入侧，吞吐立
  即被输出侧的"len+32 上界分配+逐字节收紧拷贝"钉死在 ~200 MiB/s
  平板（与算法无关=与 native 库无关=拷贝循环在扛），输出零拷贝后
  CBC 1267-1319 / GCM 2000-4413 MiB/s（raw 的 88-96%）。

## stdlib 按需拉入（demand-driven pull-in，2026-09-10）

> 以前 `using Gui;` = 目录全量 glob + 传递 using 扫描到不动点，一个空窗口
> 程序 parse 380 个文件、2.8s，且 stdlib 树里任何文件有语法错全体拖垮。
> 现在目录内文件按"声明名被拼写"过滤后才 parse（`main.c` 的 pi_* 块），
> 空窗口 269 文件、纯 hello 3 文件 0.3s。语义等价性靠 conformance 三件套
> （pullin_shadow_same_name / pullin_extension_host / pullin_qualified_escape）
> 钉死。

- **词法级名字匹配的四个假阳性/假阴性坑，全踩过**：
  - 扩展方法宿主是"不可见名字"（调用处只写 `s.CompareTo(...)`），必须当
    锚点无条件拉入。识别形状是 `( this Type`——**Type 常是内建关键字
    token**（`this string s` 的 string 是 TK_STRING 不是 IDENT），只认
    IDENT 会漏掉所有内建类型扩展；`M(this.x)` / `M(this)` 是表达式不算。
  - 方法名撞 stdlib 类名（用户方法 `Label()` vs `Gui.Widget.Label`）：
    种子阶段"点号链根是命名空间段"才把链上名字当拉入信号；类型体内
    `类型 + IDENT + (`/`{` 是方法/属性**声明**名，不标活。否则一个
    `b.Label()` 级联拉进整个 Gui。
  - 泛型委托 `delegate T Mapper<T>(T x)` 的名字 = `<>` **外**最后一个
    IDENT；不跳泛型参数会把 "T" 铸成声明名，此后任何文件提到 T 全量
    级联。
  - 扫描必须带与真实 parse 相同的 `-D`/target 宏：`#if` 停用区里的引用
    不进种子（ZanGen 的 Main 整个在 `#if ZAN_GEN_MAIN` 里，Gen* 类全靠
    它引用）。
- **用户同名类遮蔽**：用户自己 `class App` 时未限定 `App` 永远解析到用户
  自己的，不拉 stdlib 同名文件；限定 `Gui.App` 仍拉。这是 stdlib 模板
  （App/Window/Button 全是常见词）不级联的关键。
- 门控：`--emit-symbols` 恒全量（IDE 索引要完整 stdlib），`ZAN_NO_PULLIN_FILTER=1`
  回退旧行为，`ZAN_PULLIN_DEBUG=1` 打印每个文件的拉入原因（含命中名）。
- 语义等价验证定式：同一程序 `ZAN_NO_PULLIN_FILTER=1` 开关两态编译运行
  diff 输出；改拉入逻辑必须补 conformance 用例并跑 smoke+standard。
- 顺带的实证：**prune 已保证未用代码不进二进制**（关 prune 只多 7KB），
  "using Gui 导致 exe 10MB"是错觉——Gui 窗口 exe 的 1.6MB .text 是
  GuiHost→App/Style/Fx 的活代码闭包 + Zan 运行时，与 unused 无关。
- stdlib 文件引用跨命名空间类型必须写 using（ChartHost 曾裸写 `App`，
  靠用户程序恰好也有 `class App` 才碰巧编译——prune 把它藏成了哑弹）。

## 并行会话下的 ctest 假红（2026-09-11）

同一工作树里有别的会话在改 stdlib 时，standard 档会出现**与自己无关的红**。
先归因，别急着改自己的代码：

- **编译/检查类失败**：报错落在某个 stdlib 文件、而该文件在工作区是 `M`（在途
  改动）→ 属于那条车道。关键判据是**报错来自哪个阶段**：只改了 irgen/runtime
  时，checker/binder 的报错（"after type checking"、未解析调用、null 安全）不
  可能是你引入的——那些阶段在你的改动之前跑。
- **陈旧产物导致的挂起/超时**：`tests/run_case.cmake` 只在 exe 不存在或比
  `.zan` 源旧时才重编，**不看 stdlib 时间戳**。别的会话在你上次跑之后改了
  stdlib，ctest 仍会复用旧的 `build/conf_*.exe`，于是出现"单跑必挂、手编必过"
  的怪象（本次 `conformance_gui_listview_scrollbar_drag` 挂死在 5:09 的中间态
  产物上 10 分钟，`rm build/conf_<name>.exe` 重编即 PASS）。
- **归因顺序（四步）**：单跑该用例 → 删 `build/conf_<name>.exe` 重编单跑 →
  手工 `zanc` 编译 + 直接跑 exe → 旧编译器快照（如 `_scratch/zanc_head.exe`）
  复现。四步都指向"不是我"再继续；否则停下来查自己。
- 另一条常客：**端口/资源竞争与真 flaky**。判别法是把**同一个二进制**（不重编）
  连跑 5 次——通过/挂起交错就说明是被测代码里的竞争，单次的超时/失败不能当回归
  （本次 `conformance_gui_listview_scrollbar_drag` 同一 exe 3 过 2 挂，而它属
  Gui 车道在途改动；`conformance_http_client_keepalive` 则是全量并行 120s 超时、
  单跑 0.5s 过，属端口竞争）。并行档的超时值一律先单跑复核。

## 编译器调试的 scratch 卫生（bisect / A-B 对照）

> 2026-09 清理时 `_scratch` 已积到 48G：bisect 整树、A/B 快照、stdlib
> 副本、SDK 解压双份只进不出。清理是任务收尾的一部分，不是可选项。

- **bisect 用 `git worktree add _scratch/xxx_wt <commit>` 开树**，定位完
  当场 `git worktree remove --force` + `git worktree prune`。裸 `cp -r`
  出来的树不带注册，事后没人记得它是谁的；曾清出 b3_wt~b22_src 二十来棵
  整树（每棵 250M+），其中还有已掉注册的 worktree 残骸——目录在、
  `git worktree list` 没有，就是纯垃圾。
- **A/B 对照（新旧 zanc 行为对比）复用固定目录名** `_scratch/zanc-good` /
  `_scratch/zanc-mine`，下次覆盖使用，不新起名字；对照一结束两个目录就
  是垃圾，当场删。stdlib 整树快照同理——head-stdlib、pristine2、
  stdlib-fixed 这类一次名快照只会越攒越多。
- **下载的 SDK/源码包先解压验证、随即压缩包与解压副本二选一**（llvm-dl
  与 ohos-probe 的双份并存一次占 10G）。要长期留的大件写一页 README
  （是什么+怎么再取），`scripts/clean_scratch.ps1` 会跳过带 README 的
  条目，其余按 7 天清。
- **提交前自检**：本次会话在 `_scratch` 造的东西还在吗？在，删掉再提交。
  会话验收只看"任务完成"，没人替你收尾。
