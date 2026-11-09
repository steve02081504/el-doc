# 实战：图形程序

> 终端里点不到按钮。那“状态一变，界面就跟着变”这件事，在 EL 里到底由谁负责？

!!! abstract "🎯 做完这个项目，你能"
    - 从空目录建出三份源码的原生窗口应用，关窗后进程干净退出
    - 用 `@assign(mode: "shared")` 的类保存状态，让界面只读、只转发点击
    - 用 `element`／`appendChild`／`on` 搭出布局并挂上事件
    - 用 `window.every` 加一个每秒刷新的定时器，并知道它什么时候失效

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：[类与对象](../language/classes.md)、[图形界面](../stdlib/gui.md)、事件与定时器</span>

## 目标与边界

做一个计数器窗口：显示当前值和操作次数、两个加减按钮、一个清零按钮，再加一行运行秒数。值到 0 时清零按钮被禁用，定时器每秒刷新秒数。代码分成状态、界面、入口三份文件，方便继续加功能。

验收标准：

- `el run src/main.el` 打开标题为 `EL 计数器` 的窗口，里面有 `值 0，已操作 0 次`
- 点 `+1` 数值与操作次数各加一，点 `-1` 数值减一
- 清零把值归零，按钮在值为 0 时变灰不可点
- 底部秒数每秒变化；关掉窗口后 `el run` 以退出码 0 结束

刻意不做的事：不做数据持久化，不做多窗口联动，也不自绘控件。这些是练习。

## 第一步：先开一个空窗口

项目文件固定叫 `package.eol` 或 `package.eod`，`el test` 一类子命令从当前目录向上找到最近的一份来定位项目根；目录里两种同时存在会按歧义报错。

```text
counter/
├── package.eol
└── src/
    ├── main.el
    ├── state.el
    └── view.el
```

```eol
@{
	entry: "src/main.el"
}
```

入口先只做一件事：建一个根节点、开窗口、进入消息循环。

```el
import { element, showWindow, runWindow } from "el:user-interface/index.el"

let root = element("label", "计数器")
let window = showWindow(root, "EL 计数器", 380, 320)
runWindow(window)
```

`showWindow` 打开系统窗口并返回窗口对象，标题、宽、高都是可选参数，默认标题是 `"EL"`、默认尺寸 480 × 360。`runWindow(window)` 是阻塞的：它处理消息、布局、绘制和事件，直到窗口关闭或线程收到退出消息才返回，所以装配代码要写在它前面。

```text
el run src/main.el
```

!!! success "检查点"
    - [ ] 窗口弹出，标题是 `EL 计数器`，里面有一行 `计数器`
    - [ ] 关掉窗口后终端回到提示符，退出码是 0
    - [ ] 把标题换成你自己的名字，窗口标题跟着变

## 第二步：状态放进一个共享类

状态是一个普通的共享类。`@assign(mode: "shared")` 说明这个类的值按引用传递，多个窗口拿到的是同一个计数器；复制语义的类型则写成 `@assign(mode: "copy")`。私有字段用 `#` 前缀，外部只能通过 getter 与方法来用。

```el
@assign(mode: "shared")
export class Counter {
	let #value: Number = 0
	let #steps: Number = 0
	constructor() { init this }
	get value(): Number { return this.#value }
	get steps(): Number { return this.#steps }
	fn increase() { this.#value++; this.#steps++ }
	fn decrease() { this.#value--; this.#steps++ }
	fn reset() { this.#value = 0 }
	fn summary(): Text => "值 " + Text(this.#value) + "，已操作 " + Text(this.#steps) + " 次"
}
```

`summary` 用箭头形式直接返回一个表达式，`Text(this.#value)` 把数字转成文本再拼接。业务逻辑放在这里，界面文件只负责显示和转发点击。

不开窗口也能验它：

```el
import { Counter } from "file:./state.el"

let counter = Counter()
counter.increase()
counter.increase()
console.stdout.writeLine(counter.summary())
```

```text
值 2，已操作 2 次
```

!!! success "检查点"
    - [ ] 上面这段输出 `值 2，已操作 2 次`
    - [ ] 再调一次 `counter.decrease()`，输出变成 `值 1，已操作 3 次`
    - [ ] 不写 `@assign(mode: "shared")` 会被编译器拒绝

## 第三步：把状态画到窗口上

界面文件建出定义树并挂上事件。`element(kind, text, id)` 创建节点，`appendChild(parent, key, target)` 按 key 挂到父节点，key 在同一父节点内必须唯一。

```el
import { Counter } from "file:./state.el"
import { Definition, element, appendChild } from "el:user-interface/index.el"

export fn buildCounterView(counter: Counter): Definition {
	let root = element("column")
	root.style.padding = 20
	root.style.gap = 12
	let title = element("label", "计数器")
	let display = element("label", counter.summary(), "display")
	appendChild(root, "title", title)
	appendChild(root, "display", display)
	return root
}
```

