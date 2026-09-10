# Gui.Component.Chart

> 源码: `stdlib/Gui/Component/Chart/Chart.zan`, `stdlib/Gui/Component/Chart/ChartBig.zan`, `stdlib/Gui/Component/Chart/ChartController.zan`, `stdlib/Gui/Component/Chart/ChartEvents.zan`, `stdlib/Gui/Component/Chart/ChartGeoJson.zan`, `stdlib/Gui/Component/Chart/ChartHost.zan`, `stdlib/Gui/Component/Chart/ChartLayoutRelation.zan`, `stdlib/Gui/Component/Chart/ChartLayoutSpecial.zan`, `stdlib/Gui/Component/Chart/ChartMaps.zan`, `stdlib/Gui/Component/Chart/ChartModel.zan`, `stdlib/Gui/Component/Chart/ChartResolved.zan`, `stdlib/Gui/Component/Chart/ChartSkin.zan`, `stdlib/Gui/Component/Chart/ChartSvgMap.zan`, `stdlib/Gui/Component/Chart/ChartTheme.zan`, `stdlib/Gui/Component/Chart/ChartTimeline.zan`, `stdlib/Gui/Component/Chart/ChartToolbox.zan`, `stdlib/Gui/Component/Chart/ChartView.zan`, `stdlib/Gui/Component/Chart/ChartViewBar.zan`, `stdlib/Gui/Component/Chart/ChartViewDataRange.zan`, `stdlib/Gui/Component/Chart/ChartViewEventRiver.zan`, `stdlib/Gui/Component/Chart/ChartViewFinance.zan`, `stdlib/Gui/Component/Chart/ChartViewHeatmap.zan`, `stdlib/Gui/Component/Chart/ChartViewHier.zan`, `stdlib/Gui/Component/Chart/ChartViewLine.zan`, `stdlib/Gui/Component/Chart/ChartViewMap.zan`, `stdlib/Gui/Component/Chart/ChartViewMore.zan`, `stdlib/Gui/Component/Chart/ChartViewPictorial.zan`, `stdlib/Gui/Component/Chart/ChartViewPie.zan`, `stdlib/Gui/Component/Chart/ChartViewPolar.zan`, `stdlib/Gui/Component/Chart/ChartViewRelation.zan`, `stdlib/Gui/Component/Chart/ChartViewScatter.zan`, `stdlib/Gui/Component/Chart/ChartViewShared.zan`, `stdlib/Gui/Component/Chart/ChartViewVenn.zan`


## BoxItem (class)

箱线图统计量（最小值、下四分位数、中位数、上四分位数、最大值）。
分类标签与统计值一起携带，调用方不会因
并行列表而使标签与数值失同步。

- string label;

- int lo;

- int q1;

- int med;

- int q3;

- int hi;

- static BoxItem Of(string label, int lo, int q1, int med, int q3, int hi)
  - 构造一个箱线统计项（五数概括 + 分类标签）。

- static BoxItem Clone(BoxItem src)
  - 深复制；src 为 null 时返回 null。


## Bubble (class)

加权散点（x、y 和一个决定气泡大小的权重）。

- int x;

- int y;

- int weight;

- static Bubble Of(int x, int y, int weight)
  - 构造一个加权散点。

- static Bubble Clone(Bubble src)
  - 深复制；src 为 null 时返回 null。


## Candle (class)

金融/蜡烛图的一个 OHLC 柱。

- int open;

- int high;

- int low;

- int close;

- ChartItemStyle itemStyle;

- static Candle Of(int open, int high, int low, int close)
  - 构造一根 OHLC 柱。

- static Candle Clone(Candle src)
  - 深复制；src 为 null 时返回 null。


## Chart (class)

ChartView 渲染器共享的绘图工具：颜色、比例辅助、
面板/图例框架、dataZoom 滑块、标记线/区域、直角坐标系和
双轴坐标构建器。一次性的静态渲染器（Chart.Line/
Bar/Pie/...）已移除——所有图表现在声明为 ChartOption
并由 ChartView 绘制。

- static int Rgb(int r, int g, int b)
  - 不透明 0xFFRRGGBB 打包为正 int（Canvas 转 u32）。
    r/g/b 各 0..255。

- static int WithAlpha(int packed, int a)
  - 与打包不透明颜色相同的 RGB，但替换 alpha（0 透明..255 不透明，
    用于面积/扇区填充）。

- static int Transparent()
  - ECharts 'transparent'：alpha 1/255 的白色——合成后每通道
    偏移 ≤1，视觉不可见；取非 0 值是为了不与"0 = 继承系列色"
    的图表着色语义冲突（瀑布图透明占位柱）。

- static int ContrastFg(int bg)
  - 在 `bg` 上对比足够的前景：浅底深字、深底白字。
    饼图扇区 / 地图填色上的标签用它，避免白字画在黄块上。

- static int toolReserve;
  - 本帧工具箱占用的右上角宽度；DrawPanelI / PanelHead 让开它。

- static ChartOption legendOpt;
  - 本帧 option（图例子字段 orient/selectedMode/formatter 的来源）；
    Render() 分派前置位，与 toolReserve 同为帧内静态。

- static int legendBottomReserve;
  - 本帧水平图例占用的底部高度（ECharts 6 默认图例在底部，
    BuildAxesR 从绘图区底边扣除；竖排图例在顶部占位，此值为 0）。

- static bool gridPanelSub;
  - 多 grid 子面板帧内约定（DrawMultiGridPanels 置位/复位）：
    grid 矩形是纯绘图区，标题/工具箱是页级元素由派发层画一次，
    子面板不再按 PanelContentTop 预留头部（96px 成交量条带曾被
    59px 头部啃到 30px 绘图区）。

- static bool zoomBarHidden;
  - 多 grid 子面板：zoom 窗口全格生效（官方 dataZoom
    xAxisIndex:[0,1] 同窗联动），但滑条条带只随最后一个 grid
    画一次——非末格置位，视图据它跳过 zoomH 预留与 DrawZoomBar。

- static int RampAt(List<int> colors, int t)
  - 多段线性色带插值（visualMap inRange）：t ∈ [0,1000] 均匀映射
    到 colors 首尾之间，段内线性混合。colors 少于 2 个时取首色。

- static int Palette(Theme t, int i)
  - 定性调色板第 i 档：图表皮肤（ChartSkin）优先——图表配色是
    独立板块，不占全局皮肤主题的 token；当前皮肤 8 档齐全，
    命中即返回。皮肤之后依次是主题的 --chart-1 .. --chart-8
    token（Theme.chart1..8，0 = 该槽位未定义）与 ECharts 6.1
    默认主题调色板（src/visual/tokens.ts，9 档）兜底。

- static int SeriesPaintColor(ChartSeries s, Theme t, int index)
  - 系列普通状态的统一颜色回退：显式系列色、normal.color、调色板。
    ResolvedChart 会把结果物化到 series.color；此 seam 也保护
    DrawPanelI 与 ChartBig 这类可直接接收原始 series 的路径。

- static void DrawSymbol(Canvas c, int cx, int cy, int r, string shape, int color, int borderColor, int borderWidth)
  - 符号形状族绘制（ECharts series.symbol）：shape 取
    circle（默认实心圆）/ emptyCircle（环）/ rectangle / diamond /
    triangle。r 为外接半径；borderWidth>0 时用 borderColor 描边。
    全部为不透明覆盖、无二次混合，指纹稳定。

- static int SymbolRadius(int symbolSize, int defaultR)
  - symbolSize -> 外接半径。ECharts2 语义 symbolSize 是「半宽
    （半径）参数」（config.js markPoint 注释：总宽度为
    symbolSize * 2），传入值本身就是半径，不再折半。

- static void PolyVerts1000(string shape, List<int> vx, List<int> vy)
  - 符号形状的顶点表（千分比相对坐标，y 向下为正），由
    FillPoly1000 缩放到像素。star = 五角星（内接比 382），
    star6 = 六角星（内接比 577 ≈ 1/√3），arrow = 上指箭镞，
    droplet = 上尖水滴，heart = 心形（zrender Heart 贝塞尔
    采样近似：底尖在下、双瓣在上），pin/emptypin = 地图气球。

- static void FillPoly1000(Canvas c, int cx, int cy, int r, List<int> vx, List<int> vy, int color)
  - 顶点多边形扫描线填充（偶奇规则）：顶点为千分比相对坐标，
    逐行求交点、成对 FillRect。顶点数 ≤ 12，插入排序开销可忽略。

- static bool LabelShown(int ci, int interval)
  - axisLabel.interval 语义（ECharts）：-1/非整数 = 自动（渲染器
    走防重叠贪心），>=0 = 每 (interval+1) 个画一个。纯函数，
    conformance 直接断言。

- static List<int> CategoryTicks(ChartFrame f, List<string> labels, int fs, int plotX, int labelGap, ChartAxis x0)
  - 类目轴 auto 抽稀的共用判定：返回窗口内实际显示标签的类目
    下标（升序）。ECharts 2 中 axisLabel.interval 缺省 'auto'，
    splitLine 与折线拐点符号（isMainIdx）与标签同源——密集类目
    轴的竖网格和符号都只落在显示标签的刻度上，不再逐类目一条
    （雨量图 3079 点曾把竖线糊成整幅灰罩、折线满线小圆点）。
    规则与 BuildAxesR 标签绘制一致：显式 interval 走 LabelShown、
    旋转标签不抽稀、刻度模式（boundaryGap=false）首标签豁免
    （ECharts 始终画边界刻度），其余贪心让位。

- static int RotatedLabelH(int maxW, int fh, int deg)
  - 旋转分类标签的竖直占位（像素）：行盒 w×h 绕锚点旋转
    |deg| 度后的垂直跨度 = w·|sin| + h·|cos|。用 ChartView 的
    1000 倍三角表，确定性整数。

- static int NiceMax(int v)
  - 将原始最大值向上取整为友好的轴上界（2/5/10 * 10^n）：
    37 -> 50、830 -> 1000。<=5 时返回 5。

- static int AxisMinForF(List<ChartSeries> series, int axisIndex)
  - AxisMinFor 的 1/1000 定点对偶：与 AxisMaxForF 成对——原始
    数据下界直传（不许钳零），小数轴量程专用。

- static bool HasStackedBarsF(List<ChartSeries> series, int axisIndex)
  - 轴上是否存在共享 stackName 的柱族系列（堆叠柱）。小数堆叠柱
    的量程须按类目堆叠和推导，逐项极值会低估堆叠顶
    （normalization 各项 ≤0.57、堆叠顶达 1.0）。

- static ChartSpan StackExtentF(List<ChartSeries> series, int axisIndex)
  - 堆叠柱（共享 stackName 的柱族）逐类目正/负堆叠和（×1000
    定点）：hi = 正累加器最大值，lo = 负累加器最小值。正负独立
    累计与渲染路径同一语义（负段不与正段相加）。

- static int FracAxisLoF(int fixedLo, List<ChartSeries> series, int axisIndex)
  - 小数轴 extent 下界（×1000 定点）：固定 min 直接生效，否则
    原始数据下界直传（不预设 nice——向下取整是 smartSteps 的
    职责，valueAxis._calculateValue 语义）。堆叠柱并入类目堆叠
    和的负向极值。

- static int FracAxisHiF(int fixedHi, List<ChartSeries> series, int axisIndex)
  - 小数轴 extent 上界（×1000 定点）：固定 max 直接生效，否则
    原始数据上界直传。堆叠柱并入类目堆叠和的正向极值。

- class ChartSpan
  - ECharts 2 数值轴 nice 量程结果（lo/hi 取整到步长倍数）。

- class ChartExp
  - expNum 的 {c, e}：近似值 = c × 10^e。

- static int FloorDivQ(int a, int b)
  - a / b 的数学 floor（Zan 的 / 与 % 向零截断）。

- static int CeilDivQ(int a, int b)
  - a / b 的数学 ceil。

- static int DecDigits(int v)
  - 十进制位数（v ≥ 1）。

- static int StripZeros(int v)
  - 去掉十进制尾部 0（全精度有效位计数用）。

- static int JSRoundHalf(int q)
  - JS Math.round(q / 2)（半数朝 +∞，q 可为负）。

- static ChartExp ExpNum2Rat(int num, int den)
  - expNum(num/den, 2 位精度，向上)：v = num/den ≥ 0 的两位有效数
    上近似。对应 smartSteps 里 getCeil/expSpan 的 expNum(v, 2)。

- static ChartExp ExpNumFull(int n, bool byFloor)
  - expNum(n, 全精度)：整数 n 的精确分解（c × 10^e = n）。
    byFloor 只在指数对齐除法时区分 floor/ceil。

- static void SmartCeilStep(ChartExp n)
  - getCeil：两位尾数向上吸附到步长备选 [10,20,25,50]。

- static void ExpAlign(ChartExp x, ChartExp refx, bool byFloor)
  - expFixTo：把 x 的指数对齐到 ref（缩指数乘 10 精确，升指数
    按 byFloor floor / 否则 ceil 除）。

- static ChartSpan SmartForInteger(int min, int max, int section)
  - smartSteps 的 forInteger：跨度小于段数时向两侧延展跨度
    （section ≤ 0 时取 5 段），输出压回与原数据同侧。

- static int SmartTryForInt(int min, int max, ChartExp expMin, ChartExp expMax, int secs)
  - smartSteps 的 tryForInt：原最值同号（含 0）时尽量取整数步长，
    剩余误差向两侧均衡（可能改写 expMin/expMax 并强制 e = 0）。

- static ChartSpan SmartCoreCalc(int min, int max)
  - smartSteps 的 coreCalc（section = 0 自适应路径）：
    步长基准取 ceil(span/6)，段数在 [6,5,4] 中选（调整后跨度最小、
    同跨度步长小者胜），整数输入尽量整数步长并均衡误差。

- static int ExpRestore(ChartExp x)
  - c × 10^e 的整数还原（e < 0 时 c 必是 10^-e 的倍数）。

- static ChartSpan NiceRange(int lo, int hi)
  - ECharts 2.2.4 valueAxis 自动刻度（与演示站一致）：
    内层是 src/util/smartSteps.js（section=0 自适应路径）的忠实
    移植，外层套 valueAxis._reformValue 的非 scale 规则——
    同号数据一端归零（全正 min→0、全负 max→0）与 min==max 整形。
    -2..15 → -5..15/4 段、0..1320 → 0..1500/6 段、0..2570 →
    0..3000/6 段。固定 min/max 不走此函数（尊重不取整）。

- static ChartSpan ScaleRange(int lo, int hi)
  - ECharts2 valueAxis scale:true（不强制含 0）+ boundaryGap
    [0.01,0.01] 的量程：数据域两端各外扩 1% 后对齐 nice 步长
    （1/2/2.5/5×10^k，splitNumber 5 预估），一端不归零——若按
    NiceRange 的非 scale 规则把全正数据零锚定，2200..2450 的
    蜡烛会被压进 0..2500 步长 500 的底部。k1 原版 → 2200..2450
    步长 50。

- static int MaxOf(List<ChartSeries> series)
  - 全部系列中的最大值（隐藏系列不计），下界 0。

- static int MinOf(List<ChartSeries> series)
  - 系列中的最小值（无负数时为 0，隐藏系列不计）。水平条 / 旋风图用
    它把轴下界扩到 0 以下，而不是把负值裁成空柱。

- static int ValueX(int plotX, int plotW, int lo, int hi, int v)
  - 数值 → 水平像素：plotX 对应 lo，plotX+plotW 对应 hi。
    大数值 × plotW 会超 int32（bar3 Population 到百万：
    1000000×2601≈2.6e9），乘法走 long。

- static int ValueXF(int plotX, int plotW, int lo, int hi, int v, int g)
  - 定点数值 → 水平像素：v 以 值×g 承载（PointV 约定），分母按
    span×g 缩放后再除——亚单位像素精度不丢（先 PointV 取整会把
    小数坐标量化到整数值格点，scatter3 的 3 位小数云会塌成点阵）。

- static int ValueYF(int plotY, int plotH, int lo, int hi, int v, int g)
  - 定点数值 → 垂直像素（ValueXF 的纵轴对偶）。

- static int ValueY(int plotY, int plotH, int lo, int hi, int v)
  - 数值 → 垂直像素：plotY+plotH 对应 lo，plotY 对应 hi（向上增大）。
    同 ValueX：乘法走 long 防大数值 × plotH 溢出。

- static int ValueYF1000(int plotY, int plotH, int loF, int hiF, int vF)
  - 1/1000 定点值 → 垂直像素：lo/hi（值×1000）之间的线性映射，
    小数轴（leftMinF 定点域）的 YOfF 用——与 ValueY 同构，
    分子分母同放大 1000 后 long 相除，亚单位值不再量化。

- static int MaxOfWindow(List<ChartSeries> series, int i0, int i1)
  - 仅索引窗口 [i0,i1]（含端点）内的最大值，供 dataZoom
    的索引视图使用（渲染循环直接读原系列，不做有损克隆）。

- static int MaxStack(List<ChartSeries> series, int n)
  - 各分类中的最大堆叠总量（用于堆叠柱状图）。
    共享 stackName 的系列堆叠在一起；轴适配最高的组，
    使多组堆叠柱（ECharts `stack` 组）正确缩放。`n` 为分类数。

- static int MaxStackW(List<ChartSeries> series, int n, int i0)
  - MaxStack 的索引窗口版：仅累计分类 j + i0（j 在 [0,n)）。

- static int MaxStackAll(List<ChartSeries> series, int n)
  - 所有系列堆叠成一条带时的最大累计总量（堆叠面积图
    / 堆叠折线图：系列按顺序累加，与 stackName 无关）。
    隐藏的系列（图例关闭）被跳过，因此隐藏一个系列
    会重设轴范围，剩余条带正确重新堆叠。

- static int MaxStackAllW(List<ChartSeries> series, int n, int i0)
  - MaxStackAll 的索引窗口版：仅累计分类 j + i0。

- static int MaxStackGroupsW(List<ChartSeries> series, int n, int i0)
  - 堆叠感知的窗口最大值：逐 stackName 组累计组顶，未堆叠
    系列（stack=0）只按绝对值计入（ECharts 轴量程覆盖组顶与
    绝对值的最大者，绝对值不进累加和——多级控制混合图）。

- static int MaxBarStackGroupsW(List<ChartSeries> series, int n, int i0)
  - 堆叠柱（ECharts 2.2.x 负向堆积）的正侧组顶：各组正值
    依序累计，未堆叠系列按绝对值计入；负值不进正向累加
    （bar.js 正负独立累加器，bar5：收入向右、支出向左）。

- static int MinBarStackGroupsW(List<ChartSeries> series, int n, int i0)
  - MaxBarStackGroupsW 的负侧对偶：各组负值依序累计出组底
    （未堆叠系列只取自身的负值），返回值 ≤ 0。

- static int MaxInt(List<int> vs)
  - 列表最大值，下界 0（无负值语义）。

- static bool PointInPoly(List<ChartMapPoint> poly, int px, int py)
  - 整数 point-in-polygon（射线法，even-odd），无除法/浮点。
    半开约定：py >= 顶点 y 视为在射线之上，每条边最多计一次
    穿越；交点侧由叉积符号结合边方向判定。点在边界上属边缘
    情形，结果不保证——由命中层的 bbox 容差吸收。

- static int Log10(int v)
  - 10 的整数对数（floor log10），仅正值（v < 1 → 0）。

- static int Pow10(int e)
  - floor(log10) 的确定性整数逆；超出 int 范围时饱和为 2147483647。

- static List<int> LogTicks(int lo, int hi)
  - 对数轴刻度：lo/hi 边界 + 中间的 10 的幂（去重，升序）。

- static string TimeLabel(int t)
  - 从 epoch 天生成确定性短日期 "YYYY-MM-DD"（真实公历，经
    DateTime 的 civil-from-days；t = 0 是 1970-01-01）。纯表
    驱动、无系统时间依赖，供图表演示与 conformance 断言。

- static List<int> TimeTicks(int t0, int t1, int maxTicks)
  - 时间轴刻度：从 {1,2,5}×10^n 阶梯选步长，使
    (t1-t0)/step ≤ maxTicks-1；生成 t0 起等距点，
    末点不落在网格上则补 t1。跨度全程 64 位——int32 域
    相减回绕成负会让步长卡在 1、循环 43 亿次撑爆内存。

- static string FormatFixed(double v, int precision)
  - 固定小数位数的确定性格式化（四舍五入，无浮点打印依赖）。
    precision 钳制在 0..4。

- static int DrawPanel(App app, int x, int y, int w, int h, string title, List<ChartSeries> series, bool showLegend)
  - 面板背景 + 标题 + 图例色块。返回标题/图例带
    下方紧邻的 y，调用方可在其下布局绘图区。
    非交互版（wid=0）：图例色块不可点击。需要图例交互时
    用 DrawPanelI。

- static int LegendKey(int wid, int si)
  - 交互 id `wid` 下系列 `si` 的图例隐藏状态键。

- static int DRangeLoKey(int wid)
  - dataRange 交互态：calculable 滑条两端（0..1000 量化，同
    zoom 条约定）与 splitList 分段隐藏位（1 = 该段被点掉）。

- static int DRangeHiKey(int wid)
  - dataRange calculable 滑条上界状态键（千分值 0..1000）。

- static int DRangeBandKey(int wid, int bi)
  - splitList 第 bi 段的隐藏位键（1 = 该段被点掉）。

- static int DRangeHoverKey(int wid)
  - dataRange.hoverLink：指针悬停在 dataRange 条上时该图的高亮键
    （0 = 无；1 = 悬停中，消费方把接近值域的区域/点描边强调）。

- static string LegendLabel(string fmt, string name)
  - legend.formatter 纯 seam：{name} 占位替换（模板空 = 原名）。

- static bool LegendVertical()
  - 本帧图例是否纵向排布（legendOpt 未置 = 横向）。

- static string LegendFmt()
  - 本帧图例 formatter 模板（legendOpt 未置 = 空模板 = 原名）。

- static string TitleSubText()
  - 本帧标题副标题（ECharts title.subtext；legendOpt 未置 = 空）。

- static string TitleAlignMode()
  - 本帧标题水平对齐："left"（默认）| "center" | "right"。

- static string LegendAlignX()
  - 本帧图例水平对齐："left" | "center"（默认）| "right"。

- static int LegendSelMode()
  - 本帧图例点击模式：0 = multiple（现状）| 1 = single |
    -1 = false（不可点）。

- static int DataRangeValue(int dLo, int dHi, int q)
  - dataRange calculable 滑条位置（0..1000）到值域的线性映射
    （纯 seam）：q=0 → dLo、q=1000 → dHi。q 越界钳制。

- static int LegendSliceKey(int wid, int si, int di)
  - 饼/漏斗/玫瑰扇区、和弦/力导节点：按 (系列, 数据项) 持久化隐藏。
    与 LegendKey 分段错开，避免单系列多扇区共用一个键把整图关掉。

- static int PieSelKey(int wid, int si, int di)
  - 饼扇区静态选中位（点击扇区切换 data.selected 的持久键）。

- static int LegendChipW(App app, string label)
  - 单个图例色块占宽：色块 + 间隙 + 标签文本宽 + 右侧留白。

- static int HeadBandBottomValues(int y, int pad, int titleH, int toolboxH, int gap)
  - 标题行与工具箱行的底边：空标题不占大号行高，有工具箱时
    内容从工具箱下方开始，避免标题/色块和工具图标叠在一起。

- static int HeadBandBottom(App app, int y, string title)
  - 按主题内边距与标题/工具箱行高算出面板内容起始 y
    （工具箱存在性取本帧 toolReserve）。

- static bool DrawLegendChip(App app, int lx, int ly, int legendW, int lh, int color, string label, bool hidden, int stateKey)
  - 右侧色块图例一行（独立 AllocId 命中）。stateKey 跨帧持久化：
    点一下切换隐藏（变暗 + 删除线），再点恢复。stateKey=0 时
    纯展示不可点。返回是否刚点中。

- static int ZoomLoKey(int wid)
  - dataZoom 窗口状态键（分类范围的千分值 0..1000）。

- static int ZoomHiKey(int wid)
  - dataZoom 窗口上界状态键（千分值 0..1000，配对 ZoomLoKey）。

- static int TreePanXKey(int wid)
  - 树图视口平移 X（像素；世界原点相对视口的偏移）。

- static int TreePanYKey(int wid)
  - 树图视口平移 Y（像素）。

- static int TreeDragXKey(int wid)
  - 树图拖拽中最近一次指针 X。

- static int TreeDragYKey(int wid)
  - 树图拖拽中最近一次指针 Y。

- static int TreeDragPanXKey(int wid)
  - 树图拖拽按下瞬间的视口平移 X 快照（拖拽期间平移 = 快照 - 位移）。

- static int TreeDragPanYKey(int wid)
  - 树图拖拽按下瞬间的视口平移 Y 快照。

- static int TreeDraggingKey(int wid)
  - 树图拖拽进行中标志（1 = 按下未释放；释放帧清零）。

- static int TreeDragMovedKey(int wid)
  - 树图本次拖拽是否实际移动过（1 = 移动过；释放时吞掉 click）。

- static int TreeZoomKey(int wid)
  - 树缩放，为自然节点间距的百分比。0 表示尚未适配：
    首帧（或工具箱「还原」）把整棵树放进视口中心，之后镜头
    就是无限画布——平移不夹紧、缩放不因窗口尺寸变化而重置。

- static int TreeHitKey(int wid)
  - 树图漫游（平移/滚轮/拖拽）的稳定命中 id：AllocId 每帧换号
    会让滚轮/拖拽丢目标，此键给出跨帧稳定的 id。

- static int CacheKey(int slot)
  - 快照槽位的 RenderCache 指纹键（见 ChartView.RenderCached）。

- static int TbViewKey(int wid)
  - toolbox / 地图漫游 / 选中（与 Tree* 8000000 段错开）。
    数据视图覆盖层开关（1 = 打开，由工具箱「数据视图」切换）。

- static int TbMagicKey(int wid)
  - 魔法类型切换状态（1 = 切为折线，2 = 切为柱状，0 = 关）。

- static int TbZoomKey(int wid)
  - 区域缩放工具开关（1 = 开）。

- static int MapZoomKey(int wid)
  - 地图漫游缩放（百分比 40..280；读到的值 < 40 视为未初始化，
    重置为 100）。

- static int MapPanXKey(int wid)
  - 地图漫游平移 X（像素）。

- static int MapPanYKey(int wid)
  - 地图漫游平移 Y（像素）。

- static int MapSelKey(int wid)
  - 地图单选（selectedMode ""/"single"）选中区域下标（-1 = 无）。

- static int MapRegionSelKey(int wid, int region)
  - selectedMode="multiple"：按区域持久化选中位（8500000 段，
    wid*2048 容区域数，与上方各段无重叠）。

- static int MapDragKey(int wid)
  - 地图拖拽进行中标志（1 = 按下未释放；释放帧清零）。

- static int MapDragXKey(int wid)
  - 地图拖拽中最近一次指针 X。

- static int MapDragYKey(int wid)
  - 地图拖拽中最近一次指针 Y。

- static int MapDragPanXKey(int wid)
  - 地图拖拽按下瞬间的平移 X 快照。

- static int MapDragPanYKey(int wid)
  - 地图拖拽按下瞬间的平移 Y 快照。

- static int TbHitKey(int wid, int k)
  - 工具箱第 k 个按钮的命中 id（k 为按钮在当排中的序号）。

- static int ConnectGroupKey(int wid)
  - 组登记键：同组第一张到达 Resolve 的图把自己的 wid（组长）
    写进这里，其余图读它得到共享键基址；读到 0 = 尚未登记。

- static int ConnectHoverKey(int wid)
  - connect 组共享的「悬停类别下标」状态键（读写都落在组长
    wid 上）：组内图指针在绘图区内时写入自己的类别下标，
    其余图同帧读它对齐十字线；组长登记时初始化为 -1（无悬停）。

- static int ConnectHoverGenKey(int wid)
  - connect 组键段槽 2（8600000 + wid*16 + 2），当前仓库内无读写方。

- static int ZoomI0(App app, ChartOption o, int wid, int n)
  - 将缩放窗口（千分值）解析为包含端点的分类索引范围 [i0,i1]。
    首次调用时从 ChartOption.zoomStart/zoomEnd 初始化状态。

- static int ZoomI1(App app, ChartOption o, int wid, int n)
  - 窗口末端索引（与 ZoomI0 成对）。

- static List<string> WindowLabels(List<string> labels, int i0, int i1)
  - 将标签窗口化为包含端点的索引范围 [i0,i1]（仅字符串
    拷贝；渲染器对系列值也按同一 [i0,i1] 直接读原系列，
    避免有损的系列克隆丢失 itemStyle/marks 等字段）。

- static int CategoryIndexOf(List<string> cats, string name)
  - 类目名精确匹配的首个下标；未命中 -1（dataZoom
    startValue/endValue 的类目定位用）。

- static void DrawZoomBar(App app, int plotX, int plotW, int barY, int barH, int wid, int n)
  - 绘制 dataZoom 范围滑块并处理手柄拖拽。两个手柄设定
    窗口边界（千分值 0..1000）；拖动选中的带可平移。
    窗口状态以 wid 为键持久化在 App 状态映射中。

- static int LegendStartY(App app, int y, int proposed)
  - 右侧竖排图例的起始 y：工具箱占着标题行时下移，避免挡住色块。

- static List<int> LegendPrimIdx(List<ChartSeries> series)
  - 图例占用的行数：有工具箱时整排下移到标题行之下（至少 1 行）；
    否则与标题同行，仅统计放不下而换出的行。
    图例项 = 唯一系列名（ECharts2 图例按名字去重：bar9 同名的
    可见段与透明孔段共用一个图例项）。返回每个名字首个系列
    的下标；DrawPanelI 与 LegendRowCount 必须同用本函数，
    两边的行高/换行才能对齐。

- static int LegendRowCount(App app, int x, int w, string title, List<ChartSeries> series)

- static int PanelContentTop(App app, int x, int y, int w, string title, List<ChartSeries> series, bool showLegend)
  - 面板内容区顶部 y：标题/工具箱行 + 图例行 + 间隙。
    DrawPanelI 与 PanelTopI 共用，悬停层才能与主体对齐。

- static int DrawPanelI(App app, int x, int y, int w, int h, string title, List<ChartSeries> series, int wid, bool showLegend)
  - 面板 + 交互式图例。wid != 0 时每个色块是一个命中区域：
    点击切换该系列的可见性（以 wid 为键持久化在
    App 状态映射中），解析后的隐藏标志写入帧内系列
    快照，所有下游渲染器都会跳过它。隐藏的系列
    以变暗 + 删除线绘制，以便可以恢复显示。
    showLegend=false 时既绘制也不解析隐藏状态——
    图例关闭时系列恒为可见，避免状态残留让图无声消失。
    返回内容区顶部 y。悬停覆盖层请用 PanelTopI。

- static bool LegendClick(App app, int wid, List<ChartSeries> series, int si, bool hid, int mode)
  - legend 色块点击（单一实现供两个布局分支复用）：写隐藏态，
    single 模式下「显示一个」同时隐藏其余系列。返回点击后的 hid。
    触发 LegendSelected 交互事件。

