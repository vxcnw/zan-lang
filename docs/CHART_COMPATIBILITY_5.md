# Zan Chart 与 ECharts 官方示例的迁移账本

## 目标与口径

图表引擎的对照基准从 ECharts 2.2.7 迁移到 **ECharts 官方示例站当前版本
（2026-09 起为 6.1.0+）**（apache/echarts，echarts.apache.org/examples）。
画廊 `examples/gui_charts` 按**官方示例注册表**的类目与顺序 1:1 重建：
id = 官方注册表 id，标题取注册表中英文原文，option 与数据**逐字**取自
官方示例源码；`Math.random` 一律换成固定种子 LCG（同点数同分布，截图
可复现）。

- 参考源码快照：`_scratch/ref5/<id>.js`（306 例，官网拉取即 6.x 行为）+
  `_scratch/ref5_manifest.md`（官方顺序与依赖标注）；引擎默认值的权威
  基准是 v6.1.0 源码 `_scratch/echarts-master/`（临时工作材料，不入库）：
  色板/组件色 `src/visual/tokens.ts`，根默认 `src/model/globalDefault.ts`，
  轴默认 `src/coord/axisDefault.ts`，图例默认 `src/component/legend/LegendModel.ts`。
  本文件是长期账本。
- **缺口不绕过**：引擎暂缺的特性（下表）在示例侧记录并跳过对应视觉/交互，
  不用变通数据假装对齐；修引擎后回归补齐。
- 引擎**默认值**随官方当前版本走（6.x），旧版默认在引擎层翻转，不逐例覆盖。
- 只收官方注册表里的示例：不掺旧版画廊演示，不创造官方没有的示例。

## 进度

官方注册表 377 例（line 36 / bar 40 / scatter 33 / map 23 / matrix 14 /
custom 20 / …）已全部内嵌为 `examples/gui_charts/options/*.json` +
`charts-registry.json`（`zanc --embed`），demo 层只加载渲染，不掺自造
数据。渲染正确性由引擎子系统覆盖度决定：缺口见上表，按菜单顺序
"发现一个修一个"；map/geo、custom、pictorialBar、matrix、parallel、
themeRiver、graphic、dataset transform 等子系统仍缺。map/geo、custom、pictorialBar、matrix、parallel、
themeRiver、graphic、dataset transform 等子系统仍缺。每批闭环：移植 → 构建 → 截图对照官方 → 提交。

## 引擎缺口账本（示例侧已记录，未修引擎）

| 缺口 | 受影响官方示例 | 备注 |
|------|----------------|------|
| 值对坐标定点管线（ChartPoint 小数 x/y + X 定点域 + YOfF 整域定点） | line-function、scatter 回归类 | 引擎 ChartPoint 目前仅 int 坐标 |
| dataZoom 滑杆拖拽 + inside 滚轮缩放 | 全部 [dataZoom] 例 | 当前只渲染初始窗口 |
| smooth 默认值应为 false | 全部 line | 现由每例显式设置兜底 |
| markPoint pin 符号 + 标签内置 | line-marker 等 | 引擎画圆 + 值在点上方 |
| markPoint 小数坐标 / markLine label.position、端点符号 | line-marker | 周最低 @(-1.5) |
| markArea（保护区） | area-rainfall、line-aqi 等 | |
| 面积 LinearGradient 渐变 | area-simple、area-stack-gradient | 引擎实色 alpha |
| lttb 抽样 | area-simple | 全量直绘 |
| toolbox（官方版） | 全部 | 引擎有自己的内置工具钮 |
| 轴 label 多行（\n） | area-rainfall x 轴 | DrawText 单行 |
| tooltip axisPointer label 背景色 | area-rainfall | cross 本体已实现 |
| minorTick / minorSplitLine | line-function | |
| 双 y 轴 inside 缩放（y 向 zoom） | line-function | x 向用索引百分比近似 |
| emphasis.focus 系列高亮 | line-stack、area-rainfall 等 | |
| axisLine.onZero | area-rainfall | 值域非负时视觉一致 |
| 多 x 轴 | multiple-x-axis | 多 grid 已支持（grid-multiple 对齐：多面板渲染 + 单 dataZoom 滑杆挂末面板，2026-09-09） |
| axis.breaks | intraday-breaks-* | |
| dataset / dataTransform | dataset-* 例 | |
| visualMap continuous（连续色域） | line-gradient 等 | piecewise 分段已于 2026-09-09 落地（分段描边 + 面积分色 + dimension:0 类目域） |
| 动态数据流（定时追加） | dynamic-data2 | 静态首帧渲染已对齐（2026-09-09） |
| 时间轴组件 timeline | — | |

## 引擎默认值已随官方当前版本（6.x）翻转

- `yAxis.splitArea`：2.2 数值轴默认开、5.x 默认关。已加 `ChartAxis.splitArea`
  字段（默认 false，工厂/clone/JSON parse 三处一致），Chart.zan 底纹绘制按
  字段开关（2026-09-09）。
- **默认色板 = ECharts 6.1 主题九档**（2026-09-09）。权威值
  `_scratch/echarts-master/src/visual/tokens.ts` color.theme：
  `#5070DD #B6D634 #505372 #FF994D #0CA8DF #FFD10A #FB628B #785DB0 #3FBE95`。
  `ChartSkin.ColorAt("default")` 从 2.x 的 20 档（#FF7F50 coral 系）整排
  换成 v6 九档（%9）；`Chart.Palette` 末级兜底同批换成 v6。infographic/
  shine/macarons2 等官方主题包皮肤保持原样。
