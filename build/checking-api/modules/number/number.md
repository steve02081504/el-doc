# number/number.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/number.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 精确数值 {#api-d1da3697db06619147d9}

源码：`src/stdlib/number/number.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L1)

定义标准数值基类与 Number 精确有理数表示，提供算术、比较、转换、数值域传播及受约束数值类型构造。

## unbounded {#api-db75efcb59f6dbd40ec8}

源码：`src/stdlib/number/number.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L35)

指定 Number 类型工厂的无界端点。

```el-signature
export const unbounded = UnboundedNumberLimit()
```

**类型**：[`UnboundedNumberLimit`](../../types.md#api-c6880ef3c466bd9621c5)

### 示例：用法

```el
let Whole = Number<min: 0, max: unbounded, epsilon: 0, integer: t, overflow: "error">
let value = Whole(3)
```

<span id="api-c6e654c3ea9412c954c8"></span>

## Number~type {#api-3cc24d3ef702e8652fb4}

源码：`src/stdlib/number/number.el:55` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L55)

表示精确有理数的数值类型，普通算术在约分后的整数分子和分母上进行。
它也可表示 unordered 状态；该状态不是 浮点 浮点近似值。

```el-signature
@numericRepresentation(format: @{ kind: "rational", domain: "tracked" })

@assign(mode: "copy")
export class Number
```

??? note "完整声明与属性"

	```el-signature
	@numericRepresentation(format: @{ kind: "rational", domain: "tracked" })
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

源码：`src/stdlib/number/number.el:397` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/number/number.el#L397)

创建带数值域约束的 Number 类型。min/max 可用 unbounded 表示无下界或无上界；epsilon 必须是有限非负值。
integer 为真时结果必须为整数。overflow 支持 ub、error、nan、wrap；wrap 仅允许有界整数域。
epsilon 表示允许的最大绝对误差。普通算术从操作数建立新结果域。

```el-signature
@typeFlags(parameters: @["integer"])
export fn Number(min = nil, max = nil, epsilon = nil, integer = f, overflow = "ub"): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：min 下界，或 unbounded。

**参数**：max 上界，或 unbounded；提供时不得小于 min。

**参数**：epsilon 有限非负精确数值。

**参数**：integer 是否要求整数值。

**参数**：overflow 越界策略：ub、error、nan 或 wrap；wrap 要求整数且上下界有界。

**返回值**：具有所给数值域合同的 Number 类型。

**注意**：文本输入须提供完整的 min、max、epsilon。值域判定只检查已提供的约束。

**失败与异常**：NumberParameterError 实例构造时发现边界倒置、epsilon 不是有限非负值、整数标志无效或策略不支持时。

**失败与异常**：RangeError 初始构造值不符合约束。

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