- static int PanelTopI(App app, int x, int y, int w, string title, List<ChartSeries> series, bool showLegend)
  - 只算不画：与 DrawPanelI 完全一致的面板内容顶部
    （标题行高 + 图例换行占位，换行算法逐行镜像）。
    悬停覆盖层用它与主体帧对齐——覆盖层绝不能调
    DrawPanelI / PanelHead，它们会重绘面板背景盖住图形。

- static void DrawMarkArea(App app, ChartFrame f, ChartOption o)
  - 左轴上的阴影 markArea 带 [markLo, markHi]（绘制在
    系列之下）。两个边界未全部设置时为空操作。

- static int DRangeEff(App app, ChartOption o, int wid, int dMin, int dMax, bool upper)
  - 生效筛选窗口的单边边界：固定 dataRangeLo/Hi 优先（Auto →
    dMin/dMax）；calculable 时再取滑条状态位（q 0..1000，默认
    不裁剪）线性映射后与固定值取更收紧的一侧。upper=false 取下界。

- static bool DRangeBandOk(App app, ChartOption o, int wid, int v)
  - 值 v 是否落在 splitList 的某个「未点掉」分段里（无列表 = 放行）。

- static bool DRangeOk(App app, ChartOption o, int wid, int dMin, int dMax, int v)
  - 统一消费 seam：值 v 是否通过当前 dataRange 过滤
    （滑条窗口 + splitList 分段可见性）。dataRangeShow=false 时放行。

- static void DrawMarkLine(App app, ChartFrame f, ChartOption o)
  - 左轴 markLine 处的水平阈值线（虚线），带可选的
    右对齐标签（绘制在系列之上）。markLine 未设置时为空操作。

- static ChartFrame DrawFrame(App app, int x, int y, int w, int h, int plotTop, List<string> labels, int maxV)
  - 带数值网格线（左）+ 分类标签（底部）的直角坐标系框架。
    轴范围 [0, maxV]。需要双轴/固定范围/时间轴时用 BuildAxes。

- static ChartFrame DrawFrameT(App app, int x, int y, int w, int h, int plotTop, List<string> labels, int maxV, int ticks)
  - 同 DrawFrame，但刻度数显式给定（ECharts nice 步长的
    刻度数可不同于 5，如 0..1400 每 200 = 7 格）。

- static ChartFrame DrawFrameLoHi(App app, int x, int y, int w, int h, int plotTop, List<string> labels, int lo, int hi)
  - 在显式数值范围 [lo, hi] 上的直角坐标系框架（支持非零
    基线/负数），用于蜡烛图、箱线图和误差图。

- static ChartFrame DrawFrameLoHiT(App app, int x, int y, int w, int h, int plotTop, List<string> labels, int lo, int hi, int ticks)
  - 同 DrawFrameLoHi，但 y 刻度数显式给定（smartSteps 包络的
    步长数可为 4..7，如 2200..2450 每 50 = 5 格）。

- static int PointV(int v, int g)
  - 点坐标定点值除回真实值（points 存 值×pointG，g<=1 原值跳过）：
    四舍五入、负值对称。散点/值对折线的渲染映射、量程、命中与
    tooltip 统一走这里（ECharts 小数坐标在 int 管线的承载约定，
    与折线 value 的 g/1000 同构）。

- static string PointText(int v, int g)
  - 点坐标定点值的提示文本：g<=1 直接整数；g>1 按 g 的十进制
    位数输出定点小数（1000 → 3 位，-1500/1000 → "-1.5"），
    tooltip/状态栏展示与 PointV 的除回约定配套。

- static ChartSpan ScatterAutoRange(int lo, int hi)
  - 散点双 value 轴缺省 scale:true 的紧致 nice 量程：不强制含 0，
    数据域两端对齐到 nice 步长（NiceRange 的零锚定对身高体重这
    类有自然域的散点会把云挤进角落，ECharts2 原版贴数据包络）。
    步长候选同 echarts2 smartSteps：1/2/2.5/5 × 10^k，splitNumber
    （5）只是预估——实际分段数取包络/步长。

- static int NiceStepUp(int v)
  - ≥ v 的最小 1/2/2.5/5 × 10^k（echarts2 nice 步长候选）。

- static int AxisMaxFor(List<ChartSeries> series, int axisIndex)
  - 绑定到给定数值轴的（可见）系列中的最大值。

- static int AxisMaxForF(List<ChartSeries> series, int axisIndex)
  - AxisMaxFor 的 1/1000 定点对偶：小数系列按 Number（未取整）
    比较，整数按 Value×1000。ECharts extent 语义：原始数据上界
    直传（不许钳零），锚定/取整全部由 NiceRange（smartSteps）
    承担——见 valueAxis._calculateValue/_reformValue。

- static bool SeriesFracAny(List<ChartSeries> series, int axisIndex)
  - 绑定到给定轴的可见系列是否存在小数数据（numberSet 且值
    非整数）。小数轴渲染/量程/提示共用的判定开关。

- static int AxisMinFor(List<ChartSeries> series, int axisIndex)
  - 绑定到给定数值轴的（可见）系列中的最小值
    （无负数时为 0），使轴天然覆盖负数。

- static int XMinFor(List<ChartSeries> series, bool fromValues)
  - X 数值轴最小值：值对系列取 points.x，轴互换系列取 values
    （gap 项不计）；固定覆盖在调用方处理。

- static int XMaxFor(List<ChartSeries> series, bool fromValues)
  - X 数值轴最大值（XMinFor 的对偶）。

- static int FormatterExtraW(string fmt, int v, int fs)
  - 格式化标签比裸数值多占的宽度（axisLabel.formatter 模板，
    如 "{value} °C"），供轴栏预留。

- static bool AnyOnAxis(List<ChartSeries> series, int axisIndex)
  - 是否存在绑定 axisIndex 轴的可见系列。

- static int NiceMin(int v)
  - 将原始最小值向下取整为友好的负轴下界（-2/-5/-10 * 10^n）；
    没有负数需要覆盖时返回 0。

- static int AxisLo(int fixedLo, int dataMin)
  - 从数据 + 固定覆盖解析数值轴的 [lo, hi] 范围（fixedLo/fixedHi
    取 ChartOption.Auto() 时从数据推导）。有负值时下界自动扩展
    到 0 以下。

- static int AxisHi(int fixedHi, int dataMax, int lo)
  - 数值轴上界：固定覆盖优先，否则 NiceMax；保证 hi > lo。
    数据全为非正（dataMax <= 0 且有负值）时上界归 0——雨量图
    这类全负系列的上界不该被 NiceMax(0)=5 顶出一段空白。

- static string Commas(int v)
  - ECharts 2.x 数值默认千分位（axisLabel 的 {value}、tooltip 数值
    都过 addCommas）：3000 → "3,000"，负号不占分组位。

- static string FracText(int v)
  - 1/1000 定点 → 小数文本：fr 为 0 时输出整数（500000 → "500"、
    -1000 → "-1"），否则两位小数去尾零（500 → "0.5"、860 →
    "0.86"）。折线小数值（line6 流量 0.86..1.5）在 int 渲染
    管线的承载约定：值 ×1000 存整型，展示前经此除回。

- static string SeriesNumText(ChartSeries s, int i)
  - 系列第 i 项的展示文本：小数系列（numberSet 且非整数）输出
    两位小数（ECharts2 数值默认 ×1000 定点），整数系列仍是
    千分位整数——与轴刻度、tooltip 的展示约定一致。

- static int TickLabelW(int lo, int hi, int ticks, int fs)
  - [lo, hi] 范围分成 `ticks` 步时最宽的刻度标签（像素），
    用于预留左/右轴 gut 宽度。

- static int TickLabelWF(int loF, int hiF, int ticks, int fs)
  - TickLabelW 的 ×1000 定点对偶：小数轴刻度文本（FracText）
    的最宽像素。

- static ChartFrame BuildAxes(App app, int x, int y, int w, int h, int plotTop, List<string> labels, ChartOption o, List<ChartSeries> series)
  - 完整直角坐标系：左（+ 可选右）数值轴，友好刻度 / 固定边界 /
    翻转 / 对数 / 时间 X 轴、分类标签防重叠、网格内边距覆盖和轴
    标题。返回携带两个轴范围的 ChartFrame，所有渲染器通过
    f.YOf(v, axisIndex) 映射数值。

- static ChartFrame BuildAxesR(App app, int x, int y, int w, int h, int plotTop, List<string> labels, ChartOption o, List<ChartSeries> series, int leftDataMax, int rightDataMax)
  - 同 BuildAxes，但左/右轴使用显式数据最大值
    （-1 = 从系列逐点推导）；堆叠图传入堆叠总和。


## ChartAreaStyle (class)

面积填充样式（颜色 + 填充类型字符串）。

- int color;

- string type;

- int alpha;

- List<int> gradStops;

- static ChartAreaStyle Create()
  - 构造默认样式：颜色 0（跟随系列色）、type "default"。


## ChartAxis (class)

一个坐标轴（ECharts xAxis/yAxis 条目）。分类轴携带其
标签；数值轴携带可选固定范围（ChartOption.Auto()
从数据推导）和刻度数。

- ChartAxisType type;

- string title;

- int min;

- int max;

- bool reversed;

- int ticks;

- bool showGrid;

- bool splitArea;

- int labelRotate;

- int labelInterval;

- string nameLocation;

- string labelFormatter;

- bool labelNegate;

- bool boundaryGap;

- int axisLineColor;

- bool show;

- string position;

- string axisId;

- List<string> categories;

- static ChartAxis Category(List<string> cats)
  - 分类轴工厂：携带标签列表，无网格线，标签自动防重叠。

- static ChartAxis CategoryTitled(List<string> cats, string title)
  - 分类轴工厂（带轴名称）。

- static ChartAxis Value()
  - 数值轴工厂：范围自动推导、显示网格线。ticks 0 = 自动
    （ECharts splitNumber 缺省，刻度数由量程算法给出；消费方
    一律 <1 回落 5），显式 splitNumber 才赋 ticks。

- static ChartAxis ValueRange(int min, int max)
  - 数值轴工厂（固定范围 [min,max]）。

- static ChartAxis ValueTitled(string title)
  - 数值轴工厂（带轴名称）。

- static ChartAxis Time()
  - 时间轴工厂（type = Time，其余同数值轴）。

- static ChartAxis Log()
  - 对数轴工厂（type = Log，其余同数值轴）。

- static ChartAxis LogTitled(string title)
  - 对数轴工厂（带轴名称）。

- static ChartAxis Clone(ChartAxis src)
  - 深复制（含分类标签列表）；src 为 null 时返回 null。


## ChartBig (class)

虚拟 ChartSource 的高性能渲染器。每个系列被缩减为
最多约绘图区宽度列的 min/max 包络，缓存在 ChartState 中，
仅在数据版本或宽度变化时重建——
数百万点的折线/面积图每帧只需 O(width) 而非 O(points)，
图表从不持有每点一个对象的数组。用法：

ChartState st = new ChartState();          // 创建一次，由调用方保存
ChartBig.Render(app, st, mySource, ChartOption.Create(), x, y, w, h, "CPU");

- static int AnimationKey(int key)
  - 显式动画键映射到 5300000 段；key < 1 返回 0（无动画键）。

- static bool NeedsRebuild(ChartState st, ChartSource src, int w)
  - 缓存过期判定：数据版本、控件宽度或系列数任一变化即需重建。

- static void Build(ChartState st, ChartSource src, int target)
  - 将每个系列抽取为约 `target` 个 min/max 列。只追加的构建
    （不做索引写入）——任何优化级别下都安全快速；
    每次数据/尺寸变化运行一次，复杂度 O(总点数)。

- static int DrawHead(App app, int x, int y, int w, int h, string title, ChartSource src)
  - 画面板底、标题与右上角逐系列图例（名称 + 色块，自右向左
    排列；系列色缺省取调色板），返回内容区顶部 y。

- static void Render(App app, ChartState st, ChartSource src, ChartOption o, int x, int y, int w, int h, string title)
  - 将源数据作为抽取后的折线/面积图绘制到给定矩形中。


## ChartController (class)

ChartOption 的可变持有者。用于立即模式 GUI 中的动态数据：
控件可以每帧重新绑定同一个 controller，而不需要重建 ChartView。
数据 API（SetData/AppendData/ClearData）只改系列数据；
SetOption 整体替换并重置 Restore 基线；ShowLoading/SetEmptyMessage
等只切状态字。每次变更递增 Version 并抛 DataChanged。

- ChartOption option;

- ChartOption initialOption;

- int version;

- string status;

- string statusMessage;

- bool disposed;

- ChartEventHub eventHub;

- static ChartController Of(ChartOption option)
  - 构造 controller。option 为 null 时用空 ChartOption 兜底；
    initialOption 快照作为 Restore() 的基线。

- ChartOption Option()
  - 当前 option（内部引用，勿改写——改数据走 SetData/AppendData，
    整体替换走 SetOption）。

- ChartOption GetOption()
  - 返回当前 option 的深复制，调用方不能通过返回值改写 controller。

- int Version()
  - 每次 mutation（SetOption/SetData/Append/Clear/Restore/状态切换）
    递增；视图按版本号判断是否需要重绘。

- string Status()
  - 状态字："ready" / "loading" / "empty" / "error" / "disposed"。

- string StatusMessage()
  - 状态附带的消息（ShowLoading/SetEmptyMessage/SetErrorMessage 传入）。

- bool IsDisposed()
  - controller 是否已 Dispose（disposed 后所有 mutation 与
    事件注册均为 no-op）。

- ChartController On(ChartEventType type, ChartInteractionHandler handler)
  - 注册交互事件处理器（返回 this 便于链式）； disposed 后为 no-op。

- ChartController Off(ChartEventType type, ChartInteractionHandler handler)
  - 注销一个已注册的处理器（按引用匹配，移除最近一个匹配项）。

- ChartController ClearEvents()
  - 注销全部事件处理器；disposed 后为 no-op。返回 this 便于链式。

- bool HasEvent(ChartEventType type)
  - 查询某事件类型当前是否还有订阅（disposed 后恒 false）。

- void RaiseEvent(ChartInteractionEvent eventArgs)
  - 手动触发一个事件（一般由视图在交互时调用）。

- void RaiseType(ChartEventType type)
  - 触发只带类型的轻量事件（chartWid=0，其余字段为默认载荷）。

- ChartController OnClick(ChartInteractionHandler handler)
  - 便捷封装：按事件类型注册（OnClick/OnHover/OnDataZoom/OnRestore
    等一族，语义同 On(type, handler)）。

- ChartController OnDoubleClick(ChartInteractionHandler handler)
  - 注册 DoubleClick 交互事件：双击时派发。

- ChartController OnHover(ChartInteractionHandler handler)
  - 注册 Hover 交互事件：指针悬停时派发。

- ChartController OnMouseOut(ChartInteractionHandler handler)
  - 注册 MouseOut 交互事件：指针移出命中元素时派发。

- ChartController OnLegendSelected(ChartInteractionHandler handler)
  - 注册 LegendSelected 交互事件：图例项被选中。

- ChartController OnPieSelected(ChartInteractionHandler handler)
  - 注册 PieSelected 交互事件：饼图扇区被选中。

- ChartController OnMapSelected(ChartInteractionHandler handler)
  - 注册 MapSelected 交互事件：地图区域被选中。

- ChartController OnMapRoam(ChartInteractionHandler handler)
  - 注册 MapRoam 交互事件：地图漫游（平移/缩放）。

- ChartController OnTimelineChanged(ChartInteractionHandler handler)
  - 注册 TimelineChanged 交互事件：时间轴播放位置切换。

- ChartController OnMagicTypeChanged(ChartInteractionHandler handler)
  - 注册 MagicTypeChanged 交互事件：magic type 切换。

- ChartController OnRefresh(ChartInteractionHandler handler)
  - 注册 Refresh 交互事件。

- ChartController OnForceLayoutEnd(ChartInteractionHandler handler)
  - 注册 ForceLayoutEnd 交互事件：力导向布局收敛结束。

- ChartController OnDataZoom(ChartInteractionHandler handler)
  - 注册 DataZoom 交互事件：缩放区间变化。

- ChartController OnDataRange(ChartInteractionHandler handler)
  - 注册 DataRange 交互事件：数据区间选择变化。

- ChartController OnRestore(ChartInteractionHandler handler)
  - 注册 Restore 交互事件：还原初始 option 时派发。

- ChartController OnDataChanged(ChartInteractionHandler handler)
  - 注册 DataChanged 交互事件：option/数据版本变化时派发。

- ChartController SetOption(ChartOption next)
  - 替换整个 option，保留 controller 身份与图表交互键；显式
    SetOption 同时成为 Restore() 的新基线。

- ChartController SetData(int seriesIndex, List<ChartData> data)
  - 替换一个系列的数据项。data 为 null 表示清空该系列。
    系列下标越界时静默返回。

- ChartController AppendData(int seriesIndex, List<ChartData> data)
  - 追加已命名/着色的数据项，适合实时折线和滚动窗口。
    data 为 null 时 no-op（SetData 的 null 才表示清空）。

- ChartController AppendValues(int seriesIndex, List<int> values)
  - 追加纯数值数据的快捷形式（等价 AppendData + ChartData.Of）。

- ChartController ClearData(int seriesIndex)
  - 清空一个系列的数据，保留系列名称、类型、样式和轴绑定。
    状态切为 "empty"。

- ChartController Clear()
  - 清空所有系列的数据，保留 option 的图表类型、样式和轴配置。

- ChartController Restore()
  - 恢复到最近一次 SetOption/Of 的 option 快照。数据类的改动
    （SetData/Append）不在快照基线内，会被一并丢弃。

- ChartController ShowLoading(string message)
  - 显示加载中状态（视图层据此画 loading 遮罩），message 可为空串。

- ChartController HideLoading()
  - 回到 ready 状态，清除 loading/error/empty 的消息。

- ChartController SetEmptyMessage(string message)
  - 设为空数据状态并自定义提示文案。

- ChartController SetErrorMessage(string message)
  - 设为错误状态并自定义错误文案（不抛异常，由视图层渲染）。

- void Dispose()
  - 释放 controller 的 option 和快照；后续 mutation 变为 no-op。


## ChartData (class)

一个数据点（ECharts series.data[i]）：一个值加可选名称
（扇区/分类标签）和颜色。颜色 0 表示"继承系列
颜色"——这是 ECharts 三级控制的第三级
（option < series < data item）。

- int val;

- double number;

- bool numberSet;

- string name;

- int color;

- bool hidden;

- bool selected;

- int size;

- bool sizeSet;

- bool gap;

- string symbol;

- string labelText;

- int labelSide;

- bool labelHide;

- bool hasCat;

- int cat;

- ChartItemStyle itemStyle;

- static ChartData Of(int v)
  - 以整数值构造数据点（名称空、继承系列色、不隐藏、无逐项尺寸）。

- static ChartData Gap()
  - ECharts data 项 '-'：该类目缺数据，折线在此断开。

- static ChartData Numeric(double v)
  - 以 double 值构造数据点；整数字段 val 同步取截断值。

- static ChartData NamedNumber(double v, string name)
  - 带 double 值与名称（扇区/分类标签）的数据点。

- static ChartData Named(int v, string name)
  - 带整数值与名称的数据点。

- static ChartData Colored(int v, int color)
  - 带整数值与显式颜色的数据点。

- static ChartData Full(int v, string name, int color)
  - 同时带值、名称与颜色的数据点。

- static ChartData Clone(ChartData src)
  - 深复制；src 为 null 时返回 null。


## ChartDataset (class)

ECharts 风格共享数据源：命名维度按列存储，外加
可选的 x 轴分类标签。一个数据集可通过
EncodeBy / EncodeNamed 选择不同维度来驱动多个图表——
调用方从不复制或重构底层列表。

- List<ChartDimension> dimensions;

- List<string> cats;

- static ChartDataset Of(List<ChartDimension> dimensions)
  - 构造数据集（cats 初始为空，用 Labels() 的 1..N 兜底）。

- static ChartDataset WithCats(List<ChartDimension> dimensions, List<string> cats)
  - 构造数据集并附带显式 x 轴分类标签。

- int RowCount()
  - 行数 = 第一维度的值数；无维度时为 0。

- int DimOf(string name)
  - 按名称查找维度的索引，不存在返回 -1。

- List<string> Labels()
  - x 轴分类标签：给定 `cats` 时用显式值，否则
    用字符串形式的 1..RowCount。

- ChartOption EncodeBy(string title, List<int> yDims, ChartType type)
  - 从一组数值维度（按索引）构建 ChartOption。
    系列名取自维度名；颜色从主题自动解析。

- ChartOption EncodeNamed(string title, List<string> yNames, ChartType type)
  - 同 EncodeBy，但按名称选择维度。


## ChartDimension (class)

一个命名、按列存储的数据集维度。

- string name;

- List<int> values;

- static ChartDimension Of(string name, List<int> values)
  - 构造一个维度（直接持有 values 列表，不复制）。


## ChartEvent (class)

Event River 的一个事件：名称、时间区间 [start, end]、值
（驱动带宽）、可选颜色。普通标量 data 兼容转换为等距事件。

- string name;

- int start;

- int end;

- int value;

- int color;

- static ChartEvent Of(string name, int start, int end, int value)
  - 构造一个事件；color 为 0 表示继承系列颜色。

- static ChartEvent Clone(ChartEvent src)
  - 深复制；src 为 null 时返回 null。


## ChartEventHub (class)

按类型分发带载荷图表事件的保留式多播表。由 ChartController
持有；Off/Clear 在派发过程中调用是安全的（派发基于快照）。

- List<ChartEventSubscription> subscriptions;

- ChartEventHub()
  - 构造空的多播表。

- void On(ChartEventType type, ChartInteractionHandler handler)
  - 注册处理器（不查重——同一处理器注册两次会收到两次回调）。

- void Off(ChartEventType type, ChartInteractionHandler handler)
  - 注销最近一个 type 与 handler 都匹配的订阅；无匹配时
    静默返回。

- int Count(ChartEventType type)
  - 某类型当前订阅的处理器数量（HasEvent 用）。

- void Clear()
  - 清空全部订阅（整体换新列表；正在派发的快照不受影响）。

- void Raise(ChartInteractionEvent eventArgs)
  - 派发事件给所有匹配类型的处理器。取订阅快照遍历，
    处理器在回调中 Off/Clear 不影响本次派发。


## ChartEventSubscription (class)

一条订阅记录：事件类型与处理器的配对（仅 ChartEventHub 内部使用）。

- ChartEventType type;

- ChartInteractionHandler handler;

- ChartEventSubscription(ChartEventType type, ChartInteractionHandler handler)
  - 构造一条订阅。


## ChartFrame (class)

纯 Zan 图表库 —— ECharts 2.2.x 的声明性子集，全部用
stdlib 组件与确定性的整数几何绘制，无 JS / DOM / WebView：
· 17 种原生 series.type：line / bar / pie / scatter / k /
radar / chord / force / map / gauge / funnel / eventRiver /
treemap / tree / wordCloud / heatmap，外加 custom kind
（sankey / box / error / waterfall / sunburst / radialBars /
venn）。
· 轴：category / value / time（整数天数，表格驱动日期）/
log（仅正值、10 的幂刻度），独立左右轴 min/max/reversed。
· 交互：hover tooltip、图例切换可见性、dataZoom 窗口、
markLine / markPoint / markArea、emphasis（hover）paint。
· 确定性：无随机数、无系统时钟；布局/命中/指纹均为整数运算，
conformance 测试可逐值断言。
Zan 扩展（超出 ECharts 2.2.x 的便捷 API）：ChartOption.Of /
OfRings、ChartSeries.Line / Bar / Area / OfRegions / OfEvents /
OfBoxes / OfErrors / OfPoints、pieRings 嵌套环、eventRiver 由
数值系列驱动（按类别索引映射时间）、图表数据用 List<int> /
ChartData 直接表达。
渲染由 ChartView（partial）分发到每类一个渲染器；所有绘制走
ChartOption -> ResolvedChart -> Canvas 管道。

内部持有者：计算出的绘图矩形加上解析后的数值轴
范围（左轴 + 可选右轴），使每个渲染器以相同方式
映射数值 -> 像素。leftMin/leftMax 始终有效；rightMin/rightMax 仅在有右轴时有效。
leftLog/rightLog 为对数轴（仅正值）；isTime 为时间 X 轴
（整数天数，标签由 Chart.TimeLabel 生成）。

- int plotX;

- int plotY;

- int plotW;

- int plotH;

- int leftMin;

- int leftMax;

- int leftMinF;

- int leftMaxF;

- int rightMin;

- int rightMax;

- int rightMinF;

- int rightMaxF;

- bool hasRight;

- bool reversed;

- bool rightReversed;

- bool leftLog;

- bool rightLog;

- bool isTime;

- int timeMin;

- int timeMax;

- bool catBoundaryGap;

- bool catY;

- int xLo;

- int xHi;

- bool leftNegate;

- bool rightNegate;

- int CatLeft(int i, int n)
  - 第 i 类目左缘。用 i*W/n 而不是固定 step，余数摊到末格，
    最后一根柱/最后一个标签贴上绘图区右缘。boundaryGap=false
    （线落在刻度上）时槽位退化为刻度点：第 i 点 = i*W/(n-1)。

- int CatWidth(int i, int n)
  - 第 i 类目的宽度（相邻左缘之差，余数摊在末格）。

- int CatMid(int i, int n)
  - 第 i 类目的水平中线。

- int CatX(int i, int n)
  - 第 i 类目上「数据点」的 x：boundaryGap=true（带状，柱/K 线
    默认）落格子中线；false（刻度线模式，ECharts 折线/散点的
    默认轴形态）落刻度本身——首点贴 y 轴、末点贴绘图区右缘。
    折线/散点/十字线/悬浮提示等点几何一律走这里；柱/K 线继续
    用带状 CatLeft/CatMid。

- int CatIndexAt(int px, int n)
  - 局部类目窗口内的像素 -> 类目索引反解；返回值与
    CatLeft/CatMid 使用同一整数分桶规则。

- int YOf(int v, int axisIndex)
  - 左轴（axisIndex 0）或右轴（1）上数值对应的像素 Y，
    遵循各轴预设的翻转标志。

- int YOfFx(int v, int axisIndex)
  - YOf 的 16.8 定点版本（1/256 px）：堆叠面积带的填充边界走
    亚像素光栅化（FillBandFx），整数 YOf 会把边界量化到整行，
    缓坡上每列硬跳 1 行——正是"面积边缘锯齿"的来源。

- int YOfF(int vF, int axisIndex)
  - 小数轴的 Y 映射：v 为 值×1000 定点，leftMinF/leftMaxF（或右轴
    rightMinF/rightMaxF）是 ×1000 的轴界（line6 流量 0.86..1.5、
    降雨量 -0.005..-0.955 这类数据在 int Value() 四舍五入后全折成
    1..2 / 0..-1，画成平线）。轴不是小数轴时按整数轴界做定点
    映射：vF=值×1000 对 [lo×1000, hi×1000] 比例映射，整数数据
    （vF 恰为 1000 的倍数）与 YOf 逐像素一致，小数数据不再被
    vF/1000 截断丢掉小数位。

- int YOfFL(long vF, int axisIndex)
  - YOfF 的 long 版：亿级整值（candlestick-touch 成交量
    8.6e7、成交额）×1000 定点后 8.6e10 必爆 int32，调用方
    以 long 承载定点值走这里；映射体与 YOfF 同式。

- int ZeroBase(int axisIndex)
  - 系列所在轴的零线像素（ECharts 面积/柱的填充基线）：
    0 在该轴范围内时返回其映射（钳制进绘图区），否则返回
    绘图区底——与 ECharts「0 不在范围内时填到对侧边缘」一致。

- int CatMidY(int i, int n)
  - Y 类目轴第 i 槽的垂直中线（轴互换折线的点行）。

- int XOfValue(int v)
  - X 数值轴上数值 v 的像素（轴互换折线 / 值对折线）。

- int YOfLog(int v, int axisIndex)
  - 对数 Y 映射：仅正值（v < 1 钳制到 1），log10 线性化后
    按轴范围映射。低于/高于范围钳制在绘图区内。

- int ValueAtY(int py, int axisIndex)
  - 线性/对数 Y 的像素 -> 值域反解。对数轴与当前
    floor-log10 前向映射保持一致，返回所在十进制段的下界。

- int XOfTime(int t)
  - 时间 X 映射：整数时间值 → 像素 x，钳制在绘图区内。
    时间跨度（秒/毫秒）× plotW 轻易超 int32，乘法走 long。

- string ValueTextAtY(int py, int axisIndex)
  - 像素 Y → 数值文本（左/右轴，follows negate 标志）。轴是
    小数轴（leftMinF/rightMinF 生效）时按 1/1000 定点输出小数，
    整数轴与原 Commas 行为一致。


## ChartGeo (class)

ECharts geo 组件：一张底图地图 + 按名区域覆盖。解析后由
FromJsonValue 的合成块折算成 isGeoBase 的 type=Map 载体系列
（几何经 ChartMaps.BindSeries 注入）。

- string map;

- bool roam;

- bool labelShow;

- string selectedMode;

- int areaColor;

- int borderColor;

- List<ChartMapRegion> regions;

- static ChartGeo Of()

- static ChartGeo Clone(ChartGeo src)


## ChartGeoJson (class)

GeoJSON → ChartMapRegion 的运行时解析入口：地图几何以数据文件
随程序携带（echarts registerMap 的 china.json 等，构建时 --embed
烤进 exe 或从盘读取），不再生成代码硬编码。吃两种形态：
① 明文 GeoJSON（FeatureCollection / Feature，Polygon 与
MultiPolygon，coordinates 为度）；
② echarts 官方地图 JSON 的 UTF8Encoding 压缩形态——环是
delta+zigzag 编码串、逐环给 encodeOffsets 起点，解码算法与
echarts parseGeoJson.js 一致（UTF8Scale 默认 1024）。
坐标统一量化到 0.01° 整数并翻成屏幕系（y = -纬度×100，北朝上），
与 ChartMapPoint/ChartViewMap 的数据约定一致。每个 Feature 聚成
一个区域：MultiPolygon 的各部件都是外环，部件内第 2 条起的环按
GeoJSON 约定记洞。properties.value 存在时作区域值，否则 0，由
调用方按业务赋值。

- static List<ChartMapRegion> ParseText(string json)
  - 解析 GeoJSON 文本；结构不对或没有可渲染要素时返回空表。

- static List<ChartMapRegion> Parse(JsonValue v)
  - 遍历 FeatureCollection / 单个 Feature，按顶层 UTF8Encoding /
    UTF8Scale 字段判定编码形态，逐 Feature 聚成区域。

- static void Feature(JsonValue f, bool encoded, int scale, List<ChartMapRegion> into)
  - 一个 Feature → 一个区域；geometry 缺失、类型未知或没有可用环
    时跳过（Output of mapshaper may have geometry null）。

- static void Polygon(JsonValue rings, JsonValue offs, bool encoded, int scale, List<ChartMapRing> into)
  - 一个部件的环组。encoded 时环是编码串（混入的明文数组环也认），
    offs 逐环给 [ox, oy] 起点；明文时环是 [[lng,lat],...]。

