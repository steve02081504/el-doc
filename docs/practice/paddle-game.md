# 实战：做一个弹球游戏的第一面球拍

> 打开一个小球场，用方向键上下移动球拍，试着把弹来的球挡回去。

!!! abstract "🎯 做完这页，你能"
    - 写出会定时移动、碰到墙壁会反弹的小球
    - 用方向键移动球拍，并判断小球是否被挡住
    - 改变球速，观察同一套规则怎样产生不同体验

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">前置：[图形程序](gui-app.md)</span>

## 先做出能玩的球场

这一章做一个单人练习：球拍在左侧，上下方向键移动它；小球碰到上、下和右边的墙会反弹。球拍接住球后，小球向右返回；漏接时球回到中间，重新出发。窗口关闭后程序结束。本章先不计分，也没有第二位玩家。

!!! note "实现状态"
    下面的代码按 EL 仓库公开的网格和窗口接口，以及 `examples/gui/snake/` 的用法静态编写；尚未完成编译或真实窗口运行验证。需要可用的 EL 工具链和支持原生窗口的运行环境。

## 第一步：保存并运行完整程序

新建文件夹 `paddle-game`，在里面新建 `main.el`，把下面的完整程序保存进去。它没有单独的 `main` 函数：EL 从文件顶层开始执行。

```el
import { Grid } from "el:collections/grids.el"
import { showWindow, runWindow, element, appendChild, dataView } from "el:user-interface/"

let empty = @{ color: "black" }
let paddle = @{ color: "white" }
let ball = @{ color: "orange" }
let board = Grid<element: any>(12, 9, empty)

let paddleTop = 3
let ballX = 5
let ballY = 4
let velocityX = -1
let velocityY = 1

let root = element("column")
let status = element("label", "上下方向键移动球拍 · 漏接后重新发球")
appendChild(root, "status", status)
appendChild(root, "board", dataView(board))
let window = showWindow(root, "弹球练习", 600, 500)

fn draw() {
	for (let x = 0; x < 12; x++) for (let y = 0; y < 9; y++) board[x, y] = empty
	for (let offset = 0; offset < 3; offset++) board[1, paddleTop + offset] = paddle
	board[ballX, ballY] = ball
}

draw()
window.onArrow((dx, dy) => {
	let next = paddleTop + dy
	if (next >= 0 & next <= 6) paddleTop = next
	draw()
})
window.every(250, (timer) => {
	let nextY = ballY + velocityY
	if (nextY < 0 | nextY > 8) {
		velocityY = -velocityY
		nextY = ballY + velocityY
	}
	let nextX = ballX + velocityX
	if (nextX == 1 & nextY >= paddleTop & nextY < paddleTop + 3) {
		velocityX = 1
		nextX = ballX + velocityX
	}
	if (nextX > 11) {
		velocityX = -1
		nextX = ballX + velocityX
	}
	if (nextX < 0) {
		ballX = 5
		ballY = 4
		velocityX = -1
		velocityY = 1
	} else {
		ballX = nextX
		ballY = nextY
	}
	draw()
})
runWindow(window)
```

打开终端，进入 `paddle-game` 文件夹，运行：

```sh
el run main.el
```

预期看到黑色球场、左侧白色球拍和移动的橙色小球。按上、下方向键，球拍随之移动；把球拍移到小球前方，它会反向飞回去。关掉窗口，终端应回到提示符。

!!! success "检查点"
    - [ ] 小球碰到上、下或右边的边缘后改变方向
    - [ ] 用球拍接住小球后，小球向右移动
    - [ ] 故意漏接，小球回到场地中央继续移动

## 第二步：看懂坐标和速度

球场有 12 列、9 行，从左上角的 `(0, 0)` 开始。`ballX` 向右增大，`ballY` 向下增大。球拍固定在第 1 列，`paddleTop` 是它最上面一格的行号；球拍一共占三格。

每次定时器触发，程序用当前位置加速度算出下一格。`velocityX` 为 `-1` 表示向左，为 `1` 表示向右；竖直方向同理。碰到上下墙时把竖直速度取反，接住球时把水平速度改成向右。

??? question "先猜：为什么先算下一行，再判断球拍有没有接住？"
    球斜着移动时，接触球拍的高度是下一行，而不是出发时所在的行。先算下一行，才能用球实际到达的高度判断是否接住。

`draw()` 每次先清空网格，再按当前状态画球拍和球。它负责显示；位置和方向由前面的变量保存。

## 第三步：改变一个数字

把 `window.every(250, ...)` 中的 `250` 改成 `500`，保存后重新运行。这个数字以毫秒为单位，500 毫秒是半秒；预期小球每半秒走一格，比原来慢一倍。

!!! example "动手：给自己留更多反应时间"
    先将间隔设为 `500`，接住一次球；再改回 `250`。如果小球的位置更新更快，就看到了定时器间隔的作用。

## 接下来接上第二面球拍

进入[完整比赛](paddle-game-full.md)，把漏接改成对手得分，再接菜单、模式、皮肤与自动存档。原生窗口、手柄和浏览器的输入最终都应复用同一套动作。这样可以先用键盘跑通比赛，再逐个测试宿主。

## 改成你自己的

- 把球拍颜色换成另一种颜色，重新运行，确认球和背景仍容易分辨。
- 试着把球拍从三格改成两格。画球拍、限制移动范围和碰撞判断都要使用相同的长度；检查球拍不能移出场地。
- 漏接时在状态文字里显示提示。确认接球时不会误报漏接，重新开始后提示仍清楚。

## 卡住了？

- **终端找不到 `el`**：先按照[安装与运行](../getting-started.md)准备工具链，再在同一个终端检查命令是否可用。
- **提示找不到 `main.el`**：检查终端当前目录是否为保存文件的 `paddle-game`，以及文件扩展名是否确为 `.el`。
- **窗口无法打开或标准库接口报错**：核对 EL 工具链与标准库是否匹配，并确认当前环境支持原生窗口；本页示例尚未执行验证，保留完整报错以便排查。
- **球拍不响应方向键**：先点击游戏窗口使它获得键盘焦点，再按上、下方向键。

## 带走这三样

- 位置加速度得到下一位置，碰墙时改变方向。
- 用下一位置判断球是否碰到球拍，可以处理斜向移动。
- 状态与绘制分开，后面加比分、暂停和不同控制方式时更容易检查规则。

## 下一站：[计分、菜单和商店](paddle-game-full.md)

加上右球拍和比分，让这个球场能打完一局。
