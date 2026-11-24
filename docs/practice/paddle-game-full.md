# 给乒乓球加计分、菜单和商店

> 从一个球拍扩展到两边能得分的球场。打到 5 分结算，赢得的金币可以换球场配色。

!!! abstract "🎯 做完这页，你能"
    - 在人机与同机双人之间选择，并暂停、继续或确认重开
    - 检查比赛结算、金币和换肤各自何时发生
    - 为游戏接入存档、手柄和新宿主安排独立的验收步骤

    <span class="el-chip">⏱ 约 45 分钟</span> <span class="el-chip">前置：[第一个球场](paddle-game.md)</span>

!!! note "实现状态"
    下方原生 GUI 例子尚未编译或运行。跨平台手柄接线、浏览器宿主和在线多人需要单独实现与验证。

## 先做能打完一局的版本

新建一个练习目录，把程序保存为 `match.el`，运行 `el run match.el`。档案 `profile.csv` 写入当前目录，同一份档案一次只开一个游戏实例。上、下键控制左球拍。选同机双人时，第二位玩家按左、右键让右球拍上移、下移。两个球拍共用同一条移动规则。

```el
import { Grid } from "el:collections/grids.el"
import { showWindow, runWindow, element, appendChild, dataView, on, GuiEvent } from "el:user-interface/"
import { Theme } from "el:theme/"
import { resolvePath, publishFileAs } from "el:filesystem/"
import { formats, parseAs } from "el:formats/"
import { parse_integer } from "el:number/"

let board = Grid<element: any>(16, 10, @{color: "black"})
let root = element("column")
let menu = element("row")
let status = element("label")
appendChild(root, "menu", menu)
appendChild(root, "status", status)
appendChild(root, "board", dataView(board))

let phase = "menu"
let beforeConfirm = "menu"
let mode = "cpu"
let left = 3
let right = 3
let ballX = 8
let ballY = 4
let dx = -1
let dy = 1
let leftScore = 0
let rightScore = 0
let coins = 0
let rainbowOwned = f
let rainbow = f

fn applyTheme() {
	root.theme = if (rainbow) Theme(@{primary: 0x80A7F0}) else nil
}

fn saveProfile(nextCoins: Number, owned: Bool, selected: Bool) {
	let rows = @[@["1", Text(nextCoins), if (owned) "yes" else "no", if (selected) "yes" else "no"]]
	discard(publishFileAs(formats.CSV, "profile.csv", rows))
	coins = nextCoins
	rainbowOwned = owned
	rainbow = selected
	applyTheme()
}

let saved = resolvePath("profile.csv").readOptionalBytes(1024)
if (saved isnot nil_t) {
	let rows = parseAs(formats.CSV, saved)
	if (rows.count != 1) throw "存档应只有一行"
	let fields = rows[0]
	if (fields.count != 4) throw "存档应有四列"
	if (fields[0] != "1") throw "未知存档版本"
	let savedCoins = Number(parse_integer(fields[1]))
	if (savedCoins < 0) throw "存档余额不能为负"
	if ((fields[2] != "yes" & fields[2] != "no") | (fields[3] != "yes" & fields[3] != "no")) throw "存档皮肤值不合法"
	if (fields[2] == "no" & fields[3] == "yes") throw "不能使用未解锁皮肤"
	coins = savedCoins
	rainbowOwned = fields[2] == "yes"
	rainbow = fields[3] == "yes"
	applyTheme()
}

fn phaseLabel(): Text {
	switch (phase) {
		case "menu" => return "主菜单：请选择比赛模式"
		case "paused" => return "暂停菜单：继续或重开"
		case "confirm" => return "重开菜单：确认或取消"
		case "finished" => return "结算"
		default => return "比赛中"
	}
}

fn paint() {
	status.text = phaseLabel() + " · " + Text(leftScore) + ":" + Text(rightScore) + " · 金币 " + Text(coins)
	for let x in ..16 {
		for let y in ..10 board[x, y] = @{color: if (rainbow) "midnightblue" else "black"}
	}
	for let offset in ..3 {
		board[1, left + offset] = @{color: if (rainbow) "cyan" else "white"}
		board[14, right + offset] = @{color: if (rainbow) "magenta" else "white"}
	}
	board[ballX, ballY] = @{color: "orange"}
}

fn serve(direction: Number) {
	ballX = 8
	ballY = 4
	dx = direction
	dy = 1
}

fn start(selected: Text) {
	mode = selected
	left = 3
	right = 3
	leftScore = 0
	rightScore = 0
	serve(-1)
	phase = "playing"
	paint()
}

fn move(top: Number, change: Number): Number {
	let next = top + change
	return if (next < 0) 0 else if (next > 7) 7 else next
}

let window = showWindow(root, "乒乓球", 840, 520)

fn action(key: Text, label: Text, handler: fn(): nil_t) {
	let button = element("button", label)
	appendChild(menu, key, button)
	on(button, "click", (event: GuiEvent) => {
		handler()
		if (phase == "playing") window.input.focus = nil
	})
}

action("solo", "人机", fn() { if (phase == "menu" | phase == "finished") start("cpu") })
action("duo", "同机双人", fn() { if (phase == "menu" | phase == "finished") start("local") })
action("pause", "暂停 / 继续", fn() {
	if (phase == "playing") phase = "paused"
	else if (phase == "paused") phase = "playing"
	paint()
})
action("restart", "重开", fn() {
	if (phase == "playing" | phase == "paused" | phase == "finished") {
		beforeConfirm = phase
		phase = "confirm"
	}
	paint()
})
action("confirm", "确认重开", fn() { if (phase == "confirm") start(mode) })
action("cancel", "取消重开", fn() { if (phase == "confirm") { phase = beforeConfirm; paint() } })
action("menu", "主菜单", fn() { phase = "menu"; paint() })
action("shop", "商店 · 炫彩 10 金币", fn() {
	if (phase != "menu" & phase != "finished") return
	if (!rainbowOwned & coins < 10) return
	let price = if (rainbowOwned) 0 else 10
	saveProfile(coins - price, t, !rainbow)
	paint()
})

window.onArrow((horizontal, vertical) => {
	if (phase != "playing") return
	left = move(left, vertical)
	if (mode == "local") right = move(right, horizontal)
	paint()
})
window.every(200, (timer) => {
	if (phase != "playing") return
	if (mode == "cpu" & dx > 0) {
		if (right + 1 < ballY) right = move(right, 1)
		else if (right + 1 > ballY) right = move(right, -1)
	}
	let nextY = ballY + dy
	if (nextY < 0 | nextY > 9) {
		dy = -dy
		nextY = ballY + dy
	}
	let nextX = ballX + dx
	if (dx < 0 & nextX == 1 & nextY >= left & nextY < left + 3) {
		dx = 1
		nextX = ballX + dx
	}
	if (dx > 0 & nextX == 14 & nextY >= right & nextY < right + 3) {
		dx = -1
		nextX = ballX + dx
	}
	if (nextX < 0 | nextX > 15) {
		if (nextX < 0) rightScore++
		else leftScore++
		if (leftScore == 5 | rightScore == 5) {
			phase = "finished"
			saveProfile(coins + 10, rainbowOwned, rainbow)
		} else serve(if (nextX < 0) -1 else 1)
	} else {
		ballX = nextX
		ballY = nextY
	}
	paint()
})
paint()
runWindow(window)
```

