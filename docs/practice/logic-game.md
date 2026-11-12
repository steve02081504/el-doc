# 做一个能点着玩的规则式下棋机器人

!!! abstract "🎯 做完这页，你能"
    - 用二维矩阵保存棋盘，用关系规则读取坐标和假设落子
    - 区分默认答案集合与 Ordered 的过程顺序
    - 接起九按钮窗口，处理终局、搜索失败、重试和重开

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">前置：[函数与闭包](../language/functions.md)、[GUI 应用](gui-app.md)</span>

> 棋盘已经能写 `board[row,column]`，为什么还要手写九条落子规则？

这个项目保留真正的二维棋盘：玩家执 X 先手，机器人执 O。你点击空格，规则给机器人选点，窗口更新棋子和状态；结束后能重开，机器人计算失败能重试。它的策略是“能赢就赢，否则堵住立即威胁，否则选行列最靠前的空位”，并不保证不败。

!!! note "实现状态"
    示例对应 EL 仓库 `examples/gui/tic-tac-toe/` 的源码与已登记回归。当前尚未完成编译、EL 测试或真实平台窗口验证；需要具备当前语法和标准库支持的 EL。搜索同步运行在窗口线程，计算期间不保证即时响应重开或关窗。

## 第一步：事实是输入，关系描述规律

`rules` 返回管理对象：`.relations` 放关系句柄，`.entries` 放显式普通调用入口。先用一个小图观察它们：

```el
import { rules } from "el:logic/"

let route = rules {
	relation edge(source, target)
	edge("A", "B")
	edge("A", "C")
	edge("B", "C")
	relation reach(source, target) if edge(source, target) | (
		edge(source, middle) & reach(middle, target)
	)
	entry targets = reach(in source, out target as Text)
}
let targets = route.entries.targets("A").collect()
```

`edge` 是事实，`reach` 是直接可达或经过中间点可达。`&` 要求同时成立，`|` 枚举分支，`&` 优先级更高。裸名是逻辑变量；同一子句重复的名字必须同值，每次调用会产生新的变量身份。`as Text` 指定原生输出类型。

!!! success "检查点"
    - [ ] A 的答案集合包含 B 和 C，不依赖哪个先交付
    - [ ] 删除 `edge("B", "C")` 后，B 不再到达 C；A 仍由直接边到达 C

## 第二步：矩阵保持二维，规则读取快照

```el
let board = @(
	1, 1, 0;
	0, 2, 0;
	0, 0, 0
)
```

0 是空格，1 是 X，2 是 O。外层程序读写 `board[row,column]`；规则构造时把每个格子读一次，导入普通三列事实 `[row,column,mark]`。这只枚举当前九个输入格子，不枚举全部可能棋盘，也不手工列出九种着法。

`rulesFor` 里的 `at(unchanged(),r,c,mark)` 读取原局面。`at(put(r,c,mark),...)` 表示假设在一个空格落子：目标格取新棋子，其余格保留快照值。`dif([r,c],[mr,mc])` 比较整个坐标对；写成两个坐标分别不等的合取，会错误丢掉同一行或同一列的其它格子。

胜负只需四类模式：一条横向规则覆盖全部三行，一条纵向规则覆盖全部三列，另加两条对角线。`player(mark)` 排除空格连成线。原生索引仍是普通前向访问，关系 `cell` 才能在未知坐标上枚举；给普通 getter 换个名字不会让它自动可逆。

!!! example "动手：看清行列"
    把上面的盘传给完整源码中的 `chooseMove(board, 2)`。预期坐标是 `row=0, column=2`，用于堵住 X；原矩阵该格仍为 0。

## 第三步：优先级是显式数据

`candidate` 给每个合法落点附上 tier：0 表示自己立即获胜，1 表示对手立即获胜而应阻挡，2 表示普通空位。`chooseMove` 在默认 Declarative 下读完整集合，再选 `(tier,row,column)` 最小者。因此重排规则或改变合法执行顺序，不应改变策略。

同一个位置可能出现在不同 tier 中，这是不同候选；同一完整投影的多条证明会按默认集合合同去重。四角形成的双威胁仍可能击败机器人，浅层策略没有做 minimax。

`Ordered` 则承诺从左到右、按源码子句次序的深度优先过程，保留重复。用它才能把三条有序 choose 子句的首个见证当作过程选择。这里使用显式 tier，不需要依赖首解；不要仅把默认搜索的第一个结果当作最优落点。