- static List<ChartMapPoint> DecodeRing(string s, int ox, int oy, int scale)
  - echarts UTF8Encoding 环解码：码点-64 → zigzag → 累加成
    1/scale 度的整数，再量化到 0.01°。

- static int Zig(int c)
  - echarts zigzag：delta 编码（码点-64）还原成有符号数。

- static void PushPoint(List<ChartMapPoint> pts, int x, int y)
  - 0.01° 粒度下编码串常产生与上一点重合的量化点，直接丢掉，
    免得留 <3 点的退化环和零长边。

- static int QuantDeg(double d)
  - 度 → 0.01° 整数，半值远离零。

- static int QuantScaled(int v, int scale)
  - echarts 坐标（1/scale 度的整数）→ 0.01° 整数，半值远离零。

- static List<int> CodePoints(string s)
  - 编码串按 UTF-8 解成码点序列。echarts 编码以 JS charCodeAt 的
    UTF-16 码元为单位，但其 delta 有界，落在 BMP 内，码点即码元。

- static JsonValue At(JsonValue v, int i)
  - 取数组第 i 项；v 非数组或 i 越界时返回 null。


## ChartGridSpec (class)

grid 数组的一项：矩形四边 inset（百分比或像素），或直接声明
width/height（scatter-matrix 的 15 宫格形态）。多 grid 布局按
series.xAxisIndex 分组入格。

- int lPct;

- int lPx;

- int tPct;

- int tPx;

- int rPct;

- int rPx;

- int bPct;

- int bPx;

- int wPct;

- int wPx;

- int hPct;

- int hPx;

- bool containLabel;

- static ChartGridSpec Of()


## ChartHit (class)

渲染器提供给 ChartView 的当前几何命中。命中身份不包含
像素坐标，指针在同一数据点内移动时不会重复触发 Hover。

- ChartElementType elementType;
  - 指针当前命中的数据图元类型（命中空白区域时为 Chart）。

- int seriesIndex;
  - 命中的系列下标/名称；未命中具体数据时为 -1/空串。

- string seriesName;

- int dataIndex;
  - 命中的数据项下标/名称（饼图为扇区、地图为区域）。

- string dataName;

- int value;
  - 整数值（value 字段未数值化时有效）。

- bool numberValueSet;

- double numberValue;

- bool xValueSet;
  - 命中点的 x/y 数值（直角坐标系中有意义；散点/折线为数据坐标）。

- double xValue;

- bool yValueSet;

- double yValue;

- int pixelX;
  - 命中点的像素坐标（画自定义 tooltip 用）。

- int pixelY;

- int axisIndex;
  - 命中的轴下标（0 = 左/下轴，1 = 右轴）。

- static ChartHit Of(ChartElementType elementType, int seriesIndex, string seriesName, int dataIndex, string dataName, int value, int pixelX, int pixelY)
  - 构造基础命中：图元类型/系列/数据项身份、整数值与像素
    坐标按参数记录；number/x/y 数值字段未置位，axisIndex = 0。

- static bool Same(ChartHit a, ChartHit b)
  - 同一数据点命中判断（类型+系列+数据下标），指针在
    同一点内移动时用于抑制重复 Hover。

- static ChartHit Copy(ChartHit src)
  - 深复制命中（含全部数值扩展字段与轴下标）；src 为 null
    时返回 null。


## ChartHost (class)

保留式图表宿主控件：把立即模式的 ChartView 包进控件树，
设计器生成的窗体与运行期 JSON 装载因此能像普通控件一样
持有图表（此前 Chart 只能被宿主逐帧 Render，生成代码只发
Panel 占位）。

ChartHost ch = new ChartHost();
ch.SetProp("type", "pie");     // ChartKinds 注册表字符串
ch.SetProp("title", "访问来源");

`type` 收 ECharts type 字符串（line/bar/pie/scatter/gauge/
funnel/radar/wordCloud/...）与设计器别名（area/stacked/hbar/
hstacked/donut）；切换或构建时按类型现拼一份示例 option
（SampleOf），宿主接手真数据走 SetOption。依赖结构化数据的
图型（地图/关系图/事件河流图等）示例先以分类图呈现，类型
字符串原样保留，等 SetOption 换真数据。

- ChartView view;

- ChartOption opt;

- string chartType;

- ChartHost()
  - 默认柱状图示例。必须显式构建：Zan 子类不会隐式跑基类
    字段初始化，缺构造的实例 view/opt 全 null。

- override string Kind()

- override string GetProp(string key)
  - 当前图型字符串与标题的文本应答；其余键交基类
    （Props 未声明的键走 GetExtra/样式类 fallback）。

- override void SetProp(string key, string val)

- void SetChartType(string s)
  - 切换图型并重拼示例 option。宿主已用 SetOption 接管数据后
    切型会重置为示例数据——类型与数据一起由 SetOption 定。

- void SetOption(ChartOption o)
  - 整体替换 option（类型、图例、系列全由调用方定）；null
    忽略。ChartView 重建，入场动画重放一次。

- override void OnMeasure(App app)
  - 示例尺寸（自由画布/流式布局都可再覆写宽高）。

- override void OnPaint(App app)

- static ChartOption SampleOf(string type)
  - 按图型字符串现拼示例 option——设计器画布预览与 `type`
    切换共用同一份，保证"设计器所见 = 生成窗体初见"。别名
    （area/stacked/hbar/hstacked/donut）映射到对应系列风格；
    line/bar 之外的注册表类型配各自的示例系列；依赖结构化
    数据的图型先以分类示例呈现（类型串留在 chartType 上，
    真数据由 SetOption 接管）。


## ChartInteractionEvent (class)

图表交互事件的稳定载荷。未适用的字段使用 -1/空串/false，
这样同一 handler 可以按 type 选择需要的 ECharts 风格字段。

- ChartEventType type;

- ChartElementType elementType;

- bool dataHit;

- int chartWid;

- int seriesIndex;

- string seriesName;

- int dataIndex;

- string dataName;

- int value;

- bool numberValueSet;

- double numberValue;

- bool xValueSet;

- double xValue;

- bool yValueSet;

- double yValue;

- int x;

- int y;

- int axisIndex;

- bool selected;

- int zoomStart;

- int zoomEnd;

- static ChartInteractionEvent Of(ChartEventType type, int chartWid)
  - 基础载荷：仅事件类型与图表 wid，其余字段为默认值
    （下标 -1、空串、坐标 0）。

- static ChartInteractionEvent Series(ChartEventType type, int wid, int seriesIndex, string seriesName)
  - 系列级载荷：在基础载荷上补 seriesIndex/seriesName
    （图例开关等针对整条系列的事件用）。

- static ChartInteractionEvent DataPoint(ChartEventType type, int wid, int seriesIndex, string seriesName, int dataIndex, string dataName, ChartElementType elementType)
  - 数据点命中的完整载荷：dataHit=true 且 elementType 指明图元类型。

- static string ElementName(ChartElementType type)
  - 图元类型的稳定字符串名（ECharts 风格小驼峰）；Chart 与
    未列出的值一律返回 "chart"。

- string TypeName()
  - 本事件类型的字符串名（见 TypeNameOf）。

- static string TypeNameOf(ChartEventType type)
  - 事件类型的稳定字符串名（ECharts 风格小驼峰）；未知值
    返回 "unknown"。


## ChartItemStateStyle (class)

单状态（normal/emphasis）图形样式：填充、描边、圆角与线/面积子样式。

- int color;

- int color0;

- int borderColor;

- int borderWidth;

- List<int> borderRadius;

- ChartLineStyle lineStyle;

- ChartAreaStyle areaStyle;

- static ChartItemStateStyle Create()
  - 构造空样式（颜色 0 = 跟随主题，borderRadius 空表 = 缺省圆角）。


## ChartItemStyle (class)

ECharts itemStyle：normal 与 emphasis 两套状态样式。

- ChartItemStateStyle normal;

- ChartItemStateStyle emphasis;

- static ChartItemStyle Create()
  - 构造 normal/emphasis 均为空样式的项样式。

- static ChartItemStateStyle CloneState(ChartItemStateStyle src)
  - 深复制单个状态（含 borderRadius 列表与线/面积子样式）；
    src 为 null 时返回 null。

- static ChartItemStyle Clone(ChartItemStyle src)
  - 深复制 normal/emphasis 两套状态；src 为 null 时返回 null。


## ChartJsonDataset (class)

ECharts dataset：一个命名数据集。source 保留原始 JSON（首行
约定为表头），rows 是 transform 过滤/排序后的有效行号表。

- string id;

- JsonValue source;

- List<int> rows;

- List<string> dims;

- bool noHdr;

- JsonValue source1;

- List<int> rows1;

- int HdrRows()
  - 表头占的行数：dimensions / 无表头形态为 0，常规 source 形态
    首行按约定是表头，占 1 行。行号换算全走这里。

- static bool HeaderEvidence(JsonValue source)
  - 表头行推断（ECharts sourceHeader:'auto' 的对应物）：行 0 至
    少一列是字符串而同列后续行出现数值 => 行 0 是表头；全数值
    或全列同构（K 线日期列）=> 无表头。样本不足两行按有表头。

- static ChartJsonDataset ById(List<ChartJsonDataset> list, string want)
  - 按 id 查数据集；找不到返回 null。

- static ChartJsonDataset At(List<ChartJsonDataset> list, int index)
  - datasetIndex 旧形式取数据集；越界返回 null。

- int RowCount()
  - 行数（不含表头行）。

- int Width()
  - 数据列数：dimensions 形态取 dims 长度，常规形态取表头行
    宽度（无表头时取首数据行宽度）。

- string Header(int col)
  - 表头列名；越界或无表头返回 ""。第 0 行按约定是表头；
    dimensions 形态直接查 dims。

- int ColumnOf(JsonValue dim)
  - 列名/序号 -> 列下标（encode 的两种形态）。找不到返回 -1。

- JsonValue CellAbs(int absRow, int col)
  - 读单元格（绝对行号，含表头行）；越界返回 null。

- JsonValue Cell(int rowIdx, int col)
  - 读单元格原始 JsonValue；越界返回 null。

- double Num(int r, int c)
  - 数据行 r（0 = 第一条数据行）、列 c 的数值。

- string Text(int r, int c)
  - 数据行 r、列 c 的文本形态。

- static void Transform(ChartJsonDataset from, ChartJsonDataset into, JsonValue tr)
  - 应用 transform（filter / sort / ecStat 回归·聚类；boxplot
    等其余类型暂原样透传源行集）。into 的 source 指向结果数据，
    rows 为有效行号表；dims 随上游继承。

- static bool RowLess(ChartJsonDataset ds, int a, int b, List<JsonValue> cfgs)
  - 排序比较：a 行是否应排在 b 行前（按各 cfg 维度/顺序）。

- static JsonValue SynthRows(string[]header, List <List<double>> rows)
  - 用数值行集合成结果 source（带表头行）。

- static void Boxplot(ChartJsonDataset from, ChartJsonDataset into, JsonValue cfg)
  - echarts boxplot 变换（对照 boxplotTransform.ts）：逐输入行
    一只箱——行内数值升序后取四分位（H=(n−1)p+1 线性插值），
    默认 1.5×IQR 须界（boundIQR:"none" 取极值），结果 0 = 每行
    [ItemName, low, Q1, Q2, Q3, high]，结果 1 = 离群点
    [ItemName, value]（fromTransformResult:1 取）。itemName 取
    行号或 itemNameFormatter 模板（{value} = 行号）。

- static void Aggregate(ChartJsonDataset from, ChartJsonDataset into, JsonValue cfg)
  - ecSimpleTransform:aggregate——按 groupBy 列分组（组序按
    首现顺序），resultDimensions 逐列聚合：method = min/Q1/
    median/Q3/max/sum/average/count，缺 method 为直通（取组内
    首行原值）。输出表头 = 各 resultDimension.name。

- static double Quantile(List<double> asc, double p)
  - 分位数（升序序列，H=(n−1)p+1 线性插值，与 echarts
    quantile 一致）。

- static void TakeSynth(ChartJsonDataset into, JsonValue arr)
  - 合成结果落 into：source 指向新数组，rows 全量、dims 清空。

- static bool ColNumeric(ChartJsonDataset ds, int col)
  - 列是否全为数值单元格（轴型智能推断：全数值 + 类目轴无显式
    data = 该轴实为 value，与 ECharts 行为一致）。

- static int Mul1000(double v)
  - double -> 千倍定点 int（四舍五入，散点/数值点存储形态）。

- static int Rint(double v)
  - double -> 就近 int（箱线五数取整）。

- static int CatIdx1000(ChartAxis a, string text)
  - 类目位置（×1000 定点）：文本在类目轴里查序号；查不到回落
    0（类目列与轴回填同源，正常都命中）。

- static void PieceColorPoints(ChartOption o, ChartSeries cs)
  - piecewise visualMap（pieces 为 value 精确匹配形态）按 point.z
    给散点逐点上色（scatter-clustering 的 cluster 分色）。

- static void Regression(ChartJsonDataset from, ChartJsonDataset into, JsonValue cfg)
  - ecStat:regression——最小二乘拟合。linear/logarithmic/
    exponential 输出定义域两端点（与 ecStat 相同的直线形态），
    polynomial 输出 33 个等距点勾出曲线。

- static void Clustering(ChartJsonDataset from, ChartJsonDataset into, JsonValue cfg)
  - ecStat:clustering——确定性 k-means：k-means++ 初始化
    （固定种子 LCG，截图回归不抖）+ Lloyd 迭代至多 30 轮。
    输出 [x,y,cluster]。

- static List<double> Solve(List <List<double>> A, List<double> b, int k)
  - 列主元高斯消元解 k 元线性方程组；奇异时回落零解。

- static double Pow(double b, int e)
  - 整指数幂（回归正规方程用；负指数回落 0）。

- const double Ln2=0.6931471805599453;

- static double Ln(double v)
  - 自然对数：归一到 [0.5,2] 后 atanh 级数
    ln(x) = 2(t + t³/3 + t⁵/5 + …)，t = (x−1)/(x+1)。

- static double Exp(double v)
  - 指数：归一到 r∈[−ln2/2, ln2/2] 后泰勒展开，再按 2^k 缩放。

- static bool FilterRow(ChartJsonDataset ds, int absRow, JsonValue cfg)
  - 过滤子句：{and:[...]} / {or:[...]} / {dimension, op 值对}。

- static bool CellEq(JsonValue cell, JsonValue want)


## ChartKinds (class)

图表类型字符串与 ChartType 枚举互转，以及 symbol / selectedMode
等字段的词法规范化小工具。

- static ChartType TypeOf(string s)
  - ECharts type 字符串转 ChartType；未知名（含扩展渲染器标签）
    返回 ChartType.Custom。

- static string CustomOf(string s)
  - 非 ECharts 2.2.7 原生类型的扩展渲染器标签（"box"、"error"、
    "sankey"、"waterfall"、"sunburst"、"radialBars"、"venn"、
    "pictorialBar"、"themeRiver"、"parallel"、"lines"）；
    ECharts boxplot 折算为 "box"（同一箱线渲染器）；原生类型为 ""。

- static string TypeName(ChartType t)
  - ChartType 转回 ECharts type 字符串；Custom 返回 "custom"。

- static string SymbolSanitize(string s)
  - ECharts series.symbol 形状族规范化：2.2.x 全部符号形状
    （circle/emptyCircle/rectangle/diamond/triangle/star/star5/
    star6/arrow/droplet/pin/emptypin/heart/emptyHeart）+ "none"
    （该点不画符号，系列级与数据级都合法；渲染器入口统一跳过）。
    未知名返回 ""（渲染器按族默认圆点）。star5 是 star 的
    ECharts2 别名（五角星），归一到 star。

- static string SelectedModeSanitize(string s)
  - ECharts map.selectedMode 白名单："" 与 "single" 同义（单区域）；
    "multiple" 多选；"false" 禁用点击选中。其余回落 ""。

- static bool SelectedModeEnabled(string s)
  - selectedMode seam：是否允许点击选中（"false" 关闭）。

- static string RoamWheelModeSanitize(string s)
  - 地图滚轮策略：zoom（默认消费并缩放）或 pass/none（交给外层滚动容器）。

- static string LegendModeSanitize(string s)
  - legend.selectedMode 白名单："single" | "false" | 其余（含
    "multiple"）归一为 ""（多选 = 现状默认）。

- static ChartAxisType AxisOf(string s)
  - ECharts axis.type 字符串转 ChartAxisType；未知名返回 Category。

- static string AxisName(ChartAxisType t)
  - ChartAxisType 转回 ECharts axis.type 字符串。


## ChartLineStyle (class)

线样式：颜色、线宽、线型（"solid"/"dashed"/"dotted"）与阴影。
color0 为 ECharts 2.x K 线阴线配色对。

- int color;

- int color0;

- int width;

- string type;

- int shadowColor;

- int shadowBlur;

- List<int> gradStops;

- bool transparent;

- int alpha;

- static ChartLineStyle Of(int color, int width)
  - 构造实线样式；type 置 "solid"，阴影关闭。

- static ChartLineStyle Clone(ChartLineStyle src)
  - 深复制；src 为 null 时返回 null。


## ChartLink (class)

Sankey 图的有向流转链接：从节点 -> 到节点，带一个值
（链接粗细）。节点在渲染时从链接推导。

- string from;

- string to;

- int val;

- static ChartLink Of(string from, string to, int val)
  - 构造一条流转链接；val 为链接粗细。

- static ChartLink Clone(ChartLink src)
  - 深复制；src 为 null 时返回 null。


## ChartMapEntry (class)

已注册地图：echarts registerMap 的对应物。regions 是 0.01°
屏幕系几何（GeoJSON 形态，ChartGeoJson.ParseText 解析）或
SVG 用户单位几何（SVG 形态，ChartSvgMap.Scan 惰性扫描）；
svg 非 "" 即 SVG 地图，vx..vh 为其 viewBox（布局源框）。

- string name;

- string svg;

- double vx;

- double vy;

- double vw;

- double vh;

- bool scanned;

- List<ChartMapRegion> regions;

- static ChartMapEntry Of(string name)


## ChartMapPoint (class)

地图多边形的一个顶点（已规范化为整数）。

- int x;

- int y;

- static ChartMapPoint Of(int x, int y)
  - 构造一个地图多边形顶点。


## ChartMapRegion (class)

地图区域：名称、值（驱动连续色域）、可选颜色和多条环
（单环=单部件；多外环=多部件；hole=true 的环减去面积）。

- string name;

- int value;

- int color;

- List<ChartMapRing> rings;

- static ChartMapRegion Of(string name, int value, List<ChartMapRing> rings)
  - 构造地图区域（颜色由 value 映射到连续色域）。

- static ChartMapRegion Colored(string name, int value, int color, List<ChartMapRing> rings)
  - 构造带显式颜色的地图区域（不参与值→色映射）。

- static ChartMapRegion Clone(ChartMapRegion src)
  - 深复制全部环与顶点；src 为 null 时返回 null。


## ChartMapRing (class)

地图区域的一条环：外环勾出区域轮廓，hole=true 的环是其中的洞。
多部件区域用多条外环表达。

- List<ChartMapPoint> points;

- bool hole;

- static ChartMapRing Of(List<ChartMapPoint> points, bool hole)
  - 构造一条环；points 至少 3 个才被 JSON 解析接受。


## ChartMaps (class)

地图注册表：程序启动时把随包携带的地图数据注册进来
（GeoJSON 文本 / Zan 侧区域表 / SVG 源码），map 系列与 geo
组件按名字取几何（ChartMaps.BindSeries 并入数据值与覆盖）。
全仓约定：注册表是进程级的只读几何源，绑定进系列的 regions
是克隆——渲染器对 regions 的任何修改都不回写注册表。

- static List<ChartMapEntry> all;

- static List<ChartMapEntry> Table()
  - 初始化兜底（静态字段不依赖初始化器顺序）。

- static ChartMapEntry Find(string name)
  - 按名查注册表；未注册返回 null。

- static void Register(string name, string geoJsonText)
  - 注册 GeoJSON 地图（明文 GeoJSON 或 echarts UTF8Encoding
    形态，见 ChartGeoJson）。无可渲染要素时不入表。

- static void RegisterRegions(string name, List<ChartMapRegion> regions)
  - 注册 Zan 侧区域表（如 gui_gallery 的 MapChinaData）。表被
    直接持有，调用方注册后不要再改。

- static void RegisterSvg(string name, string svgText)
  - 注册 SVG 地图（echarts registerMap(name, {svg: text})）。
    几何在首次绑定时惰性扫描（大 SVG 的解析只发生一次）。

- static void EnsureScanned(ChartMapEntry e)
  - SVG 地图确保已扫描（幂等；GeoJSON 表是空操作）。

- static void BindSeries(ChartSeries s)
  - 把注册表几何绑定进 map 系列：克隆注入 s.regions，按名字
    并入 s.data 的值（data 优先）与 regions[] 覆盖（值/显式色；
    带 ring 的自定义覆盖区域原样追加）。未注册的地图名不报错、
    不注入（渲染器画空面板）。


## ChartMarkArea (class)

ECharts series.markArea 单条区间带。xMode = 类目 x 竖带
（v0/v1 为类目序号）；否则 y 值横带（v0/v1 原始整数域）。
color 0 = 主题 mark-area 缺省底色；name 非空时带内顶部
绘制标签（系列色）。

- bool xMode;

- int v0;

- int v1;

- int color;

- string name;

- static ChartMarkArea Of()


## ChartMarkLine (class)

ECharts series.markLine.data 的一条阈值线：kind 为
"average"/"min"/"max" 时从窗口数据自动推导；显式线用
yValue（水平线）；xValue + yValue 为定点斜线。label 支持
{value} 占位；lineType "" = 虚线（ECharts 默认）。

- string kind;

- string name;

- int xValue;

- int yValue;

- bool hasPoint;

- string label;

- string lineType;

- int color;

- bool labelShow;

- bool startArrow;

- bool endArrow;

- bool hasEnd;

- int x2Value;

- int y2Value;

- int valueIndex;
  - 按 kind 构造阈值线（"average"/"min"/"max" 或 "" = 显式线）。

- static ChartMarkLine Of(string kind)

- static ChartMarkLine Of(string kind, string name)
  - 带 name 的版本（ECharts data 项 {type:'average', name:'平均值'}）。

- static ChartMarkLine Average()
  - 平均线：窗口数据的算术平均。

- static ChartMarkLine Average(string name)
  - 带 name 的平均线。

- static ChartMarkLine Min()
  - 最小值线。

- static ChartMarkLine Max()
  - 最大值线。

- static ChartMarkLine At(int yValue, string label)
  - 显式水平线：y = yValue 处，label 支持 {value} 占位。

- static ChartMarkLine Clone(ChartMarkLine src)
  - 深复制；src 为 null 时返回 null。


## ChartMarkPoint (class)

标记点（ECharts markPoint.data）：在线/柱系列上标注极值或显式点。
kind = "max" | "min" | "point"；dataIndex 命中系列内的数据点；
xValue/yValue 用于显式坐标（dataIndex < 0 时）。

- string kind;

- string name;

- int dataIndex;

- int xValue;

- int yValue;

- string label;

- int color;

- string symbol;

- int size;

- int valueIndex;
  - 构造"最大值"标记点（渲染时从系列窗口数据推导位置）。

- bool sizeSet;

- static ChartMarkPoint Max()

- static ChartMarkPoint Max(string name)
  - 带 name 的版本（ECharts data 项 {type:'max', name:'最大值'}）。

- static ChartMarkPoint Min()
  - 构造"最小值"标记点（渲染时从系列窗口数据推导位置）。

- static ChartMarkPoint Min(string name)
  - 带 name 的版本（ECharts data 项 {type:'min', name:'最小值'}）。

- static ChartMarkPoint Point(int xValue, int yValue, string label)
  - 构造显式坐标 (xValue,yValue) 的标记点并附标签。

- static ChartMarkPoint Clone(ChartMarkPoint src)
  - 深复制；src 为 null 时返回 null。


## ChartNode (class)

Treemap / Sunburst 图的层级节点：名称、值和
嵌套子节点。叶子携带值；组的值由
其子节点推导（渲染为组的总量 / 环扫掠）。

- string name;

- int val;

- string symbol;

- int size;

- List<ChartNode> children;

- static ChartNode Leaf(string name, int val)
  - 构造叶子节点（自带值，无子节点）。

- static ChartNode Group(string name, List<ChartNode> children)
  - 构造组节点（值由子节点推导，val 置 0）。

- static ChartNode GroupVal(string name, int val, List<ChartNode> children)
  - 带显式 value 的组节点（ECharts data 节点的 value 字段，
    不等于子树累计时以显式值为准，tooltip 用）。

- static ChartNode Shaped(string name, int val, string symbol, int size)
  - 形状 + 尺寸变体（force 分类符号：diamond/triangle/rectangle…）。

- static ChartNode Clone(ChartNode src)
  - 深复制整棵子树；src 为 null 时返回 null。

- int Total()
  - 此节点下所有叶子值的总和（组的总量）。


## ChartOption (class)

完整图表配置（ECharts option）：标题、坐标轴、
系列和所有展示选项集中一处。用 Create() /
Of(series) / FromJson() 构建，直接调整字段，然后交给
ChartView.Of(option).Render(app, x, y, w, h)。三级控制对应
ECharts：option.*（全局）< series.*（逐系列）< data[i].*（逐项）。

- string title;

- string titleSub;

- string titleAlign;

- List<ChartAxis> xAxes;

- List<ChartJsonDataset> datasets;

- List<ChartVisualMap> visualMaps;

- List<ChartTitleSpec> titles;

- List<ChartGridSpec> grids;

- List<ChartMarkArea> markAreas;

- List<ChartAxis> yAxes;

- List<ChartSeries> series;

- List<ChartGeo> geos;

- List<ChartParAxis> parAxes;

- ChartType defaultType;

- bool showLegend;

- bool showTooltip;

- string tooltipTrigger;

- bool toolboxShow;

- bool toolboxDataView;

- bool toolboxMagicLine;

- bool toolboxMagicBar;

- bool toolboxRestore;

- bool toolboxSave;

- bool toolboxZoom;

- bool roam;

- string roamWheelMode;

- bool mapSelect;

- bool showGrid;

- bool showValues;

- bool animate;

- bool smooth;

- bool pointerCross;

- bool gradient;

- bool rounded;

- int animMs;

- int donutPct;

- int gaugeMax;

- bool pieLabels;

- bool pieCenterText;

- bool pieRings;

- bool overlay;

- List<int> radarMax;

- string radarShape;

- bool radarSplitArea;

- List<RadarPolar> polars;

- string legendOrient;

- string legendX;

- string legendSelectedMode;

- string legendFormatter;

- List<string> legendData;

- bool dataRangeShow;

- int dataRangeLo;

- int dataRangeHi;

- bool dataRangeCalculable;

- int dataRangeSplit;

- bool dataRangeHoverLink;

- List<ChartRangeSplit> dataRangeList;

- bool zoom;

- int markLine;

- bool markPoint;

- string markLabel;

- int markLo;

- int markHi;

- int gridLeft;

- int gridRight;

- int gridTop;

- int gridBottom;

- int gridLeftPct;

- int gridRightPct;

- int gridTopPct;

- int gridBottomPct;

- bool containLabel;

- int zoomStart;

- int zoomEnd;

- string zoomStartValue;

- string zoomEndValue;

- int windowStart;

- int windowEnd;

- int backgroundColor;

- int iwid;

- int connectGroup;

- List<int> rampColors;

- int rampLo;

- int rampHi;

- static int Auto()
  - 哨兵值，表示"此边界从数据推导"。

- ChartOption ConnectGroup(int groupId)
  - 声明本图加入 connect 组（ECharts connect：多图共享交互态）。
    组内所有图传同一个 groupId（任意稳定 int，通常用组长图的
    wid）。返回 this 便于链式装配。组内图共享：dataZoom 窗口、
    图例开关、十字线悬停类别。

- static ChartOption Clone(ChartOption src)
  - 深复制 option 的可变容器，供 timeline 合并和快照使用。
    返回值与输入共享的只有不可变标量字符串，不共享列表/样式外壳。

- static ChartOption Create()
  - 构造全默认 option：无标题无系列，图例与提示开启，
    入场动画 650ms，其余字段见字段注释。

- static ChartOption Of(List<ChartSeries> series)
  - 以现成系列列表构造 option（标题为空，轴另配）。

- static ChartOption Of(string title, List<string> categories, List<ChartSeries> series)
  - 声明式一次性构建：标题 + 分类轴 + 完整系列列表——
    对应 ECharts `{ title, xAxis.data, series }`。混合图表只是
    列表中不同类型的系列。

- static ChartOption Single(ChartSeries s)
  - 单系列 option 便捷形式。

- static ChartOption OfRings(string title, List<ChartSeries> series)
  - 多系列嵌套环饼图：每个 Pie 系列绘制为一层环。

- static ChartOption With(ChartType t, string title, List<string> cats)
  - 基础工厂：默认系列类型 + 可选分类轴。饼/环
    系列族将分类用作扇区标签；直角坐标系系列族用作
    x 轴标签。

- static ChartOption Line(string title, List<string> cats)
  - 折线图 option（标题 + 分类轴，后续 Add 系列默认 Line）。

- static ChartOption Bar(string title, List<string> cats)
  - 柱状图 option。

- static ChartOption Pie(string title, List<string> cats)
  - 饼图 option（cats 用作扇区标签）。

- static ChartOption Scatter(string title)
  - 散点图 option（无分类轴，数据走 points/专用列表）。

- static ChartOption Treemap(string title)
  - 矩形树图 option。

- ChartOption Add(string name, List<int> values)
  - 添加一个选项默认类型的系列；颜色自动分配。

- ChartOption Add(string name, ChartType type, List<int> values)
  - 添加显式类型的系列（混合图表：柱 + 折线叠加）。

- ChartOption AddLabel(string name, List<ChartData> data)
  - 从带名称/颜色的数据项添加系列（饼图的逐项标签、
    瀑布图总量柱、逐扇区颜色等）。

- ChartOption Add(ChartSeries s)
  - 添加现成系列（显式颜色 / 专用数据列表）。

- ChartOption Categories(List<string> cats)
  - 快速设置分类 x 轴（ECharts xAxis.data）。

- ChartOption RoamWheel(string mode)
  - 设置地图滚轮策略；非法值回退到兼容默认 zoom。

- ChartOption X(ChartAxis ax)
  - 追加一个 x 轴。

- ChartOption Y(ChartAxis ax)
  - 追加一个 y 轴（第二个 y 轴 = 右/次轴，系列用 axisIndex 绑定）。

- ChartOption RadarMax(List<int> maxs)
  - 声明雷达每轴满刻度（按指标顺序；空表 = 从数据推导）。

- ChartOption VisualRange(int lo, int hi, List<int> colors)
  - visualMap 连续映射：值域 [lo,hi] 线性经过 colors（≥2 个
    停止点，ECharts visualMap.inRange.color）。热力图按单元格
    值取色；未设的边界用数据最小/最大值。

- ChartOption DataZoom(int start, int end)
  - 设置 dataZoom 的初始窗口（百分比，自动钳制到 0..100）。

