# functions/composition.el

本页由源码注释生成；示例未运行验证。

## 函数组合 {#api-27a2936715ebc2d02e14}

源码：`src/stdlib/functions/composition.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/composition.el#L1)

将共同的输入变换与最终合并操作分开表达。`over` 由默认前导模块重导出。

## over {#api-e0ba7eca2990075a35ab}

源码：`src/stdlib/functions/composition.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/functions/composition.el#L23)

```el
export fn over(merge, transform)
```

创建一个二元函数：先分别变换两个输入，再合并变换结果。

调用顺序是 `transform(left)`、`transform(right)`、`merge`；每个输入只变换一次。创建组合函数时不调用这两个函数。

**参数**：merge 接收两个变换结果的二元可调用值。

**参数**：transform 接收单个输入的可调用值；左右输入必须都能被它接受。

**返回值**：捕获 merge 和 transform 的二元函数，返回 merge 的结果。

**失败与异常**：变换或合并抛出的异常向调用者传播；前一步失败时不执行后续调用。

**复杂度**：每次调用包含两次变换和一次合并；具体开销取决于传入函数。

**注意**：捕获值的复制或共享服从其类型的普通赋值合同；此函数不额外提供并行执行或遍历融合。

### 示例：比较两个数的平方

```el
let largerSquare = over(max, value => value * value)
console.stdout.writeLine(largerSquare(-3, 2))
```
预期标准输出：
```text
9
```
