# Gui

> 源码: `stdlib/Gui/App.zan`, `stdlib/Gui/ChildWindow.zan`, `stdlib/Gui/Component/BandGrid.zan`, `stdlib/Gui/Control.zan`, `stdlib/Gui/ControlFactory.zan`, `stdlib/Gui/Css.zan`, `stdlib/Gui/Device.zan`, `stdlib/Gui/Effects.zan`, `stdlib/Gui/Event.zan`, `stdlib/Gui/Focus.zan`, `stdlib/Gui/Fx.zan`, `stdlib/Gui/HandlerRegistry.zan`, `stdlib/Gui/HitTest.zan`, `stdlib/Gui/Icon.zan`, `stdlib/Gui/IconSvg.zan`, `stdlib/Gui/IconSvgData.zan`, `stdlib/Gui/IconVector.zan`, `stdlib/Gui/ImageHttp.zan`, `stdlib/Gui/Layout.zan`, `stdlib/Gui/Math3D.zan`, `stdlib/Gui/Menu.zan`, `stdlib/Gui/NativeLayer.zan`, `stdlib/Gui/Nav.zan`, `stdlib/Gui/OverlayPopup.zan`, `stdlib/Gui/PropSpec.zan`, `stdlib/Gui/QrEncoder.zan`, `stdlib/Gui/Reactive.zan`, `stdlib/Gui/Render.zan`, `stdlib/Gui/Serialize.zan`, `stdlib/Gui/Skin.zan`, `stdlib/Gui/Stack.zan`, `stdlib/Gui/Style.zan`, `stdlib/Gui/StyleBox.zan`, `stdlib/Gui/StyleSheet.zan`, `stdlib/Gui/Text.zan`, `stdlib/Gui/Theme.zan`, `stdlib/Gui/Types.zan`, `stdlib/Gui/Ui.zan`, `stdlib/Gui/UiErrorLog.zan`, `stdlib/Gui/UserComponents.zan`


## AnimSlot (class)

App 保留动画存储中的一个带键补间/状态槽。取代了
六个按索引对齐的 animKeys/animVals/animTarget/animFrom/animStart/animDur
并行列表：`键`=稳定 id，`cur`=当前值，`dst`=目标值，
`src`=补间起始值，`startMs`=补间开始时间，`dur`=时长（毫秒）。

- int key;

- int cur;

- int dst;

- int src;

- int startMs;

- int dur;

- AnimSlot(int k, int c, int d, int s, int st, int du)


## App (class)

- Window window;

- Canvas canvas;

- Theme theme;

- FocusManager focus;

- HitTester hitTester;

- bool isRunning;

- bool needsRedraw;

- bool pollPending;

- int frameErrors;
  - 被 SafeFrame/PumpSafe 捕下的帧异常计数与最后一条消息：
    界面可以把它当状态显示（“本次运行有 N 个错误”）。

- string lastFrameError;

- FrameBody frameBody;

- static App frameApp;

- static bool wndProcPainting;

- int frameCount;

- int mouseX;

- int mouseY;

- int scrollY;

- int contentHeight;

- int scrollSpeed;

- int dpiScale;

- int designW;

- int designH;

- bool physicalStage;

- int titlebarH;

- int captionBtnW;

- int[]capActionIds;

- string[]capActionLabels;

- string chromeBrandIcon;

- int splitX;

- int sidebarScrollY;

- int sidebarContentHeight;

- bool isDark;

- bool isTopmost;

- bool showThemeButton;

- bool showPinButton;

- bool showMinimizeButton;

- bool showMaximizeButton;

- bool showCloseButton;

- int capTipId;

- int capTipX;

- string themeTipText;

- string pinTipText;

- string minimizeTipText;

- string maximizeTipText;

- string restoreTipText;

- string closeTipText;

- List<string> themeNames;

- SignalInt themeMenuModel;

- SignalBool themeMenuOpen;

- SignalInt themeMenuScroll;

- int themeMenuBaseId;

- int themeMenuTriggerId;

- UiEvent themeMenuChange;

- int fxKindOverride;
  - 外观抽屉的附加项：强制背景效果类型（-1 = 跟随
    皮肤）和强调色覆盖（0 = 皮肤默认），两者都应用在
    当前激活的预设之上。

- int accentOverride;

- SignalInt themeDrawerTab;

- int density;

- List<int> densityBase;

- bool hasSkinDensity;

- bool autoSkins;

- int appliedSkin;

- List<string> skinPacks;

- string skinArt;

- int skinArtOpacity;

- StyleSheet sheet;

- string appCss;

- StyleSheet chartSheet;

- string chartThemeName;

- string skinName;

- StyleSheet useCssSheet;

- bool glassNative;

- bool windowRound;

- bool windowRoundSet;

- int windowOpacity;

- bool windowResizable;

- int shapeMode;

- int shapeRadius;

- string shapeSpec;

- int shapeShadow;

- List<int> shapeRects;

- int shapeOffX;

- int shapeOffY;

- bool showChrome;

- string chromeStatus;

- string chromeAccent;

- int wheelCapX;

- int wheelCapY;

- int wheelCapW;

- int wheelCapH;

- int wheelClaimSeq;

- int wheelCapOrder;

- int wheelOwnerOrder;

- int tabHoldId;

- bool blocksInputBelow;

- bool inputBlockPrevious;

- bool menuBlock;

- bool menuBlockPrevious;

- bool clickClaimed;

- int frameSeq;

- int clickSeenSeq;

- long clickEvSeq;

- int clickTargetId;

- int pressTargetId;

- bool pointerDown;

- bool pressOnBlocker;

- int rightClickTargetId;

- int rightPressTargetId;

- int lastClickId;

- int lastClickMs;

- bool doubleClickNow;

- int pressStartX;

- int pressStartY;

- int pressStartMs;

- int pressStartId;

- bool longPressFired;

- int swipeDir;

- int dragClaimId;
  - 本次按压认领拖拽的控件 id（ClaimDrag）。触摸手势分扬用：
    按住期间到达的滚轮只有归认领者（或文本/缩放光标类型的
    命中区）时才重标为移动，其余放行为滚动。每次按压复位。

- List<OverlayPopup> overlays;

- List<NativeLayerReq> nativeLayers;

- List<int> nativeOccluders;

- List<int> hitOnlyBlockers;

- int lastResizeBg;

- List<AnimSlot> anims;

- int nowMs;

- int lastFrameMs;

- bool freezeAnimClock;

- static int perfMode;

- bool partialFrames;

- bool scrollHoverDirty;

- int renderBackendMode;

- int perfFrames;

- int perfRenderMs;

- int perfPresentMs;

- int perfPartFrames;

- int perfPartRenderMs;

- int perfPartPresentMs;

- int perfWorstMs;

- int perfSlowFrames;

- int perfStyleAt;

- int perfStyleMissAt;

- int perfPxFillAt;

- int perfPxBlendAt;

- int perfPxBlurAt;

- int perfPxGlyphAt;

- int perfPxSnapAt;

- int phaseAtUs;

- int phaseBgUs;

- int phaseMeasUs;

- int phaseArrUs;

- int phaseTreeUs;

- int scopeId;

- int scopeAtUs;

- int scopeEndUs;

- int scopeEndId;

- string phaseSecTop;

- int phaseSecTopUs;

- int markAtUs;

- string phaseMarkTop;

- int phaseMarkTopUs;

- string markNow;

- string redrawWhy;

- int redrawCount;

- string frameWhy;

- int frameWhyN;

- List<WhyTally> fullWhy;

- string phaseTopNode;

- int phaseTopUs;

- int perfBgUs;

- int perfMeasUs;

- int perfArrUs;

- int perfTreeUs;

- int perfBeginMs;

- int perfFxMs;

- int perfOverlayMs;

- int lastPresentMs;

- int lastFullFrameMs;

- int perfLoopAt;

- int perfLoops;

- int perfPollPath;

- int perfAnimPath;

- int perfWaitPath;

- int perfEvNone;

- int perfEvMove;

- int perfEvOther;

- int perfLoopMs;

- int perfFxTicks;

- int perfFxOnlyTicks;

- int perfFxTickMs;

- int perfFxTickUs;

- int perfFxRestoreUs;

- int perfFxRenderUs;

- int perfFxPresentUs;

- int lastInputMs;

- int lastInX;

- int lastInY;

- int animNextMs;

- int wakeNextMs;

- int wakeFrameNextMs;

- bool animRectValid;

- bool animRectAll;

- bool inputNeedsFrame;

- bool wheelScrollInput;

- int animRX;

- int animRY;

- int animRW;

- int animRH;

- bool animPrevValid;

- int animPX;

- int animPY;

- int animPW;

- int animPH;

- bool backdropDirty;

- int blurSlotSeq;

- List<int> blurSlotKey;

- List<int> blurSlotUse;

- List<int> blurSlotNew;

- int bgThemeGen;

- int bgSnapGen;

- int metricsScale;

- string bgImagePath;

- int bgImageOpacity;

- string userWallpaperPath;

- int userWallpaperOpacity;

- bool bgImagePickWanted;

- bool fxEnabled;

- int fxNextMs;

- bool fxSnapValid;

- int fxFrameMs;

- bool partialPending;

- bool partialFrame;

- bool partialBlocked;

- bool forceFullNext;

- int dmgX;

- int dmgY;

- int dmgW;

- int dmgH;

- int presentX;

- int presentY;

- int presentW;

- int presentH;

- List<int> glassRects;

- int scrollBusyUntilMs;

- bool glassDeferred;

- bool glassRefreshOwe;

- int glassRefreshArmedAt;

- List<int> glassDeferredRects;

- int blurMissStreak;

- List<int> fxDamage;

- List<int> fxTouched;

- bool fxTouchedFull;

- App(string title, int width, int height):this(title, width, height, false)

- App(string title, int width, int height, bool physicalStage)
  - physicalStage=true 时不做显示器 DPI 放大，窗口客户区
    物理像素 == 请求尺寸（游戏舞台契约，画布逻辑尺寸恒等于请求
    值）；普通 Gui 应用保持按 DPI 放大、控件度量随 DPI 缩放。

- static App CreateDark(string title, int width, int height)

- static App CreateDarkStage(string title, int width, int height)
  - 游戏舞台变体：窗口客户区物理像素 == 请求尺寸，不做
    显示器 DPI 放大。画布逻辑尺寸恒等于请求尺寸——任何 DPI 的
    显示器、拖到哪块屏都不变，鼠标/键盘坐标 1:1。GuiHost 主循环
    用它创建窗口，游戏模板因此可以按固定逻辑分辨率绘制整个画布
    （普通 CreateDark 的窗口客户区随 DPI 放大，控件用 dpiScale
    度量自适应；固定分辨率的游戏舞台不适应该方案）。

- void SetDark(bool dark)
  - 切换当前主题（浅色/深色）并重新应用 DPI 缩放。

- void ApplyTheme(Theme t, bool dark)
  - 安装任意主题预设（重新应用 DPI 缩放）。`dark`
    控制适合深色模式的边框细节（标题悬停水色等）。

- void ScaleThemeMetrics()
  - 把当前 theme 的度量重算为"基线 × 密度档 × DPI"。基线在换肤 /
    换主题时快照（theme 实例是新建的），密度切换、DPI 变化从基线
    重推——两档缩放叠加时不会互相污染，往返切换不累积舍入误差。
    全部 metric 改写入口（SetDark / ApplyTheme / SetTheme / Show）
    都走这里，取代散落的 ScaleByDpi 调用。

- void SetDensity(int d)
  - 全局密度档：0 小（紧凑）/ 1 中（默认）/ 2 大（宽松）。整体
    缩放字号/控件高度/内边距/间距/图标/圆角——与换肤、DPI 正交，
    切换后样式缓存按代次作废，下一帧全部控件按新度量重排。

- int Density()
  - 当前密度档（0/1/2，见 SetDensity）。

- string DensityLabel()
  - 当前密度档的显示名（"Small"/"Medium"/"Large"）。

- bool UseSkin(string name)
  - 加载皮肤包 `name`（`skins/<name>/skin.css` + 美术资源文件夹）
    并应用其令牌、样式表与插图。当
    找不到皮肤包时返回 false，保持当前外观不变。

- bool ReloadSkin()
  - 从磁盘重新读取当前皮肤的 CSS（皮肤热编辑）。

- void UseAppCss(string css)
  - 安装应用自身的样式表：用于页面布局
    （`display: flex`、宽度、间距）并样式化自有元素类的 CSS。
    与 UseCss 不同，它不随皮肤切换而失效——它会重新叠加到每个
    皮肤的样式表之上，应用未指定的内容仍以皮肤外观为准。

- bool UseChartTheme(string name)
  - 安装图表主题包 `Gui.Component.Chart/themes/<name>.css`（图表
    自己的皮肤，纯 CSS 配置，由组件的 ChartTheme 负责发现与读取）。
    主题包编译成一块独立的样式表，解析时垫在内置基线之上、
    Gui 皮肤之下：皮肤写过的 chart 规则优先，主题包只补基线
    没定义的部分，与皮肤/appCss 互不合并。名称为 "default" 或
    "" 时卸载主题包。找不到主题包时保持现状并返回 false。

- string ChartThemeName()
  - 当前图表主题包名（未安装时为 ""）。

- void ApplyAppCss()
  - 将应用样式表重新叠加到当前皮肤的样式表之上。叠加层
    （皮肤包 → UseCss 底表 → appCss）每次都从干净基底重建：
    卸载/切换无法"反合并"，皮肤包的缓存 sheet 也只作只读
    合并源、不再被原地污染。图表主题包不在此处——它是
    app.chartSheet 里独立的一块，由 Style 解析时垫在皮肤之下。
    调用频率极低（UseSkin/UseCss/UseAppCss/ReloadSkin），
    重建成本可忽略，且不做指纹早退——换肤与热重载后必须重建。

- void UseCss(string css)
  - 直接安装样式表（应用内编写的 CSS 文本，或以
    资源形式提供的 CSS），无需皮肤文件夹。

- int GlassTint()
  - 交给 OS 玻璃合成器的打包 ARGB 着色：当前皮肤的
    主背景色，alpha 约 59%，使模糊的桌面既保留
    色彩与实体感，又保证文字可读。

- void EnableSkins(int index)
  - 将标题栏主题按钮变为皮肤选择器（列出磁盘上找到的
    所有 `Skin.Names` 皮肤包），并由 App 自行应用所选皮肤——
    无需各应用的处理函数或 switch 语句。每个窗口默认
    启用此功能（见 Create）；再次调用可预选持久化的皮肤。
    `index` 必须是主题已激活的皮肤，使首帧
    不会重复应用。幂等：稳定 id 块只分配一次。

- void EnableSkins()

- int SkinCount()
  - 选择器提供的皮肤数量。

- string SkinNameAt(int i)
  - 皮肤 `i` 的名称（越界时为 ""）。

- int SkinIndexOf(string name)
  - 名为 `name` 的皮肤包的索引，无匹配时为 -1。按名称
    （而非索引）查找，使持久化设置能经受皮肤新增或
    移除导致的索引变动。

- void ApplySkinName(string name)
  - 应用名为 `name` 的皮肤包；当它
    未安装时保持当前外观不变（例如配置针对旧皮肤列表编写）。

- Theme SkinThemeAt(int i)
  - 皮肤 `i` 安装的 Theme——用于选择器预览，使
    每张卡片显示各自的调色板。

- void ApplySkin(int i)
  - 应用皮肤 `i`（令牌 + 样式表 + 美术）并将其记录为
    当前皮肤，使选择器保持同步。

- int SkinDensity()
  - 皮肤包可通过 `--density: small|medium|large` 声明默认密度档。
    未声明时返回 -1（保持用户当前选择）。

- void SyncSkinDensity()
  - 换肤后校准密度：皮肤声明了 `--density` 则跟随皮肤并记住
    "皮肤说了算"，否则维持用户此前选择的档位。

- void SyncSkin()
  - 当内置皮肤选择器的选中项变化（用户选择）时应用它。
    每帧开始时调用，使内容与边框一起重绘。

- void ToggleThemeMenu(int triggerId)
  - 切换外观抽屉（皮肤/动效/壁纸/强调色设置面板）。标题栏
    可见时主题标题按钮已提供同一切换；`SetChromeVisible(false)`
    的全屏宿主（如移动端）没有标题栏，由自己的触发控件
    （例如右下角浮动按钮）调用。`triggerId` 是触发控件的稳定
    命中 id：抽屉开着时按在它上面不算“点外部”，避免开关
    互搏。未启用皮肤选择器（EnableSkins）时是空操作。抽屉
    本体由覆盖阶段绘制：chrome 可见时 RenderChrome 注册，
    隐藏时宿主每帧调用 RenderThemeMenuOverlay。

- void RenderThemeMenuOverlay()
  - 全屏宿主（SetChromeVisible(false)）的外观抽屉覆盖层。
    标题栏隐藏时 RenderChrome 不会运行，抽屉无人注册——
    宿主在每帧 Render 末尾调用它补上；chrome 可见时直接
    跳过（RenderChrome 已注册，避免双重注册）。

- void SetWindowOpacity(int percent)
  - 整窗不透明度百分比（10..100）；100 = 不透明。转发给
    OS 合成器，使控件/文本随窗口整体淡出。

- void SetResizable(bool on)
  - 用户能否改变窗口大小。关闭后边框不再充当尺寸手柄、
    双击标题栏不再最大化，标题栏也不再显示最大化按钮
    （一个点了没反应的按钮比没有更糟）。

- bool Resizable()
  - 见 SetResizable。

- int WindowOpacity()
  - 最近一次通过 SetWindowOpacity 设置的不透明度（未设置时为 100）。

- void SetWindowShape(string spec)
  - 窗口轮廓为各形状区域的并集。`spec` 为
    逻辑像素下的 "t,x,y,w,h,r;t,x,y,w,h,r;..."：类型 1 = 圆角矩形
    （r = 圆角半径），类型 2 = 椭圆（w/h = 包围盒）。"" 恢复
    为普通不透明矩形。多个区域并集为一个轮廓，
    例如一个大圆角卡片上凸出一个圆形。在 Windows 上与
    逐像素 alpha 组合（无 DWM 时回退为区域，仍兼容 Win7）；
    所有区域之外的区域对绘制和点击都透明。
    与原生玻璃互斥。在 Run 之前调用。

- void SetWindowShadow(int px)
  - 围绕异形轮廓的柔和投影。`px` 是阴影的逻辑
    扩展范围（0 禁用）。会自动在形状规格开头追加一个覆盖
    形状包围盒向四周扩展 `px` 的类型 3 区域，把 OS 表面
    外扩到轮廓之外：Win32 由 FitShapeWindow 按扩展后的包围盒
    定窗口尺寸，其他平台由后端 zan_gui_set_shape 同样外扩，
    内容轮廓保持原坐标，投影画在轮廓外的扩展带里。
    在 SetWindowShape 之后、Show 之前调用。

- bool HasShadowBand()
  - 当形状规格已包含类型 3 阴影带区域时返回 true。

- void ParseShapeSpec(string spec)
  - 将形状规格解析为 shapeRects（由 SetWindowShape 与
    SetWindowShadow 自动前置的阴影带共用）。

- int WindowShadow()
  - 异形轮廓的阴影扩展范围（逻辑像素，0 = 无）。

- string WindowShapeSpec()
  - 当前窗口轮廓规格（见 SetWindowShape）；"" = 矩形。

- int WindowShape()
  - 当前窗口轮廓（见 SetWindowShape）。

- int WindowShapeRadius()
  - 圆角矩形轮廓的圆角半径（见 SetWindowShape）。

- void SetChromeVisible(bool on)
  - 显示/隐藏自定义标题栏边框。隐藏时：OS 仍允许顶部
    TitlebarHeight() 高度的条带拖动窗口，内容从 y=0 开始。

- bool ChromeVisible()
  - 自定义标题栏边框可见时为 true。

- void SetChromeStatus(string text, string accent)
  - 标题栏上的动态信息：`text` 用常规文本色，`accent` 用强调色，
    画在窗口标题之后。应用可按需每秒刷新（登录/授权、
    平均耗时、内存占用等）。传空串即隐藏。

- void SetChromeBrandIcon(string icon)
  - 自定义标题栏品牌图标：传图标库字形名（如 "rocket"），
    传空串恢复默认 "home"。大小/颜色走 CSS `titlebar::brand`。

- void SetTitlebarHeight(int devicePx)
  - 运行期加高自绘标题栏（设备像素，不小于当前值）。chrome 的
    背景、标题、状态位与标题按钮的布局都跟随该值；后端的
    原生拖动条带同步加高，整条标题栏都能拖动。
    在帧内调用（Show 会在启动时重读后端默认值）。

- void SetCaptionActions(int[]ids, string[]labels)
  - 在系统标题按钮左侧追加应用功能按钮：玻璃胶囊样式（半透明
    白底白字，悬停变亮），随 chrome 每帧渲染并注册命中区。
    ids 须是应用以 focus.PushIds 专用段分配的稳定 id，点击
    照常经 Ui.Clicked(id) 送达。须在 RunLoop 之前设置，
    原生免拖区宽度会把这些按钮一并计入。

- string ChromeStatus()
  - 当前标题栏状态文本（常规段）。

- string ChromeAccent()
  - 当前标题栏状态文本（强调段）。

- void SetWindowTitle(string text)
  - 同步操作系统窗口标题（任务栏/Alt-Tab 显示的文字）。
    自绘标题栏上的文字由帧循环传入，见 Form.SetTitle。

- void SetNativeGlass(bool on)
  - 启用/禁用 OS 原生半透明玻璃（Win11 亚克力）：
    窗口表面半透明处，桌面在窗口后方被模糊。
    与软件渲染的磨砂玻璃
    皮肤不同。与异形窗口互斥。

- bool NativeGlass()
  - OS 原生半透明玻璃启用时为 true（见 SetNativeGlass）。

- void SetWindowRoundCorners(bool on)
  - 请求窗口外轮廓圆角（Windows 11 由 DWM 合成：抗锯齿、
    与系统投影一致、零绘制成本；旧系统安全空操作）。
    与异形窗口互斥——异形轮廓自带圆角几何，DWM 圆角不参与，
    关闭异形（SetWindowShape("")）后自动恢复此处请求的策略。

- void ApplyRoundCorners()
  - 将 windowRound 策略落到 OS 窗口上（幂等）。

- void SetToolWindow(bool on)
  - 工具窗口：细标题栏、任务栏/Alt-Tab 不显示。
    适合调色板、对话框这类附属窗口。

- bool ToolWindow()
  - 窗口是否为工具窗口（见 SetToolWindow）。

- void SetWallpaper(string path, int opacity)
  - 将 `path`（PNG/BMP/JPG）绘制为该窗口的背景，按覆盖方式缩放，
    并以 `opacity` 百分比（10..100）叠加在皮肤自身背景之上。
    空路径清除它。皮肤包美术与用户壁纸都用它；
    由皮肤层决定显示哪一个（见 SetUserWallpaper）。

- string UserWallpaperPath()
  - 用户自己的壁纸路径（"" = 无）——用户选择的图片，
    区别于当前皮肤包的美术。切换皮肤不会改动它，
    因此选定的背景在换肤后依然保留。

- int UserWallpaperOpacity()
  - 用户壁纸设置时的不透明度（未设置时为 100）。

- void SetUserWallpaper(string path, int opacity)
  - 设置用户的壁纸：与皮肤美术分开记录，使
    切换皮肤包不会替换它，再像普通壁纸一样绘制。空
    路径清除用户壁纸并恢复当前皮肤包的美术（如果
    该包带美术的话）。

- static int WithAlpha(int color, int alpha)
  - 替换打包 ARGB 颜色的 alpha 字节。

- void ApplySurfaceTranslucency()
  - 设置壁纸后，各表面让其透出，但仅作为着色：
    三个表面层级彼此保持几步之差，使每个
    面板读起来是同一材质。若让边框远低于
    文档表面，就会造成一个面板像磨砂、下一个像
    玻璃、第三个几乎只剩壁纸，还会把整个外壳
    拖到壁纸自身的暗度上。

- bool SkinArtWallpaper()
  - 当当前绘制的壁纸是当前皮肤包自身的美术
    而非用户选择的图片时为 true。

- bool HasUserWallpaper()
  - 当用户设置了自有壁纸（区别于当前皮肤包的美术）时为 true。
    用户壁纸始终优先于皮肤包美术，且
    切换皮肤不会替换它。

- bool IsSkinArtPath(string path)
  - 当 `path` 是任意已安装皮肤包自身的美术（不仅限当前
    皮肤）时为 true。持久化设置曾把皮肤包美术存为壁纸，
    因此针对旧皮肤列表编写的配置可能指向一个不再属于
    当前皮肤的横幅；IDE 会忽略这类过期路径。

- void ClearWallpaper()
  - 移除用户壁纸，恢复皮肤自身的背景。

- string WallpaperPath()

- int WallpaperOpacity()

- void RequestWallpaperPick()
  - 请求宿主选择壁纸文件（见 ConsumeWallpaperPick）。

- bool ConsumeWallpaperPick()
  - 自上次调用以来请求过壁纸文件时为 true；并清除
    该请求，使宿主只打开一次选择器。

- void RenderWallpaperImage(int x, int y, int w, int h)
  - 将壁纸快速拷贝到 [x,y,w,h]，居中裁剪覆盖，使图片
    保持宽高比，然后淡入到下方皮肤背景中。

- void BackdropBlob(int cx, int cy, int r, int cr, int cg, int cb)
  - 单个柔和壁纸光晕：平滑径向渐隐到明亮的中心（无
    生硬边缘），为背景模糊提供可柔化的真实色彩。

- void BackdropDrift(int cx, int cy, int r, int color)
  - 由打包 ARGB 主题强调色着色的柔和光晕。

- void BackdropGradientWallpaper(int ax, int ay, int aw, int ah)
  - 在垂直渐变上叠加来自主题强调色的色斑
    （非玻璃渐变预设），使渐变更像壁纸。

- void BackdropGlassWallpaper(int ax, int ay, int aw, int ah)
  - 为磨砂玻璃预设准备的 iOS 风格多彩壁纸。

- void RenderBackground(int x, int y, int w, int h, int slot)
  - 将当前皮肤的窗口背景绘制到 [x,y,w,h]：渐变 +
    柔和色斑（用于渐变/玻璃预设，使磨砂面板能模糊
    真实色彩），否则为纯色 bgPrimary 填充。每次重绘缓存——
    仅动画的帧用一次拷贝恢复像素，而非
    重绘（昂贵的）色斑。`slot` 是调用方
    为其背景预留的快照缓存槽。

- void PaintShapeFill()
  - 用皮肤底色铺满异形窗口的轮廓（见 RenderBackground）。
    类型 3 的阴影带只是把系统表面撑大，不参与填充。
    填充铺满整个轮廓：内容贴着窗口边缘，投影从轮廓边缘向外
    衰减到阴影带里（见 PaintShapeShadow）；落在轮廓内的那半圈
    衰减带被这张不透明底色盖住，不会脏到内容。

- void FillEllipse(int x, int y, int w, int h, int col)
  - 椭圆填充（渲染器只有正圆），按行扫描：轮廓由
    操作系统裁剪，这里只要把里面填实。

- static int ISqrt(int v)
  - 整数平方根（向下取整）。

- void PaintShapeShadow()
  - 将异形轮廓的柔和投影绘制到表面，
    位于控件树之下（由 RenderBackground 调用）。每个非阴影带区域
    以圆角 SDF 一次出图（Canvas.ShadowRoundRect）——外轮廓到
    圆角形状的有符号距离在 blur 带上做 smoothstep 衰减，每个像素
    只写一次，半透明阴影色合成到标称 alpha，角部衰减连续。
    类型 3 阴影带区域（由 formgen 为 winShadow 添加）只扩展
    OS 表面，不投射阴影。

- int EffectiveFx()
  - 当前生效的背景效果类型：设置了绘制器覆盖项则用覆盖项，
    否则用皮肤自身的效果。0 = 无。

- bool FxActive()
  - 当前皮肤的动画背景效果运行中时为 true。
    异形窗口上绝不运行：效果层会合成到整个
    表面，粒子会点亮轮廓之外
    的透明像素而非设计本身。

- void SetBackdropFx(bool on)
  - 启用/禁用此窗口皮肤的动态背景效果。

- void SetFxKind(int kind)
  - 从 Gui 动画库（Gui.BackdropFx）中选择动态背景效果：
    传 KindXxx() 常量覆盖皮肤自带效果，传 0 关闭，
    传 -1 恢复跟随当前皮肤。

- bool FxPresent()
  - 纯效果帧：恢复上次完整渲染帧的快照，
    在其上重新合成皮肤效果并呈现。当
    无有效快照时返回 false（调用方回退为完整渲染），
    例如在尺寸变化之后。

- int FxIntervalMs()
  - 距下次效果帧的时间：皮肤自身的帧间隔。
    只有不可见的窗口才停止计时（见 FxPresent）。

- void NoteHoverDamage(int oldId, int newId)
  - 将下次重绘标记为损伤裁剪帧，覆盖指针
    离开的控件与进入的控件（带内边距，使焦点环与细线
    位于命中区外侧时也包含在内）。同一事件处理中
    任何其他重绘原因都会通过 CancelPartialFrame() 取消它。

- bool TakeDueWheelRect()
  - 滚轮帧的裁剪条带（TakeDueFrame 在动画条带不适用时调用）。
    滚轮的消费与损伤声明都发生在渲染期，而声明者几何就是上一帧
    的 wheelCap 矩形（滚轮不改变布局，跨帧稳定）——本帧裁剪到它，
    条带外的控件既无输入也无输出。合并以下来源后仍收不住（接近
    整窗、无上一帧认领）时返回 false，调用方退回整帧：
    - 上一帧认领视口（wheelCapW>0）：主来源。触摸拖动/滚轮连续
    滚动时每一帧的声明都落在这里面；
    - 本帧已声明的损伤（dmgW>0，页面滚动 NotePageScrollDamage
    在事件期先行声明）：一并包住；
    - 指针邻域（Scale(24)）：悬停高亮随内容滚到新行的过渡帧，
    RefreshScrollHover 补的条带下一帧自己会画，这里只要不把
    指针底下那一小块留在上一帧的样子。
    判 false 的兜底：无认领（指针刚跨入滚动区，整帧——这正是
    wheel-unclaimed 注释描述的吞格场景，整帧才认得出新声明者）、
    页面级滚动（内容区近乎整窗，条带无利可图）、弹层/按住（这
    两类在泵分支已整帧承诺，走不到这里）。

- void BeginIdScope(int first)

- void EndIdScope()

- void NoteGlassRect(int x, int y, int w, int h)
  - StyleBox 在画玻璃时登记面板矩形（本帧内有效）。见 glassRects。

- bool WidenDamageToGlass()
  - 损伤条带跨出了玻璃面板：把下一帧的裁剪从条带扩到
    「条带 ∪ 相交面板」的并集，使面板模糊从一整块本帧新画的
    背景重算。没有任何相交面板（miss 来自已关闭的面板）或并集
    大到接近整窗时返回 false，调用方退回整窗重绘。

- void SettleGlassRefresh()
  - 滚动串结束后的玻璃还账：串里暂用旧模糊的面板攒在
    glassDeferredRects，这里在串结束后武装一帧「条带 ∪ 欠账
    面板」的扩展刷新，让它们的模糊从整块新鲜背景重算。整窗帧
    渲染过则一切像素本就新鲜，直接销账。每帧 EndFrame 调用。

- void NoteDamage(int x, int y, int w, int h)
  - 声明本次状态变化只改变 [x,y,w,h] 这块像素：下一帧被裁剪
    到它（与本帧其他声明合并），而不是重绘整个窗口。切换
    标签页、勾选复选框一类的控件用它取代 RequestRedraw；
    同一帧里任何 RequestRedraw 都会让下一帧回到整窗重绘。

- void NoteScrollDamage(int x, int y, int w, int h)
  - 滚轮把某块可滚动区域的内容平移了一段：变的只有这块像素，
    于是把它声明成损伤区，而不是整窗重绘。区域为空或声明不成立
    时 NoteDamage 自己会退回整窗。

- void NotePageScrollDamage()
  - 页面滚动影响的区域：标题栏以下、侧边栏（若有）以右的全部内容。

- void CancelPartialFrame()
  - 强制下一帧完整重绘（任何非单纯
    悬停移动的情况：滚动、输入、缩放、动画、换肤……）。

- void MarkPresentDirty(List<int> rects)
  - 向下一次 Present 宣告扁平的 [x,y,w,h,...] 损伤矩形列表。

- int ChromeButtonCount()

- void SetChromeButtons(bool themeButton, bool pinButton, bool minimizeButton, bool maximizeButton)

- bool CaptionTipShown(int id, int bx, int bw, int hbar)
  - 悬停在某个标题按钮上够久（提示该露出来了）。
    
    声明给动画的重绘范围必须把按钮下方那条提示一起圈进去：提示是这次悬停
    动画画出来的东西，只声明按钮自己那一格的话，被动画唤醒的那一帧就裁到
    那 46x33 —— 提示画在标题栏下方，整条都在裁剪框外，于是它一个像素也落
    不到屏幕上（只有别的原因触发整窗重绘时才闪一下）。

- int CaptionTipX(int bx, int bw)
  - 标题提示区的左边（提示居中挂在按钮下方）。

- void NoteCaptionTip(int id, int bx, int bw, int hbar)
  - 记下这一帧哪条标题提示露着（`id` 为 0 表示一条也没有），并为
    “浮出/消失”那一刻额外要一帧。
    
    提示是指针刚进按钮那一帧画出来的，而那一帧的重绘范围是悬停损伤
    （只有离开与进入的那两格按钮），提示整条都在裁剪框外，于是一个
    像素也落不到屏幕上（只有别的原因触发整窗重绘时才闪一下）；指针移开
    时反过来：没人重画提示占过的那块，那条提示就挂在那里不走。

- void SetCaptionTips(string theme, string pin, string minimize, string maximize, string restore, string close)
  - 标题按钮的悬停提示文案。默认是中文；宿主界面不是中文时，
    切界面语言时把这一套文案换掉即可 —— 标题栏是窗口自己画的，
    它上面的字不跟着界面语言走，换文案只影响这五个提示。

- void FollowCaptionTips(App src)
  - 照抄 `src` 的标题提示文案：副窗口的标题栏归框架画，
    界面语言归主窗口的宿主管，所以它只能跟着主窗口。

- UiEvent SetThemeMenu(List<string> names, int index)
  - 将标题栏主题按钮变为下拉菜单，列出
    `names`（如皮肤预设）而非简单的深/浅切换，并且
    保留在原始标题按钮位置，使其不可拖动。
    向返回的事件添加处理函数以响应选择，然后读取
    ThemeMenuIndex()。在 WidgetId.Mark() 之前调用一次，使选项 id
    块在应用生命周期内保持稳定。

- bool ThemeMenuMode()
  - 标题栏主题按钮作为预设菜单时返回 true。

- int ThemeMenuIndex()
  - 标题栏主题菜单当前选中的索引。

- void SetThemeMenuIndex(int i)
  - 同步菜单选中项而不触发变更事件（用于深度链接）。

- void SetWindowPos(int x, int y)
  - 将 OS 窗口左上角移动到屏幕工作区像素坐标 (x, y)。

- void SetClientSize(int w, int h)
  - 把 OS 窗口客户区调整为 (w, h) 逻辑像素：登录小窗长成主窗口
    这类形态切换用。画布随 WM_SIZE 自动重铺。

- void CenterWindow()
  - 将 OS 窗口在其显示器工作区居中。

- void SwapCanvas(int w, int h)
  - 换掉渲染表面。损伤裁剪帧、动画矩形与 fx 快照都以
    「表面里还留着上一帧」为前提，而新表面的像素是未初始化的：
    不清掉这些状态，换表面后的第一帧只画出损伤条带，其余部分
    是内存垃圾——看起来就是黑屏加几块残影。

- void Show()

- void Run(string title)
  - 显示窗口并运行标准事件循环直至关闭，
    每帧仅绘制标题栏边框。这是简单窗口的
    一次调用便捷方法；要绘制自己的内容，请直接驱动
    BeginFrame / RenderChrome / PresentFrame 循环。

- void SyncSurface()
  - 让渲染表面跟上真实的窗口大小（并把滚动限制到
    新视口）。由 ProcessEvent 每次事件调用，也由窗口过程
    驱动的重绘调用。

- void SetFrameBody(FrameBody body)
  - 注册每帧的绘制内容，供框架在应用循环之外
    也能画帧：拖动窗口边框会进入系统模态尺寸调整循环，
    它在松手前不会回到应用的循环，没有帧体时表面就停在
    旧尺寸上，新露出的一条一直空白。自己写循环的应用在
    Show() 之后注册一次，循环体照旧。RunLoop 会自动注册。

- static void PaintFromWndProc()
  - 从窗口过程就地画一帧(先让表面跟上新的窗口
    尺寸)。没有注册帧体时为空操作。支持主 App 和 ChildWindow:
    按当前 eventHwnd 路由到对应的窗口。

- void RunLoop(FrameBody body)
  - 受保护的标准事件循环：每一轮的事件分发与
    绘制都包在异常保护里，一帧里抛出的异常只丢掉这一帧（并记入
    UiErrorLog），而不是结束进程。<paramref name="body"/> 只负责画
    内容：BeginFrame/PresentFrame 由循环完成。

- static App guardApp;

- static FrameBody guardBody;

- static int guardWhat;

- static bool guardPumpAlive;

- static void GuardBody(nint arg)

- bool PumpGuarded()
  - PumpSafe 再加一层原生故障护栏：Zan 异常由 PumpSafe
    捕获，而硬故障（越界、空指针、除零，以及生成代码里失败的
    运行时检查）由护栏记录后丢掉这一次事件——两者都不再让
    进程消失。

- bool FrameGuarded(FrameBody body)
  - SafeFrame 再加一层原生故障护栏：这一帧里的硬故障
    只丢掉这一帧。

- static int NativeFaultCount()
  - 本次运行被原生护栏吞掉的硬故障次数。

- bool PumpSafe()
  - ProcessEvent 的受保护版本：事件处理（回调、
    命令、绑定）里抛出的异常不再终止进程。
    返回 false 只表示窗口要求退出。

- bool SafeFrame(FrameBody body)
  - 在异常保护下画一帧（BeginFrame → body →
    PresentFrame）。返回 false 表示这一帧失败并已记录；
    写自己循环的应用可以直接用它换掉裸的
    BeginFrame/PresentFrame 对。

- void RefreshScrollHover()
  - 滚轮把内容挪到指针底下之后重算悬停目标。滚轮帧处理时命中
    区还是上一帧（滚动前）的，就地 HitTest 只会得到同样过期的
    目标——所以在出帧之后按新注册的矩形重算；变了就补一条
    悬停条带帧，把新旧两个目标的预览都画对。没有这一步，滚轮
    滚过后悬停预览一直挂在滚动前的那一行上（指针明明已经在
    另一行上），直到下一次指针移动才被纠正。

- void NoteFrameError(string origin, string message)
  - 记录一条被捕获的界面异常。

- int FrameErrorCount()
  - 本次运行被捕获的界面异常数。

- string LastFrameError()
  - 最后一条被捕获的界面异常（没有则为空串）。

- int ContentTop()
  - 自定义标题栏占用的高度；内容应从其下方开始。
    边框隐藏时为 0（见 SetChromeVisible）。这是内容区内的
    相对高度：阴影带的画布偏移由渲染层处理，不在此叠加。

- int ClientWidth()
  - Client dimensions exposed without leaking the backing Canvas to
    application layout code. Controls and forms use these for their root
    arrange pass; direct pixel drawing remains an internal App concern.
    阴影带外扩的异形窗口扣掉两侧 band，返回内容区尺寸。

- int ClientHeight()

- void RenderChrome(string title)
  - 绘制无边框窗口的标题栏（品牌 + 拖动区域 + 最小化/最大化/关闭
    标题按钮）并处理标题按钮的点击。应
    每帧最后绘制，以便覆盖内容。

- int RenderCaptionButtons(Canvas c, Theme t, int W, int hbar)
  - 标题按钮（主题/置顶/最小化/最大化/关闭）：x 布局、悬停水色、字形、
    命中区与点击处理。返回主题按钮的焦点 id，供
    调用方在其下方锚定主题预设抽屉。

- void NoteRedrawWhy(string why)
  - 记下「下一帧为什么只能整窗重绘」的第一个理由（仅分析器开着
    时；见 fullWhy）。声明了范围的重绘不经过这里。

- void RequestRedraw()

- void RequestAnimationFrame(int minIntervalMs)
  - 为循环动画请求*限速*重绘：下一帧
    安排在不迟于 `minIntervalMs` 之后，事件循环
    在此之前休眠（空闲，零 CPU），而非以 60fps 忙渲染。与
    RequestRedraw 不同，它不强制立即出帧，因此持续
    动画的控件（旋转指示器、骨架屏闪烁）以较低的
    节奏重绘页面。同一帧内有多个动画时，更早的截止时间胜出。
    输入仍会及时唤醒事件循环。

- void RequestWakeIn(int minIntervalMs)

- void RequestWakeAt(int dueMs)

- void RequestWakeFrameIn(int minIntervalMs)

- void RequestAnimationFrameIn(int minIntervalMs, int x, int y, int w, int h)
  - 与 RequestAnimationFrame 相同，但同时声明这个动画只会
    改变 [x,y,w,h] 这块像素。若一帧里所有动画都声明了范围，
    由动画唤醒的那一帧就裁剪到它们的并集：转圈指示器、
    边框流光、卡片光泽只重绘自己那一小块，而不是让整页
    每 16~90ms 重新混合一遍（这正是空闲时 CPU 居高不下的原因）。

- bool BackdropDirty()
  - 当本帧玻璃表面之后的内容可能已变化时为 true
    （任何 OS 输入/缩放/主题变更），若本帧只是背景不变的
    纯动画帧则为 false。玻璃表面将其传给
    Canvas.BlurRectCached，使旋转指示器/提示条复用缓存的模糊。

- bool BackdropDirtyIn(int slot, int x, int y, int w, int h)
  - 这块玻璃区域本帧是否需要重新模糊。整窗帧同 BackdropDirty()；
    损伤裁剪帧只有与脏矩形相交的区域才算脏——条带外的面板一个
    像素也写不出去，重算纯属白费（连校验和都不用算）。
    另外 slot 本帧刚换手时必须重算：里面是上一位主人的像素。
    
    滚动串（连续的滚轮/拖拽，见 NoteScrollDamage）里再放宽一档：
    与条带相交的面板也暂用缓存的旧模糊。此时重卷积只能拿到条带
    外上一帧的合成像素，结果注定不准、还得把下一帧扩成面板并集
    重来；不如先欠着——细条带照常便宜地走，串一结束由 EndFrame
    武装一帧「条带 ∪ 欠账面板」的扩展刷新统一还账。磨砂玻璃对
    快速滚动中的一两帧模糊滞后不敏感，账还清后像素严格正确。

- bool ScrollBurstActive()

- bool RectHitsDamage(int x, int y, int w, int h)

- void NoteGlassDeferred(int x, int y, int w, int h)
  - 登记一块在滚动串里暂用旧模糊的面板（还账清单）。

- void ReuseBackdrop()

- bool PointerPressed()

- int NextBlurSlot()
  - 为匿名玻璃表面（没有控件身份可用）取模糊缓存槽：以
    「本帧第 n 个匿名面板」为身份，等价于旧的按绘制顺序分配。

- int BlurKeyId(int id)
  - 玻璃面板的身份键。控件 id（StyleBox.fxId 之类）给 idKey；
    没有 id 可用时用 BlurKey(kind, 几何)：位置/尺寸不变的面板
    至少能每帧拿回同一个槽。两者分奇偶两个命名空间（id 键为奇、
    几何键为偶），不会互相撞车；匿名面板用负键。

- int BlurKey(int kind, int x, int y, int w, int h)

- int BlurSlotFor(int key)
  - 按稳定身份 `key` 取该玻璃面板的模糊缓存槽：同一元素每帧
    拿到同一个槽，因此绘制顺序变化、别处的面板出现或消失都不再
    让它丢掉缓存。key=0 视为匿名，退回按绘制顺序。返回 -1 表示
    无槽可用（回退为未缓存模糊）。

- void SetImeCaret(int x, int y)
  - 上报焦点文本控件的插入符位置（客户区像素），使 IME
    组合/候选窗口跟随光标，而非固定在
    窗口原点。聚焦期间由 Input/TextArea 每帧调用。

- void Post(Action handler)
  - 将委托封送到该窗口的 UI 线程——相当于
    C# 的 <c>Control.Invoke</c>/<c>BeginInvoke</c>。可从任意
    线程安全调用：委托入队（运行时内用 OS 互斥锁保护）并
    在下一帧开始时于 UI 线程运行，之后
    请求重绘。后台工作线程用它把结果交回，
    而无需在非 UI 线程触碰界面状态。窗口关闭后，
    委托被丢弃而非入队：已没有 UI 线程可运行它，
    且让它在*下一个*窗口运行也是错误的。

- void StopLoop()
  - 结束事件循环，并丢弃所有仍通过
    `Post` 排队的委托。在每次窗口关闭路径上调用：
    为已关闭窗口投递的后台工作不得在下一个
    窗口上运行，其帧循环复用了同一个全局分派队列。

- void RequestClose()
  - 编程式关闭窗口：等效于点击标题栏的关闭按钮
    （post WM_CLOSE，随后从事件循环正常退出）。供自绘
    退出按钮、场景切换（"OpenScene" 动作结束当前场景）这类
    代码侧触发"该窗口该关了"的路径使用。

- void DrainPosts()
  - 在 UI 线程上运行所有通过 `Post` 排队的委托，
    若有运行则请求重绘。每个事件循环
    迭代由 ProcessEvent 自动调用；手写循环也可直接调用。

- int AnimIndex(int key)
  - 查找动画键对应的行索引，没有则为 -1。行由
    AnimTo/AnimPx 追加，并保持六列索引对齐。

- void AnimAdd(int key, int val, int target, int durMs)

- int StateGet(int key, int dflt)
  - 按键持久化的整数状态（复用动画 KV 存储作为
    通用保留状态表）。使模型每帧重建的即时模式控件
    能保留交互状态（图例显示/隐藏、dataZoom
    范围等），以稳定 id 为键。StateSet 直接设定值，无补间。

- void StateSet(int key, int val)

- int AnimToValue(int key, int target, int durMs)
  - 按时间缓动的按键值（千分比，0..1000）补间，
    在 `durMs` 内趋向 `target`，返回*已缓动*的当前值（
    不再用 Ease 包裹）。进度为 (now - start)/duration，因此运动
    与帧率或定时器精度无关，保持平滑。中途重新设目标时
    tween 从当前值重新开始；首次出现时直接跳变。

- bool AnimActive(int key)

- void AnimRestart(int key, int durMs)
  - 把一次性入场动画重置到 0，用于 toolbox 还原。

- int AnimTo(int key, int target, int durMs)

- int AnimToIn(int key, int target, int durMs, int x, int y, int w, int h)

- int AnimIntroValue(int key, int durMs)
  - 一次性入场 tween：首次出现时在 `durMs` 内将每个 key 的值从 0 缓动到 1000，
    然后保持在 1000。与 AnimTo 不同（AnimTo 会在
    首帧直接跳到目标），它总是播放增长动画，
    因此图表、柱状图或卡片首次绘制时可以从基线向上生长。
    持续请求重绘直至稳定。返回缓动后的
    0..1000 进度。

- int AnimIntro(int key, int durMs)

- int AnimIntroIn(int key, int durMs, int x, int y, int w, int h)

- int AnimPxValue(int key, int target, int tauMs)
  - 使用指数平滑将每个 key 的值在任意（像素）空间向 `target` 缓动，
    因此适用于任意范围（不像 AnimTo 那样固定
    0..1000）。`tauMs` 是平滑时间常数（越大越慢）。用于
    例如标签页下划线在不同宽度的标签之间滑动。

- int AnimPx(int key, int target, int tauMs)

- int AnimPxIn(int key, int target, int tauMs, int x, int y, int w, int h)

- static int Ease(int p)
  - 用 Smoothstep（3t^2 - 2t^3）对千分值做加减速缓动。

- static int Lerp(int a, int b, int p)
  - 按千分值 p (0..1000) 在 a 和 b 之间线性插值。

- static int LerpColor(int c0, int c1, int p)
  - 按千分值 p (0..1000) 混合两个打包的 ARGB 颜色，alpha 与 RGB
    一同插值（两端不透明时结果仍不透明）。对以负符号整数
    存储的颜色同样稳健。

- static int Darken(int color, int p)
  - 按千分值 p (0..1000) 将打包颜色向不透明黑色调暗：
    一个命名的阴影锚点，控件无需内联写出黑色常量。

- static int Lighten(int color, int p)
  - 按千分值 p (0..1000) 将打包颜色向不透明白色调亮。

- static int ScaleAlpha(int color, int p)
  - 按千分值 p (0..1000) 缩放打包颜色已有的 alpha 通道，
    保留其 RGB。p=1000 返回原色，p=0 使其完全
    透明。对不透明颜色和已带 alpha 的颜色（如玻璃色板）都有效，
    因此填充/遮罩可以淡入淡出。
    对符号整数颜色打包稳健（见 LerpColor）。

- bool CaptureWheel(int x, int y, int w, int h)
  - 可滚动控件在渲染期间调用它，以在悬停时抢占滚轮。
    最后悬停的声明者成为下一输入帧的拥有者，
    因此嵌套视图消费滚轮时不会同时滚动父级。

- void SetContentHeight(int h)

- int ViewportHeight()

- int Scale(int v)

- int ShapeOffX()
  - SetWindowShadow 外扩时内容轮廓相对画布原点的偏移
    （物理像素）。异形窗口的阴影/填充/自绘标题栏都以
    它为基准定位；矩形窗口恒为 0。

- int ShapeOffY()

- void FillChrome(int x, int y, int w, int h, int radius, int color)
  - 填充结构性框架表面（侧边栏、标签条、工具面板）：
    玻璃皮肤下会磨砂背景，使整个外壳呈现玻璃质感；
    否则为普通的主题填充。`radius` 为 0 时填充方形。

- void FillGlass(int x, int y, int w, int h, int radius, int color, int a)
  - 填充遮罩表面：皮肤为玻璃且表面
    稳定后（`a`，千分比淡入 alpha，>= 900）磨砂：背景模糊加
    主题色调，壁纸色相仍能透出。真正的系统玻璃
    已模糊桌面，只需轻微着色。其余情况
    为普通（可选淡入淡出）填充。

- void SetTheme(Theme t)

- void FreezeAnimClock(int fixedMs)

- void UnfreezeAnimClock()

- bool TakeDueFrame(int now)
  - 已到期的帧截止时间（动画 / 唤醒 / 皮肤特效）就地兑现：标记这一帧
    要画，并在纯动画唤醒时把它裁剪到动画自己声明的范围。返回 false
    表示这一拍已由特效层就地呈现、还该继续等下一拍。

- void PumpDueFrame()
  - 帧截止时间到了就兑现（不等待）。轮询那一路（有人挂起了重绘、
    或自动化驱动每圈都要求轮询）以前完全绕过截止时间：动画帧只在
    “阻塞等下一拍”那一路才产生，于是驱动一开，悬停缓动、提示浮出、
    toast 收拢这些纯动画帧一帧也不来，界面就停在最后那帧上。

- void SetPollEventMode()
  - 要求下一次 ProcessEvent 以轮询方式进行，绝不阻塞等待 OS 事件。
    供外部驱动帧循环的宿主（如 Game.Ui.GameHud：游戏主循环负责帧
    节奏，每帧都会来取事件）设置。否则空闲时走到阻塞 WaitEvent 的
    那一路，会在没有独立消息泵的窗口上永久睡死（游戏窗口的消息
    只有 SDL_PollEvent 泵送，HUD 合成循环不调它）。

- bool ProcessEvent()

- nint WindowHandle()
  - 此应用窗口的原生句柄（用于多窗口事件路由）。

- bool ApplyEvent(nint evHwnd)
  - 当事件源于本窗口时，将当前已泵出的原生事件
    应用于本窗口（evHwnd == 本窗口）。这使单个
    进程能从共享的事件泵驱动多个顶层窗口
    （如 IDE 加一个悬浮对话框）：循环泵出一次，读取事件
    hwnd，再通过 ApplyEvent 把事件提供给每个 App。
    若本窗口收到关闭事件则返回 false。

- void PresentFrame()

- void PerfLoopTick(int t0, int path)
  - 帧分析器的空闲侧：记一圈事件循环走了哪条等待路径、被什么
    唤醒、在循环体外花了多少毫秒，每 2 秒往同一个日志追一行。
    path: 0 = 有挂起重绘（轮询），1 = 动画/特效截止时间，
    2 = 阻塞等事件。窗口安静不动时这行应该几乎不增长；它涨得
    快就说明有人在无事可做时反复唤醒 UI 线程。

- void PerfMaybeFlushLoop(int now)
  - 把累计的循环/特效计数按 2 秒窗口落盘。除了事件循环本身，
    纯特效 tick（FxPresent 在等待循环内就地呈现，不经过
    PerfLoopTick）也调用这里，否则安静的效果层会让日志整段
    缺行，看起来像循环根本没在跑。

- void PerfMark(string name)
  - 宿主在一大段绘制里埋的标记点：把自上一个标记以来的时间
    记到 `name` 头上（空名字只重置起点），分析器关着时不做事。
    尖尖那一帧只报最贵的一段，不每帧刷一大篇日志。

- void NoteFullFrameWhy()
  - 记下这一整窗重绘帧是凭什么整窗重画的：脏区帧只重画一条带，
    整窗帧得把整个页面重新混一遍，因此“谁在不停地要整窗重绘”
    是帧成本的首要问题，而不是帧里画了什么。

- string FullWhyLine()
  - 本批里整窗重绘理由的前三名（name:帧数，逗号分隔）。

- void PerfNode(string kind, string nm, int us)
  - 一个节点自身绘制的耗时（不含子树）：只留本帧最贵的那个。

- void PhaseBegin()
  - 开始一段帧内相位计时（分析器关着时是空操作）。

- void PhaseEnd(int slot)
  - 把上一个标记点到现在的时间计到第 `slot` 个相位上：
    0 = 背景，1 = 测量，2 = 排版，3 = 画整棵树。

- static string UsAvg(int us, int n)
  - `us` 微秒摆到 `n` 帧上，以毫秒保留一位小数。

- bool ForceFullFrames()
  - 为真时所有局部帧路径都退回整窗重绘 + 整窗上传（本应用的默认）。

- bool PartialFrames()
  - 局部帧（悬停条带、动画矩形、纯特效就地呈现）当前是否开启。

- void SetPartialFrames(bool on)
  - 开启/关闭局部帧。**默认关闭**：局部帧要求每一处状态变化都准确
    声明自己改了哪些像素，漏一处旧像素就留在屏上（重复的面板、动画
    的移动轨迹、鼠标划过按钮时的错乱），一个真实应用里漏报的地方是
    堵不完的，所以正确性优先。这是每个应用自己的选择（不是环境变量：
    那会让一台机器上所有 Zan 程序共用一份配置），应用可以把它接到
    自己的设置项上，逐屏验证过再打开。

- int RenderBackendMode()
  - 本应用要求的光栅器（`RenderBackend.Cpu/Gpu/Auto`）。要看实际生效的
    那个用 `RenderBackendName`：要了 GPU 而这台机器给不出 GL
    上下文时，画面照旧由 CPU 光栅出来。

- string RenderBackendName()
  - 实际生效的光栅器名字（"cpu" / "gl"），供设置页与日志显示。

- int SetRenderBackend(int mode)
  - 选择本应用用哪个光栅器画每一帧。**默认 CPU**：GPU 后端还有
    阴影/模糊/图片这几个图元在 CPU 上（分派时自动同步帧），并且要靠
    每台机器的 GL 驱动，先让应用自己逐屏验证过再开。切换会带着当前
    窗口内容一起搬过去，不会闪白；随后整窗重画一帧。
    
    返回实际装上的后端：1 = GPU，0 = CPU（要了 GPU 拿到 0 就是这台机器
    没有可用的 GL 上下文——远程桌面、虚拟机、CI——不是错误）。

- static int FxSnapSlot()
  - 效果层合成前那一帧的快照槽。快照槽是一张全进程共享的表，
    而 ChartView.RenderCached 的文档把 0-7 给了宿主自己的图表缓存：
    效果层也用 7 的时候，宿主一旦缓存一张图表就把这份全窗快照顶
    掉，下一次效果跳动就把图表的旧像素修复到窗口各处，而且一直
    留到下一次整窗重绘。取一个宿主用不到的高位槽（池按需长到 512）。

- static bool PerfOn()
  - 启用可选帧分析器（ZAN_FRAME_PROF=1）时为真。

- static string MsAvg(int total, int n)
  - `total` 毫秒摊到 `n` 帧上，保留一位小数。每帧的取样本身
    只有毫秒精度，但摊到几十帧上，这一位小数足以看出
    半毫秒量级的变化——整数平均会把它们全抹平。

- static string RasterLine(int frames)
  - 帧分析器输出的一行每帧光栅化工作量：调用数与
    每个图元的数千像素，在 `frames` 帧上取平均。

- void BeginFrame()

- void AddOverlay(OverlayPopup p)
  - 将弹层排队，在主内容绘制之后绘制并分发，
    使其位于一切之上并拥有最顶层命中区域。
    `RunOverlays`.

- void RunOverlays()
  - 按注册顺序绘制并分发本帧注册的所有遮罩。
    在主渲染之后、PresentFrame 之前调用一次。

- bool HasOverlays()
  - 本帧有活动的弹层层时为真。

- bool PointerCaptured()
  - 当模态遮罩/弹层遮罩拥有指针时为真——无论是本帧
    （执行了 BlockHitsRect/BlockHitsBelow）还是上一帧
    （弹层已存在）。直接读取 mouseX/mouseY 的即时模式控件
    必须用 `!PointerCaptured()` 约束其悬停/按下/点击，
    防止指针穿过弹层落到其下方的层。

- int BlockHitsRect(int x, int y, int w, int h)
  - 注册一个吞掉 [x,y,w,h] 区域点击的命中区域，
    使模态/弹层表面拦截其下的控件。HitTester
    后注册者优先，且遮罩在页面内容之后绘制，因此
    在绘制背景时调用它——且在遮罩自身
    按钮注册之前——可使拦截器除这些按钮外
    处处优先。返回拦截器 id。

- void ReserveEdgeHit(int x, int y, int w, int h)
  - 为客户端区域抢占 [x,y,w,h]，对抗窗口边框的
    边缘缩放手柄。紧贴窗口边缘绘制的控件——如滚动条
    位于最后几像素——否则在那里无法点击：边框的
    手柄先响应系统命中测试，按下永远到不了
    客户区，只有滚轮还能滚动。角手柄保持优先，
    保证对角缩放仍可操作。绘制期间每帧调用一次。

- int BlockHitsMenu()
  - 全窗口 BlockHitsRect：模态遮罩的标准遮罩，其
    变暗背景覆盖整个窗口。
    上下文菜单专用的全窗口阻挡：和 BlockHitsBelow 一样吞掉
    主键，但右键仍解析到菜单下方的控件，于是在别处右键会把
    菜单换到新位置重开（Windows 的一贯行为），而不是要求先
    手动关掉当前菜单。

- int RightHitTest(int px, int py)
  - 右键的命中目标。菜单的遮罩不拥有次要按钮，所以这里越过
    阻挡区，解析到其下方的控件。

- int BlockHitsBelow()

- int NormalizedKind()
  - 事件分发前的规范化（本类三处读取点共用）：
    按压被控件持有（pressedId>=0）时到来的滚轮重标为移动。
    触屏拖动手势的每个采样都以滚轮形式到达（驱动只把不足
    一格的余量合成移动事件），而滚轮在按住时本就不滚动
    （见 ProcessEvent/ApplyEvent 的 wheel-pressed 分支）——
    它携带的唯一有效信息就是指针新位置。不重标的话，
    Layer 窗口拖动/缩放、文本选区延伸等一切以“kind==1
    且按住”驱动的事件期拖拽在触屏上收不到任何移动采样
    （按住拖动、控件纹丝不动，手势被下层当成了滚动）。
    桌面真滚轮按住时重标为移动是安全的：滚轮不改变指针
    位置，拖拽按同一坐标重算，等于无操作。

- bool PressOwnsWheel()
  - 按住期间到达的滚轮是否归按住的控件所有（拖拽手势）。
    桌面恒归控件：拖拽中误滚不再滚动任何内容，维持原语义。
    触摸上手势分扬：只有认领了拖拽（ClaimDrag：滑块/滚动条/
    分隔条/图表平移这类几何拖拽点）或命中区注册为文本(1)/
    缩放(4-8)光标类型——类型即"按住拖动"语义——的按压才拦住
    滚轮；列表行、按钮等普通命中区上，按住拖动就是滚动页面，
    与移动端惯例一致。

- void ClaimDrag()
  - 当前按压的控件认领后续的按住拖动（触摸手势分扬）。
    拖拽语义不在命中区类型里体现的控件（几何判定的滚动条
    滑块、分隔手柄、图表平移、专用拖拽把手）在按压帧调用；
    幂等，重复调用无害。桌面无作用（滚轮本就恒归控件）。

- int EventKind()
  - 正在处理的 OS 事件类型；当事件属于
    其他窗口时为 0（"无事件"）。原生事件状态是
    进程全局的：直接读取 window.EventKind() 的表面也会看到
    投递给兄弟或子窗口的点击和按键，并在 id 恰好
    对齐时触发自己的控件。每个窗口拥有的表面
    都必须询问其 App，而非共享的原生状态。

- bool EventIsMine()
  - 当正在处理的事件投递到了本 App 的窗口时为真。

- bool ClickFrameCurrent()
  - 当主点击（mouse-up）事件在本帧有效且
    可由当前渲染的表面处理时为真。即时模式
    表面应测试此函数而非 window.EventKind() == 3：
    点击被认领（此点击恰好打开了模态）时为 false，
    对绘制在*打开的模态遮罩之下*的内容也为 false——
    模态上一帧已存在（inputBlockPrevious），但其 BlockHitsBelow
    本帧尚未运行，意味着询问的代码渲染在其下方。
    模态自身的内部在其遮罩之后渲染，那里此函数为 true，
    因此点击永远不会穿过模态落到下面的页面。
    一次释放只属于它首次被读到的那一帧。持续动画（星空、
    spinner）会在下个事件到来前反复出帧，而 EventKind 停留
    在 3；不锁定的话按钮会在每个动画帧重新触发。同一帧内
    多个表面照常都能读到（绑定只记帧序，不做独占）。

- int FrameSeq()
  - 当前帧序号（BeginFrame 递增）。诊断用。

- bool ClickAvailable()

- void ClaimClick()
  - 将当前点击标记为本帧余下时间内已被消费。

- bool ClickClaimed()
  - 当前释放是否已被某表面认领（见 ClaimClick）。

- int ClickTarget()
  - 当前点击（mouse-up）落到的控件 id，无则 -1。

- int PressTarget()
  - 当前按下（mouse-down）落到的控件 id，无则 -1。

- int RightClickTarget()
  - 当前次要（右键）点击落到的控件 id，无则 -1。

- int RightPressTarget()
  - 当前次要（右键）按下落到的控件 id，无则 -1。

- bool DoubleClickNow()
  - 当完成的点击在双击时间窗内是同一控件上的第二次点击时
    为真（见 Ui.DoubleClicked）。

- void NoteClickTarget(int id)
  - 记录 `id` 上的完成点击，并在 400 ms 内
    同一 id 重复时标记双击。由鼠标释放路径调用。

- void NotePressStart(int id, int x, int y)
  - 快照按下目标/位置/时间，使手势（滑动、长按）
    可从按下起推导。由鼠标按下路径调用。

- void NotePressSentinel(int id)
  - 把本次按下的手势锚点改记为哨兵 id：即时模式表面
    （DataTable 单元格）的按压落在无 id 的几何区域上，
    长按轮询无法与真实控件区分。表面在按压时调用它，
    使随后的 PollLongPress(-2) 之类哨兵查询认领这次按压。
    不动焦点/按下状态，只改手势快照。

- void NoteRelease(int x, int y)
  - 根据按下到释放的位移推导滑动方向：0 无，
    1 左、2 右、3 上、4 下。由鼠标释放路径调用，
    因此在释放帧通过 SwipeDir 读取是有效的。

- int SwipeDir()
  - 当前释放帧解析出的滑动方向（见 NoteRelease）。

- int SwipeTarget()
  - 进行中的手势起始控件（按下目标）。

- bool TouchDevice()
  - 触摸优先设备（无鼠标悬停）：ANDROID/OHOS 编译期判定，与
    构造函数隐藏窗口 chrome 的闸门一致。依赖悬停才出现的交互
    （悬停显隐的手柄/图标、悬停提示、右键菜单）在此为 true 时
    应改走常显与长按等移动端等价物。桌面构建恒为 false——
    UiDriver 注入的合成事件与真实鼠标走同一条路径，悬停
    行为不受影响。

- bool PollLongPress(int id)
  - 当指针在 `id` 上按住超过阈值且未大幅移动时
    报告长按。按住期间安排低频后续帧，
    即使没有更多输入计时器也能推进；
    每次按下恰好返回一次 true。移动超过小容差则取消
    （该手势随后成为拖拽/滑动，而非长按）。
    `id` 允许负数哨兵（配合 NotePressSentinel）：哨兵查询
    无法与 focus.pressedId 比对（那里记录的是命中的真实
    控件 id，如表格行矩形），改查主键是否仍按住。

- bool LongPressFired()
  - 当前按住的手势已触发过长按时为真（见 PollLongPress）。
    标志在下一次按下时复位，因此释放帧仍能读到——
    上下文菜单据此忽略终结长按的那次释放（否则菜单
    刚打开就被松手当"点击外部"关掉）。

- int HeldPressMs()
  - 本次按压已持续的毫秒数；无按压时值无意义。
    触摸上的"长按提示"门控（Ui.HoldTipIn）用它把
    按住时长当作悬停稳定时长的等价物。


## BackdropFx (class)

带动画的窗口背景效果（"活皮肤"）。每个内置皮肤可携带
标志性的动态层（Theme.fx），由 App.RenderBackground 在节流的动画帧上
绘制在静态壁纸快照之上：
星场漂移（Dark）、极光浮动（Liquid Glass）、
下落的霓虹光束（Neon）、水墨飘丝（Chinese）、落花
（Peach Blossom）与数字雨（Matrix）。

所有效果都是无状态的：每个粒子的位置是
时钟和粒子哈希的纯函数，因此节流/不规则的帧
节奏不会使动画失步，也无需保留逐帧积分状态。
渲染只用廉价的 Canvas 原语（小填充、单字形
文本），软件渲染器在 ~15-25fps 的效果刷新下也能保持流畅。

- static List<int> damage;

- static int clipX;

- static int clipY;

- static int clipR;

- static int clipB;

- static List<int> TakeDamage()
  - 取走并清空脏区列表：x0,y0,w0,h0,x1,y1,w1,h1… 扁平 int 序列，
    供 App.FxPresent 只修复被画过的矩形。

- static void Mark(int x, int y, int w, int h)
  - 记录一个脏矩形，裁剪到当前效果区域。

- static void FR(Canvas c, int x, int y, int w, int h, int color)
  - 填充矩形并记录脏区。

- static void FC(Canvas c, int cx, int cy, int r, int color)
  - 填充圆并记录脏区（外扩 1px 容差）。

- static void DT(Canvas c, int x, int y, string s, int color, int fs)
  - 绘制文本并按字号估算记录脏区。

- static int KindStars()
  - 星场漂移（Dark，1）。

- static int KindAurora()
  - 极光浮动（Liquid Glass，2）。

- static int KindLightfall()
  - 下落霓虹光束（Neon，3）。

- static int KindInk()
  - 水墨飘丝（Chinese，4）。

- static int KindPetals()
  - 桃花瓣（Peach Blossom，5）。

- static int KindRain()
  - 数字雨（Matrix，6）。

- static int KindBokeh()
  - 失焦光球上浮（Sunset，7）。

- static int KindMesh()
  - 发光线框网格（Nebula，8）。

- static int KindFortune()
  - 新春装饰：漂云 + 翻滚金币（Fortune，9）。

- static int KindDarkGold()
  - 余烬上升 + 熔金光泽（Dark Gold，10）。

- static int KindDreamy()
  - 碎光闪烁 + 蝴蝶（Dreamy，11）。

- static int IntervalMs(int kind)
  - 某种类的重绘节奏（动画帧间隔毫秒）。慢速环境
    效果懒刷新；快速效果（光瀑、雨）略快一些。

- static int Hash(int i, int salt)
  - 小型整数哈希：由 (i, salt) 得到可复现的伪随机值，
    始终非负。

- static int Sin1000(int deg)
  - 通过粗略整数表计算 sin(deg) * 1000（10 度步长，线性
    插值）。对环境摆动足够用；避免在整个整数
    GUI 栈中使用浮点运算。

- static void Render(App app, Canvas c, int kind, int x, int y, int w, int h, int now, Theme t, int dpi)
  - 渲染一种效果到 [x,y,w,h]，帧内所有粒子矩形记入脏区
    （Render 开头重置）。kind 取 KindXxx() 常量；dpi 为 App 的
    缩放百分比，用于粒子尺寸。颜色取自 "effects" 样式部件。

- static int Px(int v, int dpi)
  - 按 DPI 百分比缩放尺寸，结果至少为 1px。

- static void Stars(Canvas c, int x, int y, int w, int h, int now, int color, int dpi)
  - 约 70 颗星缓慢斜向漂移（区域内环绕）、按各自相位闪烁，
    少数较大的星带一圈淡光晕。

- static void AuroraGlow(Canvas c, int cx, int cy, int r, int cr, int cg, int cb)
  - 一个柔光球：径向渐变圆盘（颜色按 r/g/b 分量给出）。

- static void Aurora(Canvas c, int x, int y, int w, int h, int now, int dpi)
  - 三个不同色的柔光球各绕锚点沿 Lissajous 式轨道缓慢游移。

- static void Lightfall(Canvas c, int x, int y, int w, int h, int now, int colorA, int colorB, int colorC, int dpi)
  - 14 束霓虹光束下落：向尾部渐隐的光带，加明亮的微光头部；
    三色轮换。

- static void Ink(Canvas c, int x, int y, int w, int h, int now, int dpi)
  - 四团水墨墨迹横向漂移、上下轻摆（半透明径向渐变）。

- static void Petals(Canvas c, int x, int y, int w, int h, int now, Theme t, int dpi)
  - 26 片桃花瓣下落、左右摇摆；每片由两枚错位圆盘构成，
    错位量随相位振荡，呈翻滚感。

- static void BokehOrb(Canvas c, int cx, int cy, int r, int color, int alpha)
  - 一个失焦光球：同心淡圆盘，边缘最亮，这样它
    读起来像失焦的高光而非实心球。

- static void Bokeh(Canvas c, int x, int y, int w, int h, int now, int colorA, int colorB, int colorC, int dpi)
  - 16 个失焦光球上浮（三色轮换），各带摆动相位避免轨迹重合。

- static void Mesh(Canvas c, int x, int y, int w, int h, int now, int colorA, int colorB, int dpi)
  - 线框晶格整体沿对角滑动一格并环绕，少量节点在交叉处脉动发光。

- static void Rain(Canvas c, int x, int y, int w, int h, int now, Theme t, int dpi)
  - 数字字符雨：约 2/3 的稀疏字符列下落，头部亮、8 格尾迹渐隐。

- static void Fortune(Canvas c, int x, int y, int w, int h, int now, int dpi)
  - Fortune（中国新年包）：祥云横向漂移、
    金币翻滚落下，以及元宝碎光缓缓闪烁。

- static void DarkGold(Canvas c, int x, int y, int w, int h, int now, int dpi)
  - Dark Gold（神话包）：余烬穿过烟雾上升，底部边缘
    有熔金般的光泽汇聚。

- static void Dreamy(Canvas c, int x, int y, int w, int h, int now, int dpi)
  - Dreamy（星光包）：闪烁的碎光加上几只蝴蝶
    沿缓慢的正弦路径飞行。


## BandGrid (class)

BandGrid：带分组表头的通用单元格网格（DevExpress BandedGrid
的轻量等位）。每格一个显示文本 + 一个可选数值；支持单元格级
着色回调、格内数据条、点选 / 拖选矩形 / 右键 / 双击，选中格
可批量赋值。即时模式自绘（GraphView 同款 RegisterRect +
ClickTarget 协议），数据变更后调 Poke()。
用法：
BandGrid g = new BandGrid();
g.Bind(7, 48).RowLabels(days).BandLabels(bands, 12)
.ColorOf(MyColorOf);
g.SetNum(r, c, 100);            // 逐格赋值（数值+文本）
g.SetSelectedNum(30);           // 选中格批量设值

- int rows;

- int cols;

- List<string> texts;

- List<int> nums;

- List<int> marks;

- List<string> rowLabels;

- List<string> bandLabels;

- int bandSpan;

- BandGridColorOf colorOf;

- int cellW;

- int cellH;

- int hoverR;

- int hoverC;

- int anchorR;

- int anchorC;

- bool dragSet;

- int ctxR;

- int ctxC;

- int actR;

- int actC;

- int barMax;

- int accent;

- int heatDeep;

- App lastApp;

- UiEvent Changed;

- UiEvent Context;

- UiEvent CellActivate;

- BandGrid()

- override string Kind()

- BandGrid Bind(int r, int c)
  - 行列数；单元格为空文本、无数值（-1）。

- BandGrid BindInit(int r, int c, int initNum)
  - 行列数 + 全部单元格初始化为同一数值（文本同值）。

- BandGrid RowLabels(List<string> labels)
  - 左侧行标签（每行一个，绘制在行首）。

- BandGrid BandLabels(List<string> labels, int span)
  - 顶部分组表头：每段标签横跨 span 列。

- BandGrid ColorOf(BandGridColorOf d)
  - 单元格级着色回调（返回 0 用默认底色）。

- BandGrid Heat(int deepColor)
  - 热力色带（深端锚色，0xAARRGGBB）：数值 1..5 映射为
    表面色→锚色的梯度。浅端在绘制时从当前皮肤的表面色
    派生（亮色皮肤得粉彩、暗色皮肤得暗色调），深端保留
    声明色相，换皮肤即换梯度。显式 ColorOf 优先于本接口。

- BandGrid CellSize(int w, int h)
  - 逻辑像素格尺寸（绘制时按 DPI 缩放）。

- BandGrid BarMax(int v)
  - 数据条满格值（0 关闭数据条，默认关）。

- BandGrid Accent(int argb)
  - 选中描边与数据条颜色（0xAARRGGBB）。

- BandGrid OnChanged(Action a)
  - 值/选中变化（含拖选批量赋值）后触发。

- BandGrid OnContext(Action a)
  - 右键单元格（读 ContextRow/ContextCol）。

- BandGrid OnCellActivate(Action a)
  - 双击单元格（读 CellRow/CellCol）。

- int ContextRow()
  - 最近右键命中的行号（无命中 -1）。

- int ContextCol()
  - 最近右键命中的列号（无命中 -1）。

- int CellRow()
  - 最近双击命中的行号（无命中 -1）。

- int CellCol()
  - 最近双击命中的列号（无命中 -1）。

- string TextAt(int r, int c)
  - 读单元格文本。

- void SetText(int r, int c, string s)
  - 写单元格文本（改后需 Poke() 刷新）。

- int NumAt(int r, int c)
  - 读单元格数值（未绑定返回 -1）。

- void SetNum(int r, int c, int v)
  - 数值 + 文本一并写（文本即数值十进制串）。

- void SetAllNum(int v)
  - 全部单元格写同一数值并刷新。

- int SelectedCount()
  - 当前选中格数量。

- void SelectAll()
  - 全选。

- void ClearMarks()
  - 清空选区。

- void SetSelectedNum(int v)
  - 对所有选中格批量写数值（文本同值）。

- void SetSelectedText(string s)
  - 对所有选中格批量写文本（不改数值）。

- void Poke()
  - 值或选区在窗体侧变更后调用：请求下一帧重画。

- override void OnMeasure(App app)

- int BandH(App app)

- int LabelW(App app)

- void Damage(App app)
  - 选区或悬停变化只伤矩阵自身矩形。

- override List<PropSpec> Props()
  - 覆写：设计器属性（几何与强调色；数据经 Bind/Data 面在代码侧给）。

- override void OnPaint(App app)


## Canvas (class)

由 zan_gui 运行时（软件渲染器）支撑的 2D 渲染画布。
所有绘制都进入像素缓冲（Surface），再呈现到操作系统窗口。

- [DllImport("zan_gui")]static extern int zan_gui_create_surface(int width, int height);

- [DllImport("zan_gui")]static extern int zan_gui_destroy_surface(int id);

- [DllImport("zan_gui")]static extern int zan_gui_surface_width(int id);

- [DllImport("zan_gui")]static extern int zan_gui_surface_height(int id);

- [DllImport("zan_gui")]static extern int zan_gui_write_pixels(int id, string path, int x, int y, int w, int h);

- [DllImport("zan_gui")]static extern void zan_gui_clear(int surfaceId, int color);

- [DllImport("zan_gui")]static extern void zan_gui_clear_rect(int surfaceId, int x, int y, int w, int h, int color);

- [DllImport("zan_gui")]static extern void zan_gui_fill_rect(int surfaceId, int x, int y, int w, int h, int color);

- [DllImport("zan_gui")]static extern int zan_gui_stat_read(int idx, int kind);

- [DllImport("zan_gui")]static extern int zan_gui_stat_top(int rank, int field);

- [DllImport("zan_gui")]static extern int zan_gui_stat_top_fill(int rank, int field);

- [DllImport("zan_gui")]static extern void zan_gui_draw_rect(int surfaceId, int x, int y, int w, int h, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_fill_rounded_rect(int surfaceId, int x, int y, int w, int h, int radius, int color);

- [DllImport("zan_gui")]static extern void zan_gui_draw_rounded_rect(int surfaceId, int x, int y, int w, int h, int radius, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_surface_rounded_rect(int surfaceId, int x, int y, int w, int h, int radius, int fill, int border, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_surface_rounded_rect_mask(int surfaceId, int x, int y, int w, int h, int radius, int corners, int fill, int border, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_fill_rounded_rect_mask(int surfaceId, int x, int y, int w, int h, int radius, int corners, int color);

- [DllImport("zan_gui")]static extern void zan_gui_draw_rounded_rect_mask(int surfaceId, int x, int y, int w, int h, int radius, int corners, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_shadow_rounded_rect(int surfaceId, int x, int y, int w, int h, int radius, int blur, int color);

- [DllImport("zan_gui")]static extern void zan_gui_blur_rect(int surfaceId, int x, int y, int w, int h, int radius);

- [DllImport("zan_gui")]static extern void zan_gui_blur_rect_cached(int surfaceId, int x, int y, int w, int h, int radius, int slot, int dirty);

- [DllImport("zan_gui")]static extern void zan_gui_blur_round_cached(int surfaceId, int x, int y, int w, int h, int radius, int slot, int dirty, int cornerRadius, int cornerMask);

- [DllImport("zan_gui")]static extern int zan_gui_blur_partial_miss_take();

- [DllImport("zan_gui")]static extern void zan_gui_snapshot_rect(int surfaceId, int x, int y, int w, int h, int slot);

- [DllImport("zan_gui")]static extern void zan_gui_snapshot_patch_rect(int surfaceId, int x, int y, int w, int h, int slot);

- [DllImport("zan_gui")]static extern int zan_gui_restore_rect(int surfaceId, int x, int y, int w, int h, int slot);

- [DllImport("zan_gui")]static extern int zan_gui_restore_sub_rect(int surfaceId, int x, int y, int w, int h, int slot);

- [DllImport("zan_gui")]static extern void zan_gui_surface_release(int surfaceId, int slot);

- [DllImport("zan_gui")]static extern int zan_gui_surface_dump(int surfaceId, string path);

- [DllImport("zan_gui")]static extern void zan_gui_fill_vgrad(int surfaceId, int x, int y, int w, int h, int colorTop, int colorBottom);

- [DllImport("zan_gui")]static extern void zan_gui_fill_vgrad_mask(int surfaceId, int x, int y, int w, int h, int radius, int mask, int colorTop, int colorBottom);

- [DllImport("zan_gui")]static extern void zan_gui_fill_grad_mask(int surfaceId, int x, int y, int w, int h, int radius, int mask, int dir, int colorFrom, int colorVia, int colorTo);

- [DllImport("zan_gui")]static extern void zan_gui_fill_circle(int surfaceId, int cx, int cy, int radius, int color);

- [DllImport("zan_gui")]static extern void zan_gui_draw_circle(int surfaceId, int cx, int cy, int radius, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_fill_radial(int surfaceId, int cx, int cy, int radius, int color, int innerAlpha);

- [DllImport("zan_gui")]static extern void zan_gui_draw_line(int surfaceId, int x0, int y0, int x1, int y1, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_draw_polyline(int surfaceId, nint pts, int n, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_draw_polyline_fx(int surfaceId, nint pts, int n, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_draw_polybatch(int surfaceId, nint pts, nint counts, int nPaths, int color, int thickness);

- [DllImport("zan_gui")]static extern void zan_gui_fill_sector(int surfaceId, int cx, int cy, int rInner, int rOuter, int a0Deg, int a1Deg, int color);

- [DllImport("zan_gui")]static extern void zan_gui_draw_text(int surfaceId, int x, int y, string text, int color, int fontSize);

- [DllImport("zan_gui")]static extern void zan_gui_draw_text_rot(int surfaceId, int x, int y, string text, int color, int fontSize, int angle);

- [DllImport("zan_gui")]static extern int zan_gui_measure_text(string text, int fontSize);

- [DllImport("zan_gui")]static extern int zan_gui_font_height(int fontSize);

- [DllImport("zan_gui")]static extern void zan_gui_text_stat_enable(int enabled);

- [DllImport("zan_gui")]static extern int zan_gui_text_stat_read(int idx);

- [DllImport("zan_gui")]static extern int zan_gui_get_dpi_scale();

- [DllImport("zan_gui")]static extern int zan_gui_image_width(string path);

- [DllImport("zan_gui")]static extern int zan_gui_image_height(string path);

- [DllImport("zan_gui")]static extern void zan_gui_image_evict(string path);

- [DllImport("zan_gui")]static extern void zan_gui_blit_image(int surfaceId, string path, int dx, int dy, int dw, int dh, int sx, int sy, int sw, int sh);

- [DllImport("zan_gui")]static extern int zan_gui_read_pixel(int surfaceId, int x, int y);

- [DllImport("zan_gui")]static extern int zan_gui_image_load_mem(string key, string data, int len);

- [DllImport("zan_gui", EntryPoint="zan_gui_image_load_mem")]static extern int zan_gui_image_load_mem_bytes(string key, byte[]data, int len);

- [DllImport("zan_gui")]static extern int zan_gui_image_load_svg(string key, string text, int len, int rasterW, int rasterH);

- [DllImport("zan_gui", EntryPoint="zan_gui_image_load_svg")]static extern int zan_gui_image_load_svg_bytes(string key, byte[]text, int len, int rasterW, int rasterH);

- [DllImport("zan_gui")]static extern void zan_gui_push_clip(int surfaceId, int x, int y, int w, int h);

- [DllImport("zan_gui")]static extern void zan_gui_pop_clip(int surfaceId);

- [DllImport("zan_gui")]static extern void zan_gui_reset_clip(int surfaceId);

- [DllImport("zan_gui")]static extern int zan_gui_set_render_backend(int mode);

- [DllImport("zan_gui")]static extern string zan_gui_render_backend();

- static int SetBackend(int mode)
  - 把本进程的光栅器切到 `mode`（见 `RenderBackend`），
    返回实际装上的后端：1 = GPU，0 = CPU。要了 GPU 而拿到 0 就是这台
    机器给不出 GL 上下文（远程桌面、虚拟机、CI），画面照旧由 CPU 光栅
    出来，不是失败。已存在的 surface 会带着当前内容一起搬过去，切换
    不会让窗口闪白。

- static string Backend()
  - 当前生效的光栅器名字（"cpu" / "gl"），供设置页与日志显示。

- int surfaceId;

- int SurfaceId()
  - 本画布的 zan_gui surface id（游戏场景合成 ScenePresent 用）。

- Canvas(int width, int height)

- void Destroy()

- int Width()

- int Height()

- int WritePixels(string path, int x, int y, int w, int h)

- int DumpRaw(string path, int x, int y, int w, int h)
  - 把整个 surface 转存到 .raw（BGRA + 24 字节头），
    用于 toolbox 工具箱的"保存图片"。rect 为 0 0 0 0 时转存
    整张画布；非空时仅取该矩形。返回 0=成功，非 0=错误。

- void Clear(int color)
  - 用颜色（0xAARRGGBB）清空整个 surface。

- void ClearRect(int x, int y, int w, int h, int color)
  - 只清空一个矩形：与 `Clear` 一样*存入*颜色
    （含 alpha），不与已有像素混合。损伤裁剪帧用它在损伤区内重建
    窗口底色——换成 FillRect 就是把半透明底色又叠一遍上一帧，
    玻璃皮肤下每来一个局部帧就深一点。

- static int RasterStat(int idx, int kind)
  - 一个栅格化工作计数器：`kind` 0 = 调用次数，1 = 接触
    像素数（千为单位；读 kind 1 会清零计数器）。`idx` 选择
    图元：0 不透明填充，1 混合填充，2 渐变，3 圆角
    矩形，4 径向，5 模糊计算，6 模糊缓存命中，7 图像 blit，
    8 快照，9 恢复，10 字形，11 混合填充走 4 宽路径的像素，
    12 混合填充逐像素处理的像素。供 App 的帧分析器使用。

- static void TextStatEnable(bool enabled)

- static int TextStat(int idx)
  - 开关文本栅格化统计（配合 `TextStat`）。
    读取文本栅格化统计：`idx` 选择指标（0=字形数，
    1=光栅耗时等，与 TextStatEnable 配套）。供帧分析使用。

- static int RasterTopBlend(int rank, int field)
  - 本帧面积最大的半透明填充，按面积排名：`field` 0 = 面积（千像素），
    1 = x，2 = y，3 = w，4 = h（读 4 会清除该
    条目）。指出主导混合的图层。

- static int RasterTopFill(int rank, int field)
  - 本帧面积最大的不透明填充，字段同 RasterTopBlend。被后面
    图层再次覆盖的不透明填充就是纯重复绘制，这里指出是哪几块。

- [DllImport("zan_gui")]static extern string zan_gui_mem_report();

- static string MemReport()
  - 栅格化缓存构成（单行，MB）：字形图集/覆盖池/解码
    图片/surface/模糊槽/快照槽/纹理。把进程内存归因到具体
    缓存用——进程 RSS 混进了共享代码页和驱动缓冲，说不清
    这笔账。Android 与 OHOS 驱动带此导出（桌面驱动重建时
    再放开门控），其余平台返回空串。

- void FillRect(int x, int y, int w, int h, int color)
  - 用纯色（0xAARRGGBB）填充矩形。与 ClearRect 不同，
    alpha 小于 255 时与已有像素混合，适合玻璃/叠加层。

- void PushClip(int x, int y, int w, int h)
  - 将后续绘制限制在当前裁剪区与
    (x,y,w,h) 的交集中。嵌套 push 只会缩小区域。需与
    PopClip 配对。裁剪区在每帧开始时（Clear）重置为整个 surface，
    因此容器无需手动重置。

- void PopClip()
  - 恢复最近一次 PushClip 保存的裁剪区。

- void ResetClip()
  - 丢弃所有裁剪区，重新在整个 surface 上绘制。

- void DrawRect(int x, int y, int w, int h, int color, int thickness)
  - 绘制矩形轮廓。

- void FillRoundRect(int x, int y, int w, int h, int radius, int color)
  - 填充圆角矩形。

- void DrawRoundRect(int x, int y, int w, int h, int radius, int color, int thickness)
  - 绘制抗锯齿圆角矩形轮廓，其圆角
    紧贴同几何的 FillRoundRect（带边框的圆角表面请用它
    代替 DrawRect）。

- void FillRoundRectIn(int x, int y, int w, int h, int radius, int corners, int color)
  - 填充圆角矩形，只圆化 `corners` 指定的角
    （Corner.TL|TR|BR|BL，四角全圆用 Corner.All）。焊接
    相邻元素——一组按钮、紧贴面板的标签页——会这样
    把共享接缝修成直角，而不是留下两个圆角
    挤在一起。

- void DrawRoundRectIn(int x, int y, int w, int h, int radius, int corners, int color, int thickness)
  - 描边 FillRoundRectIn 形状的轮廓。

- void SurfaceRoundRect(int x, int y, int w, int h, int radius, int fill, int border, int borderThickness)
  - 一次调用同时填充圆角矩形并描边其轮廓：
    边框先与填充色合成，再一次应用圆角覆盖率，避免外沿重复混合。
    边框向内扩展，厚度小于等于 0 时只填充；透明边框保留填充。
    这是卡片、弹窗、提示框和 chip 等共用的带边框表面惯用法。
    此操作不裁剪后续子控件绘制。

- void SurfaceRoundRectIn(int x, int y, int w, int h, int radius, int corners, int fill, int border, int borderThickness)
  - SurfaceRoundRect 的指定圆角版本；覆盖率只合成一次。

- void ShadowRoundRect(int x, int y, int w, int h, int radius, int blur, int color)
  - 圆角矩形的柔和投影：以圆角 SDF（外轮廓到形状的
    有符号距离）在整个 blur 带上做 smoothstep 衰减，而非逐圈扩张
    描边。几何连续，角部不会出现楔形缝或同心弧；每个像素只写一次，
    半透明阴影色合成到标称 alpha，不随层叠变黑。radius <= 0 退化为
    矩形阴影；blur <= 0 退化为硬填充。

- void BlurRect(int x, int y, int w, int h, int radius)
  - 就地盒式模糊一个矩形区域（毛玻璃
    背景）。先画背景，再模糊，然后叠一层半透明
    色调。`radius` 为模糊强度（px，上限 40）。

- void BlurRectCached(int x, int y, int w, int h, int radius, int slot, bool dirty)
  - 与 BlurRect 相同的毛玻璃模糊，但将模糊输出缓存到
    `slot`。当 `dirty` 为 false 且区域几何
    未变时，直接用普通拷贝恢复缓存像素，而不是
    重算（昂贵的）高斯模糊——因此屏幕上的动画
    （spinner、toast）不再每帧重模糊静态背景。
    每个玻璃表面传一个稳定的 slot，并在玻璃后内容
    可能已变化时（输入、滚动、缩放、换肤）传 dirty=true。

- void BlurRoundCached(int x, int y, int w, int h, int radius, int slot, bool dirty, int cornerRadius, int cornerMask)
  - 缓存毛玻璃模糊并裁剪到圆角矩形：
    模糊输出只写入圆角半径遮罩内，使玻璃
    面板的边角保留清晰背景，并与其上覆盖的半透明
    圆角色调对齐（方形模糊盖在圆角色调下会留下
    色调永远无法重绘的模糊边角）。`cornerMask` 是 Corner
    位集（四角全圆用 Corner.All()）。

- static int TakeBlurPartialMiss()
  - 自上次调用以来，有多少块玻璃是在「源背景只有一部分是
    本帧新画的」情况下重新模糊的（损伤裁剪帧里跨出条带的面板）：
    卷积会把条带外上一帧的*已合成*像素（面板色调、文字）混进来，
    结果与整帧渲染不再等价。调用方据此把下一帧升级成整窗帧。
    读取即清零。

- void SnapshotRect(int x, int y, int w, int h, int slot)
  - 把区域像素快照进 `slot`，便于之后用
    RestoreRect 无需重绘即可恢复。用于缓存静态
    背景（如壁纸），使纯动画帧跳过
    重绘。

- void SnapshotPatchRect(int x, int y, int w, int h, int slot)
  - 把 [x,y,w,h] 的当前像素补进 `slot` 里已有的快照
    （不改变槽的几何）：损伤条带帧只重画了条带，用它把条带的
    新基面折回整窗快照，之后的整窗恢复（如特效拍的
    RestoreRect(0,0,W,H)）继续几何匹配。槽里没有本表面的有效
    快照、或矩形越出快照范围时为空操作。

- bool RestoreRect(int x, int y, int w, int h, int slot)
  - 恢复先前由 SnapshotRect 捕获的区域。
    若快照存在且几何匹配（说明区域现已绘制）
    则返回 true；若调用方必须正常绘制它
    则返回 false。

- bool RestoreSubRect(int x, int y, int w, int h, int slot)
  - 只恢复 `slot` 中与 [x,y,w,h] 相交的部分；
    矩形无需匹配快照几何，因此许多小块受损
    区域无需整体拷贝回快照即可被修复。
    slot 中无有效快照时返回 false。

- bool Dump(string path)
  - 调试：把表面像素写成 24 位 BMP（无压缩），
    供无头环境比对画布内容与屏幕实际显示。

- void ReleaseSlot(int slot)
  - 释放快照 slot 拥有的像素缓冲并使其失效，
    把内存归还而不是在整个会话期间保留。当
    缓存的区域滚出视野时使用（如嵌在
    网格单元格中的图表）。对空闲 slot 调用安全，空操作。

- void FillVGrad(int x, int y, int w, int h, int colorTop, int colorBottom)
  - 用自上而下线性渐变填充矩形
    （0xAARRGGBB 端点，不透明）。用于渐变壁纸。

- void FillVGradMask(int x, int y, int w, int h, int radius, int mask, int colorTop, int colorBottom)
  - 用自上而下线性渐变填充圆角矩形。
    圆角弧已抗锯齿（1px 混合边缘），轮廓与
    FillRoundRect 相同——在 FillRoundRect 上平铺 FillVGrad 会
    用不透明渐变替换弧的混合像素，使
    边角锯齿化。mask 与 FillRoundRect 的角位掩码相同。

- void FillGradMask(int x, int y, int w, int h, int radius, int mask, int dir, int colorFrom, int colorVia, int colorTo)
  - 用线性渐变填充圆角矩形：`dir` 0 = 自上而下、
    1 = 自左向右、2 = 向右下对角、3 = 向左下对角，
    `colorVia` 非 0 时作为 50% 处的中间色停靠点。
    端点可带 alpha（逐像素混合），圆角弧抗锯齿且与 FillRoundRect
    同一轮廓，因此渐变面板/按钮的圆角不会出现阶梯毛刺。
    mask 与 FillRoundRect 的角位掩码相同。

- void FillCircle(int cx, int cy, int radius, int color)
  - 填充圆。

- void DrawCircle(int cx, int cy, int radius, int color, int thickness)
  - 以给定粗细描边圆轮廓，
    圆心在半径处（抗锯齿）。

- void FillRadial(int cx, int cy, int radius, int color, int innerAlpha)
  - 填充柔和径向辉光：alpha 从中心的 innerAlpha
    （0..255）平滑衰减到半径处的 0，用于发光效果。仅用 color 的
    RGB。

- void DrawLine(int x0, int y0, int x1, int y1, int color, int thickness)
  - 绘制线段。

- void DrawPolyline(List<int> xs, List<int> ys, int color, int thickness)
  - 将整条折线作为一条抗锯齿笔划绘制。路径
    单次扫描按覆盖率栅格化，因此段接缝圆滑，
    且没有像素被混合两次（拐角无亮缝）——
    不同于用 DrawLine 逐段绘制同一路径。

- void DrawPolylineFx(List<int> xs, List<int> ys, int color, int thickness)
  - 绘制顶点坐标为 16.8 定点数（1/256 px）的折线。
    亚像素精度构造的平滑曲线在栅格化时保持
    真实形状——距离场采样理想几何，
    而非整数取整的阶梯，这正是
    圆看起来平滑的原因：每个像素度量真实曲线，而非
    量化轮廓。

- void DrawPolyBatch(List<int> xs, List<int> counts, int color, int thickness)
  - 一次覆盖缓冲周期绘制 N 条互不相连、同色的折线。
    xs 为全体路径顶点的扁平交错数组，counts[i] 为第 i 条路径的
    顶点数。密集多行图（数千行的平行坐标）逐行调用 DrawPolyline
    会为每行付出一次完整的 GL 覆盖缓冲清除+合成；分桶后每帧
    每色仅一次，是大数据图表不卡的关键。

- void FillSector(int cx, int cy, int rInner, int rOuter, int a0Deg, int a1Deg, int color)
  - 填充环扇区（饼/甜甜圈切片）。角度为度，0 在
    12 点钟方向，顺时针。rInner=0 得实心饼切片。

- void DrawArc(int cx, int cy, int rInner, int rOuter, int a0Deg, int a1Deg, int color, int thickness)
  - 描边环扇区弧（饼/甜甜圈切片的轮廓）。
    角度为度，0 在 12 点钟方向，顺时针。画成外缘一圈细填充
    环，无需单独的原生描边图元；
    粗细以设备像素计。

- void DrawText(int x, int y, string text, int color, int fontSize)
  - 在指定位置绘制文本。

- void DrawTextRot(int x, int y, string text, int color, int fontSize, int angleDeg)
  - 绘制绕锚点旋转的文本。`(x, y)` 是未旋转行盒的左上角，
    整行文本绕它刚性旋转；`angleDeg` 为度，正 = 顺时针（CSS
    `transform: rotate()` 约定），钳制在 [-90, 90]。颜色 alpha 参与
    混合（0 视为不透明，同 DrawText）。旋转后的整行作为一块覆盖度
    贴片缓存，同一 (文本, 字号, 角度) 只光栅一次。水印等倾斜平铺
    文本用它与 MeasureText 自己算包围盒。

- void DrawTextCentered(int rx, int ry, int rw, int rh, string text, int color, int fontSize)
  - 在矩形内居中绘制文本。

- static int MeasureText(string text, int fontSize)
  - 测量文本宽度（像素）。

- static int FontHeight(int fontSize)
  - 返回字体高度（像素）。

- static int FontPadTop(int fontSize)
  - 栅格化器在 FontHeight 内字形墨迹上方留下的空行
    （字体的内部 leading / 行距）。
    
    由各后端已导出的两个度量推导，而非
    单独调用度量：`fontSize` 是所请求的 em 尺寸，
    `FontHeight` 是栅格化器为其报告的行盒，
    二者之差正是它加的 leading。将此逻辑留在 Zan 中也
    使原生 ABI 不变——用户项目链接的预编译
    各平台驱动中没有新的 `zan_gui` 导出。

- static int CenterTextY(int rectY, int rectH, int fontSize)
  - 在 [rectY, rectY+rectH] 内光学居中一行文本的顶部 y：
    居中墨迹盒而非整个字体盒，因此
    文本不会因半个内部 leading 而偏低。所有
    垂直文本居中都应走此函数。

- static int FontLeadTop(int fontSize)
  - 字体内部 leading 位于字形墨迹上方的部分。
    栅格器按基线放置字形：墨迹顶部在 y 之下约一整个
    leading（ascent 头部空间盖过它的只剩一点），但
    墨迹盒也比 fontSize 矮（大写字母不含下延部），两者
    方向相反、大部分相抵——实测（Windows GDI Segoe/微软雅黑、
    Android FreeType Roboto/Noto CJK，48px 按钮探针）只补
    四分之一 leading 时大写拉丁与 CJK 标签都落在 ±1px 内；
    补一半（旧值）文本整体偏高 2~3px，全补则偏低。

- static int CenterTextYAt(int centerY, int fontSize)
  - 以 `centerY` 为中心光学居中一行文本的顶部 y（
    刻度、节点、切片标签——任何按中线而非
    按盒子定位的东西）。墨迹盒横跨 `centerY`，因此文本不会
    因半个内部 leading 而偏低，与 CenterTextY 一致。

- void DrawIcon(int x, int y, int box, int color, int codepoint)
  - 在盒子内以矢量图元绘制图标字形（Unicode 码点），
    使其在所有平台外观一致。
    形状见 Gui.IconVector。

- void DrawStyledText(StyleBox s, int x, int y, string text, int fallbackColor, int fallbackFont)
  - 以已解析样式携带的颜色和字号绘制文本，
    CSS 未设置的内容回退到调用方的值。
    调用方自行解析样式（Style.Of / Style.Part），因此文本
    绘制无需中间控件。

- static string GlyphSvg(string name)
  - DrawGlyph/DrawGlyphIn 共用的 SVG 候选名解析：语义名先过
    Icon.SvgName 差异映射与 IconSvg 别名，命中 IconSvgData 才返回，
    否则返回 ""（调用方回退 IconVector 手绘，行为同从前）。

- void DrawGlyph(string name, int x, int y, int size, int color)
  - 在 (x,y) 的 `size` 盒子内绘制 `name` 代表的图标
    （图标集见 Gui.Icon）。优先画 SVG 图标集（跨平台一致、不依赖
    系统字体），SVG 里没有的名字回退 IconVector 矢量图元；
    两者都不认识时什么都不画。

- void DrawGlyphIn(string name, int rx, int ry, int rw, int rh, int size, int color)
  - 在矩形内居中绘制 `name` 代表的图标，这正是
    控件内图标无论控件高度
    如何都保持对齐的原因。SVG 优先、IconVector 回退，同 DrawGlyph。

- static int ImageWidth(string path)
  - 图像文件（PNG/JPEG/BMP/GIF/TGA/PNM/PSD，WebP）或已注册
    的内存图像 key 的像素宽度，首次使用时解码并缓存。无法加载时
    返回 0。

- static int ImageHeight(string path)
  - 图像文件或内存图像 key 的像素高度。参见 ImageWidth。

- static void EvictImage(string path)
  - 丢弃缓存的解码图像（文件路径或 ImageLoadMem /
    ImageLoadSvg 注册的内存 key），使下次绘制重新加载源。

- static int ImageLoadMem(string key, string data, int len)
  - 把一段原始图像字节注册到 `key` 下并返回图像宽度，失败
    返回 0。解码支持 PNG/JPEG/BMP/GIF/TGA/PNM/PSD（stb_image）与
    WebP（内置 libwebp，按 RIFF 头识别）。注册后这个 key 可以像
    文件路径一样传给 ImageWidth/ImageHeight/BlitImage/EvictImage；
    重复注册同一个活跃 key 是无操作。key 约定用 `mem:` 前缀。

- static int ImageLoadMem(string key, byte[]data, int len)
  - byte[] 重载，参见 ImageLoadMem(string, string, int)。

- static int ImageLoadSvg(string key, string svg, int rasterW, int rasterH)
  - 把 SVG 文本光栅化到 `key` 下并返回光栅宽度，失败返回
    0。rasterW/rasterH 是目标盒：文档保持纵横比 contain 适配；
    <= 0 时用文档固有尺寸。之后这个 key 同样可以像文件路径一样
    使用（key 约定用 `mem:` 前缀）。

- static int ImageLoadSvg(string key, byte[]svg, int len, int rasterW, int rasterH)
  - byte[] 重载（二进制安全的 SVG 源，例如 base64 data URI
    解出的字节），参见 ImageLoadSvg(string, string, int, int)；
    `len` 是字节数。

- int GetPixel(int x, int y)
  - 读一帧里的一个像素（0xAARRGGBB），越界返回 -1。
    供测试断言采样结果，应用代码一般不需要。

- void BlitImage(string path, int dx, int dy, int dw, int dh, int sx, int sy, int sw, int sh)
  - 把图像文件的矩形区域绘制到画布（按路径解码一次并
    缓存）并缩放到 (dw,dh)：缩小时对覆盖到的源像素做面积平均
    （box filter，避免 nearest 丢列/丢行的闪烁），放大或 1:1 时
    按目标像素中心最近邻采样。传 sw=0,sh=0 以整幅图像为源。

- void DrawImage(string path, int x, int y)
  - 在 (x,y) 处不缩放地绘制整幅图像文件。

- void DrawDivider(int x, int y, int width, int color)
  - 绘制水平分隔线（1px 高）。

- void FillRectColor(int x, int y, int w, int h, Color col)
  - FillRect 的 Color 对象重载。

- void DrawTextColor(int x, int y, string text, Color col, int fontSize)
  - DrawText 的 Color 对象重载。

- static int GetDpiScale()
  - 当前显示器的 DPI 缩放倍数（100%=1，150%=1.5）。
    所有逻辑坐标→设备像素的换算都应乘以它；
    控件布局一般不必手动调用（App 层已统一处理），
    自绘贴图/光标等直接按像素落笔的场景才需要。

- [DllImport("zan_gui")]static extern int zan_gui_mesh_create(int surfaceId, nint verts, int count, nint indices, int indexCount);

- [DllImport("zan_gui")]static extern int zan_gui_draw3d(int surfaceId, int mesh, nint mvp, int color, string texture);

- public int MeshUpload(Mesh3D mesh)
  - 上传网格，返回 mesh id（0 = 失败/当前后端不支持）。
    数据被运行时复制，Upload 返回后即可释放 Mesh3D 的缓冲。mesh id
    在切换 RenderBackend 后失效（需要重新 Upload）。

- public int DrawMesh3D(int mesh, float[]mvpColumnMajor, int color, string texture)
  - 按模型-视图-投影矩阵（Mat4.Mul(P, Mat4.Mul(V, M)).ToColumnMajor()
    组出）把 mesh 画进画布的 3D 层：深度测试 + 纹理映射 + 半兰伯特
    光照（法线着色，免配置）。texture 为图像路径或 ImageLoadMem 的
    "mem:" key，null/"" 用 1x1 白纹理。返回 1 = 已画，0 = 当前
    后端不支持 3D（CPU 兜底档），调用方可换 2D 回退。


## ChildWindow (class)

Base class for every secondary top-level window (dialogs, settings,
pickers that need their own OS window).

A child window is a top-level OS window of its own, so it needs more than a
shared look: it has to be woken, animated, event-routed, pumped and closed
by the main window's loop. Doing that per window meant wiring each new
window into six places in the host loop, and every miss showed up as a
window that stopped repainting. Here the plumbing lives once, and
`ChildWindows` keeps parent-owned windows in the registry `Form.Run()`
iterates. A caller running before its main window exists can instead use
`OpenStandalone` and `PumpStandaloneUntil`; that path owns its event
loop and is deliberately not registered in `ChildWindows`.

A subclass supplies the title/size/widget-id baseline, builds `root` (a
retained Control tree), wires handlers, and may override `Pending()`
(extra repaint reasons) and `AfterFrame()` (work to do once the frame is
on screen). Windows rendered by an immediate-mode widget (the Wizard) set
a render callback instead of building a tree.

Binding channel: controls declaring a `bind` path (a design-time
declaration owned by the designer, Serialize and GenForm — see
`Control.bindPath`) are synced against this window's JsonValue model
every frame: model -> UI before the frame (`SyncFromModel`), user
edits -> model after it (`SyncChangedNode`). The per-control snapshot
that detects user edits lives HERE, not on Control — it is a runtime
cache of this render loop, not a declaration. This is the dialog
"state entity" string channel; in-code realtime binding goes through
`Binding<T>` (System/Binding.zan, stdlib standards §6.1).

- App host;

- Control root;

- HandlerRegistry handlers;

- JsonValue model;

- bool open;

- bool destroyed;

- int idBase;

- Action renderCb;

- List<Control> boundKeys;
  - 绑定快照旁表（`Control.bindSnapshot` 已拆除）：SyncFromNode
    记录"模型侧确认的控件值"，SyncChangedNode 据此判断用户是否
    编辑过。按控件引用线性查找——对话框的绑定控件是个位数到
    几十个，每帧的引用比较是纳秒级。树上移除的控件残留条目
    永不命中（键是引用），随窗口生命周期一并释放。

- List<string> boundSnaps;

- ChildWindow()
  - 构造：全部字段置空/默认（idBase 基线 900000）。

- virtual string Title()
  - OS window caption.

- virtual int Width()
  - Initial client size, in unscaled pixels.

- virtual int Height()
  - 初始客户区高度（未缩放像素）。

- virtual bool ShowMinimize()
  - Caption buttons a secondary window keeps (skin and pin never appear;
    a dialog that is not resizable can also drop maximize).

- virtual bool ShowMaximize()
  - 是否保留最大化按钮。

- virtual int IdBase()
  - Fixed WidgetId baseline for this window's frames. The main window never
    rewinds the process-wide counter, so a child that did not pin its own
    baseline would get different ids every frame and its buttons would
    never see the hover/press resolved on the previous frame.

- App Host()
  - The underlying App, for hosts that render immediate-mode widgets
    (BeginFrame/PresentFrame) from a render callback.

- void SetRender(Action a)
  - Immediate-mode render mode: when set, the pump calls `a` instead of
    rendering the Control tree. The callback owns BeginFrame/PresentFrame
    and dispatches whatever action its widget reported.

- void SetRoot(Control tree, JsonValue m)
  - Mounts the window's control tree and the JSON model the `bind` paths
    of its controls read from / write to. Subclasses call this at the end
    of their BuildUi, then register handler names with Handle() and finish
    with Wire().

- void Handle(string name, Action a)
  - Registers (or replaces) the Action bound to a design handler name;
    Wire() resolves each control's `on<Event>` names through this table.

- void Wire()
  - Resolves every recorded `on<Event>` handler name to its Action and
    pushes the model into the bound controls (state -> UI). Call once
    after all Handle() registrations.

- void WireNode(Control c)
  - 递归解析控件树上的 `on<Event>` 处理器名并绑定到已注册的 Action。

- void SyncFromModel()
  - 把绑定的状态实体值推入每个声明了 `bind` 路径的控件
    （state -> UI）。不通过 SetProp 暴露 “value”/“text” 的控件
    会忽略写入，因此对所有控件类型都安全。

- void SyncFromNode(Control c)
  - 递归把模型值推入声明了 bind 路径的控件（值变化才写），
    并记录绑定快照。

- void SyncChangedNode(Control c)
  - 把每个绑定控件的当前值读回状态实体（UI -> state）。

- void RecordSnapshot(Control c, string v)
  - 记录（或更新）控件绑定属性的模型侧确认值——上次由模型
    写入/确认时 `BoundValue` 的读数，作为"用户是否编辑过"的基准。

- string SnapshotOf(Control c)
  - 控件的上一次模型侧确认值；从未记录（新绑定控件首次回写
    前的防御路径）按被拆字段的原初始值语义返回 ""。

- string BoundValue(Control c)
  - 控件绑定属性的当前值：显式 bindProp 优先，否则取 value、
    再取 text。

- void WriteBoundValue(Control c, string s)
  - 把字符串值写回模型节点：按现有节点的类型转换为
    bool / 数值 / 字符串，保持模型原有的形状。

- virtual bool Pending()
  - Extra reasons to repaint: actions raised by handlers between
    frames, background work still running, ...

- virtual void AfterFrame()
  - Runs right after the frame is presented (model sync, deferred work).

- virtual void OnLanguageChanged(string lang)
  - 语言切换广播：宿主把 UI 语言切到 `lang`（"zh" / "en" 语言码）后，
    对每个开着的子窗口调用一次。子类在这里重填 zform 的设计期
    文案（ApplyTexts 模式）并刷新依赖语言的静态扇出字段；窗口
    标题由基类重取 Title() 处理，子类无需关心。

- void OpenHost(App parent)
  - Creates and shows the window with the parent's look, then registers it
    with the pump. Subclasses call this at the end of their `Open`.

- void OpenStandalone()
  - Creates a standalone top-level host for callers that run before the
    application's main window exists. It deliberately does not inherit
    parent styling or enter the shared ChildWindows registry, so it opens
    on the product default skin (see `StandaloneSkin`) instead of the dark
    baseline every host window is constructed with.

- virtual string StandaloneSkin()
  - Skin pack a standalone window opens with. There is no parent window to
    follow, so the default is the light skin the plain `App` constructor
    preselects; an unknown name leaves the look untouched.

- void PumpStandaloneUntil(ChildWindowStop stop)
  - Drives this window without a parent application's loop. ProcessEvent
    supplies the blocking event wait when there is no redraw or animation,
    so a background job can be observed without a busy loop.

- void PumpStandaloneUntilKeepOpen(ChildWindowStop stop)
  - Drives the standalone window without closing it when the stop condition
    becomes true. The caller owns the final Close().

- void PumpStandaloneUntilMode(ChildWindowStop stop, bool closeWhenDone)
  - 独立事件泵的公共实现：泵宿主事件并逐帧渲染，直到窗口关闭
    或 stop() 为真；closeWhenDone 决定结束时是否顺带 Close()。

- void Render()
  - Renders one frame, with this window's widget ids pinned: the render
    callback when one was set, otherwise the retained Control tree.

- bool NeedsRedraw()
  - 窗口开着且有帧要出（宿主标脏或 Pending()）时为 true。

- bool IsOpen()
  - 窗口是否仍开着。

- bool OwnsWindow(nint hwnd)
  - 该 OS 窗口句柄是否归本窗口所有。

- void ApplyEvent(nint hwnd)
  - Applies one OS event addressed to this window; a close event just marks
    it closed (the main loop drops it on the next pump).

- virtual void OnCloseRequested()
  - Called when the user clicks the window's close button. Subclasses can
    mirror the behaviour of their internal "done"/"cancel" handlers here.

- void Close()
  - 关闭窗口：向 OS 发送关闭请求、标记关闭并立即 Teardown
    （幂等，见 Teardown）。

- void Teardown()
  - Destroys the OS window for good. `Window.Close()` only *requests* a
    close (it posts the close event to the window's own loop); a child the
    host has already let go of never reads that event, so without this the
    window lingers on screen, unpainted and dead to clicks. Idempotent.

- void RequestRedraw()
  - 请求宿主重绘（窗口开着时）。

- void ApplySkin(int i)
  - 转发给宿主换肤（窗口开着时）。

- void SetWindowOpacity(int percent)
  - 转发给宿主设置窗口不透明度（0-100，窗口开着时）。

- void SetUserWallpaper(string path, int opacity)
  - 转发给宿主设置用户壁纸与不透明度（窗口开着时）。

- nint WindowHandle()
  - 宿主窗口的 OS 句柄。

- void FollowSkin(int i)
  - 主窗口换肤后同步本副窗口并重绘。

- void FollowCaptionTips(App src)
  - 主窗口换了界面语言：已经开着的副窗口的标题提示也得跟上。

- void FollowOpacity(int percent)
  - 主窗口调不透明度后同步本副窗口。

- void FollowWallpaper(string path, int opacity)
  - 主窗口换壁纸后同步本副窗口。

- int AnimNextMs()
  - 宿主的下一次动画截止时刻（毫秒时钟；窗口关闭返回 -1）。

- int FxNextMs()
  - 宿主的下一次特效截止时刻（毫秒时钟；窗口关闭返回 -1）。


## ChildWindows (class)

The registry of open child windows the main window's loop drives.

`Form.Run()` asks it, once per iteration, whether anything needs a
repaint, folds in the animation deadlines, routes the OS event to whoever
owns it, and pumps a frame for each open window. Nothing in the loop names
an individual window, so a window opened from a child window is driven the
same way as one opened from the ribbon.

- static List<ChildWindow> wins;

- static FilePicker picker;

- static List<FilePicker> pickers;
  - 组件自建的附加选择器（Upload 内建选文件弹窗等）。单一 `picker`
    槽归应用 shell 注册的共享选择器所有（IDE 的 pathPicker）；这批
    由组件按需登记，数量不限。PumpAll/Route/Wants 统一照顾两处。

- static List<ChildWindow> All()
  - 注册表（惰性创建）。

- static void Register(ChildWindow w)
  - 把窗口加入主循环驱动队列（OpenHost 自动调用）。

- static void ApplyLanguage(string lang)
  - 语言切换广播：对每个开着的子窗口调用 OnLanguageChanged，并把
    自绘标题栏的文字按新语言的 Title() 重设。宿主（IDE 外壳）在
    设置窗回报语言变更时调用一次（lang 为 "zh"/"en" 语言码）；
    之后开的新窗口自然用新语言。

- static void RegisterPicker(FilePicker p)
  - Registers the shared file picker so the pump renders it while open;
    the picker dispatches its result through its own UiEvents.

- static bool RegisterComponentPicker(FilePicker p)
  - 登记一个组件自建的选择器（Upload 内建弹窗）。同一实例重复登记
    是无操作；`PrunePickers` 在它关闭后移出，因此宿主应在每次打开
    时重新登记（组件复用同一 picker 实例）。返回 true = 首次登记。

- static void Prune()
  - Forgets windows that have closed.

- static bool AnyOpen()
  - 是否还有开着的子窗口。

- static bool Wants()
  - True when any open window has a frame to draw (so the loop polls
    instead of blocking).

- static bool AnyPickerWants()
  - 任一组件选择器开着且要求重绘（轮询判据；FilePicker 文档约定：
    弹窗开着时主循环不得阻塞在 WaitEvent 上）。

- static bool AnyPickerOpen()
  - 任一组件选择器开着（主循环用它收紧阻塞等待）。

- static int Deadline(int deadline)
  - Folds every open window's animation / effect deadline into `deadline`
    (-1 means "no deadline"), so idle waits wake up for child animations.

- static bool PumpPickers(App main)
  - 组件选择器开着时把它的重绘需求折叠进主应用：轮询判据（开着时
    不得阻塞在 WaitEvent 上）+ 弹窗要出帧时唤醒主循环。

- static void PrunePickers()
  - Prunes component pickers that have closed (each Upload keeps its own
    picker instance alive for the next open; only the registry entry goes).

- static bool TickDue(int now)
  - Requests a repaint on every window whose deadline has passed; true when
    at least one was due.

- static bool Route(nint hwnd)
  - Hands the event to the window it is addressed to; false when no child
    owns it (it belongs to the main window or the file picker).

- static bool PaintForResize(nint hwnd)
  - Paints one frame for the child window that owns `hwnd` (called from the
    window procedure during WM_SIZE in the modal resize loop). Returns true
    when a matching child was found and painted; false means the hwnd belongs
    to the main window or an unknown source.

- static void PumpAll()
  - One frame of every open window and of the shared file picker, then
    drops (and destroys) the closed ones. Called by `Form.Run()` every
    iteration; safe to call again from a frame hook: a window opened from
    another window's action handler is rendered by the second call instead
    of staying blank until the next OS event.

- static void FoldDeadlines(App main)
  - Folds the child deadlines into the main app's idle wait and wakes the
    main window when a child animation comes due. Call once per loop
    iteration from the frame hook (Form.Run already sleeps on the folded
    deadline).

- static void FollowSkin(int i)
  - 主窗口换肤时同步每个开着的子窗口。

- static void FollowOpacity(int percent)
  - 主窗口调整不透明度时同步每个开着的子窗口。

- static void FollowCaptionTips(App main)
  - 把主窗口当前的标题提示文案推给每个开着的副窗口。

- static void FollowWallpaper(string path, int opacity)
  - 主窗口更换用户壁纸时同步每个开着的子窗口。

- static void RequestRedrawAll()
  - Repaints every open window (used after the shared file picker returns:
    whoever asked for it must show the result).


## Control (class)

保留模式组件树（与即时模式控件共存）。

每个节点都是一个 `Control`：有稳定的 `name`、父节点、有序的
子节点列表、停靠提示和已解析的边界矩形。容器用 `Add` 追加
子节点；任何节点都可用 `Find(name)` 定位后代。
布局是 WinForms 风格的停靠（见 `Arrange`）：停靠的子节点吸附到
边缘并按插入顺序占用空间，`Fill` 子节点占据剩余部分，
`Manual` 子节点位于父节点内的显式偏移处。绘制是
多态的——子类重写 `OnPaint`，框架通过 `Paint` 递归，
把每个子树裁剪到父节点的矩形内，内容不会
溢出（复用原生裁剪栈）。

注意：基类方法名刻意不寻常（Paint/Arrange/
MeasureTree/InitControl/OnPaint/OnMeasure），以免与
继承 Control 的控件自身的方法冲突——编译器仅按名称
解析调用（无重载），因此子类若以不同签名复用基类名称
会编译出错。

- string name;

- int dock;
  - 0 手动，1 顶部，2 底部，3 左侧，4 右侧，5 填充。

- int layout;
  - 通过 With() 添加的子节点的自动流式布局：0 无，1 列，2 行。
    容器（见 Panel.Column/Row）设置此项，使每个 With() 子节点
    自动沿流式布局轴停靠。

- bool grow;
  - 为 true 时，此节点应增长以填满其流式父节点的
    剩余主轴空间（dock == fill），覆盖流式布局的默认停靠。

- int prefW;
  - 停靠时使用的首选主轴尺寸（top/bottom 为高度，
    left/right 为宽度）。对 Fill 子节点忽略。控件的 OnMeasure
    通常根据主题设置这些值。

- int prefH;

- int mx;
  - dock == 0 时在父内容框内的手动偏移。

- int my;

- int padL;

- int padT;

- int padR;

- int padB;

- bool padSet;
  - 由 Pad()/Padding() 设置：调用方固定了内边距，因此控件的
    OnMeasure 不得用其主题默认值覆盖它。

- bool prefSet;
  - 由 Prefer()（以及 UiDoc 的 `width`/`height`）设置：调用方固定了
    首选尺寸，因此根据子节点自测量的容器
    会保留给定的那个轴。

- int logW;
  - Sizes a document declares (UiDoc `width`/`height`/`gap`/`pad`/`x`/`y`)
    are logical pixels, written as they look at 100%. They are kept apart
    from the resolved ones and converted at measure time: taken as physical
    pixels, a row declaring 38 stays 38 tall while the text inside it grows
    with the theme, so at 150% every row overlaps the next.

- int logH;

- int logGap;

- int logPad;

- int logX;

- int logY;

- bool logPlaceSet;

- int gap;

- int flexWrapMain;
  - 换行的 flex 容器有多高取决于它有多宽，而测量发生在
    分配尺寸之前——这一轮还不知道断行宽度。容器在 Arrange
    时记下自己实际断行所用的主轴框长（flexWrapMain），下一次
    测量据此算出真实行数；flexMeasMain 是上次测量用过的值，
    两者不一致说明高度还没收敛，需要再排一帧。

- int flexMeasMain;

- int hintWrapW;
  - 宿主预先告知的主轴框宽（设备像素，0 = 未知）。上面那套按帧
    收敛只在容器跨帧存活时管用；每帧重建的容器（立即模式风格的
    宿主就是这么写的）flexWrapMain 永远是 0，于是永远按单行测量。
    宿主要把子树排进一个已知宽度的矩形时，用 HintWrapWidth 直接
    给出宽度，第一次测量就能算准行数。

- bool visible;

- int bx;
  - 画布坐标下的已解析边界（由 Arrange 设置）。

- int by;

- int bw;

- int bh;

- weak Control parent;

- List<Control> children;

- List<EventBinding> events;
  - 供设计器/序列化器使用的事件处理器绑定：把事件名
    （见 Events()）映射到处理器标识符。未绑定时为空。

- WidgetEvents On;
  - 每个控件通用的事件包（指针/焦点/键盘/触摸/拖拽），
    所有控件继承。拥有稳定 id 的交互控件
    自行接线（注册命中区域后调用 On.Fire(app, id)）；
    其余控件由 RenderTree 通过 FireCommon 接线。

- int commonId;
  - 为不自持 id 的控件（容器和仅显示控件）提供支撑 `On` 的稳定 id。
    首次使用时分配；0 = 从未需要。

- bool wiresOwnEvents;
  - 由自行注册命中区域并调用 On.Fire 的控件（Button、Input 等）设置，
    这样 RenderTree 就不会在另一个 id 上第二次
    触发该事件包。

- UiEvent Paint;
  - 由 RenderTree 触发的生命周期事件：Paint 在节点每帧绘制时触发，
    Resize 在解析尺寸变化时触发，Show/Hide 在可见性翻转时触发。

- UiEvent Resize;

- UiEvent Show;

- UiEvent Hide;

- int lastBw;

- int lastBh;

- bool lastVisible;

- bool everLaidOut;

- string bindPath;
  - 设计时绑定声明（JSON `bind`）：状态实体里的点分路径，由
    设计器（Designer.Inspector）、序列化器（Serialize）、表单生成器
    （GenForm）读写，运行时由 ChildWindow 消费——每帧把 JsonValue
    模型按路径同步进控件、把用户编辑写回。空 = 未绑定。
    注意这是"对话框状态实体同步"通道，与代码内实时绑定
    `Binding<T>`（System/Binding.zan，见规范 §6.1）是两个层面，
    互不替代；无绑定机制的控件无需关心这两个字段。

- string bindProp;
  - 绑定写入的控件属性名（SetProp/GetProp 认的名字）。
    为空时 ChildWindow 依次回退 `value`/`text`。

- string Class;
  - 可选样式类（JSON `class`），供 StyleSheet 通过 `.class` 选择器
    把声明级联到此控件。空 = 无。
    以空格分隔的 CSS 类：`btn.Class = "primary small";`（直接赋值，
    无 setter）——控件拥有的每个视觉变体都对应其中一个类。

- Binding<bool> Disabled;
  - 双向禁用标志，沿树向下继承：`grp.Disabled = vm.busy;`
    会置灰并禁用整个子树（见 IsDisabled）。

- StyleBox computedStyle;

- int computedStyleGen;

- int computedStyleScale;
  - computedStyle 是在哪个主题度量缩放下解析的（App.metricsScale）：
    设计器预览会临时整体缩放度量，换了缩放的缓存不能复用。

- string computedStyleType;

- string computedStyleClass;

- string computedStyleId;

- int computedStyleState;
  - 记住 computedStyle 是按哪个状态解析出来的（-1 = 由
    悬停/按下插值出的过渡态，不可复用）。测量按常态进行，
    有了它，一帧里没有变化的节点就不必重新走一遍样式解析。

- string styleTypeLower;
  - Kind() 的小写形式（默认的类型选择器）。每帧每节点都要问
    好几次，现算就是每次一个新字符串。

- bool styleSurfaceOwned;

- int styleBg;

- int styleBgTo;

- int styleRadius;

- int styleBorderColor;

- int styleBorderWidth;

- int styleShadow;

- int styleShadowDy;

- int styleColor;

- int styleFontPx;

- int styleTransitionMs;

- void InitControl(string n, int d)
  - 所有子类在工厂/构造函数中调用的基础初始化方法。

- Control Bg(int c)
  - 设置纯色背景并清掉渐变终点（styleBg = c，styleBgTo = 0；
    传 0 即回到未设置），并使样式缓存失效；返回 this。

- Control Gradient(int top, int bottom)
  - 设置垂直渐变背景（top -> bottom），并使样式缓存失效；返回 this。

- Control Radius(int r)
  - 设置圆角半径（px），并使样式缓存失效；返回 this。

- Control Border(int color, int w)
  - 设置边框颜色与宽度（px），并使样式缓存失效；返回 this。

- Control Shadow(int color, int dy)
  - 设置阴影颜色与垂直偏移（px），并使样式缓存失效；返回 this。

- Control TextColor(int c)
  - 设置文字/前景颜色，并使样式缓存失效；返回 this。

- Control FontPx(int px)
  - 设置字号（px），并使样式缓存失效；返回 this。

- Control Transition(int ms)
  - 设置状态过渡时长（毫秒），并使样式缓存失效；返回 this。

- Control OnClick(Action a)
  - 订阅 Click 事件并返回 this。

- Control OnDoubleClick(Action a)
  - 订阅 DoubleClick 事件并返回 this。

- Control OnRightClick(Action a)
  - 订阅 RightClick 事件并返回 this。

- Control OnChange(Action a)
  - 订阅 Change 事件并返回 this。

- Control OnEnter(Action a)
  - 订阅 Enter（指针进入）事件并返回 this。

- Control OnLeave(Action a)
  - 订阅 Leave（指针离开）事件并返回 this。

- Control OnMouseDown(Action a)
  - 订阅 MouseDown 事件并返回 this。

- Control OnMouseUp(Action a)
  - 订阅 MouseUp 事件并返回 this。

- Control OnWheel(Action a)
  - 订阅 Wheel 事件并返回 this。

- Control OnFocus(Action a)
  - 订阅 Focus 事件并返回 this。

- Control OnBlur(Action a)
  - 订阅 Blur 事件并返回 this。

- Control OnKeyDown(Action a)
  - 订阅 KeyDown 事件并返回 this。

- Control OnKeyUp(Action a)
  - 订阅 KeyUp 事件并返回 this。

- Control OnLongPress(Action a)
  - 订阅 LongPress 事件并返回 this。

- Control OnSwipe(Action a)
  - 订阅 Swipe 事件并返回 this。

- Control OnDrag(Action a)
  - 订阅 Drag 事件并返回 this。

- Control OnDrop(Action a)
  - 订阅 Drop 事件并返回 this。

- Control OnResize(Action a)
  - 订阅生命周期事件 Resize（解析尺寸变化时触发）并返回 this。

- Control OnShow(Action a)
  - 订阅生命周期事件 Show（可见性翻转为可见时触发）并返回 this。

- Control OnHide(Action a)
  - 订阅生命周期事件 Hide（可见性翻转为隐藏时触发）并返回 this。

- bool IsDisabled()
  - 当控件自身被禁用或位于被禁用的祖先之下时为 true，
    控件正是据此解析其 `:disabled` 样式及其
    （缺失的）交互——禁用一个组即禁用了它的命令，
    而无需逐个修改。

- int CommonId()
  - 此控件通用事件包的稳定 id（见 FireCommon）。

- void FireCommon(App app)
  - 把已解析的矩形注册为命中区域并触发通用事件包，
    使指针/焦点/键盘事件对所有控件生效，而不只是
    自行接线 `On` 的那几个。控件自行接线
    自己的事件或无人监听时跳过——未使用的容器不能
    抢走画在它下面的内容的指针。

- int StyleTextColor(int fallback)
  - 生效的文本颜色：设置了 CSS `styleColor` 则用它，否则用控件
    从其变体/主题解析的回退值。文本控件调用此方法。

- int StyleFontSize(int fallback)
  - 生效的字体大小：设置了 CSS `styleFontPx` 则用它，否则用回退值。

- int TransitionMs(int fallback)
  - 生效的 CSS 过渡时长（毫秒）：控件的 `transition`
    （styleTransitionMs）已设置时用它，否则用 `fallback`。控件把它传给
    Ui.HoverLevelMs/PressLevelMs，使 `transition` 属性真正
    决定悬停/按下状态通过 App.AnimTo 交叉淡化的速度。

- virtual string StyleType()
  - 此控件响应的 CSS 类型选择器。默认为其 Kind，但
    Kind 指代表面而实例仅是布局节点的控件会覆盖它，
    这样针对表面的样式表规则
    （内边距、背景、模糊）不会作用于布局节点。

- StyleBox ResolveStyle(App app, int state)
  - 按本控件的 StyleType/Class/name 解析 `state` 状态的样式
    （含 inline 覆盖），并记入 computedStyle。

- StyleBox ResolveStyleAs(App app, string type, string cls, int state)
  - ResolveStyle 的显式类型/类版本（部件或借用其他类型外观的
    控件用），id 仍取本控件的 name。

- StyleBox ResolveStyleCached(App app, string type, string cls, int state)
  - 与 ResolveStyleAs 相同，但上一次解析仍然有效时直接复用它。
    控件在一帧里往往要问同一份样式两次（OnMeasure 一次、OnPaint
    一次），每次都要拼缓存键、查表并克隆一个 StyleBox。

- StyleBox ResolveEasedStyleAs(App app, int id, string type, string cls, bool disabled, bool selected)
  - 解析 hover/press/focus 三态缓动样式（Style.EasedId，含 inline
    覆盖），selected 为锁定选中位。结果是过渡混合态，不可作常态
    缓存复用（computedStyleState 记为 -1）。

- StyleBox ResolveEasedStyleAsIn(App app, int id, string type, string cls, bool disabled, bool selected, int x, int y, int w, int h)
  - ResolveEasedStyleAs 的按矩形版本：交互程度按 (x, y, w, h)
    测量（Ui.*LevelMsIn），用于命中区域与绘制矩形不一致的控件。

- StyleBox ResolveEasedLatchedStyleAs(App app, int id, string type, string cls, bool disabled, int latched, int progress)
  - 在 latched（选中/勾选一类锁定状态位）的 on/off 两套缓动样式
    之间按 progress（0..1000 千分比）混合——开关/滑块类控件由
    位置驱动外观。同样记为过渡态（不可作常态缓存）。

- StyleBox ResolveEasedLatchedStyleAsIn(App app, int id, string type, string cls, bool disabled, int latched, int progress, int x, int y, int w, int h)
  - ResolveEasedLatchedStyleAs 的按矩形版本。

- StyleBox ResolvePart(App app, string part, string fallbackType, int state)
  - 解析本控件 `StyleType::part` 部件的样式（无 inline 覆盖）。

- StyleBox ResolvePartAs(App app, string type, string part, string fallbackType, string cls, int state)
  - 解析 `type::part` 部件样式：fallbackType 非空时提供整套
    回退规则（见 Style.Part）；id 取本控件的 name。

- StyleBox ResolveEasedPartAs(App app, int id, string type, string part, string fallbackType, string cls, bool disabled, bool selected)
  - 部件版三态缓动解析（Style.EasedPartId，无 inline 覆盖）。

- StyleBox ResolveEasedPartAsIn(App app, int id, string type, string part, string fallbackType, string cls, bool disabled, bool selected, int x, int y, int w, int h)
  - 部件版三态缓动解析的按矩形版本（无 inline 覆盖）。

- StyleBox ResolveEasedLatchedPartAs(App app, int id, string type, string part, string fallbackType, string cls, bool disabled, int latched, int progress)
  - 部件版 latched 混合解析（无 inline 覆盖）。

- StyleBox ResolveEasedLatchedPartAsIn(App app, int id, string type, string part, string fallbackType, string cls, bool disabled, int latched, int progress, int x, int y, int w, int h)
  - 部件版 latched 混合解析的按矩形版本（无 inline 覆盖）。

- bool ComputedStyleCurrent(App app)
  - computedStyle 是否仍对当前主题代次/度量缩放/类型/类/名有效
    （不比对状态位）。Bg()/Class 等改动使缓存失效后为 false。

- int StyleWidth()
  - 生效宽度：样式的声明宽度（px 或已解析的百分比）夹到
    min/max 后返回；无样式时回退测量偏好 prefW。

- int StyleHeight()
  - 生效高度：同 StyleWidth，沿高度轴（回退 prefH）。

- int StylePadL()
  - 内容框的左侧内边距。显式的 Pad()/Padding() 优先于
    解析样式携带的主题默认值（自由画布根节点将其固定为 0）；
    未调用时由样式表决定。

- virtual int StylePadT()
  - 内容框的顶部内边距。之所以是虚方法，是因为绘制自身
    装饰的容器（如 Card 的标题行）无论样式表如何规定
    内边距都必须为此预留空间。

- int StylePadR()
  - 内容框右内边距：显式 Pad()/Padding() 优先于样式表（同 StylePadL）。

- int StylePadB()
  - 内容框底部内边距：显式 Pad()/Padding() 优先于样式表（同 StylePadL）。

- int StyleDisplay()
  - 此节点的 CSS `display`：0 block（子节点停靠），1 flex（子节点沿
    flex-direction 排列），2 none。

- int StyleWidthIn(int avail)
  - 在 `avail` 像素的包含块内声明的主/交叉轴尺寸，
    百分比已解析、min/max 已应用；样式未声明尺寸时
    回退到测量偏好（prefW/prefH）。

- int StyleHeightIn(int avail)
  - 生效高度：在 `avail` 像素包含块内解析样式声明的高度
    （百分比、min/max 同 StyleWidthIn），未声明时回退 prefH。

- bool StyleDeclaresWidth()
  - 样式表声明了宽度/高度（如 `button.large` 这样的尺寸类）时为 true，
    区别于测量偏好。停靠在行中的子节点
    若声明了交叉轴尺寸则保留它（并居中），而不是
    被拉伸到行高。

- bool StyleDeclaresHeight()
  - 样式表声明了高度时为 true（与 StyleDeclaresWidth 配对使用）。

- int StyleGrow()
  - 此节点的 CSS `flex-grow`（0 = 保持自身尺寸）。

- int StyleWrap()
  - CSS `flex-wrap`（0 单行，1 换行）。

- int StyleAlignContent()
  - CSS `align-content`：换行容器里各行在交叉轴上的分布
    （0 start，1 center，2 end，3 space-between，4 space-around，5 stretch）。

- int StyleAlignSelf()
  - CSS `align-self`：本子项自己的交叉轴对齐，-1 表示未声明
    （跟随容器的 align-items）。

- int StyleShrink()
  - CSS `flex-shrink`：行溢出时是否参与收缩（1 参与，0 不参与）。
    未声明按 1——CSS 的默认值。

- int StyleBasisIn(int avail)
  - CSS `flex-basis` 在 `avail` 像素主轴包含块内的值，
    未声明时返回 -1。

- int StyleAspect()
  - CSS `aspect-ratio` 的千分比（0 = 未声明）。

- int StyleMarL()
  - 样式表声明的外边距（px；未解析样式时为 0）。

- int StyleMarT()
  - 样式表声明的外边距（px；未解析样式时为 0）。

- int StyleMarR()
  - 样式表声明的外边距（px；未解析样式时为 0）。

- int StyleMarB()
  - 样式表声明的外边距（px；未解析样式时为 0）。

- int StyleGap()
  - 生效的子项间距：样式表的 `gap` 优先，其次 Gap() 设置值。

- int StyleRowGap(int fb)
  - 行距 / 列距（CSS `row-gap` / `column-gap`，未声明时回退到 `gap`，
    再回退到调用方给的默认值）：换行的容器两个方向的间距不同。

- int StyleColGap(int fb)
  - 列距（CSS `column-gap`，未声明回退 `gap`，再回退 `fb`）。

- int StyleColumns(int fb)
  - 每行的等分列数（CSS `columns`）。
    未声明时返回 `fb`（0 = 按可用宽度自动换行）。

- int StyleLineHeight()
  - 行高（CSS `line-height`，0 = 未声明：由该行最高的子项决定）。

- bool StyleVisible()
  - 本控件及样式均可见时为 true：visible 标志、CSS `display`
    非 none 且 `visibility` 非 hidden。Arrange/Render/命中都以此为准。

- void PaintStyleBox(App app)
  - 把此节点的 CSS 表面（阴影、背景/渐变、边框）
    绘制进其已解析边界，遵循 styleRadius。由 RenderTree 在
    OnPaint 之前调用，使所有控件获得统一的 CSS 样式，控件的
    OnPaint 只需在之上绘制自己的内容。未设置任何样式时为空操作，
    因此自行绘制表面的既有控件不受影响。

- void FireOn(App app, int id)
  - 针对 `id` 触发此节点的通用事件包。控件在
    注册命中区域后每帧调用一次；等价于
    On.Fire(app, id)，但调用点更统一。

- Control Dock(int d)
  - 设置停靠方式（Dock.* 值）；返回 this。

- Control Prefer(int w, int h)
  - 设置测量偏好尺寸（px）：布局优先于 OnMeasure 的自测量与
    样式回退；返回 this。

- Control Place(int x, int y)
  - 设置 dock == Manual 时在父内容框内的偏移（px）；返回 this。

- Control Pad(int p)
  - 四边统一设置内边距并锁定（OnMeasure 不得再用主题默认值
    覆盖，见 padSet）；返回 this。

- Control Padding(int top, int right, int bottom, int left)
  - 按 CSS 顺序（上、右、下、左）设置内边距并锁定（同 Pad）；
    返回 this。

- Control Gap(int g)
  - 设置流式/停靠子项间距（px）；返回 this。

- Control SetShown(bool v)
  - 设置可见性（Show/Hide 生命周期事件据此在下一帧触发）；
    返回 this。

- Control HintWrapWidth(int px)
  - 告知本容器它将在多宽的框里断行（设备像素）。换行的 flex
    容器有多高取决于它有多宽，而测量在分配尺寸之前发生；宿主
    已经知道目标宽度时（把子树排进一个已知矩形），在 MeasureTree
    之前调用这个，行数与高度第一次测量就是对的，不必等下一帧。

- Control Add(Control c)
  - 追加一个子节点（自动停靠）。返回该子节点，调用方可
    内联持有引用，如 `Button b = panel.Add(save)`。

- Control With(Control c)
  - 流式子节点追加：添加 `c` 并返回 THIS 容器（而非子节点），
    因此多个子节点可链式追加——`panel.With(a).With(b).With(c)`。若
    此节点有流式布局（列/行），子节点会自动沿
    流式轴停靠，除非它选择了 Grow()。

- bool Adoptable(Control c)
  - 一个控件在树里只能有一个位置。宿主保留控件（画廊、文档预览、
    设计出来的静态字段）会在重建时被挂到新的父节点上，旧父节点若还
    留着它，同一个节点就出现在两处；把祖先挂进自己的后代更糟——树
    成环，任何递归遍历（Wire/RenderTree/Measure）都会无限递归，栈溢
    出表现为读非法地址的崩溃。因此收养前先判断能不能收养。

- void Adopt(Control c)
  - 收养一个子节点：先从原父节点摘下（含本节点，重复 Add 不会让
    同一个控件在 children 里出现两次），再指向本节点。

- Form HostForm()
  - 本节点所在的窗口，尚未挂到任何窗口下时为 null。

- virtual void OnHostForm(Form f)
  - 挂到窗口树上时由框架下发：设计出来的控件用它记住自己的事件
    宿主，因此宿主代码不需要手动接线。

- void SpreadHostForm(Form f)
  - 把宿主窗口沿子树发下去（收养时自动调用，一棵先建好的子树在
    挂上来的那一刻整棵都收到宿主）。

- int DockSize(int avail, bool horizontal)
  - 给定父节点剩余空间时，此子节点停靠的主轴尺寸：
    由样式表决定，因此停靠面板上的 `width: 34%; min-width: 260px`
    与浏览器中的行为完全一致；没有样式尺寸的子节点
    保持其测量尺寸。

- Control Grow()
  - 标记此节点填满其流式父节点的剩余主轴空间。

- Control DockTop()
  - 停靠到顶部（占用整行宽度，按插入顺序自上而下）；返回 this。

- Control DockBottom()
  - 停靠到底部；返回 this。

- Control DockLeft()
  - 停靠到左侧（占用整列高度）；返回 this。

- Control DockRight()
  - 停靠到右侧；返回 this。

- Control DockFill()
  - 停靠为填充：占据其余停靠子节点用剩的空间；返回 this。

- Control DockManual()
  - 取消停靠，回到 Manual（用 Place() 定位）；返回 this。

- Control Named(string n)
  - 流式 id 设置器，内联构建的节点之后仍可用
    Find() 定位，或被设计器/序列化器定位。

- int IndexOf(Control c)
  - `c` 在 children 中的下标；不是本节点的子节点时返回 -1。

- void Remove(Control c)
  - 移除一个子节点（若它不是本节点的子节点则为空操作）。

- void RemoveAll()
  - 移除所有子节点：数据驱动的容器在按数据重填前调用。

- void InsertAt(int idx, Control c)
  - 在某个位置插入子节点，索引被钳制在范围内。会重新父化 `c`。

- void MoveChild(Control c, int to)
  - 把已有子节点移动到新索引（供设计器拖拽排序用）。

- Control HitTest(int x, int y)
  - 其已解析边界包含该点的最深层可见后代，
    优先选择更靠后（最上层）的子节点。用于设计器命中选择。

- Control Find(string n)
  - 按名称深度优先搜索，包括本节点。找不到返回 null。

- int ChildCount()
  - 子节点数。

- ControlChildren Children { get }
  - 子节点集合门面（getter-only 属性）：对象初始化器
    `new Panel.Row() { Children = { a, b, c } }` 对它逐个 Add，
    每次 Add 都走 `With` 的完整收养语义；这是唯一预期的用法，
    返回的包装对象是一次性的，不值得在初始化器之外持有。

- string GetHandler(string evt)
  - 绑定到 `evt` 的处理器，无则为 ""。供事件检查器使用。

- void SetHandler(string evt, string h)
  - 把处理器标识符绑定（或重新绑定）到 `evt`。

- void ApplyDeclaredUnits(App app)
  - 让节点自下而上从主题设置首选尺寸（子节点
    优先）。子类重写 OnMeasure。在 Arrange 之前运行。
    Converts the logical sizes a document declared into physical pixels at
    the app's current scale. Runs before every measure pass, so a DPI
    change (or a move to another monitor) re-resolves them.

- void MeasureTree(App app)
  - 测量阶段入口（Arrange 之前每帧调用）：换算文档声明的逻辑
    尺寸（ApplyDeclaredUnits）→ 常态样式过期时重新解析 →
    不可见节点到此为止（不测量子树）→ 传播断行宽度提示 →
    递归子节点 → OnMeasure 自测（作者用 Prefer()/文档
    width/height 声明的正数尺寸优先于自测结果）→ 容器按内容
    补齐作者留空的轴（MeasureDocked/MeasureFlexContent）。

- void PropagateWrapHint()
  - 把已知的断行宽度传给纵向排布的子节点。纵向排布（停靠成一列，
    或 `flex-direction: column`）的子节点各自铺满内宽，所以本节点
    知道的宽度对它们同样成立；横向排布的子节点要分摊宽度，这时
    还不知道各自能分到多少，就不传。
    
    少了这一步，只有最外层容器能拿到宿主给的宽度：嵌在一列里的
    换行 flex 行会按单行测量，第二行被裁掉。

- void MeasureDocked(App app)
  - 停靠容器在没人给尺寸时按内容测量：一列停靠的行
    高等于各行之和，一行停靠的控件宽等于各控件之和
    （加上内边距和间距）。少了这一步，设计器只能给
    每个容器写死一个高度，字号或 DPI 一变就错位。
    只填补留空的那根轴：OnMeasure 或作者给过的尺寸优先。

- void MeasureFlexContent(App app)
  - 按内容测量一个 `display: flex` 容器：主轴取各子项之和（换行时
    取最长那一行），交叉轴取各行之和。只填补作者留空的那根轴，
    因此 Prefer() 与样式表的 width/height 依然优先。
    
    少了这一步，一个 flex 容器的 prefW/prefH 会停在 0：停靠进
    一列里就是零高，作者只能给每个容器写死一个像素高度——
    换行的一排按钮也就永远只能是一行。

- static int FitSize(int requested, int available)
  - 把请求尺寸钳制到可用空间内；任一为负时返回 0。

- static int FitGap(int requested, int available)
  - 把请求间距钳制到剩余空间内；剩余 <= 0 时返回 0。

- virtual void Arrange(int px, int py, int pw, int ph)
  - 计算此节点及其子树（通过停靠）的边界。
    虚方法，使容器（如 ScrollColumn）可以偏移/裁剪其子节点。

- static bool overlapEnvRead;
  - 环境变量只读一次，避免每帧碰内核。

- static bool overlapEnvOn;

- static bool DebugOverlap;
  - 编程开关：测试/宿主不经环境变量直接开。

- static int overlapHits;
  - 本进程去重后命中的重叠对数；测试据此断言。

- static Dict <string, bool> overlapSeen;

- static bool OverlapActive()

- bool overlapExempt;
  - 允许刻意叠放的场景（角标、悬浮装饰）在子控件上挂免检牌。

- Control NoOverlapCheck()
  - 不参与重叠自检（本控件作为兄弟被跳过）。

- static int OverlapHits()
  - 测试读取：本进程去重后命中的重叠对数。

- static void ResetOverlapHits()
  - 测试复位：清零计数与去重表。

- void CheckOverlapKids()

- void ReportOverlap(Control a, Control b, int ix, int iy)

- static bool lintEnvRead;
  - 环境变量只读一次，避免每帧碰内核。

- static bool lintEnvOn;

- static bool DebugLayoutLint;
  - 编程开关：测试/宿主不经环境变量直接开。

- static int lintHits;
  - 本进程去重后命中的尺寸问题数；测试据此断言。

- static Dict <string, bool> lintSeen;

- static bool LintActive()

- Control FreeLayout()
  - 免检牌：同一张牌同时豁免重叠与尺寸两条自检。

- virtual bool LintLeafSize()
  - 谁参与尺寸自检：只有“宽高有正解”的文字叶子控件
    （Button/Checkbox 覆写为真；Panel/Input 这类通栏合理的
    控件不参与，免得表单里满屏误报）。

- void CheckKidsLayout()
  - Arrange 的两条出口（停靠尾、flex 尾）共用的子树自检入口。

- static int LintHits()
  - 测试读取：本进程去重后命中的尺寸问题数。

- static void ResetLintHits()
  - 测试复位：清零计数与去重表。

- void CheckKidsSizes()

- void ReportLint(Control c, string rule, string detail)

- void ArrangeFlex(int cx, int cy, int cw, int ch, int gapPx)
  - 把子节点作为一个 CSS flex 容器排布在本节点的内容框内。
    
    `flex-wrap: nowrap`（默认）时全部子节点排成一条 flex 行。
    `wrap` 时按各项自然主轴尺寸断行——一行至少容纳一项，因此
    比整框还长的子项只会自己占满一行，不会卡住断行——行与行
    之间用交叉轴间距（row 容器取 `row-gap`，column 容器取
    `column-gap`，都回退到 `gap`）分隔，多余的交叉轴空间按
    `align-content` 分配。每一行内部的规则见 ArrangeFlexLine。

- void ArrangeFlexLine(List<Control> items, int cx, int cy, int cw, int ch, int gapPx, bool row, int crossOff, int crossBox)
  - 排布一条 flex 行：每个子节点取声明的主轴尺寸（px 或框的
    百分比），未声明时取测量偏好；`flex-grow` 分配剩余空间；
    `justify-content` 安排剩余部分，`align-items` 决定交叉轴
    尺寸（默认 stretch）。支持 margins 和 `gap`，溢出的一行
    会按比例收缩而不是溢出框外。
    
    `crossOff` 是该行在交叉轴上相对内容框的偏移，`crossBox`
    是该行的交叉轴尺寸——单行容器就是整个内容框，换行容器
    则由 ArrangeFlex 逐行给出。

- int StyleClampW(int avail, int v)
  - 把此节点的 min/max-width（或 -height）应用到 `v`，
    百分比边界按 `avail` 的包含块解析。

- int StyleClampH(int avail, int v)
  - 把 `v` 限制在本节点的 min/max-height 内（百分比边界按
    `avail` 的包含块解析），同 StyleClampW。

- int MarMain(bool row)
  - 沿/跨 flex 行的总外边距。

- int MarCross(bool row)
  - 交叉方向上的总外边距（行容器为上下，列容器为左右）。

- virtual void OnPaint(App app)
  - 绘制此节点自身的视觉。基类不绘制；子类重写。

- virtual void OnPaintOverlay(App app)
  - 在延迟的覆盖层阶段绘制此控件的浮动/覆盖层（弹出菜单、选项列表、
    提示），使其绘制在所有页面内容之上
    并注册最顶层的命中区域——永不被遮挡，
    也绝不把点击漏给其后绘制的控件。基类
    不绘制；浮动控件重写此方法，打开期间用
    `app.AddOverlay(OverlayPopup.Host(this))` 延迟自身，
    而不是在主阶段内联绘制弹窗。

- virtual void OnMeasure(App app)
  - 根据内容/主题设置 prefW/prefH。基类为空操作；叶节点重写。

- virtual string Kind()
  - 用于重建此节点的稳定类型标签（见 ControlFactory）。每个
    具体控件都重写它；基类标签只是回退。

- virtual List<PropSpec> Props()
  - 供检查器和序列化器使用的控件专属可编辑属性。
    通用几何（dock/pad/gap/size/pos/name）由 Serialize 处理，
    因此这里只返回控件独有的属性。基类没有。

- virtual bool Fired()
  - 本帧此控件是否触发了它的主动作（按钮被按下、菜单项被选中）。
    这是 Click 一类事件的*轮询*版本：每帧重建控件树的宿主留不住
    处理器，而按一排按钮各挂一个处理器也说明不了任何事情——它们
    只想在排完版之后问一句「刚才谁被按了」。默认 false；有主动作
    的控件覆写它，宿主便可以遍历整棵子树一次问遍所有控件。

- Control FiredIn()
  - 子树里本帧触发了主动作的第一个控件（深度优先，绘制顺序），
    没有则为 null。

- static List<string> CommonEvents()
  - 所有控件暴露的通用事件名（指针/焦点/键盘/
    触摸/拖拽/生命周期），按检查器顺序。控件将其前置到自己的
    语义事件之前（在 Events() 中）。

- virtual List<string> Events()
  - 供设计器事件检查器使用的声明事件名。基类返回
    通用事件包；控件重写以追加自己的语义事件（并
    仍包含 CommonEvents()）。

- virtual void BindEvent(string evt, Action a)
  - 把解析出的 Action 订阅到指定事件。基类把通用事件包
    （Click/Enter/.../Drop）映射到 `On`；控件重写以把
    自己的语义事件（Change/Submit/RowClick/...）路由到正确的
    UiEvent 字段，然后为通用事件集调用基类。JSON
    加载器用它附加经注册表解析的 `on<Event>` 处理器。

- PropSpec PropOf(string key)
  - `key` 对应的规格；若此控件未发布该绑定
    属性则返回 null。

- virtual string GetExtra(string key)
  - 为无法用字段表达的属性提供的挂钩——逗号连接的条目列表、
    或多个字段派生的值。有此类属性的控件重写这一对方法；
    一切由字段支撑的属性仅由 Props() 提供。

- virtual bool SetExtra(string key, string val)
  - 写入一个额外属性；控件没有该键时返回 false，
    基类此时回退为把它当作样式类处理。

- virtual Control SlotHost(int slot)
  - 设计里放进容器某个“位”的子控件（标签页的页、分栏的
    窗格）真正的父节点。容器重写它，把设计文档的 `childTab`
    映射到自己的内部容器；普通容器直接收下子节点。

- virtual string GetProp(string key)
  - 通过控件在 Props() 中绑定的访问器，按键以文本形式读取属性——
    这样控件只需发布每个属性一次，无需自己的
    字符串映射。`class`、`name` 和 `disabled` 对所有控件都有应答。

- virtual void SetProp(string key, string val)
  - 从文本按键写入属性（GetProp 的逆操作）。未知的
    键改指样式类，要么是标志（`"round": true`），要么是
    变体名（`"size": "small"`），文档正是借此设置
    控件没有字段对应的视觉变体。

- void SetDesignText(string txt)
  - 应用设计器里的标题文本。只有声明了 `text` 属性的控件
    会接受它：容器的 label 是设计期说明，不是内容，所以
    不能像 SetProp 那样退化成样式类。

- void AddClass(string cls)
  - 若样式类尚不存在则添加它。

- void SetClassIn(string group, string cls)
  - 把 `Class` 里属于 `group`（空格分隔的候选集）的类全部去掉，
    再加上 `cls`（`cls` 为空则只做清除）。
    
    同一根轴上的变体是互斥的：`justify-center` 与 `justify-end`
    同时挂着时，最终生效的是样式表里靠后那条规则，作者每换一次
    对齐方式都得自己先去清掉上一次留下的类。这个方法把互斥
    关系收在一处，供 Flex/Grid 这类有多组变体的容器使用。

- static string SizeClass(string size)
  - Naive UI `size` prop 值对应的 class 片段：tiny/small →
    "small"，large → "large"，medium → ""（默认，不附加）。
    尺寸档的实际几何（高度/字号/内边距）在 base.css 的
    `.small/.large` 规则里，档位值来自 Style.RootFromTheme
    导出的 --height-* / --font-size-* token。

- string SizeCls()
  - 实例侧便捷：解析本控件的 `Size` 绑定字段并映射为档位
    class 片段。Binding<string> 型的 Size 字段直接调用即可。

- static string StatusSuccess()
  - 校验状态类名（Naive UI status prop）。输入族控件
    （Input/TextArea）把 `FieldStatus` 映射为这些 class，
    base.css 的 `.success/.warning/.error` 规则负责描边。
    校验成功状态类名（"success"）。

- static string StatusWarning()
  - 校验警告状态类名（"warning"）。

- static string StatusError()
  - 校验错误状态类名（"error"）。

- static string StatusSanitize(string v)
  - 校验状态白名单归一：只认 success/warning/error，其余一律
    落回 ""（无状态）。设计器/绑定路径写进来的任意字符串先过
    这里，脏值不会长出一个没人认识的 class。

- virtual Binding<string> SizeOf()
  - 反射在 Zan 里没有：子类用 `new` 覆写 SizeOf 返回自己的
    Size 绑定字段；基类返回 null。

- virtual void SyncBinding()
  - 双向绑定的统一拉取点：把外部 `Binding<T>` 的当前值拉进
    控件内部状态（model -> UI）。基类空实现；有绑定通道的
    控件 override。由 RenderTree 在每帧 OnPaint 前统一调用，
    控件不必在 OnPaint 开头自调（事件时机的回写仍走
    `data.Set(...)`，与本契约无关）。契约见
    docs/STDLIB_COMPONENT_STANDARDS.md §6.3。

- void RenderInside(App app, Rect area)
  - 在 `area` 内布局并绘制此子树：宿主只需这一句
    即可把矩形交给保留组件（测量、停靠、绘制）。

- void RenderAt(App app, int x, int y)
  - 以自身测量出的尺寸在 (x, y) 处绘制此子树：适用于
    有位置但给不出矩形的宿主（预览、状态条）。

- void RenderAt(App app, int x, int y, int w)
  - 在 (x, y) 处按 `w` 像素宽绘制此子树，高度按自身测量。

- void RenderTree(App app)
  - 渲染子树：先自身，再裁剪到本节点矩形内的子节点，
    子节点不能画到父节点之外（原生裁剪栈）。命名为
    RenderTree（而非 Paint），因为一些控件已声明了静态
    Paint，而编译器仅按名称解析方法调用。


## ControlChildren (class)

`Control.Children` 集合初始化器门面：
`new Panel.Row() { Children = { a, b, c } }` 与逐个
`With(a).With(b).With(c)` 完全同义——`Add` 就是 `owner.With(c)`，
完整收养语义（换父、HostForm 下发、流式容器自动停靠、Grow 让位）
一个不少。irgen 的成员集合初始化只对该对象逐个调用 `Add`，
因此每次 `new` 都是一次性的薄包装，不值得持有。

- weak Control owner;

- ControlChildren(Control o)
  - 一次性包装：持有目标容器（弱引用）。

- void Add(Control c)
  - 返回 void 而非子节点：集合初始化器逐个调用 Add 后丢弃返回值，
    若返回子节点（+1 所有权），每次初始化都会丢一个必须显式释放的
    引用；需要内联持有时用 `panel.Add(c)`（返回子节点）。


## ControlFactory (class)

反序列化时根据 Kind() 标签重建 Control，并为
设计器的组件面板提供数据。保持为单一 switch，这样向设计器
添加一个控件只需在这里改一行，再加上控件自身的模型
重写（Kind/Props/GetProp/SetProp）。

- static List<string> Kinds()
  - Standard retained controls exposed to the designer and JSON loader.
    Project components are appended by the project-generated registry.

- static Control Create(string kind)
  - Construct the real Control named by `kind`. There is deliberately no
    fallback: a misspelled or unavailable kind must remain visible to the
    caller instead of silently changing the document's type.


## Corner (class)

圆角盒中实际圆角的角，以位集表示
（`Corner.TL() + Corner.TR()` = 上面两角）。焊接的相邻元素会
把共享接缝修成直角。

- static int TL()

- static int TR()

- static int BR()

- static int BL()

- static int All()

- static int Top()
  - 同一侧的两个角：`Corner.Top()`、`Corner.Left()`……

- static int Right()

- static int Bottom()

- static int Left()


## Css (class)

一个小型 CSS 解析器：把以真实 CSS 文本编写的皮肤样式表转换成
StyleSheet 已能应用的 选择器 -> 声明 映射。

皮肤过去是 Zan 代码（每个皮肤一个 Theme 预设），因此任何超出
调色板交换的东西——控件形状、渐变、阴影、各状态外观——都意味着
要改控件代码。现在皮肤是放在美术资源旁的 `.css` 文件，
GUI 在运行时加载，用户可以重新设计应用外观（或自带皮肤），
而无需改动或重新构建任何代码：

:root { --accent: #d92b2b; --radius: 999; }
button.primary        { background: linear-gradient(#ffd76a, #e0a020);
radius: var(--radius); border: 1 #8a5b12; }
button.primary:hover  { background: #ffe08a; }
tab.item:active       { border-bottom: 2 var(--accent); }

有目的地支持（仅此而已，无更多级联）：声明块、选择器
列表（`a, b { }`）、`:state` 后缀、`/* 注释 */` 以及 `:root`
中以 `var(--name)` 引用的自定义属性。其余一律解析为
普通属性，由 StyleSheet/控件决定其含义。

- static StyleSheet Parse(string src)
  - 把 `src` 解析为样式表，选择器保留其 `:state` 后缀。
    格式错误的文档会产出所有干净解析出的部分，一条坏规则
    不会毁掉整个皮肤。

- static StyleSheet ParseWith(string src, List<string> extraNames, List<string> extraVals)
  - 同 Parse，但额外认得 `extraNames`/`extraVals` 里的自定义属性
    （当前皮肤的 `:root` 变量与主题 token）：应用自己的 CSS 里
    写 `var(--accent)`、`var(--bg-primary)` 因此能解析到当前皮肤/
    主题（以前展开为空，因为只看得见同一份源文本里的变量）。
    外来变量只参与展开，不会写进结果表的 vars：sheet.vars 仍然
    只代表这份 CSS 自己声明了什么（Skin.ThemeOf 按它推导主题，
    掺进主题 token 就成了自我喂养）。同名时本身的变量胜出。

- static StyleSheet ParseWithSources(string src, List<string> extraNames, List<string> extraVals, int physicalCount)
  - External theme tokens precede inherited logical skin variables. Keep
    the boundary explicit so app CSS does not mistake skin sizes for pixels.

- static JsonValue ParseBlock(string body, List<string> varNames, List<string> varVals)
  - 单个块的声明，`var(--x)` 已解析，自定义
    属性被丢弃（它们只用于被引用）。

- static JsonValue ParseBlockWithSources(string body, List<string> varNames, List<string> varVals, int externalCount)

- static bool IsPrescaledValue(string val, List<string> names, List<string> vals, int externalCount)
  - Only externally supplied theme font metrics are physical pixels. Local
    :root declarations remain logical, even when they shadow a theme token.
    Follow aliases with the same bounded expansion used by ExpandVars.

- static string StripImportant(string val)
  - 去掉结尾的 `!important`（此处的级联本就是"后规则
    胜出"，因此该标志没有额外含义）。

- static string Lower(string s)
  - 把属性名/关键字转小写（选择器保留大小写，因此 `#Save`
    仍能匹配名为 `Save` 的控件）。

- static void MergeInto(StyleSheet sheet, string sel, JsonValue block)
  - 把 `block` 的声明加入 `sel`，保留同一选择器早先规则
    已设置的声明（与 CSS 一样，后规则胜出）。

- static void CollectVars(string s, List<string> names, List<string> vals)
  - 从每个 `:root` 块中读取 `--name: value` 对。

- static string ExpandVars(string val, List<string> names, List<string> vals)
  - 替换 `val` 中的每个 `var(--name)`；未知名称展开为 ""。

- static string StripComments(string src)
  - 删除 `/* ... */` 注释（逐片处理，大样式表只需一趟
    而非每字符一个字符串）。

- static List<string> SplitTrim(string s, string sep)
  - 按 `sep` 拆分并修剪每部分（空白和换行）。

- static List<string> SplitTopTrim(string s, string sep)
  - 按顶层 `sep`（单字符）拆分并修剪每部分：括号内的分隔符
    不拆，因此 `linear-gradient(90deg, rgba(0,0,0,.5), #fff)` 的
    函数式颜色停靠点会作为整体保留。

- static int IndexFrom(string s, string needle, int start)
  - `s` 中从 `start` 起首次出现 `needle` 的下标，无则 -1。

- static bool Space(string ch)
  - ch 是否为空白字符（空格/制表/回车/换行）。

- static string Trim(string s)
  - 去除两端的空白字符。


## Cursor (class)

鼠标光标形状常量。

- static int Arrow()
  - 默认箭头（0）。

- static int Hand()
  - 可点击的手型（1）。

- static int IBeam()
  - 文本输入 I 型（2）。

- static int ResizeH()
  - 水平调整大小（3）。

- static int ResizeV()
  - 垂直调整大小（4）。


## DeviceProfile (class)

目标设备画像：新建项目向导与 .zform 设计器共用的
设备单一来源。一张画像 = 一个设备类别 + 它的设计
基准视口（逻辑像素）+ 该类别是否允许自由尺寸。

锁定的是"设计基准"而不是物理尺寸：运行时按实际表面
等比拟合（App.Show 的画布拟合）或流式重排（FbFlow
24 列网格 / Flexbox），所以手机有大小之分、折叠屏
中途变形都不需要额外的画像——它们由重排与拟合兜住。

桌面 / 2in1 是唯一的自由类别：窗口尺寸由用户决定，
沿用向导里的分辨率预设与自定义宽高。其余类别的画布
尺寸由画像给出，设计器里不可改，只允许画像声明的
横竖屏切换。

- string id;
  - 画像 id（.zform "device" 键、manifest "device=" 的取值）。

- string en;
  - 英文 / 中文显示名。

- string zh;

- int pw;
  - 竖屏（portrait）设计基准视口。

- int ph;

- int lw;
  - 横屏（landscape）设计基准视口；不支持横屏时与竖屏相同。

- int lh;

- bool locked;
  - true = 设计尺寸锁定为画像视口，不可自由填写。

- bool rotatable;
  - true = 允许横竖屏切换（画像内互换基准视口）。

- bool round;
  - true = 圆形表盘（穿戴）。

- DeviceProfile(string i, string e, string c, int pw0, int ph0, int lw0, int lh0, bool lk, bool rot, bool rnd)
  - 私有构造：全部画像在 All() 中静态声明。

- string Id()
  - 画像 id（"desktop" / "phone" / ... ）。

- string Label(string lang)
  - 按界面语言取显示名（lang "zh" 返回中文名）。

- bool Locked()
  - 该类别是否锁定设计尺寸。

- bool Rotatable()
  - 该类别是否允许横竖屏切换。

- bool Round()
  - 该类别是否为圆形表盘。

- int CanvasW(int orient)
  - 指定方向（0 竖屏 / 1 横屏）的设计画布宽 / 高。

- int CanvasH(int orient)

- static List<DeviceProfile> All()
  - 全部设备画像（顺序即向导 chips 的顺序；0 号是自由的
    桌面/2in1，也是 .zform 缺省——"device" 键为空即它）。

- static int Count()
  - 画像数量（向导 chips 行排版用）。

- static DeviceProfile At(int i)
  - 第 i 个画像；越界返回 null。

- static DeviceProfile ById(string deviceId)
  - 按 id 查画像；空串（桌面自由类别是缺省）或未知 id
    返回 null，调用方据此回退到自由类别行为。

- static int IndexOfId(string deviceId)
  - 按 id 查画像在 All() 中的下标；未找到返回 0（桌面）。


## Dispatcher (class)

对运行时 UI 线程调度队列的轻量封装。后台线程
调用 `Post` 把委托交回 UI 线程；UI 线程
每帧清空一次队列（见 <c>App.Post</c> / <c>App.DrainPosts</c>）。
队列本身由运行时内部的 OS 互斥锁保护，因此从任何线程
发布都是安全的，也不会在非 UI 线程触碰 Zan 堆。

- [DllImport("crt", EntryPoint="zan_dispatch_init")]static extern void PlatInit();

- [DllImport("crt", EntryPoint="zan_dispatch_post")]static extern int PlatPost(Action handler);

- [DllImport("crt", EntryPoint="zan_dispatch_take")]static extern Action PlatTake();

- [DllImport("crt", EntryPoint="zan_dispatch_clear")]static extern void PlatClear();

- static void Init()
  - 重置队列。在 UI 线程上、创建 worker 之前调用一次。

- static bool Post(Action handler)
  - 把要在 UI 线程运行的委托加入队列。线程安全。

- static Action Take()
  - 取出下一个排队的委托（UI 线程），为空时返回 null。

- static void Clear()
  - 清空所有排队的委托。请在 UI 线程上调用，当
    窗口关闭时，这样为已失效窗口派发的后台任务
    就不会在下一个窗口的第一帧执行。


## Dock (class)

具名停靠值，使树中写 `.Dock(Dock.Top())` 而不是魔法
数字。（该语言没有静态字段常量，因此用静态方法。）

- static int Manual()
  - 0：不停靠，用 Place() 在父内容框内定位。

- static int Top()
  - 1：吸附顶部，占整行宽度，按插入顺序自上而下占用高度。

- static int Bottom()
  - 2：吸附底部。

- static int Left()
  - 3：吸附左侧，占整列高度，按插入顺序自左向右占用宽度。

- static int Right()
  - 4：吸附右侧。

- static int Fill()
  - 5：填充其余停靠子节点用剩的空间。


## EventBinding (class)

供设计器/序列化器使用的一个事件处理器绑定：事件名映射到
处理器标识符。用单个实体取代并行的键/值列表。

- string key;

- string val;

- EventBinding(string key, string val)
  - 构造一条绑定（事件名 -> 处理器标识符）。


## EventHub (class)

整数 key 的多播事件注册表。应用以任意整数常量作事件名，
在帧循环前用 `On` 常驻订阅一次，之后每帧经
`RaiseIf` 把即时模式的布尔条件（如 Ui.Clicked）
桥接为事件。

- List<Subscription> subs;

- EventHub()

- void On(int key, Action handler)
  - 为事件 key 追加一个处理器（类似 <c>event += handler</c>）。

- void Off(int key)
  - 移除某 key 注册的全部处理器（相当于清空事件）。

- int Count(int key)
  - 某 key 注册的处理器数量。

- void Raise(int key)
  - 调用某 key 注册的全部处理器（多播）。

- void RaiseIf(int key, bool fire)
  - 仅当 <paramref name="fire"/> 为 true 时触发某 key 的处理器
    （例如传入 <c>Ui.Clicked(app, id)</c> 在点击时触发）。


## FlexNode (class)

解算树的节点：持有一个 FlexStyle、子节点列表，以及
Compute 写入的结果矩形（resultX/Y/W/H）与内容尺寸（contentW/H）。

- FlexStyle style;

- List<FlexNode> children;

- int resultX;

- int resultY;

- int resultW;

- int resultH;

- int contentW;

- int contentH;

- FlexNode(FlexStyle s)
  - 构建解算树的节点：持有一个样式与子节点列表。

- FlexNode AddChild(FlexNode child)
  - 添加子节点，返回 this 便于链式构建。

- void Compute(int containerW, int containerH)
  - 以给定容器尺寸解算整棵子树；结果写入各节点 resultX/Y/W/H（相对父节点内容框），
    contentW/H 为内容实际尺寸。解算前可修改样式，重算需重新调用。


## FocusManager (class)

即时模式 UI 的焦点/悬停/按压状态机：按控件 id 记录当前与
上一渲染帧的三个目标 id，维护 Tab 焦点环、嵌套 id 段与
IME 会话跟随。App 在解析每帧指针/键盘事件时写入，
控件在渲染时查询。

- int focusedId;

- int hoveredId;

- int pressedId;

- int prevFocusedId;

- int prevHoveredId;

- int prevPressedId;

- int nextId;

- List<int> tabOrder;

- List<int> scopeReturn;
  - 嵌套的 id 段：PushIds 时压入当前计数器，PopIds 时恢复。

- List<int> textIds;
  - 文本可编辑控件每帧登记的 id；焦点落在其中之一才开
    IME 会话（每帧随 ResetIds 重建）。

- int imeSessionId;
  - 当前 IME 会话归属的控件 id（-1=会话关闭）。只在
    翻转时通知后端；Android 软键盘随会话显隐。

- FocusManager()

- int AllocId()
  - 本帧的下一个即时模式 id（按注册顺序递增，从 0 开始）。

- void PushIds(int first)
  - 即时模式 id 按绘制顺序递增，所以一个区域多画 / 少画
    一个控件，就会把它后面所有控件的 id 整体移位；而指针
    目标是按上一帧的 id 解析的，于是这一帧的点击会落到
    另一个控件上（在设计器里点一下就切换了后面的代码页）。
    宿主把每个大区域（功能区、各面板、标签条、编辑区）包在
    自己的 id 段里，区域内部的增减就不会惊动其他区域。

- void PopIds()
  - 结束当前 id 段，恢复 PushIds 之前的计数器（栈空时空操作）。

- void ResetIds()
  - 帧开始时调用：id 计数归零，Tab 环、id 段栈与文本控件表重建。

- void RegisterFocusable(int id)
  - 可聚焦控件每帧（按渲染顺序）记录自身，使键盘
    Tab 遍历拥有稳定、按布局排序的环。

- void RegisterTextEditable(int id)
  - 文本可编辑控件（Input/TextArea/InputOtp/InputNumber 一类）
    每帧随 RegisterFocusable 一并登记，供 IME 会话跟随判断。

- int IndexOf(int id)
  - id 在 Tab 环中的下标，不在环中时 -1。

- void FocusStep(int dir)
  - 将焦点移到下一个可聚焦控件（循环）。`dir` 为 +1 表示 Tab，
    -1 表示 Shift+Tab。若无任何可聚焦控件渲染则为空操作。

- bool IsFocused(int id)
  - id 当前持有键盘焦点时为 true。

- bool IsHovered(int id)
  - 指针当前悬停在 id 上时为 true。

- bool IsPressed(int id)
  - id 是当前按下目标时为 true。

- bool WasFocused(int id)
  - 上一渲染帧 id 持有焦点时为 true（配合 IsFocused 检测获得/失去焦点）。

- bool WasHovered(int id)
  - 上一渲染帧指针悬停在 id 上时为 true（配合 IsHovered 检测进入/离开）。

- bool WasPressed(int id)
  - 上一渲染帧 id 是按下目标时为 true。

- void RollFrame()
  - 将实时 id 快照为“上一帧”基线。每渲染一帧调用一次，
    （在 App.PresentFrame 中）即控件查询完本帧的
    进入/离开/焦点转换之后。

- void UpdateImeSession()
  - IME 会话跟随文本焦点：焦点在本帧登记的文本控件上则开，
    否则关；只在翻转时触达后端。桌面端会话在建窗时已常开，
    此处的开是幂等空操作；Android 软键盘随会话显隐——
    会话常开会让键盘在没有任何可输入目标时也占住半屏。

- void SetFocused(int id)
  - 写入焦点 id（事件解析层在按下时调用，-1 = 无）。

- void SetHovered(int id)
  - 写入悬停 id（本帧命中测试的最顶层控件，-1 = 无）。

- void SetPressed(int id)
  - 写入按压 id（-1 = 无）。

- void ClearHover()
  - 清除悬停 id（-1）。

- void ClearPress()
  - 清除按压 id（-1）。

- void ClearFocus()
  - 清除焦点 id（-1）。


## Form (class)

保留模式 UI 的根：窗口本身作为一个组件。拥有 App
并驱动帧循环，每帧在标题栏装饰之下
布局并渲染整棵树。

- App app;

- string title;

- List<FormTask> tasks;
  - 周期任务（见 Every），在事件循环中按期触发。

- HandlerRegistry handlers;
  - 设计出的 `on<Event>` 绑定的 Name -> Action 表（与
    UiDoc/HandlerRegistry 契约相同）：.zform 存储处理器名，
    业务文件用 On() 注册 Action，生成的
    生成代码把每个控件的事件订阅到 Handle(name)。从未注册的
    处理器自然不会触发。

- Form(string title, int width, int height)
  - 构建底层窗口和 app。树可以在 Run() 之前
    组装并布局好。

- static Form Create(string title, int width, int height)
  - 浅色主题的窗口（默认外观）；标题栏的皮肤选择器仍可
    切换浅色/深色与已打包的皮肤。

- static Form CreateDark(string title, int width, int height)
  - 深色主题的窗口，且关闭皮肤切换（EnableSkins(0)）：
    外观锁定为内置深色主题。

- App GetApp()
  - 底层 App（画布、主题、事件泵、时钟）。

- void SetTitle(string text)
  - 运行时改写窗口标题：自绘标题栏下一帧就用新文字，
    同时同步操作系统窗口标题（任务栏/Alt-Tab）。

- string Title()
  - 当前窗口标题。

- override string StyleType()
  - 窗口根不是一张卡片：它就是客户区本身。因此它按
    `window` 解析样式（base.css 里无边框、无阴影、内边距 0），
    而不是落到"未知类型"的通用表面默认值上——那会给整个
    设计加上一圈外边框，并把内容往里缩 paddingLarge。

- Action frameHook;
  - 每帧回调（在事件处理之后、周期任务与渲染之前执行）。
    供宿主在保留模式循环中泵其它窗口 / 驱动动画 / 轮询
    后台任务（IDE 的多窗口 pump、向导等）。覆盖旧值。

- void FrameHook(Action a)
  - 安装每帧回调（覆盖旧值；回调时机见 frameHook 字段说明）。

- Action exitHook;
  - 事件循环结束（窗口关闭）后调用一次的回调，
    供宿主保存状态 / 清理。

- void OnExit(Action a)
  - 注册退出回调（事件循环结束、窗口关闭后调用一次；见 exitHook）。

- FormTask Every(int ms, Action a)
  - 每 `ms` 毫秒跑一次 `a`，由事件循环驱动（采集、报警
    扫描、趋势取点都用它）。任务跑完就请求重绘，因此
    它改的信号会在下一帧体现。

- void PumpTasks()
  - 到期的周期任务全部跑一遍，并把下一个到期时刻告知
    事件循环（以便在无输入时也能醒过来）。手写循环可
    直接调用它。

- Control Ctl(string name)
  - 第一个（深度优先）名为 `name` 的控件，或 null。
    设计器总是为每个字段分配唯一名称，因此实际中它是精确的；
    但你自己写的代码永远不要假定结果非空。

- T Get<T>(string name)
  - 类型化按名查找：`Checkbox c = form.Get<Checkbox>("agree");`
    名称不存在或控件不是该类型时返回 null。

- void On(string name, Action a)
  - 注册（或替换）绑定到设计处理器名的 Action。
    生成代码通过此表解析每个控件的 `on<Event>` 值，
    因此设计中的处理器名必须与此处一致。

- Action Handle(string name)
  - 为 `name` 注册的 Action；未注册时为 null。

- void Call(string name)
  - 运行为 `name` 注册的 Action（若有）。对未注册的名称
    安全（空操作）。让设计器和数据驱动代码无需持有
    控件引用即可触发处理器。

- void RenderFrame(App a)
  - 在当前帧中一次性测量、布局并绘制整棵树，
    位于装饰之下。公开以便手写循环可以组合调用它。

- void Run()
  - 标准保留模式循环：处理事件、泵子窗口、布局、渲染树、绘制
    装饰、呈现。子窗口（ChildWindow）与共享文件选择器由
    ChildWindows 注册表在此自动泵送，宿主无需手写任何泵逻辑。


## FormTask (class)

窗口上的一个周期任务（Form.Every 登记）。工控画面、
监控看板这类“定时重扫”的屏幕靠它驱动，不必自己
写事件循环。

- int periodMs;

- int dueMs;
  - 下次到期的时刻（App 的动画时钟）。

- Action work;

- FormTask(int ms, Action a)
  - 构造任务：周期钳制到 >= 1 毫秒，首次到期时刻由 Schedule 设定。

- int Period()
  - 任务周期（毫秒，最小 1）。

- int Due()
  - 下次到期时刻（App 动画时钟毫秒）。

- void Schedule(int atMs)
  - 安排下次到期时刻（由 Form.Every/PumpTasks 维护）。

- void Fire()
  - 执行任务体。


## Fx (class)

Fx — 面向控件和外观的声明式、可选动效。

每个效果都是自包含的静态方法，在给定的矩形*内部*绘制
（可能溢出处会 PushClip），因此开启某个效果不会改变
布局，也不会盖住相邻控件。基于时间的效果读取
帧时钟（App.nowMs）并自行重新调度动画帧，因此
调用方只需每帧声明一次：

Fx.BorderGlow(app, x, y, w, h, radius, t.primary, 2600, 220);
Fx.Specular(app, id, x, y, w, h, radius, 0xFFFFFFFF);

效果通过小型 FxOptions 包（见下）配置，使组件能够
以与 ChartOptions 相同的声明式方式暴露“开启了哪些效果”。

- static int Saw(App app, int periodMs)
  - 在 `periodMs` 内重复 0..1000 的锯齿波（线性斜坡，归零循环）。

- static int Pulse(App app, int periodMs)
  - 在 `periodMs` 内平滑的 0..1000..0 “呼吸”脉冲（缓动三角波）。

- static int Isqrt(int n)
  - 整数平方根（向下取整）。用于计算光标到边框的距离，
    使高光边缘光随真实距离平滑衰减。

- static void PointGlow(Canvas c, int cx, int cy, int r, int color, int maxAlpha)
  - 以 (cx,cy) 为中心的柔和发光：平滑的径向光晕（原生
    FillRadial），从核心的 `maxAlpha`（0..255）衰减到 `r` 处的 0。

- static void BorderGlow(App app, int x, int y, int w, int h, int radius, int color, int periodMs, int intensity)
  - 沿圆角矩形边框移动的光彗星：明亮扫描带经 FillRadial 逐点绘制，
    两侧平滑淡出，底下叠一圈微弱常驻边缘光。按 periodMs 循环，
    自行调度 33ms 动画帧；所有绘制裁剪在边框光点内，不改布局。

- static void Emboss(App app, int x, int y, int w, int h, int radius, bool pressed)
  - 拟物风格的凸起（按压时内凹）阴影对：左上浅阴影
    和右下深阴影，绘制在控件自身填充之后。

- static void DashedBorder(App app, int x, int y, int w, int h, int color)
  - 在已绘制的盒子上描出虚线边框（渲染器没有
    虚线图案），供 `dashed` 变体使用。

- static void Specular(App app, int id, int x, int y, int w, int h, int radius, int color)
  - 悬停时跟随光标的边框高光对：悬停等级（Ui.HoverLevelMsIn，
    0..1000）经缓动驱动 SpecularBorderHv，靠近光标的弧段与对角
    对称弧随悬停平滑淡入淡出；不自行调度动画帧。

- static void SpecularRun(App app, int x, int y, int w, int h, int radius, int color, int periodMs)
  - 高光“流动光”（reactbits specular-button）：一个紧凑的亮点
    拖着短小的发光尾迹，持续沿边框滑动，叠在
    微弱的常驻边缘光上。裁剪在矩形内，使其落在边框上
    不会溢出到相邻控件或盖住标签。

- static void SpecularBorderHv(App app, int x, int y, int w, int h, int radius, int color, int hv)
  - 跟随光标的高光（reactbits “specular-button”）：靠近光标的一小段
    边框亮起，同时在对角相对侧出现对称弧段，
    两侧都平滑淡出。`hv`（0..1000）
    在悬停时缓动显现这对弧段。裁剪在矩形内，使光
    落在边框上，不会溢出到相邻控件或标签。

- static void SpotlightHv(App app, int x, int y, int w, int h, int color, int reach, int maxAlpha, int hv)
  - 受缓动等级 `hv`（0..1000）控制的跟随光标聚光。作用范围与
    峰值透明度随 hv 缩放；静止时不绘制任何内容。裁剪在矩形内，
    使靠近边缘的光晕不会溢出到相邻控件。

- static void CardSheen(App app, int x, int y, int w, int h, int color, int periodMs)
  - 光泽：一条柔和的斜向光带在卡片上循环滑过，
    如同玻璃上的反光。在内容之前绘制。

- static void CardAurora(App app, int x, int y, int w, int h, int color)
  - 极光：几个大而柔和的色块在内容后方漂浮并呼吸，
    ——平静流动的渐变。透明度极低；在内容之前绘制。

- static void CardBreath(App app, int x, int y, int w, int h, int color, int periodMs)
  - 呼吸边缘光：整个边框的亮度轻柔脉动（不移动），
    如缓慢的吸气/呼气。光只在边框上，裁剪在内部。

- static void CardMotes(App app, int x, int y, int w, int h, int color)
  - 上升微尘：细小的柔光点缓慢向上漂移并循环回绕，如同余烬
    或光中的尘埃。裁剪在卡片内部；装饰性背景。

- static void Apply(App app, int x, int y, int w, int h, int radius, FxOptions o)
  - 在矩形内渲染 `o` 中启用的所有效果（裁剪在其中），
    使组件可以将可配置动效作为数据提供：表面动效
    （极光、光泽、微尘）加上边缘光（呼吸、边框辉光）再加上
    跟随光标聚光。在表面填充之后立即调用，使
    动效位于内容之后。

- static void BgLightPillar(App app, int x, int y, int w, int h, int color)
  - 光柱：几根柔和的竖直光柱在区域内缓慢漂移并
    呼吸。以竖直渐变绘制在填充之上。

- static void BgFloatingLines(App app, int x, int y, int w, int h, int color)
  - 浮动线条：细斜向丝线缓慢向上滚动并循环，
    环绕整个区域——宁静的动画背景。


## FxOptions (class)

声明式的逐控件效果开关，仿照 ChartOptions 模式，
使组件能以数据而非代码的方式指定“开启哪些动效”。

- bool ripple;

- bool specular;

- bool borderGlow;

- bool sheen;

- bool aurora;

- bool breath;

- bool motes;

- bool spotlight;

- int glowColor;

- int glowPeriodMs;

- FxOptions()


## HandlerEntry (class)

支撑 JSON UI 约定的 Name -> Action 表。视图文档只存
处理器的*名称*（如 `"onClick": "save"`）；业务代码注册
Handle("save", MyPage.Save) 一次性注册匹配的 Action。随后加载器
把每个 `on<Event>` 名称解析为其 Action 并订阅到
控件的事件（见 UiDoc.Wire）。保持设计器/JSON 与代码解耦：
双方都不直接引用对方，只共享字符串名称。

- string name;

- Action action;

- HandlerEntry(string name, Action action)


## HandlerRegistry (class)

Name -> Action 的注册表：保存 HandlerEntry 线性表，
按名称查找，供 UiDoc.Wire 把 JSON 事件名解析回 Action。

- List<HandlerEntry> entries;

- HandlerRegistry()

- void Set(string name, Action a)
  - 注册（或替换）绑定到 `name` 的 Action。

- bool Has(string name)
  - 是否已注册 `name`（不论 Action 是否为 null）。

- Action Get(string name)
  - 绑定到 `name` 的 Action，未注册时为 null。


## HitRegion (class)

一个命中矩形：控件 id、屏幕矩形与控件类型
（widgetType == -1 表示阻挡区，见 HitTester.blockers）。
`label` 是可选的语义标签（按钮文字、列名、操作名）：
dump hitregions 投影输出，供无障碍/自动化识别区域用途，
不参与命中解析；未标注时为空串。

- int id;

- int x;

- int y;

- int width;

- int height;

- int widgetType;

- string label;

- HitRegion(int id, int x, int y, int w, int h, int wtype)
  - 构造：逐字段赋值（池化复用改走 Set）。

- bool Contains(int px, int py)
  - 点 (px, py) 是否落在矩形内（左闭右开）。

- void Set(int id, int x, int y, int w, int h, int wtype)
  - 就地改写（供 HitTester 复用池中的对象）。


## HitTester (class)

每帧命中区注册表：控件渲染时登记矩形，鼠标/触摸事件据此
解析目标。附带阻挡区（模态遮罩）、事件锚点（按下/点击的
跨帧目标重绑定）与整帧快照（条带帧的事件解析基准）。

- List<HitRegion> regions;

- List<HitRegion> blockers;

- List<HitRegion> prevBlockers;

- List<HitRegion> poolA;

- List<HitRegion> poolB;

- bool useA;

- int used;

- List<int> anchorId;

- List<int> anchorX;

- List<int> anchorY;

- List<int> anchorW;

- List<int> anchorH;

- List<int> anchorType;

- List<int> anchorSet;

- List<int> snapId;

- List<int> snapX;

- List<int> snapY;

- List<int> snapW;

- List<int> snapH;

- List<int> snapType;

- int snapUsed;

- FocusManager focus;

- HitTester()
  - 构造：初始化双复用池、阻挡区表、锚点表与快照表。

- void BindFocus(FocusManager f)
  - 绑定焦点状态机，使按下锚点的矩形重绑同步到 pressedId
    （App 构造时调用一次；未绑定则只重绑锚点）。

- void KeepFullSnapshot()
  - 整帧（非条带帧）渲染结束时调用：把当前命中区拷贝为事件
    解析的基准。regions 是复用池，对象会被下一帧就地改写，因此
    必须按值拷贝（AnchorAt 只用到这六个 int）。

- void Clear()
  - 开启新的一帧：当前阻挡区转为 prevBlockers，切换到另一个
    复用池并把已用计数清零（上一帧对象留待就地改写）。

- int AnchorAt(int k, int px, int py, bool below)
  - 在最近一个完整帧的命中区快照上解析 (px, py) 的目标并记入
    锚点 `k`；`below` 为真时跳过阻挡区，解析其下方的控件（右键用）。

- void ClearAnchor(int k)
  - 作废锚点 `k`（id 复位为 -1）。

- int AnchorTypeOf(int k)
  - 锚点 `k` 最近一次 AnchorAt 命中的区域类型
    （HitRegion.widgetType，-1 = 阻挡区）。仅在 AnchorAt 返回
    id >= 0（命中）后读取才有意义；ClearAnchor 不重置类型。

- int AnchorIdOf(int k)
  - 锚点 `k` 当前对应的控件 id（本帧已按矩形改写过）。

- int RegionCount()
  - 本帧已注册的命中区数量（`regions` 是复用池，末尾
    可能残留上一帧的对象，遍历要以此为界）。

- HitRegion RegionAt(int i)
  - 第 i 个已注册的命中区（i < RegionCount()）。

- void RegisterRect(int id, int x, int y, int w, int h, int wtype)
  - 注册一个命中区，复用池中的对象（首选形式：不分配）。

- void RegisterRectL(int id, int x, int y, int w, int h, int wtype, string label)
  - 带语义标签的注册：标签随后写入 HitRegion，dump hitregions
    原样投影（无障碍/自动化读名，命中解析不用它）。

- void Register(HitRegion region)
  - 按现成的 HitRegion 注册本帧命中区（字段展开转发 RegisterRect）。

- bool BlockerAt(int px, int py)
  - 当本帧已注册的阻挡层覆盖该点时返回 true——即
    查询方表面已铺设自己的遮罩，正处于阻挡层
    主体（阻挡之上），而非其下方的内容。

- bool PrevBlockerAt(int px, int py)
  - 当上一帧的阻挡层覆盖该点时返回 true。供
    页面内容（在本帧覆盖层注册前渲染）
    判断自身是否位于模态框/弹出层/浮动窗口之下。

- int HitTest(int px, int py)
  - 本帧命中区中最顶层（最后注册）覆盖 (px, py) 的控件 id，
    无命中时 -1。

- int HitTestBelowBlockers(int px, int py)
  - 与 HitTest 相同，但跳过阻挡区域，返回其**下方**的控件。
    供右键使用：上下文菜单打开时它的遮罩会吞掉一切，于是
    在别处右键什么也不会发生（必须先关掉菜单）；右键改为
    解析到遮罩下的控件后，菜单就直接换到新位置重开。

- int HitTestFrom(int px, int py, int from)
  - 与 HitTestBelowBlockers 相同，但只匹配 `from` 下标**之后**
    注册的区域（跳过阻挡区）。弹层在覆盖阶段用它识别「自己
    内部注册的控件」——内嵌滚动条、搜索框等，它们在弹层
    blocker 之后才注册；而不带基线时，弹层正下方的内容控件
    早在内容帧就注册在前，会被误当成弹层内部控件，令弹层把
    本该选中选项的释放点击整个吞掉（SelectBox 弹层盖住滑杆/
    输入框/表格行时选项选不中）。

- List<int> RectOf(int id)
  - 上一帧为 `id` 注册的区域，以扁平的 [x,y,w,h] 列表表示；
    若该 id 未拥有区域则为 null。让框架只重绘
    状态变化的控件，而不是整个窗口。

- int GetWidgetType(int id)
  - id 注册的控件类型（HitRegion.widgetType），未注册时 -1。


## Icon (class)

图标集：语义名称映射到 "Segoe MDL2 Assets" 码点。
绘制在画布上进行，因此使用名称作为
`canvas.DrawGlyph("close", x, y, size, color)`，或在控件内部使用
`canvas.DrawGlyphIn("close", bx, by, bw, bh, size, color)`。

- static int Codepoint(string name)
  - 将语义图标名称映射到 Segoe MDL2 Assets 码点。
    未知名称返回 0（不绘制任何内容）。

- static string SvgName(string name)
  - 语义名到 SVG 图标名（Tabler 原名）的差异映射：只列与 Tabler
    同名不同形的那些；返回 "" 表示同名直用。DrawGlyph/DrawGlyphIn
    优先走 IconSvg，这里查不到的再回退 IconVector 手绘。
    目标名均核对过存在于 IconSvgData；align-top/middle/bottom 上游
    没有对应形，保持手绘。

- static List<string> Names()
  - Codepoint 认识的所有图标名，按显示顺序。让调用方（如
    组件画廊）无需硬编码即可枚举完整图标集。


## IconSvg (class)

SVG 矢量图标集：精选 Tabler Icons 子集（MIT 授权），数据与名称
表在 IconSvgData（JSON 数据包 stdlib/Gui/icons/tabler.json，发布时
自动 --embed 进可执行文件），由 scripts/gen_icons_tabler.py 生成。

与 Icon/IconVector（手绘线段近似，零依赖）互补：框架内部的
语义图标（"close"、"check" 等固定小集合）继续走 canvas.DrawGlyph；
需要更大覆盖面时用这里的 Tabler 原名，如
`IconSvg.Draw(canvas, "brand-github", x, y, 24, color)`。

实现：把 SVG body 包装成完整文档，经 Canvas.ImageLoadSvg（nanosvg）
光栅到 (box,box) 并以 `mem:i...` key 进入运行时图像缓存，再用
BlitImage 贴图。运行时的 mem 图像缓存容量有限（ZAN_IMG_MEM_CAP，
当前 64）且按 FIFO 逐出，契约是"Zan 侧保留来源、按需重注册"
（同 Image 组件）；因此这里不用自己的"已注册"表，而是每次绘制
前用 Canvas.ImageWidth(key) 探测——key 不在缓存（尚未光栅或已被
逐出）就重新光栅一次，再 BlitImage。同一（名称, 尺寸, 颜色）在
缓存存活期间只光栅一次；24~48px 的位图每份约 2~9 KB。

- static string Alias(string name)
  - 语义别名 → Tabler 名。Tabler 没有的常用叫法在这里兜底，
    让 Draw("unlock", ...) 这类习惯用名直接可用。

- static void Draw(Canvas c, string name, int x, int y, int box, int color)
  - 在 (x,y) 处绘制 box×box 的图标。color 为 ARGB，alpha<255
    以不透明度落到 SVG 的 fill/stroke 上。未知名称不绘制。

- static void DrawIn(Canvas c, int rx, int ry, int rw, int rh, string name, int color)
  - 在矩形内居中绘制，box 取矩形较短边。

- static int Count()
  - 表内图标个数。

- static List<string> Names()
  - 全部图标名（升序），供画廊 / 文档工具枚举。

- static string HexColor(int color)
  - ARGB 的低三字节 → "#rrggbb"（小写）。

- static string AlphaAttrs(int color)
  - alpha<255 时给出 fill/stroke 不透明度属性；不透明返回 ""。
    alpha=0 也输出（0.00 = 完全透明），不能回落到不透明。


## IconSvgData (class)

IconSvg 的数据表:Tabler Icons 精选子集(MIT 授权,
https://github.com/tabler/tabler-icons),由 scripts/gen_icons_tabler.py
生成——**生成物,请勿手改**;要换子集或更新上游版本时重跑该脚本。

数据以 JSON 包(stdlib/Gui/icons/tabler.json)随标准库走,编译发布时经
`zanc --embed` 烤进可执行镜像,运行时惰性解析一次:没画过图标的程序
只带一份 ~260KB 的数据文件,不再把它展开成代码节;画了才在内存里建表。

发现顺序(与皮肤 Skin.Roots 同一思路,让应用可以替换/扩充图标包):
1. 环境变量 ZAN_GUI_ICONS 指向的文件或目录;
2. exe 旁 icons/、assets/icons/;
3. exe 内嵌资源 icons/(*.json);
4. 标准库副本 stdlib/Gui/icons/(开发树)。
后发现的同名文件不覆盖先命中的;不同名的 JSON 与内置包合并(追加/覆盖
同名图标),所以应用只需放一个自己的 json 就能加图标或换掉个别图标。

约定:
· 包形如 {"图标名": "SVG body", ...},名称升序(二分查找要求);
· 所有图标均为 24x24 viewBox,IconSvg 据此包装 SVG 文档;
· body 里的双引号改写为单引号,避免 JSON/Zan 字面量转义;
· body 保留 currentColor 占位,颜色由 IconSvg 在绘制时替换。

- static List<string> names;

- static List<string> bodies;

- static void Ensure()
  - 惰性建表：首次访问时按发现顺序合并全部 JSON 包并按名排序；
    无任何包可读时也建立空表，行为与“未知图标名”一致。

- static void Merge(List<string> names, List<string> bodies, string json)
  - 有序合并一份 JSON 包到 (names, bodies):先二分定位覆盖同名项,
    再按序插入新项,调用方最后统一排序由本函数增量维护。

- static List<string> Packages()
  - JSON 包文本,按发现顺序拼接:磁盘命中的在前(应用自定义优先),
    内嵌/标准库兜底的在后;同 key 后写不覆盖先写(Merge 先到先得)。

- static void CollectDir(string dir, List<string> outp)
  - 把目录下所有 *.json 的文本按文件名序追加到 outp
    （目录不存在时为空操作）。

- static string Leaf(string path)
  - 路径的文件名部分（最后一个 / 或 \ 之后）。

- static string ReadFile(string path)
  - 读取整个文本文件；读不到/出错时返回 ""（绝不返回 null）。

- static void SortByNames(List<string> names, List<string> bodies)
  - (names, bodies) 按名称升序原地排序(插入排序:包内已经接近有序,
    合并场景位移量小;表规模 ~1k,构造期一次性成本可忽略)。

- [DllImport("crt")]static extern string getenv(string name);
  - 读取环境变量(缺失返回 "")。

- static string Env(string name)
  - getenv 的包装：null 转为 ""。

- static string ExeDir()
  - 正在运行的可执行文件所在目录(不含末尾分隔符),无法确定时返回 ""。

- [DllImport("crt")]static extern int zan_embed_has(string name);

- [DllImport("crt")]static extern string zan_embed_read(string name);

- [DllImport("crt")]static extern string zan_embed_list(string prefix);

- static int Count()
  - 表内图标个数。

- static List<string> Names()
  - 全部图标名(升序)。供画廊、文档工具枚举。

- static int IndexOf(string name)
  - 二分查找图标名,未命中返回 -1。

- static string Body(int index)
  - 按下标取 SVG body(不含 <svg> 外壳)。


## IconVector (class)

图标字形以可缩放矢量图元绘制，而非字体字形：
“Segoe MDL2 Assets” 图标字体只存在于 Windows 10+，因此字体路径
在 macOS/Linux 上会显示不同，在 Win7 上会失效。每个形状都由
Canvas 的线段、矩形、圆和扇形构成，因此图标在每个后端
上的栅格化结果完全一致。

Canvas.DrawIcon 是入口；请调用它，而不是这些辅助函数。

- static double Pi()
  - π 常量（双精度）。

- static int Iabs(int v)
  - 整数绝对值。

- static void Circle(Canvas s, int cx, int cy, int radius, int color, int thickness)
  - 使用后端原生抗锯齿圆轮廓，不在整数坐标上离散成多边形。

- static void Arrow(Canvas s, int x0, int y0, int x1, int y1, int color, int thickness)
  - 从 (x0,y0) 到 (x1,y1) 的线段，远端带两翼；两翼
    沿线段所走的轴线两侧展开。

- static List<int> StarPoints(int cx, int cy, int radius)
  - 五角星的十个交替外/内顶点，从
    12 点钟方向开始，按 x0,y0,x1,y1,... 交错返回。

- static void Star(Canvas s, int cx, int cy, int radius, int color, int thickness)
  - 线框五角星：依次连接 StarPoints 的十个顶点。

- static bool PtInPoly(List<int> pts, int n, int x, int y)
  - 对交错顶点做奇偶规则的点在多边形内测试（射线投射）。

- static void FillStar(Canvas s, int cx, int cy, int radius, int color)
  - 实心五角星：扫描线填充，每段内部像素
    输出为一个 1px 高的矩形。

- static void Draw(Canvas s, int x, int y, int box, int color, int codepoint)
  - 在 (x,y) 处的 `box` 大小正方形内绘制 `codepoint` 的字形。
    未知码点不绘制任何内容。


## ImageHttp (class)

Image 控件与 DataTable 图片列共用的网络图片加载器。
分工与 DownloadJob 一致：取回在后台 OS 线程上以协程 await 完成
（不阻塞 UI），结果经 `App.Post` 封送回 UI 线程再解码
注册；单个共享 worker 逐条处理排队的请求。UI 线程入口是
`Fetch`（控件模式）与 `EnsureUrl`（无控件
的 URL 槽模式）。

- class Req
  - 一次取回请求：UI 线程排队，worker 领走，完成后经 Post 通知。
    img 为 null 时是 URL 槽请求（见 EnsureUrl）。

- class Slot
  - URL 槽：一段 URL 的加载状态。就绪后 key 指向已注册的
    `mem:` 图像，可反复绘制；失败保持 2，不自动重试。

- static nint lockHandle;

- static List<Req> pending;

- static bool workerStarted;

- static Dict <string, Slot> urlSlots;

- static int slotSeq;

- static string EnsureUrl(App app, string url)
  - UI 线程调用：确保 `url` 的图片取回已排队（无控件场景，例如
    DataTable 图片列）。就绪返回已注册的 `mem:` key，加载中或
    失败返回 null——同一 URL 只排队一次，结果缓存供后续帧直用。

- static void Fetch(App app, Image img, string url, string key)
  - UI 线程调用：排队一次 URL 取回。worker 首次需要时启动。

- static void WorkerLoop()
  - worker 线程入口：逐条取回直到队列清空，然后退出
    （下一次 Fetch 会重新拉起）。await 让出期间 IO 反应器推进传输。

- static Req Take()

- static async int FetchOne(Req r)
  - 取回单个 URL。传输里任何一处抛出（DNS、TLS、断开的套接字、
    超时）都必须变成一条错误结果：不接住的话 worker 静静死掉，
    控件会永远停在加载占位上。

- static void Apply(Req r, byte[]bytes, string body, int len, string err)
  - UI 线程：把取回的字节注册进图像缓存并通知消费方。解码必须
    发生在 UI 线程（图像注册表与光栅器只从 UI 线程触碰）。


## Insets (class)

四边内边距/外边距（上右下左）。

- int top;

- int right;

- int bottom;

- int left;

- Insets(int top, int right, int bottom, int left)

- static Insets Uniform(int val)
  - 四边同值的便捷构造。

- static Insets Symmetric(int vertical, int horizontal)
  - 上下同值、左右同值的便捷构造。

- int Horizontal()
  - 水平总跨度（left+right）。

- int Vertical()
  - 垂直总跨度（top+bottom）。


## Mat4 (class)

3D 数学：行主序 4x4 矩阵（float[16]，下标 row*4+col）、
右手坐标系（+y 上、+z 朝向观察者、-z 为视线方向）、列向量约定
（v' = M * v）。组合顺序与约定一致：Mvp = P * V * M。

这个层是纯 Zan：矩阵只在 CPU 上组合一次再交给运行时的 3D 管线
（Canvas.DrawMesh3D），不参与逐顶点运算——后者是后端（GPU 或
未来的 CPU 软光栅）的事。

- public float[]m;

- public Mat4()

- public static Mat4 Identity()
  - 单位矩阵。

- public static Mat4 Translate(float x, float y, float z)

- public static Mat4 Scale(float x, float y, float z)

- public static Mat4 RotateAxis(float ax, float ay, float az, float rad)
  - 绕任意单位轴的旋转（Rodrigues 公式展开），角度弧度。

- public static Mat4 Mul(Mat4 a, Mat4 b)
  - 矩阵乘 this * b（先施 b 再施 this，与 v' = M*v 一致）。

- public Mat4 Mul(Mat4 b)

- public static Mat4 Perspective(float fovYRad, float aspect, float nearZ, float farZ)
  - 透视投影（D3D 风格深度 0..1），fovY 弧度，近远必须为正。

- public static Mat4 Ortho(float left, float right, float bottom, float top, float nearZ, float farZ)
  - 正交投影（D3D 风格深度 0..1），窗口 3D 视图与 HUD 场景用。

- public static Mat4 LookAt(float ex, float ey, float ez, float tx, float ty, float tz, float ux, float uy, float uz)
  - lookAt 视图矩阵（右手系，eye 望向 target，up 任意非零）。

- public float[]ToColumnMajor()
  - 转列主序 float[16]（GPU 侧 uniformMatrix4fv 的约定）。


## MenuItem (class)

富上下文菜单的一个条目（参见 `OverlayPopup.RichMenu`）。
`kind`：0 = 可点击项，1 = 分隔线，2 = 分组标题，3 = 子菜单
父项（悬停时其 `children` 在侧面板中展开，孙级同理再展开一层）。
`action` 是选择叶子项时写回调用方结果信号的值。
`swatch`/`swatch2` 是可选项的色块（ARGB；0 = 无）：单色画一枚
圆角色块，双色左右对拼（色阶预设）——画在图标列，替代图标位。

- int kind;

- string label;

- string icon;

- string shortcut;

- string key;
  - 稳定标识（Gui.Widget.Menu v2 的选中/展开 key）；空串时菜单退化为用 label 当 key。上下文菜单忽略本字段。

- int action;

- bool disabled;

- bool danger;

- int swatch;

- int swatch2;

- List<MenuItem> children;

- static MenuItem Item(string label, string icon, int action)
  - 可点击项工厂（各静态构造的公共底座）。

- static MenuItem SwatchItem(string label, string icon, int action, int c0, int c1)
  - 带色块的可点击项：`c0` 必给；`c1` 非 0 时画双色对拼
    色块（色阶类预设），为 0 时单色。色块占用图标列。

- static MenuItem Shortcut(string label, string icon, string sc, int action)
  - 带快捷键提示的可点击项。

- static MenuItem Disabled(string label, string icon, int action)
  - 置灰不可点项。

- static MenuItem Danger(string label, string icon, int action)
  - 危险操作项（红色）。

- static MenuItem DangerShortcut(string label, string icon, string sc, int action)
  - 危险操作项 + 快捷键提示。

- static MenuItem Separator()
  - 分隔线（kind=1）。

- static MenuItem Header(string label)
  - 分组标题（kind=2，不可点）。

- static MenuItem Submenu(string label, string icon, List<MenuItem> children)
  - 子菜单（kind=3，悬停时在侧面板展开 children）。


## Mesh3D (class)

网格构建器：交错顶点（px,py,pz, nx,ny,nz, u,v，每顶点 8 个 float）
+ ushort 索引，与运行时 3D 管线的顶点布局逐字节对应。Build 之后可复用
Upload 到不同表面。

- List<float> v;

- List<ushort> idx;

- public Mesh3D()

- public int Vertex(float px, float py, float pz, float nx, float ny, float nz, float u, float vv)
  - 追加一个顶点，返回其索引。

- public void Triangle(int a, int b, int c)
  - 按逆时针（从观察方向看）追加一个三角形，保证正面朝外。

- public void Quad(int a, int b, int c, int d)
  - 两个三角形组成一个四边形（a,b,c,d 逆时针）。

- public int VertexCount()

- public int IndexCount()

- public float[]VertexArray()
  - 交错顶点缓冲（Canvas.MeshUpload 封送用）。

- public ushort[]IndexArray()
  - 三角索引缓冲（Canvas.MeshUpload 封送用）。

- public void AddCubeAt(float cx, float cy, float cz)
  - 以立方体（边长 2，中心 (cx,cy,cz)）填充此网格，六面 UV 全贴。
    其余同 AddCube。

- public void AddCube()
  - 以单位立方体（边长 2，中心原点）填充此网格，六面 UV 全贴。

- public void AddGroundDisc(int n, float radius)
  - 以 XZ 平面圆盘（n 边形，法线 +y）填充，UV 极坐标展开。


## NativeLayer (class)

原生浮层（WebView2 的子 HWND、WKWebView 的 NSView 等）的遮挡裁剪。

这些视图是 OS 层的兄弟层，永远画在软件画布之上：不管 Zan 侧的
绘制顺序如何，标签条、右键菜单、下拉、模态对话框都会被网页盖住。
唯一的解法是在原生层按区域裁剪，因此控件不再自己决定可见性，
而是每帧向 App 登记「我要占这个矩形」（Register），由
App.PresentFrame 在所有自绘 UI（含 RunOverlays）之后统一结算：
可见区域 = 自身矩形 − 本帧所有遮挡区，再经 NativeClipFn 下发。

遮挡区有两个来源：命中测试里的拦截区（App.BlockHitsRect 注册的
弹层/遮罩，widgetType == -1），以及不铺遮罩但确实画在上面的浮动
内容自行调用的 Occlude()（提示气泡、Toast 之类）。

- static int MaxRects()
  - 单个浮层最多保留的可见矩形数。菜单/弹层通常只切出
    三五块；上限只是防止病态的遮挡组合把矩形炸开，超出后
    停止继续切分（宁可少切一块也不要每帧算爆）。

- static List<NativeLayerReq> tracked;
  - 曾经登记过的浮层（跨帧保留，每个句柄一条）。某一帧没有
    登记的浮层说明它这帧不该上屏：设计出来的控件树在隐藏的
    标签页上根本不会走 OnPaint，没有任何代码替它调 Hide()，
    原生兄弟层就会一直挂在窗口上盖住新的活动页。这里兜底把
    它裁成空区域（后端即隐藏）。

- static void Register(App app, int handle, int x, int y, int w, int h, NativeClipFn apply)
  - 登记本帧的原生浮层。`handle` 是后端句柄，矩形是画布坐标，
    `apply` 必须是普通静态方法（委托是纯函数指针）。

- static void Track(NativeLayerReq req)
  - 记住这个句柄（同一句柄只留最新一条）。

- static void Forget(int handle)
  - 忘掉一个已销毁的句柄（后端句柄可被复用，留着会把裁剪
    下发到别人的视图上）。

- static bool Registered(App app, int handle)
  - 本帧 `app` 是否登记过该句柄。

- static void Occlude(App app, int x, int y, int w, int h)
  - 声明一块画在原生浮层之上、但没有注册命中拦截区的区域。

- static void Flush(App app)
  - 结算本帧：给每个登记的浮层算出可见区域并下发。由
    App.PresentFrame 在弹层渲染之后调用。

- static void HideUnregistered(App app)
  - 本窗口本帧没有登记的已知浮层：裁成空区域，后端隐藏它。

- static List<int> Occluders(App app)
  - 本帧的遮挡矩形：命中拦截区 + 显式登记的浮动内容。

- static bool HitOnly(App app, int id)
  - 该拦截区是否只吞点击、不画像素（BlockHitsBelow 的全窗口
    捕获层）：这种拦截区不遮挡原生浮层。

- static List<int> Subtract(List<int> rects, int ox, int oy, int ow, int oh)
  - rects（x,y,w,h 四元组）减去矩形 (ox,oy,ow,oh)。每块被切中的
    矩形最多裂成上/下/左/右四块。

- static string Spec(List<int> rects)
  - 把矩形并集编码成后端的 "x,y,w,h;..." 规格；空集合返回 ""。


## NativeLayerReq (class)

一个原生浮层本帧申请占用的矩形，以及下发裁剪结果的回调。

- App owner;
  - 登记它的窗口：一个进程可以开多个窗口，结算某个窗口这一帧时
    不能去动别的窗口的浮层。

- int handle;

- int x;

- int y;

- int w;

- int h;

- NativeClipFn apply;

- NativeLayerReq(App owner, int handle, int x, int y, int w, int h, NativeClipFn apply)


## Nav (class)

- static List<NavRoute> routes;

- static List<NavWindow> openStack;

- static List<NavEmbed> embeds;

- static int nextIdBase;

- static NavRoute Define(string name, NavPageFactory make)
  - 登记路由（同名重登记=覆盖工厂/标题，钩子与 keepAlive 保留）。

- static NavRoute DefineTitle(string name, string title, NavPageFactory make)
  - 登记路由并指定标题（窗口标题 / 标签文案）。

- static void OnEnter(string name, NavEnterHandler h)
  - 挂进入钩子（窗口打开 / 参数重放 / 出口页构建时回调）。

- static void SetKeepAlive(string name, bool on)
  - 配出口存活策略：false = 切走销毁、再进重建（重页面按需开）。

- static void SetWindowSize(string name, int width, int height)
  - 配窗口尺寸（逻辑像素）。

- static NavRoute Find(string name)
  - 查路由（未登记返回 null）。

- static void Open(string name, App parent)
  - 打开路由（单例）：已开则激活 + 重放参数；未开则建副窗口。
    parent 是属主应用（换肤/不透明度跟随它），通常传
    `MyForm.__form.GetApp()`。

- static void OpenArgs(string name, App parent, JsonValue args)
  - 打开路由并携带参数（进入钩子收到）。

- static NavWindow FindOpen(string name)
  - 查某路由当前打开的窗口（后开者优先；未开返回 null）。

- static bool Back()
  - 返回：关掉最近打开的导航窗口（栈顶）。没有导航窗口时空操作，
    调用方（安卓 AC_BACK 的 kind-8 分支）据此自行决定退应用。

- static void CloseAll()
  - 关闭全部导航窗口。

- static void Embed(Tabs tabs, string routeCsv)
  - 把标签条绑成路由出口：csv 里的每条路由一个标签（按序），
    首个标签立即建页，其余首次选中才建（惰性）。keepAlive 默认开，
    `SetKeepAlive(name, false)` 配成临态。一条 Tabs 只绑一次。

- static void EmbedChanged()
  - TabChanged 的统一处理：遍历全部出口领走选中变化（TakeChanged
    是一次性读数，只有真变了的标签条领得到），先按临态策略清理
    别的页，再惰性建当前页。

- static void TryAddEmbedTab(NavEmbed e, string name)
  - 出口加一个标签：路由存在才加（名字表与标签下标保持对齐）。

- static void EnsureEmbedPage(NavEmbed e, int i)
  - 保证第 i 个标签的页面已构建：keepAlive 且已有内容直接复用；
    临态页重建。构建后回调进入钩子（无窗口，win 传 null）。

- static void Prune()
  - 清理栈里已被用户点标题栏关掉的窗口。

- static void Activate(NavWindow w)
  - 激活窗口（置前台）。只有 Windows 有现成的原生入口；其它平台
    交给宿主窗口管理器，属主泵循环会把它带上来。

- static int NextIdBase()


## NavEmbed (class)

一个 Embed 出口：标签条 + 各标签对应的路由名（下标对齐）。

- Tabs tabs;

- List<string> names;


## NavRoute (class)

一条路由：名字（键）+ 标题（窗口/标签文案）+ 页面工厂 + 进入钩子。

- string name;

- string title;

- NavPageFactory make;

- NavEnterHandler enter;

- bool keepAlive;
  - Embed 出口的存活策略：true（默认）切走保留，false 切走销毁。

- int winW;
  - 窗口尺寸（逻辑像素；<=0 用 NavWindow 的 560 缺省）。

- int winH;


## NavWindow (class)

Nav 打开的副窗口：把路由的标题/尺寸钉到 ChildWindow 的虚约定上，
页面树来自路由工厂，参数经 OnEnter 回注。

- NavRoute rt;

- int w;

- int h;

- int idBase;

- NavWindow()
  - 构造：缺省尺寸 560x560（路由可用 SetWindowSize 覆盖）。

- override string Title()

- override int Width()

- override int Height()

- override int IdBase()
  - 每个窗口一枚固定的 WidgetId 基线（主窗口不回卷进程级计数，
    子窗口不钉基线则按钮 hover/press 每帧错位）。

- void OpenFor(NavRoute r, App parent, JsonValue args)
  - 用路由的工厂建树、挂根并按父窗口的皮肤/不透明度约定打开。
    打开后回调一次 OnEnter。

- void Replay(JsonValue args)
  - 已开窗口被再次 Open：只重放参数（原版对已开网页标签重新
    Navigate 的语义），不重建树。


## OverlayPopup (class)

框架拥有的浮动选项列表弹窗（由 Select / SelectBox /
Dropdown / Menu 使用）。Zan 委托无法捕获局部变量或绑定 `this`，因此
弹窗以*数据*形式描述：控件在主渲染阶段将其交给 <c>App.AddOverlay</c>，
<c>App.RunOverlays</c> 在所有内容之后绘制并分发它，
因此它始终绘制在最上层，并拥有最顶部的命中
区域（HitTester 后注册者优先）。选择选项会写入
绑定的模型、触发 `onChange` 并关闭弹窗；
在其它任何位置按压都会关闭它（单一、集中式分发——没有逐控件事件
抓取，应用代码中也没有 z-order 取巧）。

- static int lastRichHover;
  - 富菜单上一帧悬停到的行（即时模式绘制，用它判断是否值得
    为一次鼠标移动重绘）。

- static int occlAx;

- static int occlAy;

- static int occlAw;

- static int occlAh;

- static int occlBx;

- static int occlBy;

- static int occlBw;

- static int occlBh;

- static int subGraceRow;
  - 子菜单悬停宽限：指针从父行斜穿父面板其它行去子面板
    （子面板贴边被上钳，必然要掠过别行）的途中，掠过的
    那几帧不该立刻关掉已开的子菜单——记下开始掠过的行与
    时刻，满宽限仍停在非子菜单行上才关/换。第二组同义，
    用于孙级面板。

- static int subGraceMs;

- static int subGraceRow2;

- static int subGraceMs2;

- int x;

- int y;

- int w;

- List<string> options;

- int baseId;

- SignalInt model;

- int triggerId;

- SignalBool openFlag;

- SignalInt scrollModel;

- UiEvent onChange;

- bool showCheck;

- bool rich;

- bool themeDrawerMode;

- List<MenuItem> menuItems;

- SignalInt result;

- SignalInt subOpen;

- SignalInt subOpen2;

- bool richSub2;

- SignalInt richScroll;

- int richMaxRows;

- int richMinW;

- Control host;

- static OverlayPopup RichMenu(int x, int y, List<MenuItem> items, int baseId, SignalInt result, SignalBool openFlag, SignalInt subOpen)
  - 富上下文菜单：包含 `items`（参见 MenuItem）的浮动面板，
    支持图标、分隔线、分组标题和两层悬停展开的
    子菜单。选中的叶子 `action` 写入 `result`；
    选择、外部按压或 Escape 都会关闭面板。`baseId` 必须是稳定的
    至少 256 个 id 的连续块（WidgetId.Block(256)）；走孙级扩展版
    时要 384（主面板 +128 = 子面板，+256 = 孙面板）。

- static OverlayPopup RichMenu(int x, int y, List<MenuItem> items, int baseId, SignalInt result, SignalBool openFlag, SignalInt subOpen, SignalInt scroll, int maxRows, int minW)
  - 滚动/宽度扩展版富菜单：`scroll` + `maxRows` 让长菜单只显示
    maxRows 行并出滚动条（偏移由宿主跨帧持有）；`minW` 给面板
    宽度下限。其余同上。

- static OverlayPopup RichMenu(int x, int y, List<MenuItem> items, int baseId, SignalInt result, SignalBool openFlag, SignalInt subOpen, SignalInt scroll, int maxRows, int minW, SignalInt subOpen2)
  - 孙级扩展版：`subOpen2` 持有子面板里展开的孙级行
    （-1 无，宿主跨帧持有并在菜单开/关时复位）。子面板里的
    kind=3 行悬停时再展开一层面板；不用孙级传 null。

- static OverlayPopup ThemeDrawer(int baseId, int triggerId, SignalBool openFlag, SignalInt scrollModel)
  - 外观抽屉：右侧停靠的设置面板，包含外观
    列表、一键动画开/关开关、背景特效选择器和
    强调色色板。`baseId` 必须是至少
    PresetCount + 24 个 id 的稳定块；状态存放在 App 上（themeMenuModel、
    fxKindOverride、accentOverride、fxEnabled）。

- static OverlayPopup Host(Control h)
  - 完全自定义的浮动层：`h` 通过 OnPaintOverlay 重写绘制自己的弹窗（chrome、选项
    及输入分发）。让任何浮动控件
    （Select 框、Popover、Tooltip 等）将整个弹窗交给
    覆盖层阶段处理——绘制在所有内容之上，命中区域最后注册——
    而无需专门的 OverlayPopup 类型。控件在主阶段将
    锚点几何存入自己的字段，并在打开时
    调用 `app.AddOverlay(OverlayPopup.Host(this))`。

- static int FitX(App app, int x, int w)
  - 将锚定在 `x`、宽度为 `w` 的弹窗保持在窗口内。

- static int FitH(App app, int h)
  - 将弹窗高度限制在窗口可显示范围内。

- static int FitY(App app, int anchorY, int trigH, int h)
  - 触发控件下方弹窗的垂直定位：`anchorY` 是
    首选顶部（触发控件底部加间距），`trigH` 是触发控件
    高度。会超出底部的弹窗翻转到触发控件上方，
    只有那里也放不下时才会被限制在窗口内
    ——因此靠近底部边缘的下拉框会向上展开，而不是被
    窗口截断。

- static OverlayPopup OptionList(int x, int y, int w, List<string> options, int baseId, SignalInt model, int triggerId, SignalBool openFlag, SignalInt scrollModel, UiEvent onChange)
  - 带选中对勾的选项列表弹窗：点击选项写入 `model`、触发
    `onChange` 并关闭；在弹窗和触发控件之外按压或 Escape 也关闭。
    第 i 个选项的命中 id 为 `baseId + i`，滚动偏移存于 `scrollModel`。

- static OverlayPopup Menu(int x, int y, int w, List<string> options, int baseId, SignalInt model, int triggerId, SignalBool openFlag, SignalInt scrollModel, UiEvent onChange)
  - 操作菜单（如 Dropdown）：与 OptionList 相同的锚定、遮罩、外部点击关闭
    弹窗，但没有常驻的选中对勾。
    选中的索引写入 `model` 并触发 `onChange`。

- void Render(App app)
  - 绘制并分发弹窗（由 App.RunOverlays 在覆盖层阶段调用）：
    按构造模式分流——宿主控件的 OnPaintOverlay、富菜单、
    外观抽屉，或内置选项列表（样式取 `popup` / `popup.option`
    规则），并集中处理选择、外部按压关闭与 Escape。

- void RenderThemeDrawer(App app)
  - 绘制外观抽屉（参见 ThemeDrawer）并分发其
    点击。所有状态均从 App 读写，使抽屉本身
    在帧间保持无状态。

- static List<int> DrawerAccents()
  - 强调色色板的候选色（0 = 跟随外观默认值）。

- static List<int> DrawerOpLevels()
  - 整窗/壁纸不透明度的候选档位（百分比）。

- static List<string> DrawerKinds()
  - 动效标签页的背景特效选项名（第 0 项 “跟随皮肤” 映射 -1，
    其余按序为 BackdropFx 种类）。

- int DrawerContentH(App app, int tab)
  - 当前抽屉标签页的可滚动内容总高度。

- int DrawDensityRow(App app, int yy)
  - 密度档选项行（标签 + 大中小三枚 chip），复用透明度选项的
    chip 样式。返回下一节的 y。

- int DrawSkinGrid(App app, int yy)
  - 外观预设网格（实时预览卡片）。

- int DrawAccentRow(App app, int yy)
  - 强调色色板行。

- int DrawOpacityChips(App app, int yy)
  - 整窗不透明度选项。

- int DrawWallpaperSection(App app, int yy)
  - 自定义壁纸选择器 + 混合强度选项。

- void DrawMotionTab(App app, int yy)
  - 动效标签页：动画开关 + 背景特效单选列表。

- void HandleDrawerInput(App app)
  - 外观抽屉的点击 / 外部按压 / Escape 分发。

- int DrawerSection(App app, int dx, int yy, int dw, string label)
  - 居中显示、两侧带分隔线的抽屉分区标题
    （“---- Label ----”）。返回标题下方的 y。

- static int RichWidth(App app, List<MenuItem> items)
  - 富项目列表的面板宽度：最宽标签加上图标列和
    右侧留白（快捷键文本 / 子菜单箭头），并限制最小宽度。

- static int MenuRowH(App app)
  - 富菜单行高：比表单控件（heightMedium）紧凑——右键菜单
    条目多，一行 26 逻辑像素才能一屏放下。

- static int RichViewH(App app, List<MenuItem> items, int maxRows)
  - 富项目列表的可视高度：窗口装得下全部条目时整高显示
    （行数上限只是小窗口的兜底，不该在满屏窗口里制造滚动条）；
    内容高过窗口时取行数上限与窗口可用高的较小者——两种
    情况都出滚动条而不是把面板截出屏。定位与渲染共用同一
    口径，宿主传进来的 y 才不会按整高翻转到触发器上方。

- static int RichHeight(App app, List<MenuItem> items)
  - 富项目列表的面板高度（分隔线和标题比
    可点击行更矮）。

- static int RichRowTop(App app, List<MenuItem> items, int upto, int startY)
  - `upto` 处项目在面板内的 Y 偏移，按行类型计算。

- static void SetOccluders(int ax, int ay, int aw, int ah, int bx, int by, int bw, int bh)
  - 登记本帧绘制的遮挡矩形（宽 0 = 无）。每次 PaintRichPanel
    绘制前由 RenderRich 按面板 z 序设置，绘制后立即清零。

- static bool PointOccluded(int mx, int my)
  - 落点是否在本帧登记的遮挡矩形内——被画在更上层面板盖住的
    区域里，后面板的行不得再响应悬停（激活用的是同一批悬停
    结果，随之一起被挡住）。

- static int PaintRichPanel(App app, List<MenuItem> items, int px, int py, int pw, int ph, int idBase, int scrollY, int barW)
  - 在 (px,py) 处绘制一个富菜单面板（图标 / 分隔线 / 标题 / 子菜单
    箭头），并为每个可点击 / 子菜单行注册命中 id `idBase + rowIndex`。
    `ph` 是可视高度，行按 `scrollY` 上移并裁进面板（可滚动主面板
    用，子菜单面板传 0）。返回光标所在的行索引，没有则为 -1。
    `barW` 是面板右缘滚动条条带的宽度（无可滚动时为 0）：
    行悬停不含条带——条带归滚动条，悬停伸进去会让拖动滑块
    的指针扫出子菜单父行，子面板开合顶漂覆盖层 AllocId，
    滚动条 IsPressed 失配后拖动中断、恢复时瞬移。

- void RenderRich(App app)
  - 绘制并分发富菜单：主面板（可按 richMaxRows 出滚动条）加
    悬停展开的一层子菜单。叶子项在左键松开时把 `action` 写入
    `result` 并关闭；面板外按压、Escape 或窗口失焦也关闭。
    行悬停按几何解析，仅悬停行变化时请求重绘。


## ParseCursor (class)

指向行列表的可变索引，使递归的 ReadNode 调用推进
同一个共享游标（Zan 没有 ref/out 参数）。

- int pos;

- ParseCursor()


## Point (class)

整数二维点。

- int x;

- int y;

- Point(int x, int y)


## PropSpec (class)

为可视化设计器和序列化器描述 Control 的一个可编辑属性，
以及读写它的方式。控件从 Props() 返回其列表，
并把每个 spec 指向它编辑的字段：

PropSpec icon = PropSpec.Text("icon", "Icon");
icon.str = Icon;            // 编译器合成的访问器对
ps.Add(icon);

因为 spec 携带访问器对，`Control.GetProp/SetProp` 就能
泛化地读写每个属性——控件只声明一次属性，
而不必在三个字符串匹配方法里重复。

kind：0 文本，1 整数，2 布尔，3 枚举（见 `options`），4 颜色，5 分组标题。

- string key;

- string alias;
  - 同一属性在文档中应答的附加键（布尔标志的 "checked on"、
    "value" 等）；序列化器从不回写它们。

- string label;

- int kind;

- List<string> options;

- Binding<string> str;
  - 绑定的字段，按 `kind` 三者取其一。在这里给字段赋值
    即成为实时绑定，值会直接读写
    到控件；给已有 Binding 赋值则共享它。

- Binding<int> num;

- Binding<bool> flag;

- SignalString sstr;
  - 针对值具有响应性的控件，用 signal 而非字段：
    写入经由 Set 走，订阅者仍能收到变更事件。

- SignalInt snum;

- SignalBool sflag;

- bool syncName;
  - 写入该属性同时重命名节点时为 true，使设计器
    树跟随标识该控件的文本。

- string tip;
  - 属性的说明文字：在属性面板中悬停该行时以气泡提示展示，
    解释这个属性的作用。为空则不显示提示。

- int step;
  - 整数属性(kind==1)的步进配置：`step` 为 +/- 按钮每次增减量，
    `lo`/`hi` 为取值范围。`hasRange` 为 true 时才做范围钳制。

- int lo;

- int hi;

- bool hasRange;

- PropSpec(string k, string lbl, int kd)

- bool IsBound()
  - spec 一旦指向字段或 signal 即为 true，这正是
    基类无需控件协助就能服务该属性的原因。

- bool Answers(string k)
  - 当 `key` 命名该属性（自身键或某个别名）时为 true。

- PropSpec AsName()
  - 将此属性标记为同时命名节点的属性。

- PropSpec WithTip(string t)
  - 给属性挂一段说明（返回 this，便于链式调用）。属性面板
    悬停该行时以气泡提示展示。

- PropSpec Step(int s, int min, int max)
  - 配置整数属性的 +/- 步进与范围（返回 this，便于链式调用）。
    `s` 为每次步进量，`min`/`max` 为钳制范围。

- PropSpec StepBy(int s)
  - 只配置步进量、不做范围钳制。

- int Clamp(int v)
  - 把 `v` 钳制到已配置范围内（未配置范围时原样返回）。

- PropSpec Also(string k)
  - 在文档中也应答 `k`（返回 this，便于链式调用）。

- string Read()
  - 属性值的字符串形式，即设计器与文档格式交换所用的形式
    （标志为 `"true"`/`"false"`，数字为十进制）。

- void Write(string val)
  - 按 `val` 字符串写回绑定：数字/布尔做解析（IsOn/ToInt32），
    文本原样写入；未绑定任何字段/signal 时为空操作。
    枚举属性（kind 3）还收选项文本：`SetProp("orient",
    "vertical")` 写入的是该选项的下标。只认数字序号的话，
    strtoll 对非数字串静默返回 0，"vertical" 会无声落回第一项。

- static string Flag(bool on)
  - 布尔的文档字符串形式（"true"/"false"）。

- static bool IsOn(string val)
  - 文档字符串是否表示开启（"true" 或 "1"）。

- static PropSpec Text(string k, string lbl)
  - 工厂：文本属性（kind 0）。

- static PropSpec Int(string k, string lbl)
  - 工厂：整数属性（kind 1）。

- static PropSpec Bool(string k, string lbl)
  - 工厂：布尔属性（kind 2）。

- static PropSpec Color(string k, string lbl)
  - 工厂：颜色属性（kind 4）。

- static PropSpec Section(string lbl)
  - 枚举属性，值为 `opts` 之一（以其标签文本存储）。
    分组标题行（只有标题文字，没有值也没有编辑器）。

- static PropSpec Enum(string k, string lbl, List<string> opts)
  - 枚举属性工厂，值为 `opts` 之一（以其标签文本存储）。

- PropSpec Option(string o)
  - 追加一个枚举选项（返回 this，便于链式调用）。


## QrEncoder (class)

纯 Zan 的 QR Code（模型 1-40）编码器，ISO/IEC 18004：

- 输入按 Unicode 码点分成 Numeric / Alphanumeric / Byte(UTF-8) 游程
混合编码（中文等多字节字符原样按 UTF-8 字节进 Byte 段，与系统
码页无关）；短游程（<=8 字符）折回 Byte，省模式切换开销。
- 自动选最小版本；L/M/Q/H 四级纠错（GF(256) Reed-Solomon，分块交织）。
- 八个掩码全试、按标准罚分四条选优；格式信息 BCH(15,5)、
v>=7 版本信息 BCH(18,6)。
- 超容量抛 Exception（与 stdlib 异常约定一致）。

`Encode(text, ecl)` 返回 `QrMatrix`。渲染/导出在 Gui.Widget.QrCode。

- static int[]EC_PER_BLOCK_L=new int[]{ -1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30};

- static int[]EC_PER_BLOCK_M=new int[]{ -1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28};

- static int[]EC_PER_BLOCK_Q=new int[]{ -1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 37, 34, 28, 30, 31, 24, 37, 32, 29, 37, 34, 31};

- static int[]EC_PER_BLOCK_H=new int[]{ -1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30};

- static int[]NUM_BLOCKS_L=new int[]{ -1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25};

- static int[]NUM_BLOCKS_M=new int[]{ -1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49};

- static int[]NUM_BLOCKS_Q=new int[]{ -1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68};

- static int[]NUM_BLOCKS_H=new int[]{ -1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81};

- static int EcPerBlock(QrEcl ecl, int ver)
  - 该版本/级别每块纠错码字数（ISO 18004 表）。

- static int NumBlocks(QrEcl ecl, int ver)
  - 该版本/级别的纠错分块数。

- static int MODE_NUMERIC=1;

- static int MODE_ALNUM=2;

- static int MODE_BYTE=4;

- static string ALNUM_CHARS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:";

- static int[]AlignPattern(int ver)
  - 校正图形的坐标轴序列（ISO/IEC 18004 Table E.1，v=1 返回空）。

- static int[]BlockPlan(int ver, QrEcl ecl)
  - 按版本/级别给出完整序列 [numBlocksG1, dataG1, numBlocksG2, dataG2]。
    从官方 (总码字 - 纠错码字) 反推数据位。

- static int TotalCodewords(int ver)
  - 总码字数 = floor(rawDataModules/8)。

- static int[]gfExp=null;

- static int[]gfLog=null;

- static void EnsureGf()
  - 首次调用时构建 GF(256) 的指数/对数表（本原多项式 0x11D）。

- static int GfMul(int a, int b)
  - GF(256) 乘法（任一操作数为 0 时结果为 0）。

- static int[]RsGenerator(int deg)
  - RS 生成多项式（Nayuki 式）：prod (x - a^i)，i = 0..deg-1。
    返回长度 deg 的数组，result[deg-1] = 1（最高次系数），升幂索引，
    最高次 x^deg 的系数隐式为 1。

- static int[]RsRemainder(int[]data, int dataLen, int[]gen)
  - data 对生成多项式 gen 取模（Nayuki 式），返回 deg 个纠错码字。

- class Segment
  - 一个编码分段：mode 为指示符值，chars 是字符数（numeric/alnum 为
    字符数，byte 为字节数），bits 是该段的数据位（不含模式/计数头）。

- public static QrMatrix Encode(string text, QrEcl ecl)
  - 按级别编码文本，返回不含静区的模块矩阵。

- public static QrEcl ParseEcl(string s)
  - 级别名 -> 枚举（大小写均可）；未知返回 M（与 layui 默认一致）。

- static bool IsNumeric(int b)
  - 字节是否为 ASCII 数字 0-9。

- static int AlnumValue(string ch)
  - 字符在字母数字表中的值（0-44），不在表内时 -1。

- static int SeqByteLen(int lead)
  - 以 lead 为首字节的 UTF-8 码点字节长度（1-4）。

- static List <QrEncoder.Segment> MakeSegments(string text)
  - 按码点游程切段：数字 / 字母数字 / 字节（UTF-8 原样），再把短的非
    Byte 游程折回 Byte（模式切换头 4+cc 位往往比直接写进 UTF-8 更贵）。

- static QrEncoder.Segment MakeByteRun(string run)
  - 把一段文本编码为 Byte 段（每字节 8 位，高位在前）。

- static int ModeOfByte(int b, string text, int pos)
  - 字节 b（UTF-8 首字节）+ 文本上下文 -> 该码点的模式。

- static int CharCountBits(int mode, int ver)
  - 模式指示符后的字符计数字段宽度（按版本 1-9/10-26/27-40 分三档）。

- static int DataCapacity(int ver, QrEcl ecl)
  - 该版本/级别的数据码字容量（总码字减去全部纠错码字）。

- static int PickVersion(List <QrEncoder.Segment> segs, QrEcl ecl)
  - 能容纳这些分段的最小版本，1..40；放不下返回 -1。

- static int WriteSegments(List <QrEncoder.Segment> segs, int ver, QrEcl ecl, int[]cw)
  - 分段位流 + 终止符 + 填充写入 cw（容量码字），返回实际数据码字数。

- static void AppendVal(List<int> bits, int val, int n)
  - 把 val 的低 n 位按高位在前追加进位流。

- static void SetFn(bool[]fn, int size, int x, int y)
  - 标记 (x,y) 为功能模块（不可掩码、不放数据），越界忽略。

- static void SetDark(bool[]dark, bool[]fn, int size, int x, int y)
  - 标记功能模块并置为深色，越界忽略。

- static void DrawFinder(bool[]dark, bool[]fn, int size, int cx, int cy)
  - 定位图形 + 分隔：以 (cx,cy) 为中心的 7x7 环，越界部分丢弃
    （Nayuki 的 dist!=2 && dist!=4 画法）。

- static void DrawAlign(bool[]dark, bool[]fn, int size, int cx, int cy)
  - 校正图形：以 (cx,cy) 为中心的 5x5 图案（同心环），越界部分丢弃。

- static int BchVersion(int ver)
  - 版本信息 18 位：版本号左移 12 位，低位接 BCH(18,6) 纠错位。

- static QrMatrix BuildMatrix(int ver, QrEcl ecl, int[]cw, int nDataCw)
  - 组装最终矩阵：画功能图形与版本/格式信息区，按 ISO 分块做
    RS 纠错并交织，蛇形放入数据模块，再对八个掩码逐一应用、
    按罚分选优。

- static bool[]ApplyMask(bool[]dark, bool[]fn, int size, int mask, QrEcl ecl)
  - 掩码 + 格式信息写入，返回成品矩阵（new 数组，深拷贝）。

- static bool MaskBit(int m, int x, int y)
  - 掩码 m 在 (x,y) 处是否翻转（ISO 18004 的八种掩码条件）。

- static int Penalty(bool[]m, int size)
  - 掩码罚分总值（ISO 18004 四条规则：同色游程、2x2 同色块、
    类定位图形 1011101、深色比例偏离 50%）。

- static int RunPenaltyLine(bool[]m, int size, int line, bool horizontal)
  - 单行/列的同色游程罚分（游程 ≥5 时加 3+(长度-5)）。

- static bool Pattern11(bool[]m, int size, int x, int y, bool horizontal)
  - 11 格窗口 == 0000 1011101（从 (x,y) 沿 horizontal 方向）。


## QrMatrix (class)

二维码编码结果：version/size/ecl + 边长 size 的模块矩阵（true = 深色，
不含静区）。`Get(x,y)` 按行主序读模块。

- public int version;

- public int size;

- public QrEcl ecl;

- public bool[]modules;

- public bool Get(int x, int y)
  - (x,y) 处模块是否深色（行主序，不含静区）。


## Rect (class)

整数矩形（x/y 为左上角，width/height 非负）。

- int x;

- int y;

- int width;

- int height;

- Rect(int x, int y, int w, int h)

- int Right()
  - 右边界（x+width，不含）。

- int Bottom()
  - 下边界（y+height，不含）。

- bool Contains(int px, int py)
  - 点是否在矩形内（左上含、右下不含）。

- bool Intersects(int ox, int oy, int ow, int oh)
  - 与另一矩形（左上角 + 尺寸）是否有正面积交集（贴边不算）。

- static Rect Inflate(int rx, int ry, int rw, int rh, int amount)
  - 四周向外扩大 amount 像素的新矩形。


## RenderBackend (class)

画布背后的光栅器。`Cpu` 是永久保留的兜底实现，`Gpu` 是
运行时自带的 OpenGL 3.3 后端（不引入任何第三方运行时），`Auto`
表示这台机器能给出 GL 上下文就用 GPU、否则用 CPU。

这是每个应用自己的选择（不是环境变量：那会让一台机器上所有 Zan
程序共用一份配置），应用可以把它接到自己的设置项上。

- static int Cpu()

- static int Gpu()

- static int Auto()


## Selector (class)

一个已解析的选择器：把 `button.ghost.primary::icon:hover` 拆成类型名、
其类链、可选的 id、可选的 `::part` 和可选的
`:state`。这就是引擎建模的全部选择器语法——足以用 CSS 描述
组件的完整外观（其部件和状态），而且
足够小，匹配保持为一次表扫描。

- string type;

- string classes;

- string id;

- string part;

- string state;
  - 以空格分隔的伪类名（`:hover:selected` -> "hover selected"），
    无状态时为 ""。多个伪类是与关系，因此“选中且悬停”
    这类组合外观能写在 CSS 里，而不必回到代码里分支。

- string clsContains;
  - `[class*="frag"]` 里的 frag：class 属性原文的子串匹配，
    用于 `custom-{hex}` 这类复合 class 片段（无该条件时为 ""）。

- static Selector Parse(string sel)
  - 解析一个选择器；遇到本引擎不建模的形式（后代/子组合器、
    `class*` 之外的属性选择器、`:root`）时返回 null，
    这类选择器永远不会匹配。

- int Specificity()
  - 此选择器在级联中的权重。伪状态高于
    其他一切，因此无论作者写在哪里，`:hover` 都叠加在基础外观之上；
    其下按 CSS 顺序：type <
    class < 类链 < id。

- static string ClassContains(string attr)
  - `class*="frag"`（允许内部空白，双引号或单引号）→ frag；
    其余属性写法不是子串匹配，返回 null（选择器不建模）。

- static bool NameChar(string ch)
  - 可作为类型/类/id/部件名称字符时为 true。


## Serialize (class)

在 Control 树与紧凑文本文档之间往返，保留
父子关系（前序加显式子节点数）以及每个
节点的几何和控件特有属性（经 GetProp/SetProp）。

每行一个节点，制表符分隔：
kind name dock padL padT padR padB gap mx my prefW prefH nChildren nProps
[propKey propVal]* nEvents [evtName handlerId]* bindPath bindProp class
值会转义，制表符/换行/反斜杠得以保留；子节点
紧跟在父节点之后按前序排列。

- static string Esc(string s)
  - 转义值文本中的反斜杠/制表符/换行（序列化行格式用）。

- static string Unesc(string s)
  - <c>Esc</c> 的逆操作。

- static void WriteNode(Control c, List<string> lines)
  - 前序遍历控件树，每节点输出一行追加到 lines。

- static string Save(Control root)
  - 控件树 → 紧凑文本文档（配对 Save/Load 往返无损）。

- static List<string> SplitLines(string s)
  - 按换行切分（保留末尾空行语义）。

- static List<string> SplitFields(string line)
  - 按制表符切分一行字段。

- static Control ReadNode(List<string> lines, ParseCursor cur)
  - 从 lines[cur.pos] 读一行并还原为控件：解析字段、属性、
    事件绑定，再递归读入紧随其后的 childCount 行子节点。
    遇到未注册的控件 kind 时读掉并丢弃其整棵子树的行，
    返回 null（子树仍被消费，文档不错位）。

- static Control Load(string text)
  - 解析 Save 产出的文本文档，还原并返回根控件；未知控件
    子树被跳过后可能返回 null。


## SignalBool (class)

布尔版内部状态缓冲：可变值 + 单调递增版本号，
渲染帧轮询 Version() 检测变化（契约同 SignalInt）。

- bool val;

- int version;

- SignalBool(bool initial)

- bool Get()
  - 当前值。

- void Set(bool v)
  - 写入。版本号无条件 +1，轮询方一律以版本号变化为准。

- void Toggle()
  - 取反写入。版本号无条件 +1。

- int Version()
  - 写入次数，用于帧轮询检测变化。


## SignalInt (class)

控件内部状态缓冲（immediate-mode 专用，非对外绑定协议）。

语义：可变值 + 单调递增版本号。渲染帧轮询 `Version()`（或直接
比对值）即可检测变化——Gui 的变更路径是帧轮询，不是事件订阅。

对外数据绑定统一走 `System/Binding.zan` 的 `Binding<T>`
（`control.data = model.field;` 编译器降级为实时存取器对）。
通道契约见 docs/STDLIB_COMPONENT_STANDARDS.md §6。

- int val;

- int version;

- SignalInt(int initial)

- int Get()
  - 当前值。

- void Set(int v)
  - 写入。版本号无条件 +1，轮询方一律以版本号变化为准。

- int Version()
  - 写入次数，用于帧轮询检测变化。


## SignalString (class)

字符串版内部状态缓冲：可变值 + 单调递增版本号，
渲染帧轮询 Version() 检测变化（契约同 SignalInt）。

- string val;

- int version;

- SignalString(string initial)

- string Get()
  - 当前值。

- void Set(string v)
  - 写入。版本号无条件 +1，轮询方一律以版本号变化为准。

- int Version()
  - 写入次数，用于帧轮询检测变化。


## Size (class)

整数二维尺寸。

- int width;

- int height;

- Size(int w, int h)


## Skin (class)

皮肤包：一个目录，含 `skin.css`（`:root` 里的语义令牌加上
每控件规则）及其美术资源。皮肤是数据而非代码——用户可以在
应用旁放一个文件夹并在运行时选用：

stdlib/Gui/skins/fortune/skin.css
stdlib/Gui/skins/fortune/banner.png

Skin s = Skin.Load("fortune");
s.Apply(app);            // 主题令牌 + 样式表 + 背景美术

`:root` 自定义属性供给语义 Theme（因此任何未被
CSS 样式化的东西仍得到皮肤的调色板），其余每条规则供给控件绘制所用的
样式解析器（Style/StyleBox）。两半都可选：
只有 `:root` 的皮肤就是换调色板，只有规则的皮肤在当前主题之上
重设控件样式。

- string name;

- string dir;

- StyleSheet sheet;

- Theme theme;

- bool dark;

- string art;
  - 背景插画（绝对或相对应用路径，皮肤不带则为 ""）
    及其叠加在壁纸上的强度（百分比）。

- int artOpacity;

- bool loaded;

- static List<string> cacheNames;

- static List<Skin> cacheSkins;

- Skin(string skinName)

- static Skin Load(string name)
  - 加载（并记忆）名为 `name` 的皮肤，在皮肤根目录中查找。
    找不到时返回带空样式表的皮肤，因此缺失的
    皮肤会退化为当前主题而不是失败。

- static Skin Reload(string name)
  - 从磁盘重新读取皮肤（供皮肤热重载路径使用，使 CSS
    编辑无需重启应用即可生效）。

- bool IsLoaded()
  - 在磁盘上找到该包时为 true。

- string ArtPath()
  - 该包自己的背景插画路径（不带时为 ""）。

- Theme NewTheme()
  - 由该包 `:root` 令牌构建的新 Theme；若包
    只有规则则为 null。调用方拥有结果并可修改它。

- void Apply(App app)
  - 把皮肤安装到 `app`：`:root` 的 Theme（回退到
    当前主题）、每个控件都要解析的样式表，以及
    背景美术。只有用户未自选壁纸时，包的美术才填充背景——
    用户壁纸永远优先，因此
    切换皮肤永远不会拿包背景换掉用户自选的壁纸。

- static List<string> Roots()
  - 搜索皮肤包的根，最具体者优先：`$ZAN_GUI_SKINS`、
    应用自己的 `skins/`，然后是 stdlib 副本（从构建树运行时）。

- static string ExeDir()
  - 正在运行的可执行文件所在目录（不含末尾分隔符），无法确定时返回 ""。
    便于按 exe 目录定位资源，
    而非当前工作目录。

- static string FindDir(string name)
  - 皮肤 `name` 所在目录，没有任何根目录持有该皮肤时返回 ""。

- static List<string> Available()
  - 磁盘上所有可发现的皮肤包（包含 skin.css 的目录）。

- static string EmbedSkinName(string line)
  - "skins/dark/skin.css" -> "dark"；无包文件夹的名称返回 ""
    （例如顶层 "skins/base.css"）。

- static string KindOf(string name)
  - 皮肤包的类别：`--kind` 令牌，缺省 "ui"（整套 UI 皮肤）。
    组件皮肤——如 SkinBuilder 产出的 Chart 皮肤声明
    `--kind: "chart"`——只贡献单个组件的配色，不是整套 UI
    皮肤，因此不进标题栏的皮肤选择列表；按名 UseSkin 仍可用。

- static List<string> Names()
  - 整套 UI 皮肤，按选择器顺序：`--order` 在前（内置包自编号
    0..n），未声明顺序的包随后按字母序。组件皮肤（`--kind`
    非 "ui"，如图表配色）不在此列——皮肤选择器选的是整个
    界面外观，不该混进单组件的配色方案。这是应用、标题栏
    选择器和持久化设置共同引用的唯一一份皮肤列表。

- static int OrderOf(string name)
  - 来自 `--order` 的排序键（未声明的包排在内置包之后）。

- static string LabelOf(string name)
  - 显示名取自 `--name`，未设置时回退到文件夹名。

- static List<string> Labels(List<string> names)
  - `names` 对应的显示名列表，保持相同顺序。

- static string FindArt(string dir)
  - 皮肤的插图：`--art` 指定的文件，否则用包内约定的
    横幅文件。

- static Theme ThemeOf(StyleSheet sheet)
  - 从皮肤的 `:root` 自定义属性构建其 Theme。`--base`
    选择起始预设（"dark"、"light" 或预设名/索引），
    其余每个 `--token` 覆盖 Theme 的一个字段；CSS 拼写同样
    被接受，所以 `--bg-primary` 设置 `bgPrimary`。皮肤未声明任何
    token 时返回 null（沿用应用当前主题）。

- static Theme BaseOf(StyleSheet sheet)
  - 皮肤起步的 token 基线（`--base: light | dark`），默认
    为 dark。只有这两种：其余皮肤都是
    在它们之上覆写的 CSS 包。

- static int DensityOf(StyleSheet sheet)
  - 皮肤是否需要深色窗口边框（`--dark: 1`，否则
    从 `--base` 推断）。
    皮肤声明的密度档（`--density: small|medium|large`），
    未声明时返回 -1（App 保持用户当前选择）。

- static bool DarkOf(StyleSheet sheet)
  - 皮肤是否需要深色窗口边框（`--dark: 1`，否则
    从 `--base` 推断）。

- static string TokenName(string key)
  - `--bg-primary` / `--bgPrimary` / `bg-primary` 统一映射为 `bgPrimary`。

- static string Unquote(string v)
  - 去掉 CSS 字符串值两端的引号（`--name: "Liquid Glass"`）。

- static string ReadIfExists(string path)
  - 读取文本文件，文件不存在时返回 ""。

- static string BaseCss()
  - 内置组件基线 `base.css`，与皮肤包使用同样的搜索根。
    它作为基础层垫在应用每个 sheet 之下，注入当前主题的 token，
    使控件的默认外观由数据（CSS）决定，
    而非硬编码在 Style.zan。没有根目录持有它时返回 ""。

- static string Leaf(string path)
  - 路径的末级名称（最后一个 / 或 \ 之后）。

- static bool Contains(List<string> list, string v)
  - 列表中是否已含该字符串。

- static extern string getenv(string name);

- static string Env(string name)
  - getenv 的包装：null 转为 ""。

- static extern string zan_embed_read(string name);

- static extern int zan_embed_has(string name);

- static extern string zan_embed_list(string prefix);

- static string EmbedRead(string name)
  - 内置于 exe 的文本资源，缺失（或未嵌入任何资源）时返回 ""。

- static bool EmbedHas(string name)
  - 内置资源是否存在。

- static string EmbedList(string prefix)
  - `prefix` 下以 '\n' 连接的内置资源名列表。


## Stack (class)

立即模式组合用的线性布局游标。

Stack 包装一个内容矩形和一个主轴方向（row/column）。
调用方通过 Slot()/Fill()/Space() 依次从中切出子矩形，
控件无需再手算 x/y/w/h。每次分配都会推进
内部游标，并遵守配置的 gap 与 padding。

由于框架是立即模式，Stack 是每帧的轻量值：
创建、自上而下（或从左到右）摆放子项、丢弃。

示例（带内边距的工具栏行：固定按钮 + 弹性搜索框）：
Stack bar = Stack.Row(x, y, w, h);
bar.SetPad(8);
bar.SetGap(8);
Rect btn = bar.Slot(96);
Rect search = bar.Fill();

- int ox;
  - 游标在内部移动的内容框（已按 padding 内缩）。

- int oy;

- int ow;

- int oh;

- int dir;
  - 主轴：0 = row（水平），1 = column（垂直）。

- int gap;

- int cursor;
  - 游标沿主轴相对内容框的偏移。

- int placed;
  - 已摆放的子项数（决定 gap 的插入）。

- static Stack Of(int x, int y, int w, int h, int direction, int gap)
  - 指定矩形、主轴方向（0=row，1=column）与 gap 的栈。

- static Stack Column(int x, int y, int w, int h)
  - 自上而下（垂直）铺满给定矩形的栈。

- static Stack Row(int x, int y, int w, int h)
  - 从左到右（水平）铺满给定矩形的栈。

- static Stack ColumnIn(Rect r)
  - 在已有 Rect 内布局的垂直栈。

- static Stack RowIn(Rect r)
  - 在已有 Rect 内布局的水平栈。

- Stack SetGap(int g)
  - 设置相邻子项之间插入的间隙。返回 this 以便
    可作独立语句使用（而不是在其他调用之前链式调用）。

- Stack SetPad(int p)
  - 四边统一内缩内容框。须在摆放子项之前调用；
    它会缩小可摆放区域，Slot/Fill/Remaining 都会遵守。

- Stack SetPadding(int top, int right, int bottom, int left)
  - 按各边分别内缩内容框（上、右、下、左）。

- int MainSize()
  - 主轴长度（row 为宽度，column 为高度）。

- int CrossSize()
  - 交叉轴长度（row 为高度，column 为宽度）。

- int Remaining()
  - 沿主轴在已摆放内容之后剩余的空间。

- bool HasRoom(int mainSize)
  - 给定主轴尺寸的子项（非首个子项时加上前导 gap）
    仍能放进剩余空间时返回 true。

- void Space(int mainSize)
  - 只推进游标而不产生子矩形（用作间隔）。

- Rect Slot(int mainSize)
  - 切出下一个给定主轴尺寸的子矩形。交叉轴
    拉伸到内容区全幅，并推进游标。

- Rect Fill()
  - 切出一个占满主轴剩余空间的子项（弹性
    填充）。适合作为栈的最后一个子项。

- Rect SlotFraction(int permille)
  - 按原始主轴长度的比例（千分比，0..1000）切出子项——
    适合 300/700 侧边栏这类按比例分栏。

- Rect SlotFractionClamped(int permille, int minSize, int maxSize)
  - 保持可用的比例槽：原始主轴长度的比例，
    限制在 `minSize`/`maxSize`（0 = 不限）以及
    剩余空间之内，因此面板在窄窗口下不会塌缩，
    在宽窗口下也不会超过可读宽度。

- List<Rect> SlotsGrown(List<int> naturalSizes)
  - 按每个自然尺寸切出一个子项，剩余的主轴空间
    在它们之间均分（自然尺寸放不下时按比例收缩）——
    一排按钮想要的 flex 行，调用方无需
    再手动分配宽度。


## Style (class)

样式解析器：把（控件类型、类、状态）解析为一个
StyleBox——依次叠加当前主题的默认值、当前皮肤的
样式表以及控件自身的 inline 样式，并在状态之间
交叉淡入淡出，从而支持 `transition`。

这正是控件无需携带各皮肤绘制代码即可换肤的关键。
控件的整个视觉层变成：

int st = Style.StateOf(app, id, disabled);
StyleBox s = Style.Eased(app, id, "button", "primary", disabled);
s.Paint(app, x, y, w, h);
s.DrawLabel(app, x, y, w, h, label);

选择器遵循 CSS：`button`、`.primary`、`button.primary`、`#save` 以及
它们的 `:hover / :active / :focus / :disabled / :checked / :selected` 状态
变体，按特异性升序解析（type、class、type.class、id）。
主题 token 提供默认值，皮肤只需声明差异，
没有 skin.css 的应用外观与内置主题完全一致。

- static int SNormal()
  - 常态（0，无任何状态位）。

- static int SHover()
  - 悬停位（1）。

- static int SActive()
  - 按下位（2）；StateOf 只在悬停中按下才置位。

- static int SFocus()
  - 焦点位（4）。

- static int SDisabled()
  - 禁用位（8）；StateOf 置位它时屏蔽其余交互状态。

- static int SSelected()
  - 选中位（16）；锁定状态，先于 hover/press 淡入淡出叠加。

- static int SChecked()
  - 勾选位（32）；与 SSelected 相同的锁定语义。

- static int AnimNone()
  - 无动画（0）。

- static int AnimSpin()
  - `spin`：持续旋转（StyleBox.SpinDeg 消费）。

- static int AnimPulse()
  - `pulse`：盒内呼吸填充（StyleBox.PaintAnim 消费）。

- static int AnimBreath()
  - `breath`：卡片呼吸光泽（Fx.CardBreath）。

- static int AnimShimmer()
  - `shimmer`：扫过的斜向高光（Fx.CardSheen）。

- static int AnimFloat()
  - `float`：上下浮动偏移（StyleBox.FloatOffset 消费）。

- static int AnimGlow()
  - `glow`：边框辉光（Fx.BorderGlow）。

- static int AnimAurora()
  - `aurora`：极光渐变（Fx.CardAurora）。

- static int AnimMotes()
  - `motes`：漂浮微粒（Fx.CardMotes）。

- static int AnimKind(string name)
  - 把 CSS 动画名映射为 Anim* 种类（未知返回 0）。

- static string StateName(int bit)
  - 某个状态位对应的 CSS 伪类名（基础状态返回 ""）。

- static int StateBit(string name)
  - CSS 伪类名对应的状态位（不代表任何状态时返回 0）。

- static int StateOf(App app, int id, bool disabled)
  - 控件 `id` 的实时交互状态，以状态位掩码表示。

- static Dict <string, StyleBox> cache;

- static int cacheGen;

- static int statResolve;

- static int statHit;

- static void CacheReset(int gen)
  - 重建解析缓存并记下主题代次 `gen`；旧代次的全部键作废。

- static int StatPeek(int idx)
  - 读解析计数但不清零，供按帧算差值（0 = 解析次数，1 = 命中次数）。

- static int StatRead(int idx)
  - 取走并清零解析计数（0 = 解析次数，1 = 缓存命中次数）。

- static StyleBox CacheGet(App app, string key)
  - 查解析缓存（每次调用计入解析统计，命中计入命中统计）；
    缓存为空或主题代次不符时重建并返回 null（未命中）。

- static void CachePut(string key, StyleBox box)
  - 把解析结果放入缓存；同键已存在时保留先到的。

- static StyleBox Of(App app, string type, string cls, int state)
  - 解析 `type`.`cls` 在 `state` 下的样式（主题默认值 + 皮肤）。

- static StyleBox Full(App app, string type, string cls, string id, int state)
  - 包含 id 选择器（`#name`）的解析，即特异性最高的一层。

- static StyleBox Part(App app, string type, string part, string fallbackType, string cls, string id, int state)
  - 解析 `type::part` 部件样式（`menu::item` 一类）：fallbackType
    非空时先按它走整套主题默认值与皮肤规则，再叠加 base 与应用
    sheet 的 `type::part` 选择器，最后应用 Shell 与度量缩放。
    结果同样按键缓存并返回克隆。

- static void ScaleLayout(App app, StyleBox b, StyleBox themed)
  - 把样式表的长度（box 尺寸、外边距、字号、圆角半径）
    缩放到显示设备：CSS 按 100% 编写，而主题自身的
    度量已按 DPI 缩放，因此 sheet 的 `width: 260px` 必须
    按相同系数缩放才能保持相同的物理尺寸。百分比
    无需缩放。
    
    `themed` 是主题默认值处理后的 box：若某长度仍等于
    其主题值，说明它已带有显示缩放系数，不能再乘
    第二次（否则 150% 显示下每个按钮、输入框和 chip 都会被放大
    到 1.5 倍）。

- static void ApplySheet(StyleSheet sheet, StyleBox b, string type, string cls, string id, int state)
  - 把 sheet 中选中该控件的每条规则叠加到 `b` 上，
    按从弱到强的顺序（参见 StyleSheet.ApplyMatch）。
    
    别名类型先应用：浮动按钮就是一颗圆按钮，它要吃到整套
    `button` 规则（角色、变体、状态），但皮肤仍能用
    `floatbutton` 只改它自己——因此是别名在前、本名在后，
    而不是把上百条按钮规则在 CSS 里复制一遍。

- static string SheetAlias(string type)
  - 该控件族借用哪个类型的 CSS 规则（"" = 不借）。

- static void ApplyPartSheet(StyleSheet sheet, StyleBox b, string type, string part, string cls, string id, int state)
  - 控件某个 `type::part` 的同样处理（`menu::item`、`card::title`）。

- static List<string> Classes(string cls)
  - 拆分以空格分隔的类列表（"primary ghost" -> [primary, ghost]）。

- static bool Has(string cls, string name)
  - `cls` 包含给定类 token 时返回 true。

- static StyleBox Eased(App app, int id, string type, string cls, bool disabled)
  - 解析控件样式，并在基础、悬停和按下三种外观之间
    用缓动后的交互程度做交叉淡入淡出——取代
    所有控件手写的 hover/press 颜色插值。
    获得焦点的控件会在最上层叠加其 `:focus` 规则（同样缓动），
    禁用控件则直接采用 `:disabled` 外观。

- static StyleBox EasedId(App app, int id, string type, string cls, string name, bool disabled, bool selected)
  - 带 id 选择器以及显式 selected/checked 标志的缓动解析
    （标签页、列表行、开关：选中是锁定状态而非
    交互，所以在 hover/press 淡入淡出之前叠加）。

- static StyleBox EasedIdIn(App app, int id, string type, string cls, string name, bool disabled, bool selected, int x, int y, int w, int h)
  - EasedId 的按矩形版本：悬停/按下/焦点的缓动程度按
    (x, y, w, h) 矩形测量（Ui.*LevelMsIn），用于命中区域
    与绘制矩形不一致的控件。

- static StyleBox EasedStateId(App app, int id, string type, string cls, string name, bool disabled, int latched)
  - 缓动解析的核心：禁用时直接返回 `:disabled`（+latched）外观；
    否则以常态为基础，按 hover/press/focus 的缓动程度分别叠加
    对应状态外观并混合，过渡时长取常态样式的 `transition`。
    latched 是选中/勾选一类锁定状态位，先于交互状态叠加；
    返回的 box 带上 fxId 供高光跟踪悬停。

- static StyleBox EasedStateIdIn(App app, int id, string type, string cls, string name, bool disabled, int latched, int x, int y, int w, int h)
  - EasedStateId 的按矩形版本（交互程度按 (x, y, w, h) 测量）。

- static StyleBox EasedPartId(App app, int id, string type, string part, string fallbackType, string cls, string name, bool disabled, bool selected)
  - 部件版 EasedId：解析 `type::part`（fallbackType 提供回退规则）
    的三态缓动样式，selected 为锁定选中位。

- static StyleBox EasedPartIdIn(App app, int id, string type, string part, string fallbackType, string cls, string name, bool disabled, bool selected, int x, int y, int w, int h)
  - 部件版 EasedIdIn。

- static StyleBox EasedPartStateId(App app, int id, string type, string part, string fallbackType, string cls, string name, bool disabled, int latched)
  - 部件版 EasedStateId：`type::part` 的禁用直返与三态交叉淡入淡出。

- static StyleBox EasedPartStateIdIn(App app, int id, string type, string part, string fallbackType, string cls, string name, bool disabled, int latched, int x, int y, int w, int h)
  - 部件版 EasedStateIdIn。

- static int Curve(int easing, int p)
  - 对线性的 0..1000 进度应用 CSS 缓动函数。

- static int RoleColor(Theme t, string cls, int state)
  - 角色类（primary/info/success/warning/error）在某状态下的强调色，
    无角色类时为 0。按钮/tab 的上色已经全在 skins/base.css 里，这里
    留给自绘标记的控件（时间轴的圆点等）按角色取一个主题色。

- static int RoleBase(Theme t, string cls)
  - 角色的静态强调色（不受状态影响）。

- static void Defaults(App app, StyleBox b, string type, string cls, int state)
  - 用当前主题对某控件族的默认值填充 `b`，这样皮肤的
    CSS 只需声明想要改变的部分，而完全没有 CSS 的
    主题应用外观与内置主题分毫不差。

- static void Shell(App app, StyleBox b, string type, string cls, int state)
  - 静态 CSS 规则无法表达的运行时处理，在
    sheet 之后应用：玻璃磨砂，以及新粗野主义的偏移阴影外壳
    （均受主题标志/状态控制）。禁用态的弱化文字不在这里——
    它是默认层（Style.Defaults）的事，否则皮肤写的
    `button:disabled { color: ... }` 会被这里抹掉。

- static Dict <int, StyleSheet> baseSheets;

- static int baseSheetGen;

- static StyleSheet BaseSheet(App app)
  - 内置基线样式表（skins/base.css，主题 token 以 :root 注入），
    每次解析都垫在应用自身 sheet 之下。按主题代次 + 度量缩放
    缓存；base.css 为空（未打包皮肤资源）时返回空表。

- static string RootFromTheme(Theme t)
  - 当前主题的调色板输出为 `:root` 块，使 base.css 的 var(--token)
    规则解析到当前（可能被皮肤覆写的）颜色。值以
    纯十进制输出——正是 ParseColor 存储的格式——使 CSS
    路径与旧代码路径的颜色逐位一致。

- static string VariantTokens(string name, int tint, int surface)
  - 一个角色的 ghost / secondary 变体色。CSS 没有混色函数，而
    这些混色只随主题变化，所以在导出 token 时算一次：
    ghost 用角色色的低透明度作悬停/按下底色，secondary 是
    角色色与页面底色的浅混。皮肤可以逐个 token 改写。

- static string Tok(string name, int v)
  - 颜色 token 行 `--name: #AARRGGBB`（值经 Hex8 输出，可被
    StyleSheet.HexToInt 原样往返）。

- static string TokN(string name, int v)
  - 数值 token（长度/强度/开关），以十进制输出。

- static int FontFallback(App app, string size)
  - 尺寸档对应的主题字号：tiny/small/large/huge，
    medium 与未知档回退 fontSizeMedium。

- static string Hex8(int v)
  - 把 32 位颜色输出为 8 位十六进制（#AARRGGBB），按二进制补码
    逐 nibble 提取，这样经 StyleSheet.HexToInt 能原样往返
    回同一个带符号 int——与 `%` 的符号约定无关。

- static string HexDigit(int n)
  - 0–15 的单个十六进制大写数字字符。

- static bool FlatType(string type)
  - 对直接绘制在给定区域内、不拥有表面的
    类型返回 true，这样皮肤的全局边框和阴影外壳就不会
    给它们框出盒子。

- static void SizeDefaults(App app, StyleBox b, string cls)
  - `tiny` / `small` / `medium` / `large` 类对应的尺寸档位，
    作用于高度、字号和水平内边距。所有带尺寸的控件
    （button、tag 等）共用它，所以 `button.large` 和 `tag.large` 表示
    同一档，皮肤仍可覆写其中任何一项。

- static string TypeClass(int type)
  - 语义类型：1 primary，2 info，3 success，4 warning，5 error。

- static string RoleClass(string cls)
  - 列表已携带的角色类（"primary" … "error"），中性时返回 ""。
    需要按角色选择图标或部件样式的控件
    读取它，而不是自行逐个判断角色名。

- static string FillClass(int fill)
  - 填充方式：1 outline，2 text，3 dashed（0 = solid，无类）。

- static string SizeClass(int size)
  - 尺寸：0 tiny，1 small，2 medium，3 large。

- static string StateClass(int index, int current, int errorIndex)
  - 条目在序列中的位置：`done` 表示在当前项之前，
    `active` 是当前项，`pending` 在其后，失败时为 `error`。所有
    序列展示（步骤指示器、时间线、向导轨道）共用它，
    这样一条皮肤规则即可统一各处同一状态的样式。

- static int Fade(int color, int a)
  - 把不透明打包颜色的 alpha 缩放到 `a` 千分比（0..1000），
    任何元素都能通过它绘制来实现淡入淡出。

- static int TypeColor(Theme t, int type)
  - 按钮类型的强调色（默认回退到主文字色，
    保证 tinted/ghost/text 样式仍然可读）。

- static int TypeFill(Theme t, int type, int style, bool hovered, bool pressed)
  - 给定交互状态下按钮型表面的背景。
    `style` 0 = solid，1 = outline。

- static int TypeFg(Theme t, int type, int style)
  - 与 TypeFill 匹配的前景（label）颜色。

- static void ButtonDefaults(App app, StyleBox b, string cls, bool active, bool disabled)
  - 按钮的几何量与非声明式装饰。颜色（角色、变体、各状态）
    全在 skins/base.css 里，这里一律不碰——否则皮肤写了
    `button.primary:active` 也改不动一个按下色。

- static void SurfaceDefaults(App app, StyleBox b, string cls)
  - 通用表面（卡片/面板）的主题默认值：背景、文字、圆角、细边框、
    柔和投影与四边内边距；玻璃主题改为半透明色调 + 背景模糊并去
    边框。解析主路径的这些外观已改由 skins/base.css 声明，此方法
    当前无调用方，保留给绕过 CSS 的场景。

- static void TabDefaults(App app, StyleBox b, string cls)
  - 单个标签页的几何量。颜色（基础/悬停/选中、下划线与卡片
    描边）在 skins/base.css 的 `tab`、`tab.card`、`tab.segment`
    规则里。

- static void Inline(StyleBox b, Control c)
  - 把控件自身的 inline 样式（Control.Bg/Radius/Border/... 或 UiDoc 应用的
    CSS）叠加到已解析的 box 上，使 retained-mode 控件与
    immediate-mode 控件共用一条解析路径。


## StyleBox (class)

已解析的视觉样式：主题默认值加上皮肤样式表中
匹配某个控件某个状态的声明，展平后的结果。

这是 GUI 唯一知道如何 *paint* 一个带样式 box 的地方，
控件无需再携带按皮肤分叉的绘制代码，它只解析一次
然后绘制：

StyleBox s = Style.Eased(app, id, "button", "primary", disabled);
s.Paint(app, x, y, w, h);
s.DrawLabel(app, x, y, w, h, "Save");

每个字段都是 int（GUI 栈不使用浮点）。`0` 表示颜色"未设置"，
`-1` 表示度量未设置，因此声明可以把任何一项留给主题默认值；
通过接收回退值的 `*Or` 访问器读取它们。

- int prescaled;
  - 设备像素来源标记：每个位（SourceFont 等）对应一个长度属性，
    置位表示该属性的当前值已是设备像素，ScaleLayout 不再对其二次缩放。

- int bg;

- int bgTo;

- int bgVia;

- int bgDir;

- int opacity;

- int blur;

- int fg;

- int accent;

- int fontPx;

- int fontWeight;

- int lineHeight;

- int letterSpacing;

- int align;

- int valign;

- int textCase;

- int ellipsis;

- int nowrap;

- int borderColor;

- int borderW;

- int borderTopW;

- int borderTopColor;

- int borderRightW;

- int borderRightColor;

- int borderBottomW;

- int borderBottomColor;

- int borderLeftW;

- int borderLeftColor;

- int radius;

- int radiusTL;

- int radiusTR;

- int radiusBR;

- int radiusBL;

- int shadow;

- int shadowDx;

- int shadowDy;

- int shadowBlur;

- int shadowInset;

- int borderStyle;

- int emboss;

- int specular;

- int fxId;

- int sheen;
  - 玻璃光泽（`-zan-sheen`）：盒子内侧的一道自上而下衰减的
    高光加一圈内缘亮边，强度为 0..1000 千分比（0 = 关闭）。
    这是真实玻璃“上沿受光、边缘出亮线”的部分，声明在 CSS 里，
    由绘制盒子的每个控件统一应用。

- int sheenColor;

- int padL;

- int padT;

- int padR;

- int padB;

- int marL;

- int marT;

- int marR;

- int marB;

- int width;

- int height;

- int minW;

- int minH;

- int maxW;

- int maxH;

- int widthPm;
  - 上述六种度量的百分比形式，以包含块内容框的
    千分比表示（-1 未设置）。`width: 34%` 设置 widthPm = 340，布局
    再针对父级给出的空间解析它。

- int heightPm;

- int minWPm;

- int minHPm;

- int maxWPm;

- int maxHPm;

- int gap;

- int rowGap;
  - 轴向独立的间距（-1 未设置，回退到 `gap`）：换行的选项组
    需要行距和列距不同（列距贴着标签，行距要拉开）。

- int colGap;

- int columns;
  - 每行的等分列数（-1 未设置 = 按可用宽度自动换行）。

- int display;

- int flexDir;

- int justify;

- int alignItems;

- int wrap;

- int alignContent;
  - 换行容器里各行在交叉轴上的分布（CSS `align-content`）：
    0 start，1 center，2 end，3 space-between，4 space-around，5 stretch。
    默认 start——本框架的容器按内容测量自身高度，若按 CSS
    的 `stretch` 默认值，一个被停靠成 fill 的换行容器会把两行
    悄悄撑到上下两端，与作者写下的紧凑排版不符。

- int alignSelf;
  - 单个子项覆盖容器的 `align-items`（CSS `align-self`）：
    -1 未声明（跟随容器），0 stretch，1 start，2 center，3 end。

- int grow;

- int shrink;
  - CSS `flex-shrink`：-1 未声明（等同 1，行溢出时按比例收缩），
    0 = 不参与收缩（固定宽的侧栏、图标不该被挤扁）。

- int basis;
  - CSS `flex-basis`：主轴基准尺寸，优先于 width/height 与测量
    偏好。-1 未声明；basisPm 是同一属性的千分比形式（`50%`）。

- int basisPm;

- int aspect;
  - CSS `aspect-ratio`：宽高比的千分比（1778 = 16/9）。0 未声明。
    只声明了一根轴时，另一根由这个比例推出。

- int order;

- int position;

- int posT;

- int posR;

- int posB;

- int posL;

- int overflow;

- int zIndex;

- int cursor;

- int visible;

- int transitionMs;

- int easing;

- int anim;

- int animMs;

- int tx;

- int ty;

- int scale;

- int rotate;

- static int Unset()
  - 度量未设置的通用哨兵（-1）。

- static int SourceFont()
  - prescaled 位 1：字号已按设备像素。

- static int SourceWidth()
  - prescaled 位 2：宽度类度量（width/minW/maxW/basis）已按设备像素。

- static int SourceHeight()
  - prescaled 位 4：高度类度量（height/minH/maxH）已按设备像素。

- static int SourceGap()
  - prescaled 位 8：间距（gap/rowGap/colGap）已按设备像素。

- static int SourceRadius()
  - prescaled 位 16：圆角半径已按设备像素。

- static int SourcePadding()
  - prescaled 位 32：内/外边距已按设备像素。

- static int SourceIcon()
  - prescaled 位 64：图标尺寸已按设备像素。

- bool IsPrescaled(int source)
  - `source` 位标记的属性是否已是设备像素（无需再缩放）。

- void SetPrescaled(int source, bool value)
  - 置位/清位 `source` 属性的设备像素标记。

- StyleBox()
  - 空 box：什么都不设置，所有访问器都返回其回退值。

- StyleBox Clone()
  - 逐字段复制（解析缓存发放副本，以便控件可以
    微调自己的 box 而不污染缓存）。

- int BgOr(int fb)
  - 填充背景色；未设置（0）返回 fb。

- int FgOr(int fb)
  - 文字/图标颜色；未设置返回 fb。

- int AccentOr(int fb)
  - 强调色；未设置返回 fb。

- int FontOr(int fb)
  - 字号（px）；未声明（<= 0）返回 fb。

- int RadiusOr(int fb)
  - 统一圆角半径；未声明（< 0）返回 fb。

- int BorderWOr(int fb)
  - 统一边框宽度；未声明（< 0）返回 fb。

- int BorderOr(int fb)
  - 统一边框颜色；未设置返回 fb。

- int GapOr(int fb)
  - 子项间距；未声明（< 0）返回 fb。

- int RowGapOr(int fb)
  - 行距；未声明回退 GapOr。

- int ColGapOr(int fb)
  - 列距；未声明回退 GapOr。

- int ColumnsOr(int fb)
  - 每行等分列数；未声明返回 fb。

- int HeightOr(int fb)
  - 高度；未声明（< 0）返回 fb。

- int WidthOr(int fb)
  - 宽度；未声明（< 0）返回 fb。

- int Corners()
  - 圆角实际应用的角（Corner.TL|TR|BR|BL）。
    声明自身圆角为 0 的角是直角，所以 `border-radius:
    6 6 0 0`（标签页、焊接组的末尾按钮）会绘制成真正的
    半圆角盒子，而不是四角全圆。

- void SetCorners(int m)
  - 把 `m` 之外的角改为直角，其余角保留圆角。

- static int MetricIn(int pm, int abs, int avail, int fb)
  - 按包含块解析度量：百分比优先，其次
    绝对值声明，最后才是调用方的回退值。

- int WidthIn(int avail, int fb)
  - 在 `avail` px 的包含块内声明的宽度（样式未声明时用 `fb`），
    所以 `width: 50%` 和 `width: 200px` 都可用。

- int HeightIn(int avail, int fb)
  - 在 `avail` 像素包含块内解析声明的高度
    （百分比优先、绝对值次之、`fb` 兜底），同 WidthIn。

- int BasisIn(int avail)
  - `flex-basis` 在 `avail` 像素的主轴包含块内解析出的基准尺寸，
    未声明时返回 -1（调用方回退到 width/height 或测量偏好）。

- int ClampWIn(int avail, int v)
  - 将 `v` 限制在 min/max-width 内，百分比边界相对
    containing block 解析。

- int ClampHIn(int avail, int v)
  - 把 `v` 限制在 min/max-height 内，百分比边界相对
    `avail` 的包含块解析。

- int TransitionOr(int fb)
  - 状态过渡时长（毫秒）；未声明（< 0）返回 fb。

- int PadLOr(int fb)
  - 内容框左内边距；未声明（< 0）返回 fb。

- int PadTOr(int fb)
  - 内容框顶部内边距；未声明（< 0）返回 fb。

- int PadROr(int fb)
  - 内容框右内边距；未声明（< 0）返回 fb。

- int PadBOr(int fb)
  - 内容框底部内边距；未声明（< 0）返回 fb。

- int ClampW(int w)
  - 将 `w` 限制在盒子的 min/max-width 内（未设置的边界忽略）。

- int ClampH(int h)
  - 把 `h` 限制在盒子的 min/max-height 内（未设置的边界忽略）。

- void SetPad(int v)
  - 一次设置所有 padding 边（`padding: n` 简写用）。

- void SetMargin(int v)
  - 一次设置所有 margin 边。

- void SetRadius(int v)
  - 一次设置四个圆角半径。

- void SetBorder(int w, int color)
  - 一次设置统一边框的宽度与颜色。

- static StyleBox Blend(StyleBox a, StyleBox b, int p)
  - 按千分数 `p` 线性混合两个已解析的盒子——`transition` 如何
    让控件在基础外观与状态外观之间淡入淡出。颜色
    通过 App.LerpColor 混合（一侧未设置时用 ScaleAlpha 保留 alpha），
    度量值插值，flags/枚举在
    中点处切换。

- static int MixColor(int c0, int c1, int p)
  - 混合两个颜色，把 0（未设置）视为“淡出另一个颜色”，这样
    只*添加*填充的状态仍会平滑淡入而非突然出现。

- static int MixMetric(int v0, int v1, int p)
  - 插值一个度量值，-1 表示“未设置”（未设置的一侧保留
    另一侧的值，而不是从无效的 -1 过渡）。

- static int AlphaOf(int color)
  - 取打包颜色的 alpha 分量（0..255）。

- int Fade(int color)
  - 对颜色应用 `opacity`（完全不透明时不做任何事）。

- void Paint(App app, int x, int y, int w, int h)
  - 绘制盒子：背景模糊、投影、填充（纯色或渐变）、
    各边边框，然后叠加任意 `animation`。遵循 `transform`
    （translate/scale）和 `opacity`；`display: none` / `visibility: hidden` 的
    盒子不绘制任何内容。

- void PaintShadow(App app, int x, int y, int w, int h, int r)
  - 投影：圆角 SDF 一次出图（见 Canvas.ShadowRoundRect）。
    以外轮廓到圆角形状的有符号距离在 blur 带上做 smoothstep 衰减，
    半跨带正好落在轮廓上（半个覆盖），与高斯 box-shadow 的观感一致；
    衰减连续，角部不会留下逐圈扩张描边的楔形缝/同心弧，每个像素
    只写一次，半透明阴影色合成到标称 alpha。

- void PaintSheen(App app, int x, int y, int w, int h, int r)
  - 玻璃光泽（`-zan-sheen`）：上半部分一道自上而下衰减到透明的
    高光带（裁进盒子的上圆角），加一圈 1px 内缘亮边，上沿最亮。
    这就是液态玻璃“受光面 + 出亮线”的部分，皮肤按强度声明，
    所有画 box 的控件统一得到同样的质感。

- void PaintGradient(App app, int x, int y, int w, int h, int r)
  - 带圆角半径的渐变填充：方形不透明渐变直接用 FillVGrad，
    其余交给抗锯齿的圆角渐变原语 FillGradMask。

- void PaintBorders(App app, int x, int y, int w, int h, int r)
  - 任一侧已设置时绘制各边边框，否则绘制统一边框。

- void PaintSideArc(App app, int x, int y, int w, int h, int r, int on, int cx, int cy, int hw, int vw, int hcol, int vcol)
  - 补画一个圆角上的边框弧：裁剪到该角的 r×r 方块，再用整盒
    圆角描边（与圆角填充同一轮廓、已抗锯齿）画出弧段。粗细取
    相邻两边中较粗的一边，颜色取水平边、缺省用竖直边。

- int SideColor(int col)
  - 某条边的边框色：该边未单独指定颜色时回退统一
    borderColor；结果做 opacity 衰减。

- void PaintAnim(App app, int x, int y, int w, int h, int r)
  - `animation` 层：在盒子内绘制的关键帧式动画，
    且自触发（运行期间持续请求帧）。

- int FloatOffset(App app, int x, int y, int w, int h)
  - 本帧 `float` 动画贡献的额外偏移（控件把它加到
    内容原点，使整个控件上下浮动）。

- int SpinDeg(App app, int x, int y, int w, int h)
  - 本帧 `spin` 动画贡献的旋转角度（度）。

- int DrawLabel(App app, int x, int y, int w, int h, string label)
  - 在 [x,y,w,h] 内绘制标签，遵循颜色、字号/字重、
    text-align、vertical-align、letter-spacing、text-transform 和
    text-overflow: ellipsis。返回实际绘制的宽度。

- void DrawRun(Canvas c, int x, int y, string s, int color, int fs)
  - 在精确原点绘制一段文本（无盒子对齐），应用
    字间距以及 `font-weight >= 600` 的模拟加粗。

- static int MeasureSpaced(string s, int fs, int spacing)
  - 文本宽度：MeasureText 加上 letter-spacing（每字符 spacing 像素）。

- static string Truncate(string s, int fs, int spacing, int avail)
  - `s` 的最长前缀加 “...”，且能放入 `avail` px 内。


## StyleSheet (class)

CSS 声明级联，应用于已解析的 StyleBox（
皮肤路径，每个控件通过 Style 使用）或 retained-mode Control
（在 UiDoc 构建期间）。

样式表是 selector -> declaration-block 映射。选择器保留 CSS
拼写（`button`、`.primary`、`button.primary`、`#save`），并可能带有
`:state` 后缀（`:hover`、`:active`、`:focus`、`:disabled`、`:selected`、
`:checked`）。特异性按 type -> class -> type.class -> id 递增，状态
规则叠加在基础外观之上，所以 `button:hover` 只需注明
变化的部分。

值是真正的 CSS：颜色用 `#rgb / #rrggbb / #aarrggbb / rgb() / rgba() /
hsl() / hsla()` 或命名颜色，长度带或不带 `px`，时长用
`120ms / 0.2s`、`linear-gradient(...)`、`box-shadow: x y blur color`、
`backdrop-filter: blur(20px)`、`transform: translate/scale/rotate`、flex
布局、排版和 `animation: <name> <dur> <easing>`。

- JsonValue rules;

- JsonValue vars;
  - 解析后保留的 `:root` 自定义属性（`--name` -> 值），这样
    皮肤除了控件规则外，也能供给语义化 Theme token。

- string state;
  - 下次 Apply 在普通选择器之外还要解析的伪状态
    （“hover”、“active”、“focus”、“disabled”；“” = 仅基础外观）。

- List<string> selText;

- List<string> selType;

- List<string> selClasses;

- List<string> selClass0;
  - 规则要求的第一个类名（无类要求时为“”）。把颜色与状态
    下沉进 CSS 后，`button` 那一桶里绝大多数规则都带类
    （`button.ghost.primary:hover` 之类），先用这一个字符串比较筛掉，
    就不必为每条规则再切分一次类名串。

- List<string> selContains;
  - `[class*="frag"]` 要求的 class 属性子串（无该要求时为“”）。

- List<string> selId;

- List<string> selPart;

- List<string> selState;

- List<int> selStateMask;
  - 选择器要求的状态位（多个伪类取与）；引擎不认识其中
    任何一个伪类时为 -1（该规则永不匹配）。

- List<int> selSpec;

- int indexedCount;

- List<JsonValue> selBlock;
  - 每条规则的声明块，索引与上面的选择器表对齐：匹配后直接取，
    不再按选择器文本回查 rules（一次首帧解析要按名字查上百次）。

- Dict <string, List<int>> byType;
  - 按类型名分桶的规则下标（升序，因此与 anyType 归并后仍是级联顺序）。
    一个控件只需看自己类型那一桶加上无类型的那些规则，
    而不是每次解析都扫全表——冷解析（首帧、换肤）的主要成本在此。

- List<int> anyType;
  - 没有类型选择器的规则下标（`.primary`、`#save`、`::option`）。

- StyleSheet()
  - 构造空表（规则/变量为空 JSON 对象，索引延迟建立）。

- static StyleSheet FromCss(string src)
  - 解析以 CSS 文本编写的样式表（见 Css）。皮肤以 `.css` 文件发布，
    以便在不重新构建应用的情况下编写和替换。

- void MergeSheet(StyleSheet other)
  - 将另一张表的规则和自定义属性叠加到当前表上
    （另一张表优先），这样应用样式表可以重新应用
    到当前激活的皮肤之上，而不会被其替换。

- static StyleSheet FromJson(string src)
  - 从 JSON 源字符串解析样式表。格式错误 / 非对象的
    文档会产生空样式表，因此坏文件永远不会中断加载。

- bool IsEmpty()
  - 样式表完全没有规则时为 true（应用未加载皮肤）。

- string Var(string name)
  - `:root` 自定义属性的值（`Var("--accent")`），不存在时返回“”。

- JsonValue Block(string selector)
  - 单个选择器的声明块（选择器不存在时为 null）。

- void ApplyBox(StyleBox b, string selector)
  - 将一个选择器的声明叠加到已解析的样式盒上。未知
    属性在此忽略（它们是控件属性，由
    ApplySelector 处理）。

- void ApplyMatch(StyleBox b, string type, string cls, string id, string part, int stateBits)
  - 将匹配控件的每条规则应用到 `b`，最弱的匹配优先，
    因此最具体的声明胜出。`classes` 是控件的 class
    列表，`part` 选择 `type::part` 规则（“”表示控件本身），
    `stateBits` 是 Style.S* 掩码。
    
    排序以状态为主：所有无状态规则先应用（按 CSS
    特异性：type < class < class chain < id），然后是每个
    活动状态的规则，因此无论作者把 `:hover` 放在文件
    何处，它都只需注明变化的部分。

- void ApplyDecls(StyleBox b, JsonValue block)
  - 把已经取到的声明块叠加到样式盒上。

- bool Matches(int i, string type, List<string> classes, string id, string part, int stateBits, string cls)
  - 规则 `i` 是否选中给定的控件/部件/状态。`cls` 是 class
    属性原文，供 `[class*="frag"]` 做子串匹配。

- static int StateMask(string state)
  - 一组伪类名对应的状态位掩码（含未知伪类时为 -1）。

- static string FirstClass(string classes)
  - 空格分隔类名串里的第一个名字（“”表示没有类要求）。

- static bool Holds(List<string> list, string name)
  - 类名列表中是否含 name。

- void Index()
  - 一次性解析每个选择器，并按权重保持规则有序，因此
    匹配就是对已排序表的扫描。

- static string ValStr(JsonValue v)
  - 声明值的文本形式（数字转成字符串，因此 JSON 表中的 `radius: 8`
    行为与 CSS 中的 `radius: 8px` 一致）。

- static bool IsPrescaled(JsonValue block, string key)
  - 声明 key 的值是否直接来自 `var(--font-size-*)`（主题已按
    DPI/密度缩放，应用样式不得再叠加缩放；见 Css.ParseBlock）。

- static bool Decl(StyleBox b, string key, string val)
  - 将一条 CSS 声明应用到样式盒。当该
    属性不是引擎理解的视觉/布局属性时返回 false。

- static bool DeclSource(StyleBox b, string key, string val, bool prescaled)
  - 应用一条声明，并按属性类别记录“预缩放来源”位
    （Decl 不认得的属性返回 false）。

- static int SourceFor(string key)
  - 属性对应的预缩放来源类别（StyleBox.Source*），无关属性为 0。

- static bool DeclFill(StyleBox b, string k, string v)
  - fill：背景 / 透明度 / 模糊滤镜。

- static bool DeclText(StyleBox b, string k, string v)
  - text：颜色 / 字体 / 对齐 / 变换 / 换行。

- static bool DeclBorderBox(StyleBox b, string k, string v)
  - border / 圆角 / 阴影。

- static bool DeclBoxMetrics(StyleBox b, string k, string v)
  - 盒子度量：padding / margin / size / gap。

- static void DeclMetric(StyleBox b, int which, string v)
  - 单个盒子度量（0 宽、1 高、2/3 min、4/5 max）：`%` 值保留
    为包含块的比例（千分数），其余按像素处理。

- static bool DeclLayout(StyleBox b, string k, string v)
  - layout：display / flexbox / position / overflow / visibility / cursor。

- static int JustifyCode(string v)
  - `justify-content` 的取值码：0 start，1 center，2 end，
    3 space-between，4 space-around/evenly。

- static int AlignContentCode(string v)
  - `align-content` 的取值码：0 start，1 center，2 end，
    3 space-between，4 space-around/evenly，5 stretch。

- static void DeclFlex(StyleBox b, string val)
  - `flex: none | auto | initial | <grow> [<shrink> [<basis>]]`。

- static void DeclBasis(StyleBox b, string val)
  - `flex-basis: auto | content | <px> | <pct>`：主轴基准尺寸。
    `auto` 撤销声明，回退到 width/height 或控件的测量偏好。

- static void DeclAspect(StyleBox b, string val)
  - `aspect-ratio: auto | <w> / <h> | <ratio>`，存为千分比
    （`16 / 9` -> 1778）。

- static bool DeclMotion(StyleBox b, string k, string v)
  - motion：transition / transform / animation。

- static void DeclBackground(StyleBox b, string val)
  - `background: <color> | linear-gradient([<dir>,] a, b[, c])`。

- static int GradientDir(string tok)
  - 渐变方向关键字/角度作为 StyleBox.bgDir，当该
    token 是颜色停靠点（color stop）时返回 -1。

- static string StopColor(string stop)
  - 去掉停靠点的位置（`#fff 40%` -> `#fff`）。

- static void DeclBorder(StyleBox b, string val, int side)
  - `border[-side]: <width> [style] <color>`（顺序任意，宽度可选）。

- static void DeclRadius(StyleBox b, string val)
  - `border-radius: all | tl tr br bl`（`999`/`50%` 将形状完全圆化）。

- static void CornerRadius(StyleBox b, int which, int v)
  - 单个角的圆角（`border-top-left-radius` 等，`which`：0 TL、
    1 TR、2 BR、3 BL）。
    
    未被声明过的角先继承当前的 `radius`：StyleBox 用"四个角都
    未声明"表示全圆角，只写一个角的话另外三个必须落成具体值，
    否则 Corners() 会把它们当成直角，一条
    `border-top-left-radius: 0` 就会把整个盒子削成方的。

- static void DeclShadow(StyleBox b, string val)
  - `box-shadow: [inset] <dx> <dy> [blur] <color>`（或仅一个颜色）。

- static void DeclSheen(StyleBox b, string val)
  - `-zan-sheen: none | <strength> [color]`：玻璃光泽强度（`0.35`、
    `35%` 或千分比 `350`），可选高光颜色（默认白）。绘制由
    StyleBox 统一完成，因此任何画 box 的控件都能被皮肤点亮。

- static void DeclSides(StyleBox b, string val, int which)
  - `padding/margin: all | v h | t h b | t r b l`。

- static void DeclTransition(StyleBox b, string val)
  - `transition: [prop] <duration> [timing]`——这里只有时长和 timing
    有意义（所有可动画属性一起缓动）。

- static void DeclTransform(StyleBox b, string val)
  - `transform: translate(x,y) translateX(x) translateY(y) scale(n) rotate(deg)`。

- static void DeclAnimation(StyleBox b, string val)
  - `animation: <name> <duration> [timing] [infinite]`。名称映射到
    内置关键帧（spin、pulse、breath、shimmer、float、glow、aurora、
    motes），由 Fx 绘制。

- static int BlurArg(string val)
  - 滤镜值中的 `blur(20px)` -> 20（无时为 0）。

- static int Easing(string val)
  - 缓动函数名转枚举码：ease/linear/ease-in/ease-out/ease-in-out，
    不认识返回 -1。

- static int Weight(string val)
  - 字重关键词转数值：bold=700 / normal=400 / light=300，
    其余按数字解析。

- static int CursorCode(string val)
  - cursor 关键词转系统光标码（pointer/text/resize 等，
    不认识回退箭头）。

- void Apply(Control c, string type, string cls, string id)
  - 将匹配的规则应用到 `c`，按特异性升序（type，然后
    class，然后 id），最具体的选择器胜出。

- void ApplySelector(Control c, string selector)
  - 将一个选择器的声明应用到控件：layout 键落在
    控件自身的字段上，视觉键走共享的 StyleBox 解析器
    （因此 CSS 在 retained 和 immediate 模式下行为一致），其余
    通过 SetProp 发布给控件。

- static void CopyToControl(StyleBox b, Control c)
  - 复制控件内联携带的视觉属性（Control 只保留
    一小部分；其余在绘制时存于解析后的 StyleBox 上）。

- static void ApplyBackground(Control c, string val)
  - 在控件上设置纯色填充或 `linear-gradient(a,b)`。

- static void ApplyBorder(Control c, string val)
  - 解析 `border: <width> <color>`（宽度可选，默认为 1）。

- static int ParseColor(string val)
  - 将 CSS 颜色解析为打包的 0xAARRGGBB int。接受 `#RGB`、
    `#RRGGBB`、`#RRGGBBAA`、`#AARRGGBB`、`rgb()/rgba()`、`hsl()/hsla()`、
    `0x...`、纯十进制数和 CSS 命名颜色。空值或无法解析的值
    返回 0（= 未设置），因此坏规则只是什么都不做。

- static int ParseRgb(string val)
  - `rgb(r,g,b)` / `rgba(r,g,b,a)`，`a` 为 0..1 或百分比。

- static int ParseHsl(string val)
  - `hsl(h,s%,l%)` / `hsla(...)` 转换为 RGB（整数运算）。

- static int Chan(string tok)
  - 单个 rgb() 通道：`0..255` 或百分比。

- static int Clamp255(int v)
  - 钳制到 0..255。

- static int Pack(int a, int r, int g, int b)
  - 将 a,r,g,b（0..255）打包为 GUI 的有符号 0xAARRGGBB int。

- static int NamedColor(string name)
  - 皮肤实际会用到的 CSS 命名颜色（未知时为 0）。

- static int HexToInt(string h)
  - 将十六进制字符串（最多 8 位）转换为打包 int。最高位为 1
    （alpha >= 0x80）自然产生负数，与 Theme token 一致。

- static int HexDigit(string ch)
  - 单个十六进制字符的值（0-15），非十六进制时 -1。

- static bool Digit(string ch)
  - 字符是否为十进制数字。

- static bool IsNumeric(string tok)
  - token 读作数字时返回 true（可选符号、十进制、带
    px/ms/s/%/deg 等单位后缀），而非关键字或颜色。

- static int Num(string val)
  - 将 CSS 长度/数字转为 int：感知符号、容忍单位（`12px`、`-4`、
    `1.5rem` -> 1、`200ms`），非数字 token 返回 0。

- static int Perm(string val)
  - 比例转千分数：`1` / `1.0` -> 1000、`0.5` -> 500、`60%` -> 600、
    `255`（alpha 通道）由调用方保持 255 比例。

- static int Ms(string val)
  - CSS 时长（毫秒）：`200`、`200ms`、`0.25s`。

- static int ParseInt(string s)
  - 值转整数（透传 Num 解析）。

- static List<string> Tokens(string val)
  - 将值按空白拆分为 token，保持 `fn(a, b)`
    分组完整，使 `rgba(0,0,0,.4)` 作为一个 token 保留。

- static bool StartsWith(string s, string prefix)
  - s 是否以 prefix 开头。

- static int IndexOf(string s, string ch)
  - 子串首次出现位置（无则 -1，转发 Css.IndexFrom）。

- static bool EndsWith(string s, string suffix)
  - s 是否以 suffix 结尾。

- static int LastIndexOf(string s, string ch)
  - 单字符查找（`ch` 只取首字符）。

- static string Lower(string s)
  - 转小写（属性名/关键字匹配用）。

- static string Trim(string s)
  - 转发 Css.Trim（去两端空白）。

- static int DockValue(string text)
  - 把停靠名（`top`/`bottom`/`left`/`right`/`fill`）解析为
    Dock 常量。供样式表 / JSON 文档共用。

- static string Scalar(JsonValue v)
  - 把标量 JSON 值渲染为 SetProp 期望的文本。


## Subscription (class)

一个保留式多播事件注册表，将 C# 风格的委托事件
叠加在即时模式控件上。处理器只需注册一次（在帧
循环之前，按稳定的整数 key 注册），然后每帧把即时模式的点击
通过 `RaiseIf` 桥接进来：

EventHub hub = new EventHub();
hub.On(BTN_SAVE, () => { ... });   // like  OnClick += handler
// per frame:
int id = Button.Render(app, x, y, "Save");
hub.RaiseIf(BTN_SAVE, Ui.Clicked(app, id));

同一 key 的多次 `On` 调用都会被执行（多播）；
`Off` 清除它们（相当于对整个 key 执行 <c>OnClick -= handler</c>）。

- int key;

- Action handler;

- Subscription(int key, Action handler)


## Text (class)

文本编辑控件（Input、CodeEditor、
过滤器输入框）共用的纯字符串小工具。放在这里意味着每个控件无需重复实现
字符解码和编辑原语。

字符串是 UTF-8 字节数组，下文所有索引均为字节偏移。字符
辅助函数让这些偏移始终位于 UTF-8 序列边界，使多
字节字符（CJK、带变音拉丁字母、emoji）能被整体
插入、删除和导航，而不是按原始字节处理。

- static string ByteChar(int b)
  - 单个字节值（0..255）转为单字节字符串。通过字节缓冲区
    写入，而不是 sprintf("%c")：sprintf 是变参函数，而变参
    参数在 Darwin arm64 上遵循不同的 ABI（栈上传递，而非
    寄存器），因此那里的字节会变成垃圾值。

- static string CharStr(int code)
  - 将 Unicode 码点编码为 UTF-8 字符串。控制
    码、DEL、孤立代理项和越界值返回“”，以便调用方忽略
    非文本输入（运行时以码点形式交付键入的字符）。

- static bool IsPrintable(int code)
  - `code` 为可打印字符（任何非控制码点）时为 true。

- static int SeqLen(int b)
  - 以 `b` 为引导字节的 UTF-8 序列的字节数。

- static int PrevCharStart(string s, int pos)
  - 恰好在 `pos` 之前结束的字符的起始字节索引（向后扫描
    UTF-8 连续字节）。限制到 0。

- static int NextCharEnd(string s, int pos)
  - 从 `pos` 开始的字符之后的第一个字节索引。限制到字符串长度。

- static int ClampCharStart(string s, int pos)
  - 将字节偏移回退到它所在的 UTF-8 字符
    的起点，因此按结果切片永远不会切开多字节字符
    （被切开的字符会渲染为替换字形）。已在
    边界上的偏移原样返回。

- static string DropLast(string s)
  - 移除 `s` 的最后一个字符（空字符串保持为空）。

- static string Left(string s, int pos)
  - `s` 的左切片 [0, pos)，限制到有效边界。

- static string Right(string s, int pos)
  - `s` 的右切片 [pos, len)，限制到有效边界。

- static string InsertAt(string s, int pos, string ins)
  - 在字节索引 `pos`（0..len）处将 `ins` 插入 `s`。

- static string RemoveAt(string s, int pos)
  - 移除从字节索引 `pos` 开始的整个字符（越界时
    无操作）。

- static string DeleteBefore(string s, int pos)
  - 移除恰好在字节索引 `pos` 之前结束的整个字符（退格键）。

- static int Chars(string s)
  - `s` 里的码点个数（一个 CJK 字 / 一个基础 emoji 记 1，与字节数
    无关）。字符上限与字数统计都按这个口径。

- static int CpAt(string s, int pos)
  - `pos` 处码点的数值（越界返回 -1）。按 UTF-8 前导字节还原：
    n 字节序列取前导字节低 7-n 位，续字节各取低 6 位。

- static bool IsExtend(int cp)
  - 码点是否属于"并入前一簇"的扩展集（简化规则，覆盖 emoji 与
    带音拉丁字母的常见情形）：Mn 组合段、符号组合段、变体选择符、
    半标记、组合键帽、肤色修饰符、emoji tag、韩文字母尾音段。

- static int Graphemes(string s)
  - `s` 里的字素簇个数（Naive UI `count-graphemes` 的口径）。在码点
    计数上合并扩展簇：区域指示符成对（🇨🇳=1）、零宽连接符把后一个
    码点并入同簇（👨‍👩‍👧=1）、其余组合标记/变体/肤色/tag
    并入当前簇（💐️=1、🥷🏿=1）。


## TextWrap (class)

位于 `Text` 类之外的文本辅助函数，这样声明了同名
`Text` 成员（Label）的控件仍能调用它们，而不被成员遮蔽
类名。对字符串的纯函数，外加基于像素的换行。

- static string Trim(string s)
  - 去除首尾的 ASCII 空白（空格、制表符、CR、LF）。

- static List<string> Lines(string s, int maxW, int fs)
  - 将 `s` 拆成行，每行在 `fs` 磅下都能放进 `maxW` 像素，
    尽可能在空格处换行，否则在任意字符处换行（因此无空格的 CJK
    文本也能换行）。硬换行（字节 10）始终断行。
    至少返回一行；结尾换行不会增加空行。


## Theme (class)

NaiveUI 主题 token。所有颜色打包为 0xAARRGGBB 存入 int。

- int primary;

- int primaryHover;

- int primaryPressed;

- int info;

- int infoHover;

- int infoPressed;

- int success;

- int successHover;

- int successPressed;

- int warning;

- int warningHover;

- int warningPressed;

- int error;

- int errorHover;

- int errorPressed;

- int textPrimary;

- int textSecondary;

- int textTertiary;

- int textDisabled;

- int textInverse;

- int bgPrimary;

- int bgSecondary;

- int bgTertiary;

- int bgHover;

- int bgActive;

- int bgDisabled;

- int borderPrimary;

- int borderSecondary;

- int borderHover;

- int borderFocus;

- int divider;

- int overlay;

- int glass;

- int glassBlur;

- int glassTint;

- int glassChromeTint;

- int glassSheen;

- int glassRadius;

- int glassShadowDy;

- int glassShadowBlur;

- int gradient;

- int bgGradTop;

- int bgGradBottom;

- int neu;

- int brutal;

- int fx;

- int scrollbar;

- int scrollbarHover;

- int tooltipBg;

- int tooltipBorder;

- int tooltipText;

- int tooltipTextMuted;

- int scrim;

- int scrimChip;

- int scrimChipHover;

- int onScrim;

- int statusDebugBg;

- int chart1;

- int chart2;

- int chart3;

- int chart4;

- int chart5;

- int chart6;

- int chart7;

- int chart8;

- int borderRadiusSmall;

- int borderRadiusMedium;

- int borderRadiusLarge;

- int borderWidth;

- int fontSizeTiny;

- int fontSizeSmall;

- int fontSizeMedium;

- int fontSizeLarge;

- int fontSizeHuge;

- int heightTiny;

- int heightSmall;

- int heightMedium;

- int heightLarge;

- int paddingTiny;

- int paddingSmall;

- int paddingMedium;

- int paddingLarge;

- int gapSmall;

- int gapMedium;

- int gapLarge;

- int iconSizeSmall;

- int iconSizeMedium;

- int iconSizeLarge;

- int iconSizeCaption;

- int shadowColor;

- int animFastMs;

- int animMediumMs;

- int animSlowMs;

- static Theme Light()
  - 浅色预设主题（NaiveUI 风格 token 的默认取值）。

- static Theme Dark()
  - 深色预设主题，动画背景默认为星空（BackdropFx.KindStars）。

- static int Rgb(int r, int g, int b)
  - 由 8 位 r/g/b 生成不透明颜色。

- static int Rgba(int r, int g, int b, int a)
  - 由 8 位 r/g/b 与 8 位 alpha（0 透明 .. 255 不透明）生成颜色。

- int GlassTint()
  - OS 玻璃合成器使用的当前主题着色。

- bool IsLightBg()
  - 当前主题表面的 RGB 亮度是否达到浅色阈值。

- void ApplyAccent(int color)
  - 应用外观抽屉选择的强调色覆盖。

- void MakeSurfacesOpaque()
  - 让三层窗口表面恢复完全不透明。

- void ApplyTranslucency(int surface, int chrome, int rail)
  - 按已推导出的 alpha 写回三层窗口表面。

- static int TokenColor(JsonValue v)
  - 颜色 token：解析 “#..”/“0x..”/十进制字符串，或直接接受原始 int。

- static void SetToken(Theme t, string key, JsonValue v)
  - 按 Theme 字段名将一条 token 应用到 `t`（去掉前导 “--”）。

- static Theme BaseTheme(JsonValue b)
  - “base” token 命名的起始 Theme：“light” 或 “dark”（皮肤是
    CSS 打包的，因此皮肤绝不会基于另一皮肤的代码）。

- static void ApplyTokens(Theme t, JsonValue obj)
  - 将 JSON 对象中的每个 token 应用到 `t`（跳过 “base” 键）。

- static Theme FromTokens(string json)
  - 从 JSON token 样式表构建 Theme：“base” token 选择
    起始 Theme，其余覆盖单个 token。格式错误 / 空的
    文档产生默认（Dark）主题，坏皮肤永远不会崩溃。

- void ScaleByDpi(int dpiPercent)
  - 按 DPI 百分比整体放大字号/高度/内边距/间距/图标/圆角等
    度量；dpiPercent ≤ 100 时不变，边框宽下限钳制为 1。

- List<int> SnapshotMetrics()
  - 把所有随缩放变化的度量（字号/高度/内边距/间距/图标/圆角/边框）
    快照成一个列表，顺序与 ApplyMetricsScaled 一一对应。用于设计器
    在渲染真实控件预览前保存基线，之后精确还原。

- void ApplyMetricsScaled(List<int> bm, int num, int den)
  - 以 `bm`（SnapshotMetrics 的返回值）为基线，按 num/den 缩放所有
    度量并写回。与 ScaleByDpi 不同，它支持缩小（num < den），且始终从
    基线计算，所以用 num == den 调用即可精确还原、不累积舍入误差。

- static int DensityPermille(int density)
  - 档位对应的度量缩放比（千分比）。档位是经验值而非线性
    百分比：小档字号别小于 12（可读性下限），大档约放大 15%。

- static string DensityName(int density)
  - 当前密度档的显示名（选择器 / 配置持久化共用）。

- static int DensityOf(string name)
  - 密度档名（"small"/"medium"/"large"，大小写不敏感）转档位，
    无法识别时返回 1（中）。

- void ApplyDensityScaled(List<int> bm, int density)
  - 以 `bm`（SnapshotMetrics 基线）为基线应用密度档：中档即基线，
    小/大档整体缩放后按可读性/可点性钳制下限。与
    ApplyMetricsScaled 相同的基线语义——任何档位切换都从
    快照重推，往返切换不累积舍入误差。


## Ui (class)

为 immediate-mode 控件提供的统一交互查询辅助函数。

每个控件的 Render() 返回一个 int id（从 App 的 focus
管理器分配并注册为命中区域）。这些静态辅助函数在一个地方
回答有关此类 id 的常见交互问题，每个控件
不再需要自己的 WasClicked/IsHovered 样板代码，应用
代码也能统一阅读：

int save = Button.Primary("Save").Render(app, r.x, r.y, r.width);
if (Ui.Clicked(app, save)) { ... }

- static bool Clicked(App app, int id)
  - 在鼠标主键于 `id` 上释放的那一帧返回 true
    （即点击在控件上完成）。使用 App 一次性解析的
    点击目标（指针下最顶层的控件，含弹出层），因此
    点击只投递给一个控件，而不是每一个与其重叠的控件。
    重新读取原始事件，修复遮挡/重复处理。

- static bool OwnsClick(App app, int id)
  - 精确自绘命中在矩形候选 owner 上的点击所有权。
    几何命中仍由调用方完成；此处只保证不会穿透上层控件。

- static bool PressedDown(App app, int id)
  - 按下（鼠标按下）落在 `id`（最上层目标）的帧为 true。

- static bool PressedOutside(App app, int id)
  - 本帧鼠标按下落在其他控件上时为 true，
    弹窗据此在外部点击时自动关闭。

- static bool Hovered(App app, int id)
  - 指针悬停在控件上时为 true。

- static bool Over(App app, int x, int y, int w, int h)
  - 指针落在矩形 [x,y,w,h] 内且没有被上层弹层/遮罩接管时
    为 true。凡是按几何自己算悬停的即时模式表面都该走这里：
    直接比较 app.mouseX/mouseY 的写法看不见画在它上面的
    下拉弹层，点击就会穿透到下面那一层。

- static bool ClickedIn(App app, int x, int y, int w, int h)
  - 本帧的主键释放落在 [x,y,w,h] 内，且该点击既未被认领
    也不属于上层弹层时为 true（按几何处理点击的表面用它
    代替 `EventKind() == 3` + 自己比坐标）。

- static bool Pressed(App app, int id)
  - 控件作为按下（mouse-down）目标时为 true。

- static bool Focused(App app, int id)
  - 控件持有键盘焦点时为 true。

- static bool Active(App app, int id)
  - 按钮按住且指针仍停留在其上时为 true，
    即绘制按下外观所用的“armed”（待触发）状态。

- static int HotId(App app)
  - 当前指针下方的控件 id，无则 -1。

- static bool MouseReleased(App app)
  - 本帧任意左键释放时为 true（与目标无关）。

- static bool MousePressed(App app)
  - 本帧任意左键按下时为 true。

- static bool Entered(App app, int id)
  - 指针首次移入 `id`（mouse-enter）的帧为 true。触摸屏上
    没有悬停，故该事件与按下重合。

- static bool Left(App app, int id)
  - 指针首次离开 `id`（mouse-leave）的帧为 true。

- static bool FocusGained(App app, int id)
  - `id` 获得键盘焦点的帧为 true。

- static bool FocusLost(App app, int id)
  - `id` 失去键盘焦点的帧为 true。

- static bool DoubleClicked(App app, int id)
  - `id` 上完成双击/双触的帧为 true
    （双击窗口内对同一控件的两次点击）。

- static int KeyDown(App app)
  - 本帧按键按下事件的键码，没有则为 0。（事件
    类型 4 为按键按下；键码为平台虚拟键值。）

- static bool KeyPressed(App app, int code)
  - 本帧按下指定键码的按键时为 true。

- static bool Tapped(App app, int id)
  - 触摸/指针轻点：等同于 `id` 上的完成点击。命名
    为触摸代码的清晰；单指轻点以合成点击送达。

- static int Swipe(App app)
  - 本释放帧完成的滑动/轻扫方向：0 无，
    1 左、2 右、3 上、4 下。支持鼠标拖拽与单点触摸。

- static bool SwipedOn(App app, int id, int dir)
  - 方向为 `dir`（1 左 / 2 右 / 3 上 / 4 下）的滑动
    在手势起始控件 `id` 上完成时为 true。

- static bool LongPressed(App app, int id)
  - `id` 上触发长按/长触的帧为 true（按住超过
    阈值且未大幅移动）。每次按下只触发一次。

- static bool MouseUpOn(App app, int id)
  - 在 `id` 上按下后松开按钮的帧为 true，
    （即使指针移开，mouse-up 仍送达按下所属控件）。

- static bool MovedOver(App app, int id)
  - 指针悬停 `id` 期间发生移动的帧为 true（mouse-move）。

- static bool Wheeled(App app, int id)
  - 指针在 `id` 上时滚轮帧为 true。用 WheelDelta(app)
    读取有符号格数（>0 表示向上/远离用户）。

- static int WheelDelta(App app)
  - 本帧的有符号滚轮增量（非滚轮帧为 0）。运行时
    将格数打包进滚轮事件的键码槽位。

- static bool KeyDownOn(App app, int id)
  - 本帧有按键按下且 `id` 持有焦点时为 true。用
    KeyDown(app) 读取键码。

- static int KeyUp(App app)
  - 本帧按键释放事件的键码，没有则为 0。（事件类型 5
    为按键释放；键码为平台虚拟键值。）

- static bool KeyReleased(App app, int code)
  - 本帧释放指定键码的按键时为 true。

- static bool KeyUpOn(App app, int id)
  - 焦点控件上的按键释放（事件类型 5）。用 KeyUp(app)
    读取键码。

- static bool RightClicked(App app, int id)
  - `id` 上的次键（右键）点击：右
    鼠标按钮在其按下的控件上松开时为 true。App
    只解析一次右键目标（指针下最上层），因此
    只送达一个控件，且不会触发主 Clicked。

- static bool RightPressedDown(App app, int id)
  - `id` 上按下右键的帧为 true。

- static bool SwipedAny(App app, int id)
  - 松开时，任意方向滑动在
    手势起始控件 `id` 上完成则为 true。

- static bool Dragging(App app, int id)
  - `id` 为按下目标且指针在移动时为 true（拖拽进行中）。
    与 DragStart（按下）/ Drop（松开）搭配使用。

- static bool Dropped(App app, int id)
  - 在 `id` 上按下后松开时为 true（drop / 拖拽结束）。

- static int ThemeMs(App app, int kind)
  - 交互 `kind` 的默认缓动过渡时长（ms）
    （0 悬停 / 1 按下 / 2 焦点），取自当前皮肤的动画
    令牌，使主题掌控全局交互手感。按下比悬停更干脆，
    焦点则稍慢。无主题/令牌时回退到历史
    120/80/140 ms 默认值。

- static int HoverLevel(App app, int id)
  - 缓动悬停等级（0..1000），过渡时长取主题令牌（ThemeMs kind 0）。

- static int HoverLevelMs(App app, int id, int ms)
  - 带显式过渡时长的缓动悬停等级，使控件的
    CSS `transition`（Control.styleTransitionMs）可以覆盖默认的
    120ms 交叉淡化。`ms <= 0` 时回退默认。

- static int HoverLevelMsIn(App app, int id, int ms, int x, int y, int w, int h)
  - 同 HoverLevelMs，但补间期间的动画重绘请求限定在矩形
    [x,y,w,h] 内（见 App.AnimToIn）。

- static bool HoldTipIn(App app, int id, int x, int y, int w, int h)
  - 触摸长按等价的提示门控：触摸设备上正按住 `id`、指针
    仍在矩形内且按住已达 900ms（与悬停提示阈值一致）时为真。
    桌面恒假——提示继续走悬停通道。阈值前安排低频唤醒帧，
    静止按住（没有输入事件）也能推进到阈值并绘制气泡。
    与长按菜单共存的原则：已有长按语义的区域不加此门控。

- static int PressLevel(App app, int id)
  - 缓动的“armed”等级：仅当按下且指针仍停留在控件上时为 1000，
    松开时缓动回落（比悬停更干脆）。
    缓动 armed 等级（0..1000），过渡时长取主题令牌（ThemeMs kind 1）。

- static int PressLevelMs(App app, int id, int ms)
  - 带显式过渡时长的 armed 等级（ms <= 0 回退 80ms）。

- static int PressLevelMsIn(App app, int id, int ms, int x, int y, int w, int h)
  - 同 PressLevelMs，但补间期间的动画重绘请求限定在矩形内。

- static int FocusLevel(App app, int id)
  - 缓动焦点等级（0..1000），过渡时长取主题令牌（ThemeMs kind 2）。

- static int FocusLevelMs(App app, int id, int ms)
  - 带显式过渡时长的焦点等级（ms <= 0 回退 140ms）。

- static int FocusLevelMsIn(App app, int id, int ms, int x, int y, int w, int h)
  - 同 FocusLevelMs，但补间期间的动画重绘请求限定在矩形内。

- static int LiftLevel(App app, int id, int maxPx)
  - 缓动的悬停抬升像素：静止为 0，悬停时缓动升至 `maxPx`
    （离开时回落）。悬停时按此值上移控件视觉，
    形成轻微浮起；命中区域保持静止矩形，悬停才稳定。

- static bool Activate(App app, int id, int x, int y, int w, int h)
  - 让一个矩形可交互并上报本帧激活：注册
    命中区域和焦点停靠点，然后响应指针点击或 Enter/Space
    （聚焦时）。所有可点击控件共用此逻辑，键盘激活
    与命中注册就不会被重复实现（或遗漏）。

- static void Ripple(App app, int id, int x, int y, int w, int h, int color)
  - Material 风格点击涟漪：从按下瞬间捕获的起点向外扩张并
    淡出的圆盘（480ms），裁剪在控件矩形内。仅当 `id` 是本帧
    按下目标时绘制，动画期间自行调度 16ms 重绘帧。


## UiErrorLog (class)

界面层的错误记录。一帧里抛出的异常不应该结束进程，
但也不能无声消失：异常记录在这里，落到 exe 旁边的
<c>zan_ui_errors.log</c>（硬崩溃另有原生的 <c>zan_crash.log</c>），
并留在内存环里，供「帮助与反馈」面板直接读取，
不必去翻文件。

- static int keep=100;
  - 内存里保留的最近条数（面板显示用）。

- static List<string> recent;

- static int total;

- static string lastBody="";
  - 上一条记录的正文与它连续重复的次数：一次坏帧通常每帧
    重复一次，逐条写盘会在几秒内塞满日志。

- static int repeats;

- static int Record(string origin, string message)
  - 记录一条界面错误，返回本进程累计的条数。
    <paramref name="origin"/> 是发生位置（如 "frame"、"event"）。

- static int Count()
  - 本进程记录过的错误条数。

- static List<string> Recent()
  - 最近的错误行（最旧在前）。

- static string LogPath()
  - 日志文件路径（与可执行文件同目录）。

- static void Clear()
  - 清空内存里的记录（不删日志文件）。

- static void Append(string line)
  - 写盘失败（只读目录、磁盘满）不能反过来把进程弄崩：
    内存里的记录仍然可用。


## UiEvent (class)

C# 风格的多播事件。与 `EventHub`（按键轮询）不同，
UiEvent 是控件上的一个一等字段，支持委托
<c>+=</c> / <c>-=</c> 运算符，因此注册处理器的方式与 C# 完全一致：
C#：

Button save = new Button { Text = "Save" };   // retained
save.Click += () => { Console.WriteLine("saved"); };
save.Click += Store.Commit;            // method group
// per frame:
save.Render(app, x, y, 120);           // fires Click on click

内置控件事件在 <c>Render</c> 内部触发，即在 UI 线程上，
因此处理器访问 UI 始终是安全的。要从工作线程触发，
可使用 `Post`，它会将所有处理器调度回
UI 线程的分发队列。

- List<Action> handlers;

- UiEvent()

- static UiEvent op_add(UiEvent self, Action handler)
  - 支持 <c>event += handler</c> 的运算符（追加，多播）。

- static UiEvent op_sub(UiEvent self, Action handler)
  - 支持 <c>event -= handler</c> 的运算符（移除最近的
    相同注册项；若从未添加则为空操作）。

- void Add(Action handler)
  - 注册一个处理器（等同 <c>+=</c>）。

- void Clear()
  - 清空所有处理器。

- int Count()
  - 已注册的处理器数量。

- void Raise()
  - 在当前线程上调用所有处理器。

- void RaiseIf(bool fire)
  - 仅当 <paramref name="fire"/> 为 true 时才调用处理器。

- void Post()
  - 将所有处理器调度到 UI 线程的分发队列。可从
    任何线程安全调用；处理器稍后在 UI 线程上执行（参见 App.DrainPosts）。


## UserComponentRegistry (class)

用户组件的运行期注册表。编译期展开（GenForm
ExpandRefs）覆盖设计器/声明式用法；这里是动态一侧：
应用不重编译就能按名实例化 components/*.zcomp（WinForms
UserControl 的动态加载形态）。构建用 FormBuilder.Build，
属性应用与设计器预览、生成器展开三者共用同一语义：
实例值优先，缺省取声明的 def，落到声明的目标控件上。

- static List<string> names;

- static List<string> jsons;

- static void EnsureInit()

- static void Register(string name, string json)
  - 注册/替换一个组件文档（.zcomp 原文）。

- static void SetAll(List<UserComponent> comps)
  - 批量装载（与 Designer.SetUserComponents 同源）。

- static string JsonOf(string name)
  - 组件名对应的文档原文；未注册返回 ""。

- static Control Build(string name, JsonValue instanceProps)
  - 实例化：按组件文档建整棵控件树并应用声明
    属性（无实例值时用默认值）。未注册/解析
    失败返回 null。instanceProps 键 = 声明的 key，可为 null。

- static Control Build(string name)

- static void ApplyProps(Control root, JsonValue compRoot, JsonValue instanceProps)
  - 属性应用：遍历组件文档根的 "props" 声明，
    实例值优先，缺省取 def，SetProp 到目标控件
    （按组件文档里的原始名查找）。与设计器预览
    同用此入口。


## WhyTally (class)

一条「整窗重绘理由 → 帧数」计数（参见 App.NoteFullFrameWhy）。

- string why;

- int n;

- WhyTally(string why)


## WidgetEvents (class)

常用控件事件的可复用集合。保留式控件内嵌
一个 <c>WidgetEvents</c> 字段，每帧调用一次 `Fire`
（在渲染完并注册命中区域之后），而不必手动
推导每次状态转换，应用代码因此呈声明式风格：

btn.On.Enter += () => { ... };
btn.On.Click += () => { ... };

触屏安全：在触摸屏上，单次触摸会作为合成的鼠标
事件序列到达，因此 <c>Click</c> 相当于轻点，<c>MouseDown</c>/<c>MouseUp</c> 框住
整个触摸过程；没有真正的悬停，所以 <c>Enter</c>/<c>Leave</c> 只在按压期间触发
且不会误触发。

- UiEvent Click;

- UiEvent DoubleClick;

- UiEvent RightClick;

- UiEvent MouseDown;

- UiEvent MouseUp;

- UiEvent Enter;

- UiEvent Leave;

- UiEvent Move;

- UiEvent Wheel;

- UiEvent Focus;

- UiEvent Blur;

- UiEvent KeyDown;

- UiEvent KeyUp;

- UiEvent KeyPress;

- UiEvent Tap;

- UiEvent LongPress;

- UiEvent Swipe;

- UiEvent DragStart;

- UiEvent Drag;

- UiEvent Drop;

- WidgetEvents()

- bool AddByName(string evt, Action a)
  - 将 `a` 订阅到名为 `evt` 的通用事件（该名称由
    Control.CommonEvents 返回，也用于设计器的 `on<Event>` JSON 键）。
    未知名称会被忽略，这样引用特定控件
    事件（在别处接线）的文档不会在此报错。匹配时返回 true。

- bool Any()
  - 当内置事件中至少有一个监听器时返回 true。允许
    容器跳过命中区域的注册（从而不抢占
    下方内容的指针），直到有人监听。

- void Fire(App app, int id)
  - 本帧对 `id` 满足条件的已注册处理器都会触发，
    在控件注册命中区域后每帧调用一次。
    低频/轮询驱动的事件（移动、滚轮、按键、手势、拖拽）以
    有无监听器为门槛，空闲控件无需付出开销。


## WidgetId (class)

为每个控件实例提供稳定 id 的单调递增来源。保留式控件
在工厂（Create）中领取一个 id，使身份在其整个生命周期内固定，
不受帧间兄弟控件出现或消失的影响
（弹出窗口不再导致其后所有 id 重编号）。id 从高位开始，
这样它们永远不会与旧式逐帧位置 id 冲突，
后者由 `FocusManager.AllocId` 分配。

- static int seq;

- static int frameBase;

- static int Next()
  - 新的、进程唯一的控件 id（在调用方生命周期内稳定）。

- static void Mark()
  - 将当前计数器记录为逐帧基线。即时模式
    应用应在所有保留式控件 id 分配完成后调用一次，
    （chrome、常驻控件），这样 ResetFrame() 只会回退到此处，
    绝不会重复发放已由保留式控件持有的 id。

- static void ResetFrame()
  - 将 id 计数器回退到帧基线（参见 Mark）。纯
    即时模式 UI（每帧重建控件）每帧调用一次，
    使按相同顺序绘制的控件在帧间获得相同的 id——
    否则不断递增的计数器会给每个
    重建的控件分配新 id，悬停/按压/点击（均按 id 关联）将永远
    匹配不到上一帧框架解析出的指针目标。
    保留式控件应用不得调用此方法。

- static int SeqValue()
  - 当前原始计数器。与 SetSeq 配合使用，使次级即时模式
    表面（例如渲染在同一共享计数器上的子对话框窗口）
    可以固定自己的稳定逐帧基线，之后再恢复主
    应用的计数器。

- static void SetSeq(int v)
  - 强制将计数器设为 `v`（参见 SeqValue）。子表面在渲染前设置一个固定的、
    高位基线，使其控件每帧获得相同 id
    （悬停/按压/点击按 id 关联），且不与主应用冲突。

- static int Block(int n)
  - 预留 `n` 个连续的稳定 id 并返回第一个。需要注册
    多个命中区域的控件（如 Rate 的每个星）可用它保证
    子 id 在帧间连续且稳定。


## bool (delegate)

独立泵的停止条件（返回 true 即结束 PumpStandaloneUntil 循环）。

`delegate bool ChildWindowStop();`


## int (delegate)

单元格着色委托（BandedGrid 的 RowCellStyle 等位）：返回单元格
底色 0xAARRGGBB；返回 0 表示用默认底色。

`delegate int BandGridColorOf(int row, int col, string text, int num);`


## void (delegate)

一帧的绘制体（参见 App.RunLoop / App.SafeFrame）。

`delegate void FrameBody();`


## void (delegate)

无参数的 GUI 事件处理器，类似 C# 的 <c>Action</c> / <c>EventHandler</c>。
可赋值为 lambda（<c>() => { ... }</c>）或静态方法组。

`delegate void Action();`


## void (delegate)

把一个原生浮层的可见区域下发给它的后端。`spec` 是
"x,y,w,h;x,y,w,h;..." 的矩形并集（画布坐标，与
Render 收到的矩形同一坐标系）；空串表示本帧完全被遮挡，
后端应把视图隐藏起来。

`delegate void NativeClipFn(int handle, string spec);`


## void (delegate)

进入钩子：窗口打开 / 已开重放 / 出口页构建时调用。
`win` 为承载窗口；页内出口（Embed）没有窗口，传 null。

`delegate void NavEnterHandler(NavWindow win, JsonValue args);`


## QrEcl (enum)

纠错级别（ISO/IEC 18004）。

- L = =0

- M = =1

- Q = =2

- H = =3


## Color (struct)

颜色：打包的 0xAARRGGBB 值，文本形式为 CSS。

这是值类型，因此传递无需分配内存；打包
表示是渲染器和平台层使用的格式，
并且只在那个边界通过 <c>ToArgb()</c> 产生。alpha 为
零表示“未设置”（<c>Color.None()</c>），与 CSS 的 `transparent` 及
样式层一直使用的哨兵值一致。

- uint argb;

- static Color FromArgb(uint packed)
  - 从打包的 0xAARRGGBB 值构造。

- static Color Parse(string css)
  - 解析任意 CSS 颜色形式：`#rgb`、`#rgba`、`#rrggbb`、`#aarrggbb`、
    `rgb()/rgba()`、`hsl()/hsla()`、`0x...`、十进制和命名
    颜色。空值或无法解析的值产生 <c>None()</c>。

- static Color FromRGBA(int r, int g, int b, int a)
  - 各分量 0..255 构造（超过范围按位截断）。

- static Color FromRGB(int r, int g, int b)
  - 不透明色（alpha=255）。

- static Color FromHex(int hex)
  - 0xRRGGBB 字面量，视为完全不透明。

- static Color None()
  - 未设置的颜色：不会用它绘制任何内容。

- bool IsNone()
  - 是否为“未设置”（alpha=0），绘制时会被跳过。

- int A()
  - 各分量读取（0..255）。

- int R()
  - 红分量（0..255）。

- int G()
  - 绿分量（0..255）。

- int B()
  - 蓝分量（0..255）。

- Color WithAlpha(int a)
  - 只改 alpha、保留 RGB 的新颜色。

- uint ToArgb()
  - 交给渲染器和平台层的打包值。

- int ToARGB()
  - <c>ToArgb()</c> 的旧拼写。

- string ToCss()
  - `#rrggbb`，颜色半透明时用 `#aarrggbb`。

- static string Hex2(int v)
  - 两位小写十六进制（0..255）。

- static Color White()
  - 命名色：与主题令牌无关的固定值，正式 UI 请优先用样式层语义令牌。

- static Color Black()
  - 不透明黑（0,0,0）。

- static Color Red()
  - 不透明红（208,48,80）。

- static Color Green()
  - 不透明绿（24,160,88）。

- static Color Blue()
  - 不透明蓝（32,128,240）。

- static Color Yellow()
  - 不透明黄（240,160,32）。

- static Color Gray()
  - 不透明灰（128,128,128）。
