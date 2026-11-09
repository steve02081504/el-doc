# 实战：像 Lean 一样证明

> 抽样测试只能说明“这次对”。要说明“对任意自然数都对”，你得写一份内核能重检的证明。

!!! abstract "🎯 做完这个项目，你能"
    - 用 `data` 声明归纳类型，用 `match` 写出按构造子归约的 `add`
    - 用 `prove` 的 `induction`、`all`、`simp` 关掉加零与加后继
    - 用 `case` 显式分支、用 `calc` 把交换律写成一行行等式
    - 分辨洞、`admit` 与内核重检，知道什么才算已检查证明

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：归纳类型、模式匹配、证明前端</span>

## 目标与边界

证明的写法适合回答“对所有输入都成立”这一类问题：测试只能覆盖样本，而完整候选证明要过内核重检。EL 的前端只产生候选，不产生用户可伪造的已检查证明；候选完整、约束已解且核心项通过重检，才算完成。

这一页证明自然数加法的三条基本事实：加零、加后继、加法交换律。写法与 Lean 的归纳证明并排看很接近，但两边是不同实现；下面一直把“证明骨架相同”和“实现相同”分开。

验收：三条定理都通过内核重检；把 `refl` 换成错的方向时构建失败；带洞的声明不能发布；`admit` 的位置出现在依赖报告里。

先准备两个名字：`Prop` 是命题的 sort，`Eq` 是命题等式。两者都按真实声明身份解析，不按拼写给任何定理开特权。

```el
import { Prop, Eq } from "el:language/proofs.el"
```

`prove { ... }` 是产生证明请求的源码前端：它接收目标类型与局部上下文，维护带作用域的目标列表，最后输出候选核心项。

## 第一步：先定义自然数与加法

```el
data Nat { zero; succ(pred: Nat) }

fn add(n: Nat, m: Nat): Nat {
	match n {
		zero => m
		succ k => succ(add(k, m))
	}
}
```

??? note "可选 · 深入：同一套 data 还能声明索引族"
    ```el
    data Le: Nat -> Nat -> Prop {
    	z(n: Nat): Le(zero, n)
    	s(a: Nat, b: Nat, p: Le(a, b)): Le(succ(a), succ(b))
    }
    ```
    `Le` 的构造子结果类型带下标，于是同一个 `data` 同时声明了类型族和它的引入规则。本页不证明 `Le` 的定理；列在这里是为了说明 `data` 不止能声明无索引的 `Nat`，而证明前端会按真实构造子身份分派，不按名字猜。

`data` 声明两个构造子，`zero` 是常元，`succ` 带一个 `Nat` 字段。构造子可以写 `Nat.zero`／`Nat.succ`，也可以在同一模块里写短名；模式里写 `zero`、`succ k` 就是在匹配这两个构造子。

`add` 对第一个参数做结构递归：`zero` 时返回第二个参数，`succ k` 时先递归求 `add(k, m)`，再套一层 `succ`。这是普通可归约定义，没有算术魔法；证明里展开 `add`，就是按这两条定义做归约和重写。

目标类型用 Π 写：`addZero : Πn. Eq(Nat, add(n, zero), n)` 在代码里写成 `fn addZero(n: Nat): Eq(Nat, add(n, zero), n)`，Π 的 binder 就是函数参数。`Eq` 的第一个参数是载体类型，后面两个是左右端；本页统一写全 `Eq(Nat, 左, 右)`，形状和标准库 `mathematics/arithmetic/natural.el` 里的真实证明一致。写成别的载体时，检查的是另一个类型上的等式，不会因为两端都由 `add` 产生就被自动接受。

!!! success "检查点"
    - [ ] `add(zero, m)` 归约为 `m`，`add(succ(k), m)` 归约为 `succ(add(k, m))`
    - [ ] 两条定义式就是后面所有证明能用的全部“算术”

## 第二步：定义相等的地方，`refl` 就够了

三条目标并排写出来：

```text
addZero : Πn. Eq(Nat, add(n, zero), n)
addSucc : Πa b. Eq(Nat, add(a, succ(b)), succ(add(a, b)))
addComm : Πa b. Eq(Nat, add(a, b), add(b, a))
```

