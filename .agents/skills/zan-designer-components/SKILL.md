---
name: zan-designer-components
description: Zan 窗口设计器用户组件（components/*.zcomp）的全链路定式——引用节点（{"kind":X,"ref":X}）、对外 props 声明（{"props":[{key,label,kind,target,prop,def}]}）、实例值直通表、GenForm 展开、设计器预览、运行期 UserComponentRegistry、双击进组件编辑；附 stdlib/Json 与 .zform 的尖锐边（Put/Set 语义、role window vs control 的 static/instance 字段、ZanGen 缓存陈旧）与并行会话下 CMakeLists 局部暂存技巧。做或改设计器组件、.zcomp/.zform 管线、GenForm 生成器、UserComponentRegistry、或踩到 JsonValue Put/Get、多实例叠前缀名、role:window static 字段报错时使用。
---

# Zan 设计器用户组件全链路

> 提炼自三期组件化改造（引用化 924e1566 / props 全链路 a7b0ead5 /
> 双击编辑 48d3f130 / BatchJobProgress dogfood 1218aa2d /
> 运行期注册表 c1adb56a）。每条都是踩坑后验证过的事实。

## 架构：一份组件文档，三个消费方，一种属性语义

- .zcomp 根可带 `"props":[{key,label,kind,target,prop,def}]`（v1 只消费
  text 型）：target = 组件内部控件名，prop = 控件 SetProp 认的键。
- 实例值存引用节点 extra 的 `"props"` 直通对象（键 = 声明 key）。
  `"props"` 不在 IsModeledKey 里，SaveJson/LoadJson 原样透传——不要
  给它另建模型字段。
- 三个消费方必须同语义（实例值优先、缺省取 def、落到 target）：
  GenForm 展开（编译期）、Designer 预览 PvCompCtl、
  UserComponentRegistry.Build（运行期）。预览与运行期已合到
  `UserComponentRegistry.ApplyProps` 一个入口，改语义只改这里和
  GenForm 两处。

## 展开（GenForm.ExpandRefs）的坑

- **组件文档缓存是共享的，展开会原地改写**：第一个实例的
  壳名前缀、dock、props 合并都写进 CompDoc 缓存。不 DeepCopy 就会
  出现第二个实例拿到 `Card2_Card1_InnerBtn` 叠前缀名。展开前
  必须 `GenForm.DeepCopy(cf)`（标量节点不可变可共享）。
- 壳上消费过的实例 props 必须清空（Set 成空对象）：EmitField
  会把字段级 props 逐键 `SetProp` 到壳上，Panel 不认的键会
  退化成样式类（SetProp 的 fallback 是 AddClass）。
- 改已有键必须用 `Set`：**JsonValue.Put 是追加不去重，Get 只认
  第一个**——曾导致 kind 改了不生效而新键全生效的灵异 bug。
  新建对象上的首次写才用 Put。
- 目标控件缺失时报指名错误（`component 'X' prop 'Y' targets
  missing control 'Z'`），不要静默跳过——那是组件作者的错。

## .zform / 生成代码的尖锐边

- **role 决定字段形态**：role:control 生成实例字段（`new X()` 后
  `app.Field1`）；role:window 生成 **static** 字段，实例访问直接编译
  错（`'Job1' is a static field... qualify with the type name`）。
  无头测试一律用 role:control；入口文档必须是 window 才能用 window。
- 引用展开后内部控件不生成具名声明（匿名），运行期只能
  `shell.Find("壳名_内部名")` 触达。Label 的 text 属性 syncName：
  SetDesignText 会把控件改名为标题，Find 要用 caption 而不是设计名。
- Badge/Panel 等没有 `text` 属性，GetProp("text") 返回 ""；断言文本
  时选有 PropSpec text 的控件（Label/Button）。Progress 有数值型
  `percent` prop，SetProp/GetProp 走字符串形式（"30"）。

## 控件 Props() 补属性的定式（2026-09 审计实证）

- **普通字段直赋即实时绑定**：`spec.num = someIntField`（编译器合成
  访问器对，双向读写控件字段）。Progress.fillColor、ChoiceGroup.columns
  都是这么写的且已过测试；**不要信「设计期常量走快照 Binding 写不回」
  的旧注释**（InputNumber 那条是过时顾虑，已订正）——担心写不回就写
  往返探针（SetProp→GetProp）实证，别凭注释下结论。
- **裸 `ps.Add(PropSpec.Text("class", "Classes"))` 是合法的**：读写
  走 Control.GetProp/SetProp 对 "class" 的基类特判，spec 只负责属性
  面板可见性。同理 "name"。
- Zan **没有 C# 式跨行相邻字符串隐式串接**，`"a"\n"b"` 直接报
  expected ')', got STRING_LIT——换行拼接必须显式 `+`。
- 颜色属性（PropSpec.Color，kind 4）的文档串形式就是 ARGB 整数十进制
  （Read/Write 走 Convert.ToString/ToInt32），探针往返用 "-65536" 这类。
- **Step(s, lo, hi) 一律置 hasRange**：hi=0 就是「上限钳到 0」，不是
  「无上限」——只配步进不配范围必须用 `StepBy(s)`（实测：step 属性挂
  Step(1,0,0) 会把步进值钳死成 0）。
- 新增属性的最小验证：实例化→SetProp→GetProp 往返 +（有访问器时）
  断言公开 getter，一处探针覆盖九组件 24 断言即可全绿提交。

## 生成器与构建链

- **ZanGen 缓存按内容寻址，只有 zanc 跑设计管线才会重建**。
  直接调 `ZanGen_<hash>.exe` 做探针时若刚改过 GenForm.zan，先跑一次
  `zanc ... --auto-stdlib` 触发重建，否则在验证陈旧行为。多个
  缓存 exe 共存时按文件名排序不一定拿到最新。
- 驱动生成器：请求 JSON `{mode:"design", files:[{name,text,emitMain}],
  components:[{name,text}]}`，两个参数 = 入/出 json 路径。.zcomp 只进
  components，永远不被当作 Zan 源解析。
- 改 GenForm.zan 后 policy_zform_schema 会扫所有 ObjStr/ObjNum/ObjBool/
  .Get 读的键：新键必须写进 tools/mcp_server/zform.doc.json（反向也
  查：文档了但 GenForm 不再读→把读法改成 ObjStr 这种可扫描形式
  或移进 note）；生成器请求区的键（files/components）在测试的
  allowed_region_keys 白名单。设计器私有键（如 pvOff）走 UnmodeledKeys
  透传，写进 note，不建 key 条目。

## 并行会话下的工程动作

- CMakeLists.txt 被并行会话占着时，不要整文件 add：先改工作树，
  再用 `git show HEAD:file` 重构"只含自己 hunk"的版本，
  `git diff --no-index` 生成补丁后 sed 修正路径头，
  `git apply --cached` 只把自己的 hunk 进索引。手写 hunk 头容易
  corrupt，重构法稳。
- 验证阶段直接手跑受影响的 conformance 子集
  （`ctest -R "gui_compref|gui_batchjob|..."`），不跑全量 ctest。

## 测试地图

- tests/gui/compref_test.zan：编译期展开端到端（多实例/实例覆盖/
  默认回落）。
- tests/gui/compref_designer_test.zan：无头 Designer 验收（落节点/往返/
  预览/解包/双击请求/注册表）。
- tests/gui/batchjob_test.zan：dogfood：实例 props + 运行期 Find+SetProp
  驱动进度（批量任务进度窗工作流）。
