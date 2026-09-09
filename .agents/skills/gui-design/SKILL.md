---
name: gui-design
description: Zan GUI (stdlib/Gui) 的审美与排版规范——对齐、间距、尺寸统一、层级与克制,以及商务/街头嘻哈/赛博/国风/极简/玻璃拟态/新拟态/豪华/波普等风格配方,适用于任何使用 Zan 标准库 Gui 的项目(随工具链发布给用户)。凡是用 stdlib/Gui 写界面(窗口、页面、HMI、自定义组件)、做皮肤/换风格,或用户提到 好看/美观/精致/精美/对齐/间距/尺寸统一/风格/审美/商务/酷炫 时使用;界面写完收尾自查也用它。界面出现 控件重叠/压住/排版混乱/位置乱/尺寸乱,或提到 停靠/Flex/Grid/手摆坐标/ gui-overlap / ZAN_GUI_OVERLAP 时先用"排版原语纪律"一节。按钮被钉成巨块/忽大忽小、反复手调按钮尺寸(手写宽高),或提到 gui-lint/ZAN_GUI_LAYOUTLINT/FreeLayout 时也用它。用户给截图要求 照着做/严格还原布局/复刻界面/按图排版,或提到 布局账本/交互体验/UX优化/反馈闭环/防呆/键盘操作 时,先用 references/screenshot-restore.md。界面出现 毛刺/锯齿/边缘硬跳/月牙缝/抗锯齿 等渲染瑕疵,或画图表(斜线/曲线/面积)时也用它。复杂窗口布局迭代(标题栏/导航/内容/弹窗/动效从混乱到收口)、自定义或加高标题栏、窗口拖动与命中区、弹窗居中与层序、飘带等氛围动效,写码前先读 references/layout-iteration.md。界面尺寸忽大忽小、DPI 缩放错乱(双重缩放/漏缩放)也用它。
---

# Zan GUI 界面审美规范

**精美 = 一致 + 克制 + 有方向。** 一致靠档位:stdlib/Gui 内置了字号、高度、
间距三套全库统一的阶梯 token,永远从档位里取值,界面就自动"齐";克制靠取舍:
一个画面只有一个视觉重心;方向靠配方:选定风格方向后,一切从那张配方卡推导。

- 主流风格九张配方卡:`references/style-directions.md`(用户点名风格、
  或要求"好看一点"而现有皮肤不对味时,写码前先选卡)
- 页面搭配模式与反模式:`references/composition.md`(写页面布局前先读)
- 一张截图严格还原布局:`references/screenshot-restore.md`(用户给截图要
  求"照这个做/还原/复刻这个界面"时先读——测量转写→布局账本→原语映射
  决策树→同尺寸对拍验证;内含交互体验基线清单:反馈闭环/防呆/键盘/
  状态完整,还原或新写收尾都过一遍)
- 复杂窗口的迭代过程纪律(先问框架要、加高标题栏三处同步、动效帧调度、
  弹窗层序、截图驱动的小步收口):`references/layout-iteration.md`
  (标题栏+导航+内容+弹窗+动效的窗口,动手前先读——每条都是真实返工换来的)
- 把老程序迁移/复刻到 Zan、或参照现有产品做同族工具:先读 `app-migration`
  skill(复刻不创造、映射账本、行为/体验保真、验证闭环)——本文件管"好看",
  还原度纪律在那里。
- 游戏:实时/帧循环类(动作、手感、HUD 合成、失焦、移动端触屏)先读
  `game-dev` skill;文字/棋类/回合制/放置等控件驱动的游戏照常用本文件的
  排版规范即可。游戏内面板间距都走 4 的倍数档位。同屏混排(自绘 HUD +
  Gui 面板)时,缩放路径的边界按下文"缩放纪律"划分,字号必须同源。
- 立即模式心智模型/控件目录:`docs/agent-kb/gui-development.md`
- 样式解析规则:`docs/GUI_STYLE_RESOLUTION.md`;Tailwind 原子类全集:`docs/GUI_TAILWIND.md`

## 三条尺寸阶梯(硬规则)

token 定义在 `stdlib/Gui/Theme.zan`,由 `Style.zan` 导出为 `:root` 变量,
皮肤可整体改值——**永远不要写死数字**。

**字号**:`var(--font-size-tiny/small/medium/large/huge)` = 12/13/14/16/20。
正文 medium(14),辅助/标签 small(13)或 tiny(12),区块标题 large(16),
页面标题 huge(20)。更大的展示数字用 Tailwind 原子类 `text-xl..text-3xl`,
但一个画面至多出现一个超档大字。

