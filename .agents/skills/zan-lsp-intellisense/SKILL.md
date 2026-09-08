---
name: zan-lsp-intellisense
description: Zan LSP（src/lsp/zan-lsp）与 intellisense 引擎的供数定式与验证方法——stdio JSON-RPC 探针（scripts/lsp_baseline_probe.mjs 三档场景）、索引收敛跳过目录、工具链 stdlib 按 exe 相对规则入共享项目索引、goto-def/成员补全的数据来源（g_project_intel 回退 + 手写 stdlib_classes 表的局限）、INTEL_MAX_COMPLETIONS 容量挤占坑。做或改 zan-lsp、intellisense.c、LSP 补全/导航/诊断供数，或量 LSP 延迟/命中率基线时使用。
---

# Zan LSP 供数与基线

> 提炼自四期 LSP 改造第一批（基线 094d28f0 / 收敛+stdlib 1ecf29d8）。
> 每条都是实测踩坑后验证过的。

## 数据流（改供数前必读）

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
- didChange 是全文同步重解析（736KB 文档每击键 ~46ms）——改这个
  就是"编译器前端增量入口"批次本身，别在 lsp_main.c 里绕。

## 验证仪式

1. `cmake --build build` 后必跑 `build/lsp_integration_test.exe
   build/zan-lsp.exe`（UTF-16 位置编码回归，PASS 一行）。
2. `LSP_PROBE_MODE=ra2 node scripts/lsp_baseline_probe.mjs`（秒级）
   看补全 P50/命中率/goto-def；`LSP_PROBE_MODE=gallery` 看 stdlib
   类型成员补全；`repo` 模式是发散回归的金丝雀（历史上 19 分钟
   不收敛，改索引路径后必跑，timeout 420s 内应完成）。
3. 基线数字与前后对比记 TASKS.md 对应批次条目（探针在 _scratch
   的临时版会丢，正式版在 scripts/）。
