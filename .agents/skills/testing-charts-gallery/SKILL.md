---
name: testing-charts-gallery
description: Zan charts gallery (examples/gui_charts, 335 ECharts 官方对照 demo) 的代码级完整度对照与实机验证定式——scripts/chart_gap_audit.py 的未读配置键倒排/源引用率、源函数逐条对抄、数值 oracle（ECharts getLayout 归一化对比，bar 布局样板）、颜色/字号预算闸门、recheck2 截图驱动、bindprobe 探针、--bench 帧计时、stdlib 快照同步坑、多 grid/dataZoom/定点数值三大契约。凡是要盘点图表迁移完整度、修复 stdlib/Gui/Component/Chart 引擎改动、核对某个 demo 与 ECharts 官方语义是否一致、排查"图表空板/缺元素/多面板窗口不同步"时使用。
---

# Charts gallery 验证与修复定式（Windows 实机）

## 口径：先比代码，后谈截图（2026-09-11 定调）

**截图不是完整度判据。** 引擎的完整性按 **ECharts 源函数**记账；
"跑 demo 看图"抓不到语义错误，而且这种账本会自己腐烂。

为什么（本仓实测，踩过的坑）：

- ECharts 6.1 有 **596** 个 `src/*.ts`；引擎 35 个文件里只有 **6 个**
  引用过源（共 14 个源文件），核心的 `barGrid.ts` / `LineSeries.ts` /
  `PieView.ts` / `Scale.ts` / `axisNiceTicks.ts` / `symbol.ts` /
  `LegendView.ts` / `ChartView.ts` 一个没引。大多数代码是 2.2.7 时代
  手写的（`ChartModel.zan` 的 `ChartType` 注释自己写着 2.2.7），v6 语义
  没抄——这就是"有些完全就是错的"的来源，不是玄学。
- `docs/CHART_PORT_AUDIT_2026-09-10.md` 的"82 例白板"基于 2026-09-10
  02:54 的构建，它引用的 Zan 侧截图 `_scratch/shots/`（335 张）**现在只剩
  5 张**，`render_audit.json` 早于其后 4 个修复提交。截图口径的账本
  既不自证正确，也留不住。
- 着色占比只能抓白板。已核实的三个语义错误在着色占比里全都"正常"：
  ① 柱宽公式 `ChartViewBar.zan:351-354` 手写 `step*7/10`、`Scale(2)` 像素
  间距，对照 `layout/barGrid.ts:206-349` 的 `barCategoryGap` 求解
  （**已修**：`ChartBarLayout.zan` 严格对抄，见"数值对照 oracle"节）；
  ② 折线符号漏了 `chart/line/LineView.ts:371-410` 的数值轴提前返回与
  `canShowAllSymbolForCategory()` 通过分支；
  ③ `axis.scale` 从不读取，且 `Chart.zan:1019,3006` 的
  `AxisMinForF/AxisMaxForF` 初值为 0 → 量程无条件并入 0，
  但 `coord/axisModelCommonMixin.ts:33` 只在 `!scale` 时并入。

定式：

1. 动手前先跑 `python scripts/chart_gap_audit.py`（仓库根）。它列出官方
   option 用到、而引擎**从不通过 Json 访问器读取**的配置键（当前
   278/470），以及每个引擎文件引用了哪些源。**未读键 = 静默丢弃 =
   这张图不可能对**，先看这里再决定修哪个。
2. 引擎新增/修改的逻辑，注释必须写 ECharts 源 `文件:行`。没有出处 =
   这条无法审计，等于欠债（审计工具就是按这个引用率给结论的）。
   **"已修"必须能在工作区 grep 到那行代码 / 有 conformance 用例支撑**：
   台账/提交信息写着"加了守卫"而代码里没有，就是僵尸结论——空 points
   越界（B3）这样假报修好一次，直到 2026-09-11 实测复现出
   `Chart.zan:3031 list index out of bounds` 才补上。复现靠"直接调
   `Chart.AxisMaxForF(series, 0, 2, 4)`"这种最小探针（比开窗口截图快得多）。