- ChartOption Grid(int left, int right, int top, int bottom)
  - 覆盖绘图区边距，等价于 ECharts grid.left/right/top/bottom。

- ChartAxis XAxis0()
  - 第一个 x 轴；未配置时用 XCategories() 现场拼一个分类轴。

- ChartAxis YAxis0()
  - 第一个 y 轴；未配置时返回默认数值轴（不写入列表）。

- ChartAxis YAxis1()
  - 第二个 y 轴；只有一根时回退为 YAxis0()（双轴图右轴）。

- List<string> XCategories()
  - x 轴的分类标签：第一个 x 轴的分类，否则为
    第一个系列的数据名，再否则 1..N。

- static ChartOption FromJson(string src)
  - 解析 ECharts 风格的选项文档。结构：
    
    {"title":"Revenue",
    "xAxis":{"type":"category","data":["Q1","Q2","Q3"]},
    "yAxis":{"type":"value"},
    "series":[{"type":"bar","name":"Rev","data":[12,28,20]},
    {"type":"line","name":"Cost","data":[{"value":8,"name":"Q1"},14]}]}
    
    旧的紧凑结构（labels + series[].values）仍然接受。

- static long TimeValueSec(JsonValue v, long dflt)
  - ECharts 时间值归一为 epoch 秒：数值 ≥1e11 视为毫秒（官方
    面积时间轴数据形态），其余为秒；字符串取其中的数字段按
    "YYYY-MM-DD"、"YYYY/M/D" 或 "M/D/YYYY"（可带 HH:MM(:SS)）
    解析（dynamic-data2 的 ["1997/10/4", 730] 形态）。不可解析
    返回 dflt。

- static int TimeDayOf(JsonValue v)
  - 时间轴 x 域归一：epoch 毫秒/秒/日期串 → epoch 天。引擎的
    时间域是天（TimeLabel/XOfTime/旧整数天数路径同域）。秒直接
    装 int32 会在 2038 后回绕成负值，TimeTicks 的 span 随之整型
    溢出、步长卡在 1 → 43 亿次刻度循环把内存撑爆（area-time-
    axis 20k 天数据挂死的根因）。天域 int32 安全到 ±580 万年。

- static long TimeStringSec(string s)
  - 提取字符串中的数字段（至多 6 段：年 月 日 时 分 秒），
    按日历转 epoch 秒；段数 <3 或字段非法返回 -1。

- static ChartScalar ParseScalar(JsonValue v, ChartScalar dflt)
  - 解析标量：数字按像素；字符串带 "%" 按百分比，否则按像素。
    v 为 null 时返回 dflt。

- static int ParseColor(JsonValue v, int dflt)
  - 解析颜色：数字直接用；"auto" 归 0（继承）；字符串经
    StyleSheet.ParseColor，无法解析且非空时返回 dflt。
    "transparent" 返回 alpha≈0 的哨兵色（非 0，不与"继承系列色"
    的 0 值语义冲突；视觉上不可见——瀑布图占位柱依赖它）。

- static List<int> ParseGradStops(JsonValue cv)
  - __grad 渐变对象（converter 序列化 echarts.graphic.
    LinearGradient 的产物）的 colorStops → ARGB 表。offset 暂
    忽略（等分插值，绝大多数示例是 0/1 双停）；非渐变对象
    或停点不足两个返回 null。

- static void ParseTextStyle(JsonValue v, ChartTextStyle text)
  - 把 JSON textStyle 逐字段并入 text（缺省字段保持原值）。

- static void ParseLineStyle(JsonValue v, ChartLineStyle line)
  - 把 JSON lineStyle 逐字段并入 line（color/color0 不接受数组形式）。

- static ChartPosition ParsePoint(JsonValue v, ChartPosition dflt)
  - 解析 [x,y] 数组为标量坐标；元素不足两个或非数组时返回 dflt。
    dflt 允许 null（cs.center 等字段语义就是 null = 未设）：此时
    元素缺失用 Auto 兜底，不能解引用 dflt。

- static void ParseGauge(JsonValue v, GaugeOption gauge)
  - 把 JSON gauge 段逐字段并入 gauge（center/radius/角度/值域与
    轴线、刻度、标签、分隔线、指针、标题、数值牌子对象）。

- static void ParseItemStateStyle(JsonValue v, ChartItemStateStyle style)
  - 把 JSON 单状态样式并入 style：颜色对、描边、borderRadius
    （数组最多取 4 个，单数值展开为四角同值）与线/面积子样式。

- static void ParseItemStyle(JsonValue v, ChartItemStyle style)
  - 解析 itemStyle：顶层字段并入 normal，再叠加
    normal/emphasis 子对象（ECharts 的紧凑与完整两种形式）。

- static void ParseSeriesStyle(JsonValue v, ChartSeries s)
  - 解析系列级样式：itemStyle、顶层 lineStyle、areaStyle
    （对象 {show,color,type} 或 bool）、label/{show,label}，
    以及顶层 color/show 覆盖。

- static void ParseGrid(JsonValue v, ChartOption o)
  - 解析 grid.left/right/top/bottom 绘图区边距覆盖。
    grid.{left,top,right,bottom}：数字=像素；"N%"=面板尺寸百分
    比（ECharts grid 双形态）。containLabel=true 时边距之外再
    包住轴标签（标签计入 grid 内）。

- static void ParseGridBody(JsonValue v, ChartOption o)

- static void ParseGridEdge(JsonValue e, bool isLeft, bool isVert, ChartOption o)
  - 解析 grid 单边：isLeft 选 gridLeft/gridRight，isVert 选水
    平/垂直字段对（px 与 pct 互斥，后写覆盖）。

- static int PercentOf(string s, int dflt)
  - "3%" -> 3；无 % 或空串返回 dflt。

- static void ParseDataZoom(JsonValue v, ChartOption o)
  - 解析 dataZoom（对象或数组取首项）：show/start/end 百分比，
    startValue/endValue 按类目名定位窗口（line-aqi），钳制到
    0..100 且 end < start 时交换。

- static void ParseMarkArea(JsonValue v, ChartOption o)
  - 解析 markArea（option 级与 series 级各挂一次）。data 的每对
    [{xAxis|yAxis, name?}, {...}]：x 对按类目名/序号成竖带，
    y 对成横带。首对"无名无色"的纯 y 影子带仍走旧
    markLo/markHi 通道（等价绘制，避免与旧金样重复）。

- static int MarkAreaNone()
  - markArea x 端点找不到时的哨兵。

- static int MarkAreaCatIdx(ChartOption o, JsonValue xv)
  - markArea 的 x 端解析：字符串在 x 类目表里查序号，数字直接
    取；"min"/"max"（scatter-weight 的数据范围矩形）暂不展开，
    返回哨兵跳过。

- static int StackIdFor(string name)
  - 把 ECharts 字符串 stack 组名映射为稳定正 int id
    （字符散列 + 1；空名返回 1；0 保留表示"无堆叠"）。

- static void ParseLinks(JsonValue v, List<ChartLink> into)
  - 解析 links 数组：source/from + target/to + value/val
    （缺省 1，负值归 0）；端点名为空的项跳过。

- static void ParseGraphLinks(JsonValue v, List<ChartLink> into, List<string> gnames)
  - graph 系列的 links 解析：端点可以是节点名、id 字符串
    （les-miserables 的 "1"）或数字序号（graph-grid source:0）。
    名字精确命中优先；否则按 gnames 序号解析；解析失败跳过。

- static string GraphNodeName(JsonValue a, JsonValue b, List<string> gnames)
  - graph link 端点解析（见 ParseGraphLinks）：JsonValue 取
    source/from 与 target/to 中第一个存在的；名字精确命中优先，
    其次全数字串/数字按序号落到 gnames。

- static void ParseCandles(JsonValue v, List<Candle> into)
  - 解析蜡烛数据：[open,high,low,close] 数组或同名键对象。

- static void ParseBubbles(JsonValue v, List<Bubble> into)
  - 解析气泡数据：[x,y,weight] 数组（weight 缺省 1）或
    {x,y,value|weight} 对象。

- static void ParseBoxes(JsonValue v, List<BoxItem> into)
  - 解析箱线数据：[lo,q1,med,q3,hi] 数组（标签空）或
    {name,value:[...]} 对象（不足五值跳过）。

- static void ParseErrors(JsonValue v, List<ErrorItem> into)
  - 解析误差条数据：{value,err|y±err} 对象（err 取绝对值）。

- static int GeoQ(double d)
  - 度 → 0.01° 定点整数（半值远离零，与 ChartGeoJson 量化
    一致）；geo 系列坐标（lines/scatter/graph）统一走这里。

- static void ParsePoints(JsonValue v, List<ChartPoint> into)
  - 解析散点数据：[x,y] 数组或 {x,y,symbolSize?,color?} 对象。

- static void ParseEvents(JsonValue v, List<ChartEvent> into)
  - 解析事件数据：{name,start,end,value?}（end < start 交换、
    value 缺省 1 且负值归 0，color 可选）。

- static List<ChartMapPoint> ParseMapPoints(JsonValue arr)
  - 解析顶点数组：[x,y] 或 {x,y}；非数组输入返回空表。

- static void ParseRegions(JsonValue v, List<ChartMapRegion> into)
  - 解析地图区域：{name,value,color?,rings:[{points,hole?}]}，
    或单环快捷形式 {points:[...]}；环不足 3 点或区域无环则跳过。

- static void ParseGeo(JsonValue v, ChartOption o)
  - ECharts geo 组件（对象或数组）。

- static void ParseParAxes(JsonValue v, ChartOption o)
  - ECharts parallelAxis：数组按 dim 下标落位（dim 缺省用数组序）。

- static void ParseGeoOne(JsonValue g, ChartOption o, int index)

- static int MarkCoordX(JsonValue p, int dft)
  - ECharts series.markLine：{data:[{type:'average'}|{yAxis:3}
    |[{xAxis,yAxis},{xAxis,yAxis}], label|name]}。也吃裸数组。
    markLine 两点形式的单点坐标：{coord:[x,y]} 优先，退回
    {xAxis,xValue} / {yAxis,yValue} 字段。

- static int MarkCoordY(JsonValue p, int dft)

- static void ParseMarkLines(JsonValue v, List<ChartMarkLine> into)

- static void ParseTitlePos(JsonValue v, string key, ChartTitleSpec ts, bool isTop)
  - 位置值：数字 = 像素，"N%" = 面板百分比，center/middle = 居中。

- static ChartTitleSpec ParseTitleOne(JsonValue tit)

- static ChartGridSpec ParseGridOne(JsonValue it)
  - grid 数组单项：四边 inset 解析（数字 px / "N%" pct）。

- static void ParseVisualMap(JsonValue v, List<ChartVisualMap> into)
  - 解析 visualMap（对象或数组，逐项调 ParseVisualMapOne）。

- static void ParseVisualMapOne(JsonValue v, List<ChartVisualMap> into)

- static int Lerp2(int a, int b, int tF)
  - 两色中点插值（tF 0..1000）。

- static int VisualSegmentColorAt(ChartOption o, int seriesIndex, int k0, int k1)
  - dimension 0（类目序号域）上子段区间 [k0,k1] 与 piece 区间
    的重叠命中——ECharts 的 piece 是 x 域范围而非逐点判定，
    area-pieces 的 (1,3) 段同时覆盖 1-2、2-3 两个子段。返回 0
    表示未命中。

- static int VisualColorAt(ChartOption o, int seriesIndex, int absIdx, int val)
  - visualMap 对某系列第 absIdx 个数据项的颜色覆盖（dimension
    0 = 类目序号，1 = 数据值 val）；未命中返回 0。

- static void ParseMarks(JsonValue v, List<ChartMarkPoint> into)
  - 解析 markPoint.data：{type:"max"|"min"} 或显式
    {xAxis,yAxis|dataIndex,name}；label/color 可选。

- static bool HasUserMapSeries(ChartOption o)
  - 解析整个 option 文档为 ChartOption：title/subtitle、grid、
    dataZoom、legend、dataRange、tooltip、connectGroup、markLine/
    markPoint/markArea、radar、xAxis/yAxis（对象或数组）与
    series 数组；未知字段忽略，缺省字段保持 Create() 默认。
    用户声明的 map 系列是否存在（geo 合成载体系列不算）。

- static ChartOption FromJsonValue(JsonValue v)

- static void ParseAxis(JsonValue v, List<ChartAxis> into, bool isX)
  - 解析 xAxis/yAxis（对象或数组，逐项调 ParseAxisOne）。

- static void ParseAxisOne(JsonValue v, List<ChartAxis> into, bool isX)
  - 解析单根轴：category 轴读 data[]，数值轴读 min/max；
    name/inverse/nameLocation 与 axisLabel.rotate（钳 -90..90）、
    axisLabel.interval 通用。


## ChartParAxis (class)

平行坐标的一根轴（ECharts parallelAxis[dim]）：轴名、显式
min/max、类目维的类目表。渲染时 min/max 缺省由该维数据推导。

- string name;

- int min;

- int max;

- bool minSet;

- bool maxSet;

- bool inverse;

- List<string> cats;

- static ChartParAxis Of()

- static ChartParAxis Clone(ChartParAxis src)


## ChartPoint (class)

直角坐标系散点的一个 x/y 数据点，可带逐点尺寸与颜色
（散点/折线的 points 专用列表用）。

- int x;

- int y;

- int z;

- int size;

- bool sizeSet;

- int color;

- string name;

- static ChartPoint Of(int x, int y)
  - 构造一个点（无逐点尺寸，继承系列颜色）。

- static ChartPoint Sized(int x, int y, int size)
  - 构造带逐点尺寸（直径像素）的点。

- static ChartPoint Clone(ChartPoint src)
  - 深复制；src 为 null 时返回 null。


## ChartPosition (class)

二维标量坐标（仪表盘 center、指针 offsetCenter 等用）。

- ChartScalar x;

- ChartScalar y;

- static ChartPosition Of(ChartScalar x, ChartScalar y)
  - 构造一个 (x,y) 标量坐标。

- static ChartPosition Clone(ChartPosition src)
  - 深复制（含两个标量）；src 为 null 时返回 null。


## ChartRangeSplit (class)

dataRange.splitList 的一个命名值区间（ECharts dataRange.data）。
lo/hi 用 ChartOption.Auto() 表示开口。

- string label;

- int lo;

- int hi;

- static ChartRangeSplit Of(string label, int lo, int hi)
  - 构造一个命名区间；lo/hi 可为 ChartOption.Auto() 表示开口。

- static ChartRangeSplit Clone(ChartRangeSplit src)
  - 深复制；src 为 null 时返回 null。


## ChartScalar (class)

长度/位置标量：像素（Px）或相对主体的百分比（Pct，0..100）。

- int amount;

- bool percent;

- static ChartScalar Px(int amount)
  - 固定像素标量。

- static ChartScalar Pct(int amount)
  - 百分比标量（amount = 百分数）。

- static ChartScalar Clone(ChartScalar src)
  - 深复制；src 为 null 时返回 null。


## ChartSeries (class)

一个数据系列（ECharts series[i]）。每个系列携带自己的类型，
混合图表自然实现：带折线叠加的柱状图只是
共享同一坐标系的两个不同类型系列——无需 AsKind 垫片。
axisIndex 将系列绑定到 yAxis（0 = 左/主，1 = 右/次）；
stack 将系列归入一个堆叠柱/面积（相同正 id；
StackedBar / StackedArea 工厂默认 stack = 1）。
旧的伪类型（Area、StepLine、Donut、Rose 等）已移除：其行为现由
系列子实体表达——areaStyle、step、innerPct、roseType、sort
——与 ECharts 的建模完全一致。数据为统一的 List<ChartData>；
多值系列族（candle/bubble/box/error/scatter）使用专用的
列表。

- string name;

- ChartType type;

- int axisIndex;

- int xIndex;

- bool visBlocked;

- int stack;

- string stackName;

- int color;

- bool hidden;

- int smooth;

- bool areaStyle;

- bool endLabelShow;

- int endLabelDistance;

- string endLabelFormatter;

- string step;

- string sort;

- string roseType;

- ChartPosition center;

- ChartScalar radius;

- ChartScalar radiusInner;

- int startAngle;

- bool clockWise;

- int polarIndex;

- int selectedOffset;

- int barWidth;

- int barWidthPct;

- int barHeight;

- int barGapPct;

- bool silent;

- string symbol;

- int symbolSize;

- int pointG;

- string symbolSizeFn;

- int showSymbol;

- bool showBackground;

- int backgroundColor;

- int innerPct;

- bool hbar;

- string treeOrient;

- ChartLineStyle lineStyle;

- ChartLineStyle treeLine;

- bool piePerPoint;

- string custom;

- string selectedMode;

- string mapName;

- int geoIndex;

- bool isGeoBase;

- string picSymbol;

- string picRepeat;

- bool picClip;

- string picPos;

- int picBound;

- int picW;

- int picH;

- int picWPct;

- int picHPct;

- List <List<int>> parRows;

- List<string> riverTimes;

- List<int> riverVals;

- List<int> riverCat;

- List<string> riverNames;

- int forceScaling;

- int forceGravity;

- int forceMinRadius;

- int forceMaxRadius;

- int forceNodeColor;

- int forceLinkColor;

- string forceLinkSymbol;

- string chordRibbonType;

- int chordSort;

- bool chordSortSub;

- int chordGapDeg;

- int chordRingWidthPct;

- List <List<int>> matrix;

- string funnelAlign;

- int funnelGap;

- bool funnelPercent;

- int maxSizePct;

- bool funnelLabelOut;

- int forceCurveness;

- int wcMinFontSize;

- int wcMaxFontSize;

- string wcRotate;

- string wcRotateList;

- ChartItemStyle itemStyle;

- ChartTextStyle label;

- bool labelShow;

- bool pieLabels;

- string labelFmt;

- string labelPos;

- int labelRotate;

- List<ChartData> data;

- List<Candle> candles;

- List<Bubble> bubbles;

- List<BoxItem> boxes;

- List<ErrorItem> errors;

- List<ChartPoint> points;

- List<ChartNode> tree;

- List<ChartLink> links;

- List<ChartMapRegion> regions;

- List<ChartEvent> events;

- List<ChartMarkPoint> marks;

- List<ChartMarkLine> markLines;

- string graphLayout;

- List<int> nodeX;

- List<int> nodeY;

- List<string> graphCats;

- string coordSys;

- List <List<ChartPoint>> geoLines;

- GaugeOption gauge;

- static ChartSeries Of(string name, ChartType type, List<int> values)
  - 从纯 int 值构建系列（每个值变为 ChartData.Of(v)）。

- static ChartSeries Named(string name, ChartType type, List<ChartData> data)
  - 从显式数据项构建系列（名称 / 逐项颜色）。

- static ChartSeries Line(string name, List<int> values)
  - 折线系列。

- static ChartSeries Area(string name, List<int> values)
  - 面积折线系列（areaStyle = true，折线下方填充）。

- static ChartSeries Bar(string name, List<int> values)
  - 柱状系列。

- static ChartSeries StackedBar(string name, List<int> values)
  - 堆叠柱系列（stack = 1；同名 stackName 分组可用 JSON 覆盖）。

- static ChartSeries HBar(string name, List<int> values)
  - 水平条形系列（类目在 Y 轴）。

- static ChartSeries HStacked(string name, List<int> values)
  - 水平堆叠条形系列（hbar + stack = 1；同名 stackName 分组）。

- static ChartSeries OfBarPoints(string name, List<ChartPoint> pts)
  - 值对柱状系列（ECharts 双数值轴柱形 bar13）：柱画在 points[i].x
    处、从零线长到 points[i].y；x/y 都是数值轴。

- static ChartSeries StepLine(string name, List<int> values)
  - 阶梯折线系列（step = "middle"）。

- static ChartSeries StackedLine(string name, List<int> values)
  - 堆叠折线系列（stack = 1）。

- static ChartSeries StackedArea(string name, List<int> values)
  - 堆叠面积系列（stack = 1 且 areaStyle = true）。

- static ChartSeries Pie(string name, List<int> values)
  - 饼图系列（数据项名称作扇区标签）。

- static ChartSeries Donut(string name, List<int> values)
  - 环形图系列（innerPct = 55）。

- static ChartSeries Gauge(string name, int val)
  - 仪表盘系列：单值，值域由 GaugeRange / option.gaugeMax 决定。

- static ChartSeries GaugeNumber(string name, double val)
  - 仪表盘系列（double 值版本，保留小数）。

- static ChartSeries Polar(string name, List<int> values)
  - 雷达（极坐标）系列；每轴满刻度由 option.radarMax 声明。

- static ChartSeries WordCloud(string name, List<ChartData> words)
  - 词云系列；data 项名称为词、值为权重。

- static ChartSeries Funnel(string name, List<int> values)
  - 漏斗系列（默认按值降序）。

- static ChartSeries Pyramid(string name, List<int> values)
  - 金字塔系列（sort = "ascending"，倒漏斗）。

- static ChartSeries Rose(string name, List<int> values)
  - 玫瑰图系列（roseType = "radius"，扇区半径随值变化）。

- static ChartSeries OfCandles(string name, List<Candle> candles)
  - 由 OHLC 柱构建蜡烛图系列（ECharts type "k"）。

- static ChartSeries OfBubbles(string name, List<Bubble> bubbles)
  - 由气泡构建加权散点系列（ECharts scatter + symbolSize）。

- static ChartSeries OfBoxes(string name, List<BoxItem> boxes)
  - 由逐分类统计量构建箱线图系列（扩展渲染器：
    ECharts 2.2.7 没有 boxplot 类型）。

- static ChartSeries OfErrors(string name, List<ErrorItem> errors)
  - 由值 +/- 误差对构建误差条系列（扩展渲染器）。

- static ChartSeries OfPoints(string name, List<ChartPoint> points)
  - 由显式 x/y 点构建散点系列。

- static ChartSeries OfLinePoints(string name, List<ChartPoint> points)
  - 值对折线系列（ECharts series.type='line' 且 data 为
    [[x,y],...]：line7 双数值轴）。与 OfPoints（散点点云）的
    区别在类型：折线渲染器画连线+符号+markLine 全套。

- static ChartSeries OfTree(string name, ChartType type, ChartNode root)
  - 由根节点构建层级系列（Treemap / Tree / Sunburst）。
    系列持有根列表；子节点可任意深度嵌套。

- static ChartSeries OfTreeOrient(string name, ChartNode root, string orient)
  - 带显式布局方向的树系列（ECharts tree.orient）。
    树默认显示节点标签（ECharts label.show 默认 true），
    JSON label.show=false / labelShow=false 时隐藏、悬停显。

- static ChartSeries OfLinks(string name, List<ChartLink> links)
  - 由有向流转链接构建 Sankey 系列（节点从链接推导；
    扩展渲染器——ECharts 2.2.7 没有 sankey 类型）。

- static ChartSeries Chord(string name, List<ChartLink> links)
  - 和弦图系列：节点从 links 的 from/to 推导。

- static ChartSeries ChordMatrix(string name, List<string> nodes, List <List<int>> matrix)
  - ECharts2 chord 矩阵形式：matrix[i][j] = 节点 i → j 的权重
    （对角 = 自环），节点名/逐点色取 data（按行序补齐 ChartData）。

- static ChartSeries Force(string name, List<ChartLink> links)
  - 力导向图系列：节点从 links 的 from/to 推导。

- static ChartSeries Venn(string name, List<ChartData> data)
  - 韦恩图系列：data 项依次为 [A, B, A∩B]（名称 + 值）。

- static ChartSeries Waterfall(string name, List<ChartData> data)
  - 由命名的累计柱数据构建瀑布图系列（渲染器构建
    不可见的堆叠基底；扩展渲染器）。

- static ChartSeries SunburstTree(string name, ChartNode root)
  - 由层级根构建 Sunburst 系列（径向环；
    扩展渲染器——ECharts 2.2.7 没有 sunburst 类型）。

- static ChartSeries RadialBars(string name, int val)
  - 同心进度环，一个系列 = 一个环（扩展渲染器；
    option 的 gaugeMax 为满刻度）。

- static ChartSeries OfRegions(string name, List<ChartMapRegion> regions)
  - 地图系列：从调用方提供的多部件区域构建。渲染器
    不硬编码世界地图，polygon 由调用方决定（确定性
    样例见 gallery）。

- static ChartSeries OfEvents(string name, List<ChartEvent> events)
  - Event River 系列：从显式事件构建。

- ChartSeries MarkPoint(ChartMarkPoint m)
  - 给线/柱系列追加一个 markPoint。option.markPoint=true 时
    渲染器也会自动推导 max/min；显式 marks 优先展示。

- ChartSeries MarkLine(ChartMarkLine m)
  - 给线/柱系列追加一条 markLine（threshold/average/min/max）。

- ChartSeries GaugeRange(int min, int max)
  - 仪表盘的几何与范围。百分比相对图表主体。

- ChartSeries GaugeArc(int startAngle, int endAngle)
  - 以钟面约定设置起止角（0 = 12 点钟、顺时针增），
    内部换算为数学角 360-角度。

- ChartSeries GaugeLayout(int centerXPct, int centerYPct, int radiusPct)
  - 设置圆心（百分比）与半径（百分比，相对图表主体）。

- ChartSeries GaugeTicks(int splitNumber, int minorTicks)
  - 设置主刻度数与每主格内的细刻度数（axisTick.splitNumber）。

- ChartSeries GaugeSizes(int axisWidth, int tickLength, int splitLength, int pointerLengthPct, int pointerWidth)
  - 一次性设置轴线宽、刻度长、分隔线长与指针长（百分比）/宽。

- ChartSeries GaugeVisible(bool axis, bool ticks, bool labels, bool title, bool detail)
  - 逐项开关轴线 / 刻度 / 轴标签 / 标题 / 数值牌。

- ChartSeries GaugeText(int titleX, int titleY, int detailX, int detailY, string suffix)
  - 标题/数值牌改用像素偏移，并把数值牌 formatter 设为
    "{value}" + suffix。

- ChartSeries GaugeColors(int stop1, int color1, int stop2, int color2, int stop3, int color3, int stop4, int color4)
  - 以四段停靠点替换轴线色带；stop1..stop4 为百分比（0..100），
    存储时乘 10 换算为 0..1000 千分位。

- int Count()
  - data 项数；纯值对系列（[[x,y],...]，无 data 项）返回
    points 数——极值/均值/markLine 等窗口推导据此看到值对。

- double Number(int i)
  - 第 i 项的 double 值；i 越界返回 0.0，整型项返回其 val。
    值对系列取第 i 对的 y。

- int Value(int i)
  - 第 i 项的值取整为 int（四舍五入、半数远离零；越界同 Number
    返回 0）。不截断：小数数据（line6 流量基流 0.86..1.5）截断后
    全体归 0，画出的基线与悬停数值（number 保留小数）对不上。

- bool SeriesFrac(int i)
  - 第 i 项是否小数（numberSet 且值非整）。折线族渲染/量程/
    提示对这类数据按 1/1000 定点承载（line6 流量 0.46..365、
    降雨量 -0.005..-0.955），轴走 leftMinF/rightMinF 定点域。

- static ChartSeries Clone(ChartSeries src)
  - 复制系列外壳和所有可变数据列表。Merge 只会替换这些列表
    或显式样式字段，因此不会反向修改输入 option。


## ChartSkin (class)

图表皮肤（ChartSkin）：图表配色的独立板块，与全局皮肤主题
（Theme）解耦——一套皮肤就是一份命名的定性调色板：default 取
ECharts 6.1 默认主题色板（src/visual/tokens.ts color.theme 9 档），
infographic/shine/macarons2 取官方主题包各前 8 档。Chart.Palette
在主题 chart token 未定义时回落到当前皮肤，换肤一次即生效于
全部图型（折/柱/饼/漏斗……）。未知名一律按 default 处理。

- static string current;
  - 当前全局图表皮肤名。null = "default"。

- static string Current()
  - 当前皮肤名（规范化：null / 未知名都归 default）。

- static void SetCurrent(string name)
  - 切换当前图表皮肤；未知名回退 default。

- static int Count()
  - 内置皮肤数量；选择器按 Name(i)/Label(i) 枚举。

- static string Name(int i)
  - 第 i 套内置皮肤名。

- static string Label(int i, bool en)
  - 第 i 套皮肤的显示名。

- static int IndexOf(string name)
  - 皮肤名转下标；未知名 -1。

- static int ColorAt(string name, int i)
  - 皮肤第 i 档定性色（ARGB，i 自动取模 8 循环）。8 档齐全；
    返回 0 仅当皮肤名未知，由调用方走自己的默认兜底。


## ChartSource (class)

图表的虚拟、拉取式数据源——图表无需持有
原始点数组，数百万点的系列也不产生逐单元对象
分配（对应 DataTable 的 DataSource）。子类化它，
按需从自己的列式/类型化存储读取点，或用 SeriesListSource 包装
内存中的 List<ChartSeries>。

- virtual int SeriesCount()
  - 系列数。

- virtual string SeriesName(int s)
  - 系列 s 的名称。

- virtual int SeriesColor(int s)
  - 系列 s 的颜色；0 = 自动（调色板）。

- virtual int PointCount(int s)
  - 系列 s 的数据点数。

- virtual int ValueAt(int s, int i)
  - 系列 s 第 i 点的数值。


## ChartStage (class)

漏斗/玫瑰/饼图的一个阶段：值、填充色和显示名。

- int val;

- int color;

- string name;

- int seriesIndex;

- int dataIndex;

- ChartStage(int v, int col, string nm, int si)
  - 构造一个阶段；si 为所属系列下标，dataIndex 初始为 0。


## ChartState (class)

高性能图表路径的缓存 min/max 抽取。每个大图表
持有一个（类似 DataTableState）；底层数据变化时
调用 Invalidate()。ChartBig 惰性填充并在帧间复用。

- int version;

- int builtVersion;

- int builtW;

- int builtSeries;

- int cols;

- int axisLo;

- int axisHi;

- List <List<int>> colMin;

- List <List<int>> colMax;

- int animationKey;

- bool animationKeySet;

- ChartState()
  - 默认构造：入场动画用 legacy 键（5200000 + 控件宽）。

- ChartState(int key)
  - 显式实例键构造；key != 0 时入场动画键与控件宽度解耦。

- int IntroKey(int w)
  - 入场动画键：显式键 > 0 时用 5300000+key，否则 legacy 回退
    5200000+w。

- void Invalidate()
  - 将缓存标记为过期，使下次渲染重新抽取源数据。


## ChartSvgCursor (class)

文本区间数字游标：SVG 属性/路径里的十进制数流（分隔符任意，
负号直接拼在前一个数后也是新数，如 "10-5" = [10, -5]）。

- string s;

- int i;

- int to;

- public bool any;

- static ChartSvgCursor Of(string s, int from, int to)

- bool HasMore()
  - 是否还有非分隔符字符可读。

- int Peek()
  - 越过空白/逗号后返回下一个字符（到尾返回 0），不推进。

- double NextNum()
  - 读一个带符号十进制数（含指数），推进游标；无数字时
    any=false 并返回 0（游标原地不动）。

- void SkipSep()

- static double ParseDouble(string s, int start, int end)
  - [start,end) 十进制串 → double（手写，免逐数 JSON 开销；
    1e308 内安全，指数钳 300）。


