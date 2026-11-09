# 图形界面

> 你改一个 `label.text`，下一帧窗口就变了；这里没有 HTML，也没有 DOM 查询。EL 的界面是一组普通对象，被标准库布局、命中、绘制到系统窗口里。

!!! abstract "🎯 读完这页，你能"
    - 用两种入口之一建出会响应点击的窗口，并挂事件、起定时器、按 id 找节点
    - 分清定义图、布局样式与绘制主题，知道改哪个字段会重绘
    - 认出“规范目标但当前未实现”的写法

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[值与类型](../language/values.md)</span>

这一页讲**原生窗口**，入口在 `el:user-interface/index.el`。网页产物（`wasm32-browser`）尚未接入，见最后一节；规范第 9 章是目标合同，本页以源码为准，`class` 与词法绑定会标“实现状态”。

## 最小窗口：先让它出现

```el
import { element, appendChild, showWindow, runWindow } from "el:user-interface/index.el"

let root = element("column")
appendChild(root, "hello", element("label", "你好，EL"))
runWindow(showWindow(root, "第一个窗口", 320, 200))
```

看到窗口里显示“你好，EL”就说明对了；关掉窗口，`runWindow` 返回，程序继续。

!!! example "动手 30 秒"
    把 `"你好，EL"` 改成你的名字，把窗口尺寸改成 `480, 240` 再跑。标题栏、内容和宽度一起变了，说明这些参数直接决定这次呈现。

## 界面是对象图，不是 HTML

每个节点是一个 `Definition`，带 `kind`、`text`、`id`、`style`、`theme` 和子节点表 `children`。布局、命中、焦点、事件传播与绘制都由标准库在这张图上完成，平台层只管系统窗口和像素表面。

```el
let label = element("label", "你好", "greeting")
label.text = "你好，EL"
```

`label` 是普通对象，改 `text` 就是改字段，不创建 DOM、不拼 HTML。描述字符串只是构造同一套对象的另一种写法，本身始终是 `Text` 数据；同一张图可以交给原生窗口或浏览器页面，两边各自本地布局，不依赖可见 DOM。入口分工：`element`、`appendChild`、`on` 建图，`showWindow`、`runWindow` 显示，`View` 与窗口的 `getById` 查找节点。

## 入口一：写一段描述，解析成对象图

`showWindow` 接受 `Text` 描述，解析成定义图后打开窗口。支持标签 `row`、`column`、`div`、`label`、`button`、`input`、`title`、`data`，属性 `id`、`text`、`width`、`height`、`padding`、`gap`、`weight`、`overscroll`、`enabled`。`title` 必须在根元素之前，其余标签按嵌套建树；`label`、`button`、`input` 是叶子，文字写在属性或内容里。

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

`<data/>` 是数据槽，按顺序消费传入的绑定；二维数据源用 `dataView(source)`，需提供 `columnCount()`、`rowCount()`、`cellAt(row, column)`，格子值可为文本、数字或带 `content` 与命名颜色 `color` 的对象。

描述是数据，解析器不查名字、不调函数，只按固定标签与属性建节点。格式错误抛 `ViewDescriptionError`（带偏移与原因）；单份描述上限 1 MiB，展开上限 4096 节点、64 层。

!!! note "实现状态：字符串里没有事件和绑定"
    规范 12.9 的目标入口是 `buildView(description)` 加 `bind:value` 绑定宏。当前有描述字符串与元素对象 API 两条路径，字符串里暂不支持事件与绑定引用；绑定与词法变量观察还没实现。

## 入口二：要事件，就用元素对象 API

需要事件或运行时改文字时，用对象 API。`element(kind, text, id)` 只接受 `column`、`row`、`label`、`button`、`input`；`appendChild(parent, key, target)` 的 `key` 在同一父节点内必须唯一，重复报错；`on` 挂事件；`runWindow(showWindow(...))` 进入消息循环。

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