按钮是常驻工具栏，`phase` 决定当前哪些动作生效。把它换成每种画面专属的按钮组时，先保留同样的状态转换。重开确认期间球不动，只有确认后比分才归零。用两个轴控制两位玩家是本练习的键位选择，方便先验收同机双人。

!!! example "核对暂停和结算"
    选同机双人，在 1:0 时暂停，等一秒后看球和比分是否原样。继续打到任一边 5 分，金币增加 10。点商店购买炫彩，再点一次切回经典配色，余额只扣一次。

## 自动保存和加载

程序在购买、换肤、结算时自动发布玩家档案，加载时检查格式版本、余额和皮肤状态。领取一局奖励并购买后，关闭程序再开启，检查余额、皮肤和解锁状态。用一个副本把首列版本改成 2，程序应拒绝读取该档。

要恢复未完成比赛，再保存球拍位置、球的位置和方向、模式、比分、状态及局号。以暂停状态恢复，让玩家决定何时继续。金币、已结算局号、比赛状态应在同一次档案发布中提交。先写候选档案，发布成功后更新画面上的余额。测试关闭重开、写入失败及重复打开结算页，三个路径都不能多发金币。

## 给游戏换宿主

| 目标 | 接线与验收 |
| --- | --- |
| Windows、Linux | 把键盘和窗口计时转成游戏动作与固定步进。在两端分别检查键位、焦点丢失和存档目录，验证真实窗口运行 |
| 手柄 | 将方向键、方向帽或摇杆映射到同一移动动作。给模拟轴设置死区，记住设备与玩家绑定；断开时清除该设备输入 |
| 网页 | 浏览器宿主提供帧回调、Canvas、键盘和手柄、可用的本地存储。输入事件只产生动作，按累计时间推进固定步数；页面隐藏再恢复时暂停，避免补跑一大段 |
| 在线多人 | 同机双人先验收。联机房间由权威端推进球与比分，按输入序号应用动作并发送快照；重连按最新快照恢复。奖励只接受完成局号一次 |

用同一份初始状态和动作记录，在各宿主回放固定的步数，比较球、比分与结算。平台发布命令要以可用的目标工具和宿主为准。

## 下一站：[三维瞄准练习器](aim-trainer.md)

保留输入、规则和呈现三层，把网格坐标换成三维位置和方向。