入口改成装配：建状态、建界面、开窗口。

```el
import { Counter } from "file:./state.el"
import { buildCounterView } from "file:./view.el"
import { showWindow, runWindow } from "el:user-interface/index.el"

let counter = Counter()
let root = buildCounterView(counter)
let window = showWindow(root, "EL 计数器", 380, 320)
runWindow(window)
```

```text
el run src/main.el
```

窗口里应当出现两行：`计数器` 和 `值 0，已操作 0 次`。

!!! success "检查点"
    - [ ] 窗口里两行文字自上而下排列，间距 12
    - [ ] 把 `element("label", "计数器")` 的文字换成你的标题，界面跟着变
    - [ ] 两个 `appendChild` 的 key 写成一样时，第二次挂载报错

## 第四步：按钮改状态，界面跟着变

在 `buildCounterView` 的 `return root` 之前追加控件、更新函数与两个点击处理器：

```el
	let controls = element("row")
	controls.style.gap = 8
	let increase = element("button", "+1", "increase")
	let decrease = element("button", "-1", "decrease")
	appendChild(root, "controls", controls)
	appendChild(controls, "increase", increase)
	appendChild(controls, "decrease", decrease)
	let update = fn() {
		display.text = counter.summary()
	}
	on(increase, "click", (event: GuiEvent) => { counter.increase(); update() })
	on(decrease, "click", (event: GuiEvent) => { counter.decrease(); update() })
	update()
```

导入行同时补上 `on` 与 `GuiEvent`：`import { Definition, element, appendChild, on, GuiEvent } from "el:user-interface/index.el"`。

!!! tip "给有别的语言经验的读者"
    这里没有事件循环回调注册表，也没有 `addEventListener` 的选项对象：`on` 接收元素、事件名和处理器，捕获阶段通过第四个参数 `t` 选择。事件对象是 `GuiEvent`，`event.target` 是呈现身份编号，不是 DOM 节点引用。

三个处理器都做同一件事：改状态，再调用 `update` 刷新文字与禁用状态。`display.text = ...` 是定义字段赋值，会发布变更，窗口把这一帧的修改合并到下一次绘制；不需要手动调用刷新，也不要在事件里自己画。

!!! success "检查点"
    - [ ] 点 `+1` 一次，文字变成 `值 1，已操作 1 次`
    - [ ] 点 `-1` 两次，文字变成 `值 -1，已操作 3 次`
    - [ ] 点按钮时窗口没有卡住，文字立刻更新

## 第五步：清零按钮为什么会自己变灰

再加一个清零按钮，把 `update` 换成这一版：

```el
	let reset = element("button", "清零", "reset")
	appendChild(controls, "reset", reset)
	let update = fn() {
		display.text = counter.summary()
		reset.enabled = counter.value != 0
	}
	on(reset, "click", (event: GuiEvent) => { counter.reset(); update() })
```

??? question "先猜：点十次 `+1` 再点清零，界面会显示 `值 0，已操作 0 次` 吗？"
    不会。`reset` 只写 `this.#value = 0`，`#steps` 继续累加，所以显示的是 `值 0，已操作 11 次`。想一并清空操作次数，得自己改 `reset` 的实现。

`reset.enabled = counter.value != 0` 演示了逐呈现覆盖：`reset` 是共享定义，但这里改的是这棵定义树上的节点字段。如果同一个定义交给两个窗口显示、又想只禁用一个窗口里的按钮，用 `window.getById(id).enabled = nil`，那才是只影响单个窗口的句柄覆盖。

!!! success "检查点"
    - [ ] 窗口刚打开时清零按钮就是灰的
    - [ ] 点一次 `+1` 后清零按钮恢复可点，点它把值归零
    - [ ] 清零后操作次数没有归零，与你猜的结果对一下

## 第六步：让秒数每秒走一格

先给界面加一行时钟，放在 `display` 之后、`controls` 之前：

```el
	let clock = element("label", "运行 0 秒", "clock")
	appendChild(root, "clock", clock)
```

再在入口里按 id 取句柄、挂定时器：

```el
let clock = window.getById("clock")
let seconds = 0
discard(window.every(1000, (tick) => {
	seconds++
	clock.text = "运行 " + Text(seconds) + " 秒"
}))
runWindow(window)
```

`window.getById("clock")` 按 id 取出这次呈现的句柄，句柄只属于这个窗口，窗口关闭后失效。`window.every(1000, action)` 的间隔必须是 10 到 2147483647 之间的整数毫秒，返回值可以 `cancel()`；这里不需要保存定时器，窗口关闭时会自动取消，`discard(...)` 表示明确丢弃返回值。

