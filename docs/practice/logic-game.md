# 实战：规则式下棋机器人

这一页不写下棋算法：没有 minimax，没有评估函数，也不维护开局库。我们只把「棋子怎么放、怎样算赢」写成规则，让搜索去填「下在哪里」这个空；井字棋（tic-tac-toe）小到能在一页里看完，正好当例子。

规则、搜索和语义标记由逻辑库提供，下面的代码假定这些名字已经导入：

```el
import { rules, search, Ordered } from "el:logic/index.el"
```

## 目标与边界

目标是一个规则模块：给它一个当前棋盘和轮到的棋子，它回答该下哪一格。棋盘、落子、胜负、选择优先级全部写在 `rules` 里；调用方只负责把棋盘送进去、把答案拿回来。

刻意不做的事：不估分，不提前剪枝，不建「最佳着法」表。井字棋的搜索空间很小，规则加子句次序就够用；换成更大的棋盘，这份规则首先是一个合法性检查器，而不会自动变成强棋手。

下面代码按规范里的表面语法书写；本文讲写法和语义，不声明这些示例已在当前版本编译或运行通过。

## 规则模块与事实子句

`rules { ... }` 返回一个管理对象：关系句柄挂在 `.relations`，显式调用入口挂在 `.entries`。`relation` 声明关系的名字与元数，之后的事实子句和带 `if` 的规则子句都追加到同一关系上。

```el
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

let first: Text = route.entries.targets("A")[0]
```

`edge("A", "B")` 是事实子句：关系名后面直接给参数，没有 `if`。`reach` 有两条子句，分别表示「直接有一条边」和「先走一条边、再递归到达」；`|` 枚举分支，`&` 要求两个目标同时成立，`&` 比 `|` 结合得更紧，括号用来分组。

规则参数里的裸名建立逻辑变量，每次调用都会重新新鲜化；同一个子句里重复出现的名字表示同一个变量。`middle` 只出现在 `reach` 的子句体里，这种分支局部变量不必先声明。

`entry` 把关系包装成普通调用形状：`in source` 是输入，`out target as Text` 是输出并指定原生类型。取 `[0]` 只是拿第一个交付的答案；默认语义下并不承诺它就是源码里第一条子句的答案，这要等后面讲 `Ordered` 才成立。

## 完整规则

把整盘棋写成一个 `rules` 块。`place` 管落子位置，`wins` 管三连，`opponent` 把两个棋子对上，`choose` 按三层优先级选择落点。

```el
let game = rules {
	relation place(mark, move, before, after)
	place(mark, 0, [" ", b1, b2, b3, b4, b5, b6, b7, b8],
		[mark, b1, b2, b3, b4, b5, b6, b7, b8])
	place(mark, 1, [b0, " ", b2, b3, b4, b5, b6, b7, b8],
		[b0, mark, b2, b3, b4, b5, b6, b7, b8])
	place(mark, 2, [b0, b1, " ", b3, b4, b5, b6, b7, b8],
		[b0, b1, mark, b3, b4, b5, b6, b7, b8])
	place(mark, 3, [b0, b1, b2, " ", b4, b5, b6, b7, b8],
		[b0, b1, b2, mark, b4, b5, b6, b7, b8])
	place(mark, 4, [b0, b1, b2, b3, " ", b5, b6, b7, b8],
		[b0, b1, b2, b3, mark, b5, b6, b7, b8])
	place(mark, 5, [b0, b1, b2, b3, b4, " ", b6, b7, b8],
		[b0, b1, b2, b3, b4, mark, b6, b7, b8])
	place(mark, 6, [b0, b1, b2, b3, b4, b5, " ", b7, b8],
		[b0, b1, b2, b3, b4, b5, mark, b7, b8])
	place(mark, 7, [b0, b1, b2, b3, b4, b5, b6, " ", b8],
		[b0, b1, b2, b3, b4, b5, b6, mark, b8])
	place(mark, 8, [b0, b1, b2, b3, b4, b5, b6, b7, " "],
		[b0, b1, b2, b3, b4, b5, b6, b7, mark])

	relation wins(mark, board)
	wins(m, [m, m, m, c3, c4, c5, c6, c7, c8])
	wins(m, [c0, c1, c2, m, m, m, c6, c7, c8])
	wins(m, [c0, c1, c2, c3, c4, c5, m, m, m])
	wins(m, [m, c1, c2, m, c4, c5, m, c7, c8])
	wins(m, [c0, m, c2, c3, m, c5, c6, m, c8])
	wins(m, [c0, c1, m, c3, c4, m, c6, c7, m])
	wins(m, [m, c1, c2, c3, m, c5, c6, c7, m])
	wins(m, [c0, c1, m, c3, m, c5, m, c7, c8])

	relation opponent(mine, theirs)
	opponent("X", "O")
	opponent("O", "X")

	relation choose(mark, board, move)
	choose(mark, board, move) if place(mark, move, board, after) & wins(mark, after)
	choose(mark, board, move) if opponent(mark, other) & (
		place(other, move, board, threat) & wins(other, threat)
	)
	choose(mark, board, move) if place(mark, move, board, _)
}
```

