# platform/machine/integer.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/platform.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 目标机器整数 {#api-dc56584fb34c28e4b2b7}

源码：`src/stdlib/platform/machine/integer.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/machine/integer.el#L1)

目标机器整数相关接口。

## NativeSignedInteger {#api-45690472287900730a5f}

源码：`src/stdlib/platform/machine/integer.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/machine/integer.el#L21)

目标机器选定宽度的有符号整数；宽度不保证为 64 位或指针宽度。

```el-signature
export @builtin:vome:signed:integer class NativeSignedInteger
```

??? note "完整声明与属性"

	```el-signature
	@optimize(using: optimize_number, data: @{ model: "integer", zero: NativeSignedInteger(0) }, proof: @{
		relation: NumberPolicy, rules: NumberPolicy,
		trusted: "registered exact numerical evaluation policy; native types, effects and resources remain checked",
		reify: @{
			zero: PolicyIndex.zero, succ: PolicyIndex.succ, atom: PolicyExpression.atom,
			textEmpty: PolicyText.empty, textCons: PolicyText.cons, number: PolicyExpression.number, string: PolicyExpression.string,
			add: PolicyExpression.add, sub: PolicyExpression.sub, mul: PolicyExpression.mul, div: PolicyExpression.div, mod: PolicyExpression.mod, neg: PolicyExpression.neg,
			compareEqual: PolicyExpression.compareEqual, ifexpression: PolicyExpression.condition,
			calls: @[
				@{ target: NativeSignedInteger, arity: 1, model: PolicyExpression.convert },
				@{ target: NativeSignedInteger, arity: 0, model: PolicyExpression.zero },
				@{ target: NativeUnsignedInteger, arity: 1, model: PolicyExpression.convert },
				@{ target: NativeUnsignedInteger, arity: 0, model: PolicyExpression.zero }
			]
		}
	})
	export @builtin:vome:signed:integer class NativeSignedInteger
	```

### 示例：用法

```el
import { NativeSignedInteger } from "el:platform/machine/integer.el"
let value = NativeSignedInteger(42)
```