**控件高度**:`var(--height-tiny/small/medium/large)` = 22/28/34/40。
按钮/输入框/选择框用 `.tiny/.small/.medium/.large` 皮肤档位类
(`skins/base.css` 已消费这些 token)。**同一行的操作控件必须同档**;
整块画面主按钮统一 medium,工具条统一 small,别混。

**间距**:一切间距是 4 的倍数(命中 7/13/17 这类值就是错)。
- flex/grid 容器的 gap 用档位类:`gap-none/small/medium/large` = 0/6/8/12
  (值取 `var(--gap-*)`),换肤时整套留白跟着变。
- padding/margin 用 Tailwind 原子类:`p-2`=8px、`p-3`=12px、`p-4`=16px
  (刻度 = n×4px;样式引擎原生翻译 Tailwind token,见 `Gui/Tailwind.zan`)。
- 惯例:卡片内边距 `p-3`/`p-4`,紧凑工具条 `px-2 py-1`,节与节之间
  `gap-large`(12)再往上只有 16/24,不要发明中间值。

## 对齐规则

- **表单行**:标签列固定宽(`Prefer(90, 0)`),输入列吃剩余空间;多行表单
  同一列宽、所有输入框同高同档。模式示例见 `references/composition.md`。
- **数字右对齐**(金额/计数/尺寸),**标题左对齐**,**操作按钮右对齐**
  (工具条、弹窗脚部一律右侧,主按钮在最右)。
- **垂直居中**:同行图标+文字组合挂类串 `flex items-center gap-2`
  (经 `Control.Class` 字段或 `AddClass()` 挂上);控件混排靠高度档一致
  保证基线齐,不靠逐个调 y。
- **网格对齐**:等宽卡片用 `grid`(`grid-cols-3 gap-3` 原子类或
  `Grid.Of(n).Gap(px)`),不要手摆 x/y。
- 容器边缘:相邻区块共享同一条左边界,面板左 padding 必须同值。

## 层级与颜色

- **层级靠中性色 + 字号阶梯**:`var(--text-primary)` 正文、`text-secondary`
  次级、`text-tertiary` 弱提示、`text-disabled` 禁用。标题只升字号,不变色。
- **强调色只有一种**:`var(--primary)`。主按钮一个,其余 `.secondary/.ghost`
  变体;success/warning/error 只表状态,不当装饰。
- **颜色必须走样式层**:控件代码禁直读主题语义色、禁裸 `0xAARRGGBB`、
  禁直读字号——取色/取字一律走 StyleBox(`Style.Of(app, type, cls, ...)`,
  属性带兜底如 `s.FgOr(...)`/`s.FontOr(...)`)。
- Tailwind 原子类只用于布局/间距/圆角/阴影,**不用它的调色板**
  (`bg-slate-500` 会绕开皮肤主题,换肤即脏);要颜色写语义类或 `var(--token)`。
- 圆角同档:`var(--border-radius-small/medium/large)`;同一画面出现 3 种
  圆角就是没设计。阴影只用小/中档,弹层才允许大阴影。

## 风格方向(先选卡,再写码)

统一档位解决"任何风格都不塌";风格本身走**皮肤配方**:一个皮肤包 = 一个
`skins/<name>/skin.css` 的 `:root` token 覆写,零代码,随应用发布
(应用自带 `skins/` 优先于内置皮肤)。

九张现成配方卡(商务/街头嘻哈/赛博朋克/暗金豪华/国风/极简日式/玻璃拟态/
新拟态/卡通波普)在 `references/style-directions.md`,含可粘贴的 `:root`
覆写、排版/动效/文案性格、能力边界与验收点。选卡前过"选型三问":题材的
身体记忆、签名元素只放一处、拒绝 AI 模板脸(米色+衬线+赤陶、纯黑+荧光绿、
报纸细线)。

## 克制

- **把大胆花在一处**:一个画面一个签名元素,其余安静;删掉不服务内容的
  装饰——"出门前照镜子,摘掉一件配饰"。
- **留白是材料**:分组靠间距与分隔线,不靠框套框;拿不准时多留 4px。
- **空态与错误给方向**:空态用 `Empty` 组件 + 一句"下一步做什么";错误
  说清原因与修法。文案写用户视角:"保存更改"不是"提交",一个动作全程同名。
- **动效一处点睛**:内置关键帧 `animate-spin/pulse/breath/shimmer/float/glow`
  等一个画面至多一处;hover 微反馈可以普遍,入场动画不要。

## 组件封装的反哺