同一份定义可交给多次 `showWindow`，每个窗口有独立的布局、焦点与滚动；窗口按呈现查找节点，不共享查找表。

## 先猜：给 `<button>` 写 onclick 会触发吗？

??? question "先猜：描述字符串里写 `<button onclick="...">`，点击会执行吗？"
    不会。描述字符串入口没有事件语法，属性检查阶段就拒绝未知属性；事件只能挂在对象 API 节点上，用 `on(button, "click", ...)`。

## 布局：样式字段与校验

`Definition.style` 是 `LayoutStyle`，字段有 `flow`、`padding`、`gap`、`width`、`height`、`weight`、`basis`、`wrap`、`autoSize`、`overscroll`。`element("row")` 把 `flow` 设成 `"row"`，`column` 默认纵向；`padding`、`gap` 是逻辑单位，非负，`weight` 必须大于零。

刷新呈现时校验样式：未知 `flow`、未知 `overscroll`、负间距、零权重都抛错并保留上一帧。未指定尺寸的控件按内容定尺寸，容器按权重分配剩余主轴空间；内容超出时产生可滚动范围，`overscroll = "contain"` 阻止滚动量传给父级。

## 样式只有 LayoutStyle 与主题，class 还没生效

单个元素能调的样式就是 `LayoutStyle` 那组字段，加上可选的 `theme`。窗口另有绘制主题入口 `window.theme`，类型 `PaintTheme`，和元素主题不是同一个名字，别混用。

```el
import { Theme, ThemeContext } from "el:theme/index.el"

let root = element("column")
root.theme = Theme(fn(context: ThemeContext) => @{base100: 0x191B20; primary: 0x80A7F0})
```

`Theme` 接收由 `ThemeContext` 计算颜色表的函数，只需显式给出要覆盖的角色值。

!!! note "实现状态：class 与主题 token 还没做"
    规范 GUI-30 至 GUI-33 的目标是用 `class` 加主题 token 组织样式，并支持主题默认到局部属性的优先级。当前 `Definition` 没有 `class` 字段，也没有 class 到 token 的映射，只有 `style` 与 `theme`；写 `class` 不会生效，别把规范里的优先级当成已实现。

## 事件从捕获到冒泡，输入框给完整文本

`on(element, kind, action, capture = nil)` 挂监听器。事件先捕获（根到目标），再在目标调用，最后沿父链冒泡；`capture = t` 的监听器只在捕获阶段调用。当前分发的 `kind` 包括 `click`、`pointerdown`、`pointermove`、`pointerup`、`pointercancel`、`wheel`、`keydown`、`keyup`、`beforeinput`、`input` 与列表行的 `itemactivate`。

处理器收到 `GuiEvent`，字段有 `kind`、`target`、`currentTarget`、`phase`、`x`、`y`、`key`、`text`、`inputType`、`deltaX`、`deltaY`、`itemIndex`。`input` 的 `text` 是编辑后的完整文本，`beforeinput` 的 `inputType` 说明编辑种类；`stopPropagation()` 停止后续传播，`preventDefault()` 取消可取消的默认动作。

```el
let nameInput = element("input", "写点东西", "name")
let greeting = element("label", "你好", "greeting")
on(nameInput, "input", (event: GuiEvent) => {
	greeting.text = "你好，" + event.text
})
```

## 改字段自动重绘，查找用 getById

改公开字段会发布变更：`text`、`enabled`、`id`、`kind` 与 `style` 的 setter 都通知订阅者，窗口把变化合并到下一帧重绘，不需要手动刷新；同一帧内多次修改合并成一次呈现，读取仍同步。

`window.getById(id)` 按 id 精确查找（不接受选择器或模糊匹配），返回该次呈现的 `ElementHandle`；它的 `text`、`enabled` 是呈现级覆盖，只影响这个窗口，`editText` 没有覆盖时写回共享定义。id 为空抛错，同一挂载里重复 id 在刷新时报错。句柄还有 `scrollTo(x, y)`、`scrollX`、`scrollY`、`editing`、`identity`、`theme`；窗口关闭或节点卸载后失效，再用抛 `gui: element is no longer mounted`。