## 第四步：搜索结束不一定表示搜索完整

`next().done` 可能来自耗尽、取消、预算或关闭。项目在取得所有候选后检查 `cursor.complete`，未完成就抛 `SearchInterrupted`；即使已经拿到候选，也不会用不完整集合冒充最终选择。cursor 和 plan 分别在 finally 中关闭。

`limit` 是工作步数预算，不是墙钟上限；准备与枚举分别应用预算。`Game` 的 outcomeLimit 和 moveLimit 分别控制胜负检查和选点，默认 100000 尚未经过运行测量。预算不足时可以调整实例上的预算再重试，不要无限自动重试同一份失败计算。

!!! success "检查点"
    - [ ] `chooseMove(board, 2, 0)` 应报告搜索中断，不能返回“无候选”
    - [ ] 完整搜索得到空候选才返回 void；平局另由“无赢家且满盘”判断

## 第五步：先准备完整结果，再发布到窗口

`Game.play` 在独立矩阵上准备玩家落子，先判胜再判满盘。准备失败时原棋盘不动；玩家已经成功落子、机器人随后失败时，保留玩家盘并启用“重试机器人”。重试只补机器人一步。发布阶段的异常向窗口循环传播，不能被包装成“未提交”继续对弈。

视图不拥有另一份业务棋盘：九个按钮只显示 `game.board`，控制器自己检查轮次、占位和坐标，不能只依赖按钮禁用。每次绑定捕获独立坐标；回调弱引用视图，关闭会解绑并关闭游戏。视图单独成文件，便于用同一套输入分派测试九个按钮。

## 完整源码

将四个文件放在同一目录。导入标准库使用 `el:`，项目文件使用相对 `file:`。

```text
tic-tac-toe/
├── rules.el
├── game.el
├── view.el
└── main.el
```

```sh
el run tic-tac-toe/main.el
```

### `rules.el`

