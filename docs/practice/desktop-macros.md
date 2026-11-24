# 用桌面宏定时按键、看血条和登录

> 让 EL 在半秒左右敲一次键。搞清楚它在向哪个窗口发送输入，再把规则换成看血条决定是否按键。

!!! abstract "🎯 做完这个项目，你能"
    - 运行一段在指定编辑器前台时发送五次按键的脚本
    - 通过截图的颜色比例判断一条固定样式的血条是否低于阈值
    - 打开本机练习页，填写账号与密码并核对表单结果

    <span class="el-chip">⏱ 约 20 分钟</span> <span class="el-chip">前置：[函数与闭包](../language/functions.md)</span>

!!! note "实现状态"
    本页以桌面自动化和计时模块的源码为依据，EL 示例尚未运行。按键需要宿主授权，截图示例使用 Windows 或 Linux X11 的区域捕获。Wayland 上应按桌面实际提供的能力选择入口。

## 第一步：先让编辑器收到五次按键

打开一个空白编辑器，在脚本中把 `title` 换成它当前的完整窗口标题。把下面的完整程序保存为 `tap.el`。运行后有三秒切回编辑器。

```el
import { sleep } from "el:concurrency/index.el"
import { Random } from "el:random/index.el"
import { DesktopInput, WindowSelector, WindowTextMatch, findActiveDesktopWindow } from "el:desktop-automation/index.el"

let title = "把这里换成完整窗口标题"
let target = WindowSelector(title: WindowTextMatch(title))
let random = Random()
let input = DesktopInput()
try {
	sleep(3s)
	for (let count = 0; count < 5; count++) {
		sleep(random.between(430, 570) * 1ms)
		if (findActiveDesktopWindow(target) is nil_t) break
		input.sendKeys("A")
	}
} finally {
	input.close()
}
```

```sh
el run tap.el
```

预期在空白编辑器中看到五个 `a`，实际字符由键盘布局、修饰键和编辑器决定。把 `A` 换成应用绑定的道具键，就得到定时使用道具的基本结构。这里的等待时间每次独立抽取，单位为毫秒。

??? question "先猜：第三次按键之后切走，会发生什么？"
    脚本在发送下一键之前重新查前台窗口。查不到匹配就结束循环。查询和发送之间仍可能切换焦点，所以先用空白编辑器练习。

!!! example "动手 30 秒"
    把循环次数改成 3，保留编辑器前台，检查是否收到三次键。再跑一次，中途切走，检查脚本是否结束。

## 第二步：手动校准血条区域

把下面的完整程序保存为 `bar.el`。填入血条扫描线的桌面坐标、宽度和目标窗口标题。示例把偏红像素计作填充、近黑像素计作空白。先只输出判断，再启用按键。

```el
import { sleep } from "el:concurrency/"
import { DesktopPoint, DesktopInput, WindowSelector, WindowTextMatch, captureScreen, imagePixel, findActiveDesktopWindow } from "el:desktop-automation/"

let width = 100
let origin = DesktopPoint(120, 80)
let target = WindowSelector(title: WindowTextMatch("换成练习窗口的完整标题"))
let dryRun = t

fn healthPercent(): Number | nil_t {
	let frame = captureScreen(origin, width, 1)
	try {
		let filled = 0
		for (let x = 0; x < width; x++) {
			let pixel = imagePixel(frame.image, x, 0)
			if (pixel.red > 150 & pixel.green < 100 & pixel.blue < 100) filled++
			else if (pixel.red > 30 | pixel.green > 30 | pixel.blue > 30) return nil
		}
		return 100 * filled / width
	} finally {
		frame.close()
	}
}

sleep(3s)
let input = if (dryRun) nil else DesktopInput()
try {
	for (let sample = 0; sample < 20; sample++) {
		if (findActiveDesktopWindow(target) is nil_t) break
		let percent = healthPercent()
		if (percent is nil_t) {
			console.stdout.writeLine("血条颜色不匹配，停止")
			break
		}
		console.stdout.writeLine("血量：", percent, "%")
		if (percent < 30) {
			console.stdout.writeLine("低于补药阈值")
			if (input isnot nil_t & findActiveDesktopWindow(target) isnot nil_t) input.sendKeys("Q")
			sleep(2s)
		} else sleep(250ms)
	}
} finally {
	if (input isnot nil_t) input.close()
}
```

```sh
el run bar.el
```

把扫描线放在一条前 25 像素纯红、后 75 像素黑色的测试图条上，预期输出 `血量：25%` 和 `低于补药阈值`。满血、刚好 30%、低血各测一次，只有低血触发。黑色也可能来自尚未绘制的画面，接入真实界面时，额外采样一个只会出现在血条边框上的定位像素，确认坐标和缩放对应当前界面。校准后把 `dryRun` 改为 `f`，把 `Q` 换成练习应用的药水键；每次触发后有两秒冷却，20 次采样后退出。

## 第三步：打开自己的练习页并填写登录表单

将[登录练习页](fixtures/login-demo.html)保存到一个空目录，以 `login-demo.html` 命名。在该目录运行下面的命令，把练习页提供给本机浏览器。

```sh
python -m http.server 8766 --bind 127.0.0.1
```

保存下面的完整程序为 `login.el`，在另一扇终端运行 `el run login.el`。页面打开后应自动聚焦空账号框。如果浏览器弹出密码管理器或恢复了旧输入，先关闭弹窗并清空输入框。

```el
import { sleep } from "el:concurrency/"
import { DesktopInput, WindowSelector, WindowTextMatch, WindowTextMode, findActiveDesktopWindow, openDesktopUri } from "el:desktop-automation/"

let target = WindowSelector(title: WindowTextMatch("EL 本机登录练习 271", WindowTextMode.Contains))
fn requirePracticeWindow() {
	if (findActiveDesktopWindow(target) is nil_t) throw "练习页不在前台"
}

openDesktopUri("http://127.0.0.1:8766/login-demo.html")
for (let attempt = 0; attempt < 50; attempt++) {
	if (findActiveDesktopWindow(target) isnot nil_t) break
	sleep(100ms)
}
requirePracticeWindow()
let input = DesktopInput()
try {
	requirePracticeWindow()
	input.sendText("demo")
	requirePracticeWindow()
	input.sendKeys("Tab")
	requirePracticeWindow()
	input.sendText("practice-only")
	requirePracticeWindow()
	input.sendKeys("Enter")
} finally {
	input.close()
}
```

预期页面显示“练习登录成功”。故意把教学密码改错一次，页面应改为“账号或密码不匹配”。练习页在浏览器内核对固定示例值，表单无网络提交。窗口标题和键盘焦点会受浏览器设置影响，这个例子只使用页面上公开的测试值。需要真实凭据时，应使用拥有明确站点匹配的浏览器密码管理器或以可信浏览器接口定位来源和表单的自动化，提交后核对网站返回的登录状态。

## 下一站：[从 Excel 导出分类结果](workbook-to-csv.md)

把脚本里的“取输入、按规则判定、做动作”换成“读工作表、归类、输出文件”，就能把同一种思路用在办公批处理中。
