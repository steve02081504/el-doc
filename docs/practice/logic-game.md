# 实战：规则式下棋机器人

> 不写下棋算法：没有 minimax，没有评估函数，也不维护开局库。那“该下哪一格”这个答案，到底从哪来？

!!! abstract "🎯 做完这个项目，你能"
    - 用 `relation` 与事实子句写出棋盘、落子与胜负
    - 用 `search` 把“下哪一格”交给搜索，而不是自己写 minimax
    - 说清 `Ordered` 与默认 `Declarative` 的差别，知道默认语义下不能指望首解
    - 读游标状态，区分“没有更多答案”与“预算耗尽”

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：逻辑关系、搜索、答案语义</span>

## 目标与边界

规则式写法适合能拆成“事实 + 关系 + 优先级”的问题：写清“什么算赢”，让搜索去填“下哪里”；需要数值打分或启发式剪枝的场合不适合。

项目是一个规则模块：给它棋盘和轮到的棋子，它回答该下哪一格。刻意不做：不估分、不剪枝、不建“最佳着法”表。井字棋（tic-tac-toe）的搜索空间很小，规则加子句次序就够用；换成大棋盘，它首先只是一个合法性检查器。

验收：`route.entries.targets("A")[0]` 返回 `Text`；第四步钉住的局面上第一个落点是 2；去掉 `Ordered` 后答案集合不变，但第一个不再保证是最高优先级。

规则、搜索和语义标记由逻辑库提供，代码假定这些名字已经导入：

```el
import { rules, search, Ordered } from "el:logic/index.el"
```

!!! note "实现状态"
    下面代码按规范里的表面语法书写。本文讲写法和语义，不声明这些示例已在当前版本编译或运行通过。

## 第一步：先看清“规则”是什么形状

`rules { ... }` 返回管理对象：关系句柄在 `.relations`，显式调用入口在 `.entries`；`relation` 声明名字与元数，事实子句和带 `if` 的规则子句都追加到同一关系。

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

`edge("A", "B")` 是事实子句：关系名后直接给参数，没有 `if`；`reach` 两条子句分别表示“直接有边”和“先走一条边再递归到达”，`|` 枚举分支，`&` 要求同时成立，`&` 比 `|` 更紧，括号分组。

裸名是逻辑变量，每次调用重新新鲜化，同一子句里重复的名字是同一个变量；`middle` 只在子句体里出现，分支局部变量不必声明。`entry` 把关系包成普通调用形状：`in source` 输入，`out target as Text` 输出并指定原生类型；`[0]` 只是取第一个交付的答案，默认语义不承诺它是源码第一条子句的答案。

!!! success "检查点"
    - [ ] `route.entries.targets("A")` 交付 B 与 C 两个答案
    - [ ] 删掉 `edge("B", "C")` 后，从 A 到达 C 的答案消失

## 第二步：棋盘、落子与胜负

整盘棋写成一个 `rules` 块：`place` 管落子位置，`wins` 管三连，`opponent` 把两个棋子对上，`choose` 按三层优先级选择落点。

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

棋盘是 `[...]` 模板写成的有限逻辑项，不是原生数组：`" "` 是空格，`"X"`／`"O"` 是棋子，位置靠列表结构区分，不需要下标。

`place(mark, move, before, after)` 在 `before` 的 `move` 处放下 `mark` 得到 `after`：每位置一条子句共 9 条，子句头的 `" "` 匹配空格，共享的 `b0` 到 `b8` 让没动的格子原样保留。子句头就是模式：位置 0 的 `mark` 同时出现在 `after` 第一格，重复变量要求同值；8 个 `b` 变量前后各出现一次，绑定的格子不变。位置 0 到 8 的顺序在 `Ordered` 下就是枚举空位顺序。

`wins(mark, board)` 说棋盘上有一条由 `mark` 占满的线：8 条线各一条子句，重复变量 `m` 把线上三格绑到同一个值，其余 6 格用 `c` 接收。没有 `if` 体的事实也能含变量：引擎把子句头与目标合一，重复的 `m` 同时检查第一参数与三个格子，所以它匹配任何三连。`mark`、`board` 只是位置说明，子句头用自己的变量名，重复与否才决定约束；三条横线、三条竖线、两条对角线各一条，写错一条就漏判一种赢法。

