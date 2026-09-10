# Game.Foundation

> 源码: `stdlib/Game/Foundation/Input.zan`, `stdlib/Game/Foundation/Scene.zan`, `stdlib/Game/Foundation/Timing.zan`


## DeterministicRandom (class)

小型可复现随机源（PCG 线性同余变体），状态对外暴露——保存
state 即可完整恢复随机序列，用于存档、确定性回放与网络同步。
同一种子的序列永远一致；种子 0 视为 1（避免全零序列）。

- long state;

- DeterministicRandom(long seed)
  - 用种子构造；种子 0 自动改为 1。

- long NextRaw()
  - 原始 64 位 LCG 状态推进（含符号位，可直接做哈希/噪声）。

- long Next()
  - 非负 64 位随机数（0..2^63-1）。

- int NextBelow(int bound)
  - [0, bound) 的随机整数；bound≤0 返回 0。

- int Between(int minimum, int maximumExclusive)
  - [minimum, maximumExclusive) 的随机整数；
    上界不大于下界时恒返回 minimum。

- double NextDouble()
  - [0,1) 的随机小数（精度 1e-6）。

- long State()
  - 当前 LCG 状态（存档这个值即可完整恢复序列）。

- void Restore(long state)
  - 恢复到指定状态（0 自动改为 1），后续序列与保存时一致。


## FixedStepClock (class)

确定性固定步长累加器。每帧 Advance(真实帧间隔)，然后在
HasStep() 为真时反复 ConsumeStep() 驱动模拟；渲染插值用
Alpha()。单帧补步数有上限（防死亡螺旋），时间缩放只影响
累加速度。

- int stepMilliseconds;

- int maxStepsPerFrame;

- int accumulator;

- int pendingSteps;

- bool paused;

- double timeScale;

- FixedStepClock(int stepMilliseconds, int maxStepsPerFrame)

- int Advance(int deltaMilliseconds)
  - 累加一帧的真实毫秒数并换算成本帧待执行的固定步数。
    缩放后的时间超过 步长×每帧上限 时截断（补步最多
    maxStepsPerFrame 个），避免卡顿后一帧内狂补模拟。
    暂停中或 delta≤0 返回 0。每次调用会先清空上次余量。

- bool HasStep()
  - 本帧是否还有未消费的固定步。

- int ConsumeStep()
  - 消费一个固定步，返回其毫秒数（恒等于步长，供模拟代码
    做确定性积分）；无步可消费时返回 0。

- int StepMilliseconds()
  - 固定步长毫秒数（构造时 ≤0 钳为 16）。

- int PendingSteps()
  - 本帧剩余待执行的固定步数。

- double Alpha()
  - 渲染插值系数：accumulator/步长，0..1。渲染时用
    前后两次模拟状态按 alpha 混合可消除固定步的颗粒感。

- void SetPaused(bool paused)
  - 暂停/恢复累加（暂停时 Advance 直接返回 0）。

- bool Paused()
  - 是否暂停中。

- void SetTimeScale(double scale)
  - 时间流速倍率，影响 Advance 的累加速度（0=冻结，1=正常，
    2=两倍速）。超出 [0,8] 钳到边界；不影响已累计的余量。

- double TimeScale()
  - 当前时间流速。

- void Reset()
  - 清零累计余量与待执行步数（不影响暂停/流速设置）。


## GameTimer (class)

可复用的一次性或循环毫秒定时器。

- int duration;

- int remaining;

- bool repeating;

- bool running;

- int triggers;

- static GameTimer Once(int durationMilliseconds)
  - 创建一次性定时器（触发一次后自动停止）。

- static GameTimer Repeating(int intervalMilliseconds)
  - 创建循环定时器（按间隔反复触发）。

- GameTimer(int durationMilliseconds, bool repeating)

- int Tick(int deltaMilliseconds)
  - 推进定时器并返回本次触发的次数（一帧可能触发多次）。
    每次调用都会重置触发计数。已停止或 delta≤0 返回 0；
    一次性定时器触发后自动停止。

- void Restart()
  - 重置到满时长并恢复运行（触发计数清零）。

- void Stop()
  - 停止定时器（Restart 可再启动）。

- bool Running()
  - 是否运行中。

- int Remaining()
  - 距下次触发的剩余毫秒。

- int Duration()
  - 定时时长/循环间隔毫秒（构造时 ≤0 钳为 1）。

- int Triggers()
  - 最近一次 Tick 的触发次数。


## InputActionState (class)

单个语义动作的运行时状态。pressed/released 是边沿标志：
Set 只在按下的转换沿置位，之后保持锁存，直到 BeginFrame 清除，
因此每帧开头必须调用一次 BeginFrame 才能读到正确的边沿。

- string name;

- bool down;

- bool pressed;

- bool released;

- double amount;

- InputActionState(string name)

