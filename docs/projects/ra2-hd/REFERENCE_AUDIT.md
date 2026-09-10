# 参考引擎界面还原对账本（参考引擎 ↔ Zan 模板）

**对照基准（权威）**：`_scratch/reference-ra2/redalert2/src/`（TypeScript 参考引擎）
**还原目标**：`templates/game/ra2/src/`（Zan 实现）
**素材根**：`D:\project\Ra2\data\`（YR 整合版：ra2md.mix / rulesmd.ini / ra2md.csf），
运行 exe 需从该目录启动（`DataDir()` 相对 cwd 找 `data/`）。

**用户拍板（本轮定调）**：**全部以参考引擎为准**，现有零售版实现本身是错的、要推翻重做。

---

## 素材可用性实测（`_scratch/ra2_shell_probe.exe`）

用 `AssetDb.MountInstall("data")` 挂 37 个档案后逐名哈希探测。**HIT = 渲染器能按同一查找路径取到**。

### 主菜单/壳层素材——全部就位

| 素材 | 结果 | 用途（参考引擎证据） |
|---|---|---|
| `MNSCRNL.SHP` | HIT 359008 | 主画面底图 `MainMenu.ts:253` |
| `LWSCRNL.SHP` | HIT 20256 | 状态条 + 工具提示宿主 `MainMenu.ts:254,281-285` |
| `SDTP.SHP` | HIT 66920 | 右栏底板，**frame 0=收起/1=展开** `SidebarPreview.tsx:60` |
| `SDWRNANM.SHP` | HIT 446272 | 右栏动画 `SidebarPreview.tsx:76-83` |
| `SDWRNTMP.SHP` | HIT 178568 | 右栏滑入覆盖层 `SidebarPreview.tsx:70-75` |
| `SDBTNBKGD.SHP` | HIT 7088 | 按钮槽底板（**槽数 = floor(高/此高)**）`MainMenu.ts:317` |
| **`SDBTNANM.SHP`** | **HIT 111800** | **按钮 17 帧状态机 `MainMenu.ts:344-349`** ← 现用 MNBTTN 是错的 |
| `SDBTM.SHP` | HIT 10952 | 槽底封盖（**需按剩余高度裁剪**）`MainMenu.ts:319-320` |
| **`SDMPBTN.SHP`** | **HIT 74896** | **MP 槽 `MainMenu.ts:332-343`** |
| `SHELL.PAL` / `SHELL2.PAL` / **`SDBTNANM.PAL`** | HIT 768 ×3 | 对应调色板 |

### 对局内 HUD 素材——全部就位

`CREDITS.SHP` `TOP.SHP` `RADAR.SHP` `SIDE1/2/2B/3.SHP` `ADDON.SHP` `POWERP.SHP`
`GCLOCK2.SHP` `SIDEBTTN.SHP` `SIDEBAR.PAL` `SIDEC01.MIX` `SIDEC02.MIX` 全部 HIT。
命令条：`LENDCAP.SHP` `RENDCAP.SHP` `BTTNBKGD.SHP` 全 HIT。
结算：**`GRFXTXT.SHP` HIT 195432 + `GRFXTXT.PAL` HIT** —— 结算图可直接换真素材。

### 真缺失（本整合版没有，需回退）

| 素材 | 说明 |
|---|---|
| `RADARY.SHP` / `RADARY.PAL` | 尤里雷达罩。本版是 RA2 系（非 YR 完整），尤里侧继续用苏联罩 |
| `LS800*.PCX`（ALLIED/SOVIET/YURI/OBS） | YR 新增载入底图；`LOAD.PCX` HIT，沿用现有回退 |

---

## 已确认的架构性错误（用户定调后全部要改）

| ID | 错误 | 参考证据 | Zan 现状 |
|---|---|---|---|
| A1 | **主菜单按钮清单是零售版，不是参考引擎的** | `HomeScreen.ts:47-159`：Skirmish / Load Game / Live Interaction / Replays / LAN Multiplayer / Mods / Info & Credits / Options / Test Tools / Fullscreen | `Screens.zan:612-620` 硬编码 单人游戏/网际网络/网络对战/影片与制作群/选项/退出游戏 |
| A2 | **按钮精灵用错** | `sdbtnanm.shp`+`sdbtnanm.pal`，17 帧 `MainMenu.ts:316,346` | `Screens.zan:735-737` 用 MNBTTN.SHP 3 帧；实测 `sidebttn frames=3 125x25` |
| A3 | **悬停无反馈**（主路径） | `MenuSlotAnimationRunner.ts:85-93` Unlit=1/Normal=2/Active=4 | `Screens.zan:642-644` 算出 `hov` 后丢弃，从不传给 `DrawSdbtnanm` |
| A4 | **无滑入/滑出动画** | `MainMenu.ts:165-183` + 帧 5-10/11-16 | 静态绘制，无折叠态 |
| A5 | **无版本号** | `VersionString.tsx` + `MainMenu.ts:295-301` y=`sidebarViewport.height-20` | 完全没有 |
| A6 | **无悬停工具提示** | `MenuTooltip.tsx:18-23` + `data-r-tooltip` | 只有静态 `STT:MainHint` 一行 |
| A7 | **单人页是自创屏** | 参考 `src/gui/screen/` 全树**无** SinglePlayer 屏；`ScreenType.ts` 20 项无此项 | `Shell.zan:18` `Scene.SinglePlayer()` + `Screens.zan:1744` |
| A8 | **遭遇战→单人→主菜单"零售顺序"不成立** | `HomeScreen.ts:55` Skirmish 是**顶层**入口 | `Shell.zan:307-310`、`main.zan:3153-3158` 断言零售顺序 |
| A9 | **无屏幕栈** | `Controller.ts:41-76` pushScreen/popScreen + onStack/onUnstack | `Shell.zan:252-266` 单个 int + 硬编码 if 链 |
| A10 | **壳层被缩放** | `UiScene.ts:82-96` menuViewport **固定 800x600 不缩放** | `BlitShell` 全部按 `bw/800,bh/600` 缩放（1280x720 下 1.2× 重采样） |
| A11 | **注释引用幽灵文件** | `ui_layout.rs`/`ui_slots.rs`/`compose_main_menu_page` 全树 0 匹配 | `Screens.zan:15,431-434,536-537,806-810,1740` |
| A12 | **载入进度是假的** | `SpLoadingScreenApi.ts:75-81` 真进度 ← GameLoader | `main.zan:2065-2078` `pct=loadFrames*4`，恒 25 帧 |

## 对局内 HUD 差距（32 项，详表见下）

缺大功能：命令条(M20)、超级武器(M31)、游戏时间(M7)、消息面板(M26)、
基地级四页签(M9)、雷达罩动画+尤里雷达(M3/M4/M5)。
渲染错误：小地图拉伸(M1)、结算用文字且 result 映射错位(M23)、
幂带行数差一(M32)、菜单几何取错 SHP(M29)、菜单留下壳层空洞(M30)。
数学错误：电力 pips 无对数曲线(M15)、无 pips 动画(M16)、队列数/进度钟(M13/M14)。

## 遭遇战设置屏差距（详表见下）

M1 队伍列缺失、M2 起始点列缺失、M3 列序只到 2 列、M4 **选图是死桩**、
M5 无地图列表 UI、M6 预览无 contain/无出生点编号、M7 资金滑轨区间错、
M8 **9 个复选框只画 4 个**、M10 AI 难度词汇不全、M11 槽位是循环非下拉、
M12 AI 行无阵营配色、M14 颜色无随机项、M16 侧栏显示文件名非地图标题、
M17 无开局校验。**根因**：正文按臆造的 DLU 布局手写，而非照 `LobbyForm.tsx`。

---

## 执行顺序（按用户选定的四个方向）

1. **壳层底座**：A10 固定 800x600 不缩放 + A2 换 SDBTNANM + A3 悬停 + A4 滑入动画
   + A5 版本号 + A6 工具提示 → 主菜单质感
2. **A1/A7/A8/A9**：主菜单清单改参考引擎、去掉自创单人页、引入屏幕栈
3. **遭遇战补齐**：M1-M3 列、M8 复选框、M4/M5 选图屏、M6 预览、M7 滑轨
4. **对局 HUD**：按 M1-M32 优先级推进
5. **载入链**：A12 真实进度 + 玩家列表