3. 代码级账本：`docs/CHART_PORT_AUDIT_2026-09-10.md` 是**已提交**的
   完整度审计报告；逐条施工台账在 `_scratch/ECHARTS_PORT_LEDGER.md`
   （A=缺席 / B=已修 / C=待定位 / D=验证纪律）。按源函数记账，
   **修一条删一条**，不留已完成项。
4. 截图留给**渲染层**问题：控制点已与源一致、画出来仍不对的那种
   （如 smooth 的"麻花"，见下节——控制点手算与 JS 参考逐值相同，
   病在采样率/描边光栅器）。语义层用截图判等会误判，渲染层才是它的地盘。

## 数值对照 oracle：布局/量程这类纯计算，直接对 ECharts 自己算的数

"逐函数对抄"之后仍要证明抄对了。几何/布局/刻度这类**纯计算**不要靠
截图，走数值 oracle：让 ECharts 把它的中间结果吐出来，Zan 侧用**同一份
option** 复算，逐字段 diff。

- **权威钩子**：`seriesModel.getData().getLayout('offset'|'size'|'bandWidth')`
  ——即 `layout/barGrid.ts:calcBarWidthAndOffset` 的输出，由
  `createCrossSeriesLayoutHandler.overallReset` 经 `data.setLayout` 挂上。
  不要量 rect（首帧显示表里第一个矩形常是被裁剪的残片，会得到 3 个假
  不一致；柱溢出绘图区时尤其）。绘图区原点/跨度用 `grid.getRect()`；
  `axis.getExtent()` 返回的是相对 [0,span]，**不是**绝对像素。
- **归一化再比**：`offU = offset/band×1e4`、`wU = size/band×1e4`。两引擎
  绘图区尺寸不同也不影响；只有 px 形态的选项（`barWidth:20`、
  `barMinWidth:12`、`barMaxWidth:8`）才依赖 band，**把 ECharts 报的 band
  原样喂给 Zan 探针**。可直接复用的骨架在 `_scratch/chart_oracle/`
  （带 README，`clean_scratch` 跳过）：`bardemo.js` 出
  `bardemo.oracle.txt` → `bardemo.zan` 读 oracle 行取 band/n，走真实
  `ChartOption.FromJson` + 渲染层同一选取规则 + `ChartView.CalcBarCols`，
  输出同格式后 `diff --strip-trailing-cr`。探针必须用**工作区** stdlib
  编译（`--auto-stdlib`，别带 `--stdlib-path _scratch/stdlib_snap`，
  那份快照会落后——本地 6:13 的 gallery 构建就是拿 3:45 的旧快照跑的，
  新柱布局根本没进去）。
- **覆盖要分两层**：① 构造配置打边界（默认/显式 px/%/负 gap/堆叠/混
  堆叠/min-max 宽度/"末个声明系列覆盖"语义）——23 组；
  ② **真实 demo 打集成**（`examples/gui_charts/options/bar-*.json`：纵向
  11 / 横向 4 / 瀑布 2，含 `bar-tick-align` 的 `xAxis` 数组形态）——17 组。
  两层都 IDENTICAL 才算这条修完。真实 demo 层还能顺带查出类目数推导
  （Zan 侧 n 与 ECharts 的 n 不一致时输出 `MISMATCH-N`）。
- **ECharts SSR 进程不退**：`echarts.init(null,null,{renderer:'svg',ssr:true})`
  留下未清的帧句柄，脚本跑完仍挂住（`head` 管道下表现为"永远在跑"）。
  末尾 `process.exit(0)`；后台跑时重定向到文件再读。

## 构建（快照 stdlib，避开并发会话的在途编辑）

并发会话常在改 `stdlib/System/Net/...`（编译会挂）。图库构建走快照：

```bash
# 快照只需建一次；此后【每次改 stdlib 后必须重新同步】，否则构建
# 静默用旧代码——修好的 bug 看起来"还在"，排查浪费几轮（踩过 3 次）。
cp stdlib/Gui/Component/Chart/*.zan _scratch/stdlib_snap/Gui/Component/Chart/

./build/zanc.exe examples/gui_charts/gui_charts.zan examples/gui_gallery/MapChinaData.zan \
  --auto-stdlib --stdlib-path _scratch/stdlib_snap \
  --embed examples/gui_charts/options --embed examples/gui_charts/charts-registry.json=charts-registry \
  --embed examples/gui_charts/maps --libpath build \
  --link-lib zan_gui_charts_gnu --link-lib ws2_32 --link-lib mswsock --link-lib psapi \
  --link-lib advapi32 --link-lib dwmapi --link-lib gdi32 --link-lib imm32 --link-lib user32 \
  --link-lib rpcrt4 --link-lib ole32 -o _scratch/charts_pc.exe
```