!!! note "实现状态：变量与界面还没有自动绑定"
    规范 GUI-5、GUI-6 的目标是让词法变量与界面绑定互相同步，需要捕获槽与观察机制配合；当前只有定义属性与样式变更通知，自动绑定尚未交付。

## 定时器按窗口管理，多窗口用 runWindows

`window.every(milliseconds, action)` 注册窗口级定时器，返回 `WindowTimer`，回调收到定时器本身，`timer.cancel()` 停止；间隔必须是 10 到 2147483647 的整数毫秒，窗口关闭时一起取消。

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

Windows 后端会合并迟到 tick，所以 `every` 是近似的界面节奏，不是经过时间；精确计时用时间库。方向键走 `window.onArrow((dx, dy) => ...)`，没有元素焦点时接收，三个桌面后端都实现了；规范第 9 章还没写这个入口，按实现使用即可。

`window.close()` 释放定时器、订阅与呈现资源，重复调用无副作用。`runWindow(window)` 处理消息直到窗口关闭；同时管理多个窗口用 `runWindows(@[first, second])`，它退出时关闭自己管理的所有窗口。处理失败时错误记录在 `window.failure` 并由循环抛出；要收尾就把清理放进 `finally`，正常关闭也会离开消息循环。

!!! warning "常见坑：窗口没反应，先查这三处"
    - 点按钮没反应：描述字符串不认 `onclick`，事件只能挂对象 API 节点。
    - 改了字段界面不动：确认改的是句柄还是共享定义，呈现级覆盖只影响当前窗口。
    - 秒数不准：`every` 会合并迟到 tick，它是界面节奏，不是经过时间。

## 可选 · 深入：同一份界面，也出网页

界面不绑死在系统窗口上：换掉平台层就能在别处显示。目标里的浏览器后端把整份程序编译成一个 HTML 文件：wasm 内嵌，不需要服务器、构建工具或外部运行时，`file://` 双击就能跑；视觉由 EL 用 Canvas 自绘，浏览器只提供画布、输入事件、字体度量和不可见的语义 DOM，不用可见 DOM/CSS 排版，标签描述也不当 HTML 执行。文件、目录、时间、随机与摘要由页面胶水换成浏览器实现，语言层调用面不变。

```sh
elc --target wasm32-browser app.el app.html
```

默认入口是 Canvas 自绘的控制台窗口；调用 `showWindow` 时，同一张定义图在页面里布局、绘制、命中与响应输入。页面还能内嵌开发链，`el repl`、`eval`、`el build` 都在浏览器里跑。

!!! note "实现状态：这条产物链路尚未接入"
    当前编译器把 `wasm32-browser` 当未接入目标直接拒绝，GUI 也没有浏览器后端；本页其余行为以原生后端源码为准，目标合同见规范的 GUI-52 与 wasm 目标设计文档。

## 带走这三样

- 界面是 `Definition` 对象图；两种入口构造同一套对象，但只有元素对象 API 能挂事件。
- 改公开字段会在下一帧合并重绘；节点用 `getById` 查，句柄随窗口关闭失效。
- 样式只认 `LayoutStyle` 与 `theme`；`class`、自动绑定、网页产物都还没实现。

## 下一站：声音与音频

> 窗口能弹出来了，但它还是哑的。怎么发一声提示音，甚至合成自己的波形？

- 主推进：[声音与音频](audio.md)：`playPitch`、`playFormula`、WAV 读写与平台后端。
- 想先练手：[实战：图形程序](../practice/gui-app.md)：用三份源码写一个完整的小应用。
- 后面会用到：[类与对象](../language/classes.md)：`@assign`、构造函数与共享语义。
