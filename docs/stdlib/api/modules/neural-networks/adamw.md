# neural-networks/adamw.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/neural-networks.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## AdamW 优化器 {#api-053d670ea1c2ecfb78a1}

源码：`src/stdlib/neural-networks/adamw.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/adamw.el#L10)

提供按模型参数状态保存一阶、二阶矩并应用权重衰减的 AdamW 优化器。

## AdamW {#api-72ebca138f336dfe1a20}

源码：`src/stdlib/neural-networks/adamw.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/adamw.el#L25)

```el
export fn AdamW(element: type, storage: type = Tensor<element: element>): type
```

创建指定元素与存储类型的 AdamW 优化器类型。

**参数**：element 参数及优化状态使用的数值元素类型。

**参数**：storage 参数张量存储类型，默认是主机 Tensor。

**返回值**：可构造 AdamW 实例的类型。

### 示例：创建 Number 参数的 AdamW

```el
let Optimizer = AdamW<element: Number>
let optimizer = Optimizer(rate: .001, weightDecay: .01)
```
示例展示接口用法；未运行验证。

## AdamW.update {#api-221135265f4603f4a498}

源码：`src/stdlib/neural-networks/adamw.el:105` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/adamw.el#L105)

```el
fn update(model, gradient)
```

按 AdamW 更新规则应用梯度，并维护此优化器身份对应的参数矩状态。

**参数**：model 产生该梯度的模型。

**参数**：gradient 模型级 valueAndGrad 返回的梯度。

**失败与异常**：StaleGradient 当梯度不属于模型当前参数修订时由模型抛出。

### 示例：应用一次 AdamW 更新

```el
optimizer.update(model, step.grad)
```
