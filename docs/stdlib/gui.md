# 图形界面

这一页说明 EL 的窗口由什么组成、两种建界面方式怎么选，读完你能写出一个会响应点击的窗口。

## 界面是对象图，不是 HTML

EL 的界面是一组普通 EL 对象：每个节点是一个 `Definition`，带 `kind`、`text`、`id`、`style`、`theme` 和子节点表 `children`。布局、命中、焦点、事件传播和绘制命令都由标准库在这张图上完成，平台层只负责系统窗口与像素表面。

```el
let label = element("label", "你好", "greeting")
label.text = "你好，EL"
```

这段代码不创建 DOM 节点，也不拼 HTML 字符串：`label` 是普通对象，改 `text` 就是改字段。标记式描述字符串只是构造同一套对象的另一种写法，它本身始终是 `Text` 数据。同一定义图可以交给原生窗口，也可以交给浏览器页面；两种显示环境各自做本地布局，界面语义不依赖可见 DOM。

公开入口集中在 `el:user-interface/index.el`：`element`、`appendChild`、`on` 负责建图，`showWindow`、`runWindow` 负责显示，`View` 与窗口的 `getById` 负责在呈现里查找节点。规范第 9 章描述的是目标合同，下面所有函数名与参数以当前源码导出为准。

!!! note "实现状态"
    规范 12.9 的目标入口是 `buildView(description)` 加 `bind:value` 绑定宏。当前源码提供的是描述字符串入口与元素对象 API 两条路径，字符串里暂不支持事件与绑定引用；绑定与词法变量观察还没实现。

## 入口一：描述字符串

`showWindow` 接受一段 `Text` 描述，解析成定义图后打开窗口。解析器支持的标签是 `row`、`column`、`div`、`label`、`button`、`input`、`title`、`data`；支持的属性是 `id`、`text`、`width`、`height`、`padding`、`gap`、`weight`、`overscroll`、`enabled`。`title` 必须写在根元素之前，其余标签按嵌套关系建树，`label`、`button`、`input` 是叶子，文字可以写在属性里也可以写在标签内容里。

`<data/>` 是数据槽，按顺序消费调用者显式传入的绑定，二维数据源由 `dataView(source)` 转换。数据源需要提供 `columnCount()`、`rowCount()` 和 `cellAt(row, column)`，格子值可以是文本、数字，也可以是带 `content` 与命名颜色 `color` 的对象。

```el
import { showWindow, runWindow } from "el:user-interface/index.el"
import { Grid } from "el:collections/grids.el"

let board = Grid<element: any>(3, 3, @{color: "green"})
board[1, 1] = @{color: "red", content: "●"}
runWindow(showWindow(
	'<title>棋盘</title><column padding="12" gap="8"><label text="3 × 3"/><data/></column>',
	board, 320, 320,
))
```

描述是数据，不会被当成 EL 执行：解析器不查名字、不调用函数，只按固定标签与属性建节点。格式错误会抛 `ViewDescriptionError`，带出错偏移与原因；单份描述上限 1 MiB，展开上限 4096 个节点、64 层深度。

## 入口二：元素对象 API

需要事件、运行时改文字或精确控制布局时，直接用对象 API 建图。`element(kind, text, id)` 只接受 `column`、`row`、`label`、`button`、`input` 五种；`appendChild(parent, key, target)` 的 `key` 在同一父节点内必须唯一，重复会报错；`on` 挂事件；`runWindow(showWindow(root, title, width, height))` 进入消息循环。

```el
import { element, appendChild, on, GuiEvent, showWindow, runWindow } from "el:user-interface/index.el"

let root = element("column")
root.style.padding = 20
root.style.gap = 12
let display = element("label", "0", "count")
let button = element("button", "加一", "add")
appendChild(root, "count", display)
appendChild(root, "add", button)
let count = 0
on(button, "click", (event: GuiEvent) => {
	count++
	display.text = Text(count)
})
runWindow(showWindow(root, "EL 计数器", 320, 240))
```

