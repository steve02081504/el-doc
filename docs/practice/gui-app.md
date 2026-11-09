# 实战：图形程序

这一页用一个完整的计数器应用，把窗口、布局、事件、状态和定时器串起来；读完你能自己拆文件、运行并构建出一个原生窗口程序。

## 目标

程序显示一行当前值和操作次数、两个加减按钮、一个清零按钮，再加一行运行秒数。值到 0 时清零按钮被禁用，定时器每秒刷新秒数。代码分成状态、界面、入口三份文件，方便继续加功能。

```text
counter/
├── package.eol
└── src/
    ├── main.el
    ├── state.el
    └── view.el
```

`package.eol` 声明项目入口。项目文件固定叫 `package.eol` 或 `package.eod`，`el test` 一类按项目工作的子命令从当前目录向上找到最近的这一份；目录里两种同时存在会按歧义报错。

```eol
@{
	entry: "src/main.el"
}
```

## 状态：src/state.el

状态是一个普通的共享类。`@assign(mode: "shared")` 说明这个类的值按引用传递，多个窗口拿到的是同一个计数器；复制语义的类型则写成 `@assign(mode: "copy")`。私有字段用 `#` 前缀，外部只能通过 getter 与方法来用。

```el
@assign(mode: "shared")
export class Counter {
	let #value: Number = 0
	let #steps: Number = 0
	constructor() { init this }
	get value(): Number { return this.#value }
	get steps(): Number { return this.#steps }
	fn increase(): void_t { this.#value++; this.#steps++ }
	fn decrease(): void_t { this.#value--; this.#steps++ }
	fn reset(): void_t { this.#value = 0 }
	fn summary(): Text => "值 " + Text(this.#value) + "，已操作 " + Text(this.#steps) + " 次"
}
```

`summary` 用箭头形式直接返回一个表达式，`Text(this.#value)` 把数字转成文本再拼接。业务逻辑放在这里，界面文件只负责显示和转发点击。

## 界面：src/view.el

界面文件建出定义树并挂上事件。`element(kind, text, id)` 创建节点，`appendChild(parent, key, target)` 按 key 挂到父节点，key 在同一父节点内必须唯一；`on(element, "click", handler)` 挂点击事件。

```el
import { Counter } from "file:./state.el"
import { Definition, element, appendChild, on, GuiEvent } from "el:user-interface/index.el"

export fn buildCounterView(counter: Counter): Definition {
	let root = element("column")
	root.style.padding = 20
	root.style.gap = 12
	let title = element("label", "计数器")
	let display = element("label", counter.summary(), "display")
	let clock = element("label", "运行 0 秒", "clock")
	let controls = element("row")
	controls.style.gap = 8
	let increase = element("button", "+1", "increase")
	let decrease = element("button", "-1", "decrease")
	let reset = element("button", "清零", "reset")
	appendChild(root, "title", title)
	appendChild(root, "display", display)
	appendChild(root, "clock", clock)
	appendChild(root, "controls", controls)
	appendChild(controls, "increase", increase)
	appendChild(controls, "decrease", decrease)
	appendChild(controls, "reset", reset)
	let update = fn() {
		display.text = counter.summary()
		reset.enabled = counter.value != 0
	}
	on(increase, "click", (event: GuiEvent) => { counter.increase(); update() })
	on(decrease, "click", (event: GuiEvent) => { counter.decrease(); update() })
	on(reset, "click", (event: GuiEvent) => { counter.reset(); update() })
	update()
	return root
}
```

三个处理器都做同一件事：改状态，再调用 `update` 刷新文字与禁用状态。`display.text = ...` 与 `reset.enabled = ...` 是定义字段赋值，会发布变更，窗口把这一帧的修改合并到下一次绘制；不需要手动调用刷新，也不要在事件里自己画。

`reset.enabled = counter.value != 0` 演示了逐呈现覆盖：`reset` 是共享定义，但这里改的是这棵定义树上的节点字段。如果同一个定义交给两个窗口显示、又想只禁用一个窗口里的按钮，用 `window.getById(id).enabled = nil`，那才是只影响单个窗口的句柄覆盖。

