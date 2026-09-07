# {{NAME}} — 传奇类游戏服务端（区服 + MVC 管理 + 网页注册）

权威服务端（authoritative server）骨架：HTTP 站点（玩家注册/找回密码 +
GM 管理后台）与局域网 TCP 游戏网关跑在**同一个进程**里，游戏世界是进程内
内存态，由固定 tick 驱动，落库走脏标记批量回写。区服（服务器分区）是
一等公民：玩家用账号登录，**每个区服一个角色**，聊天/走位/同图查询按区
收窄。适合传奇类 / ARPG 挂机 / 局域网多人等玩法二开。

框架本身不在模板里：路由、请求上下文、ORM、缓存、会话与 RBAC 都来自
标准库 `System.Web` / `System.Data.Orm`（`WebApp`、`Router`、`WebServer`、
`DbContext`、`Worker` …）。模板只保留游戏域与页面这些"自己的代码"。

## 账号 / 角色 / 区服

| 表 | 粒度 | 内容 |
|---|---|---|
| `game_account` | 全局唯一 | 用户名、密码散列、密保问题+答案散列、错误次数限频、封禁状态 |
| `game_realm` | 区服 | 名称、state（0=开放 / 1=维护）、排序 |
| `game_player` | 账号×区服 | 角色（昵称区内唯一、职业、等级、血量/经验、武器/防具装备位、金币元宝、坐标）、离线结算时间戳 |
| `game_mob` | 刷怪点模板 | 怪物（等级/四维/经验/金币区间/重生秒数/数量/掉落物+万分比概率）；怪**实例**只存内存，不落库 |
| `game_item` | 物品模板 | kind（0 消耗品 / 1 武器 / 2 防具 / 3 材料）、atk/def/回复量、售价、等级门槛；材料只掉落卖店，是打金出口 |
| `game_bag` | 账号×区服×物品 | 背包行（同物品合并计数）；在线以内存为准，flush/下线整包重写 |

- 一账号在**每个区服至多一个角色**；换区服先退当前世界（落库），再挂
  新区的角色，金币/等级随角色走。
- 封禁是**账号级**：封禁后该账号所有区服都无法登录；在线会话立即踢。
- 维护中的区服拒绝 `enter` / `create`，GM 在后台一键开放/维护。

## 架构

```
                      ┌────────────── 单进程 ──────────────┐
  玩家浏览器 ──HTTP──▶ WebApp :8099   / 首页(区服列表)      │
                      │   · /register 网页注册             │
                      │   · /forgot 找回密码（三步密保）     │
                      │   · /admin GM 后台                 │
  游戏客户端 ──TCP────▶ Gateway :7100  换行 JSON，一行一消息 │
                      │        └ 流程：register → login →  │
                      │          realms → create/enter     │
                      │                                     │
                      │  World（内存权威态，按区收窄）        │
                      │   · Session{cid, conn, accountId,   │
                      │     realmId, row, dirty}            │
                      │   · tick(1s)：心跳超时踢线、怪重生、  │
                      │     自动挂机回合（ev fight 推送）      │
                      │   · flush(10s)：脏行回写 SQLite      │
                      │   · 下线/封禁/改值 → 立即落库 + 推送  │
                      └─────────────────────────────────────┘
```

- **在线玩家以内存为准**：GM 改值、聊天、走位全部先改 `World` 里的
  `Session.row`（脏标记），由 flush 协程统一回写；GM 页与网关不会互相
  覆盖对方的写入。
- **离线结算发生在进区时**：角色表的 `lastLogoutAt` 起算，按
  `offlineGoldPerHour` **按秒折算**挂机收益（封顶 `offlineCapHours`），
  进区回复带 `offline:{seconds, gold}` 摘要，与 `lastLoginAt` 合并为一条
  UPDATE。
- **封禁总是立即落库**并踢在线会话（`ev kick`；协议约定客户端收到后
  自行断开，服务端在该连接下一条消息后收口）。
- Zan 调度器是协作式单线程：世界状态无需加锁，唯一纪律是**不要跨
  `await` 持有半更新的状态**。
- `[worker].count` 必须为 1（`main.zan` 会强制并告警）：世界在进程内，
  多 worker 各持一份内存态就是分叉。