- 快照是**双刃**：它让构建绕开并发会话的在途编辑，也会把"修好"
  静默吞掉——提交前必须 `diff stdlib/... _scratch/stdlib_snap/...`
  核对工作区与快照逐字节一致（Render.zan 曾在快照里有
  DrawPolyBatch 而工作区没有，`git status` 全绿、构建全过、改动丢了）。
  修完 Zan 源码后立刻 `diff -q` 校验；提交范围以**工作区**为准。
- `ole32` 是并发会话的 WASAPI 音频引入的；少它链接失败时先想依赖漂移。
- GUI 子程序**没有 stdout**：`Console.WriteLine` 不可见。追踪一律
  `System.IO.File.AppendAllText("D:/project/zan-lang/_scratch/dbg_xxx.txt", ...)`，
  绝对路径；收尾必须剥离。

## 截图单 demo（recheck2.ps1）

```bash
mkdir -p _scratch/shotsN   # OutDir 不存在时 GDI+ Save 直接抛异常
powershell -File _scratch/recheck2.ps1 -OutDir D:/project/zan-lang/_scratch/shotsN -Ids <demo-id>
```

- 参数是 **-Ids**（不是 -Demo）；bash 里 `powershell -File ... -Ids a,b,c`
  不会拆数组——逐个跑 for 循环。
- zanc 的进度杂音（"compiling code generators..."）走 stderr，PowerShell
  把它升级成 NativeCommandError，构建脚本会**假失败退出 1 且无真实诊断**。
  判定成败用独立探针跑同款 zanc 参数并显式打印 `$LASTEXITCODE`
  （如 `_scratch/zanc_charts_probe.ps1`），别信包装脚本的 throw。
- demo id 用 **registry 全名**（`scatter-anscombe-quartet` 而非
  `anscombe-quartet`）；打错 id 应用会静默回落到首个 demo，截图对不上号。
- recheck2 会杀旧进程→启动→最大化→截图；它把窗口临时 TOPMOST，
  并发会话的置顶工具窗可能压在截图上——重拍或最小化对方窗口，
  别隔着遮挡下结论。
- 看细节用 python PIL 裁剪放大，别靠整图目测。

## 探针

- **bindprobe**（`_scratch/bindprobe.zan`）：解析态 Dump——grids/axes/series
  的 data/points/candles 计数与首值。改 Dump 列表后用同款 embed 参数编译。
  「缺元素」先分清是**解析没进数据**还是**渲染画不出来**，探针定分界。
- **--bench**：`charts_pc.exe <demo> --bench` 渲 30 帧写 `_scratch/bench.txt`，
  卡顿量化用。

## 引擎三大契约（踩坑出处）

1. **Gap 不进极值、不连线**：ECharts data 项 `'-'` 解析为
   `ChartData.Gap()`（gap=true, val=0）。任何包络计算、折线段对 `s.Value(i)`
   的读取都必须先查 `s.data[i].gap`，否则 MA 前段把量程拖到 0，
   scale:true 紧致包络被撑爆（candlestick-touch 蜡烛压成细线 + 空成交量）。
2. **多 grid 子面板**：grid 矩形是纯绘图区（ECharts 语义）——
   标题/工具箱/图例是页级元素，派发层画一次；子面板若走 PanelContentTop
   会被 59px 头部吃掉（96px 成交量条带只剩 30px 绘图区）。
   dataZoom 窗口**全格生效**（官方 xAxisIndex:[0,1] 同窗联动），
   滑条条带只随最后一个 grid 画一次（`Chart.zoomBarHidden` 帧内静态）。