## ChartSvgMap (class)

SVG 地图（echarts registerMap(name, {svg})）的 Zan 侧扫描器。
不做完整 XML 解析，只提取地图渲染需要的最小集合：
① 根元素 viewBox（缺省退化 width/height，再缺省 0 0 100 100）；
② 形状元素 path/rect/circle/ellipse/polygon/polyline 的几何，
经 g/形状上的 translate/scale/matrix 仿射栈换算（素材中
无 rotate，暂不实现）；
③ 区域命名：name= > data-name= > id=（ECharts SVG 地图的
region 名同源）。
曲线（C/S/Q/T/A）只取端点做折线近似——按名填色、命中与
标签锚点在这个精度下足够；底图质感由 nanosvg 光栅承担
（ChartViewMap 的 svgMode）。text 不参与（nanosvg 同样
不渲染文字）；defs/clipPath/marker/mask/symbol/pattern 内的
形状不渲染，整体跳过。
坐标输出为 SVG 用户单位取整（int，y 向下与屏幕系一致），
MapLayout 可直接 contain-fit；viewBox 作为布局源框，保证
光栅底图与折线覆盖共用同一仿射、像素对齐。

- static void Scan(ChartMapEntry e)
  - 扫描入口：填充 entry 的 viewBox 与 regions（幂等）。

- static void RootBox(ChartMapEntry e)
  - 根 viewBox：svg 根标签的 viewBox="x y w h"；退化 width/height
    （数值带 px/pt 单位尾巴也认；百分比不认）；再缺省 0 0 100 100。

- static bool IsSkipEl(string name)
  - defs/clipPath/marker/mask/symbol/pattern：内部形状不渲染。

- static void Tag(string svg, int lt, int gt, List<double> tf, List<string> skip, List<ChartSvgShape> shapes)
  - 处理一个标签：闭标签弹仿射栈/跳过栈；开标签解析 transform、
    形状出几何。lt/gt 是 '<'/'>' 下标。

- static string RegionName(string svg, int from, int to)
  - 区域名优先级 name= > data-name= > id=。

- static List<ChartMapRing> ShapeRings(string name, string svg, int from, int to, double a, double b, double c, double d, double ee, double f)
  - 一个形状元素的环组（折线化）。line 无法成面，跳过。

- static List<ChartMapRing> PathRings(string dd, double a, double b, double c, double d, double ee, double f)
  - path d → 环组。M/m 起环；Z/z 闭合并落环（≥3 点才留）；
    C/S/Q/T 取终点，A 取末参端点，H/V 单轴；命令后的数对
    隐式重复（SVG 语义）。子路径的洞判定在落环时统一做
    （首点落在第 0 条子路径内 = 洞）。

- static void Finish(List<ChartMapRing> rings, List<ChartMapPoint> cur)
  - 落环：子路径 1..n 的首点在第 0 条子路径内 → hole。

- static void Emit(List<ChartMapPoint> pts, double x, double y, double a, double b, double c, double d, double ee, double f)
  - 仿射换算后取整落点；与上一点重合的丢弃（免零长边）。

- static List<double> ParseTransform(string tr, double a, double b, double c, double d, double ee, double f)
  - transform 属性串："translate(12.5,3) scale(2)" 等，逐段
    local ∘ current 复合。rotate 素材中未出现，不支持。
    返回 [a,b,c,d,e,f]。

- static string Attr(string svg, int from, int to, string name)
  - 读 [from,to) 区间里的属性值（' 与 " 两种引号、无引号都认）。
    name 必须是完整属性名（前面不能是字母/-/_，防止 name= 误配
    data-name= 的尾部）。

- static double UnitNum(string s)
  - "12.5px" → 12.5；解析失败或百分比 → 0。

- static void Push(List<double> tf, double a, double b, double c, double d, double ee, double f)


## ChartSvgShape (class)

扫出的一个形状：区域名 + 折线化环组（环内含洞标记）。

- string name;

- List<ChartMapRing> rings;

- static ChartSvgShape Of(string name, List<ChartMapRing> rings)


## ChartTextStyle (class)

文本样式（颜色、字号、字体族、阴影），JSON 可逐字段覆盖。

- int color;

- int fontSize;

- string fontStyle;

- string fontWeight;

- string fontFamily;

- int shadowColor;

- int shadowBlur;

- static ChartTextStyle Create()
  - 构造默认样式：颜色 0（跟随主题）、字号 0（渲染器缺省）。

- static ChartTextStyle Clone(ChartTextStyle src)
  - 深复制；src 为 null 时返回 null。


## ChartTheme (class)

图表主题包（图表自己的皮肤层）：`themes/<名>.css` 纯 CSS 配置，
调色板走 `chart::series-N`，轴线/网格/图例/缩放柄等走
`chart::<part>`，深色包另带 `chart` 画布底色。由
`App.UseChartTheme(name)` 按名叠加到样式表顶层，与 Gui 皮肤
相互独立、分层生效——换 Gui 皮肤不动图表配色，换图表主题
不动界面。

本类只负责发现与读取（磁盘优先、exe 内嵌兜底），不含任何
色值：图表的颜色全部在 CSS 包里，改主题请改包，不要把色值
写进代码。包的属性映射见各包文件头注释。

- static string Css(string name)
  - 读取主题包 `themes/<name>.css` 的文本。name 为 ""/"default"
    或找不到包时返回 ""（= 不用主题包，图表跟随 Gui 皮肤）。
    搜索根：$ZAN_CHART_THEMES、exe 旁与自解包布局、cwd 上溯的
    stdlib 副本；磁盘优先（用户可整包覆盖），编译进 exe 的
    内嵌资源 `chartthemes/<name>.css` 兜底（发布后的单文件
    程序靠它找到内建包）。

- static List<string> Names()
  - 可发现的主题包名（各搜索根下 `*.css` 的文件名 + exe 内嵌
    的 `chartthemes/*.css` 资源），去重、字典序。

- static List<string> Roots()
  - 主题包搜索根（最具体者优先）：环境变量指定的目录、exe
    所在位置与自解包/发布布局、cwd 上溯到源码树的 stdlib 副本
    （从构建树或工程目录运行时命中）。


## ChartTimeline (class)

ECharts timeline（2.2.7 bar11/pie7/map14/map19/scatter4 的动态时间轴）：
多帧 option + 底部播放器（播放/暂停、前/后帧、帧轴点选）+ 帧合并。

模型（全链路确定性——不读时钟做逻辑，帧推进只由显式输入驱动）：
- 调用方把 N 帧的 `ChartOption` 装进 `frames`，
当前帧号持久化在 App 状态键（`ChartTimeline.TlIdxKey`），跨帧存活。
- `Draw` 画播放器条（面板底部，dataRange 条之上），
返回当前帧号；宿主用 `Current` 从 frames 取帧渲染。
- 自动播放：挂钟只用于「距上拍是否已过 intervalMs」的判断
（Carousel.autoplay 同款模式），上拍时刻由调用方持有
（即时模式宿主每帧重建，实例字段会归零）。
- `Merge` 把当前帧的数据/标题叠加到基础 option 上，
供 ECharts「baseOption + options[]」时间轴语义：轴/图例等
外壳留在 base，series data 逐帧替换。

- List<ChartOption> frames;
  - 帧序列：每帧一个完整 option（ECharts timeline 的 options[]）。

- List<string> labels;
  - 帧标签（空 = 用帧 option 的 title，再退化为 1..N）。

- int intervalMs;
  - 自动播放间隔（毫秒；0 = 不自动播放）。

- ChartTimeline()

- static ChartTimeline Of()
  - 构造空时间轴（帧与标签逐个经 Frame/Labels 追加）。

- ChartTimeline Frame(ChartOption o)
  - 追加一帧（返回 this 便于链式装配）。

- ChartTimeline Labels(List<string> ls)
  - 逐帧标签（与 Frame 同序；超出部分忽略，缺省回退 title/序号）。

- ChartTimeline AutoPlay(int interval)
  - 自动播放（毫秒/帧；ECharts timeline.autoPlay + PlayState）。

- int FrameCount()
  - 帧数。

- ChartOption FrameAt(int i)
  - 第 i 帧的 option；越界返回 null。

- ChartOption Current(int idx)
  - 当前帧（钳制后；空序列返回 null）。

- static int TimelineIdxOf(App app, int wid, int n)
  - 宿主侧帧号读取：从 App 状态取当前帧号（未初始化/越界钳到
    有效域），供「先渲染当前帧、再画播放器条」的调用顺序。

- static ChartTimeline FromJsonValue(JsonValue tl, JsonValue optionsNode)
  - 从 ECharts timeline JSON 节点解析：
    {"timeline":{"data":["2011","2012"],"autoPlay":true,"playInterval":800},
    "options":[{"series":[...]}, ...]}
    也接受单对象 timeline（2.2.x 全部是单对象）。data[] 是逐帧标签；
    options 缺失时退回 baseOption（空时间轴，无帧）。base 的
    外壳字段（轴/图例/标题等）由调用方持有，本解析只产帧与标签。

- string LabelAt(int i)
  - 帧显示名：labels[i] → frames[i].title → 序号。

- static int Clamp(int i, int n)
  - 帧号钳制：负值回 0，越界回尾帧（空序列恒 0）。

- static int StepPlay(int i, int n, int last, int now, int interval)
  - 自动播放推进：now - last >= interval 时翻下一帧（循环）。
    纯函数 seam：返回新的帧号与新的上拍时刻。

- static ChartOption Merge(ChartOption baseOpt, ChartOption frame)
  - 帧合并（ECharts baseOption + options[i] 语义的落地）：
    base 的轴/图例/缩放/标记等外壳保留，把帧的 series 逐条
    叠进同名系列（数据 + 每帧样式字段），base 没有的系列追加；
    帧标题非空时覆盖 base 标题。base 自身不被修改。

- static int TlIdxKey(int wid)
  - 当前帧号（持久化；默认 -1 = 首帧前未初始化）。

- static int TlPlayKey(int wid)
  - 播放/暂停（1 = 播放中）。

- static int TlTickKey(int wid)
  - 本帧上拍时刻（autoplay 用；由宿主每帧回写）。

- static int TlHitPlay(int wid)
  - 命中 id：播放/暂停按钮、前后帧、第 bi 个帧点。

- static int TlHitPrev(int wid)
  - 命中 id：前一帧按钮。

- static int TlHitNext(int wid)
  - 命中 id：后一帧按钮。

- static int TlHitDot(int wid, int bi)
  - 命中 id：第 bi 个帧点（点选跳帧）。

- static int Height(App app)
  - 播放器条高度（宿主在 dataRange 之上让位；不画时为 0）。

- int Draw(App app, int wid, int x, int y, int w)
  - 画播放器条并驱动帧状态（面板内底部一横条）：
    [播放/暂停] [前一帧] [轨道 + 帧点] [后一帧] [当前帧标签]。
    帧号/播放态持久化在 wid 的 App 状态里；autoplay 到拍推进
    （Carousel.autoplay 同款：上拍时刻由 App 状态持有，宿主
    每帧重建也不丢）。返回当前帧号。


## ChartTitleSpec (class)

title 数组的一项（line-gradient 等多标题示例）。top/left 支持
百分比（pct 0..100）或像素（px）；-1 = 未声明（走缺省头位）。

- string text;

- string sub;

- int topPct;

- int topPx;

- int leftPct;

- int leftPx;

- string align;

- static ChartTitleSpec Of()


## ChartToolbox (class)

ECharts 风格工具箱：右上角图标按钮组 + 悬停 tip。
按钮组占位由 Chart.toolReserve 告诉标题/图例，避免互相遮挡。

- static int Btn(App app)
  - 单个工具按钮的边长。

- static int Gap(App app)
  - 按钮间距。

- static int Chrome(App app)
  - 按钮排底座四周的描边留白。

- static int Height(App app)
  - 工具箱占用的总高度（按钮 + 上下留白）。

- static int Pad(App app)
  - 与 DrawPanelI 同一套内边距（Theme 已按 DPI 缩放，禁止再 Scale）。

- static bool Cartesian(ChartOption o)
  - 主导系列是否为直角坐标系类型（折线/柱状/散点/K 线）——
    决定按钮组是 3 枚还是 6 枚。

- static List<int> Actions(ChartOption o)
  - feature 声明掩码 -> 本帧实际渲染的按钮动作列表。直角坐标
    专属按钮（切折线/切柱状/区域缩放）只在直角坐标图出现。

- static int Width(App app, ChartOption o)
  - 工具箱占用的宽度（含右侧内边距外的按钮排）。

- static void Draw(App app, int x, int y, int w, int h, int wid, ChartOption o)
  - 绘制右上角按钮排并处理点击：按钮集合来自 feature 声明掩码
    （Actions）；悬停显示 tip，开合态叠加数据视图浮层。

- static void Click(App app, int action, int wid, ChartOption o, int x, int y, int w, int h, int magic, int zOn)
  - 按钮动作分发：0 数据视图开合、1/2 魔法切换（写 TbMagicKey
    并抛 MagicTypeChanged）、3 还原、4 排队保存图片、5 区域
    缩放开合。


## ChartView (class)

组件化、带动画的图表控件（Chart 控件的现代形态）。
一次性绑定 ChartOption（ECharts 风格：标题 + 轴 + 系列，
每个系列携带自己的类型），然后每帧调用 Render。
它会播放增长入场动画，绘制渐变/平滑系列和可选的悬停
十字线 + 数值工具提示。多级控制对应 ECharts：option.*
（全局）< series.*（逐系列）< data[i].*（逐项），因此混合图表
只是共享同一坐标系的不同类型系列。

- ChartOption option;

- ChartOption sourceOption;

- ChartOption initialOption;

- ChartController controller;

- string directStatus;

- string directStatusMessage;

- ResolvedChart resolved;

- bool staticFrame;

- int wid;
  - 每个图表稳定的动画键。默认为新 WidgetId，但
    即时模式/虚拟化列表中的调用方（控件 id 顺序随
    行滚动进出而变动）应通过 Keyed() 传入自有稳定键，
    避免增长入场动画每帧被重置为 0。

- UiEvent Rendered;
  - 保留式生命周期通知。图表仍由 Render 驱动，但调用方
    可以在创建后订阅，不必改写每个 renderer 的交互分支。

- UiEvent Resized;

- UiEvent Updated;

- UiEvent Disposed;

- int lastRenderW;

- int lastRenderH;

- int directVersion;

- int lastControllerVersion;

- int lastDirectVersion;

- bool hasRendered;

- bool disposed;

- ChartEventHub eventHub;

- int eventHitId;

- bool pointerWasOver;

- ChartHit currentHit;

- ChartHit previousHit;

- int lastZoomLo;

- int lastZoomHi;

- int lastEventStateWid;

- static ChartView activeEventView;

- void InitLifecycle()
  - 初始化保留式生命周期字段（事件、动画/版本跟踪、事件 hub）。

- static void ApplyDataLegend(App app, ChartOption o)
  - 把图例开关写回 data.hidden（多数据项）或 series.hidden（单值系列）。
    画廊每帧重建 option，必须从 App 状态恢复，否则点了等于没点。

- static string ttName;
  - 层级图表（treemap/sunburst）最近一次的悬停命中。
    由命中追踪辅助函数设置，调用方立即读取以绘制工具提示，
    因此不会跨帧存留。

- static int ttVal;

- static int ttX;

- static int ttY;

- static int ttW;

- static int ttH;

- static int ttRadius;

- static ChartNode ttNode;

- static int ttA0;

- static int ttA1;

- static int ttDepth;

- static ChartNode ttSunNode;

- static ChartView Of(ChartOption o)
  - 绑定一个选项（内部深复制为 initialOption 供 Restore 用），
    动画/交互键取新 WidgetId。

- static ChartView Keyed(ChartOption o, int key)
  - 绑定一个选项及调用方所有的稳定动画键。

- static ChartView KeyedStatic(ChartOption o, int key)
  - 静态首绘的 Keyed 变体：跳过增长入场动画，首帧即最终
    形态（对齐 ECharts 官方示例站的静态示例）。文档预览、
    虚拟化单元格与滚动路径上的图表用它，避免卡片滚入视口时
    入场动画触发数百毫秒的连续重绘突发。

- static ChartView Bind(ChartController controller)
  - 将 ChartView 绑定到可变 controller。Render 时读取 controller 的当前 option。

- static ChartView BindKeyed(ChartController controller, int key)
  - 带稳定交互键的 controller 绑定，适合列表和虚拟化单元格。

- ChartView OnRendered(Action a)
  - 生命周期事件：在保留的 ChartView 实例上订阅。

- ChartView OnResize(Action a)
  - 尺寸回调：Render 帧检测到本图表宽高变化时触发。

- ChartView OnUpdated(Action a)
  - 更新回调：Render 帧检测到 option/数据版本变化时触发。

- ChartView OnDisposed(Action a)
  - 释放回调：Dispose 时触发一次，随后清空全部回调列表。

- ChartView On(ChartEventType type, ChartInteractionHandler handler)
  - 注册/移除带载荷的图表交互事件。

- ChartView Off(ChartEventType type, ChartInteractionHandler handler)
  - 注销一个交互事件处理器（按引用匹配最近一个；disposed 后 no-op）。

- ChartView ClearEvents()
  - 注销全部交互事件处理器；disposed 后为 no-op。返回 this 便于链式。

- void RaiseInteraction(ChartInteractionEvent eventArgs)
  - 派发交互事件：先发给自身 eventHub 订阅者，controller 绑定
    模式下再转发给 controller（DataChanged 除外，避免回环）。

- void RaiseLocal(ChartInteractionEvent eventArgs)
  - 只派发给自身 eventHub，不转发 controller（本地回声用）。

- static void RaiseActive(ChartInteractionEvent eventArgs)
  - 渲染器侧事件出口：转发给当前帧的 activeEventView
    （即时模式渲染器没有 view 引用时使用）。

- static ChartInteractionEvent EventAt(ChartEventType type, int wid, int px, int py)
  - 构造仅带类型/wid/像素坐标的图表级事件载荷。

- static ChartInteractionEvent EventFromHit(ChartEventType type, int wid, ChartHit hit)
  - 由命中结果构造数据点事件载荷；hit 为 null 时退化为
    Of(type, wid)（图表级事件）。

- static void OfferActiveHit(ChartHit hit)
  - 当前帧由 renderer 提供的命中候选。renderer 按绘制顺序调用，
    后来的具体图元覆盖早先的候选，但不会产生额外事件。

- static bool HoverBlocked(App app)
  - 指针被上层弹层/抽屉/遮罩接管时，图表悬停命中整体静默：
    命中点的 tooltip 卡在 PresentFrame 末尾统一绘制，会叠到
    弹层上面（悬停穿透）。入口在此统一拦截，各 Offer*/PointsHover
    无需重复判断。

- static void OfferTopmostCategoryHit(ChartHit hit)
  - 混合 Cartesian 图在渲染结束后才复算部分 overlay 命中。
    系列索引与主体绘制顺序一致：后面的系列视觉上覆盖前面的
    系列；较早系列的延迟命中不能反过来遮掉已经命中的后层。

- static ChartHit MakeDataHit(ChartSeries s, int seriesIndex, int dataIndex, string fallbackName, ChartElementType elementType, int px, int py, int value)
  - 构造数据点命中：数据项名取 s.data[dataIndex].name（无则用
    fallbackName），并携带 number 值与系列 axisIndex。
    s 为 null 时返回 null。

- static void OfferCategoryPointHits(App app, ChartFrame f, List<string> labels, List<ChartSeries> series, int baseIdx, int g, ChartElementType elementType, bool forceTopmost)
  - 折线数据点的 proximity 命中：在绘图区内找最近可见 Line
    系列点（命中半径 Scale(10)），命中后经 OfferActiveHit /
    OfferTopmostCategoryHit 提交。baseIdx 为 dataZoom 窗口基址。

- static bool HasInteraction(ChartView v, ChartEventType type)
  - 该图（自身 hub 或其 controller）是否订阅了 type 事件。

- static bool OwnsActiveClick(App app, int id)
  - id 是否属于当前 activeEventView 的可点击命中（id < 0 恒假）；
    渲染器用它仲裁扇区/区域点击归属。

- void DispatchPointerEvents(App app, int x, int y, int w, int h, string statusNow)
  - 帧尾指针事件派发：进入/离开、Hover/MouseOut（命中变化时）、
    Click/DoubleClick（经 eventHitId），随后清空 activeEventView。
    statusNow != "ready" 时不产生指针事件。

- ChartView OnClick(ChartInteractionHandler handler)
  - 按事件类型注册交互处理器（Click/Hover/LegendSelected/…），
    组文档覆盖以下 17 个链式方法，各自对应一个 ChartEventType。

- ChartView OnDoubleClick(ChartInteractionHandler handler)
  - 注册 DoubleClick 交互事件：双击时派发，命中元素或整图坐标。

- ChartView OnHover(ChartInteractionHandler handler)
  - 注册 Hover 交互事件：指针悬停时派发，命中元素或整图坐标。

- ChartView OnMouseOut(ChartInteractionHandler handler)
  - 注册 MouseOut 交互事件：指针移出上一命中元素时派发。

- ChartView OnLegendSelected(ChartInteractionHandler handler)
  - 注册 LegendSelected 交互事件：图例项被选中。

- ChartView OnPieSelected(ChartInteractionHandler handler)
  - 注册 PieSelected 交互事件：饼图扇区被选中。

- ChartView OnMapSelected(ChartInteractionHandler handler)
  - 注册 MapSelected 交互事件：地图区域被选中。

- ChartView OnMapRoam(ChartInteractionHandler handler)
  - 注册 MapRoam 交互事件：地图漫游（平移/缩放）。

- ChartView OnTimelineChanged(ChartInteractionHandler handler)
  - 注册 TimelineChanged 交互事件：时间轴播放位置切换。

- ChartView OnMagicTypeChanged(ChartInteractionHandler handler)
  - 注册 MagicTypeChanged 交互事件：magic type 切换。

- ChartView OnRefresh(ChartInteractionHandler handler)
  - 注册 Refresh 交互事件。

- ChartView OnForceLayoutEnd(ChartInteractionHandler handler)
  - 注册 ForceLayoutEnd 交互事件：力导向布局收敛结束。

- ChartView OnDataZoom(ChartInteractionHandler handler)
  - 注册 DataZoom 交互事件：缩放区间变化，事件携带 zoomStart/zoomEnd。

- ChartView OnDataRange(ChartInteractionHandler handler)
  - 注册 DataRange 交互事件：数据区间选择变化。

- ChartView OnRestore(ChartInteractionHandler handler)
  - 注册 Restore 交互事件：还原初始 option 时派发。

- ChartView OnResizeEvent(ChartInteractionHandler handler)
  - 注册 Resize 交互事件：图表尺寸变化，事件携带新宽高。

- ChartView OnDataChanged(ChartInteractionHandler handler)
  - 注册 DataChanged 交互事件：option/数据版本变化时派发。

- ChartOption GetOption()
  - 返回 option 快照；controller 绑定和直接 option 两种模式都不暴露
    内部可变对象。

- string Status()
  - 状态字符串："ready" / "loading" / "empty" / "error" /
    "disposed"（controller 绑定模式透传 controller 状态）。

- string StatusMessage()
  - 伴随状态的补充消息（SetEmptyMessage/SetErrorMessage 等设置）。

- bool IsDisposed()
  - 实例是否已释放（Dispose 后为真；disposed 后所有操作为 no-op）。

- ChartView SetOption(ChartOption next)
  - 替换 option；绑定 controller 时保留 controller 身份。

- ChartView Refresh()
  - 立即模式的显式刷新入口。Render 每帧都会读取最新 option，
    因此这里仅提供与 ECharts refresh() 对齐的可链式语义。

- ChartView Restore()
  - 还原为创建/最近一次 SetOption 时的 initialOption 深拷贝，
    并触发 Restore 事件（controller 模式转发 controller.Restore）。

- ChartView Clear()
  - 清空所有系列的 data 列表并把状态置 "empty"（不销毁系列外壳）。

- ChartView ShowLoading(string message)
  - 置 "loading" 状态并显示 message（Render 时由状态层覆盖呈现）。

- ChartView HideLoading()
  - 结束 loading，恢复 "ready"。

- ChartView SetEmptyMessage(string message)
  - 置 "empty" 状态并自定义空态文案。

- ChartView SetErrorMessage(string message)
  - 置 "error" 状态并自定义错误文案。

- void Dispose()
  - 释放 view 的事件订阅并使后续 Render/操作失效。
    controller 的生命周期由创建它的调用方拥有，view 不会替其 Dispose。

- static int cacheSeq=16;
  - RenderCached 的动态快照槽位分配器：运行时池按需增长
    （ZAN_SNAP_CACHE_MAX_SLOTS = 512），任意数量的缓存
    图表可以共存；将图表嵌入会滚走的单元格的调用方
    应 ReleaseCached(slot) 归还像素缓冲区。

- static int AllocCacheSlot()
  - 分配下一个快照槽位（16..511 循环复用，不做占用检查）。

- static void ReleaseCached(Canvas c, int slot)
  - 释放 RenderCached 槽位拥有的像素缓冲区（在区域
    离开视口时调用，如网格单元格滚走）。槽位稍后
    可复用——指纹键按槽位区分，过期的快照
    直接失配并重新渲染。

- static bool RenderCached(App app, ChartOption o, int slot, int x, int y, int w, int h)
  - 静态且光栅化成本高的图表的缓存区域渲染（热力图、
    密集系列）：首次调用把最终形态（关闭动画）绘制进
    快照槽位 0-7 并记录数据指纹；后续调用以单次拷贝
    恢复缓存像素而非重新光栅化，
    因此 100x50 热力图每帧成本为 O(区域) 而非 O(单元格)。
    缓存对任何数据 / 可见性 / 缩放 / 主题 /
    几何变化自动失效（指纹比较 + 几何匹配）。
    悬停反馈（如 HeatmapHover）由调用方在命中*之后*绘制，
    使工具提示保持活跃。帧由缓存提供时返回 true。
    交互事件由每槽位的持久 owner view 承载：缓存命中帧也
    设置 activeEventView 并派发 Hover/MouseOut/Click/
    DoubleClick，调用方补画的命中层（HeatmapHover 等）的
    OfferActiveHit 由此到达持久 view，handler 不再丢失。

- static List<ChartView> cachedOwners;
  - RenderCached 每槽位的持久 owner view。Keyed 临时实例在
    缓存 miss 帧产生，这里把它保留下来：后续缓存命中帧复用
    同一实例，previousHit 连续性与事件订阅归属由此成立。
    平行数组按槽位序存放（slot 数量少且有限）。

- static List<int> cachedOwnerKeys;

- static List<int> cachedOwnerRects;

- static void SetCachedOwner(int key, ChartView v, int x, int y, int w, int h)
  - 登记 key（zwid）对应的持久 owner view 及其矩形
    （平行数组按 key 首次出现顺序存放；重复 key 原位更新）。

- static ChartView CachedOwner(ChartOption o, int key, int x, int y, int w, int h)
  - 取 key 的持久 owner view 并刷新其缓存矩形；不存在或已
    disposed 时现建一个 Keyed view 并登记返回。

- void BeginCachedEventFrame(App app, int x, int y, int w, int h)
  - 缓存命中帧的事件帧开销等价于 Render 的尾部：注册根命中
    区、设置 activeEventView，由调用方补画的命中层填
    currentHit，最后统一派发。像素不被触碰——快照已经恢复。

- static int CacheFingerprint(App app, ChartOption o, ResolvedChart resolved, int x, int y, int w, int h)
  - RenderCached 的数据指纹：系列值 + 类型/轴/隐藏、
    dataZoom 窗口、当前主题，以及全部专用数据
    （links/tree/points/candles/bubbles/boxes/errors/events/
    regions/marks/gauge/radarMax）。任何会改变
    像素的因素都使缓存快照失效；悬停位置刻意不
    不（悬停层在缓存命中后绘制于其上）。

- static int FoldStr(int h, string s, int seed)
  - 把字符串内容折叠进指纹。Zan 没有 char 值类型，但
    s[i] 给出字符编码（UTF-8 字节）；逐字节折叠使长度相同、
    内容不同的标签/名称折叠出不同值，避免陈旧缓存。
    空串返回 h 原值。

- static int FingerprintCore(int themeGen, int zoomLo, int zoomHi, ChartOption o, ResolvedChart resolved)
  - 指纹的纯核心。主题代（themeGen）与 dataZoom 状态
    （zoomLo/zoomHi）作为整数注入，使 conformance 测试
    无需 App 即可验证数据/可见性/主题/缩放变化都会改变指纹；
    CacheFingerprint 从 App 读取这两个状态，语义与旧版完全一致。

- static ChartSeries LeadSeries(ChartOption o)
  - 第一个可见序列（整图系列族从中选取布局
    标志位 —— innerPct、roseType、sort、hbar、custom）。

- static int LeadSeriesIndex(ChartOption o)
  - 第一个可见系列的下标；全部隐藏时返回 0，无系列返回 -1。

- static int SeriesIndexOf(ChartOption o, ChartSeries target)
  - target 系列在 o.series 中的下标（引用相等）；无则 -1。

- static ChartType LeadType(ChartOption o)
  - 主导图表族：第一个可见序列的类型（
    整图系列族 —— pie、gauge、heatmap 等 —— 从中选择布局，
    笛卡尔系列族则逐序列混用）。全部隐藏时仍用首条系列类型，
    保留坐标轴/图例，而不是整图变成空状态。

- static string DispatchKind(ChartOption o)
  - 渲染器分发键：每个 ChartType 和 custom kind 都映射到
    一个显式渲染器；没有未知类型回退为折线图。
    未知/空 kind 返回 "empty"（渲染明确的空状态）。
    这是 chart_kinds_complete 测试的确定性锚点。

- static void DrawEmptyState(App app, int x, int y, int w, int h, ChartOption o)
  - 未知 / 空 kind 的明确空状态：不绘制错误的图表。

- static void DrawStatusState(App app, int x, int y, int w, int h, string status, string message)
  - 非.ready 状态的整面覆盖绘制（loading/empty/error 文案；
    "ready" 为空操作）。

- static bool HasArea(ChartOption o)
  - 任一序列为面积线时返回 true（对应 ECharts line.areaStyle.show）。

- static bool IsLineFamily(ChartType t)
  - 折线族类型以折线绘制（可选填充 / 阶梯 /
    堆叠 —— 目前均为 Line 类型；它们是序列的子实体）。

- static bool IsBarFamily(ChartType t)
  - 柱状族类型占据一个柱位（分组 / 堆叠 / 水平）。

- static int GroupIndex(List<string> groups, string name)
  - 堆叠组名称的索引，无则 -1（柱状图按 stackName 分组）。

- void Render(App app, int x, int y, int w, int h)
  - 每帧渲染入口：解析 option（ResolvedChart）、按需播放入场
    动画（AnimIntroIn，键 5000000+wid；map/heatmap/wordCloud/
    force/treemap 恒静态）、分发渲染器、画工具箱/状态层/dataRange，
    并派发指针交互与 Rendered/Resized/Updated/DataChanged 事件。