- **水平图例默认画在面板底部居中**（2026-09-09）。权威值
  `src/component/legend/LegendModel.ts` defaultOption：`left 'center' +
  bottom tokens.size.m`。引擎 DrawPanelI：水平图例底部起排（行数计入
  `Chart.legendBottomReserve`，BuildAxesR/DrawFrameLoHiT/散点/极坐标/
  误差棒各绘图区公式从底边扣除，含 x 轴刻度带 gutter）；竖排图例
  （orient vertical，官方例显式声明）保持顶部标题行之下左对齐。
  旧 2.2 式"顶部右侧从右往左"图例布局删除。
- v6 其余默认差异（未翻转，随需要再动）：轴轴线/刻度/标签色
  `#54555A`（neutral70）、分割线 `#DBDEE4`（neutral15，现随 Gui 皮肤
  token，视觉中性）；grid outerBounds 标签防溢出（轴可能微移，
  `outerBoundsMode:'none'` 可关）；label.rich 继承普通标签字体属性
  （`richInheritPlainLabel:false` 可关）。

### 已修的引擎缺陷（来自官方示例移植）

- 数据值 × 动画因子 g 的 int32 溢出（2026-09-09）。bar-waterfall 堆叠和
  2900（×1000 定点 = 2.9e6）乘 g(0..1000) 超 2^31，终帧 yTop 算到零线下方
  → 整段柱"消失"。修复：全部数据值 × g 位点（柱/线/散点/极径/误差棒/
  漏斗宽/大图）改 long 乘法；像素/扫描角/透明度等有界位点不动。教训：
  小数值验证不出的时变缺陷先怀疑溢出类，用终态帧（g=1000）定点追踪。
- `transparent` 哨兵色 `Chart.Transparent()`（alpha≈1 非零，避免与
  0=继承系列色冲突），瀑布图占位系列用。
- `YOfF` 整数轴回落路径定点化：vF(×1000) 对 [lo×1000, hi×1000] 比例映射，
  整数数据与旧 int 路径逐像素一致；堆叠感知的 frac 轴界
  （HasStackedBarsF/StackExtentF 折入 FracAxisLo/Hi）。
- 时间轴域改 epoch 天 + TimeTicks long 化（2026-09-09）。引擎时间域全程
  int32 epoch **天**；此前数据解析把 epoch 秒直接塞 int（2038 后溢出为负，
  epoch ms 恒溢出），area-time-axis 18100 点（跨度跨 2038）解析成负域，
  TimeTicks 里 `int span = t1 - t0` 变负 → 步进阶梯立即断档按步长 1 逐天
  建刻度 → 43 亿次 List.Add、17–33GB 内存挂死。修复：TimeDayOf 解析
  （秒/ms/日期字符串 → 天），TimeTicks span/step/循环全部 long。教训：
  大跨度时间数据挂死/空白先查 int32 纪元溢出，用点数二分定位
  （18000 过 / 18100 挂 = 2147011200 秒边界）。
- series 单对象形式（2026-09-09）。ECharts 单系列 options 常写
  `series: {...}`（line-aqi），解析器此前只收数组 → "(no data)"。解析
  入口按 IsObject/IsArray 双形态展开。
- symbolSize 语义 = 直径（2026-09-09）。ECharts symbolSize 是直径，
  SymbolRadius 此前原值当半径 → bump-chart 空心大半圆。现返回
  symbolSize/2；数据级 item symbolSize 仍按半径（遗留，随需要翻转）。
- dataZoom startValue/endValue（2026-09-09）。ECharts 允许用类目文本
  定窗口（line-aqi '2014-06-01'）；ZoomI0/ZoomI1 渲染期先 CategoryIndexOf
  解析成索引再算 permille 窗口。
- 分段 visualMap 面积叠加走稠密平滑路径（2026-09-09）。area-pieces 的
  分色填充此前按数据点分段直连，平滑曲线下出现月牙缝；现沿 pathX/pathY
  稠密路径切窗填充。分段描边（起点段颜色硬切）此前已有。
- yAxis.interval 显式（2026-09-09）。min/max 与 interval 同时给时
  ticks = (max-min)/interval（bump-chart interval:1 → 9 档反序轴）。
- 时间域窗口化（2026-09-09）。BuildAxesR 有 dataZoom 时按 ZoomI0/ZoomI1
  扫可见窗口定时间域（area-time-axis 0–20% 窗口拉满绘图区），不再全量
  定域；ECharts filterMode 的 y 向窗口域仍未做（见待办）。

## 待办

- 值对坐标定点管线（见缺口表首行）：补齐后 line-function 按官方位置回补
  目录（func(x)=sin(x/10)·cos(2x/10+1)·sin(3x/10+2)·50，x∈[-200,200]
  步长 0.1，y 固定 ±100，x 向 inside 缩放初始 [-20,20]；Math.Sin/Cos
  内置已就绪，conformance `builtin_math_trig` 覆盖）。
- line-markline 标签位、confidence-band 置信带、
  line-log 对数轴小数：随引擎能力补齐逐例回补。
- dataZoom filterMode 的 y 向窗口域：窗口内数据重定 y 轴范围
  （area-time-axis 当前 y 仍按全量 -2000..2000，官方窗口内约 -900..1000）。