3. **×1000 定点只到 2.1e6**：柱/线渲染把值 ×1000 定点后走
   `YOfF/YOfFL`。亿级整值（成交量 8.6e7）×1000 = 8.6e10 **爆 int32**，
   柱子全体消失。大值路径一律 long：`YOfFL(long vF, int axis)` +
   调用方 `(long)(d * 1000.0 + 0.5)`。横向柱的 `v×g/1000` 链（ChartViewBar
   1083/1216 一带）同坑未修——值 >2.1e6 的横向柱要接 YOfFL 化。
4. **并行坐标 `layout:'vertical'`**：名字指**轴的排布方向**——vertical =
   轴从上到下堆叠、每根轴横向（官方 nutrients 样子）；默认 horizontal =
   轴从左到右、每根轴纵向（parallel-aqi）。不是"横着的轴叫 horizontal"。
   `parallelAxis[].dim` 显式绑定数据列（无 dim 按数组槽位），
   `visualMap` piecewise `categories` 模式按行在
   `dimension`（缺省 1）列找类目名取 `inRange.color`（官方 25 色由
   `echarts.color.modifyHSL('#5A94DF', hStep*i)`、hStep=round(300/(n-1))
   彩虹生成，末色 #5ADF8A）。
5. **密集折线图用 Canvas.DrawPolyBatch**：数千行平行坐标逐行
   `DrawPolyline` 在 GL 后端每行付一次完整覆盖缓冲清除+合成（45ms/帧
   主要来源）。`DrawPolyBatch(xs, counts, color, thickness)` 把 N 条
   同色互连路径并进**一次**覆盖缓冲周期（runtime `polybatch` vtable
   op，CPU 后端自动回落逐行）。行色互不相同的图先按色分桶再批量。
   配套流式渲染：ECharts `progressive` 语义 = restore 首帧快照 +
   每 24ms 预算增量画行 + 帧尾 SnapshotRect 累积。
6. **option JSON 一律单行紧凑**：`examples/gui_charts/options/*.json`
   全仓约定单行（separators=(',',':')）；pretty-print 过的 nutrients
   曾到 14.5 万行 1.17MB。改 option 用 Python json 重新序列化紧凑输出，
   diff 才能落在一行内可审。
7. **ChartOption 新增列表字段要拷三处**：`Create()`、`Clone()` 之外还有
   `ResolvedChart.DrawOption`（ChartResolved.zan 逐字段组装渲染用
   option）——漏第三处的症状极阴险：解析探针（直接 FromJson 后读字段）
   全对、渲染却回落缺省值。polar 落地时 angleAxes 漏拷 DrawOption，
   startAngle=0 探针打印正常、渲染整图转 90°（ax=null 走缺省 90）。
   新字段先 grep `o.polars = new List` 的三处落点再收工。
8. **极坐标/新坐标系投影全程保持 ×1000 milliunit**：points 存的是
   值×1000（pointG）。任何"先 PointV 除回整数再算"的写法都会双重
   失真——量程推导把 0..0.5 的小数域炸成 0..5（line-polar2 花瓣缩成
   点），角度 ×1000 当度数用再 mod 360 出锯齿螺旋（line-polar 心脏线
   两轮返工的根因）。定点参与运算、除回放最后一步；非整度角配
   SinDegX10/CosDegX10（整度值线性内插，1° 内曲率误差 <0.02%）。
9. **ECharts 极坐标角度语义**（对源 polarCreator.ts 核过）：
   startAngle = 轴值 0 所在的数学角（0=东、90=上，缺省 90），
   逆时针为正；angleAxis extent = [startAngle, startAngle+360]；
   屏幕 x = cx + r·cos(θ)，y = cy − r·sin(θ)（y 翻转）。
   line-polar 官方是 r=5+5sinθ 的心脏线、cusp 朝下——不是圆。

## 已知刻意偏差（勿当 bug 修）

- candlestick-touch.json 的 grid px 已 ×2.4（适配本机更高的画布）。
- scatter-matrix.json 删了 parallel 系列（引擎无平行坐标系，记 TASKS 债）。
- media 响应式查询、graphic 元素不支持（data-transform-multiple-pie
  竖排是 base option 的样子，官方横排来自 media，不是 bug）。

## ctest 档位

