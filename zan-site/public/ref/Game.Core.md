# Game.Core

> 源码: `stdlib/Game/Core/Anim.zan`


## AnimClip (class)

基于方向优先帧表的单个动画片段（
Mir 式布局：先是方向 0 的全部帧，再是方向 1，……）。
由 IDE 资源管理器写入的 `.anim` 旁置 JSON 加载。

- string image;

- int frameW;

- int frameH;

- int baseFrame;

- int dirs;

- int framesPerDir;

- int fps;

- int loopMode;

- int loopStart;

- AnimClip(int dirs, int framesPerDir, int fps, int loopMode, int loopStart)

- static AnimClip ParseJson(string json)
  - 解析 `.anim` JSON 文档；不是该格式则返回 null。

- static AnimClip Load(string path)
  - 从磁盘上的 `.anim` 文件加载片段（失败返回 null）。

- string Image()
  - 帧表图片条目/路径（`.anim` 的 image 字段，默认空串）。

- int Base()
  - 多动作帧表中该动作的首帧（`.anim` 的 base 字段）。

- int FrameW()
  - 帧单元宽（0 = 未知，从帧表推导）。

- int FrameH()
  - 帧单元高（0 = 未知，从帧表推导）。

- int Dirs()
  - 方向数量（构造时小于 1 钳制为 1；经典 Mir 移动为 8）。

- int FramesPerDir()
  - 每个方向的帧数（构造时小于 1 钳制为 1）。

- int Fps()
  - 播放帧率（FPS，构造时小于 1 钳制为 1）。

- int LoopMode()
  - 循环模式：0 播放一次，1 循环，2 循环片段。

- int LoopStart()
  - 循环片段（模式 2）的首帧（钳制在 [0, framesPerDir-1]）。


## AnimPlayer (class)

播放 AnimClip：按流逝毫秒推进，可随时切换
朝向（帧位置保持不变，与经典 Mir 渲染器一致），
并读回帧表中要绘制的绝对帧。
循环模式：once（停在最后一帧，Done() 变为 true）、loop（回到
0）、section（先播放 0..loopStart-1 的前奏一次，再循环
loopStart..末尾——例如施法前摇后接持续施法）。

- AnimClip clip;

- int dir;

- int frame;

- int accMs;

- bool done;

- AnimPlayer()

- void Play(AnimClip c)
  - 从第 0 帧开始（或重新开始）播放片段，保持当前朝向。

- void SetDir(int d)
  - 切换朝向；片段内帧位置保持不变，
    转身的角色不会重新开始步伐。

- int Dir()
  - 当前朝向（0..dirs-1，SetDir 已归一化）。

- bool Done()
  - once 模式片段是否已停在最后一帧；循环片段恒为 false。

- int Frame()
  - 当前方向内的帧索引（0..framesPerDir-1）。

- void Update(int dtMs)
  - 按流逝毫秒推进。

- int SheetFrame()
  - 当前朝向与位置在帧表中的绝对帧索引
    ：base + dir * framesPerDir + frame。
