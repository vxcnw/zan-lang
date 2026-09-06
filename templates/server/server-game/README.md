# {{NAME}} — 传奇类游戏服务端（MVC + GM 管理）

权威服务端（authoritative server）骨架：HTTP MVC 管理后台与局域网 TCP
游戏网关跑在**同一个进程**里，游戏世界是进程内内存态，由固定 tick 驱动，
落库走脏标记批量回写。适合传奇类 / ARPG 挂机 / 局域网多人等玩法二开。

框架本身不在模板里：路由、请求上下文、ORM、缓存、会话与 RBAC 都来自
标准库 `System.Web` / `System.Data.Orm`（`WebApp`、`Router`、`WebServer`、
`DbContext`、`Worker` …）。模板只保留游戏域与后台页面这些"自己的代码"。

## 架构

```
                      ┌────────────── 单进程 ──────────────┐
  浏览器 (GM) ──HTTP──▶ WebApp :8099   MVC 管理后台 + API      │
                      │   └ AppController 每请求借还连接     │
  游戏客户端 ──TCP────▶ Gateway :7100  换行 JSON，一行一消息    │
                      │        └ 未登录只许 register/login/hb│
                      │                                     │
                      │  World（内存权威态）                 │
                      │   · Session{cid, conn, row, dirty}   │
                      │   · tick(1s)：心跳超时踢线           │
                      │   · flush(10s)：脏行回写 SQLite      │
                      │   · 下线/封禁/改值 → 立即落库 + 推送  │
                      └─────────────────────────────────────┘
```

- **在线玩家以内存为准**：GM 改值、聊天、走位全部先改 `World` 里的
  `Session.row`（脏标记），由 flush 协程统一回写；GM 页与网关不会互相
  覆盖对方的写入。
- **离线玩家直改数据库**：下线即结算，登录时按 `offlineGoldPerHour`
  结算挂机收益（封顶 `offlineCapHours`），一条 UPDATE 折叠完成。
- **封禁总是立即落库**并踢在线会话（`ev kick` + 断开）。
- Zan 调度器是协作式单线程：世界状态无需加锁，唯一纪律是**不要跨
  `await` 持有半更新的状态**。
- `[worker].count` 必须为 1（`main.zan` 会强制并告警）：世界在进程内，
  多 worker 各持一份内存态就是分叉。

## 目录

```
config/app.json         运行时配置（HTTP/TCP 端口、tick、结算参数）— 不参与编译
src/main.zan            引导：Cfg → 池 → Schema → World.Start + Gateway.Start → Worker.RunAll
src/Game/Gateway.zan    TCP 网关：协议分发、注册/登录、移动/聊天/同图查询
src/Game/World.zan      世界：会话表、tick/flush 协程、改值/踢线/广播
src/Game/Session.zan    在线会话（连接 + 玩家行 + 脏标记）
src/Model/Game/         [Table] 实体：game_player / game_map / game_announce
src/Controller/Admin/Game/  GM 页：Players（玩家）/ Online（在线）/ Announces（公告）
src/Framework/Schema.zan    建表 + 种子（内置角色、5 张地图、欢迎公告）
views/Admin/Game/       GM 页视图（与控制器一一对应）
tools/e2e.py            端到端自检：HTTP 后台 + 完整 TCP 协议 + GM 流程（42 项断言）
```

## 快速开始

```bash
# 用 zanc 编译（模板是多文件工程：把 src 下所有 .zan 一起给编译器）
zanc src/main.zan src/**/*.zan --auto-stdlib -o server-game.exe
# 或者用 IDE 新建项目（模板名"游戏服务端"）后直接运行

./server-game.exe
# [game] tcp://0.0.0.0:7100
# http-worker http://0.0.0.0:8099
```

- 管理后台：`http://127.0.0.1:8099/admin`，种子账号 **admin / admin1234**。
- 数据库默认 SQLite（`data/app.db`），首次启动自动建表与种子；换 MySQL
  改 `[database]` 即可，游戏代码不感知驱动。
- 客户端**不走网页注册**：游戏账号经 TCP `register` 协议创建。

## 局域网多人

服务端两个监听都默认 `0.0.0.0`：

| 端口 | 用途 | 谁访问 |
|---|---|---|
| 8099 | HTTP 管理后台（GM 用浏览器） | 仅内网/运维段，建议防火墙不对公网放行 |
| 7100 | TCP 游戏网关 | 局域网玩家 |

- Windows 放行：`netsh advfirewall firewall add rule name="zan-game" dir=in action=allow protocol=TCP localport=7100`
- Linux 放行：`ufw allow 7100/tcp`（或对应 iptables 规则）。
- 玩家客户端连 `服务器内网IP:7100`；`[game].host` 保持 `0.0.0.0`。
- 修改端口/参数都在 `config/app.json` 的 `[game]` 段，重启生效。

## 客户端协议（TCP，换行分隔 JSON，UTF-8，单行 ≤ 8KB）