!!! success "检查点"
    - [ ] `place` 正好 9 条子句，缺一条就有一个格子永远下不了
    - [ ] 删掉一条对角线子句，只有那条线上的三连会漏判
    - [ ] 把位置 0 子句里的 `[" ", ...]` 改成 `[b0, ...]`，空格匹配立刻失效

## 第三步：优先级就是子句顺序

`choose(mark, board, move)` 三层：能立刻赢就赢，对手下一手能赢就堵，否则任意空位；子句顺序就是优先级。第一条先落子再查 `wins`，`after` 是分支局部变量。

第二条先由 `opponent(mark, other)` 把 `other` 钉成对手棋子，再检查对手在 `move` 落子后能赢，所以我们下在 `move` 堵住；没有 `opponent`，`other` 可能绑到空格，把“空格自己连成线”当成威胁。

第三条退化为任意空位：`place(mark, move, board, _)` 成功即表示 `move` 未占；`_` 每次独立。

??? question "先猜：把第二条子句里的 `opponent(mark, other)` 删掉，程序会怎样？"
    答案里会混进空格。`other` 成了自由变量，搜索会试着让空格自己在某个位置连成线，“威胁”层因此给出无效落点。

这套规则不检查轮到谁、棋盘是否合法、是否终局，这些前提由调用方保证。

!!! success "检查点"
    - [ ] 自己有成线机会时，第一个答案是成线的那一格
    - [ ] 对手有成线威胁时，答案里出现堵点的位置

## 第四步：让搜索去找落点

钉住局面：`X` 占 0、1，`O` 占 4，轮到 `O`；`O` 没有立刻成线的落点，但 `X` 在位置 2 有威胁，答案应当是 2。

```el
let answers = search(semantics: Ordered) {
	fresh board, move
	unify(board, ["X", "X", " ", " ", "O", " ", " ", " ", " "])
	call $(game.relations.choose)("O", board, move)
	yield move as Number
}.ground().collect()
let move: Number = answers[0]
console.stdout.writeLine("move: ", move)
```

```text
move: 2
```

`fresh` 声明逻辑变量；`unify(board, [...])` 把棋盘钉成 9 元素逻辑项，不钉住 `board` 就是自由变量、会枚举所有棋盘。`call $(game.relations.choose)(...)` 在搜索里调用关系句柄，`$()` 是外层表达式进入逻辑目标的入口；`yield move as Number` 声明输出类型。

`.ground()` 检查残余约束并解码成原生值，`.collect()` 收成原生数组。答案可能重复：同一落点可能同时被第一层和第三层选中，`Ordered` 原样保留。让 `O` 自己成线时第一层就给答案；谁都没威胁时落到第三层，按位置顺序返回第一个空位。

!!! success "检查点"
    - [ ] 钉住的局面上 `move` 是 2，说明第二层在堵 `X` 的威胁
    - [ ] 谁都没有威胁的棋盘上，答案是位置顺序里的第一个空位
    - [ ] 去掉 `unify` 后搜索变慢甚至跑不完，因为 `board` 成了自由变量

## 第五步：同一份规则，两种答案语义

`search` 默认 `Declarative`：交付满足答案合同的集合，不承诺首解与枚举顺序；同一投影按有限项结构、真实名义身份和未约束变量的重命名去重。执行计划可以重排目标、使用索引或启发式，源码子句次序不是默认屏障。

`Ordered` 是另一份合同：从左到右的目标、源码子句次序的深度优先搜索，保留重复，无限分支可能挡住后续答案；它才是“先赢、再堵、再随便”成立的地方。

规则没变，变的是语义：去掉 `semantics: Ordered` 仍得到一组合法落点，但第一个不再保证是优先级最高的那层；`once`、`cut`、`scope` 这类过程剪枝在默认计划里没有位置。`strategy:` 可以指定策略，例如 `DepthFirstSearch` 要求配合 `Ordered`，冲突的选项会在准备阶段被拒绝。

它读起来像 Prolog：关系名、事实、`|` 与 `&`、逻辑变量、匿名 `_`；但默认语义不以深度优先与源码子句次序为兼容约束，把默认结果当“第一个解”、把 `cut` 当 `take(1)` 最容易错。