## 目录

```
config/app.json         运行时配置（HTTP/TCP 端口、tick、结算参数）— 不参与编译
src/main.zan            引导：Cfg → 池 → Schema → World.Start + Gateway.Start → Worker.RunAll
src/Game/Gateway.zan    TCP 网关：协议分发、注册/登录/找回、选区建角、世界交互
src/Game/World.zan      世界：会话表、tick/flush 协程、改值/踢线/按区广播
src/Game/Fight.zan      战斗闭环：怪/物品模板缓存、刷怪与挂机 tick、回合结算、背包/商店/穿戴
src/Game/Session.zan    在线会话（连接 + 账号 + 区服 + 角色行 + 脏标记）
src/Model/Game/         [Table] 实体：game_account / game_realm / game_player / game_map /
                        game_announce / game_mob / game_item / game_bag
src/Dao/Game/AccountDao.zan   账号读写唯一入口：注册/验密/密保散列/限频/封禁（网页与 TCP 共用）
src/Controller/Account/     玩家网页：Register（注册）/ Forgot（找回密码三步）
src/Controller/Index/       首页：区服列表（开放/维护、实时在线）+ 注册/找回入口
src/Controller/Admin/Game/  GM 页：Realms（区服）/ Players（角色）/ Online（在线）/ Announces（公告）
src/Framework/Schema.zan    建表 + 种子（3 区服、内置角色、5 图、13 种物品、6 个刷怪点、欢迎公告）
views/                  视图（与控制器一一对应；Account/Index/Admin 三套布局）
tools/e2e.py            端到端自检：注册/找回 + 完整协议 + GM + 战斗闭环（114 项断言）
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

- 玩家网页：`http://127.0.0.1:8099/` — 区服列表 + **注册账号** +
  **找回密码**；注册即建 `game_account`，之后连 TCP 网关进游戏。
- 管理后台：`http://127.0.0.1:8099/admin`，种子账号 **admin / admin1234**。
- 数据库默认 SQLite（`data/app.db`），首次启动自动建表与种子；换 MySQL
  改 `[database]` 即可，游戏代码不感知驱动。

## 完整玩家流程（前后端都通）

1. **注册**：网页 `/register`（用户名 3-32 字、密码 6-64 字、密保问题/
   答案 2-50 字）或 TCP `register` —— 同一套校验与散列（`AccountDao`）。
2. **登录**：TCP `login` 拿 `uid` + 区服列表（含各区实时在线数）；同账号
   重复登录**顶号**（旧连接收 `ev kick`）。封禁账号拒绝并带原因。
3. **找回密码**：网页 `/forgot` 三步（账号 → 密保问题 → 新密码），TCP 走
   `forgot` / `reset` 两个 op —— 行为一致；答错 5 次锁 1 小时
   （`AnswerLimit` / `AnswerWindowSec`），锁定期连正确答案也拒绝。
4. **创建角色**：TCP `create`（昵称 2-16 字区内唯一、职业 0 战士/1 法师/
   2 道士）；每区一角色，重复创建答 `该区已有角色`。
5. **进区游玩**：`enter` 进世界（维护区拒绝）；此后 `say`/`walk`/`who`
   只在**本区同图**内生效，`move` 过图有 `minLevel` 门槛。
6. **战斗闭环**：`mobs` 看怪 → `hunt` 手动回合 → 经验升级/金币/掉落入包 →
   `shop`/`buy`/`sell` 买卖 → `use` 嗑药、`equip`/`takeoff` 穿脱 → `auto`
   挂机（每 tick 一回合推 `ev fight`）→ 死亡回城半血重开。

## 战斗闭环（刷怪 → 战斗 → 掉落 → 成长 → 商店 → 死亡回城）

`src/Game/Fight.zan` 一个文件装下整条链路，全部确定性数值（不掷骰），
只有金币区间与掉落概率用随机：

- **刷怪**：`game_mob` 一行 = 一个刷怪点（模板 + 数量）。启动时按
  `count` 生成实例（只存内存并行表），被杀后 `respawnSec` 秒重生；
  怪物只在 `move` 过图后的当前地图可见/可打。