- string Name()
  - 动作名，即创建时的标识符。

- bool Down()
  - 当前是否处于按住状态（持续为 true，非边沿）。

- bool Pressed()
  - 本帧内是否发生了按下动作；锁存直到 BeginFrame。

- bool Released()
  - 本帧内是否发生了抬起动作；锁存直到 BeginFrame。

- double Value()
  - 模拟量强度（键盘按下为 1.0，抬起时清零）。

- void BeginFrame()
  - 清除 pressed/released 边沿标志；每帧开头调用一次。

- void Set(bool down, double amount)
  - 更新状态并做边沿检测：down 从 false 变 true 置 pressed，
    从 true 变 false 置 released 并将强度清零。


## InputBinding (class)

一个"动作-按键"绑定项；用静态 Key 工厂创建。

- string action;

- int key;

- bool down;

- static InputBinding Key(string action, int key)
  - 创建绑定：动作名 + 后端按键码。

- string Action()
  - 绑定的动作名。

- int KeyCode()
  - 绑定的后端按键码。

- bool Down()
  - 该按键当前是否按住。

- void SetDown(bool down)
  - 由 InputMap 内部更新；一般不必直接调用。


## InputMap (class)

将后端按键码映射为语义动作。多个按键可对应同一个
动作，直接调用 SetAction 则支持触摸、手柄或 AI 输入。

- List<InputActionState> actions;

- List<InputBinding> bindings;

- InputMap()

- int ActionIndex(string name)
  - 动作的下标；不存在返回 -1。

- InputActionState EnsureAction(string name)
  - 取动作状态，不存在则先创建（首次查询即注册）。

- InputMap BindKey(string action, int key)
  - 绑定按键到动作，可链式调用；同名动作可绑定多个键。

- void BeginFrame()
  - 清除所有动作的 pressed/released 边沿；每帧开头调用。

- void ProcessKey(int key, bool down)
  - 后端按键事件入口：key 变化时刷新其绑定的所有动作。
    多键绑定同一动作时任一键按住即视为按下（OR 逻辑）。

- void RefreshAction(string action)
  - 按全部绑定重算动作状态；供 ProcessKey 内部调用。

- void SetAction(string action, bool down, double amount)
  - 直接设置动作状态：触摸、手柄、AI 等非键盘输入的入口，
    amount 为模拟量强度（键盘路径固定 1.0）。

- bool Down(string action)
  - 动作当前是否按住；未注册的动作返回 false。

- bool Pressed(string action)
  - 动作本帧是否按下过（边沿，锁存到 BeginFrame）。

- bool Released(string action)
  - 动作本帧是否抬起过（边沿，锁存到 BeginFrame）。

- double Value(string action)
  - 动作的模拟量强度；未注册的动作返回 0。

- void Clear()
  - 清空全部输入：所有绑定与动作复位为未按下。


## SceneStack (class)

基于栈的游戏状态管理者，用于菜单、加载画面、游戏过程、暂停
覆盖层与结算画面。

- List<IGameScene> scenes;

- SceneStack()

- void Push(IGameScene scene)
  - 压入新场景：旧栈顶 Pause，新场景 Enter 后成为栈顶。
    null 直接忽略。

- IGameScene Pop()
  - 弹出栈顶场景（收到 Exit）并返回它；下层场景收到 Resume。
    栈空时返回 null 且无副作用。

- void Replace(IGameScene scene)
  - 弹出当前栈顶并压入新场景（旧栈顶 Exit、新场景 Enter）。

- IGameScene Current()
  - 当前栈顶场景；栈空返回 null。

- int Count()
  - 栈中场景数。

- void FixedUpdate(int deltaMilliseconds)
  - 把固定步长更新转发给栈顶场景（栈空时忽略）。

- void Update(int deltaMilliseconds)
  - 把每帧更新转发给栈顶场景（栈空时忽略）。

- void Clear()
  - 依次弹出全部场景（每个都收到 Exit），清空栈。


## IGameScene (interface)

栈式场景生命周期契约：只有栈顶场景接收 FixedUpdate/Update
（由 SceneStack 转发）。Push 时旧栈顶收到 Pause、本场景收到
Enter；Pop 时本场景收到 Exit、新栈顶收到 Resume。

- string Name();
  - 场景名（用于调试与存档定位）。

- void Enter();
  - 进入场景（Push/Replace 压入时调用一次）。

- void Exit();
  - 退出场景（Pop/Replace 弹出时调用一次）。

- void Pause();
  - 被新场景覆盖时调用（保持状态但不接收更新）。

- void Resume();
  - 覆盖场景弹出后恢复时调用。

- void FixedUpdate(int deltaMilliseconds);
  - 固定步长模拟回调，仅栈顶场景收到。

- void Update(int deltaMilliseconds);
  - 每帧可变更新回调，仅栈顶场景收到。