- static int ConnectedWid(App app, int wid, int group)
  - connect() 组交互键重定向：组内第一张到达的图把「组长 wid」
    记到组登记键（ConnectGroupKey(groupId)），组内所有图（含
    组长自己）的交互态键都以组长 wid 为基——任意一张图里改的
    dataZoom 窗口/图例开关/悬停类别，组内其余图同帧读到。
    未入组（group == 0）返回图自己的 wid（无联动）。
    主路径在 ResolvedChart.Resolve（stateWid）；此处保留给无
    Resolve 的轻量调用方。

- static void ApplyMagic(ChartOption o, int magic)
  - 工具箱「魔法类型」落地：magic 1/2 把全部 Line/Bar 系列的
    type 就地改为 Line/Bar（切柱状时关掉 areaStyle）；其余值
    空操作。

- void DispatchRender(App app, int x, int y, int w, int h, int g)
  - 显式分发：每个 kind 都有一个明确的分支。没有未知
    kind 回退为折线图；未知/空 kind 绘制明确空状态。

- static void RenderOnce(App app, int x, int y, int w, int h, ChartOption option, int g)
  - 分发链本体：DispatchRender 与多 grid 子面板共用（子 option
    的 kind 按组内系列重算，蜡烛+成交量、行/列布局混排各自
    落到正确的渲染器）。

- static void DrawOverlaySeries(App app, int x, int y, int w, int h, ChartOption o, int g, string kind)
  - 混搭覆盖层：把与面板主导类型不同的 pie/gauge/funnel 系列
    逐条再画一遍。覆盖层 option 置 overlay=true（渲染器跳过
    面板底/头），交互键沿用 o.iwid（悬停/命中与整板一致）。


## ChartView (class)

- static void DrawBars(App app, int x, int y, int w, int h, ChartOption o, int g, bool stacked, bool horizontal)
  - 柱状图渲染入口：分组 / 堆叠（stacked）/ 水平（horizontal，
    委托 HBarCore）三种形态，可混入折线与散点覆盖层；含
    dataZoom 窗口、barWidth/barGapPct/showBackground、负值柱、
    markPoint/markLine、typed 命中与笛卡尔 tooltip。

- static void DrawValueXBars(App app, ChartFrame f, ChartSeries s, int si, int i0, int i1, int g, ChartOption o)
  - 双数值轴柱形（ECharts bar13）：points[i] = (x, y)。默认竖柱
    画在 x 值处、从零线长到 y（宽取相邻 x 间隙或量程 1/4，数值
    标签在柱顶/柱底）；barHeight>0 时为横条——厚度 = barHeight px、
    垂直中心在 y 值处、从 x=0 基线长到 x 值（官方 _buildOther
    barHeight 横向分支：value[0]>0 向左铺、<0 向右铺）。悬停
    命中出 tooltip。

- static void BarCell(Canvas c, int x, int y, int w, int h, int rad, int color, bool gradient)
  - 单个柱格，可选垂直渐变（color -> 更浅）。

- static void BarCellR4(Canvas c, int x, int y, int w, int h, List<int> r4, int radDef, int color, bool gradient)
  - 带四角独立圆角的柱格（itemStyle.borderRadius）。渐变路径
    退化为统一半径；实色路径先整块圆角矩形再补平方角。

- static ChartFrame HBarCore(App app, int x, int y, int w, int h, ChartOption o, List<string> labels, List<ChartSeries> series, bool stacked, int g, int baseIdx)
  - 水平柱状图：类别在左纵排，数值横伸。stacked 为 true 时，
    共享 stackName 的序列每组堆成一条水平色带
    （对应 ECharts stacked bar4），各行上下排列各组。
    含负值时从零轴左右展开（旋风 / 人口金字塔）。
    `g` 为动画因子（柱长乘 g，轴范围用最终值）；`baseIdx` 是
    labels[0] 对应的数据索引（dataZoom 窗口起点）。绘图区几何
    以 ChartFrame 返回，供调用方画缩放滑块。