- **回合**：玩家先手，`Damage = max(1, atk - def)`；怪没死就还手一下。
  攻防血全部由等级/职业/装备推导：`atk = 6 + 等级×2 + 职业加成
  （战 5 / 法 3 / 道 2）+ 武器 atk`，`def = 1 + 等级 + 防具 def`，
  `maxhp = 40 + 等级×20 + 职业血量（战 20 / 法 8 / 道 12）`。
- **成长**：击杀得 `exp`，`ExpNext(级) = 15×级`，连升循环推 `ev levelup`；
  金币在模板区间内随机，掉落按万分比 `dropRate` 判定入包并推 `ev drop`。
- **打金闭环**：材料（兽皮/蝎子壳/祖玛头像…）不可购买只能卖店
  （半价、下限 1 金）→ 换钱买药/买装备 → 打更高级的怪。新手图稻草人
  `dropRate=10000` 首杀必掉，入门丝滑。
- **挂机**：`auto` 挂上模板 id 后，每 `tickMs` 世界拍给在线会话打一
  回合并推 `ev fight`，关掉或下线即停；跨图自动暂停（找不到目标静默
  空转），回到怪的地图续打；被踢会话不参与 tick。
- **死亡**：`hp<=0` 立即回新手村（地图 1），保留一半血量、关闭挂机，
  推 `ev die`；不掉装备不掉级，死亡惩罚留给二开。GM 改等级会把血量
  钳到新上限（升不溢出、降不悬空）。
- **背包**：在线态是会话里的并行表（同物品合并计数），`bagDirty` 由
  flush 整包重写；`use`/`equip`/`takeoff`/`buy`/`sell`/GM 发放都走
  同一套 `BagAdd/BagTake`，穿上的装备不在背包里（装备位在角色行）。

## 客户端协议（TCP，换行分隔 JSON，UTF-8，单行 ≤ 8KB）

会话分两段：`register/login/forgot/reset/realms/hb` 无需登录；
`characters/create/enter` 需已登录；`state/maps/move/walk/say/who`
需已进区（否则答 `请先选择区服进入（enter）`）。

| 客户端 → 服务端 | 服务端 → 客户端 |
|---|---|
| `{"op":"register","user","pass","question","answer"}` | `{"ok":1,"msg"}` / `{"ok":0,"err"}` |
| `{"op":"login","user","pass"}` | `{"ok":1,"uid","realms"}` |
| `{"op":"forgot","user"}` | `{"ok":1,"question"}` / 与不存在账号同一句错误 |
| `{"op":"reset","user","answer","newpass"}` | `{"ok":1,"msg"}`（限频内） |
| `{"op":"realms"}` | `{"ok":1,"realms":[{id,name,state,online}]}` |
| `{"op":"characters","realm":1}` | `{"ok":1,"rows":[{id,name,level,job}]}` |
| `{"op":"create","realm":1,"name","job"}` | `{"ok":1,"self","maps","announce"}` |
| `{"op":"enter","realm":1}` | `{"ok":1,"self","maps","announce"[,"offline"]}`<br>`{"ok":0,"err":"该区还没有角色，请先创建","needCreate":1}` |
| `{"op":"hb"}` | `{"ok":1,"t","online"}` |
| `{"op":"state"}` | `ev state`（见推送） |
| `{"op":"maps"}` | `{"ok":1,"maps"}` |
| `{"op":"move","map":2}` | `{"ok":1,"self"}` + 本区 `ev move`（地图有 `minLevel` 门槛） |
| `{"op":"walk","x","y"}` | `{"ok":1}` + 本区同图 `ev walk`（坐标钳到 `walkMax`） |
| `{"op":"say","text"}` | `{"ok":1}` + 本区 `ev chat`（≤200 字，超长截断） |
| `{"op":"who"}` | `{"ok":1,"rows":[同图同区玩家]}` |
| `{"op":"mobs"}` | `{"ok":1,"rows":[当前地图怪（含未重生的 respawnIn）]}` |
| `{"op":"hunt","mob":tpl}` | `{"ok":1,"fight","self"}`（一回合：dmg/mdmg/killed/exp/gold/drop） |
| `{"op":"auto","mob":tpl,"on":0/1}` | `{"ok":1,"auto"}`；on=1 起 tick 挂机，每回合另推 `ev fight` |
| `{"op":"bag"}` | `{"ok":1,"items":[{id,name,kind,count,atk,def,heal,price,minLevel}],"self"}` |
| `{"op":"use","item":id}` | `{"ok":1,"self"}`（消耗品回血；满血答错不消耗） |
| `{"op":"equip","item":id}` / `{"op":"takeoff","slot":"weapon"/"armor"}` | `{"ok":1,"self"}`（按 kind 落位，minLevel 门槛，原装备回包） |
| `{"op":"shop"}` | `{"ok":1,"shop":[在售物品（消耗品/装备，材料不卖）]}` |
| `{"op":"buy","item":id,"count"}` | `{"ok":1,"self"}`（金币即时扣，1-99 件） |
| `{"op":"sell","item":id,"count"}` | `{"ok":1,"self"}`（半价回收，下限 1 金） |

