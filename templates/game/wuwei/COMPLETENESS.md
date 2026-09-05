# 完成度清单

对照原版《无为修仙传》的功能与本次重制的状态。测试矩阵的“本轮实际
验证”一节在每次跑完 `tools/test.ps1` 后更新真实数字。

## 功能

| 模块 | 状态 | 说明 |
|------|------|------|
| 主菜单（原版式复刻） | ✅ | 整幅背景 cover、题字 contain（原坐标 92,78 600×255）、四入口按钮、版本号；资源分步真实加载 |
| 背景音乐 | ✅ | 主菜单起循环播放，设置页音量调节（含事件探针） |
| 档位/新档 | ✅ | 5 槽位档案（`Profiles.zan`），新档向导 |
| 修行 | ✅ | 吐纳/炼气/突破，境界 10 层（`realms.csv`），气血/攻防成长 |
| 历练 | ✅ | 29 图 69 敌，遭遇战、掉落、章节分页 |
| 杂学/百艺 | ✅ | 108 配方，分类=真筛选（只显示当前类），横向居中分页 |
| 万宝/行囊 | ✅ | 236 物品，使用/装备/售出/分解 |
| 坊市 | ✅ | `market.csv` 买卖 |
| 宗门 | ✅ | 入门/任务/宝库 |
| 轮回（转生） | ✅ | 因果/世数继承、天赋、熟练度星级 |
| 成就 | ✅ | 33 项 |
| 存档 | ✅ | AES-256-GCM `.wsv`，损坏即拒载（`security.zan` 回归） |
| 数值表 | ✅ | 21 张 CSV 权威表；发布加密内嵌，`model.zan` 全量回归 |
| 素材 | ✅ | 365 张 WebP 11.88 MiB 内嵌（`ASSETS.md`） |
| 皮肤 | ✅ | `skins/wuwei` 按路径打包；游戏窗口关闭皮肤选择器（`SetChromeButtons(false,false,true,true)`） |
| 窗口 | ✅ | 1280×800，标题栏仅保留关闭/最大化 |

## 测试矩阵（tests/templates/wuwei/）

| 测试 | 覆盖 |
|------|------|
| `test_data.py` | 跨表引用完整性（配方↔材料↔地图↔敌人…） |
| `test_pack.py` | 表格加密：机密性、认证（篡改必败）、覆盖张数 |
| `test_prepare_assets.py` | 题写着色器逐像素、WebP-only、可重复导入 |
| `model.zan` | 无头模型：修炼/战斗/百艺/任务/ negative time 等 |
| `profiles.zan` | 槽位路径与 `WUWEI_SAVE_DIR` 重定向 |
| `security.zan` | 存档加解密、篡改拒绝、缺档 |
| `gameplay.ui`（`-Gui`） | UiDriver 驱动真实窗口：菜单→设置→成就→新档→修炼→历练→百艺→行囊→存读档全流程 |

## 本轮实际验证

2026-09-06，`powershell tools/test.ps1 -Gui -GuiOutput build/wuwei/restored`，
结果 **ALL PASS**：

- `test_data.py` 5 项、`test_pack.py` 1 项、`test_prepare_assets.py` 4 项
  单测全过；
- 无头模型回归 `model.zan`（修炼/战斗/百艺/任务/迁移/飞升）、
  `profiles.zan`（槽位与音频）、`security.zan`（加密存档）全过；
- 保护式发布 362 个文件至 `build/wuwei/restored/`（无散装
  data/assets/skins 目录，20 张 CSV 加密内嵌、365 张 WebP 与音频内嵌）；
- `gameplay.ui` UiDriver 真实窗口全流程 **73 项断言 0 失败**
  （菜单→设置→成就→双档位新档→修炼→历练→百艺分类筛选与翻页→行囊→
  设置自愈/音量→存档→回菜单→载入，断言跨档状态隔离）；
- 截图验收（UiDriver `dump pixels`，`_scratch/wuwei-shots/`）：主菜单、
  修炼、任务/野外/险地/绝境、坊市、宗门/宝库/擂台、系统/图鉴、杂学
  （8 类真筛选+居中分页）、行囊、轮回、历练共 17 张，标题栏仅存
  最小化/最大化/关闭三键；
- 排版复检：坊市/宗门/宝库/擂台/存档等卡片行统一为
  Flex `[内容][grow 间隔][按钮]` 右对齐（Panel.Row 的 Grow 只作用于
  首子元素且被排到末尾，属保留模式布局既定行为）；地图卡简介加高至
  124px，四行文本不再压住「前往历练」按钮；空装备栏不显示「卸下」；
  存档摘要不再出现「仙缘 N · 仙缘 N」重名。

与 IDE 通用 Run/Publish 的边界：本模板的发布形态依赖
`tools/build.ps1` 的 `--publish --embed`（加密表格 + skins 路径打包），
IDE 对任意项目的通用 Run 不会做这些模板专用内嵌，二者不等价。

## 已知限制

- `tools/import_data.py`（CSV ← 原作表格的反向导入工具）在一次会话
  事故中丢失且无存档，未重建；`data/*.csv` 本身是权威编辑源，
  直接改表即可，不影响任何工作流。
- 素材解码器只支持静态 WebP（原作素材不含动画 WebP，无影响）。
