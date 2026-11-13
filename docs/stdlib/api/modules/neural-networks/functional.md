# neural-networks/functional.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/neural-networks.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 神经网络张量函数 {#api-9812025086fc89027ab6}

源码：`src/stdlib/neural-networks/functional.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/functional.el#L7)

提供 softmax、分类损失、归一化与注意力等张量层常用运算。

## softmax {#api-b4b475e208e3fc45c7a0}

源码：`src/stdlib/neural-networks/functional.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/functional.el#L21)

```el
export fn softmax(value, axis: Number = 1, policy: TensorMathPolicy = TensorMathPolicy())
```

沿指定轴将输入转换为和为 1 的指数归一化值。

**参数**：value 输入张量。

**参数**：axis 归一化轴，默认是 1。

**参数**：policy 控制数值计算的策略。

**返回值**：与输入形状相同的概率张量。

### 示例：沿类别轴计算概率

```el
let probabilities = softmax(logits, axis: 1)
```
示例展示接口用法；未运行验证。

## logSoftmax {#api-1764884006cd0be44f7e}

源码：`src/stdlib/neural-networks/functional.el:32` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/functional.el#L32)

```el
export fn logSoftmax(value, axis: Number = 1, policy: TensorMathPolicy = TensorMathPolicy())
```

沿指定轴计算数值稳定的对数 softmax。

**参数**：value 输入张量。

**参数**：axis 归一化轴，默认是 1。

**参数**：policy 控制数值计算的策略。

**返回值**：与输入形状相同的对数概率张量。

### 示例：计算对数概率

```el
let logProbabilities = logSoftmax(logits, axis: 1)
```

## crossEntropy {#api-6cc740068d672b42626f}

源码：`src/stdlib/neural-networks/functional.el:48` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/functional.el#L48)

```el
export fn crossEntropy(logits, targets, axis: Number = 1, policy: TensorMathPolicy = TensorMathPolicy())
```

计算稠密目标权重与 logits 对应的交叉熵，并对非类别轴样本取均值。

**参数**：logits 未归一化类别分数。

**参数**：targets 与 logits 同形状的稠密类别权重。

**参数**：axis 类别轴，默认是 1。

**参数**：policy 控制 log-softmax 数值计算的策略。

**返回值**：rank-zero 平均损失张量。

**失败与异常**：ShapeError 当 logits 与 targets 形状不一致时抛出。

### 示例：从 logits 与稠密目标计算损失

```el
let loss = crossEntropy(logits, targets)
```
示例展示接口用法；未运行验证。

## oneHot {#api-956d05922bbc9c543e7d}

源码：`src/stdlib/neural-networks/functional.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/functional.el#L64)

```el
export fn oneHot(element: type, labels: Number[], classes: Number)
```

将类别编号数组转换为每行一个类别权重为 1 的稠密二维张量。

**参数**：element 输出张量的元素类型。

**参数**：labels 每个样本的类别编号，编号必须小于 classes。

**参数**：classes 类别总数，必须为正数。

**返回值**：形状为 [样本数, 类别数] 的 one-hot 张量。

**失败与异常**：ShapeError 当类别数为零或标签越界时抛出。

### 示例：将两个标签编码为三类目标

```el
let targets = oneHot<element: Number>(@[0, 2], 3)
```
