# functions/composition.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/functions.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 函数组合 {#api-27a2936715ebc2d02e14}

源码：`src/stdlib/functions/composition.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/composition.el#L1)

将共同的输入变换与最终合并操作分开表达。`over` 由默认前导模块重导出。

## over {#api-e0ba7eca2990075a35ab}

源码：`src/stdlib/functions/composition.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/composition.el#L23)

创建函数：先逐项变换输入，再以相同数量、相同顺序的结果调用 merge。

transform 按输入顺序执行，每个输入只变换一次，全部成功后才调用 merge。创建组合函数时不调用这两个函数。

```el
export fn over(merge, transform)
```

**参数**：merge 接收变换结果的可调用值；其普通元数、默认参数与位置类型合同继续适用。

**参数**：transform 接收单个输入的可调用值；每个输入都必须能被它接受。

**返回值**：捕获 merge 和 transform 的函数，返回 merge 的结果；merge 允许零实参时也允许零输入。

**失败与异常**：变换或合并抛出的异常向调用者传播；前一步失败时不执行后续调用。

**复杂度**：n 个输入调用 n 次变换和一次合并；参数序列的物化与转发开销取决于输入形状和优化。

**注意**：捕获值的复制或共享服从其类型的普通赋值合同；此函数不额外提供并行执行或遍历融合。

### 示例：比较多个数的平方

```el
let largerSquare = over(max, value => value * value)
console.stdout.writeLine(largerSquare(-3, 2, -4))
```
预期标准输出：
```text
16
```