同一份定义可以交给多次 `showWindow`，每个窗口有独立的布局、焦点与滚动；窗口按呈现查找节点，不共享查找表。

## 布局

`Definition.style` 是 `LayoutStyle`，字段有 `flow`、`padding`、`gap`、`width`、`height`、`weight`、`basis`、`wrap`、`autoSize`、`overscroll`。`element("row")` 会把 `flow` 设成 `"row"`，`column` 默认纵向排列；`padding`、`gap` 是逻辑单位，非负，`weight` 必须大于零。

刷新呈现时会校验样式：未知 `flow`、未知 `overscroll`、负间距、零权重都抛错并保留上一帧。未显式指定尺寸的控件按内容定尺寸，容器按权重分配剩余主轴空间，内容超出容器时产生可滚动范围，`overscroll = "contain"` 阻止剩余滚动量继续传给父级。

## 样式、class 与主题

当前实现里，单个元素能调的样式就是 `LayoutStyle` 那组字段，加上可选的 `theme`。窗口另有一个绘制主题入口 `window.theme`，类型是 `PaintTheme`，它和元素主题不是同一个名字，别混用。

```el
import { Theme, ThemeContext } from "el:theme/index.el"

let root = element("column")
root.theme = Theme(fn(context: ThemeContext) => @{base100: 0x191B20; primary: 0x80A7F0})
```

`Theme` 接收一个由 `ThemeContext` 计算颜色表的函数，只需显式给出要覆盖的角色值。

!!! note "实现状态"
    规范 GUI-30 至 GUI-33 的目标是用 `class` 属性加主题 token 组织样式，并支持主题默认到局部属性的优先级。当前 `Definition` 没有 `class` 字段，也没有 class 到 token 的映射，只有 `style` 与 `theme`。写 `class` 不会生效，也不要把规范里的 class 优先级当成已实现行为。

## 事件

`on(element, kind, action, capture = nil)` 给一个定义挂监听器。事件先按捕获阶段从根走到目标，再在目标上调用，最后沿父链冒泡；`capture = t` 的监听器只在捕获阶段调用。当前源码分发的 `kind` 包括 `click`、`pointerdown`、`pointermove`、`pointerup`、`pointercancel`、`wheel`、`keydown`、`keyup`、`beforeinput`、`input` 和列表行的 `itemactivate`。

处理器收到一个 `GuiEvent`，字段有 `kind`、`target`、`currentTarget`、`phase`、`x`、`y`、`key`、`text`、`inputType`、`deltaX`、`deltaY`、`itemIndex`。`input` 事件的 `text` 是编辑后的完整文本，`beforeinput` 的 `inputType` 说明这次编辑的种类。`stopPropagation()` 停止后续传播，`preventDefault()` 取消可取消的默认动作。

```el
let nameInput = element("input", "写点东西", "name")
let greeting = element("label", "你好", "greeting")
on(nameInput, "input", (event: GuiEvent) => {
	greeting.text = "你好，" + event.text
})
```

事件只能挂在对象 API 的节点上。描述字符串入口当前没有事件语法，写 `<button onclick="...">` 不会触发任何回调，属性检查阶段就会拒绝未知属性。

## 状态更新

改 `Definition` 的公开字段会发布变更：`text`、`enabled`、`id`、`kind` 以及 `style` 的 setter 都会通知订阅者，窗口把变化合并到下一帧重绘，不需要手动刷新。同一帧内的多次修改合并成一次呈现，读取仍然是同步的。

`window.getById(id)` 返回该次呈现的 `ElementHandle`，它的 `text` 与 `enabled` 是呈现级覆盖，只影响这一个窗口；`editText` 在没有呈现级覆盖时写回共享定义。句柄在窗口关闭或节点卸载后失效，再用会抛 `gui: element is no longer mounted`。

