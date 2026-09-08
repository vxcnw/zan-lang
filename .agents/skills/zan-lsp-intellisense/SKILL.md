---
name: zan-lsp-intellisense
description: Zan LSP（src/lsp/zan-lsp）与 intellisense 引擎的供数定式与验证方法——stdio JSON-RPC 探针（scripts/lsp_baseline_probe.mjs 三档场景）、索引收敛跳过目录、工具链 stdlib 按 exe 相对规则入共享项目索引、goto-def/成员补全的数据来源（g_project_intel 回退 + 手写 stdlib_classes 表的局限）、INTEL_MAX_COMPLETIONS 容量挤占坑。做或改 zan-lsp、intellisense.c、LSP 补全/导航/诊断供数，或量 LSP 延迟/命中率基线时使用。
---

# Zan LSP 供数与基线

> 提炼自四期 LSP 改造（基线 094d28f0 / 收敛+stdlib 1ecf29d8 /
> typed member completion 第二批）。
> 每条都是实测踩坑后验证过的。

## 数据流（改供数前必读）

- **线程模型（四期2 第三批起）**：dispatch 全程持 doc_lock（串行，
  与单线程时代语义一致）；didChange 在请求线程只做 range 拼接 +
  便宜的项目索引刷新，昂贵的编译器前端跑在 worker 线程（编辑静默
  200ms 后快照→无锁跑→publish）。协议帧经 lsp_write 的 write_lock
  串行化。改诊断/编辑路径时别把共享状态碰出锁外，也别把前端跑
  挪回请求线程——那是这个批次修掉的 46–63ms 击键阻塞。
- 补全/导航的数据源有两层：打开文档的即时解析（每次请求新建
  intellisense_t 单文件解析）→ 未命中回退 `g_project_intel`
  （工作区扫描 + stdlib 一次性解析，共享缓存）。
- **stdlib 不在工作区里**：用户项目根（templates/*、IDE 打开的任意
  项目）不含 stdlib，靠 `lsp_stdlib_root()` 按 zanc --auto-stdlib 同款
  exe 相对规则（`exe_dir/../stdlib`，ZAN_STDLIB 环境变量覆盖）定位后
  `ensure_stdlib_indexed()` 一次性 `intel_index_project` 进共享索引。
  动供数逻辑先跑 ra2/gallery 探针确认 goto-def `l.Add` 与 `app.` 补全
  不回退。
- 成员补全对 stdlib 类型有张**手写表**（intellisense.c `stdlib_classes[]`，
  只覆盖 File/Math/Thread 等一小撮）——表外的类型（App、Control、
  Designer…）要靠索引里的类体解析。手写表补条目是权宜，正解是
  前端类型信息。

## 已量过的坑（别再踩）

- **索引发散**：walker 只跳 bin/obj/build/.git 时，仓库根 19 分钟
  不收敛 RSS 2.7GB——_scratch/dist 里的探针产物会被逐文件解析。
  跳过目录改动在 index_skip_dir 一处（两平台 walker 合用）。
- **INTEL_MAX_COMPLETIONS 容量挤占**：接收者解析不出类型时成员
  补全退化为全项目符号倾倒（`d.` 返回 64~203 条），目标成员被
  挤出容量上限——表现为"有结果但没命中"，不是空。别把它当
  索引缺失去修。
- **首开代价**：项目扫描 + stdlib 解析落在首个 didOpen 的诊断上
  （实测 +2.4~16.6s 视根大小）。把它挪进后台/懒化之前，先想清楚
  首次补全请求会接住同样的代价。
- didChange 已是增量同步（change:2）+ 静默合并诊断：didChange→诊断
  延迟读数约 200ms+ 是**设计值**（静默窗），不是回退；看
  completion-after-change 指标判断击键是否被前端跑阻塞。探针的
  didChange 段带拼接正确性断言（垃圾行注入/清除），改编辑路径必跑。
- **接收者解析必须文档优先**：把 `d.` 的接收者名直接喂项目索引
  intel_resolve_type，反向扫描会被任何无关文件里的同名变量顶掉
  （后者覆盖前者）→ 成员列表整批是陌生类型的。先对打开文档的
  intellisense_t 解析，解析不出才回退项目索引；项目成员与文档局部
  结果要**始终合并去重**，`count==0` 才回退会让项目成员在文档局部
  有 1 条结果时整体缺席（四期2 第二批修的就是这两处）。
- **探针 offset 是按"匹配起点"数的**：completion 查询的 offset =
  正则匹配起点到光标的字符数，光标要落在 `.` 之后。正则一变
  （比如前面多包了 `string saved = `）offset 全作废——光标落在
  标识符中间发出去的是普通前缀补全（返回几百条），极易误诊成
  "某成员未入索引"。改查询先重数 offset。

## 验证仪式

1. `cmake --build build` 后必跑 `build/lsp_integration_test.exe
   build/zan-lsp.exe`（UTF-16 位置编码回归，PASS 一行）。
2. `LSP_PROBE_MODE=ra2 node scripts/lsp_baseline_probe.mjs`（秒级）
   看补全 P50/命中率/goto-def；`LSP_PROBE_MODE=gallery` 看 stdlib
   类型成员补全；`repo` 模式是发散回归的金丝雀（历史上 19 分钟
   不收敛，改索引路径后必跑，timeout 420s 内应完成）。
3. 基线数字与前后对比记 TASKS.md 对应批次条目（探针在 _scratch
   的临时版会丢，正式版在 scripts/）。