服务端主动推送：`ev chat / walk / move / announce / kick`（客户端收到
kick 自行断开）、`ev online`（tick 每 30 秒在线数）、`ev state`（GM 改值
实时推给在线会话）；战斗另推 `ev fight`（每回合详情）、`ev levelup`、
`ev drop`（掉落/GM 发放）、`ev die`（死亡回城）。密码与密保答案都是盐化散列，网页与 TCP 共用
`AccountDao`，行为不会漂移。

用 `nc` 就能当客户端试：

```
$ nc 127.0.0.1 7100
{"op":"register","user":"bob","pass":"secret1","question":"宠物名字","answer":"旺财"}
{"op":"login","user":"bob","pass":"secret1"}
{"op":"create","realm":1,"name":"刀狂","job":0}
{"op":"say","text":"一区的兄弟们好"}
{"op":"walk","x":10,"y":10}
```

## GM 管理后台

侧边栏"游戏管理"分节（`MenuBuilder.Section("game", ...)`），四个页面：

- **区服管理** `/admin/game/realms`：新增/改名/排序；开放↔维护一键切换
  （维护区拒绝 enter/create）；有角色的区不允许删除。
- **角色管理** `/admin/game/players`：按账号搜索、按区过滤；编辑昵称/
  职业/等级/金币/元宝/驻地；**在线走 `World.ApplyEdit/Adjust` 即时生效并
  推送，离线直改数据库**；同页可**发物品**（在线入包即推 `ev drop`，离线
  直写 `game_bag` 合并行）；封禁/解封**账号**（填原因，在线立即踢）；
  在线角色换区被拒（先踢下线）。
- **在线管理** `/admin/game/online`：会话快照（账号/角色/区服/阶段
  在世界中·未进区/心跳空闲），按 cid 踢线，全服广播（署名 GM，跨区可见）。
- **公告管理** `/admin/game/announces`：CRUD + 推送（`ev announce` 推给
  所有在线会话，停用状态的公告不允许推）。

首页仪表盘带游戏 KPI：账号数/封禁数/角色数（跨区）/实时在线。

权限沿用 RBAC：内置角色 `gm`（只管理游戏域：区服、玩家、在线、公告）
只授 `/admin/game/*` 屏，`admin` 全量；新 GM 页只要控制器方法带
`[Route]` + `[Custom(IsMenu)]` 就会出现在侧边栏与授权表里，启动时
`SyncRoleGrants` 自动补发。

## 持久化模型

| 时机 | 行为 |
|---|---|
| 每 `flushSeconds`（默认 10s） | 脏会话回写：level/hp/exp/weaponId/armorId/gold/gems/mapId/x/y/updatedAt；脏背包整包重写（删全插） |
| 下线 / 换区退出 | 立即回写 + 记角色 `lastLogoutAt` |
| 进区 | 按角色离线时长结算挂机收益（按秒折算、封顶），与 `lastLoginAt` 合并为一条 UPDATE；同时从 `game_bag` 装载背包 |
| 离线发物品 | GM 直写 `game_bag`（同物品合并行），下次登录可见 |
| 封禁 | 立即 UPDATE 账号表 + 在线则 `ev kick` 踢线 |
| 踢线/顶号/心跳超时 | `ev kick` 后立即 Leave：角色与背包当场落库、会话移出世界（连接本体由 worker 懒收口） |

