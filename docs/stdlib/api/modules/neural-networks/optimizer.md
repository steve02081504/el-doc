# neural-networks/optimizer.el

本页由源码注释生成；示例未运行验证。

## 随机梯度下降 {#api-2f34095d6329c5f02f1c}

源码：`src/stdlib/neural-networks/optimizer.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/optimizer.el#L4)

提供以固定学习率将模型梯度写回参数的 SGD 优化器。

## SGD {#api-6d3c31621381d78a2d47}

源码：`src/stdlib/neural-networks/optimizer.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/optimizer.el#L17)

```el
export @assign(mode: "copy") class SGD
```

创建随机梯度下降优化器；更新时按学习率应用模型梯度。

**参数**：rate 有限且非负的学习率。

**失败与异常**：InvalidLearningRate 当学习率非有限或为负时抛出。

### 示例：创建 SGD 优化器

```el
let optimizer = SGD(rate: .01)
optimizer.update(model, step.grad)
```
示例展示接口用法；未运行验证。

## SGD.update {#api-fda9885666e0c1fb1e9b}

源码：`src/stdlib/neural-networks/optimizer.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/optimizer.el#L39)

```el
fn update(model, gradient)
```

按已配置学习率把梯度应用到模型参数。

**参数**：model 产生该梯度的模型。

**参数**：gradient 模型级 valueAndGrad 返回的梯度。

**失败与异常**：StaleGradient 当梯度不属于模型当前参数修订时由模型抛出。

### 示例：应用一次模型梯度

```el
optimizer.update(model, step.grad)
```
