# SkinBuilder — Zan Gui Chart 皮肤配置工具

所见即所得的 Chart 组件皮肤编辑器：左边调色，右边是**真实 Chart
组件**的实时预览，每一帧把当前配置写成皮肤包并走 `App` 的皮肤热
重载通道，预览零延迟跟手。全部使用标准库组件
（ColorPicker / Input / RadioGroup / Button / Label / Panel + Chart），
无任何自绘。

## 构建与运行

在 ZanIDE 里打开 `SkinBuilder.zan` 一键运行即可；命令行等价形式：

```bash
build/zanc tools/skinbuilder/SkinBuilder.zan --auto-stdlib -o build/skinbuilder.exe
```

`--auto-stdlib` 自动拉齐 Gui/Widget/Chart 组件，`[DllImport("zan_gui")]`
的原生驱动由 zanc 从 `stdlib/Gui/drivers/<平台>/` 自动发现并捆绑到
输出旁，无需任何手工链接步骤。

## 界面

| 区域 | 内容 |
|------|------|
| 左列 A | 皮肤包名称、亮色/暗色基底、系列调色板 `--chart-1..8`（初值 = ECharts 2.2.7 默认定性色）、重置/导出按钮 |
| 左列 B | 图表部件颜色：grid / axis / 刻度文字 / 轴标题 / 数据标签 label / legend / mark / accent / tooltip 底·字·边 |
| 右侧 | 两块真实 Chart 预览：折柱混搭（覆盖调色板 1..3、轴、网格、数据标签、图例、平均线标记）+ 环形占比图（调色板 1..5、扇区标签、中心合计） |

## 产出

**草稿（自动）**：每次改动即时写入
`<exe目录>/skins/skinbuilder-draft/skin.css` 并热应用——这就是预览
实时跟手的机制，也可以拿它当"当前进度"直接用。

**导出**：点「导出皮肤包」固化成
`<exe目录>/skins/<名称>/skin.css`。生成的 css 形如：

```css
:root {
  --name: "my-chart-skin";
  --order: 40;
  --base: light;          /* 亮/暗基底（--dark 同步置 0/1） */
  --chart-1: #FF7F50;     /* Chart.Palette 的第 1 槽，以此类推到 --chart-8 */
  ...
}
chart::grid    { background: #CCCCCC; }
chart::axis    { background: #4488BB; color: #333333; }
chart::axis-title { color: #6E7079; }
chart::legend  { color: #6E7079; }
chart::label   { color: #333333; }
chart::mark    { background: #E43C4E; color: #E43C4E; }
chart::accent  { background: #4488BB; }
chart::tooltip { background: #FFFFFF; color: #333333; border: 1 #DDDDDD; }
```

## 在应用里使用皮肤包

把整个 `<名称>/` 目录拷到应用的皮肤发现根之一（见
`stdlib/Gui/Skin.zan` 的 `Roots()`）：`$ZAN_GUI_SKINS`、
`$ZAN_APP_DIR/skins`、exe 旁 `skins/`、工作目录 `skins/` 等，然后
`app.UseSkin("<名称>")`，或直接用标题栏的皮肤选择器切换。皮肤是
纯 CSS 包，无需任何注册代码。

只想要图表换色、其余跟随应用皮肤的，可以只保留 `:root` 里的
`--chart-*` 与 `chart::*` 规则——皮肤 css 是逐层叠加的，未写明的
部分继承下层（base.css）。