```el
import { rules, search, SearchInterrupted } from "el:logic/"
import { Tensor } from "el:numerical-computing/"

export fn blankBoard() => @(0, 0, 0; 0, 0, 0; 0, 0, 0)

export fn inside(row: Number, column: Number): Bool {
	return row >= 0 & row < 3 & row % 1 == 0 &
		column >= 0 & column < 3 & column % 1 == 0
}

fn checkBoard(board: Tensor<element: Number>) {
	if (board.rank != 2 | board.rowCount() != 3 | board.columnCount() != 3)
		throw "Expected a 3 by 3 board"
}

// 通用数据适配，不是胜线表或着法表。每格只读一次。
fn cellRows(board: Tensor<element: Number>): Number[][] {
	checkBoard(board)
	let rows: Number[][] = @[]
	for (let row = 0; row < board.rowCount(); row++) {
		for (let column = 0; column < board.columnCount(); column++) {
			let mark = board[row, column]
			if (mark != 0 & mark != 1 & mark != 2) throw "Unknown board mark"
			rows.push(@[row, column, mark])
		}
	}
	return rows
}

export fn rulesFor(board: Tensor<element: Number>) {
	return rules {
		relation cell(row, column, mark) from $(cellRows(board))
		relation player(mark) from @[@[1], @[2]]
		relation opponent(mine, theirs) from @[@[1, 2], @[2, 1]]

		// unchanged() 与 put(...) 是内部有限逻辑结构项。
		// at 只是“在当前盘或假设落一子后的盘中读取格子”。
		relation at(change, row, column, mark)
		at(unchanged(), r, c, mark) if cell(r, c, mark)
		at(put(r, c, mark), r, c, mark) if player(mark) & cell(r, c, 0)
		at(put(mr, mc, placed), r, c, mark) if
			player(placed) & cell(mr, mc, 0) & cell(r, c, mark) &
			dif([r, c], [mr, mc])

		relation wins(change, mark) if player(mark) & (
			at(change, r, 0, mark) & at(change, r, 1, mark) & at(change, r, 2, mark) |
			at(change, 0, c, mark) & at(change, 1, c, mark) & at(change, 2, c, mark) |
			at(change, 0, 0, mark) & at(change, 1, 1, mark) & at(change, 2, 2, mark) |
			at(change, 0, 2, mark) & at(change, 1, 1, mark) & at(change, 2, 0, mark)
		)

		relation winningMove(mark, row, column) if
			player(mark) & cell(row, column, 0) &
			wins(put(row, column, mark), mark)

		// tier 是明确的策略层级，不依赖默认搜索的枚举顺序。
		relation candidate(mark, row, column, tier)
		candidate(mark, r, c, 0) if winningMove(mark, r, c)
		candidate(mark, r, c, 1) if opponent(mark, other) & winningMove(other, r, c)
		candidate(mark, r, c, 2) if player(mark) & cell(r, c, 0)
	}
}

// 只检查满盘；胜负必须先调用 winner。
export fn isFull(board: Tensor<element: Number>): Bool {
	checkBoard(board)
	for (let row = 0; row < 3; row++) {
		for (let column = 0; column < 3; column++) {
			if (board[row, column] == 0) return nil
		}
	}
	return t
}

// 返回 0=无人获胜、1=X、2=O。双赢家是非法盘，不随便挑一方。
export fn winner(board: Tensor<element: Number>, limit: Number = 100000): Number {
	let game = rulesFor(board)
	let plan = search(limit: limit) {
		call game.relations.wins(unchanged(), mark)
		yield mark as Number
	}
	try {
		let cursor = plan.ground().iterator()
		try {
			let result = 0
			while (t) {
				let step = cursor.next()
				if (step.done) break
				if (result != 0 & result != step.value) throw "Both players have winning lines"
				result = step.value
			}
			if (!cursor.complete) throw SearchInterrupted(cursor.status)
			return result
		} finally { cursor.close() }
	} finally { plan.close() }
}

// 调用前提：合法的进行中棋局，mark 为轮到的一方。
// 返回坐标记录，满盘无候选返回 void；预算/取消/错误不会变成 void。
export fn chooseMove(board: Tensor<element: Number>, mark: Number,
	limit: Number = 100000) {
	if (mark != 1 & mark != 2) throw "Expected X or O"
	let game = rulesFor(board)
	let plan = search(limit: limit) {
		call game.relations.candidate($(mark), row, column, tier)
		yield [row as Number, column as Number, tier as Number]
	}
	try {
		let cursor = plan.ground().iterator()
		try {
			let best: Number[] = @[]
			while (t) {
				let step = cursor.next()
				if (step.done) break
				let item = step.value
				let better = best.count == 0
				if (!better) {
					better = item[2] < best[2] | (
						item[2] == best[2] & (item[0] < best[0] |
							(item[0] == best[0] & item[1] < best[1]))
					)
				}
				if (better) best = item
			}
			if (!cursor.complete) throw SearchInterrupted(cursor.status)
			if (best.count == 0) return void
			return @{row: best[0], column: best[1]}
		} finally { cursor.close() }
	} finally { plan.close() }
}
```

### `game.el`