- static void DrawWaterfall(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 瀑布图渲染入口：首系列逐项累计（name == "total" 的项画为
    从 0 到当前累计的总计柱），增/减/总计三色 + 阶间连接线 +
    tooltip；累计在整个数据上算完后再按 dataZoom 窗口切片。


## ChartView (class)

- static int EventRiverWaveAmp(int height)
  - 事件带波浪振幅：height/5，钳在 [1, height/2]；h < 2 时
    无波浪（返回 0）。

- static int EventRiverColorIndex(List<string> names, string name)
  - bands 按时间排序后，不能再用 band 下标取色；否则输入
    未按时间升序时图例与实际事件带会交换颜色。按图例去重
    顺序映射名称，保证图例、带和 tooltip 共用稳定色彩身份。

- static void DrawEventRiver(App app, int x, int y, int w, int h, ChartOption o, int g)
  - Event River 渲染入口：events 经 EventRiverLayout 按时间
    布局成堆叠波浪带，从左向右按 g 揭示；右侧去重图例（上限
    8 条）与时间轴端点标签；带矩形命中（EventBand 事件，
    dataIndex 用排序前的源 events 下标）+ tooltip。


## ChartView (class)

- static int FinanceRevealAlpha(int progress)
  - 入场进度（0..1000，越界钳制）换算为 0..255 的透明度，
    金融族各渲染器按 g 渐显时共用。

- static void DrawCandles(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 蜡烛图渲染入口：series[0].candles 只绘 dataZoom 窗口
    [i0,i1]；ECharts 2.x K 线语义逐根绘制（44 根以内不分桶）：
    2px 影线 high→low 走边框色（lineStyle.color/color0），实体
    实心填充（itemStyle.normal.color/color0）+ 边框，body 宽 =
    槽宽一半（barMaxWidth 20 缺省封顶）。首根逐项 itemStyle 覆盖
    （k1 蓝色阴线）。markPoint 在窗口最高价定位 teal 气球徽标。
    量程走 valueAxis scale:true + boundaryGap[0.01] 的 smartSteps
    紧致包络（2200..2450，非零锚定）。大数据（>44 根可见）仍分
    桶（每桶首开/末收/最高/最低）。折线族覆盖层（如 MA）共用价
    格轴。命中为 Candlestick 事件（dataIndex = 桶首源下标）+
    OHLC tooltip 与十字光标。

- static void CandleMarkPin(App app, Canvas c, int lx, int ly, int rad, int col, string lbl, int mFs, ChartFrame f)
  - 蜡烛 markPoint 的徽标：ECharts2 pin 气球，几何按参照站 k1
    像素实测锚定——气球头（宽 ≈ symbolSize，圆心在数据点上方
    3px）在上，细尾从气球顶上收窄到数据点上方 17px 的尖端；
    数值标签（如 "2444.8"）以系列色画在尾尖上方的空白处。

- static void DrawBubbles(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 加权散点/气泡图渲染入口：Bubble(x, y, weight)，半径 =
    ISqrt(weight) * maxR / ISqrt(最大 weight)，随 g 从 0 放大。
    轴范围取窗口内数据最大值经 NiceMax，xAxes/yAxes 的
    min/max（非 Auto）可覆盖；支持 dataZoom。命中取半径
    +2px 内最近的气泡（ScatterPoint 事件，携带 x/y 值）+
    x/y/w tooltip。

- static List<string> BoxLabels(List<BoxItem> items)
  - 箱线图底轴标签：逐 BoxItem 取 label。

- static List<string> ErrorLabels(List<ErrorItem> items)
  - 误差棒底轴标签：逐 ErrorItem 取 label。

- static void DrawBox(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 箱线图渲染入口：收集全部 custom=="box" 系列（dataset
    boxplot 变换的绑定产物）。单系列逐类别取调色板，多系列
    逐系列取色在类目格内分槽；yAxis category 时横排（轴互换，
    velocity2 / data-transform-aggregate）。dataset 绑定的散点
    系列（离群点/聚合明细）按点叠加圆点。yAxis/xAxis 显式
    min/max 钉值域（boxplot-multi 的 -400..600）。命中为
    BoxPlot 事件 + min/Q1/med/Q3/max tooltip。

- static void BoxTooltip(App app, ChartOption o, List<ChartSeries> bxs, int k, int s, int mx, int my)
  - 箱线 tooltip：标题取类目标签（空回落 "Service N"），五行
    min/Q1/med/Q3/max 取命中系列的箱。

- static void DrawBoxOverlay(App app, ChartOption o, int lo, int hi, int n, bool horiz, int pX, int pY, int pW, int pH, int rowH, int revealAlpha)
  - 箱线叠加散点（dataset 绑定的离群点/聚合明细系列）：类目侧
    序号定位行/列，数值侧定值；半径取 series.symbolSize 的一半
    （缺省 2pt），色取系列色（缺省调色板顺位）。

- static void DrawError(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 误差棒渲染入口：series[0].errors 逐类别画值点、±err 竖
    线与端帽（数值随 g 揭示），点间连成折线；颜色取 chart
    accent 样式，series[0].color 非 0 时覆盖。命中为 ErrorBar
    事件（value = y）+ "y ± err" tooltip（标题取 x 轴类别，
    空时回落 "Item N"）。


## ChartView (class)

- static void DrawHeatmap(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 热力图入口：同帧先画主体 DrawHeatmapCore，再画悬停
    覆盖层 HeatmapHover（Core 可被缓存，命中提示始终实时）。

- static int HeatmapCellStart(int dimension, int index, int count)
  - 网格每列/行的累计像素边界。与 CatLeft 同样使用整数
    累计除法，余数落在末端而不是被固定 cell 尺寸吞掉。

- static int HeatmapCellSize(int dimension, int index, int count)
  - 第 index 行/列的像素厚度（HeatmapCellStart(index+1) -
    HeatmapCellStart(index)）。

- static int HeatmapIndexAt(int q, int dimension, int count)
  - q 是相对网格左/上缘的像素坐标，按累计边界反解类目。

- static void DrawHeatmapCore(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 仅热力图主体（面板、表头、色块）—— 不含悬停覆盖层，
    以便 RenderCached 缓存，指针反馈在
    缓存命中后重绘于其上。

- static void HeatmapHover(App app, int x, int y, int w, int h, ChartOption o)
  - 热力图悬停覆盖层：高亮指针下的单元格并
    显示其值。在 DrawHeatmapCore（或 RenderCached
    恢复）之后绘制，缓存主体在鼠标移动时无需重绘。


## ChartView (class)

- static string TreeNodeName(ChartNode n)
  - 节点安全名（null → ""）。

- static int TreeChildCount(ChartNode n)
  - 直接子节点数（null → 0）。

- static int TreemapValue(ChartNode n)
  - Treemap 面积只接受正值（负值/零值不占像素）；有子节点时取
    子树累计和，且累计和饱和到 int 上限，避免异常输入把布局
    边界推进到负数或溢出。

- static int TreemapTotal(List<ChartNode> nodes)
  - 同层节点列表的 TreemapValue 总和（饱和）。

- static int TreemapAdd(int left, int right)
  - 饱和加法：负数钳 0，溢出饱和 int 上限。

- static void DrawTreemap(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 矩形树图（treemap）绘制入口：面积按 TreemapValue 分配，
    交替方向递归切片；支持 hover tooltip 与 Node 点击事件。
    `g` 为出现动画进度（千分值 0..1000）。

- static void TreemapSlice(App app, int x, int y, int w, int h, List<ChartNode> nodes, int depth)
  - 一层分割；单元格足够大时递归进子节点，
    否则以名称 + 值标记该单元格。偶数层竖切、奇数层横切。

- static void TreemapCell(App app, int x, int y, int w, int h, string name, string val)
  - 矩形树图单元格内的名称（+ 值）标签，仅放得下时绘制，
    并用单元格矩形裁剪，避免长名称画出格子。

- static int TreeDepth(ChartNode n)
  - ---- 旭日图（同心环；最内环 = 根的子节点） ----

- static int SunburstRingCount(ChartNode root)
  - 旭日图实际绘制的环数 = 根到叶的父子边数（根节点本身
    不占一圈）；因此 root->leaf 应为 1 圈，而不是 TreeDepth=2
    再额外除以一圈，造成外径只到 rMax/3。

- static int SunburstRingHeight(int rMax, int rings)
  - 每环厚度：rMax 均分给 rings 环（至少 1px）。

- static int TreemapCornerRadius(int depth, int scale)
  - 单元格圆角半径：外层格 4、内层格 2（乘 scale）。

- static int TreeNodeCount(ChartNode n)
  - 子树节点总数（含根）。

- static int TreeNodeIndex(ChartNode root, ChartNode target)
  - 稳定 preorder 下标供 Tree/Treemap 的 dataIndex 使用；节点对象
    没有独立 id，因此不能使用每帧重新分配的命中句柄。
    不在子树内返回 -1。

- static bool TreeRoamEnabled(bool roam)
  - 树图漫游开关（o.roam 透传；独立 seam 便于测试）。

- static int TreeHitRadius(int radius, int zoom, int scale)
  - 节点命中热区半径：补固定可访问性余量；zoom < 50 时减半，
    不能随 zoom 无限扩大，否则空白或相邻节点会被远距离圆点吞掉。

- static bool TreemapContains(int px, int py, int x, int y, int w, int h, int radius)
  - 圆角矩形包含测试（含圆角处精确判定），treemap 命中用。

- static int TreemapSliceStart(int dimension, int prefix, int total)
  - 按累计值计算像素边界；绘制和命中必须使用同一组边界，
    避免逐项 floor 后在最后一列/最后一行留下不可命中的空带。

- static int TreemapSliceEnd(int dimension, int prefix, int value, int total)
  - 切片末端像素 = Start(prefix+value)，与 Start 同界。

- static int TreemapSliceSize(int dimension, int prefix, int value, int total)
  - 切片厚度 = End - Start（恒非负）。

- static void TreemapHit(App app, int x, int y, int w, int h, List<ChartNode> nodes, int depth, int px, int py)
  - 矩形树图命中测试：按 TreemapSlice 相同的切片布局遍历，
    仅当指针位于子单元格内（且深度足够
    被分割）时才递归。填充静态命中字段 ttName/ttVal。

- static int SunburstVisibleEnd(int rawEnd, int sweepMax)
  - 旭日图可见扫掠末端：rawEnd 裁到 sweepMax（rawEnd < 0 = 完整圆）。

- static void SunburstHit(App app, int cx, int cy, int ringH, ChartNode node, int depth, int a0, int a1, int sweepMax, int px, int py)
  - 旭日图环形命中测试：按 SunburstRing 相同的角扫掠遍历，
    指针位于子扇形内时递归。填充静态命中字段 ttName/ttVal
    （角度命中不做半径早退，否则内环会挡住所有外环指针）。

- static void DrawSunburst(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 旭日图绘制入口：同心环自内向外，环厚均分；中心标签为根名。
    支持 hover 高亮 + tooltip + Node 点击事件。`g` 为出现动画
    进度（千分值 0..1000，映射扫掠角）。

- static void SunburstRing(App app, int cx, int cy, int ringH, ChartNode node, int depth, int a0, int a1, int sweepMax, int parentCol)
  - 递归绘制一层旭日环：子扇区按子树 Total() 分配父扇区角度，
    颜色向父色向白色插值区分层级。

- static int SankeyIndexOf(List<SankeyNodeLayout> nodes, string name)
  - ---- 桑基图（分层节点间的流量连线） ----

- static int SankeyRevealAlpha(int progress)
  - 出现动画进度（0..1000）→ 连线/节点 alpha（0..255）。

- static void DrawSankey(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 桑基图（sankey）绘制入口：links 驱动，最长路径分层（松弛
    最多 n-1 轮 + 回边压平，循环图布局稳定终止）。节点高度按
    max(入, 出) 流量分配；连线按流量定宽，支持连线 hover
    tooltip（Link 事件）。`g` 为出现动画进度（0..1000 → alpha）。

- static int TreeLeafCount(ChartNode n)
  - 节点下的叶子槽位数（一个叶子 = 1 个槽位）。

- static void TreeAssign(ChartNode n, int lo, int depth, List<TreeLayoutNode> layout)
  - 为每个节点分配 span 坐标：节点跨越叶子 [lo, hi)，
    其中心位于该叶子范围中点。span 在垂直树中
    从左到右，在水平树中从上到下。

- static int TreeSpan(TreeLayoutNode node, int spanG, int leaves)
  - 布局节点在增长缩放后的 span 上叶子范围的中心。

- static int TreeLabelWidth(ChartNode n, int fs)
  - 子树中最宽节点标签（像素），预留树图 span 间距用。

- static void TreeEdgePoints(List<int> xs, List<int> ys, int p0, int p1, int q0, int q1, bool horiz, string type)
  - 树图父子边折线点集（屏幕坐标）：type 语义同 ECharts2
    lineStyle.type——""/"broken" 三段直角、solid 直线、curve
    三次贝塞尔（控制点在深度中点，12 段采样）、dashed/dotted
    直角折线（虚线由调用方 DrawDashed 实现）。

- static bool WordCloudFits(List<WordCloudItem> placed, int x, int y, int w, int h)
  - 词云放置尝试：矩形 (x,y,w,h) 与已放置词条是否都不相交。

- static void DrawWordCloud(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 词云（wordCloud）绘制入口：放置结果按内容指纹缓存（每帧
    重建 option 不重算布局）；字号按权重、放不下自动缩小。
    支持 hover tooltip + WordTag 点击事件。`g` 为出现动画进度。

- static List<WordCloudItem> PlaceWordCloud(App app, Theme t, List<ChartData> src, int aw, int ah, int minFs, int maxFs, int maxV, bool vary, string rotList)
  - 阿基米德螺旋放置：字号按权重，放不下就缩小，坐标相对绘图区。
    vary 为真时奇数词条旋转 90°（ECharts wordCloud rotateRange
    的 0/90 两态）；rotList 非空时按词条序号对角度集取模轮转
    （ECharts textRotation 数组的确定性取法——随机/任意角度会破坏
    布局缓存与截图回归，角度仍限于 ±90 内由 DrawTextRot 支持）。
    旋转项的包围盒按 |sin|/|cos| 投影计算（非 90° 角不再简单交换
    宽高），碰撞检测与裁剪都用包围盒。

- static int WordCloudFingerprint(List<ChartData> data, int aw, int ah, int minFs, int maxFs, int rotate)
  - 词云内容指纹（词条 + 盒子几何 + 旋转模式）：布局缓存键，
    必须覆盖所有影响放置结果的输入。

- static int WordCloudRotListKey(string rotList)
  - 自定义角度集的指纹成分："0,45,-45" → 稳定小整数（空串 = 0）。

- static List<WordCloudCacheEntry> wcCache;
  - 词云布局缓存：指纹 → 放置结果（小容量，见 WordCloudCacheEntry）。

- static int TreeGridFirst(int origin, int view0, int gs)
  - 无限画布网格：世界原点落在视口 (ax - panX, ay - panY)，
    间距随缩放变稀/变密，密到看不清时跳级。
    无限画布网格第一根线：从世界坐标原点向视口 [view0, view0+…)
    对齐的最近网格线。

- static void DrawTreeCanvasGrid(App app, Canvas c, int ax, int ay, int aw, int ah, int panX, int panY, int zoom)
  - 画无限画布网格：世界原点落在视口 (ax - panX, ay - panY)，
    间距随缩放变稀/变密，密到看不清时跳级。

- static void DrawTree(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 树形图（tree）绘制入口：ECharts type 'tree' 的分层节点连接
    图。roam 开启时滚轮缩放（CaptureWheel 仲裁防外层滚动打架）
    + 拖拽平移，首帧自动适配整树；无限画布网格背景。支持
    hover tooltip + Node 点击（拖拽超过阈值时吞掉 click）。


## ChartView (class)

- static void BuildPath(List<int> px, List<int> py, bool smooth, List<int> ox, List<int> oy)
  - 把原始点展开为密集折线（直线穿过，或
    Catmull-Rom 曲线）。填充与描边共用同一路径，
    使填充区域的顶边与轮廓走完全相同的曲线
    （平滑描边与直线段填充之间无缝隙）。

- static void BuildPathFx(List<int> px, List<int> py, bool smooth, List<int> ox, List<int> oy)
  - 同一条平滑曲线（单调三次 Hermite，见 BuildPathFxEx），但
    输出顶点为 16.8 定点数（1/256 px）。整数运算会把每个顶点
    截断到像素网格；平缓曲线上相邻顶点会相差 0 或 1 行，
    使曲线退化为平直段 + 单像素跳变，任何抗锯齿渐变都掩盖不了
    （这就是按真实几何采样的圆看起来平滑、
    而折线曲线呈阶梯状的原因）。亚像素顶点
    让描边光栅化器能采样到真实曲线的距离。
    输入顶点既可以是整数像素（x 常规情形），也可以是已经
    16.8 定点的坐标（堆叠面积带边界 y 来自 YOfFx）——
    直线透传分支统一 ×256 会把定点输入放大 256 倍，因此
    用 inFx 标志区分：定点输入直线段原样透传，曲线插值
    本来就在 1/256 域内进行，两种输入自然一致。

- static void BuildPathFxEx(List<int> px, List<int> py, bool smooth, bool inFx, List<int> ox, List<int> oy)
  - BuildPathFx 的显式输入精度版本：inFx=true 时输入顶点已是
    16.8 定点数，输出不再二次 ×256。

- static long[]MonoTangents(List<int> v, int n)
  - Fritsch–Carlson 切线（16.8 定点输入，返回 n 条切线）：
    端点取单侧割线；内部割线变号（该点是局部极值）时取 0，
    否则取两侧割线平均并限幅到任一侧割线的 3 倍以内——
    保证每个段内不产生越出两端点的假振荡。

- static void FillUnder(Canvas c, List<int> ox, List<int> oy, int baseY, int color, bool gradient, int topA, int botA)
  - 填充密集（从左到右）路径与 baseY 之间的区域，使
    顶边获得亚像素抗锯齿覆盖率。内部以
    实心 1px 列填充；每列唯一的边界行按
    小数覆盖率混合，使顶部呈现平滑曲线而非阶梯。
    ox/oy 来自 BuildPath 的整数像素路径。平滑路径细分后
    相邻子步可小于 1px，逐子步只画起点列会在跨像素处成片
    跳列（百叶窗条纹）。按像素列双指针推进：每列在路径上
    找到覆盖该列的子步再插值顶边。

- static void FillColumnAA(Canvas c, int px, int yyF, int baseY, int color, bool gradient, int topA, int botA, int solidA)
  - 单个抗锯齿填充列。yyF 是以 1/256 px 表示的小数顶部；
    solidA 是平铺（非渐变）填充的 alpha。

- static void FillBandColumnAA(Canvas c, int px, int topF, int botF, int color, bool gradient, int topA, int botA, int solidA)
  - 堆叠色带的单个抗锯齿列：顶部和底部
    边界都带小数覆盖率。底部被吸附到整像素的色带
    会与下方色带（其顶部自带小数部分）形成阶梯状接缝，
    使两个堆叠颜色之间的接缝参差不齐，
    尽管各自顶边都平滑。对两条边都混合，
    使共享行的两份覆盖率合计为一整行。

- static void FillBandFx(Canvas c, List<int> topX, List<int> topY, List<int> botX, List<int> botY, int color, bool gradient, int topA, int botA, int solidA)
  - 平滑路径经 BuildPathFx 细分成 48 步/段，相邻子步往往不足 1px——
    按子步的半开像素区间 [ceil(ax0/256), ax1/256) 逐段填会整段落空
    （区间为空），表现为平滑堆叠面积只剩描边、带间露出大片背景。
    这里改为双指针整列推进：每个像素列在两条边界路径上各找到
    覆盖该列起点的子步，按列起点插值上下边界，一列不漏。
    solidA 是实色区 alpha：堆叠带用 255（ECharts 2 实色）；
    渐变带传 <255 做半透明衰减。

- static void PolyLine(Canvas c, List<int> px, List<int> py, bool smooth, int color, int th)
  - 折线描边入口：BuildPathFx 亚像素路径交给 DrawPolylineFx。

- static void OfferCategoryOverlayHits(App app, ChartFrame f, List<string> labels, List<ChartSeries> series, int baseIdx, int g)
  - 混合折线图中的柱/散点覆盖层不经过各自主渲染器，
    因此在同一分类槽位复算实际矩形/圆点几何，避免视觉上
    可见却只能收到整图 Click 的错位。

- static void DrawMultiGridPanels(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 多 grid 布局（grid[] ≥ 2）全 kind 通用拆分，由 DispatchRender
    拦截进入：按 series.xAxisIndex 分组，每组在自己的 grid 矩形
    里重入分发链 RenderOnce（组内系列重算 kind——蜡烛+成交量、
    行/列布局混排各归各位）。grid.top/bottom 百分比按面板高定
    位，width/height 形态（scatter-matrix 宫格）同理；标题数组
    （位置为面板百分比）与图例全图各画一次，子调用不再画。

- static int sPanelFg(App app)
  - 面板前景色（标题用，与 DrawPanelI 同源）。

- static void DrawLines(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 折线/面积/阶梯线渲染入口：折线族可平滑/渐变/虚线，可
    混入柱状与散点覆盖层；带 dataZoom 窗口、markPoint/markLine、
    typed 命中与笛卡尔十字线 tooltip。

- static void OfferStackedAreaHits(App app, ChartFrame f, List<string> labels, List<ChartSeries> series, int baseIdx, int g, int maxV)
  - 堆叠面积的可视点位位于累计 top/bottom 带上，而不是原始值
    的 Y。命中沿用绘制时相同的组/序列累加顺序，避免指针落在
    色带上却把事件坐标解析到带外；事件 value 仍保留源项值。

- static void DrawStackedArea(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 堆叠面积图渲染入口：按 stackName 分组自下而上分层
    （组底 = 下方各组的逐类合计），色带亚像素填充 + 顶边
    亚像素描边，可平滑/渐变；命中与 tooltip 与绘制同域。


## ChartView (class)

- static int MapRamp(ChartOption o, int value, int vMin, int vMax)
  - 连续色域：优先 option.rampColors（visualMap）；否则浅蓝 → 深蓝。

- static long FloordivLong(long a, long b)
  - 地图坐标在高 zoom 或大 GeoJSON 数据下可能超过 32 位
    乘法中间范围；除法方向与 Floordiv 保持一致，最终像素
    仍收敛为 int。

- static void FillPolygon(Canvas c, List<ChartMapPoint> poly, int color)
  - 扫描线填充任意多边形（even-odd），逐行生成 span 用 FillRect
    绘制。行 y 半开穿越（与 PointInPoly 同侧判定），交点取在
    像素中心线 y+0.5（2 倍定点）。

- static void PolyOutline(Canvas c, List<ChartMapPoint> poly, int color)
  - 闭合多边形轮廓（DrawPolyline 首尾相接）。

- static void DrawMap(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 地图渲染入口：头部面板 + 可选 visualMap 色条；roam 时处理
    滚轮缩放与拖拽平移（抛 MapRoam）；区域按系列色/MapRamp
    填色（dataRange 过滤灰显），g>=1000 时按指纹快照/恢复像素
    缓存；随后是区域命中、单/多选（抛 MapSelected）、hover
    强调描边、hoverLink 白描边、tooltip 与 markPoint 图钉。

- static int GeoProjectX(MapLayout l, int lngQ)
  - 地图布局 → geo 经纬度（0.01° 定点）的投影换算：lng/lat
    直接线性映射到像素（注册表 GeoJSON 与 geo 系列坐标同为
    未投影的线性度坐标，ECharts 默认投影同为线性）。

- static int GeoProjectY(MapLayout l, int latQ)

- static void DrawGeoOverlay(App app, ChartOption o, MapLayout layout, int plotX, int plotY, int plotW, int plotH, int g)
  - geo 坐标系叠加渲染（DrawMap 末段调用）：逐系列画 lines
    折线（curveness 弯曲 / dotted 虚线）与散点（带名标签）。
    命中经 OfferActiveHit 出 tooltip（silent 系列跳过）。

- static void DrawMapMark(App app, Canvas c, int px, int py, string txt, int fg, int fs, int clipX, int clipY, int clipW, int clipH)
  - 地图/弦图共用的 markPoint 图钉：引线 + 圆点 + 文本，
    文本钳制在绘图区内。


## ChartView (class)

- static int parProgFp;

- static bool parProgHas;

- static int parProgDone;

- static int parProgSlot=-1;

- static bool parProgFresh;

- static int ParHash(int h, int v)

- static void DrawParallel(App app, int x, int y, int w, int h, ChartOption o, int g)

- static int di2(int d, List<int> row, int dims)

- static void DrawThemeRiver(App app, int x, int y, int w, int h, ChartOption o, int g)

- static void DrawLinesCustom(App app, int x, int y, int w, int h, ChartOption o, int g)


## ChartView (class)

- static void DrawPictorialBar(App app, int x, int y, int w, int h, ChartOption o, int g)

- static void Symbol(App app, Canvas c, ChartFrame f, ChartSeries s, int sx, int yBase, int sw, int hVal, int col, int colA, int v)
  - 一个数据槽的符号绘制（模式分派见类注释）。

- static void DrawSource(App app, Canvas c, ChartSeries s, string sym, int dx, int dy, int dw, int dh, int fullH, int col, int colA, bool clip)
  - 符号源分派：内置形状 / path:// 折线仿射 / image:// 位图。
    fullH 仅 clip 模式用（位图裁剪的源窗口比例）。

- static void Poly(Canvas c, int dx, int dy, int dw, int dh, int col, int[]uv)
  - 内置多边形：uv 千分比坐标对仿射到 (dx,dy,dw,dh) 后填充。

- static void DrawPath(Canvas c, string dd, int dx, int dy, int dw, int dh, int colA, int col)
  - path:// 折线化后各向异性仿射进目标盒（ECharts 把 path bbox
    拉到 symbolSize 盒，不保纵横比），随系列色填充、洞回填底色。

- static void DrawImageUri(Canvas c, string uri, int dx, int dy, int dw, int dh, int fullH, bool clip)
  - image://data:...;base64,DATA：解码注册进运行时 mem 图像缓存
    （键 = 数据指纹，逐出后按需重注册），按目标盒缩放；clip 时
    源窗口取位图下部（符号底边贴基线、上沿裁到值高）。

- static int Fingerprint(string data)
  - base64 数据指纹（采样哈希；只为缓存键稳定，不作校验）。

- static byte[]B64Decode(string s)
  - 标准 base64 解码（忽略空白；'=' 截断）。失败返回已解出的
    前缀（调用方以长度门槛兜底）。


## ChartView (class)

- static int PieSelectedOffset(int raw)
  - 计算一个环在当前半径下的实际内外径。绘制、命中和
    emphasis 必须共享这组边界，避免配置内孔被不同路径重复夹取。

- static int ScalarRatioPromille(ChartScalar a, ChartScalar b)
  - 两个同类标量的比值（千分比）：radiusInner/radius 这类比率
    只依赖 amount（percent/percent 或 px/px 均同量纲可除）。

- static bool PieHasEmphasisPaint(int fill, int borderColor, int borderWidth)
  - 是否配置了任何 emphasis paint（填充/边框色/边框宽任一
    非零）；全零时命中不重画高亮。

- static void PieRingBounds(PieLayout layout, int ring, int ringCount, int rOuter, int band, int minGap, out int ri, out int ro)
  - 计算第 ring 环（0 = 最外）的内外径：非最内环 ri = ro - band；
    最内环内孔 = ringInner% × rOuter（0 = 实心，钳到 ro-minGap）；
    结果保证 0 <= ri < ro。绘制与命中必须同用本函数。

- static int PieSliceRo(int ri, int ro, int roseP)
  - 玫瑰图扇区外径：roseP（千分比带内位置）在环内径..环外径间
    内插；非玫瑰（roseP <= 0）直接返回环外径。

- static void DrawPie(App app, int x, int y, int w, int h, ChartOption o, bool sliceLabels, int g)
  - 饼图/环图渲染入口：上方数据图例（LegendSliceKey 可点击
    开关扇区），主体按 PieLayout 扇区绘制（入场扫掠随 g，
    选中/悬停扇区沿中角外偏）；随后是百分比标签/引导线、
    markPoint 极值标注、环图中心标注、扇区命中（PieSelected
    点击 + emphasis 重画）与 tooltip。

- static int GaugeSweep(GaugeOption gauge)
  - 仪表盘扫掠角（度）：start-end 顺时针跨距，非正回绕加 360，
    超过 360 钳为整圈。

- static int GaugeStart(GaugeOption gauge)
  - 仪表盘起始边屏幕角：ECharts 数学角（0=3 点钟逆时针）换算为
    Canvas 顺时针域（90-start），回绕到 [0,360)。

- static int GaugeScalar(App app, ChartScalar scalar, int extent)
  - ChartScalar -> 像素：百分比标量按 extent 取比例，固定值
    标量按 DPI 缩放。

- static int GaugeX(int angle)
  - FillSector 以 12 点钟方向为 0 度并顺时针递增。保持
    仪表盘的矢量几何处于同一坐标系。

- static int GaugeY(int angle)
  - 仪表角（12 点钟为 0°、顺时针递增）的 Y 分量 = -cos(angle)。

- static void GaugeSector(Canvas c, int cx, int cy, int inner, int outer, int start, int sweep, int color)
  - 以 (start, sweep) 画仪表弧段；跨 0° 时拆成两段 FillSector。

- static int GaugeColor(GaugeOption gauge, int perMille)
  - 千分比进度对应的轴带色阶色：取第一个 stop >= perMille 的
    色阶，超出取末档；未配色阶返回 0。

- static int GaugeFont(App app, int requested, int fallback, int radius, int permilleOfRadius)
  - 仪表文字大小：表盘的标签、标题和读数按表盘定尺寸，
    而非窗口。固定 px 字号（ECharts 的 30px detail）只在
    demo 的表盘尺寸下合适 —— 小卡片上同样字号会盖住
    刻度标签并溢出圆弧，这正是此前
    仪表与参照完全不像的原因。`permilleOfRadius` 把
    请求字号限制在半径的一定比例内。

- static void DrawGauge(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 仪表盘渲染入口：每条可见 Gauge 系列一个表盘——轴带色阶
    （随 g 生长）、刻度/分隔线、刻度标签、指针（含阴影）、
    标题与读数（detail 背景/边框、防重叠钳制）；整盘命中
    （Gauge 事件，单数据点语义）+ tooltip。

- static void DrawRadialBars(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 径向柱状图渲染入口：每条系列一个同心进度环（环序自外向
    内），扫掠角 = 值/gaugeMax 并随 g 生长；右侧值图例 +
    环带 hover tooltip。

- static List<ChartStage> GatherStages(App app, List<ChartSeries> series)
  - 收集漏斗/金字塔/玫瑰图各阶段：每阶段一个值+颜色+名称，来源为
    多个单值系列或一个多值系列；隐藏系列/数据项被跳过。

- static void DrawFunnel(App app, int x, int y, int w, int h, ChartOption o, int g, bool pyramid)
  - 漏斗（pyramid=false）/金字塔（pyramid=true，阶段序反转）
    渲染入口：阶段宽度 ∝ 值/maxV，逐行按 1/256 亚像素覆盖率
    画斜边；对齐/层间隙/转化率百分比取首系列配置；右侧可选
    图例；行命中（FunnelStage 事件）+ 横向指示线 + tooltip。

- static string StageName(int i)
  - 阶段缺省名："Stage N"（N 从 1 起）。

- static string FunnelPct(List<ChartStage> stages, int idx)
  - 转化率（ECharts funnel 的逐层转化）：相对上一阶段的百分比
    后缀 " (x%)"；顶层恒 100%；除零返回空串。

- static int DrawStageLegendWrap(App app, ChartOption o, int x, int y, int w, int top)
  - 横向自动换行的阶段图例（多条系列走系列开关，单系列走
    数据项开关），返回图例底部 y（图区顶部）。

- static void DrawStageLegend(App app, ChartOption o, int lx, int ly, int legendW)
  - 漏斗/玫瑰等"阶段图"的图例绘制（单列定宽）。

- static void DrawPieMark(App app, Canvas c, int cx, int cy, int rOuter, int rot, List<PieSlice> slices, int idx, string lbl, Theme t, List<ChartSeries> series)
  - 饼图 markPoint：在扇区中角方向延伸一个标签。线 + 圆 + 文字。
    idx < 0 时不画；与 SliceOutMidAngle 共享角度约定（rot + 中角），
    屏幕位置按数学域 +270° 换算（与 selectOffset 路径同源）。
    扇区静态选中时整体外偏 selectedOffset：引线与标签必须锚在
    偏移后的圆心，否则 mark 点落在与扇区脱开的位置。


## ChartView (class)

- static int RadarAxisMax(List<ChartSeries> series, List<int> radarMax, int j)
  - 雷达图第 j 轴的上限（ECharts radar.indicator.max）：
    radarMax[j] > 0 用显式值，否则从各系列该轴数据推导并取
    友好刻度。纯函数，供 chart_option_behavior 直接断言。

- static int RadarAxisAt(int angle, int n)
  - 指针角度（0=正上，顺时针）映射到最近的雷达轴。
    角度在 0/360 接缝处必须环回到轴 0，不能把四舍五入后的
    n 夹到 n-1，否则正上方左侧的小扇区会显示错误轴数据。

- static int RadarTooltipRadius(int radius, int progress, int tolerance)
  - 雷达图入场动画按数据半径从中心向外展开；tooltip 的可见
    命中域必须跟随同一半径，否则 g=0 时中心外的不可见数据也会
    提前响应。容差只在已有可见半径时生效。

- static void DrawPolar(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 极坐标/雷达图渲染入口：同心环（circle/polygon 两种
    radarShape）+ 可选 splitArea 交替色带 + 轴线与标签；系列画
    闭合多边形（可选 areaStyle 半透明填充与符号点）。轴扇区
    命中（RadarAxis 事件，dataIndex = 轴下标）与 tooltip，命中
    半径跟随入场动画进度。
    option.polars 非空时走多 polar 路径（DrawPolarMulti），
    系列按 polarIndex 分组；空 = 下方单 polar 历史路径原样。

- static void DrawPolarMulti(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 多 polar 路径（ECharts2 polar[] + series.polarIndex）：每个
    坐标系独立画网格/轴线/指示器名，系列按 polarIndex 分组
    各自绑定圆心/半径/轴上限。线型 solid/dashed/dotted 与
    符号形状（含 star5 别名）按系列生效；轴命中与 tooltip
    落到最近的 polar。


## ChartView (class)

- static List<ForceLayoutCache> forceCache;
  - 力导向布局的逐帧记忆化：布局是数据与几何的纯函数（局部
    坐标，与卡片在屏幕上的位置无关），即时模式调用方每帧重建
    option，按内容指纹复用同一次弹簧模拟，滚动/悬停帧不再
    重算 O(n²) 迭代。小容量即可——同屏一般只有一两个力导向图。

- static int ForceFingerprint(List<ChartLink> links, int r, int w, int h, int scaling, int gravity)
  - 力导向布局的内容指纹：几何参数与全部 link 的 (from, to, val)
    依次折叠进一个 < 2^31 的整数，供 ForceLayoutCache 复用比对。

- static ForceLayout CachedForceLayout(List<ChartLink> links, int r, int w, int h, int scaling, int gravity)
  - 带记忆化的力导向布局入口：指纹命中缓存直接复用上一次的
    ForceLayout，未命中才重算并存入（容量 4，挤掉最旧）；
    空 links 直接布局、不入缓存。

- static void DrawChord(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 弦图渲染入口：ChordLayout 输出的节点弧与 ribbon；图例为
    节点色块（LegendSliceKey 持久化隐藏，悬停图例即高亮对应
    弧）。节点弧随 g 扫入（sweepMax）；悬停优先命中外环带内
    的节点弧，其次按贝塞尔折线逐段测距命中 ribbon，命中节点
    时相关 ribbon/弧加亮。命中为 Node（value = 权重）或 Link
    （dataName = "from -> to"，value = 流量）事件 + tooltip；
    markPoint 画在权重最大节点弧外侧（"max N"）。

- static void AppendArcPts(List<int> px, List<int> py, int cx, int cy, int r, int a0, int a1)
  - 把 [a0,a1] 弧离散成像素点列追加进 px/py；步数约 span/2，
    钳在 4..48。

- static int ChordNodeColor(ChartSeries s, Theme t, int i, string name)
  - 弦图节点 i 的颜色：data 中同名项的 color 显式优先
    （ECharts chord.data[i].itemStyle.normal.color），否则调色板。

- static int GraphNodeColor(ChartSeries s, Theme t, int i)
  - graph 节点 i 的颜色：显式 itemStyle.color 优先，其次类别
    调色板（ECharts category 着色，同类别同色），无类别回退
    节点序调色板。

- static void DrawForceArrow(Canvas c, int ax, int ay, int bx, int by, int nodeR, int col)
  - 力导向边的目标端箭头（ECharts force.linkSymbol 'arrow'）：
    由 a→b 流向在 b 节点圆周外画实心三角，尖指向圆心。

- static void AppendQuadPts(List<int> px, List<int> py, int x1, int y1, int cx, int cy, int x2, int y2)
  - 把以 (cx,cy) 为控制点的二次贝塞尔（(x1,y1)→(x2,y2)）按
    16 段离散追加进 px/py（不含起点）。

- static void StrokeQuad(Canvas c, int x1, int y1, int cx, int cy, int x2, int y2, int color, int th)
  - 以 (cx,cy) 为控制点描 (x1,y1)→(x2,y2) 的二次贝塞尔
    （24 段折线，1/256 定点输出）。

- static void FillChordRibbon(Canvas c, int cx, int cy, int r, int sa0, int sa1, int da0, int da1, int color, int alpha)
  - 填充一条弦图 ribbon：源/目标子弧加两条贝塞尔边围成的闭合
    区域（winding 填充 + 半透明描边）；空子弧钳到 1 度。

- static bool InSweep(int ang, int a0, int a1)
  - 角度（FillSector 约定，0 = 12 点）是否落在 [a0,a1)（含跨 0 回绕）。

- static void DrawForce(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 力导向图渲染入口：CachedForceLayout 在局部坐标里布局，
    绘制与命中统一平移回屏幕；g<1000 时节点位取圆周初值→
    终态的线性补间。边宽 ∝ 流量，悬停节点相邻边高亮；节点
    形状/尺寸经 ApplyShapes 按 series.tree 逐节点匹配。右侧
    图例每节点一行（LegendSliceKey 持久化隐藏）。命中为 Node
    事件（value = 节点权重，半径含 2px 容差）+ tooltip。


## ChartView (class)

- static void ScatterSpan(List<ChartSeries> series, int i0, int i1, out int minX, out int maxX, out int minY, out int maxY)
  - 可见散点在闭区间窗口内的原始值域；无有效点时四端均为 0。
    绘制主体与悬停命中共用此 seam，避免两套域推导漂移。

- static void DrawScatter(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 散点图入口：同帧先画主体 DrawScatterCore，再画悬停
    覆盖层 ScatterHover（Core 可被缓存，命中提示始终实时）。

- static void DrawScatterCore(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 仅散点图主体（面板、坐标轴、点）—— 不含悬停覆盖层，
    可由 RenderCached 缓存（2000 点的散点云每帧只需一次像素
    拷贝），命中后指针反馈再绘制于其上。

- static void ScatterHover(App app, int x, int y, int w, int h, ChartOption o)
  - 散点图悬停覆盖层：在命中半径内查找最近点
    并显示其坐标。在 DrawScatterCore（或
    RenderCached 恢复）之后绘制，使缓存的密集点云仍有实时提示。
    窗口与 DrawScatterCore 锁定同一 [i0,i1]。


## ChartView (class)

- static int PanelHead(App app, int x, int y, int w, int h, string title)
  - 共享面板头部：圆角卡片背景 + 边框 + 可选标题，返回内容
    区顶部 y（标题行底部，已含右上角工具按钮的横向预留）。

- static void DrawToolbox(App app, int x, int y, int w, int h, int wid, ChartOption o)
  - 绘制图表右上角的工具箱按钮组（转发 ChartToolbox.Draw）。

- static void ToolboxRestore(App app, int wid, ChartOption o)
  - 工具箱「还原」：把本图全部交互态复位——魔法类型/数据
    视图/缩放、dataZoom 窗口、地图缩放平移与选择、树图缩放
    平移、图例开关与饼扇区选择（扇区键按系列数 × max(32,
    数据量) 扫描清零）——再重启入场动画并广播 Restore。

- static void DrawDataView(App app, int x, int y, int w, int h, int wid, ChartOption o)
  - 工具箱「数据视图」浮层：半透明遮罩 + 居中卡片逐行展示
    OptionTsv 文本；「复制」把全文写入剪贴板，「关闭」清
    TbViewKey 回到图表。

- static string OptionTsv(ChartOption o)
  - 把 option 导出为 TSV 文本：首行为标题。有类别轴时第二行
    是 "category" + 各系列名，随后每类别一行；否则每系列一块
    （name\tvalue 逐数据项，另附 regions 两列、links 三列
    from/to/val）。

- static void FlushToolboxSave(App app, int wid)
  - 执行挂起的「保存为图片」：把 QueueToolboxSave 记录的矩形
    写入 chart_<wid>.png；无挂起或 wid 不匹配时跳过。

- static bool tbSavePending;
  - 工具箱「保存为图片」的挂起任务（QueueToolboxSave 记录，
    FlushToolboxSave 消费；每帧至多一个待保存矩形）。

- static int tbSaveWid;

- static int tbSaveX;

- static int tbSaveY;

- static int tbSaveW;

- static int tbSaveH;

- static void QueueToolboxSave(int wid, int x, int y, int w, int h)
  - 记录一个待保存的画布矩形（帧末由 FlushToolboxSave 落盘）。

- static int WheelTicks(App app)
  - Win32/SDL 滚轮键码是 ±120/格，不是 ±1。按格数用会把
    缩放乘爆（1.15^120）再把 pan 甩出 int 范围，图就「滚没了」。

- static int ZoomByTicks(int zoom, int ticks, int lo, int hi)
  - 按滚轮格数缩放 zoom 值：每正格 ×115/100、每负格 ×100/115，
    结果钳在 [lo,hi]；纯整数运算保证确定性。

- static int ClampPan(int pan, int content, int view)
  - 把平移量钳进 [-slack, content+slack]（slack =
    max(content+view, view)），两侧保留有限的过滚动余量。

- static void CartesianTooltip(App app, ChartFrame f, List<string> labels, List<ChartSeries> series, int maxV, int step, int half, int baseIdx)
  - 悬停十字准线 + 数值提示（笛卡尔图表）。
    baseIdx 是 dataZoom 窗口起点：labels 已是窗口内子列表，
    系列值按窗口内索引 baseIdx + idx 读取（无 zoom 时为 0）。
    指针不在本图绘图区时，本图属于 connect 组则改画组共享
    悬停类别的跟随十字线，否则直接不画。

- static void StrokeSector(Canvas c, int cx, int cy, int ri, int ro, int a0, int a1, int color, int w)
  - 扇区轮廓描边：外缘与内缘各一条环带，两条半径边用
    细楔形近似（角度宽度按外半径换算）。pie/rose 的
    itemStyle 边框与 emphasis 高亮共用。

- static void StrokeRect(Canvas c, int x, int y, int w, int h, int color, int t2)
  - 矩形四边描边（用四条填充边实现，避免依赖原生
    描边图元的透明度语义）。柱条 itemStyle 边框与
    emphasis 高亮共用。

- static List<TooltipRow> tipRows;
  - ---- 延迟工具提示 ----
    提示卡片必须绘制在一切之上，但图表在帧内绘制较早：同页
    之后渲染的控件会盖住它，图表自身的 PushClip 也会把越出
    图表矩形的卡片裁掉。因此悬停时只*记录*请求（与 Widget.Tooltip
    的 Request/Flush 契约一致；本帧最后一次请求胜出——指针只在
    一个图表上），由 App.PresentFrame 在所有内容与弹层之后调用
    FlushTooltips 统一绘制。

- static int tipPx;

- static int tipPy;

- static int tipRight;

- static void TooltipCard(App app, int px, int py, int maxRight, List<TooltipRow> rows)
  - 带彩色色块行的悬停提示卡片请求。px/py 是锚点（
    十字准线 / 指针）；当卡片会越过图表右缘（maxRight）时
    翻转到左侧。

- static void FlushTooltips(App app)
  - 绘制本帧请求的图表提示卡片（若有）并清空队列。
    由 App.PresentFrame 在所有内容与弹层之后调用。

- static int SeriesMaxIndex(ChartSeries s, int i0, int i1)
  - 系列在窗口 [i0,i1]（含端点）内最大值的下标；
    窗口外或空数据返回 -1。markPoint 自动推导共用。

- static int SeriesMinIndex(ChartSeries s, int i0, int i1)
  - 同 SeriesMaxIndex，取最小值下标；空窗口返回 -1。

- static int SeriesAverage(ChartSeries s, int i0, int i1)
  - 窗口 [i0,i1] 内系列均值（ECharts markLine type:'average' 的
    纯推导 seam；空窗口返回 0）。

- static int SeriesAvg1000(ChartSeries s, int i0, int i1)
  - 窗口均值，千分固定点（不会像整数均值那样把 85/7 抹成 12）：
    sum×1000/cnt（×pointG 定点序列再除 g，原始值均值 = sum/(cnt·g)，
    文本需要 avg_raw×1000 = sum×1000/(cnt·g)），中间量走 long。

- static string Avg1000Text(int avg1000)
  - 均值显示串（ECharts markLine 默认标签是具体数值，不是
    "avg" 字样）：千分固定点四舍五入到两位小数，整数均值不加
    小数点（12142 → "12.14"，12000 → "12"）。

- static int AverageY(ChartFrame f, ChartSeries s, int i0, int i1)
  - 均值线的 y 像素：均值可带小数，落在两个数据刻度之间。
    YOf 是仿射（y = B + v*C），因此 y(sum/cnt) = y(0) +
    (y(sum) - y(0)) / cnt——把 sum 当横向量外推再除以 cnt，
    不用浮点也能得到亚数据单位的像素位。×pointG 定点序列
    再除 g（sum 本身是定点和）：y(sum/(cnt·g)) =
    y(0) + (y(sum)−y(0))/(cnt·g)。

- static int MarkLineValue(ChartMarkLine m, ChartSeries s, int i0, int i1)
  - markLine 一条线的实际 y 值（threshold seam）：kind
    average/min/max 从窗口推导，显式线用 yValue；窗口无数据
    返回 Auto() 哨兵 = 不画。

- static void DrawValueXMarkLines(App app, ChartFrame f, ChartSeries s, int i0, int i1, int nCat)
  - 值对折线的 x 轴标注线（ECharts markLine data 项
    valueIndex:0）：对窗口内 points.x 取 max/min/average 画
    竖线 + 顶部标签。线色默认 #1e90ff（ECharts 示例惯例）。

- static void DrawMarkAreaBands(App app, ChartFrame f, ChartOption o, int i0, int nCat, int seriesColor)
  - ECharts series.markArea 区间带（o.markAreas）：x 类目竖带
    横跨整个绘图区（boundaryGap=false 时贴刻度），y 值横带；
    显式 itemStyle 色原样，缺省走主题 mark-area 低透明底。
    name 非空时在带内顶部居中绘制标签（系列色，同 markLine）。

- static void DrawPointsMarkPoints(App app, ChartFrame f, ChartSeries s, int i0, int i1)
  - 值对折线（points 系列）的 markPoint（ECharts series.markPoint）：
    valueIndex -1（默认纵轴）按 points.y 取 max/min，标签
    上/下（ECharts position top/bottom）；valueIndex 0（横轴）
    按 points.x 取 max/min，标签右/左。符号/颜色逐项覆盖
    （参考站 line7：红纵轴 + 蓝横轴空心圆）。

- static string LabelText(ChartSeries s, int di, string cat, int v)
  - 数据标签文本（柱状/条形族）：data[i].labelText 覆盖（bar10
    Forecast 的标签是两系列之和）→ series.labelFmt 模板
    （{a}=系列名 {b}=类目 {c}=值）→ 缺省数值字符串。

- static void PointsHover(App app, ChartFrame f, List<ChartSeries> series, int i0, int i1, int g, bool cross)
  - 值对折线（points 系列）的悬停：按距离命中最近点并出
    tooltip 卡（line7 formatter："系列 : [ x, y ]"）。双数值轴
    配 axisPointer type:'cross' 时（tooltip.js _showAxisTrigger）
    先画十字虚线（lineStyle dashed width 1），并跟随光标出
    "( x , y )" 轴值读数——x/y 反解自两个数值轴（getValueFromCoord
    的 toFixed(2)-0 语义：两位小数去尾零），文本象限按右缘
    100px / 顶缘 50px 阈值择向。

- static bool VisualStrokeOn(ChartOption o, int seriesIndex, ChartSeries s)
  - 该系列折线是否被 visualMap 逐点着色（连续渐变或分段）：
    窗口内任一数据点命中即开——描边切子段插值通道。

- static bool VisualPiecewiseOn(ChartOption o, int seriesIndex)
  - 系列是否落在 piecewise visualMap 作用域内：分段着色的段
    边界取起点 piece 色（硬切换），不做连续渐变。

- static void DrawMarkArrow(App app, Canvas c, int ex, int ey, int col, bool horizontal)
  - markLine 末端箭头（ECharts markLine 默认
    symbol:['none','arrow']）：horizontal 时在 (ex,ey) 画右向
    箭镞，否则画下向箭镞。箭头属线色，尺寸随刻度；终点在
    绘图区边上，clip 放行 1px 防整箭头被裁。

- static void DrawSeriesMarkLines(App app, ChartFrame f, ChartSeries s, int i0, int i1, ChartOption o)
  - 系列级 markLine（ECharts series.markLine）：窗口水平线 +
    右端标签。kind average/min/max 从窗口推导；显式 yValue。
    线色默认系列色（2.x markLine 用 itemStyle 色，非全局 mark
    灰），lineType 默认 dashed。柱/线渲染器共用。

- static void DrawHBarMarkLines(App app, int plotX, int plotY, int plotW, int plotH, int lo, int hi, ChartSeries s, int i0, int i1)
  - 水平柱的系列级 markLine（DrawSeriesMarkLines 的转置）：
    值经 lo/hi -> 横向像素映射后画纵向线，顶部标签右旋对齐。

- static int BarMarkX(ChartFrame f, int barX, int slot, int nWin)
  - 系列 markPoint 标记：o.markPoint=true 时自动标出窗口
    [i0,i1] 内的最大/最小值；series.marks 的显式项也绘制
    （dataIndex 定位；kind=max/min 回退到自动推导的极值）。
    柱状图与折线图共用。f 提供 YOf 映射。
    markPoint 的本系列柱内 x：barX 是类目 0 处本系列柱条中线，
    数据点挂在第 slot 类目 —— 按类目带宽平移（CatMid 差值含末格
    余数摊薄，与主循环 bx = CatLeft + g0 + slot*(barW+gap) 精确
    同式）。barX == 0 是折线模式的哨兵：走数据点 CatX。

- static void DrawSeriesMarks(App app, ChartFrame f, ChartSeries s, int i0, int i1, int step, int barX, ChartOption o)

- static void MarkAt(App app, ChartFrame f, ChartSeries s, int idx, int slot, int nWin, string lbl, bool below, int colorOv, string symbolOv, int sizeOv, int axOv)
  - 在数据点（类别下标 idx，槽位 slot = idx - i0）上绘制单个
    标记。无显式 symbol 时画 ECharts 默认的气球徽标（pin，
    _iconPin 几何：尾尖钉在数据点上、头在上方，头半径 =
    symbolSize；label 缺省 {c} 只写数值白字居中）——**具体
    数值**写在头里，与拐点零重叠。axOv 传入本系列柱条中线在
    类目 0 处的像素（ECharts2 bar.js xMarkMap：显式/自动
    markPoint 的 x 都是本系列柱内偏移，不是类目带中线；DrawSeriesMarks
    已按数据点类目平移，折线传 0 走 CatX）。
    显式 symbol 的标记仍画符号 + 点旁小标签。below 为 true 时
    徽标翻到点下方——该系列同时显示数值标签时，点上方已被
    数值占据。

- static void MarkLabelAt(App app, Canvas c, ChartFrame f, int lx, int ly, int rad, string lbl, bool below)
  - 符号旁的小标签（显式 symbol 的标记用）：点上方/下方，
    水平钳制进绘图区。

- static int AngleOf(int dx, int dy)
  - 指针角度（度，0..360，从 12 点方向顺时针——与 FillSector
    的扫掠方向/角度零位一致），通过对 CosDeg/SinDeg 二分查找求解，
    无需浮点运算。dx/dy 是相对圆心的像素偏移。

- static int DistToSeg(int px, int py, int x0, int y0, int x1, int y1)
  - 点到线段距离（像素，定点数）。

- static void DrawDashed(Canvas c, List<int> px, List<int> py, int color, int width, int dash, int gap)
  - 沿折线分段绘制虚线/点线：每边独立按 dash 实 / gap 空
    交替（相位在顶点处重置），整数坐标，确定性。

- static void FillPolyAlpha(Canvas c, List<int> px, List<int> py, int color, int alpha)
  - 多边形扫描线填充（半透明，用于雷达 areaStyle）。逐行在
    像素中心 (y+0.5) 求边交点（1/256 定点 x）、排序后成对填
    段；段的首末列按小数覆盖率混合——整数交点配硬 FillRect
    会让雷达斜边成整列硬跳的阶梯。顶点数少（雷达 ≤ 十几轴），
    O(高×边) 足够。

- static void FillSpanAlpha(Canvas c, int xF0, int xF1, int y, int color, int alpha)
  - 一条水平段的亚像素填充：两端以 1/256 px 给定，首末列按
    小数覆盖率混合，中间整列实铺。

- static void FillPolyWinding(Canvas c, List<int> px, List<int> py, int color, int alpha)
  - 非零环绕填充：弦图缎带过圆心自交，偶奇规则会挖空。

- static int ISqrt(int v)
  - 整数平方根（向下取整；v <= 0 返回 0）。

- static int SinDeg(int deg)
  - sin(deg) × 1000，Bhaskara I 近似（误差 < 0.2%）。

- static int CosDeg(int deg)
  - cos(deg) × 1000（借 SinDeg(deg + 90)）。

- static int RadialRadius(int areaW, int areaH, int pct)
  - ECharts `radius:'pct%'`：半径 = pct% × min(w,h)/2。
    饼/环/玫瑰/和弦共用，避免撑满绘图区把标签和圆弧裁掉。

- static void StrokePolyFx(Canvas c, List<int> px, List<int> py, int color, int th)
  - 闭合多边形特效描边：坐标放大 ×256 后交给
    DrawPolylineFx（首尾点相连），th 为笔触宽。

- static int FillDx(int a)
  - FillSector 角 `a`（0=12 点顺时针）对应的屏幕方向分量（×1000）。
    CosDeg/SinDeg 的 0 在 3 点钟，不能直接当扇区方向用。

- static int FillDy(int a)
  - 同 FillDx，屏幕 y 方向分量。

- static int FillX(int cx, int r, int a)
  - 圆心 cx + 半径 r + FillSector 角 a -> 屏幕 x。

- static int FillY(int cy, int r, int a)
  - 同 FillX，屏幕 y。

- static void PushPlotClip(App app, int plotX, int plotY, int plotW, int plotH)
  - 把系列图形裁进坐标网格，避免圆点/折线/柱帽画出轴线。

- static void DrawTextClamped(Canvas c, int x, int y, string text, int color, int fs, int clipX, int clipY, int clipW, int clipH)
  - 把文本画进 clip 矩形：先平移进框，再用裁剪挡住残余溢出。

- static void DrawPolarLabel(App app, Canvas c, int cx, int cy, int r, int ang, string lbl, int color, int fs, int boxX, int boxY, int boxW, int boxH)
  - 极坐标标签：按象限锚定（左半右对齐、右半左对齐），并钳进绘图区。

- static void RingOutline(Canvas c, int cx, int cy, int r, int color)
  - 环形轮廓：一圈 1px 细圆（仪表盘/水球图的底环描边）。


## ChartView (class)

- static void DrawVenn(App app, int x, int y, int w, int h, ChartOption o, int g)
  - 韦恩图（custom kind 'venn'）渲染入口：lead.data[0..1] 为两圆
    （半径按值、圆心距按重叠量），data[2] 为交集值；半透明叠加
    自然混出第三色 + 三处锚点标签。整个图形按 g 从中心等比
    放大；命中身份取 data 下标 0=A、1=B、2=交集（VennCircle
    事件）+ tooltip。

- static string VennName(ChartSeries s, int i, string fallback)
  - 集合名：data 项 name，缺失时用回退名。

- static int VennRadius(int areaW, int areaH, int minGap)
  - 最坏的相离布局宽度为 4*r + gap（两圆半径均取 r）。
    先按真实 gap 规则反解可用半径，避免无交集/低重叠时圆被
    绘图区边缘硬裁；高度仍保留上下各一半的安全空间。

- static void VennLabel(Canvas c, int ax, int ay, int fh, int fs, string name, int value, int color)
  - 锚点标签：名称 + 值两行，围绕锚点居中。

- static bool InCircle(int mx, int my, VennCircle v)
  - 点是否在圆内（r < 1 的未用圆恒假）。


## ChartViewDataRange (class)

ECharts 2.x dataRange：图表底部的值域筛选条（两种形态）。
splitList：每段一个色块，点击把该段灰掉（DRangeBandKey）；
连续形态：色带（RampAt 分段着色），calculable 时两端叠加
可拖拽手柄（0..1000 量化状态，同 zoom 条约定）。
过滤判定统一走消费方 seam Chart.DRangeOk（地图区域 / 散点），
本组件只负责画条与写状态。占位由 Render() 在分派前扣掉，
与 Chart.toolReserve 同一帧内静态模式（这里直接缩 h 传参，
不新增全局）。

- static int Pad(App app)
  - 条内左右留白（主题 paddingMedium）。

- static int Height(App app, ChartOption o)
  - 条占用的总高度（0 = dataRange 未开启）。

- static void DataSpan(ChartOption o, out int lo, out int hi)
  - 数据定义域：统计所有已建模系列的数据集合；无可见值时
    回退 [0,100]。专用集合采用主数值语义：K 线取 low/high，
    bubble 取 weight，box 取 lo/hi，error 取 y +/- err，
    event/link 取 value，tree 取根节点 Total。

- static void Draw(App app, int x, int y, int w, int h, ChartOption o)
  - 在 (x,y,w,h) 矩形内画 dataRange 条。h = Height() 返回值。

- static bool HoverHighlight(App app, ChartOption o, int vMin, int vMax, int v)
  - hoverLink 消费 seam：悬停 dataRange 期间，值落在当前滑动
    窗口（或显式 lo..hi）内为真——地图/散点把满足者描边强调。
    未开 hoverLink、未悬停或无 App 时恒假（不改变默认观感）。

- static void DrawSplits(App app, Canvas c, int x, int y, int w, ChartOption o, int fs, int fg)
  - splitList 形态：横向色块 + 标签，点击切灰。


## ChartVisualMap (class)

ECharts visualMap（type = continuous | piecewise）。先覆盖数据
着色通道（面积/符号按 dimension 命中换色）；控件面板绘制
（continuous 渐变条 / piecewise 色块列表）随 heatmap/scatter
示例补。min/max/分段界暂按整数域（类目序号与整数值已覆盖
大多数示例；小数值域在 scatter 轮扩 ×1000 定点）。

- int type;

- bool show;

- bool hasMin;

- bool hasMax;

- int minV;

- int maxV;

- int dimension;

- int seriesIndex;

- List<int> rangeColors;

- List<ChartVisualPiece> pieces;

- static ChartVisualMap Of()

- static ChartVisualMap Clone(ChartVisualMap src)

- static int Lerp(List<int> stops, int tF)
  - inRange.color 多 stop 线性插值；tF 为 0..1000 归一位置。


## ChartVisualPiece (class)

visualMap.piecewise 的一段：[lo,hi]（含端与否）或等值 eq，
命中数据项（dimension 0 = 类目序号 / 1 = 数据值）映射 color。

- bool hasLo;

- int lo;

- bool loIncl;

- bool hasHi;

- int hi;

- bool hiIncl;

- bool hasEq;

- int eq;

- int color;

- string label;

- static ChartVisualPiece Of()

- bool Hit(int probe)
  - probe 是否落在本段内。


## ChordLayout (class)

弦图布局：节点 = links 的 from/to 首现序；节点权重 = 入 + 出；
圆周 360° 先扣除每节点稳定 gap，再按权重以最大余数法分整数弧；
每个节点内 incident links（按 link 原序）再分子弧，ribbon
连接源/目标子弧中心。输出节点弧 + ribbon 角度。

- List<ChordNodeArc> nodes;

- List<ChordRibbon> ribbons;

- int gap;

- int arcTotal;

- static ChordLayout Of(List<ChartLink> links, int sortMode, bool sortSub, int gapDeg)
  - sortMode：0 = 首现序（现状逐像素一致）| 1 = 权重降序 | 2 = 升序
    （ECharts 2.x chord.sort）。sortSub = sortSub：true 时子弧按
    link 值降序（ECharts chord.sortSub），false = 旧对端序。
    gapDeg：节点间隙度数，-1 = 自动（2，拥挤时 0；现状）。

- static int OtherIndex(List<ChordNodeArc> nodes, ChartLink lk, int self)
  - link 的对端节点下标（self 为 from 时返回 to，否则返回 from）。

- static void SortInc(List<int> inc, List<ChartLink> links, List<ChordNodeArc> nodes, int self, bool byValue)
  - 稳定插入排序某节点的 incident link 下标：byValue（sortSub）
    时按 link 值降序，否则按对端节点下标升序；同序保持 link
    原序。

- static int NodeIndex(List<ChordNodeArc> nodes, string name)
  - 按名查节点下标，无则 -1。

- static int Pos(List<int> list, int v)
  - 在下标表里找 v 的位置，无则 -1。


## ChordNodeArc (class)

弦图的一个节点弧（布局输出；角度为度，0=12 点钟方向，顺时针）。

- string name;

- int weight;

- int a0;

- int a1;

- static ChordNodeArc Of(string name, int weight, int a0, int a1)
  - 构造一个节点弧（weight 为入+出权重，[a0,a1) 为整数角度弧）。


## ChordRibbon (class)

弦图的一条 ribbon（布局输出）：源/目标节点子弧的中心角与端点。

- int from;

- int to;

- int val;

- int srcAngle;

- int dstAngle;

- int srcA0;

- int srcA1;

- int dstA0;

- int dstA1;

- static ChordRibbon Of(int from, int to, int val, int srcAngle, int dstAngle)
  - 构造一条 ribbon；子弧范围退化为中心角单点（OfSpan 的简式）。

- static ChordRibbon OfSpan(int from, int to, int val, int srcAngle, int dstAngle, int srcA0, int srcA1, int dstA0, int dstA1)
  - 构造一条 ribbon；val 为流量值，src/dstAngle 为源/目标子弧
    中心角，srcA0/srcA1、dstA0/dstA1 为对应子弧起止角。


## ErrorItem (class)

带对称误差范围（y +/- err）的数值，用于误差条图。
分类标签与测量值一起携带。

- string label;

- int y;

- int err;

- static ErrorItem Of(string label, int y, int err)
  - 构造一个误差条项（值 y、对称误差 ±err、分类标签）。

- static ErrorItem Clone(ErrorItem src)
  - 深复制；src 为 null 时返回 null。


## EventBand (class)

Event River 的一条带（布局输出；绝对像素矩形）。

- string name;

- int start;

- int end;

- int value;

- int x0;

- int x1;

- int y;

- int h;

- int row;

- int src;

- static EventBand Of(string name, int start, int end, int value, int x0, int x1, int y, int h, int row, int src)
  - 构造一条事件带（[x0,x1) × [y, y+h) 绝对像素矩形）。


## EventRiverLayout (class)

Event River 布局：统一时间范围 [t0, t1] 线性映射到水平轴；
事件按 (start, end, 原序) 稳定排序后做区间着色（贪心放入
第一条空闲行，行数最优），每条带高度 ∝ value，行围绕
中线上下对称堆叠。输出绝对像素 band 矩形，不接触 App/Canvas。

- int t0;

- int t1;

- int span;

- int rowCount;

- List<EventBand> bands;

- static EventRiverLayout Of(List<ChartEvent> events, int x, int y, int w, int h, int pad)
  - 按类注释的规则布局；pad 为绘图区内边距（像素）。事件
    start > end 时容错交换；value < 0 按 0（带高下限 2px）。

- static bool Less(List<ChartEvent> evs, int i, int j)
  - 排序键比较：start 升序 → end 升序 → 原序（稳定）。


## ForceEdge (class)

力导向图的一条边（布局输出；去重后的无向对）。

- int a;

- int b;

- int val;

- static ForceEdge Of(int a, int b, int val)
  - 构造一条无向边；val 为该无向对的 link 值之和。


## ForceLayout (class)

力导向布局：节点 = links 首现序；边 = 无向对（自环丢弃、
重复边求和）。初始位置为圆周（无随机）；固定轮数的整数
定点弹簧模拟（近距离斥力 + 边吸引 + 中心引力 + 边界钳制）。
节点数 > 60 时降迭代。相同输入 → 相同输出。

- List<ForceNode> nodes;

- List<ForceEdge> edges;

- int iterations;

- List<int> startX;

- List<int> startY;

- static ForceLayout Of(List<ChartLink> links, int r, int w, int h, int scaling, int gravity)
  - 在**局部坐标**里模拟：绘图区左上角为原点，中心在
    (w/2, h/2)，钳制到 [0..w]×[0..h]。调用方绘制时再平移到
    屏幕位置。这样布局只取决于数据与盒子尺寸——卡片滚动
    时形状不变，逐帧缓存也能跨滚动位置命中。
    scaling / gravity（百分比，100 = 现状逐像素一致）：
    分别缩放弹簧斥力/边吸引与中心引力（ECharts force.scaling /
    force.gravity）。

- static int NodeIndex(List<ForceNode> nodes, string name)
  - 按名查节点下标，无则 -1。

- static ForceLayout Build(List<ChartLink> links, List<string> nodeNames)
  - 节点/权重/边骨架（布局共有前置）：显式节点名（graph 的
    data/nodes 即节点，可能没有任何 link 引用）先行，links 里
    新出现的名字按首现序补齐；权重 = 入 + 出；边去自环、同
    无向对累加。不设坐标、不模拟。

- static ForceLayout CircularOf(List<ChartLink> links, List<string> nodeNames, int w, int h)
  - 环形布局（ECharts graph layout:'circular'）：节点按声明
    序均匀落在圆周；无模拟、无入场补间（startX 保持 null）。

- static ForceLayout FixedOf(List<ChartLink> links, List<string> nodeNames, List<int> xs, List<int> ys, int w, int h)
  - 固定坐标布局（ECharts graph layout:'none'）：节点按声明
    序取数据坐标 (xs[i], ys[i])，逐轴线性映射进绘图区（留
    pad 边距）。数据坐标缺失/退化为一点时该轴回落圆周。

- static void ApplyShapes(ForceLayout l, List<ChartNode> shapes, int minR, int maxR)
  - ECharts force 的 symbol/symbolSize 是**逐节点**声明：调用方把
    节点形状放在 series.tree（ChartNode.Shaped 叶），布局仍由 links
    推导，这里按名匹配把 symbol/size 抄到 ForceNode 上。未匹配的
    节点保持圆 + 自动尺寸。
    minR/maxR（ECharts force.minSize/maxSize，像素，0 = 关闭）：
    无显式 size 的节点直径按权重在两者间线性插值；显式 size 仍
    优先。绘制端用 size/2 当半径。

- static int EdgeIndex(List<ForceEdge> edges, int a, int b)
  - 查无向对 (a,b)（调用方保证小端在前）的边下标，无则 -1。


## ForceLayoutCache (class)

力导向布局的逐帧记忆化条目：布局是数据与几何的纯函数，
即时模式调用方每帧重建 option 对象，按内容指纹复用
同一次弹簧模拟，避免滚动/悬停帧反复重算 O(n²) 迭代。

- int fp;

- ForceLayout layout;

- static ForceLayout Lookup(List<ForceLayoutCache> cache, int fp)
  - 指纹命中则返回缓存布局；未命中返回 null。

- static void Store(List<ForceLayoutCache> cache, int fp, ForceLayout l, int capacity)
  - 存入布局（同指纹去重；超出容量时挤掉最旧的一条）。


## ForceNode (class)

力导向图的一个节点（布局输出；整数像素坐标）。

- string name;

- int x;

- int y;

- int weight;

- string symbol;

- int size;

- static ForceNode Of(string name, int x, int y, int weight)
  - 构造一个力导向节点（symbol = ""、size = 0 即圆 + 按权重
    自动直径）。


## GaugeAxisLabel (class)

仪表盘轴标签：开关、formatter（"" = 显示原值）与文本样式。

- bool show;

- string formatter;

- ChartTextStyle textStyle;

- static GaugeAxisLabel Create()
  - 构造默认标签：显示、无 formatter、默认文本样式。

- static GaugeAxisLabel Clone(GaugeAxisLabel src)
  - 深复制；src 为 null 时返回 null。


## GaugeAxisLine (class)

仪表盘轴线：线样式 + 渐变色带（colors 按 stop 顺序着色）。

- bool show;

- ChartLineStyle lineStyle;

- List<GaugeColorStop> colors;

- static GaugeAxisLine Create()
  - 构造默认轴线：显示、宽 10，并预置 ECharts 风格三段色带
    （20% 以下绿、80% 以下蓝、以上红）。

- static GaugeAxisLine Clone(GaugeAxisLine src)
  - 深复制（含色带列表）；src 为 null 时返回 null。


## GaugeAxisTick (class)

仪表盘刻度线：主刻度数、刻度长度与线样式。

- bool show;

- int splitNumber;

- int length;

- ChartLineStyle lineStyle;

- static GaugeAxisTick Create()
  - 构造默认刻度：显示、5 个主刻度、长 6px、灰细线。

- static GaugeAxisTick Clone(GaugeAxisTick src)
  - 深复制；src 为 null 时返回 null。


## GaugeColorStop (class)

仪表盘轴线色带的一个停靠点：stop 为 0..1000 的弧长千分位，
color 为自该点起的颜色。

- int stop;

- int color;

- static GaugeColorStop Of(int stop, int color)
  - 构造一个色带停靠点。

- static GaugeColorStop Clone(GaugeColorStop src)
  - 深复制；src 为 null 时返回 null。


## GaugeDetail (class)

仪表盘数值牌：背景/边框、相对圆心偏移与 formatter
（{value} 占位替换为当前值）。

- bool show;

- int backgroundColor;

- int borderWidth;

- int borderColor;

- int width;

- int height;

- ChartPosition offsetCenter;

- string formatter;

- ChartTextStyle textStyle;

- static GaugeDetail Create()
  - 构造默认数值牌：显示、无边框底色、100x40、(0px, 40%)、30px 字。

- static GaugeDetail Clone(GaugeDetail src)
  - 深复制；src 为 null 时返回 null。


## GaugeOption (class)

仪表盘完整配置（ECharts gauge.*）：圆心/半径、角度区间
（数学角，默认 225°→-45°）、值域 [min,max]、小数位与分割数，
以及轴线/刻度/标签/分隔线/指针/标题/数值牌子配置。

- ChartPosition center;

- ChartScalar innerRadius;

- ChartScalar radius;

- int startAngle;

- int endAngle;

- int min;

- int max;

- int precision;

- int splitNumber;

- GaugeAxisLine axisLine;

- GaugeAxisTick axisTick;

- GaugeAxisLabel axisLabel;

- GaugeSplitLine splitLine;

- GaugePointer pointer;

- GaugeTitle title;

- GaugeDetail detail;

- static GaugeOption Create()
  - 构造默认配置：中心 50%/50%、内径 0、半径 75%、
    角度 225→-45、值域 0..100、precision 0、10 分割。

- static GaugeOption Clone(GaugeOption src)
  - 深复制全部子配置；src 为 null 时返回 null。


## GaugePointer (class)

仪表盘指针：长度（标量）、宽度、颜色（0 = 默认）与阴影。

- ChartScalar length;

- int width;

- int color;

- int shadowColor;

- int shadowBlur;

- static GaugePointer Create()
  - 构造默认指针：ECharts2 默认长 80%、宽 8px；
    color 0 = 'auto'（跟随轴线色阶段色，见 DrawGauge）。

- static GaugePointer Clone(GaugePointer src)
  - 深复制；src 为 null 时返回 null。


## GaugeSplitLine (class)

仪表盘分隔线：开关、长度与线样式。

- bool show;

- int length;

- ChartLineStyle lineStyle;

- static GaugeSplitLine Create()
  - 构造默认分隔线：显示、长 10px、灰粗线（宽 3）。

- static GaugeSplitLine Clone(GaugeSplitLine src)
  - 深复制；src 为 null 时返回 null。


## GaugeTitle (class)

仪表盘标题（系列名）：开关、相对圆心的偏移与文本样式。

- bool show;

- ChartPosition offsetCenter;

- ChartTextStyle textStyle;

- static GaugeTitle Create()
  - 构造默认标题：显示、位于 (0px, 20%)、灰字 16px。

- static GaugeTitle Clone(GaugeTitle src)
  - 深复制；src 为 null 时返回 null。


## MapLayout (class)

地图布局：全局数据边界等比 fit 到绘图区（居中），输出变换
后的环、缩放（千分比像素/单位）与变换原点。纯几何，不碰
Canvas，命中走 bbox + 整数 point-in-polygon。

- List<MapPolygon> polys;

- int regionCount;

- int scale;

- int minX;

- int minY;

- int maxX;

- int maxY;

- int offX;

- int offY;

- static MapLayout Of(List<ChartMapRegion> regions, int x, int y, int w, int h, int pad)
  - 静态布局：等价 OfRoam(zoom=100, pan=(0,0))。

- static MapLayout OfRoam(List<ChartMapRegion> regions, int x, int y, int w, int h, int pad, int zoom, int panX, int panY)
  - 全局数据边界等比 fit 进 (w-2pad)×(h-2pad) 并居中，再按
    zoom（百分比，钳 40..280）放大、平移 (panX,panY)。输出
    变换后的环列表与 scale（千分比像素/单位）；所有环都退化
    （<3 点）时 scale=0 且 polys 为空。

- static MapLayout OfRoamBox(int mnX, int mnY, int mxX, int mxY, List<ChartMapRegion> regions, int x, int y, int w, int h, int pad, int zoom, int panX, int panY)
  - 显式源框（minX..maxX）版布局：数据边界由调用方给定
    （SVG 地图传 viewBox 框，让折线覆盖与光栅底图共用同一
    contain-fit 仿射）。其余语义同 OfRoam。

- static int RegionAt(MapLayout l, int px, int py)
  - 命中：返回包含 (px,py) 的区域下标（在任一外环内且不在
    任何洞内；区域从后往前先到先得），否则 -1。


## MapPolygon (class)

已变换到屏幕坐标的一条环（外环或洞），带 bbox 与质心。

- int region;

- bool hole;

- List<ChartMapPoint> points;

- int minX;

- int minY;

- int maxX;

- int maxY;

- int cx;

- int cy;

- static MapPolygon Of(int region, bool hole, List<ChartMapPoint> points)
  - 构造一条已变换的环：points 为屏幕坐标（非空），据此计算
    bbox 与顶点均值质心。


## PieLayout (class)

纯饼图布局：把可见 Pie 系列的 data 项归一化为扇区，供
chart_pie_layout 测试直接断言几何。语义：
- 每条可见 Pie series 的每个 ChartData 是一个扇区；
- 隐藏扇区（data.hidden 或系列 hidden）不进 total，也不占角度；
- pieRings=true 时每条可见系列 = 一独立环，各自计算 total
（各自 360°）；否则所有可见系列的扇区合并进同一张饼；
- 颜色解析：数据项色 > 单数据项系列的系列色 > 按扇区序调色板。
- 总和用 long 宽累计（totalWide / ringTotalWide），角度与
百分比一律按宽值计算；int total / ringTotal 是饱和兼容
字段，超过 int 上限时钉在 int.MaxValue。
不触碰 App/Canvas —— (主题, 选项) 进，扇区几何出。

- List<PieSlice> slices;

- int total;

- long totalWide;

- int ringCount;

- List<int> ringTotal;

- List<long> ringTotalWide;

- List<int> ringInner;

- List<ChartPosition> ringCenter;

- List<ChartScalar> ringRadius;

- List<ChartScalar> ringRadiusIn;

- int rot;

- static PieLayout Of(Theme t, ChartOption o)
  - 归一化布局入口：收集可见 Pie 系列的全部正值非隐藏数据项；
    环模式（pieRings）逐环独立 total，合并模式共享 total；
    startAngle 换算为起始边顺时针偏移 rot。无可见 Pie 系列
    或 total < 1 时返回空布局。

- static int ClampInt(long v)
  - long -> int 饱和夹取：兼容字段保持正值语义，超过 int 上限
    钉在 int.MaxValue，不发生二补码回绕成负数。

- static int GlobalColorIndex(ChartOption o, string nm, int fallback)
  - ECharts2 同名同色：扇区调色板下标按名字在整个 option 中首次
    出现的顺序（去重）分配——多饼同板时同名项恒取同色（官方
    pie.opt.js 三饼里 直达 恒为第 1 色、邮件营销 恒为第 4 色）。
    无名项回落 fallback（系列下标*16+项下标）。

- static int SlicePalIndex(ChartOption o, ChartSeries s, int di, int fallback)
  - 扇区调色板下标入口：数据项自带名字才参与同名同色去重
    （ECharts2 语义按项名，不是系列名）；无名项回落 fallback
    （系列下标*16+项下标），各项取各自的色。不能拿 SliceName
    的系列名回退去重——同一系列的无名项会全部共享系列名的
    同一个下标，整张单色。

- static int SliceColor(Theme t, ChartSeries s, int di, int sliceIndex)
  - 扇区颜色：数据项色 > 单数据项系列的系列色 > 按数据项下标调色板。
    用 di（而不是可见扇区序）着色，图例开关后颜色不会错位。

- static string SliceName(ChartSeries s, int di)
  - 扇区名：数据项名优先，其次系列名，最后回退到序号。


## PieSlice (class)

饼图一个扇区（归一化后）：值、颜色、显示名、所属系列/数据项
索引、角度区间 [a0,a1]（度，Canvas 顺时针，0 在 12 点）与环索引。
环索引在 pieRings 模式下是可见 Pie 系列的顺序；否则恒为 0。

- int value;

- int color;

- string name;

- int seriesIndex;

- int dataIndex;

- int a0;

- int a1;

- int ring;

- bool selected;

- int roseP;

- static PieSlice Of(int value, int color, string name, int seriesIndex, int dataIndex, int a0, int a1, int ring)
  - 构造扇区：值/色/名/系列与数据项下标/角度区间/环号按参数
    记录，selected 初始为 false（由 PieLayout 按 data.selected 置位）。


## RadarPolar (class)

雷达/极坐标系统（ECharts2 polar[]）：一个 option 可带多个
polar，radar 系列用 polarIndex 绑定到对应坐标系。指示器
（轴名+满刻度）、圆心/半径、起始角、环数、网格形状与
指示器名样式都按 polar 独立配置。

- List<string> indicatorText;

- List<int> indicatorMax;

- ChartPosition center;

- ChartScalar radius;

- int startAngle;

- int splitNumber;

- string type;

- int nameColor;

- string nameFormat;

- int axisLineColor;

- int axisLineWidth;

- int splitLineColor;

- int splitLineWidth;

- List<int> splitAreaColors;

- static RadarPolar Create()

- static RadarPolar Clone(RadarPolar src)


## ResolvedChart (class)

ChartOption 的只读、逐帧规范化结果。

- ChartOption source;

- List<ResolvedSeries> series;

- int wid;

- int stateWid;

- bool animate;

- int windowStart;

- int windowEnd;

- static ResolvedChart Resolve(ChartOption source, Theme theme, App app, int wid)
  - 逐帧解析入口：确定 connect 组交互态基址 stateWid（组内
    首图把组长 wid 登记进组键并初始化共享悬停为 -1）、锁定
    dataZoom 窗口 [windowStart, windowEnd]（无 zoom 或 n<2 时
    为全范围），并逐系列生成 ResolvedSeries（图例隐藏态与
    CSS chart::series-N 颜色覆写在此一并应用）。

- ResolvedSeries For(ChartSeries source)
  - 按源系列引用查找解析快照；未命中返回 null。

- List<ChartSeries> MaterializeSeries()
  - 把全部解析快照物化为 ChartSeries 副本（顺序同源 option）。

- ChartOption DrawOption(int wid, bool animate)
  - 创建渲染器使用的帧内 option。数据集合继续共享，可能被旧
    渲染器修改的 option/series 外壳则复制并与源模型隔离。
    iwid 用 stateWid（connect 组的组长 wid）：渲染器所有交互
    键（dataZoom/图例/十字线）自动落到组共享的键上。


## ResolvedSeries (class)

单个源系列的只读绘制快照。保留 source 引用，使渲染器
无需复制数据，同时把继承值和交互状态隔离在当前帧。

- ChartSeries source;

- int color;

- int lineColor;

- int lineWidth;

- int areaColor;

- int labelColor;

- int labelFontSize;

- int emphColor;

- int emphBorderColor;

- int emphBorderWidth;

- bool hidden;

- int wid;

- bool animate;

- bool visBlocked;

- static ResolvedSeries Of(ChartSeries source, Theme theme, int index, int wid, bool animate, bool hidden)
  - 解析单个系列：主色/线色/线宽/面积色/标签字号按
    系列值 -> itemStyle.normal -> 调色板/theme 依次回退；
    emphasis 强调 paint 同步解析（缺省回退 normal）。
    hidden/wid/animate 原样记录。

- int DataColor(int index)
  - 第 index 个数据项的绘制色：数据项自带 color 非零时优先，
    否则回退系列解析主色。

- void OverrideColor(int cssColor)
  - CSS 覆写入口（chart::series-N）：替换系列主色并同步
    未被显式指定的派生色（线/面积/强调色跟随主色）。

- int EffectiveColor(bool hovered)
  - 命中（hover）后的有效 paint：强调色优先；普通状态
    返回解析色。三者都只读，不触碰源系列。

- int EffectiveBorderColor(bool hovered)
  - 有效边框色：hovered 取 emphasis.borderColor（解析时缺省
    已回退 normal），普通状态取 normal.borderColor。

- int EffectiveBorderWidth(bool hovered)
  - 有效边框宽：hovered 取 emphasis.borderWidth（解析时负值
    已钳为 0），普通状态取 normal.borderWidth。

- ChartSeries Materialize()
  - 把解析结果物化回一份源系列的深复制：外壳样式字段（主色/
    hidden/线色/线宽/面积色/标签色与字号）用解析值覆盖，数据
    集合与其余字段原样保留。供仍按 ChartSeries 绘制的路径使用。


## SankeyNodeLayout (class)

桑基图节点布局：按最长路径分层的层号 + 累计流量决定的
高度与 x/y 落点（见 ChartView.DrawSankey）。

- string name;

- int layer;

- int flowOut;

- int flowIn;

- int x;

- int y;

- int h;

- static SankeyNodeLayout Of(string name)
  - 构造桑基节点：仅记名字，layer/flow/x/y/h 由布局阶段填充。


## SeriesListSource (class)

适配器：把已有的 List<ChartSeries> 暴露为 ChartSource，
高性能路径直接接受内存数据，无需重构。

- List<ChartSeries> series;

- static SeriesListSource Of(List<ChartSeries> series)
  - 包装内存系列列表（直接持有引用，不复制）。

- override int SeriesCount()
  - 系列数 = 内存列表长度。

- override string SeriesName(int s)
  - 系列 s 的名称。

- override int SeriesColor(int s)
  - 系列显式色，其次 itemStyle.normal.color，否则 0（调色板）。

- override int PointCount(int s)
  - 系列 s 的数据点数。

- override int ValueAt(int s, int i)
  - 系列 s 第 i 点的数值。


## TooltipRow (class)

提示框内容的一行：可选色块 + 文本（color=0 不画色块，
用于标题行/合计行）。

- int color;

- string text;

- static TooltipRow Of(int color, string text)
  - 构造一行提示：color 为色块颜色（0 = 不画色块，用于
    标题行/合计行），text 为该行文本。


## TreeLayoutNode (class)

树形图布局的中间记录：节点 + 深度 + 叶子 span 起点
（见 ChartView.TreeAssign）。

- ChartNode node;

- int depth;

- int lo;

- int count;

- static TreeLayoutNode Of(ChartNode node, int depth, int lo, int count)
  - 构造布局记录：node/depth/lo/count 全按参数记录
    （count = 子树叶子槽位数，由调用方传入）。


## VennCircle (class)

韦恩图的一个集合圆（布局输出）。

- string name;

- int value;

- int cx;

- int cy;

- int r;

- static VennCircle Of(string name, int value, int cx, int cy, int r)
  - 构造一个集合圆（name 为 "" 时由渲染器回退命名）。


## VennLayout (class)

两圆韦恩图布局：data[0]=A、data[1]=B、data[2]=A∩B（缺失按 0）。
hidden 数据项按 0 处理（不进布局）。半径按面积比例
（r ∝ sqrt(v)）由 rMax 缩放；圆心距按重叠比例 vI/vMin
从相离 (rA+rB+gap) 线性压向包含，全部确定性整数运算。
输出两圆圆心/半径、圆心距、重叠千分比、包含标志和
三个标签锚点（A-only / B-only / 交集中心）。

- VennCircle a;

- VennCircle b;

- int d;

- int overlap;

- bool contained;

- int gap;

- int ax;

- int ay;

- int bx;

- int by;

- int ix;

- int iy;

- static VennLayout Of(List<ChartData> data, int rMax, int gap, int cx0, int cy0)
  - 按类注释的规则布局：rMax 为最大半径（像素），gap 为相离时
    的圆心间距，(cx0, cy0) 为整体中心。

- static int Val(ChartData d)
  - 数据项取值：hidden 按 0 处理（不进布局）。

- static int Rad(int v, int vMax, int rMax)
  - 半径按面积比例缩放：r = rMax * sqrt(v / vMax)。


## WordCloudCacheEntry (class)

词云放置结果的逐帧记忆化条目：螺旋放置只依赖词条内容与
盒子几何，即时模式调用方每帧重建 option 对象，按内容指纹
复用同一次放置搜索（见 ChartView.DrawWordCloud）。

- int fp;

- List<WordCloudItem> items;

- static WordCloudCacheEntry Lookup(List<WordCloudCacheEntry> cache, int fp)
  - 按内容指纹查找缓存的放置结果；未命中返回 null。

- static void Store(List<WordCloudCacheEntry> cache, int fp, List<WordCloudItem> items, int capacity)
  - 存入放置结果（同指纹去重；超出容量时挤掉最旧的一条）。


## WordCloudItem (class)

词云单个词条的放置结果：内容（ChartData 引用）+ 轴对齐
包围盒 + 字号/颜色/旋转角。坐标相对绘图区。

- ChartData data;

- int x;
  - 包围盒左上角（rot != 0 时为旋转后的包围盒）。

- int y;

- int w;

- int h;

- int fontSize;

- int color;

- int rot;
  - 旋转角（度，0/90 来自 ECharts rotateRange 的两态，自定义角度集
    由 wcRotateList 提供）；旋转项的 x/y/w/h 存的是旋转后的包围盒。

- static WordCloudItem Of(ChartData data, int x, int y, int w, int h, int fontSize, int color, int rot)
  - 构造词条放置项：内容引用与几何/样式全按参数记录。


## void (delegate)

图表交互回调签名：所有事件类型共用，handler 按载荷的
type 与字段自行分流。

`delegate void ChartInteractionHandler(ChartInteractionEvent e);`


## ChartAxisType (enum)

ECharts xAxis/yAxis.type。

- Category

- Value

- Time

- Log


## ChartElementType (enum)

图表元素分类。Chart 表示整图空白区域，其余类型表示具体
数据图元；这是有限整数枚举，不承诺 ECharts DOM 的完整组件树。

- Chart

- LinePoint

- Bar

- ScatterPoint

- HeatmapCell

- PieSlice

- MapRegion

- FunnelStage

- Node

- Link

- VennCircle

- EventBand

- RadarAxis

- Candlestick

- BoxPlot

- ErrorBar

- Gauge

- WordTag


## ChartEventType (enum)

ECharts 2.2.7 风格的图表交互事件类型。
类型使用独立枚举，避免与 Event River 的 ChartEvent 数据实体重名。

- Click

- DoubleClick

- Hover

- MouseOut

- LegendSelected

- PieSelected

- MapSelected

- MapRoam

- DataZoom

- DataRange

- TimelineChanged

- MagicTypeChanged

- Restore

- Resize

- DataChanged

- Refresh

- ForceLayoutEnd


## ChartType (enum)

ECharts 2.2.7 原生 series.type。样式、堆叠、半径等行为由 series 子实体表达，不能伪装成类型。

- Line

- Bar

- Pie

- Scatter

- K

- Radar

- Chord

- Force

- Map

- Gauge

- Funnel

- EventRiver

- Treemap

- Tree

- WordCloud

- Heatmap

- Custom