| 客户端 → 服务端 | 服务端 → 客户端 |
|---|---|
| `{"op":"register","user","pass","nick"}` | `{"ok":1,"msg"}` / `{"ok":0,"err"}` |
| `{"op":"login","user","pass"}` | `{"ok":1,"uid","self","maps","announce","offline"}` |
| `{"op":"hb"}` | `{"ok":1,"t","online"}` |
| `{"op":"state"}` | `{"ok":1,"self"}` |
| `{"op":"maps"}` | `{"ok":1,"maps"}` |
| `{"op":"move","map":2}` | `{"ok":1,"self"}` + 全服 `ev move`（地图有 `minLevel` 门槛） |
| `{"op":"walk","x","y"}` | `{"ok":1}` + 同图 `ev walk`（坐标钳到 `walkMax`） |
| `{"op":"say","text"}` | `{"ok":1}` + 全服 `ev chat`（≤200 字） |
| `{"op":"who"}` | `{"ok":1,"rows":[同图玩家]}` |

服务端主动推送：`ev chat / walk / move / announce / kick`（踢线后断开）、
`ev online`（tick 每 30 秒在线数）。密码散列与管理后台同一套（`AuthUser`）。

用 `nc` 就能当客户端试：

```
$ nc 127.0.0.1 7100
{"op":"register","user":"bob","pass":"bob12345","nick":"小明"}
{"op":"login","user":"bob","pass":"bob12345"}
{"op":"say","text":"大家好"}
{"op":"walk","x":10,"y":10}
```

## GM 管理后台

侧边栏"游戏管理"分节（`MenuBuilder.Section("game", ...)`），三个页面：

- **玩家管理** `/admin/game/players`：搜索/状态过滤；编辑金币/元宝/等级/
  职业/地图/昵称；封禁/解封（填原因）；踢线。在线玩家显示实时值，保存
  走 `World.ApplyEdit/Adjust` 增量改内存并即时推送；离线玩家直改数据库。
- **在线管理** `/admin/game/online`：会话快照（账号/等级/地图/空闲时长），
  按 cid 踢线，全服广播（署名 GM）。
- **公告管理** `/admin/game/announces`：CRUD + 推送（`ev announce` 推给
  所有在线会话，停用状态的公告不允许推）。

权限沿用 RBAC：内置角色 `gm`（游戏运营）只授 `/admin/game/*` 屏，
`admin` 全量；新 GM 页只要控制器方法带 `[Route]` + `[Custom(IsMenu)]`
就会出现在侧边栏与授权表里，启动时 `SyncRoleGrants` 自动补发。

## 持久化模型

| 时机 | 行为 |
|---|---|
| 每 `flushSeconds`（默认 10s） | 脏会话回写：level/gold/gems/mapId/x/y/updatedAt |
| 下线 | 立即回写 + 记 `lastLogoutAt` |
| 登录 | 按离线时长结算挂机收益，与 `lastLoginAt` 合并为一条 UPDATE |
| 封禁 | 立即 UPDATE + 在线则 `ev kick` 踢线 |

`game_player / game_map / game_announce` 三张表由 `Schema.Ensure` 建表，
种子地图五张（新手村→赤月峡谷，`minLevel` 递增），改玩法先改这里。

## 配置 `[game]`

```json
"game": {
  "host": "0.0.0.0",   "port": 7100,
  "tickMs": 1000,
  "kickSeconds": 90,
  "flushSeconds": 10,
  "offlineGoldPerHour": 500,
  "offlineCapHours": 12,
  "walkMax": 511
}
```

- `tickMs`：世界 tick 周期（心跳超时检查、定时推送的节拍）。
- `kickSeconds`：多久没心跳算掉线并踢出。
- `flushSeconds`：脏会话回写数据库的周期。
- `offlineGoldPerHour` / `offlineCapHours`：挂机结算速率与封顶。
- `walkMax`：走位坐标上限（服务端钳位，客户端不可信）。

## 端到端自检

`tools/e2e.py`（标准库 urllib/socket，无第三方依赖）对运行中的服务端跑
42 项断言：HTTP 后台登录/权限、TCP 注册/登录/心跳/地图/走位/聊天/同图
查询、GM 加币/升级/封禁/踢线的实时推送、公告推送、tick 回写落库、离线
结算封顶。在服务端目录里运行（它会读 `data/app.db` 验证落库），跑之前
删掉 `data/app.db*` 重启服务端，保证注册流程从空表开始；用法详见文件头。

## 二次开发

- **加一个协议 op**：`Gateway.Handle` 的 `op == "..."` 分发链上加分支，
  广播用 `Gateway.Broadcast` / `PushChat`，改值走 `World.Adjust`。
- **加一张地图**：`Schema.SeedGame` 加一行（`minLevel` 控制进入门槛），
  客户端 `op:maps` 与 GM 页自动带出。
- **加一个 GM 页**：拷 `Controller/Admin/Game/Announces.zan` 的骨架，
  `[Table]` 实体 + `Index/Form/Save` + 同名视图即可，权限与侧边栏自动。
- 玩法升级（战斗、背包、组队）都在 `src/Game/` 里长，保持同一条纪律：
  在线态改内存打脏标记，落库交给 flush；不要在协议线程里直接写库。