!!! tip "给有别的语言经验的读者"
    这里没有事件循环回调注册表，也没有 `addEventListener` 的选项对象：`on` 接收元素、事件名和处理器，捕获阶段通过第四个参数 `t` 选择。事件对象是 `GuiEvent`，`event.target` 是呈现身份编号，不是 DOM 节点引用。

## 入口：src/main.el

入口文件只做装配：建状态、建界面、开窗口、挂定时器、进入消息循环。

```el
import { Counter } from "file:./state.el"
import { buildCounterView } from "file:./view.el"
import { showWindow, runWindow } from "el:user-interface/index.el"

let counter = Counter()
let root = buildCounterView(counter)
let window = showWindow(root, "EL 计数器", 380, 320)
let clock = window.getById("clock")
let seconds = 0
discard(window.every(1000, (tick) => {
	seconds++
	clock.text = "运行 " + Text(seconds) + " 秒"
}))
runWindow(window)
```

`showWindow` 打开系统窗口并返回窗口对象，标题、宽、高都是可选参数，默认标题是 `"EL"`、默认尺寸 480 × 360。`window.getById("clock")` 按 id 取出这次呈现的句柄，定时器每秒改它的 `text`；句柄只属于这个窗口，窗口关闭后失效。

`window.every(1000, action)` 的间隔必须是 10 到 2147483647 之间的整数毫秒，返回值可以 `cancel()`；这里不需要保存定时器，窗口关闭时会自动取消。`discard(...)` 表示明确丢弃返回值。

`runWindow(window)` 是阻塞的：它处理消息、布局、绘制和事件，直到窗口关闭或线程收到退出消息才返回，所以装配代码要写在它前面。

## 运行

在项目根目录（`package.eol` 所在目录）执行：

```text
el run src/main.el
```

`el run` 编译入口到临时产物并立即执行，产物在程序退出后删除。窗口出现后：点 `+1` 数值加一、操作次数加一；点 `-1` 数值减一；点清零把值归零，按钮在值为 0 时变灰不可点；底部秒数每秒变化。关掉窗口，`runWindow` 返回，`el run` 以退出码 0 结束。

给程序传参数时写在入口文件之后，`el run` 会原样转交并保持次序：

```text
el run src/main.el --demo
```

## 构建

```text
el build src/main.el
```

`el build` 只编译不运行，默认输出到入口文件旁边，把入口文件名的扩展名换成本平台可执行后缀，并把绝对路径写到标准输出。Windows 上得到 `src\main.exe`，Linux 与 macOS 上得到 `src/main`。

```text
el build -o build/counter.exe src/main.el
el build --release src/main.el
```

`-o` 与 `--output` 是同一个选项身份，指定别的输出路径；`--release` 选择 release 安全检查等级，默认是 debug，`--debug` 与 `--release` 互斥。产物是原生可执行文件，双击或用命令行直接运行都会出现同样的窗口，不再需要 `el`。

入口文件也可以用 `.els` 扩展名；`.els` 与 `.el` 一样由 `el run` 接受，区别只在宿主安装关联上，当前两者共享同一套顶层语句语义。

## 再加一点功能

- 记录历史：把每次操作追加到数组，用第二个 `label` 拼接最近几条；`Text.join` 或 `join_text` 来自文本库。
- 主题切换：给根元素赋 `Theme(...)`，见[图形界面](../stdlib/gui.md)的主题小节；两个窗口可以各自覆盖。
- 键盘操作：`window.onArrow((dx, dy) => ...)` 接收方向键，适合替换 `+1`／`-1` 的鼠标点击。
- 自动保存：在 `runWindow` 之前的 `finally` 里写文件，或把清理放进 `try` 的 `finally`。

改完先 `el run src/main.el` 看行为，再 `el build` 验证产物；行为对但界面不更新，先查是不是改了局部变量而没有改定义字段。

## 继续阅读

- [图形界面](../stdlib/gui.md)：对象图、两种入口、事件与定时器的完整说明。
- [类与对象](../language/classes.md)：`@assign`、构造函数、私有字段与共享语义。
- [命令行工具](cli-tool.md)：另一个从零开始、但输出到终端的完整项目。