stdlib Chart 改动 → `cd build && ctest -R conformance_chart`（26 例，~96s）；
calendar 相关再加 `ctest -R conformance_gui_chart_calendar`（离屏 Canvas
几何/墨迹断言）。Chart 目录还挂两条 **smoke 级预算闸门**，改颜色/字号时
必跑：`policy_theme_color_budget`（`stdlib/Gui/**` 里除 Theme/Style/
StyleBox/Fx 外不得直读 `t.textPrimary` 这类语义色）、
`gui_theme_font_budget`（不得直读 `t.fontSize*`）。预算逐文件为 0，
要取颜色/字号走 `Style.Part(app,"chart","label",...).FgOr(0)` /
`Style.FontFallback(app,"small")`——皮肤才覆盖得到。（2026-09-10 的
calendar 提交直读 `t.textPrimary`/`t.fontSizeSmall`，两条闸门常红到
2026-09-11 才修；闸门是逐行正则扫描，同一行出现两次算两个。）

**离屏"墨迹"判据看不见叠写文字**：`InkStats` 那种"非纯白即算墨"的计数
在**填色格**上失效——格子本身已被计入，往上写黑字不新增任何像素
（`conformance_gui_chart_calendar` 的"农历日名确实写出来"断言就这么假红
过，实现其实是对的）。判"文字画出来了"要数**深色像素**（RGB 三通道
< 96），且用"开/关 label 两趟之差"消掉网格自带的深色轴标签。

两个 golden（chart_option_behavior.out 的 sr、chart_pie_layout.out 的 pal）
曾在语义提交（symbolSize 直径、v6 色板）时没跟上，属欠账——引擎语义
提交必须连 golden 一起核对，否则 standard 档永远挂着看不见的失败。
断言里读**定点存储**字段（`points[].x` 存 值×pointG）要先
`Chart.PointV(v, s.pointG)` 除回，否则改定点倍率就把解析测试扫成假红
（chart_specialized_json 的 `points[0].x` 就这么红过）。

## 渲染帧克隆税（大数据 demo 卡顿排查顺序）

大数据 demo 卡顿先量化三处税源，别急着怀疑渲染器本体（`--bench` 对照）：
1. **逐项深拷**：`ChartSeries.Clone` 默认全量深拷 data/points/candles 等
   大集合。渲染帧对数据集合只读的类型走 `Clone(src, shareData:true)`
   共享引用（`ResolvedSeries.Materialize(allowShare)` 按类型门控）。
   **pie/funnel 系必须保持全量克隆**——它们经 `ApplyDataLegend` 写
   `data[].hidden/selected`，共享会把交互态漏写进长寿缓存的源 option。
   审计法：grep 渲染帧路径全部 `s.data`/集合写入点，逐个确认只在
   drawOption/克隆列表上写（ChartView ApplyDataLegend 是唯一例外源）。
2. **外壳标量漏抄**：`Clone(src, shareData)` 的早退共享分支会让
   "早退之后才赋值"的字段全部漏抄。force*/chord*/funnel*/wc*/label*
   等标量外壳字段必须在早退**之前**抄完——conformance drb6 探针
   （DrawOption 物化后核对批 6 字段）就是抓这个的，别删探针迁就。
3. **平滑细分步数**：BuildPathFxEx 固定 48 步/段在 600 段×2 边界的
   时间轴面积图上每帧近百万插值点。步数按段像素跨度自适应
   （定点域 ÷256，钳 2..48）——窄段亚像素插值由描边光栅化器采样，
   收到 2 步也无可见折角；宽段保持原平滑度。
另外 multi-grid 子面板曾每帧 `ChartOption.Clone` 整个 option（全系列
逐项深拷）：子面板改的只有 xIndex/axisIndex 两个整数，改成 Create 空壳
+显式重建 axes/grids/titles/visualMaps+系列共享原对象（渲染只读）。

## 快照也是灾备

并发会话 checkout/分支切换会静默覆写工作区（本会话 4 个 Chart 文件被
覆写、git 历史与全部 stash 均无痕迹）。每次改完 stdlib 同步进快照的那份
副本**就是最近一次验证过的现场**：发现工作区被覆写时先
`md5sum` 对比工作区与快照、`grep` 快照里的关键标记（如新增函数名），
从快照整文件恢复再 `git diff --numstat` 核对范围，能省掉全部重写。
快照恢复后必须重跑编译探针 + ctest 档位——被覆写可能同时吞掉后续
手工修复（本会话 drb6 标量漏抄修复就被快照回滚了一次）。

