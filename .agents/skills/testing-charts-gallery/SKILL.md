---
name: testing-charts-gallery
description: Zan charts gallery (examples/gui_charts, 335 ECharts 官方对照 demo) 的构建、截图、探针与修复定式——recheck2 截图驱动、bindprobe 解析态探针、--bench 帧计时、stdlib 快照同步坑、多 grid/dataZoom/定点数值三大契约。凡是要验证或修复 stdlib/Gui/Component/Chart 引擎改动、核对某个 demo 与 ECharts 官方语义是否一致、排查"图表空板/缺元素/多面板窗口不同步"时使用。
---

# Charts gallery 验证与修复定式（Windows 实机）

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

## 已知刻意偏差（勿当 bug 修）

- candlestick-touch.json 的 grid px 已 ×2.4（适配本机更高的画布）。
- scatter-matrix.json 删了 parallel 系列（引擎无平行坐标系，记 TASKS 债）。
- media 响应式查询、graphic 元素不支持（data-transform-multiple-pie
  竖排是 base option 的样子，官方横排来自 media，不是 bug）。

## ctest 档位

stdlib Chart 改动 → `cd build && ctest -R conformance_chart`（26 例，~96s）。
两个 golden（chart_option_behavior.out 的 sr、chart_pie_layout.out 的 pal）
曾在语义提交（symbolSize 直径、v6 色板）时没跟上，属欠账——引擎语义
提交必须连 golden 一起核对，否则 standard 档永远挂着看不见的失败。