- **铁律:控件自己负责绘制,使用处只配置**(实例化→配属性→喂数据→摆位置)。
  禁止在使用处用 Canvas 原语重画已有控件——组件修好后示例还在按旧画法显示,
  就会"组件是对的,demo 是错的"。
- 觉得某控件"不精美"→ 修 `stdlib/Gui/Widget/` 或 `skins/base.css` 里的规则,
  让所有使用处一起变好;新皮肤值写进皮肤包的 `:root`,不散落。
- **新增 Gui 类先查重名**(2026-09-08 踩坑):c977c311 在 `Gui.Component` 下新增
  彩带动画组件 `Ribbon`,把 SceneDesigner 等只 `using Gui.Component` 的文件里
  裸写的 `Gui.Widget.Ribbon`(功能区控件)整体劫持到新类上,调用点报
  "no member",离肇因提交很远——Zan 的名字解析按 using 就近绑定,同名类不警告。
  新增类落名前 `grep -rn "class <Name>" stdlib/Gui/`;撞名要么改名、要么调用点限定名。

## 毛刺防治(斜线/曲线/圆角的抗锯齿)

**毛刺 = 数据边被量化到整像素。** 斜线/曲线在光栅化器眼里只有"每像素覆盖
多少";只要把 1/256 定点的小数坐标交给它,AA 就自动正确。标准库的折线原语
(`DrawLine`/`DrawPolyline`/`DrawPolylineFx`)与 Chart 系列填充
(`FillColumnAA`/`FillBandFx`/`FillSpanAlpha`/`FillPolyAlpha`)都已是亚像素
的;界面出现毛刺,几乎总是绕开了它们自己拼:

- **数据边定点进光栅化器**:图表的线/面积边界这类数据驱动边,计算时保留
  1/256 定点(`yF = base*256 - num*256/den`),填充用带小数覆盖率混合的
  列填充(`ChartView.FillColumnAA`,边界行按 frac 混合)。把边量化成整数 y
  再用 1px 竖条 `FillRect(x, y, 1, h, ...)` 逐列拼,缓坡上每列硬跳一整行
  = 阶梯锯齿,条顶与 AA 折线之间还会露月牙缝(真实案例:DataTable spark
  面积、ChartBig 面积,修复均收口到 FillColumnAA)。
- **折线一笔连成**:整条线一次 `DrawPolyline`/`DrawPolylineFx`;逐段
  `DrawLine` 在拐角处两端各落一次实心像素,双重混合亮一像素、还可能留缝。
- **多边形填充用亚像素扫描线**:半透明多边形(雷达/弦图)用
  `ChartView.FillPolyAlpha`(过圆心自交的非零环绕用 `FillPolyWinding`),
  行中心采样、1/256 定点求交、段首末列小数覆盖混合;不要自己写整数交点
  配整行 FillRect,斜边会成整列硬跳的阶梯。
- **叠画月牙**:两段重合圆弧叠画,下层形状的 AA 边缘会在上层弧外露出一条
  浅色月牙(真实案例:异形窗口关闭钮悬停红 × 标题栏圆角)。修法是上层沿
  下层轮廓内收 1–2 逻辑像素(半径 -2),把下层 AA 带盖进去;不要试图用
  更多叠画去补月牙。
- **一次成形**:圆角控件禁止"方角画完再叠圆角盖"——克隆样式改
  Radius/Corners,一次画对;覆盖裁剪的原语自己拥有边缘,叠补必留边。
- **AA 渐变带固定 1 物理像素**:抗锯齿过渡带宽度是原语内部固定的,别随
  线宽/DPI 自行加宽;要更柔的效果用半透明描边,不动 AA。
- **半透明量程 0–255**:`Chart.WithAlpha` 直写 alpha 字节,传 256 会整型
  溢出成全透明——画了但看不见,极难排查。
- **验证仪式**:离屏 `new Canvas(w, h)` + `GetPixel` 统计"纯色直贴纯背景"
  的硬相接对数做阈值断言(仓库范式 `tests/gui/chart_fillaa_test.zan`、
  `chart_stackedarea_aa_test.zan`:同一图形整数实现 56/152 处硬相接,
  亚像素实现 0/4);肉眼收尾用 PrintWindow 截图放大 6× 看角与斜边。

## 缩放纪律(DPI:为什么界面忽大忽小)