## 平滑曲线（`smooth: true`）的 ECharts 语义与实现坑

ECharts line 的平滑算法不是「单调 Hermite / Cardinal / Catmull-Rom」，
是 **`poly.ts:drawSegment`**（`src/chart/line/poly.ts:36-209`）的
自研贝塞尔。关键事实——从源码逐行确认：

- `LineView.ts:118-119` `getSmooth(s) = isNumber(s) ? s : (s ? 0.5 : 0)`
  — `smooth:true` ≠ 1，是 0.5（张力系数）。`smooth:0.3` ≠ smooth:true`。
  引擎若把 `smooth` 当 0/1 bool 处理，`smooth:0.3 / 0.5 / 0.8` 画出来一样。
- `LineView.ts:854` 把 `series.smoothMonotone` 透传给 polyline；
  `LineSeries.ts:200` 默认 `null`。`poly.ts:134/143/152` 的三分支中
  唯一走的是 `else`（无单调约束的通用贝塞尔）。
- `poly.ts:152-191` 七步：cp1/nextCp0 初算 → nextCp0 钳到 [x,nextX]×[y,nextY]
  → cp1 反算 → cp1 钳到 [prevX,x]×[prevY,y] → nextCp0 再反算（**此处不再钳**）。
  poly.ts 没有「切线归零」，所以极值点不会水平搁架——而是轻微过冲。
- `poly.ts:91-101` 跳过**严格重复点**（X 和 Y 都相同）。bump-chart
  的 Pasta 2002=2003=#1（**Y 相同但 X 不同**）不在此列。

**实现时的关键陷阱**（session 4 三次尝试都栽在这里）：

1. **「局部极值点的切线归零」是单调 Hermite 的特征，不是 ECharts 的。**
   把单调 Hermite 替成 ECharts 贝塞尔后，bump-chart 的「顶上变水平」
   变成「顶上过冲」——也是 ECharts 的真行为，不是 bug。
2. **控制点正确 ≠ 渲染正确。** 三次尝试后**手算控制点**已与 ECharts
   JS 参考完全一致，但**渲染仍然「麻花」**——根因在下游
   （bezier 采样率 `steps = segW/256` 在长斜线段可能降到 2，
   把贝塞尔退化成折线；或描边光栅器对子像素控制点的处理不同）。
   排查**必须**用探针把控制点和 `steps` 同时打印出来，
   至少验证：`cp0.x/cp0.y/cp1.x/cp1.y` 与 `_scratch/official_shots/`
   同一数据下采样后一致。
3. **Zan 窗口 3222 宽、官方 1200 宽——同一算法视觉差 2.7×。**
   同样 75px 过冲，官方看不见、Zan 显眼。**不要靠像素 diff 判等**，
   要把 Zan 用 1200×780 的等比裁切后再比（见 _scratch/compare_shot.ps1）。
4. **Zan 凸图（bump-chart）的「端点过冲」是 ECharts 行为**。
   如果产品想要不过冲，得改默认 `smooth` 张力（如 0.3），
   **或**用 `smoothMonotone:'x'` / `'y'`，**或**画分类型图（line 改 bar）。
   引擎层不修。
5. **「鼠标经过没响应」可能是 IME 抢焦点**——微软拼音/搜狗候选窗口
   出现在 Zan 截图中时，是 IME 在拦截输入，**不是 hover 不工作**。
   先 dismiss IME 再复现。
6. **会话中**改 smooth 算法超过两次没收敛——立即回退
   `git checkout HEAD -- stdlib/Gui/Component/Chart/ChartViewLine.zan`
   并把「无结论」写进 CHART_RESIDUAL。**不要**继续在 commit 之间
   反复猜测。ECharts 6.1 poly.ts 是一段精密但**对稀数据不稳定**的
   算法，凭眼睛和直觉调试不收敛。

**已验证 commit**：
- `ec24a91b` 修复了 Y-extent（dataZoom 窗口）、axisLabel.margin、
  time-axis `points.x` 去定点。**不**碰 smooth 算法。
