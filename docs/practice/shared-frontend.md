# 用 EL GUI 做联动控制台

> 同一块计数器出现在两个窗口里。点右边加一，左边也更新，但左边的加一按钮始终灰着。

!!! abstract "🎯 做完这个项目，你能"
    - 用同一份定义呈现两个原生窗口，并让共享信号驱动主题切换
    - 共享业务数据，同时让一个视图拥有自己的交互状态
    - 说出将这个界面搬到浏览器还需要哪些宿主能力

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[图形程序](gui-app.md)</span>

!!! note "实现状态"
    代码依据 EL 仓库的 `examples/gui/shared-views/index.el`，尚未运行。浏览器发布依赖仍待实现的 Wasm GUI 宿主。

## 让两个窗口读同一个值

把程序存为 `shared-counter.el`，运行 `el run shared-counter.el`。两个窗口的计数都从 0 开始。点击“控制窗口”的按钮后，两边都显示 1。

```el
import { element, appendChild, on, GuiEvent } from "el:user-interface/model.el"
import { showWindow, runWindows } from "el:user-interface/window.el"
import { Theme } from "el:theme/"

let root = element("column")
root.style.padding = 20
root.style.gap = 12
let display = element("label", "脉冲 · 0", "count")
let meter = element("label", "等待输入", "meter")
let increment = element("button", "加一", "increment")
appendChild(root, "count", display)
appendChild(root, "meter", meter)
appendChild(root, "increment", increment)
let warm = Theme(@{primary: 0xF59E0B})
let cool = Theme(@{primary: 0x60A5FA})
root.theme = cool

let count: Number = 0
on(increment, "click", (event: GuiEvent) => {
	count++
	display.text = "脉冲 · " + Text(count)
	meter.text = if (count % 2 == 0) "冷色信号" else "暖色信号"
	root.theme = if (count % 2 == 0) cool else warm
})

let readOnly = showWindow(root, "展示窗口", 360, 210)
try {
	let controls = showWindow(root, "控制窗口", 460, 280)
	try {
		readOnly.getById("increment").enabled = f
		runWindows(@[readOnly, controls])
	} finally {
		controls.close()
	}
} finally {
	readOnly.close()
}
```

??? question "先猜：禁用一边的按钮，两边会一起灰掉吗？"
    这里只通过 `readOnly.getById` 改一个窗口的呈现实例。计数更新则写到共享定义 `display`，所以两边都能看到。

!!! example "动手 30 秒"
    把“展示窗口”拉宽，再点两下“控制窗口”的按钮。检查两边是否都显示 2，且仍各自使用自己的窗口尺寸。

## 从原生窗口走到网页

把同一份界面定义接到两个呈现宿主，做一个可点击的控制台和一个可投屏的只读展示台。修改共享数据时两处一起更新，各视图的焦点、窗口尺寸和按钮可用性分别变化；无需为第二个视图复制业务逻辑。

浏览器宿主需要把 EL 绘制输出接到 Canvas，同时为每处呈现同步语义 DOM 的角色、名称、焦点和动作。窗口尺寸变化、缩放、触屏和键盘输入也应通过对应事件适配。先用同一个网页里的两处呈现验收，再测跨标签页同步；跨标签页需要额外的消息与权限设计。网页打包入口待 Wasm GUI 宿主接通后补充。

| 验收动作 | 应看到的结果 |
| --- | --- |
| 点控制台三次 | 两处都显示 3 和暖色信号 |
| 只改变展示台尺寸 | 展示台重新排版，控制台的焦点与计数保持 |
| 用 Tab 和读屏打开浏览器版 | 可操作按钮有名称和焦点，禁用状态能读出 |
| 断开一个呈现再重连 | 重新显示当前计数；旧的事件监听器已释放 |

## 下一站：[弹球游戏](paddle-game.md)

计数器的状态只在点击时变化。游戏还需要定时更新位置，并按输入决定下一帧。