框架的缩放是自动且不重复的,混乱全是绕开它造成的。机制:主题 token
(字号/高度/间距)由 `App.ScaleThemeMetrics()` 按"基线×密度档×DPI"统一重算;
CSS 里非 token 的长度由 `Style.ScaleLayout` 补乘,`StyleBox.IsPrescaled`
保证来自 `var(--token)` 的值不再乘第二次;Canvas 自绘是唯一例外——
`Canvas.DrawText` 的 fontSize、手算的坐标间距都不经过任何自动缩放。

从截图还原界面时的倍数判定是另一类坑:先按 `references/screenshot-restore.md`
1.5 节"三票定倍数"判出原图 DPI 档,换算只在布局账本里发生一次;把截图
物理像素直接抄进代码是双重缩放的头号来源。

硬规则只有一条:**每个尺寸值必须明确属于下面两条路径之一,全项目不得第三种**:

1. **样式路径(自动缩放,禁止再乘)**:CSS 声明、控件属性、`FontOr/Width`
   等 StyleBox 取值——写 token/档位值即可,框架已缩放,手再乘一遍就是
   "150% 显示下按钮大 1.5 倍"的双重缩放。
2. **自绘路径(手动缩放,禁止忘记)**:`Canvas.DrawText` 字号、HUD/自绘的
   坐标与边距——必须过 `app.Scale()`;且**封装成项目内单一 helper**(如
   `Ui.Dp()`),禁止在使用处散落内联 `* dpiScale / 100`。

自绘文字字号不许裸写数字:取主题字号阶梯(`Style.FontFallback(app,
"medium")` 等)或经 helper 缩放的档位值。审计手段:grep 直写字号数字
(如 `DrawText(..., 20)` 这类)、内联 `dpiScale`/`Scale(` 乘法、裸
`0xAARRGGBB`——每处命中都是"忽大忽小"的候选。

## 排版原语纪律(硬规则)——界面为什么会重叠

运行时给了完整的布局原语:**停靠**(Dock(1..5) 吃边、构造上互不重叠)、
**自动流**(`Panel.Column()/Row()` + `With()`)、**Flex**(一行/一列、可换行、
间距对齐全由档位类)、**Grid**(N 等宽列、可响应降列)、**FormBuilder**(表单)。
`Control.Arrange` 里只有 `dock==0`(手摆 `mx/my` + 手工宽高)这一条分支
能产生重叠。AI 生成的界面之所以"经常重叠在一起、尺寸位置乱七八糟"
(实证:大刷新钮盖住旁边的省略号钮、四张指标卡宽窄不齐、底部大片死
空间),根因全是**绕开布局原语、按像素手摆控件**——HTML 绝对定位的
习惯在这里没有兜底,窗口一缩放就散架。

硬规则:

1. **窗口骨架用停靠**:侧栏 `Dock(3).Prefer(w,0)`、顶栏 `Dock(1).Prefer(0,h)`、
   内容 `Dock(5)`;状态条 `Dock(2)`。停靠的子节点按声明顺序吃边,
   永远不会互相压住。
2. **内容面用流式/弹性容器**:`Panel.Column()/Row()` 的 `With()` 自动流是
   默认;一行多物用 Flex(`.Gap()`/`.Between()`/`.Wrap()`),卡片墙/指标行用
   `Grid.Of(n)` 等宽——**不要逐个手设宽度**(宽窄不齐就是这么来的)。
3. **手摆 `mx/my` 只属于画布类场景**:游戏场景、图表自绘、自由画布设计
   导出的坐标。表单/工具窗口里出现手摆坐标就是错的,先问"该用哪个容器"。
4. **尺寸只 `Prefer` 语义值,高度让控件自己量**:Flex/Grid 的容器高度按
   内容测量,不写死像素高度(死空间和裁剪都来自写死)。
5. **交付前跑重叠自检,清零才算完**:`ZAN_GUI_OVERLAP=1` 运行一次窗口,
   每对压在一起的兄弟会打一行
   `gui-overlap #N in <父>: <控件>[x,y w×h] overlaps <控件>[…] by ax×bypx`
   (窗口子系统程序无控制台时设 `ZAN_GUI_OVERLAP_LOG=<文件>` 落盘;
   测试里可 `Control.DebugOverlap = true` + `Control.OverlapHits()` 断言)。
   刻意叠放(角标/悬浮装饰)对那个子控件挂 `.NoOverlapCheck()` 免检,
   其余命中必须修到 0。命中为 0 的界面,必然不存在"叠在一起"。

