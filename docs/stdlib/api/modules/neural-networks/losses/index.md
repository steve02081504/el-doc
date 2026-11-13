# neural-networks/losses/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 神经网络损失 {#api-f24d9a048a3539d38467}

源码：`src/stdlib/neural-networks/losses/index.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/losses/index.el#L4)

提供逐元素回归损失、概率损失及分类损失入口，默认归约为均值。

## reduceLoss {#api-a63260eef4f189bf2f49}

源码：`src/stdlib/neural-networks/losses/index.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/losses/index.el#L20)

按 none、sum 或 mean 规则归约损失张量。

```el
export fn reduceLoss(loss, reduction: Text = "mean")
```

**参数**：loss 待归约的损失张量。

**参数**：reduction 归约方式，默认 mean。

**返回值**：none 时返回原形状张量，sum 或 mean 时返回 rank-zero 张量。

**失败与异常**：ShapeError 当 reduction 不是 none、sum 或 mean 时抛出。

### 示例：对逐元素损失求和

```el
let total = reduceLoss(loss, "sum")
```

## maeLoss {#api-cc55a668339edc941395}

源码：`src/stdlib/neural-networks/losses/index.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/losses/index.el#L37)

计算输入与目标的逐元素绝对误差，并按 reduction 归约。

```el
export fn maeLoss(input, target, reduction: Text = "mean")
```

**参数**：input 预测张量。

**参数**：target 与 input 同形状的目标张量。

**参数**：reduction none、sum 或 mean，默认 mean。

**返回值**：按所选方式归约的绝对误差损失。

**失败与异常**：ShapeError 当输入与目标形状不一致时抛出。

### 示例：计算平均绝对误差

```el
let loss = maeLoss(prediction, target)
```

## huberLoss {#api-86753a5a07c600430493}

源码：`src/stdlib/neural-networks/losses/index.el:54` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/losses/index.el#L54)

计算阈值 delta 内为二次、超出部分为线性的 Huber 损失。

```el
export fn huberLoss(input, target, delta: Number = 1, reduction: Text = "mean")
```

**参数**：input 预测张量。

**参数**：target 与 input 同形状的目标张量。

**参数**：delta 正的有限转折阈值，默认 1。

**参数**：reduction none、sum 或 mean，默认 mean。

**返回值**：按所选方式归约的损失。

**失败与异常**：ShapeError 当形状不匹配或 delta 非正、非有限时抛出。

### 示例：计算 Huber 损失

```el
let loss = huberLoss(prediction, target, delta: 1.5)
```