!!! note "实现状态"
    规范 GUI-5、GUI-6 的目标是让普通词法变量与界面绑定互相同步，这需要捕获槽与观察机制配合；当前实现只有定义属性与样式变更通知，`capture`、`buildView` 的自动绑定尚未交付。

## 查找元素与定时器

`window.getById(id)` 按 id 精确查找，不接受选择器或模糊匹配；id 为空抛错，同一次挂载里出现重复 id 会在刷新时报错。句柄还提供 `scrollTo(x, y)`、`scrollX`、`scrollY`、`editing`、`identity` 和 `theme`。

`window.every(milliseconds, action)` 注册窗口级定时器，返回 `WindowTimer`，回调收到定时器本身，`timer.cancel()` 停止；间隔必须是 10 到 2147483647 之间的整数毫秒，窗口关闭时所有定时器一起取消。

```el
let root = element("column")
let clock = element("label", "运行 0 秒", "clock")
appendChild(root, "clock", clock)
let window = showWindow(root, "EL 计时器", 320, 200)
let handle = window.getById("clock")
let seconds = 0
discard(window.every(1000, (tick) => {
	seconds++
	handle.text = "运行 " + Text(seconds) + " 秒"
}))
runWindow(window)
```

Windows 后端会合并迟到的 tick，因此 `every` 是近似的界面节奏，不是经过时间；需要精确计时用时间库，不要累加 tick 数当秒表。

方向键走窗口级入口：`window.onArrow((dx, dy) => ...)` 只在没有元素焦点时接收方向键，三个桌面后端都实现了它。规范第 9 章还没写这个入口，按实现使用即可，不要期待跨版本稳定。

## 关闭与多窗口

`window.close()` 关闭窗口并释放定时器、订阅和呈现资源，重复调用无副作用。`runWindow(window)` 处理消息直到窗口关闭；要同时管理多个窗口用 `runWindows(@[first, second])`，它退出时关闭自己管理的所有窗口。

窗口处理失败时错误记录在 `window.failure` 并由循环抛出，不会静默退出。需要在自己代码里收尾时，把清理放进 `try` 的 `finally`，因为正常关闭也会离开消息循环。

## 同一份界面，也出网页

EL 的界面不绑死在系统窗口上。定义、布局、命中与绘制命令都是普通 EL 对象和函数，把平台层换掉就能在别处显示。目标里的浏览器后端把整份程序编译成一个 HTML 文件：wasm 模块内嵌在页面里，不依赖服务器、构建工具或外部运行时，`file://` 双击就能运行；视觉仍由 EL 用 Canvas 自绘，浏览器只提供画布、输入事件、字体度量和一层视觉不可见的语义 DOM。不用可见 DOM 或 CSS 排版，也不把标签描述当 HTML 执行。文件、目录、时间、随机与摘要这些平台调用由页面胶水换成浏览器实现，语言层的调用面不变。

```sh
elc --target wasm32-browser app.el app.html
```

默认入口是一个 Canvas 自绘的控制台窗口；程序自己调用 `showWindow` 时，就是同一张定义图在页面里布局、绘制、命中与响应输入。同一个页面还能内嵌开发链，`el repl`、`eval` 与 `el build` 都在浏览器里跑。

!!! note "实现状态"
    这条产物链路尚未接入。当前编译器入口把 `wasm32-browser` 当成未接入目标直接拒绝，GUI 也还没有浏览器后端；本页其余函数名与行为以当前原生后端源码为准。目标合同见 EL 规范的 GUI-52 与 wasm 目标设计文档。

## 继续阅读

- [实战：图形程序](../practice/gui-app.md)：用三份源码写一个完整的小应用。
- [声音与音频](audio.md)：提示音、`SoundPlayer` 与自定义公式播放。
- [类与对象](../language/classes.md)：`@assign`、构造函数与共享语义。
- [常见问题](../appendix/faq.md)：GUI 与 HTML 的关系、输出与运行的常见卡点。