```el
import { assign } from "el:language/contracts.el"
import { Tensor } from "el:numerical-computing/"
import { SearchInterrupted } from "el:logic/"
import { blankBoard, inside, winner, chooseMove, isFull } from "file:./rules.el"

fn failureText(error): Text {
	if (error is SearchInterrupted) {
		if (error.reason == "limited") return "搜索预算耗尽"
		if (error.reason == "cancelled") return "搜索已取消"
		return "搜索未完成"
	}
	return "计算或资源清理失败"
}

// 完整准备成功后才交给控制器发布，不把搜索放进提交阶段。
@assign(mode: "shared") class PreparedTurn {
	let board: Tensor<element: Number>
	let phase: Text
	let message: Text
	constructor(board: Tensor<element: Number>, phase: Text, message: Text) {
		init this; this.board = board; this.phase = phase; this.message = message
	}
}
fn prepareTurn(board: Tensor<element: Number>, nextPhase: Text, nextMessage: Text, limit: Number): PreparedTurn {
	let outcome = winner(board, limit)
	if (outcome == 1) return PreparedTurn(board, "human-won", "你赢了！")
	if (outcome == 2) return PreparedTurn(board, "bot-won", "机器人赢了")
	if (isFull(board)) return PreparedTurn(board, "draw", "平局")
	return PreparedTurn(board, nextPhase, nextMessage)
}

export @assign(mode: "shared") class Game {
	let #board = blankBoard()
	let #phase: Text = "human"
	let #revision: Number = 0
	let #message: Text = "你执 X，请落子"
	let outcomeLimit: Number
	let moveLimit: Number
	constructor(outcomeLimit: Number = 100000, moveLimit: Number = 100000) {
		if (outcomeLimit < 0 | outcomeLimit % 1 != 0 | moveLimit < 0 | moveLimit % 1 != 0) throw "Expected finite nonnegative search budgets"
		init this
		this.outcomeLimit = outcomeLimit
		this.moveLimit = moveLimit
	}

	get board(): Tensor<element: Number> { return this.#board }
	get phase(): Text { return this.#phase }
	get revision(): Number { return this.#revision }

	fn summary(): Text { return this.#message }
	fn canRetry(): Bool { return this.#phase == "failed" }
	fn canPlay(row: Number, column: Number): Bool {
		if (this.#phase != "human" | !inside(row, column)) return nil
		return this.#board[row, column] == 0
	}

	fn #publish(next: PreparedTurn) {
		let revision = this.#revision + 1
		this.#phase = "publishing"
		this.#board = next.board
		this.#revision = revision
		this.#message = next.message
		this.#phase = next.phase
		// 发布失败向上传播并停止对弈，不被包装为“未提交”后继续。
	}

	fn play(row: Number, column: Number) {
		if (!this.canPlay(row, column)) return
		let prepared: PreparedTurn | void_t = void
		try {
			let next = this.#board
			next[row, column] = 1
			prepared = prepareTurn(next, "thinking", "机器人正在思考…", this.outcomeLimit)
		} catch (error) {
			this.#message = "这一步未提交：" + failureText(error) + "；可重试或重开"
			return
		}
		if (prepared is void_t) throw "Missing prepared turn"
		// 放在准备阶段的 catch 之外，不能吞掉可能的发布失败。
		this.#publish(prepared)
		if (this.#phase == "thinking") this.#bot()
	}

	fn #bot() {
		this.#phase = "thinking"
		this.#message = "机器人正在思考…"
		let expected = this.#revision
		let prepared: PreparedTurn | void_t = void
		try {
			let snapshot = this.#board
			let move = chooseMove(snapshot, 2, this.moveLimit)
			if (this.#phase != "thinking" | this.#revision != expected) return
			if (move is void_t) throw "Ongoing board has no candidate"
			if (!inside(move.row, move.column)) throw "Bot returned an invalid coordinate"
			if (this.#board[move.row, move.column] != 0) throw "Bot chose an occupied cell"
			let next = this.#board
			next[move.row, move.column] = 2
			let ready = prepareTurn(next, "human", "你执 X，请落子", this.outcomeLimit)
			if (ready.phase == "human-won") throw "Bot turn started from an ended game"
			prepared = ready
		} catch (error) {
			if (this.#phase != "thinking" | this.#revision != expected) return
			this.#phase = "failed"
			this.#message = "机器人未落子：" + failureText(error) + "；可重试或重开"
			return
		}
		if (this.#phase != "thinking" | this.#revision != expected) return
		if (prepared is void_t) throw "Missing prepared turn"
		this.#publish(prepared)
	}

	fn retry() { if (this.canRetry()) this.#bot() }
	fn restart() {
		if (this.#phase == "closed") return
		// 空盘和状态先准备成功，再改变当前局面或修订。
		let prepared = PreparedTurn(blankBoard(), "human", "你执 X，请落子")
		this.#publish(prepared)
	}
	fn close() {
		if (this.#phase == "closed") return
		this.#phase = "closed"
		this.#revision++
	}
}
```

### `view.el`

