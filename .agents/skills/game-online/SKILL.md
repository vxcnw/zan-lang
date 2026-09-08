---
name: game-online
description: Zan 上做"客户端展示 + 服务端权威"网游模板（templates/game/* 客户端 + templates/server/server-* 服务端）的架构定式与全链路验证方法——发布内置单服务器入口、一个账号通进所有区、登录流页序（请登录/建号/修改密码/分区/选角/建角）、服务端表结构自动迁移、ORM 字面量查询铁律、原版素材恢复的盘点顺序、表单页 state-only 回调 + 轮询重建定式、UiDriver 端到端驱动（坐标点击/DPI 物理像素/探针断言/空闲停摆光标保活）。做或改网游类模板（legend、server-game 及后续同类）、补登录/分区/建角/好友等服务端功能、或提到 服务器地址配置/区服列表/建删角色/UiDriver 驱动卡顿时使用；纯单机帧循环游戏走 game-dev，迁移方法论走 app-migration。
---

# Zan 网游模板：客户端展示 + 服务端权威

> 提炼自迷你传奇复刻（templates/game/legend + templates/server/server-game）
> 登录流重构到建角页定稿的完整迭代。每条都是验证过的事实；被推翻的规则
> 当场删除（见文末迭代纪律）。参考 testing-zanide-uidriver（UiDriver 通用
> 陷阱）、game-dev（帧循环类）、app-migration（复刻不创造不阉割）。

## 1. 架构定式：服务端权威，客户端展示

- **一切数据与计算在服务端**：账号、角色、背包、战斗结算、挂机收益全在
  server-game；客户端只发意图（op 请求）+ 渲染推送。客户端不存任何可
  授予资源的本地状态。
- **发布内置单一服务器入口**：`data/server.txt` 首行 `host:port|gatepass`，
  客户端启动即自动连接（`ConnectPublished`）；`LEGEND_SERVER` 环境变量可
  覆盖（测试用）。登录窗不再有"自定义服务器"输入框——照原版，玩家只见
  账号密码。服务端网关校验 gatePass（config app.json 里配），不匹配直接
  断开（客户端报"服务器密码不正确"）。
- **一个账号通进所有区**：账号表全局唯一；角色按 realmId 隔离（模板每区
  一个角色，列表按多角色返回，放开多角色客户端不用改）。登录成功即拿全
  部区服列表（应答自带 realms 数组，含 grp 分组/expRate/dropRate/online/
  state），照原版停在「分区」选择页不自动进区。
- **协议**：一问一答严格按序（op JSON 进 FIFO，回复按序对号入座
  replySinks）；推送类走 chat/state。加 op = 服务端 dispatch 加一行 +
  客户端 Net 加一个带回调的方法。

## 2. 服务端 ORM / 迁移铁律（踩过坑的）

- **表达式树查询里只写字面量，不写局部串变量**：`Where(a => a.name ==
  "布衣(男)")` 稳；`Where(a => a.name == someLocalString)` 求值不稳。
  必须按变量查时拆成两个字面量分支（如按性别查起点装备）。
- **表结构演进用自动迁移**：启动时 `SyncStructureAllAsync()` 会给既有表
  补新列（Account.email、Realm.grp、Player.gender 都这么加的），种子数据
  用计数守卫（存在即跳过），别写手工 ALTER。
- **删号等危险操作先查在线**：`World.HoldsPlayer(playerId)` 命中即拒；
  删角色连背包一起删（同 accountId+realmId）。
- **自增主键不自动回填内存行**：`ExecuteIdentityAsync()` 返回 id 后手动
  `row.id = id`，会话与 GM 页都按 row.id 定位角色。

## 3. 原版素材恢复：先盘点，后裁图

- **先全量盘点资源包的序号资源**（data/*.pak 解包出的 ui/ 277 张、tupu/
  skill/show…），按序号猜语义前先问用户或对照原版窗口——本项目建角页
  头像就是 ui 包里的 00111-00116（顺序=战士男女、道士男女、法师男女，
  不按职业索引排），一开始却去 exe 内嵌表/Skin.dll 里大海捞针，最后从
  截图裁图，绕了一大圈被用户一句"不是有这组素材吗"点破。
- 用户截图裁图是**最后手段**：裁出的图带原窗底色、尺寸非标，直接摆会
  丑（缩放进框=变形+模糊+套底框）。要用就 1:1 原尺寸、无底框、选中才
  描边。
- exe 逆向找图多为死路：E 语言程序的嵌的资源常只有 JPEG/GIF 块与运行时
  字符串表，Skin.dll/dll 后缀可能是音频或加壳数据——别在这上面烧时间。

## 4. 登录窗表单页定式（stdlib/Gui）

- **按钮回调只置状态，绝不同步重建**：在 click 处理器里 RemoveAll 自己
  所在容器会弄坏派发链（重建出的输入框收不到键）。页面切换统一为
  `formPage = "xxx"`，由 120ms 轮询泵（PumpNetStage）比较 `formPage !=
  renderedFormPage` 后重建。
- **异步数据到达靠重建 key**：每页一个 key（修改密码页=问题+结果串，
  选角页=就绪位+数量+armDel，建角页=job+gender），key 变了才重建。
  key 要把"需要立刻反视觉反馈的状态"（如两击删除的 armDel）计入。
- **输入草稿跨重建保留**：重建会丢输入框内容；切页/点块前把
  `input.GetText()` 存字段，Build 时 SetText 回填（建角页名字草稿、修改
  密码页账号都是这么保的）。
- **提示行分页治理**：只有"动态页"（登录页=连接/服务器消息，建号页=
  注册结果）让泵改 netHint；其余页的提示是页面固定说明，泵一概不碰，
  否则本地校验消息下一拍就被聊天流冲掉。
- **图标块（职业/性别/头像）**：块=Panel.Column（Class 控制选中态边框，
  默认透明底无框）+ Image（原生尺寸或整数倍，"contain"）+ Label；点块
  一次选定多个维度（如职业+性别）比两层联动简单得多——用户原话：
  "6 张图，5 个按钮你怎么玩的"。
- **小窗口**：登录窗 440x520，进世界才 SetClientSize 长成主窗。控件
  Prefer 高度给足（输入 34-42、主按钮 44-46）。

## 5. UiDriver 全链路验证仪式（Windows 实机）

1. **launcher 保活**（必须）：Gui 事件循环空闲会停摆，注入事件以 ~3s/个
   爬行、`wait` 冻结。launcher 每隔 ~1.2s 在窗口内 `SetCursorPos` 轻移
   真实光标（不点击）保持出帧，事件即刻恢复即时处理。
   `_scratch/legend_launch3.ps1` 是可抄的模板——**纯 ASCII**，PowerShell
   5.1 把 BOM-less ps1 当 GBK 读，中文注释都会炸语法。
2. **坐标点击，别用数字 id**：控件 id 每次重建重新编号，几何在固定窗
   尺寸下稳定。先 `dump hitregions` 拿区域再换算中心点。
3. **坐标是物理像素**：150% DPI 下 = 逻辑值×1.5（ Prefer(108) 的块实测
   162 宽）；`dump pixels` 的 ZPX 尺寸也是物理像素（含 48px 标题栏偏移
   y0）。UI 布局代码里写的都是逻辑值。
4. **首击激活**：对未聚焦窗口的第一个注入点击只激活窗口，脚本开头先来
   一次中性 click。
5. **事件可能被吞**：页面重建瞬间注入的点击会丢（按序处理跨 RemoveAll）。
   关键导航点击"两击保险"（第二击落在下一页的等位控件时应无害——比如
   落在"创建并进入"上，空名会被服务端拒绝）。
6. **断言用探针**：应用每拍 `UiDriver.SetProbe("form", ...)` 发布表单状
   态（页名/职业/草稿/输入框现文），脚本 `dump probe form x.txt` 直接断
   言，比截图快且准。像素截图（ZPX 解码：24 字节头，BGRA，先转 RGBA 再
   存 PNG）用于最终视觉验收。
7. **`type` 进不了 CJK**：中文名验证用拼音/ASCII 代之，不阻塞流程。
8. 每轮验证 = launcher 起进程 + 脚本（wait→click→type→dump probe→
   redraw full→dump pixels）+ Python 解码截图 + 对照原版截图逐项过。

## 6. 经验迭代纪律（本项目约束，写进 AGENTS.md）

- 会话里**验证过**的新经验：当天并入本 skill（或对应 skill），随功能
  同一提交。
- 被**推翻**的旧经验：同一提交里删除，不留"可能也对"的僵尸规则。
- 每条规则必须带"为什么"（踩过的坑），没有坑的规则不配存在。
