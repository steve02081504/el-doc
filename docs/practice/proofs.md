# 实战：像 Lean 一样证明

这一页用 EL 自己的归纳类型和证明前端，证明自然数加法的三条基本事实：加零、加后继、加法交换律。写法与 Lean 的归纳证明并排看很接近，但两边是不同实现；下面会一直把「证明骨架相同」和「实现相同」分开。

先准备两个名字：`Prop` 是命题的 sort，`Eq` 是命题等式。两者都按真实声明身份解析，不按拼写给任何定理开特权。

```el
import { Prop, Eq } from "el:language/proofs.el"
```

`prove { ... }` 是产生证明请求的源码前端：它接收目标类型与局部上下文，维护带作用域的目标列表，最后输出候选核心项。前端只能生成候选，不能生成用户可伪造的已检查证明；候选完整、约束已解且核心项通过内核重检，才算完成。

## 先定义自然数与加法

```el
data Nat { zero; succ(pred: Nat) }

fn add(n: Nat, m: Nat): Nat {
	match n {
		zero => m
		succ k => succ(add(k, m))
	}
}
```

`data` 声明两个构造子，`zero` 是常元，`succ` 带一个 `Nat` 字段。构造子可以写 `Nat.zero`／`Nat.succ`，也可以在同一模块里写短名；模式里写 `zero`、`succ k` 就是在匹配这两个构造子。

`add` 对第一个参数做结构递归：`zero` 时返回第二个参数，`succ k` 时先递归求 `add(k, m)`，再套一层 `succ`。这是普通可归约定义，没有算术魔法；证明里展开 `add`，就是按这两条定义做归约和重写。

目标类型用 Π 写。`addZero : Πn. Eq(Nat, add(n, zero), n)` 在代码里写成 `fn addZero(n: Nat): Eq(Nat, add(n, zero), n)`，Π 的 binder 就是函数参数。

`Eq` 的第一个参数是等式所在的载体类型，后面两个是左右端。本页统一写全 `Eq(Nat, 左, 右)`，形状和标准库 `mathematics/arithmetic/natural.el` 里的真实证明一致；写成别的载体时，检查的是另一个类型上的等式，不会因为两端都由 `add` 产生就被自动接受。

## 同一套 data 还能声明索引族

```el
data Le: Nat -> Nat -> Prop {
	z(n: Nat): Le(zero, n)
	s(a: Nat, b: Nat, p: Le(a, b)): Le(succ(a), succ(b))
}
```

`Le` 的构造子结果类型带下标，于是同一个 `data` 同时声明了类型族和它的引入规则。本页不证明 `Le` 的定理，列在这里是为了说明 `data` 不止能声明无索引的 `Nat`，而证明前端会按真实构造子身份分派，不按名字猜。

## 证明的形状：目标、分支与归纳假设

三条目标并排写出来：

```text
addZero : Πn. Eq(Nat, add(n, zero), n)
addSucc : Πa b. Eq(Nat, add(a, succ(b)), succ(add(a, b)))
addComm : Πa b. Eq(Nat, add(a, b), add(b, a))
```

`addZero` 与 `addSucc` 对第一个参数归纳；`addComm` 先证前两条，再对 `a` 归纳并泛化 `b`，因为归纳假设要对任意 `b` 成立。`prove` 里的命令只操作当前目标；要对多个分支执行同一段命令，必须显式写 `all { ... }`，不让 `simp` 隐式跨分支。

这些命令的集合与行为是工程默认，不是对所有 tactic 的承诺。复杂归纳自动化与搜索策略的覆盖有限，但这不影响证明检查的严格性：结果最终都要过内核。

## 零：refl

```el
fn zeroAdd(n: Nat): Eq(Nat, add(zero, n), n) => prove { refl }
```

`add` 的第一条定义式让 `add(zero, n)` 归约为 `n`，目标两侧在定义上相等，`refl` 请内核确认这种转换。它不是「相信我」的标记：转换不成立时它失败，而不是把坏命题变成真。

## 归纳：simp 与上下文里的归纳假设

```el
fn addZero(n: Nat): Eq(Nat, add(n, zero), n) => prove {
	induction n
	all { simp [add] }
}

fn addSucc(a: Nat, b: Nat): Eq(Nat, add(a, succ(b)), succ(add(a, b))) => prove {
	induction a
	all { simp [add] }
}
```

`addZero` 的 zero 分支是 `Eq(Nat, add(zero, zero), zero)`，展开 `add` 后两侧都是 `zero`，由反身性关闭。succ 分支里，上下文中有归纳假设 `Eq(Nat, add(k, zero), k)`；先把 `add(succ(k), zero)` 展开成 `succ(add(k, zero))`，再用归纳假设把它重写成 `succ(k)`，两侧相同。