## 落子：place

棋盘是 9 个元素组成的列表逻辑项：空格是 `" "`，棋子是 `"X"` 与 `"O"`。它不是原生数组，而是一个用 `[...]` 模板写成的有限逻辑项；位置靠列表结构区分，规则按形状匹配，不需要下标。

`place(mark, move, before, after)` 的意思是：在 `before` 棋盘的 `move` 位置放下 `mark`，得到 `after`。每个位置一条子句，共 9 条；子句头里的 `" "` 负责匹配空格，共享的 `b0` 到 `b8` 让没有被改动的格子原样保留。

子句头本身就是模式。以位置 0 为例，`place(mark, 0, [" ", b1, ...], [mark, b1, ...])` 的第一个参数 `mark` 也出现在 `after` 的第一格，重复变量让这两处必须取同一个值；8 个 `b` 变量在前后两个列表里各出现一次，于是它们绑定的格子前后不变。

位置 0 到 8 的子句按顺序写。在 `Ordered` 下，这个书写顺序就是搜索枚举空位的顺序。

## 胜负：wins

`wins(mark, board)` 说棋盘上有一条由 `mark` 占满的线。8 条线各一条子句；每条子句用重复变量 `m` 把这条线的三个格子绑到同一个值，其余 6 个格子用 `c` 变量接收，不关心它们具体是什么。

这是典型的模式头：没有 `if` 体的事实也可以含变量，调用时引擎把头部与目标合一，重复的 `m` 同时检查第一参数与三个格子。因此它匹配任何三连，而不只是某一种棋子。

声明里的参数名 `mark`、`board` 只是位置说明；子句头用自己的变量名，重复与否才决定约束。三条横线、三条竖线、两条对角线分别对应一条子句，写错一条就等于漏判一种赢法。

## 选择：choose

`choose(mark, board, move)` 分三层：能立刻赢就赢，对手下一手能赢就堵，否则任意空位。三层写成三条子句，靠顺序表达优先级。

第一条子句先落子再检查 `wins`，`after` 是分支局部变量：只要存在一个让 `mark` 成线的落点，这一层就给出答案。

第二条子句先由 `opponent(mark, other)` 把 `other` 绑定为对手棋子，再用 `place(other, move, board, threat)` 检查对手在 `move` 落子后能赢，于是我们也下在 `move` 堵住。没有 `opponent` 这一步，`other` 可能绑定到空格，规则会把「空格自己连成线」也当成威胁，答案就脏了。

第三条子句退化为任意空位：`place(mark, move, board, _)` 成功即表示 `move` 还没被占；`_` 每次独立，不参与输出。

这套规则不检查轮到谁、棋盘本身是否合法，也不检查是否已经终局；这些前提由调用方保证，或再加一条前置关系来检查。

## 让搜索去找落点

下面把棋盘钉成一个局面：`X` 占 0、1，`O` 占 4，轮到 `O`。`O` 没有立刻成线的落点，但 `X` 在位置 2 有威胁，所以答案应当是 2。

```el
let answers = search(semantics: Ordered) {
	fresh board, move
	unify(board, ["X", "X", " ", " ", "O", " ", " ", " ", " "])
	call $(game.relations.choose)("O", board, move)
	yield move as Number
}.ground().collect()
let move: Number = answers[0]
```

`fresh` 声明两个逻辑变量。`unify(board, [...])` 把棋盘钉成 9 个元素的逻辑项；若不先钉住，`board` 就是自由变量，搜索会去枚举所有可能的棋盘。`call $(game.relations.choose)(...)` 在搜索里调用关系句柄，`$()` 是外层表达式进入逻辑目标的入口；`"O"` 直接作为文本项传入。`yield move as Number` 声明输出的原生类型。