先证最直接的一条：

```el
fn zeroAdd(n: Nat): Eq(Nat, add(zero, n), n) => prove { refl }
```

`add` 的第一条定义式让 `add(zero, n)` 归约为 `n`，目标两侧在定义上相等，`refl` 请内核确认这种转换。它不是“相信我”的标记：转换不成立时它失败，而不是把坏命题变成真。

!!! success "检查点"
    - [ ] `zeroAdd` 通过，因为它只用到 `add` 的第一条定义式
    - [ ] 把目标改成 `Eq(Nat, add(n, zero), n)` 后直接 `refl`，构建失败

## 第三步：归纳之后，归纳假设就在上下文里

??? question "先猜：`induction n` 之后，两个分支各自还剩什么要证？"
    zero 分支剩 `Eq(Nat, add(zero, zero), zero)`，succ 分支剩 `Eq(Nat, add(succ(k), zero), succ(k))`，而且上下文里多了归纳假设 `Eq(Nat, add(k, zero), k)`。`refl` 只关得掉第一个。

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

`all { simp [add] }` 的意思是：对每个分支执行同一块命令；`simp` 展开列出的透明定义，并把当前上下文里的 `Eq` 当作定向重写，所以归纳假设会被用上。`prove` 里的命令只操作当前目标，要对多个分支执行同一段命令必须显式写 `all { ... }`，不让 `simp` 隐式跨分支；需要更细的控制时，把 `all` 拆成几个 `case`，逐个命令展开。这些命令的集合与行为是工程默认，不是对所有 tactic 的承诺：复杂归纳自动化与搜索策略的覆盖有限，但这不影响内核重检的严格性。

!!! success "检查点"
    - [ ] 两条定理都过内核重检，`all { simp [add] }` 不需要列出归纳假设
    - [ ] 把 `all { simp [add] }` 换成只写 `simp [add]`，只有一个分支被处理
    - [ ] 把 `induction n` 换成 `induction a`，`addZero` 因变量不存在而失败

## 第四步：交换律要显式分支与 `calc`

`addComm` 先证前两条，再对 `a` 归纳并泛化 `b`，因为归纳假设要对任意 `b` 成立。

```el
fn addComm(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	induction a generalizing b
	case Nat.zero b { simp [add, addZero] }
	case Nat.succ k, hypothesis, b { simp [add, addSucc, hypothesis] }
}
```

`induction a generalizing b` 把 `b` 放回每个分支的上下文，使归纳假设对整个 `b` 成立。`case` 后面的名字按“构造子字段、归纳假设、被泛化的变量”排列：zero 没有字段和归纳假设，所以写 `case Nat.zero b`；succ 分支写 `case Nat.succ k, hypothesis, b`。构造子可以写全 `Nat.zero`、`Nat.succ`，也可以在同一模块里用短名；`case` 按真实构造子身份选择分支，不按标签文本比较。

zero 分支的目标是 `Eq(Nat, add(zero, b), add(b, zero))`：`simp [add, addZero]` 先把 `add(zero, b)` 展开成 `b`，再用 `addZero` 把 `add(b, zero)` 改写成 `b`。succ 分支的目标是 `Eq(Nat, add(succ(k), b), add(b, succ(k)))`：展开 `add` 得到 `succ(add(k, b))`；用 `addSucc` 把 `add(b, succ(k))` 改写成 `succ(add(b, k))`；再用归纳假设 `hypothesis` 把 `add(k, b)` 换成 `add(b, k)`。

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

zero 分支的 `calc` 从左边出发：链的第一步用 `zeroAdd(b)` 得到 `add(zero, b) = b`；第二步用 `reverse addZero(b)` 得到 `b = add(b, zero)`。链的两端正好是目标两端，`calc` 按实际证据构造传递项，端点与方向都逐项检查。succ 分支仍用 `simp`，因为主要动作是展开定义和重写归纳假设，写成 `calc` 反而更长。

!!! success "检查点"
    - [ ] `addComm` 与 `addCommByCalc` 都通过，且 `calc` 两步方向都对
    - [ ] 把 `calc` 第一步换成 `reverse zeroAdd(b)`，端点方向对不上，构建失败
    - [ ] `case` 里省掉 `, b`（不写被泛化的变量）后，归纳假设变弱

