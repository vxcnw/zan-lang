# Zan Chart 与 ECharts 5 官方示例的迁移账本

## 目标与口径

图表引擎的对照基准从 ECharts 2.2.7 迁移到 **ECharts 5**（apache/echarts，
echarts.apache.org/examples）。画廊 `examples/gui_charts` 按**官方示例注册表**
的类目与顺序 1:1 重建：id = 官方注册表 id，标题取注册表中英文原文，option
与数据**逐字**取自官方示例源码；`Math.random` 一律换成固定种子 LCG（同点数
同分布，截图可复现）。

- 参考源码快照：`_scratch/ref5/<id>.js`（306 例）+ `_scratch/ref5_manifest.md`
  （官方顺序与依赖标注）。快照属于一次性工作材料，不进版本库；本文件是
  长期账本。
- **缺口不绕过**：引擎暂缺的特性（下表）在示例侧记录并跳过对应视觉/交互，
  不用变通数据假装对齐；修引擎后回归补齐。
- 引擎**默认值**随 5.x 走，2.2 时代的默认在引擎层翻转，不逐例覆盖。

## 进度（按官方顺序逐批补位）

| 段 | 已移植 | 说明 |
|----|--------|------|
| line (40) | 13 | line-simple / line-smooth / area-basic / line-stack / area-stack / line-marker / area-simple / area-rainfall / area-time-axis / line-style / line-in-cartesian-coordinate-system / line-step / line-y-category |
| bar (46) | 0 | 下一批 |
| 其余段 | 0 | pie → scatter → candlestick → gauge → funnel → radar → … 按注册表顺序 |

每批闭环：移植 → 构建 → 截图对照官方 → 提交。目录里只放已移植条目，
未移植的随批按官方位置插入。

## 引擎缺口账本（示例侧已记录，未修引擎）

| 缺口 | 受影响官方示例 | 备注 |
|------|----------------|------|
| dataZoom 滑杆拖拽 + inside 滚轮缩放 | 全部 [dataZoom] 例 | 当前只渲染初始窗口 |
| 5.x 默认配色主题（palette） | 全部 | 引擎仍是 2.2 色板 |
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
| 多 x 轴 / 多 grid | multiple-x-axis、grid-multiple | |
| axis.breaks | intraday-breaks-* | |
| dataset / dataTransform | dataset-* 例 | |
| visualMap | area-pieces、line-gradient 等 | |
| 动态数据流（定时追加） | dynamic-data2 | |
| 时间轴组件 timeline | — | |

## 引擎默认值已随 5.x 翻转

- `yAxis.splitArea`：2.2 数值轴默认开、5.x 默认关。已加 `ChartAxis.splitArea`
  字段（默认 false，工厂/clone/JSON parse 三处一致），Chart.zan 底纹绘制按
  字段开关（2026-09-09）。

## 待办

- `Math` 内置补 `Sin/Cos/Tan`（builtin_api.c）：line-function 及后续 custom
  段大量依赖；补齐后 line-function 按官方位置回补目录。
- line-markline 标签位、confidence-band 置信带、bump-chart endLabel、
  line-log 对数轴小数：随引擎能力补齐逐例回补。