6. **文字控件的宽高永远不手写**:按钮/勾选框的大小 = 文字 + 皮肤内边距,
   由测量自算;`Prefer(w,h)` 钉死按钮,改文案就裁字、换皮肤就变形,
   AI"一个按钮调来调去"反复微调的正是这个数。交付前 `ZAN_GUI_LAYOUTLINT=1`
   跑一遍,三类命中必须清零:`gui-lint … 固定尺寸`(手写宽高)、`拉高`
   (按钮被拉成巨块)、`裁剪`(矩形装不下文字);图标钮、画布图元、分隔条
   等刻意定尺寸的挂 `.FreeLayout()`(同一张牌同时免重叠与尺寸两检;
   测试用 `Control.DebugLayoutLint = true` + `Control.LintHits()`)。
   **同一条布局代码改到第二遍就停**:不是数值没调对,是结构选错了,
   回到规则 1-3 换容器。

自定义控件的子类契约:写 `Control` 子类(自绘控件/画布图元)必须有显式
构造器调用 `InitControl(名字, 停靠)`;隐式默认构造器不会跑基类字段初始化,
`children` 为 null、`visible` 为 false,首次 `With`/`Arrange` 即段错误。

## 收尾自查(逐条过)

1. 字号只来自阶梯(含 Tailwind `text-*` 档),没有即兴值。
2. 同排/同组控件高度同档;按钮不再三种高度并存。
3. 一切间距 ∈ 4 的倍数;gap 用档位类;区块间隙全画面一致。
4. 相邻区块左边界共线;表单列宽全表统一。
5. 数字列右对齐;操作按钮集中在右侧;主按钮只有一个且最右。
6. 颜色只来自 token/语义类,没有调色板色/裸色值/直读主题字段。
7. 中性色三档承担全部次级信息,没用加粗/彩色冒充层级。
8. 圆角、阴影、图标尺寸全画面同档。
9. 至多一个签名元素 + 至多一处氛围动效;风格方向有明确出处(配方卡)。
10. 空态/加载/错误都有下文(Empty/Spin/具体错误文案)。
11. 文案:动词具体、全程同名、句式一致,气质匹配所选风格卡。
12. 换 dark/light 两个皮肤各看一眼,没有写死的颜色残留。
13. 斜线/曲线/圆角放大看无硬跳阶梯与浅色月牙;数据边走了定点亚像素原语,
    没有整数 1px 条拼接或逐段 DrawLine。
14. 每个尺寸值出处明确:样式值走 token 没被手动乘过缩放;自绘值全走
    项目单一缩放 helper,没有内联 dpiScale 乘法与裸字号。
15. Gui 面板与自绘 HUD 混排的画面,两边的字号/间距同源(同一 theme 或
    同一 helper),肉眼没有"一边大一边小"。
16. 骨架是停靠、内容面是流式/弹性容器;表单/工具窗口里没有手摆 mx/my。
17. `ZAN_GUI_OVERLAP=1` 跑过一遍,`gui-overlap` 命中为 0(免检牌只给
    刻意叠放的装饰)。
18. `ZAN_GUI_LAYOUTLINT=1` 跑过一遍,`gui-lint` 命中为 0;按钮/勾选框
    代码里没有 `Prefer` 写死的宽高(免检牌只给图标钮/画布图元)。

## 验证

- 编译:`zanc <file>.zan --auto-stdlib -o out.exe`(GUI 程序自动带 zan_gui 驱动)。
- 跑起来真实看一眼,截图对照自查清单(截图必须锚定被调试窗口的 PID、按窗口
  截取并先验证再判断,规范见 `testing-gui-screenshot` skill);交互(点击/拖拽/键盘)用
  `ZAN_UI_SCRIPT` UiDriver 驱动做可重复流程,不要手点一次就算完。

## 在 zan-lang 仓库内工作(仅仓库内,发布给用户的版面无此节内容)

- 完整心智模型、皮肤与样式解析:`docs/agent-kb/gui-development.md`、
  `docs/GUI_STYLE_RESOLUTION.md`。
- 守门测试:`policy_no_widget_drawing`(examples 自绘)、三条颜色/字号预算
  棘轮;新组件必带 conformance 测试(`docs/STDLIB_COMPONENT_STANDARDS.md`)。
- 构建回归:`scripts\build_gallery.ps1` + `scripts\build_ide.ps1` 必须过;
  视觉检查用 gallery 深链(组件名+皮肤直达,如 `./gui_gallery Slider
  liquidglass zh`),完整流程与 Linux 环境坑见 `testing-gui-gallery` skill;
  像素级改动参照 `tests/conformance/conformance_gui_chart_symbol` 加离屏回归。
- 新增内置皮肤:在 `stdlib/Gui/skins/<name>/skin.css` 建包即可自动发现
  (可选 `banner.png` 预览图)。