## 第五步：定向改写用 `rewrite`，直接给项用 `exact`

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

`exact` 直接给出证明项，不做证明搜索：`reverse addOne(n)` 把 `addOne(n)` 的等式反向，端点正好是当前目标。类型或端点对不上时 `exact` 失败，不会退化成“先猜一个”。

`calc` 和 `rewrite` 的分工也在这里显出来：`calc` 适合把一串等式按读者顺序写出来，每步用 `by` 给证据；`rewrite` 适合在当前目标里做定向替换。两者都只是构造候选证明项的命令，最终仍要过内核。

!!! success "检查点"
    - [ ] `addOne` 的两步改写顺序反过来也能过，但 `refl` 之前必须只剩同一项
    - [ ] `exact addOne(n)`（不反转）因端点方向不符而失败

## 第六步：洞与承认都不是证明

```el
fn addCommSketch(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	exact ?commutativity
}
```

`?name` 是具名洞，`?_` 是匿名洞：洞保存位置、目标类型与局部上下文，是待填目标，不构造核心项，也不把目标标为已证明。具名洞在同一 prove 请求内不能重复，匿名洞每次独立；洞不是类型、运行值、逻辑变量或公理，普通表达式里的 `?`、`?.`、`??` 与规则变量各有含义。

含洞声明不进已检查环境、不导出接口，也不能用于转换、优化、代码生成或证明别的定理；编译含未完成声明的模块必须失败。可以存编辑器草稿，但没有让洞通过的构建开关，草稿不是定理。

```el
fn addCommAdmitted(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	admit "先承认，后面再补"
}
```

`admit` 在合法上下文 Γ 中为目标 P 生成带源码身份的显式假设 `ΠΓ.P`，再用它取得条件证据。内核通过只说明“在这些假设下合类型”，不是无缺口证明；每个承认位置及其使用都记成 admission 依赖，普通构建必须报告，完整验收要求依赖为空。

`admit` 不能填运行数据、伪造实现或优化资格、隐藏残余目标，`sorry` 也不是它的别名；洞让证明无法发布，`admit` 让证明带假设发布并留下痕迹。

“未决”另算：搜索预算耗尽、取消或数据库失败保留未决／失败状态，既不推出无解，也不推出否定或已检查证明。只有候选完整、过内核重检、依赖报告如实列出的结果才算已检查证明；内核通过本身也不排除显式公理依赖。

!!! success "检查点"
    - [ ] 含 `?commutativity` 的模块构建失败，且没有任何开关能让它通过
    - [ ] `addCommAdmitted` 的依赖报告里出现这次承认的位置
    - [ ] 预算耗尽的搜索既不算“无解”，也不算“已证明”

洞、`admit` 与预算都不会替你产生已检查证明。下面换一个角度：同一份证明骨架，在另一种语言里长什么样。

??? quote "彩蛋：和 Lean 并排看，差别在定义方向"
    ```text
    -- Lean 写法（仅对照，不是 EL 代码）
    theorem addZero (n : Nat) : n + 0 = n := rfl
    ```
    Lean 的 `Nat.add` 递归第二个参数，所以 `n + 0` 在定义上就归约为 `n`，`rfl` 足够；EL 的 `add` 递归第一个参数，`add(n, zero)` 只随 `n` 的构造子逐步展开，所以要归纳。同名、同记号不等于同一组定义方程；跨两种定义方向时，`addZero` 与 `addSucc` 这类桥接引理是必要的。

    ```text
    -- Lean 写法（仅对照，不是 EL 代码）
    theorem addComm (a b : Nat) : a + b = b + a := by
    	induction a generalizing b with
    	| zero => simp
    	| succ k ih => simp [Nat.succ_add, ih]
    ```

    Lean 的交换律版本对 `a` 归纳并泛化 `b`，zero 分支收尾、succ 分支用归纳假设重写，结构与 EL 同构。差别在命令集合、定义方向和 `Eq` 的声明身份：一条 `simp` 可能关掉 EL 需要几步才能关掉的分支，EL 的 `refl`／`rewrite`／`calc` 目前是工程默认的一小套，别把它外推成完整的 Lean 体验。