预算也是这份合同的一部分：`limit:` 定非负整数步数上限，`-1` 表示没有显式上限；预算按准备与枚举分别计算，每个 iterator 独立，嵌套否定共享当前这一轮的预算。计数粒度包括准入、分支展开、索引、调度、目标、子句候选与答案比较，不承诺墙钟或内存上限。

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

游标的结束状态有 `active`、`exhausted`、`closed`、`cancelled`、`limited` 与 `failed`；只有正常耗尽才是 `exhausted`，`next()` 返回的 `done` 只表示没有下一项。

预算耗尽得到 `limited`，它和取消、失败、提前 `close()` 一样都不是“无解”，更不是证明了 `False`：只说明这次搜索没有交付更多答案。`complete` 只在集合合同下全量正常完成时为真；`Ordered` 的枚举即使跑完，也不获得原解集“已完成”的声明。普通枚举的 `optimal` 始终为假，最优化要另走携带证据的入口。

!!! success "检查点"
    - [ ] 带 `Ordered` 时第一个答案由第一层优先给出；去掉它，答案集合不变但顺序不再保证
    - [ ] 把 `limit` 改成 1，状态是 `limited` 而不是 `exhausted`
    - [ ] 预算耗尽时界面或日志不该显示“无解”

## 完整源码

```text
tic-tac-toe/
├── package.eol
└── src/
    ├── game.el
    └── main.el
```

`src/game.el` 是文件顶部的导入行，加上第二步那个完整的 `rules` 块（从 `let game = rules {` 到最后的 `}`），一字不改；再把 `let game` 改成 `export let game`，`main.el` 才能导入。第一步的 `route` 只是教学用的最小模型，不进最终文件。

```el
import { search, Ordered } from "el:logic/index.el"
import { game } from "file:./game.el"

let answers = search(semantics: Ordered) {
	fresh board, move
	unify(board, ["X", "X", " ", " ", "O", " ", " ", " ", " "])
	call $(game.relations.choose)("O", board, move)
	yield move as Number
}.ground().collect()
console.stdout.writeLine("move: ", answers[0])
```

## 改成你自己的

1. **让 `X` 也走同一套规则。** 把调用里的 `"O"` 换成 `"X"`，规则本身不用动。验收：同一个局面上 `X` 给出合法落点。
2. **把棋盘换大。** 换成 4×4 或五子棋：列表加长、`place` 子句同步加、`wins` 的线按新棋盘重写。验收：任意一条线都能被判出胜负。
3. **包成普通函数，并回答“对手有没有必胜点”。** 用 `entry` 的显式 `in`／`out` 包装一次调用；“对手没有必胜点”要用分层或 ground 的否定表达，不能把搜索失败当证明。验收：`entry` 调用形状像普通函数，否定结论有明确证据来源。

## 卡住了？

- **现象：每次搜索都返回同一个落点，优先级看不出来。** 没写 `semantics: Ordered`，默认集合语义不承诺首解。检查：加上 `Ordered` 再跑。
- **现象：答案里出现空格，或“威胁”位置根本不存在。** 第二条 `choose` 子句缺了 `opponent`。检查：确认 `opponent(mark, other)` 在 `place(other, ...)` 之前。
- **现象：搜索很慢，内存一直涨。** `board` 没被 `unify` 钉住，自由变量在枚举所有棋盘。检查：`fresh` 之后第一句就 `unify`。
- **现象：`limited` 被当成“无解”展示。** 结束状态只说明这次没有更多答案。检查：打印 `cursor.status` 区分两者。

## 带走这三样

- 规则式问题拆成事实、关系、优先级三层，答案空间交给搜索。
- `Ordered` 是“先赢、再堵、再随便”成立的前提；默认语义只承诺答案集合。
- 结束状态不是无解：`limited`、`cancelled`、`failed` 都不能当否定证据。

## 下一站：[定理证明](proofs.md)

> 规则能回答“下哪里”，但它不证明任何事。要证明“对任意自然数都成立”，又该写什么？

- 主推进：[定理证明](proofs.md)：用归纳类型与证明前端，让每一步都过内核重检。
- 想补普通计算：[函数与闭包](../language/functions.md)：`fn`、`match`、递归与块体返回值。