`game_account / game_realm / game_player / game_map / game_announce /
game_mob / game_item / game_bag` 八张表由 `Schema.Ensure` 建表；种子三个
区服（三区为维护态演示）、五张地图（新手村→赤月峡谷，`minLevel` 递增）、
13 种物品与 6 个刷怪点（稻草人→赤月恶魔），改玩法先改这里。

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
- `kickSeconds`：多久没消息（含 hb）算掉线并踢出。
- `flushSeconds`：脏会话回写数据库的周期。
- `offlineGoldPerHour` / `offlineCapHours`：挂机结算速率（按秒折算）与封顶。
- `walkMax`：走位坐标上限（服务端钳位，客户端不可信）。

## 端到端自检

`tools/e2e.py`（标准库 urllib/socket，无第三方依赖）对运行中的服务端跑
**114 项断言**：网页注册/重复注册、找回密码三步与 5 次答错锁定、TCP
注册/登录/选区/建角/进区全流程、维护区拒绝、每区一角色与区内昵称唯一、
按区收窄的聊天/走位/同图查询、换区后角色状态保持、GM 区服 CRUD（含
维护门控与删除保护）、GM 发奖/封禁/踢线实时推送、公告推送、按秒折算的
离线结算，以及**战斗闭环全程**——新手图稻草人首杀必升级必掉兽皮、商店
目录与买药扣款、过图门槛、多钩猫反击与嗑药回血、GM 补金币/发铁剑
（`ev drop` 实时推）、穿脱武器攻防变化、卖皮半价回收、自动挂机逐 tick
推 `ev fight`、跨图自动暂停回图续打、30 级打赤月恶魔三回合倒下回城
半血、GM 降级钳血与满血拒药、flush 后 hp/经验/穿戴/背包落库核验。
**114 项断言**。在服务端目录里运行（它会读 `data/app.db` 验证落库），
跑之前删掉 `data/app.db*` 重启服务端，保证注册流程从空表开始；用法
详见文件头。

## 局域网多人

服务端两个监听都默认 `0.0.0.0`：

| 端口 | 用途 | 谁访问 |
|---|---|---|
| 8099 | HTTP 玩家注册/找回 + GM 后台 | 仅内网/运维段，建议防火墙不对公网放行 |
| 7100 | TCP 游戏网关 | 局域网玩家 |

- Windows 放行：`netsh advfirewall firewall add rule name="zan-game" dir=in action=allow protocol=TCP localport=7100`
- Linux 放行：`ufw allow 7100/tcp`（或对应 iptables 规则）。
- 玩家客户端连 `服务器内网IP:7100`；`[game].host` 保持 `0.0.0.0`。
- 修改端口/参数都在 `config/app.json` 的 `[game]` 段，重启生效。
- 区服目前是**进程内逻辑分区**（广播按区收窄）；要做成多进程多物理服，
  给 `game_realm` 加 `host/port` 并按区路由网关连接即可，表结构已留好口。

## 二次开发

- **加一个协议 op**：`Gateway.Handle` 的 `op == "..."` 分发链上加分支；
  全服广播用 `World.Broadcast`，**区服内**播报用 `World.DeliverRealm`，
  改值走 `World.Adjust`。
- **加一个区服**：GM 页新增即可；种子区服在 `Schema.SeedGame`。
- **加一张地图**：`Schema.SeedGame` 加一行（`minLevel` 控制进入门槛），
  客户端 `op:maps` 与 GM 页自动带出。
- **加一个 GM 页**：拷 `Controller/Admin/Game/Announces.zan` 的骨架，
  `[Table]` 实体 + `Index/Form/Save` + 同名视图即可，权限与侧边栏自动。
- **加怪/加物品**：`Schema.SeedMobs / SeedItems` 各加一行（掉落物按名字
  关联，`dropRate` 万分比）；刷怪数量、重生节奏都在行上，不用改代码。
- 玩法升级（组队、副本、行会）都在 `src/Game/` 里长，保持同一条纪律：
  在线态改内存打脏标记，落库交给 flush；不要在协议线程里直接写库。