## 完整源码

```text
proofs/
├── package.eol
└── src/
    └── main.el
```

`src/main.el` 是把上面的块按顺序拼起来的单文件：

```el
import { Prop, Eq } from "el:language/proofs.el"

data Nat { zero; succ(pred: Nat) }

fn add(n: Nat, m: Nat): Nat {
	match n {
		zero => m
		succ k => succ(add(k, m))
	}
}

fn zeroAdd(n: Nat): Eq(Nat, add(zero, n), n) => prove { refl }

fn addZero(n: Nat): Eq(Nat, add(n, zero), n) => prove {
	induction n
	all { simp [add] }
}

fn addSucc(a: Nat, b: Nat): Eq(Nat, add(a, succ(b)), succ(add(a, b))) => prove {
	induction a
	all { simp [add] }
}

fn addComm(a: Nat, b: Nat): Eq(Nat, add(a, b), add(b, a)) => prove {
	induction a generalizing b
	case Nat.zero b { simp [add, addZero] }
	case Nat.succ k, hypothesis, b { simp [add, addSucc, hypothesis] }
}

fn addOne(n: Nat): Eq(Nat, add(n, succ(zero)), succ(n)) => prove {
	rewrite [addSucc(n, zero), addZero(n)]
	refl
}
```

`addCommByCalc` 与两个洞、`admit` 的例子是同一文件的变体，按需追加；`addCommAdmitted` 会让依赖报告非空，交付前应当删掉或补完。

## 改成你自己的

1. **先证一条不需要归纳的引理。** `add(succ(a), b)` 与 `succ(add(a, b))` 按定义相等，用 `refl` 关掉 `Eq(Nat, add(succ(a), b), succ(add(a, b)))`。验收：`prove { refl }` 通过，并能解释为什么这条不像 `addZero` 那样需要 `induction`。
2. **证 `add` 的结合律。** `Eq(Nat, add(add(a, b), c), add(a, add(b, c)))`，对 `a` 归纳、泛化 `b` 与 `c`。验收：三个变量都出现在 `case` 的泛化列表里，证明通过。
3. **把洞换成真证明。** 删掉 `addCommSketch`，让 `addComm` 独立完成；再把 `admit` 版本移除，确认依赖报告为空。验收：`prove` 块里没有任何 `?` 与 `admit`，构建与依赖检查都干净。

## 卡住了？

- **现象：`refl` 关不掉 `add(n, zero) = n`。** `add` 递归第一个参数，`n` 是变量时归约不动。检查：先 `induction n`，再看每个分支两侧。
- **现象：`case` 分支选错或报“找不到构造子”。** `case` 按真实构造子身份匹配，不认标签文本。检查：写全 `Nat.zero`／`Nat.succ`，并核对字段、归纳假设、泛化变量的顺序。
- **现象：`simp` 只用上了定义，没用归纳假设。** 归纳假设不在重写集合里，或分支没展开。检查：把 `hypothesis` 补进 `simp [...]`。
- **现象：模块因为一个洞就整个构建失败。** 设计如此：含洞声明不进已检查环境。检查：补完洞，或临时移到草稿。

## 带走这三样

- 归纳类型加递归定义决定证明能展开什么；定义方向不同，桥接引理就不同。
- `all` 管分支、`case` 管控制、`calc`／`rewrite` 管等式推理；它们都只产生候选，内核重检才算数。
- 洞让证明无法发布，`admit` 让证明带着假设发布并留下依赖；两者都不等于证明。

## 下一站：[矩阵与数值脚本](numerics.md)

> 证明关心“对所有输入都成立”，而数值脚本关心“这一组输入算出的结果够不够准”。同一门语言怎么处理这两种完全不同的确定性？

- 主推进：[矩阵与数值脚本](numerics.md)：从 `solve` 到矩阵字面量、逐元素运算与精确／浮点两条路径。
- 想补普通控制流：[控制流](../language/control-flow.md)：分支、模式匹配与块体返回值。
