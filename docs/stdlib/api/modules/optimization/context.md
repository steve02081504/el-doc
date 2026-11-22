# optimization/context.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/optimization.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 优化器上下文 {#api-8fffb86f2be61483637a}

源码：`src/stdlib/optimization/context.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/optimization/context.el#L11)

为源码优化器提供受约束的输入、上下文与语法构造辅助函数。

## OptimizationInput {#api-1e9a091adfd266480b0b}

源码：`src/stdlib/optimization/context.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/optimization/context.el#L24)

表示交给优化器的表达式，并提供识别优化区域的查询。

```el-signature
export class OptimizationInput
```

### 示例：读取待优化表达式

```el
let input = OptimizationInput()
let expression = input.expression()
```

## OptimizationContext {#api-9f36e53c073598aafc53}

源码：`src/stdlib/optimization/context.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/optimization/context.el#L36)

在优化区域内构造替换、调用、成员访问、绑定和控制流语法。

```el-signature
export class OptimizationContext extends SyntaxContext
```

### 示例：创建优化上下文

```el
let context = OptimizationContext()
```

## unchanged {#api-ca19d040014517ecd1ed}

源码：`src/stdlib/optimization/context.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/optimization/context.el#L78)

返回优化输入中的原表达式，作为不改写输入的优化器实现。

```el-signature
export fn unchanged(input: OptimizationInput, context: OptimizationContext): UncheckedSyntax
```

**返回类型**：[`UncheckedSyntax`](../language/syntax/index.md#api-3628c09626a9be6ba1ba)

**参数**：input 待优化的输入。

**参数**：context 优化上下文；此实现不需要构造新语法。

**返回值**：输入表达式本身。

### 示例：保留输入表达式（需调用方提供对象或绑定）

```el
// @external input: OptimizationInput, context: OptimizationContext
let result = unchanged(input, context)
```
