# neural-networks/autograd.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/neural-networks.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Autograd.square](#api-c7cdb29630ea7e9ca4c3)
- [Autograd.sum](#api-4c5a860a89bb4e088fe1)
- [Autograd.mean](#api-31175d2b66a5ce9e4d5f)
- [Autograd.variable](#api-ab3276f9117e60133442)
- [Autograd.valueAndGrad](#api-2c37c8b473d37f9243b7)

## 自动微分 {#api-4a1ebdbc6830dc672faf}

源码：`src/stdlib/neural-networks/autograd.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L20)

提供记录张量运算并通过反向传播计算梯度的 tape 类型。

## Autograd {#api-fe9b9dee2c2f03ef38d0}

源码：`src/stdlib/neural-networks/autograd.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L37)

```el
export fn Autograd(element: type, storage: type = Tensor<element: element>): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

创建指定元素和存储类型的自动微分 tape 类型。

**参数**：element 被跟踪张量的元素类型。

**参数**：storage 张量存储类型，默认主机 Tensor。

**返回值**：含 variable、constant 与 valueAndGrad 操作的 tape 类型。

### 示例：创建 Number 自动微分 tape

```el
let Tape = Autograd<element: Number>
let tape = Tape()
```
示例展示接口用法；未运行验证。

## Autograd.square {#api-c7cdb29630ea7e9ca4c3}

源码：`src/stdlib/neural-networks/autograd.el:333` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L333)

```el
fn square()
```

对跟踪张量逐元素平方，并在 tape 上记录乘法节点。

**返回值**：与输入形状相同的跟踪张量。

### 示例：对跟踪值逐元素平方

```el
let squared = x.square()
```

## Autograd.sum {#api-4c5a860a89bb4e088fe1}

源码：`src/stdlib/neural-networks/autograd.el:342` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L342)

```el
fn sum()
```

将跟踪张量所有元素相加，返回可继续参与求导的 rank-zero 值。

**返回值**：记录归约操作的标量跟踪值。

### 示例：对平方值求和形成损失

```el
let loss = x.square().sum()
```

## Autograd.mean {#api-31175d2b66a5ce9e4d5f}

源码：`src/stdlib/neural-networks/autograd.el:350` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L350)

```el
fn mean()
```

对跟踪张量所有元素求平均并在 tape 上记录归约。

**返回值**：记录均值运算的标量跟踪值。

### 示例：对误差张量取平均

```el
let loss = (prediction - target).square().mean()
```

## Autograd.variable {#api-ab3276f9117e60133442}

源码：`src/stdlib/neural-networks/autograd.el:523` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L523)

```el
fn variable(value: Dense): Tracked
```

**返回类型**：[`Tracked`](../../types.md#api-90e17b44158251ad4d5b)

将输入张量注册为需要对其求导的叶变量。

**参数**：value 作为叶节点的张量值。

**返回值**：可参加 tape 运算的跟踪张量。

### 示例：将输入注册为变量

```el
let x = tape.variable(input)
```

## Autograd.valueAndGrad {#api-2c37c8b473d37f9243b7}

源码：`src/stdlib/neural-networks/autograd.el:811` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/autograd.el#L811)

```el
fn valueAndGrad(loss: Tracked, variables: Tracked[]): Result
```

**返回类型**：[`Result`](../../types.md#api-666c52dd6d3d5f3f1651)

对 rank-zero 跟踪损失反向传播，返回损失值及各变量梯度。

**参数**：loss tape 上的 rank-zero 损失。

**参数**：variables 需要返回梯度的变量，返回顺序与此数组一致。

**返回值**：含 value 与 grad 数组的结果。

**失败与异常**：DifferentiationError 当损失形状或记录的运算不支持求导时抛出。

### 示例：计算输入平方和的梯度

```el
let step = tape.valueAndGrad(x.square().sum(), @[x])
```
