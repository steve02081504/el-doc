# neural-networks/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/neural-networks.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Sequential.forward](#api-daa36f8828e242c94dc1)

## 神经网络模型 {#api-36f84d954a69a30a4783}

源码：`src/stdlib/neural-networks/model.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L10)

定义可组合的网络层、顺序模型、参数梯度计算与基础优化器接口。

## Linear {#api-f9616a28e08030b55cfb}

源码：`src/stdlib/neural-networks/model.el:76` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L76)

```el
export fn Linear(input: Number, output: Number): Layer
```

**返回类型**：`Layer`

创建全连接层，前向计算输入与转置权重的矩阵积并加上偏置。

**参数**：input 输入特征数，必须为正数。

**参数**：output 输出特征数，必须为正数。

**返回值**：用于 Sequential 层列表的线性层描述。

**失败与异常**：InvalidModel 当任一维度非正时抛出。

### 示例：创建一个 2 到 4 维的全连接层

```el
let layer = Linear(2, 4)
console.stdout.writeLine(layer.input, " -> ", layer.output)
```
示例展示接口用法；未运行验证。

## ReLU {#api-f46f2b7a970cd6420534}

源码：`src/stdlib/neural-networks/model.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L87)

```el
export fn ReLU(): Layer
```

**返回类型**：`Layer`

创建逐元素整流线性单元层，将负值变为零。

**返回值**：用于 Sequential 层列表的 ReLU 层描述。

### 示例：将 ReLU 放入网络层列表

```el
let layer = ReLU()
```

## Sequential {#api-3de3a8b723127e06dd74}

源码：`src/stdlib/neural-networks/model.el:147` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L147)

```el
export fn Sequential(element: type, storage: type = Tensor<element: element>): type
```

**返回类型**：`type`

创建按顺序应用层列表的模型类型，可选择元素类型和参数存储类型。

**参数**：element 模型张量的元素类型。

**参数**：storage 参数张量的存储类型；默认使用主机 Tensor。

**返回值**：可构造模型实例的类型。

### 示例：构造一个两层主机模型

```el
let Network = Sequential<element: Number>
let model = Network(@[Linear(2, 4), ReLU(), Linear(4, 1)], seed: 1)
```
示例展示接口用法；未运行验证。

## Sequential.forward {#api-daa36f8828e242c94dc1}

源码：`src/stdlib/neural-networks/model.el:418` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L418)

```el
fn forward(input: Values): Values
```

**返回类型**：`Values`

依次执行模型中的各层并返回前向结果；Linear 使用权重转置与偏置，ReLU 对负值置零。

**参数**：input 形状符合首层输入特征数的张量。

**返回值**：按层列表变换后的张量。

**失败与异常**：ShapeError 当输入形状与层参数不兼容时抛出。

### 示例：对批次输入执行前向计算

```el
let prediction = model.forward(input)
```

## valueAndGrad {#api-74a208b8786c54fae08b}

源码：`src/stdlib/neural-networks/model.el:610` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/model.el#L610)

```el
export fn valueAndGrad(model, function)
```

对模型闭包返回的标量损失求值并计算模型参数梯度。

**参数**：model 要求导的模型实例。

**参数**：function 接收模型并返回 rank-zero 损失张量的闭包。

**返回值**：含损失 value 与参数梯度 grad 的结果。

**失败与异常**：DifferentiationError 当损失不可微或形状违反求导合同。

### 示例：对模型损失计算梯度

```el
let step = valueAndGrad(model, current => current(input).square().mean())
optimizer.update(model, step.grad)
```
示例展示接口用法；未运行验证。