`addSucc` 的 zero 分支：`add(zero, succ(b))` 归约为 `succ(b)`，右边 `succ(add(zero, b))` 也归约为 `succ(b)`。succ 分支里归纳假设是 `Eq(Nat, add(k, succ(b)), succ(add(k, b)))`；目标左边展开一次得到 `succ(add(k, succ(b)))`，右边展开得到 `succ(add(succ(k), b))`，再用 `add` 的定义把里层展开，最后用归纳假设把 `add(k, succ(b))` 换成 `succ(add(k, b))`，两侧一致。

`all { simp [add] }` 的意思是：对每个分支执行同一块命令；`simp` 展开列出的透明定义，并把当前上下文里的 `Eq` 当作定向重写，所以归纳假设会被用上。若需要更细的控制，把 `all` 拆成几个 `case`，逐个命令展开即可——下一节就是这样写的。

## 交换律：显式分支与 calc

```el
fn addComm(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	induction a generalizing b
	case Nat.zero b { simp [add, addZero] }
	case Nat.succ k, hypothesis, b { simp [add, addSucc, hypothesis] }
}
```

`induction a generalizing b` 把 `b` 放回每个分支的上下文，使归纳假设对整个 `b` 成立。`case` 后面的名字按「构造子字段、归纳假设、被泛化的变量」排列：zero 没有字段和归纳假设，所以写 `case Nat.zero b`；succ 分支写 `case Nat.succ k, hypothesis, b`。构造子可以写全 `Nat.zero`、`Nat.succ`，也可以在同一模块里用短名；`case` 按真实构造子身份选择分支，不按标签文本比较。

zero 分支的目标是 `Eq(Nat, add(zero, b), add(b, zero))`。`simp [add, addZero]` 先把 `add(zero, b)` 展开成 `b`，再用 `addZero` 把 `add(b, zero)` 改写成 `b`，两侧相同。

succ 分支的目标是 `Eq(Nat, add(succ(k), b), add(b, succ(k)))`：展开 `add` 得到 `succ(add(k, b))`；用 `addSucc` 把 `add(b, succ(k))` 改写成 `succ(add(b, k))`；再用归纳假设 `hypothesis` 把 `add(k, b)` 换成 `add(b, k)`，两侧都是 `succ(add(b, k))`。

同一段推理也可以写成显式的 `calc`，读起来更接近手算：

```el
fn addCommByCalc(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	induction a generalizing b
	case Nat.zero b {
		calc {
			add(zero, b) = b by zeroAdd(b)
				= add(b, zero) by reverse addZero(b)
		}
	}
	case Nat.succ k, hypothesis, b {
		simp [add, addSucc, hypothesis]
	}
}
```

zero 分支的 `calc` 从左边出发：第一步用 `zeroAdd(b)` 得到 `add(zero, b) = b`；第二步用 `reverse addZero(b)` 得到 `b = add(b, zero)`。链的两端正好是目标两端，`calc` 按实际证据构造传递项，端点与方向都逐项检查。succ 分支仍用 `simp`，因为主要动作是展开定义和重写归纳假设，写成 `calc` 反而更长。

也常见把整个归纳交给 `all { simp [add, addZero, addSucc] }` 的写法。本文不宣称这个简化集一定能关掉所有分支，所以上面把每步要展开什么、归纳假设在哪里用写清楚。

## 改写与引用：rewrite、exact

```el
fn addOne(n: Nat): Eq(Nat, add(n, succ(zero)), succ(n)) => prove {
	rewrite [addSucc(n, zero), addZero(n)]
	refl
}

fn succEqAddOne(n: Nat): Eq(Nat, succ(n), add(n, succ(zero))) => prove {
	exact reverse addOne(n)
}
```

`rewrite [p]` 用 `p` 的等式按方向替换目标中的子项，每一步生成传递或运输证明，不能把它当作内核转换。这里先用 `addSucc(n, zero)` 把 `add(n, succ(zero))` 改写成 `succ(add(n, zero))`，再用 `addZero(n)` 把里层的 `add(n, zero)` 改写成 `n`，最后 `refl` 关闭。

`exact` 直接给出证明项，不做证明搜索：`reverse addOne(n)` 把 `addOne(n)` 的等式反向，端点正好是当前目标。类型或端点对不上时 `exact` 失败，不会退化成「先猜一个」。