!!! success "检查点"
    - [ ] 窗口打开后秒数每秒加一
    - [ ] 点按钮不影响秒数，秒数也不影响值
    - [ ] 把 1000 改成 100，刷新明显变快；改成 5 会因为低于 10 被拒绝

## 第七步：构建成可交付的产物

```text
el build src/main.el
```

`el build` 只编译不运行，默认输出到入口文件旁边，把入口文件名的扩展名换成本平台可执行后缀，并把绝对路径写到标准输出。Windows 上得到 `src\main.exe`，Linux 与 macOS 上得到 `src/main`。产物是原生可执行文件，双击或用命令行直接运行都会出现同样的窗口，不再需要 `el`。

```text
el build -o build/counter.exe src/main.el
el build --release src/main.el
```

`-o` 与 `--output` 是同一个选项身份，指定别的输出路径；`--release` 选择 release 安全检查等级，默认是 debug，`--debug` 与 `--release` 互斥。入口文件也可以用 `.els` 扩展名；`.els` 与 `.el` 一样由 `el run` 接受，区别只在宿主安装关联上，当前两者共享同一套顶层语句语义。

给程序传参数时写在入口文件之后，`el run` 会原样转交并保持次序：`el run src/main.el --demo`。

!!! success "检查点"
    - [ ] `el build src/main.el` 打印产物的绝对路径，Windows 上是 `src\main.exe`
    - [ ] 双击产物，出现同样的窗口，不经过 `el`

## 完整源码

```text
counter/
├── package.eol
└── src/
    ├── main.el
    ├── state.el
    └── view.el
```

`src/state.el`：

```el
@assign(mode: "shared")
export class Counter {
	let #value: Number = 0
	let #steps: Number = 0
	constructor() { init this }
	get value(): Number { return this.#value }
	get steps(): Number { return this.#steps }
	fn increase() { this.#value++; this.#steps++ }
	fn decrease() { this.#value--; this.#steps++ }
	fn reset() { this.#value = 0 }
	fn summary(): Text => "值 " + Text(this.#value) + "，已操作 " + Text(this.#steps) + " 次"
}
```

`src/view.el`：

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

`src/main.el`：

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

## 改成你自己的

1. **记录历史。** 把每次操作追加到一个数组，再加一个 `label` 显示最近几条；拼接文本用 `Text.join` 或文本库的 `join_text`。验收：连点五次能看到最近五条记录，清零也留下一条。
2. **键盘操作。** 用 `window.onArrow((dx, dy) => ...)` 接收方向键，左右键分别对应 `+1`／`-1`，鼠标点击仍然可用。验收：按键时窗口不失去焦点，两个入口改的是同一个状态。
3. **自动保存。** 在 `runWindow` 之前用文件的写入口保存当前值，程序重启后恢复；清理逻辑放进 `try` 的 `finally`。验收：关窗再开，值还在。

顺便：给根元素赋 `Theme(...)` 可以换主题，见[图形界面](../stdlib/gui.md)的主题小节，两个窗口可以各自覆盖。

## 卡住了？

- **现象：窗口一闪就没了，或者终端直接结束。** 装配顺序反了，`runWindow` 必须最后调用，它一返回程序就往下走。检查：确认 `runWindow(window)` 在 `main.el` 的最后一行。
- **现象：点按钮值变了，界面文字不动。** 改的是局部变量，或者处理器里漏了 `update()`；只有定义字段赋值才会发布变更。检查：在 `update` 里加一次输出，看点击时它有没有被调用。
- **现象：清零按钮一直可点。** `update` 里没有设置 `reset.enabled`，或者只在建树时算了一次。检查：确认 `update` 在每次状态变化后都执行。
- **现象：秒数不动。** 间隔不在 10 到 2147483647 之间，或者取句柄的 id 和 `element` 里写的不一致。检查：打印 `clock` 拿到的是不是 `void`，再把间隔换回 1000 试。

## 带走这三样

- 状态用 `@assign(mode: "shared")` 的类保存，界面只读状态、只转发事件。
- 定义字段赋值会自动发布变更，刷新靠“改字段”，不靠手动重绘。
- `runWindow` 阻塞，装配在前；窗口一关，定时器与句柄一起失效。

## 下一站：[手写 JSON 解析器](json-parser.md)

> 窗口里的输入框总要读懂用户贴进来的 JSON，那么“文本 → 结构”这一步，能不能不靠正则、只靠一层层拼装规则完成？

- 主推进：[手写 JSON 解析器](json-parser.md)：用 Parser 组合子从字面量拼到数组与对象，再对照手写递归下降。
- 想先看别的输出方式：[命令行工具](cli-tool.md)：同一个项目骨架，全部输出到终端。
