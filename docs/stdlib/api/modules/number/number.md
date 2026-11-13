# number/number.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

<span id="api-c6e654c3ea9412c954c8"></span>

## Number~type {#api-3cc24d3ef702e8652fb4}

源码：`src/stdlib/number/number.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L39)

```el
@optimize(using: optimize_number, data: @{ model: "rational", domain: "tracked", zero: Number(Integer(0)) }, proof: @{
	relation: NumberPolicy, rules: NumberPolicy,
	trusted: "registered exact numerical evaluation policy; native types, effects and resources remain checked",
	reify: @{
		zero: PolicyIndex.zero, succ: PolicyIndex.succ, atom: PolicyExpression.atom,
		textEmpty: PolicyText.empty, textCons: PolicyText.cons, number: PolicyExpression.number, string: PolicyExpression.string,
		add: PolicyExpression.add, sub: PolicyExpression.sub, mul: PolicyExpression.mul, div: PolicyExpression.div, mod: PolicyExpression.mod, neg: PolicyExpression.neg,
		compareEqual: PolicyExpression.compareEqual, ifexpression: PolicyExpression.condition,
		calls: @[
			@{ target: Number, arity: 1, model: PolicyExpression.convert },
			@{ target: Number, arity: 0, model: PolicyExpression.zero },
			@{ target: Integer, arity: 1, model: PolicyExpression.convert },
			@{ target: Integer, arity: 0, model: PolicyExpression.zero },
			@{ target: NumericRatio, arity: 1, model: PolicyExpression.convert },
			@{ target: NumericRatio, arity: 0, model: PolicyExpression.zero },
			@{ target: NumericRatio, arity: 2, model: PolicyExpression.ratio }
		]
	}
})
@assign(mode: "copy")
export class Number
```

表示精确有理数的数值类型，普通算术在约分后的整数分子和分母上进行。
它也可表示 unordered 状态；该状态不是 IEEE 浮点近似值。

### 示例：精确计算三分之一

```el
let third = Number(1) / Number(3)
console.stdout.writeLine(third * 3 == 1)
```
预期标准输出：
```text
t
```

## Number~constraints {#api-ad6f905ba12a9a7c223e}

源码：`src/stdlib/number/number.el:173` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L173)

```el
export fn Number(min = void, max = void, epsilon = void, integer = nil, overflow = "ub"): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

创建带数值域约束的 Number 类型。min/max 可用 unbounded 表示无下界或无上界；epsilon 必须是有限非负值。
integer 为真时结果必须为整数。overflow 支持 ub、error、nan、wrap；wrap 仅允许有界整数域。
epsilon 用于算术结果在约束域内的紧凑表示，不把 Number 改成二进制浮点类型。

**参数**：min 下界，或 unbounded；必须提供。

**参数**：max 上界，或 unbounded；必须提供且不小于 min。

**参数**：epsilon 有限非负精确数值；必须提供。

**参数**：integer 是否要求整数值。

**参数**：overflow 越界策略：ub、error、nan 或 wrap；wrap 要求整数且上下界有界。

**返回值**：具有所给数值域合同的 Number 类型。

**注意**：min、max 或 epsilon 缺失，以及 epsilon 为 unbounded 时，当前入口使用 die_with 报告并终止程序，不是可捕获异常。其余参数校验在生成类型的实例构造时进行。

**失败与异常**：NumberParameterError 实例构造时发现边界倒置、epsilon 不是有限非负值、整数标志无效或策略不支持时。

**失败与异常**：RangeError 初始构造值不符合约束，或 error 策略下的算术结果越界时；nan 策略可将越界算术结果变为 unordered。

### 示例：创建有界整数类型

```el
let Small = Number<min: 0, max: 10, epsilon: 0, integer: t, overflow: "error">
let value = Small(7)
console.stdout.writeLine(value + 1)
```
预期标准输出：
```text
8
```