`calc` 和 `rewrite` 的分工也在这里显出来：`calc` 适合把一串等式按读者顺序写出来，每步用 `by` 给证据；`rewrite` 适合在当前目标里做定向替换。两者都只是构造候选证明项的命令，最终仍要过内核。

## 洞与承认：都不是证明

```el
fn addCommSketch(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	exact ?commutativity
}
```

`?name` 是具名洞，`?_` 是匿名洞。洞保存当前位置、目标类型与局部上下文，是待填目标；它不构造核心证明项，也不把目标标为已证明。同一 prove 请求内具名洞不能重复，匿名洞每次独立；洞不是类型、运行值、逻辑变量或公理，普通表达式里的 `?`、`?.`、`??` 和规则里的逻辑变量各有自己的含义，不能借用洞的语义。

含洞的声明不进入已检查环境，不导出接口，也不能用于定义转换、优化、代码生成或证明别的定理。正常编译含未完成声明的模块时，构建与测试必须失败；可以保存编辑器草稿，但没有让洞通过的构建开关。草稿不是定理。

```el
fn addCommAdmitted(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	admit "先承认，后面再补"
}
```

`admit` 是另一套机制：在当前位置的合法上下文 Γ 中，它为目标 P 产生带源码身份的显式假设 `ΠΓ.P`，再用这个假设取得 P 的条件证据。内核检查通过只说明「在这些承认假设下这个项合类型」，不是 P 的无缺口证明。每个承认位置和它传递到的使用都会记录成 admission 依赖；普通构建必须报告这些依赖，完整数学验收要求依赖为空。

`admit` 不能填运行数据，不能伪造被信任的实现或优化资格，也不能隐藏任意残余目标；`sorry` 也不设成它的别名。它和待填洞的区别是：洞让证明无法发布，`admit` 让证明带着假设发布，并在依赖报告里留下痕迹。

还要把「未决」和上面两种分开：证明搜索的步数、深度与取消由独立预算控制，预算耗尽、取消或数据库执行失败保留未决／失败状态，既不能推出无解，也不能推出否定或已检查证明。只有候选完整并通过内核重检、依赖报告也如实列出的结果，才能叫已检查证明；内核检查通过本身也不表示没有显式公理依赖。

## 和 Lean 并排

Lean 一侧的代码只作对照；EL 一侧的 `prove` 只是前端，生成候选后必须通过内核重检。下面只对照证明骨架，不把 Lean 的可运行性当成 EL 的当前实现。

```text
-- Lean 写法（仅对照，不是 EL 代码）
theorem addZero (n : Nat) : n + 0 = n := rfl
```

Lean 的 `Nat.add` 递归第二个参数，所以 `n + 0` 在定义上就归约为 `n`，`rfl` 足够。EL 的 `add` 递归第一个参数，`add(n, zero)` 只随 `n` 的构造子逐步展开，所以要归纳。这说明同名、同记号不等于同一组定义方程；跨两种定义方向时，`addZero` 与 `addSucc` 这类桥接引理是必要的。

```text
-- Lean 写法（仅对照，不是 EL 代码）
theorem addComm (a b : Nat) : a + b = b + a := by
	induction a generalizing b with
	| zero => simp
	| succ k ih => simp [Nat.succ_add, ih]
```

结构是同构的：对 `a` 归纳并泛化 `b`，zero 分支收尾，succ 分支用归纳假设重写。EL 版本对应地写成 `induction a generalizing b`、zero 分支用 `calc`、succ 分支用 `simp` 加归纳假设，归纳假设出现的位置一致。

差别在可用的命令集合、定义方向和 `Eq` 的声明身份：Lean 的一条 `simp` 可能关掉 EL 前端需要几步才能关掉的分支，EL 的 `refl`／`rewrite`／`calc` 目前是工程默认的那一小套。不要把这段 Lean 的可运行当成 EL 已实现同样的自动化，也不要把 EL 的这几条定理外推成完整的 Lean 体验。

## 检查清单

- 先写清目标与定义方向，再选归纳变量；归纳假设要覆盖整个分支时写 `generalizing`。
- 每步注明展开哪条定义、用了哪条引理、归纳假设在哪一步重写，别让 `simp` 自动走太远再回头猜。
- `?name` 只留在草稿；`admit` 只用于显式承认并接受依赖报告；预算未决不冒充结论。
- 判断完成看内核重检与依赖报告，不看 `prove` 块有没有写完。

## 继续阅读

- [规则式下棋机器人](logic-game.md)：用 `rules` 与 `search` 声明规则，让搜索去找答案。
- [控制流](../language/control-flow.md)：分支、模式匹配与块体返回值，读懂 `match` 与 `case` 之外的普通控制流。
