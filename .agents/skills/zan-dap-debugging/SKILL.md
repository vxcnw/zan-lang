---
name: zan-dap-debugging
description: Zan 调试链路（src/dap zan-dap + irgen DWARF 发射）的定式与坑——irgen 给 Zan class/List/string 发真实 DWARF 结构类型的规则（opaque 指针下 zan_type_t 是唯一真相、泛型参数按名字替换、List 元素槽是 8 字节擦除槽 data 必须 long*）、DAP 变量展开的 refs 布局与 -var-list-children --all-values、验收用 gdb ptype/p *p 探针、conformance 不带 -g 所以 DI-only 改动不背 conformance 失败。做或改 src/dap、irgen 的 DI 发射、调试器变量展开/Watch，或排查"调试器里字段展开不出来/类型是 byte*"时使用。
---

# Zan DAP 调试链路（irgen DWARF + 变量展开）

> 提炼自五期主体（2026-09-09）：irgen 结构化 DI 发射 + DAP 变量展开。
> 每条都是实测踩坑后验证过的。

## irgen 发 DWARF（src/compiler/irgen.c 的 DI 段）

- **opaque 指针时代 LLVMTypeRef 不含 pointee 信息，`local_add` 传入的
  `zan_type_t *zt` 是唯一真相**。类型描述一律从 zan_type_t 递归
  （di_type_for_zan），LLVM 类型只当兜底（di_type_from_llvm）。DI 全部
  挂在 `g->emit_debug` 早退上（di_declare_var 第一行）——**不带 -g 的编译
  一条 DI 代码都不执行**，这是"DI-only 改动不可能背 conformance 失败"
  的结构性依据（conformance 用例 ZANC_ARGS 不带 -g）。
- **泛型类型参数必须按名字替换，不能按符号同一性**：binder 给
  `Box<int>` 内部化的 TYPE_TYPE_PARAM 与 class 符号表里的
  SYM_TYPE_PARAM 是两份独立对象，指针永不相等；先在 cls->members 里按
  名字找，找不到再回退 decl->type_decl.type_params（数量一致时按下标）。
- **List 元素缓冲是 8 字节擦除槽（generic_field_slot 加宽），DI 里的
  `data` 必须描述成 `long *` 而不是 `T *`**：写成 int* 时 gdb 按 4 字节
  步进读槽，`data[1]` 显示成半截——实测 xs={7,9} 显示 data[1]=0 的根因。
  StringBuilder 用 byte*、Dict 用 8 字段结构（前 4：count/capacity/keys/
  values），Span 是值结构 {base,length}。这些是编译器自造布局
  （irgen.c list_fields / zan_abi.h），文档只认代码。
- **class 环（自引用/互相引用）用 replaceable composite**：
  LLVMDIBuilderCreateReplaceableCompositeType 占位 → 成员递归 →
  LLVMMetadataReplaceAllUsesWith 收口（LLVM-C 没有
  LLVMDIBuilderReplaceTemporary）。缓存键是 zan_type_t，`building` 标志
  防递归重入。每次 emit 开头 di_debug_types_reset() 清缓存——DI
  metadata 随 module 死，缓存不能跨 module 活。
- **DI 只描述 payload**：Zan 对象前面有 16 字节 ARC 头（zan_abi.h，
  obj-16 引用计数），局部变量是指针，DWARF 给指针类型即可，gdb 解一次
  引用正好落在 payload 第 0 字节。
- 数组描述：`len`（long）在 offset -16（数组头），`elements` 是
  0 长度元素数组在 offset 0——gdb ptype 显示成结构 + 柔性数组语义。

## DAP 变量展开（src/dap/debugger.c / dap_main.c）

- **`-var-list-children` 默认不给 value=，必须显式 `--all-values`**——
  否则展开树全有名字没值，看起来像"展开坏了"。
- MI 的子节点输出是 `child={name=...,exp=...,type=...,value=...}`，
  value 里可能带嵌套引号和花括号，解析必须引号感知 + 花括号配平，
  不能找第一个 `}`。
- **指针类型字段的子节点列表是单个 `*expr` 伪子节点**（gdb varobj 语义：
  指针要先解一层才有成员），展开时发现 n==1 且 name 以 `*` 开头就替
  用户多走一跳。
- has_children 判定在 gdb 的类型字符串上做启发式：`struct` 前缀或结尾
  `*` 可展开；`byte *`/`char *`/string 除外（字符串便利性显示已够读）。
- refs 布局：locals 的子展开用 3000+i，动态（varobj 树）节点用
  DBG_VARREF_DYN(4000)+下标映射 varobj 名；handle_variables 里两段分支
  都走 dbg_expand_variables。

## 验收仪式

- **编译器侧验收不看 ctest，看 gdb**：`zanc -g pp.zan -o pp.exe` +
  `gdb -batch -x pp.gdb`，断言 `ptype p` 出
  `struct P {int x; int y; string name;} *`、`p *p` 出字段名值对、
  `ptype xs` 出 `struct List<int> {long count; long capacity; long *data;}`、
  `p xs.data[0]@2` 出 7/9。探针 _scratch/pp1.zan + pp1.gdb（模式保留，
  换类型就改它）。
- **DAP 侧**：stdio JSON-RPC 全手工驱动（initialize/launch/
  setBreakpoints/configurationDone/stopped/stackTrace/scopes/variables），
  断言 locals 带类型、可展开节点 variablesReference>0、子节点值正确；
  既有回归 tests/dap/dap_integration_test.c（目标是 tests/dap/
  dbgtarget.zan，不是你的探针）必须 0 failures。
- stopped 事件的 reason 可能缺省（DAP 规范允许，默认 breakpoint），
  探针别把 reason==undefined 当失败。

## ctest 归属纪律（编译器批次的验证）

- **一次完整的 tier run 的 LastTest.log 会被任何后续 ctest 调用轮转掉**
  （变成 .tmpN，N 复用不保证），完整跑完先解析/复制失败清单
  （build/Testing/Temporary/LastTestsFailed.log 只反映最后一次调用）。
- 归属三板斧：① 看 hunk 是否全在 DI 门内（不带 -g 的用例碰不到）；
  ② git 考古——失败家族的根因提交日期早于本批（golden 内容新旧一眼
  可辨，如 1.#QNAN=旧 MSVC 拼写 vs NaN=C# 拼写）；③ 历史 tier 日志
  （.tmp 文件）里同一测试的过/挂状态。历次已登记的存量挂法：泛型
  string+引用拼接被 de41f214b（9/5）拒绝、primitive_constants golden
  停在 93ac441b3（9/8）前、orm_* 是 A90 裁剪账、cs_b08_arrays 的
  int[,] 挂在 9/8 parser 批后、clipboard/http/mysql/web_menu 是
  环境依赖（无网/无桌面会话）。