`.ground()` 在取答案时检查残余约束并解码成原生值，`.collect()` 把所有答案收成一个原生数组。答案里可能出现重复：同一个落点可能同时被第一层和第三层选中，`Ordered` 会原样保留重复。

如果把棋盘换成让 `O` 自己成线的局面，同一段代码会由第一层给出答案；如果棋盘上谁都没有威胁，则落到第三层，按位置顺序返回第一个空位。

## Ordered 与默认的 Declarative

`search` 默认使用 `Declarative` 语义：它交付满足答案合同的集合，不承诺首解，也不承诺枚举顺序；同一投影按有限项结构、真实名义身份和未约束变量的重命名去重。执行计划可以在不改变答案合同的前提下重排目标、使用索引或启发式，源码子句次序不是默认屏障。

`Ordered` 是另一份合同：从左到右的目标、源码子句次序的深度优先搜索，保留重复；无限分支可能挡住后续答案。它才是「先赢、再堵、再随便」这种过程读法成立的地方。

规则文本没变，变的是答案语义。若把上面的 `search` 改成默认语义，得到的仍是一组合法落点，但调用方不能指望第一个就是优先级最高的那一层；这也意味着 `once`、`cut`、`scope` 这类过程剪枝在默认计划里没有位置。

需要指定搜索策略时还可以传 `strategy:`；例如 `DepthFirstSearch` 要求配合 `Ordered`，冲突的选项会在准备阶段被拒绝，而不是被悄悄改写成另一种语义。

## 预算与结束状态

`limit:` 给一次搜索定非负整数步数上限，`-1` 表示没有显式上限。预算按准备与枚举分别计算，每个 iterator 独立；嵌套否定共享当前这一轮的预算。计数粒度包括准入、分支展开、索引、调度、目标、子句候选和答案比较，不承诺墙钟或内存上限。

```el
let cursor = search(semantics: Ordered, limit: 10000) {
	fresh board, move
	unify(board, ["X", "X", " ", " ", "O", " ", " ", " ", " "])
	call $(game.relations.choose)("O", board, move)
	yield move as Number
}.ground().iterator()
let step = cursor.next()
if (!step.done) {
	let first: Number = step.value
	console.log.value(first)
}
let status = cursor.status
cursor.close()
```

游标的结束状态分别是 `active`、`exhausted`、`closed`、`cancelled`、`limited` 与 `failed`。只有正常耗尽才是 `exhausted`；`next()` 返回的 `done` 只表示没有下一项，不能替代结束原因。

预算耗尽得到 `limited`，取消、失败、提前 `close()` 各有自己的状态。这些状态都不是「无解」，更不是证明了 `False`：它们只说明这次搜索没有交付更多答案，规则本身是否有解仍需要别的证据。

`complete` 只在集合合同下全量正常完成时为真；`Ordered` 的枚举即使跑完，也不因此获得原解集「已完成」的声明。普通枚举的 `optimal` 始终为假，最优化要另走携带证据的入口。

## 对照 Prolog

这段规则读起来很像 Prolog：关系名、事实、`|` 与 `&`、逻辑变量、匿名 `_`。但 EL 的关系接口默认是集合答案语义加自适应策略，不以 Prolog 的深度优先与源码子句次序为兼容约束，也不把 Prolog 当作兼容目标。

需要 Prolog 那种过程读法时，显式选择 `Ordered`；需要集合答案和无序枚举时，保持默认。把两种语义混着用最容易出错的地方，是把默认搜索结果当成「第一个解」，或者把 `cut` 当成结果序列的 `take(1)`。

## 再加一点功能

- 把棋盘从 3×3 换成 4×4 或五子棋，只需改列表长度和 `wins` 里的线。
- 给界面加一个 `entry`，用显式 `in`／`out` 把规则调用包装成普通函数形状。
- 让 `X` 也走同一套规则：把 `choose` 调用里的 `"O"` 换成 `"X"`，规则本身不用动。
- 想判断「对手有没有必胜点」，仍用 `wins` 与 `place` 组合；要表达「没有」，需要分层或 ground 的否定，不能把搜索失败当证明。
- 把 `status` 和 `delivered` 接到日志或界面上，`limited` 时不要显示「无解」。

## 继续阅读

- [像 Lean 一样证明](proofs.md)：同一门语言里的归纳类型、证明前端与内核重检。
- [函数与闭包](../language/functions.md)：`fn`、`match`、递归与块体返回值，规则之外的普通计算。