```el
import { assign } from "el:language/contracts.el"
import { Definition, GuiEvent, element, appendChild, on } from "el:user-interface/model.el"
import { WeakShared } from "el:memory/ownership/weak-shared.el"
import { Game } from "file:./game.el"

fn cellText(mark: Number): Text {
	return if (mark == 1) "X" else if (mark == 2) "O" else "·"
}

export @assign(mode: "shared") class GameView {
	let game: Game
	let root = element("column")
	let status = element("label", "你执 X，请落子", "status")
	let restart = element("button", "重新开始", "restart")
	let retry = element("button", "重试机器人", "retry")
	let cells: Definition[][] = @[]
	let #closed: Bool = nil

	constructor(game: Game = Game()) {
		init this
		this.game = game
		try {
			this.root.style.padding = 16
			this.root.style.gap = 10
			let boardView = element("column")
			boardView.style.gap = 8
			let controls = element("row")
			controls.style.gap = 8
			appendChild(this.root, "status", this.status)
			appendChild(this.root, "board", boardView)
			appendChild(this.root, "controls", controls)
			appendChild(controls, "restart", this.restart)
			appendChild(controls, "retry", this.retry)
			appendChild(this.root, "strategy", element("label", "先赢，再堵，再选空位；不保证永不输。"))
			let weak = WeakShared<element: GameView>(this)
			for (let row = 0; row < 3; row++) {
				let strip = element("row")
				strip.style.gap = 8
				let rowCells: Definition[] = @[]
				appendChild(boardView, Text(row), strip)
				for (let column = 0; column < 3; column++) {
					let cell = element("button", "·", "cell-" + Text(row) + "-" + Text(column))
					cell.style.width = 90
					cell.style.height = 90
					rowCells.push(cell)
					appendChild(strip, Text(column), cell)
					bindCell(weak, row, column, cell)
				}
				this.cells.push(rowCells)
			}
			on(this.restart, "click", (event: GuiEvent) => {
				let view = weak.lock()
				if (view is void_t) return
				view.game.restart(); view.render()
			})
			on(this.retry, "click", (event: GuiEvent) => {
				let view = weak.lock()
				if (view is void_t) return
				view.game.retry(); view.render()
			})
			this.render()
		} catch (error) { this.close(); throw error }
	}

	fn render() {
		if (this.#closed) return
		this.status.text = this.game.summary()
		let board = this.game.board
		for (let row = 0; row < 3; row++) {
			for (let column = 0; column < 3; column++) {
				let cell = this.cells[row][column]
				cell.text = cellText(board[row, column])
				cell.enabled = this.game.canPlay(row, column)
			}
		}
		this.retry.enabled = this.game.canRetry()
	}

	fn close() {
		if (this.#closed) return
		this.#closed = t
		this.game.close()
		for (let row in this.cells) for (let cell in row) cell.listeners.clear()
		this.restart.listeners.clear()
		this.retry.listeners.clear()
	}
	destructor() { this.close() }
}

// 坐标参数属于每次绑定；弱引用避免按钮回调形成拥有环。
fn bindCell(weak: WeakShared<element: GameView>, row: Number, column: Number, cell: Definition) {
	on(cell, "click", (event: GuiEvent) => {
		let view = weak.lock()
		if (view is void_t) return
		view.game.play(row, column)
		view.render()
	})
}
```

### `main.el`

```el
import { showWindow, runWindow } from "el:user-interface/window.el"
import { GameView } from "file:./view.el"

let view = GameView()
try { runWindow(showWindow(view.root, "井字棋 · 规则机器人", 380, 460)) }
finally { view.close() }
```

## 改成你自己的

1. **调整预算并观察失败状态。** 用 `Game(moveLimit: 0)` 创建视图，点击后应保留 X 并启用重试；提高 moveLimit 后重试，只出现一个 O。
2. **用同一套关系查另一方。** 给合法的进行中棋盘调用 `chooseMove(board, 1)`，确认返回空格且原盘未变。控制器仍保持玩家 X 先手。
3. **扩展矩形盘的连续 k 子。** 把固定三格模式换成四个方向与长度递减的关系，沿 `(dr,dc)` 递推；不需要按位置增加 place 表。验收包含矩形尺寸、边界、k=1、长连和预算，不能仅因棋盘有限就声称递归已取得耗尽证明。

## 卡住了？

- **堵错行列。** 检查事实列顺序是否为 row、column、mark，用第二步的非对称盘验证；不要按矩阵物理存储顺序猜坐标。
- **窗口显示搜索预算耗尽。** 记录错误与预算，提高对应实例预算后重试；这不是无解，也不是平局。
- **点击重复落子。** 检查事件是否只调用 Game.play，以及绑定时是否捕获了独立坐标；控制器不能被视图绕过。
- **思考时窗口不能立即响应。** 当前版本是同步搜索，计时器也不会自动变成后台执行；窗口后台任务与取消协议属于后续能力。

## 带走这三样

- 二维矩阵负责状态，关系快照负责查询，假设 put 不修改业务棋盘。
- 默认答案集合的策略优先级用 tier 表达，并在完整读取后选择。
- 交互程序必须区分准备失败、发布失败、终局和关闭，不能把任何搜索停止都当平局。

## 下一站：[定理证明](proofs.md)

规则求出见证，不等于任意命题都通过了证明内核。下一页用归纳类型与证明前端说明内核检查的边界。
