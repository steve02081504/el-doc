# 神经网络

这一页从张量布局讲到一次完整训练，读完你能用 EL 标准库搭出两层模型，跑通前向、损失、自动微分与参数更新，并知道换到设备存储时要改哪些类型参数。

## 张量：元素、存储与布局

`Tensor<element: T>` 是普通值类型，`element` 决定每个元素是什么数值。普通训练用 `Number`；需要固定 IEEE 格式时，把 `BitFloat` 派生出的类型作为元素类型，例如 `F32`。

```el
import { Tensor } from "el:numerical-computing/index.el"

let Dense = Tensor<element: Number>
let x = Dense(@[2, 3], @[1, 2, 3, 4, 5, 6])
let bias = Dense(@[1, 3], @[10, 20, 30])
let shifted = x + bias

console.stdout.writeLine(x.extent(0))    // 2
console.stdout.writeLine(x.extent(1))    // 3
console.stdout.writeLine(x[0, 0])        // 1
console.stdout.writeLine(x[1, 2])        // 6
console.stdout.writeLine(shifted[1, 2])  // 36
```

这一页的回归与全连接示例把输入组织成 `[batch, features]` 的二维张量：第 0 轴是样本，第 1 轴是特征。上面 `x` 的形状是 `@[2, 3]`，即两个样本、每个三个特征。

存储是列优先的：第 0 轴变化最快。`@[1, 2, 3, 4, 5, 6]` 按列摆放，先 `(0,0)`、`(1,0)`，再 `(0,1)`、`(1,1)`，最后 `(0,2)`、`(1,2)`，所以 `x[1, 2]` 是 6。

广播按轴 0 对齐，缺失的尾部轴长度按 1 处理；每一轴要么两侧相等，要么一侧为 1。`shifted = x + bias` 中 `bias` 的形状是 `@[1, 3]`，样本轴广播到 2，因此每个样本加上同一行偏置。

`Sequential<element: T, storage: S>` 同时接受元素类型与存储类型。默认存储是 `Tensor<element: T>`，即值放在主机内存；设备章节会把 `storage` 换成 `DeviceTensor<element: F32>`。

## 前向：Sequential、Linear 与 ReLU

`Linear(input, output)` 声明一个全连接层。权重形状是 `[output, input]`，偏置形状是 `[1, output]`，前向计算为 `input * weight.T + bias`；显式二维偏置让样本轴与特征轴的广播互不依赖尺寸。

`ReLU()` 是按元素作用的激活层。`Sequential` 依次执行层列表，模型本身可调用，调用一次就是一次前向。

```el
import { Tensor } from "el:numerical-computing/index.el"
import { Linear, ReLU, Sequential } from "el:neural-networks/index.el"

let Dense = Tensor<element: Number>
let Network = Sequential<element: Number>
let model = Network(@[Linear(2, 4), ReLU(), Linear(4, 1)], seed: 1)
let prediction = model(Dense(@[2, 2], @[1, 2, 3, 4]))

console.stdout.writeLine(prediction.extent(0))  // 2
console.stdout.writeLine(prediction.extent(1))  // 1
```

`seed` 控制参数初始化的随机数；同一个 seed 给同一组层列表，初始化结果相同。参数初始化的具体取值由模型维护，不需要在层的声明里手写。

`Sequential` 的层列表不只这两类：同一个公开入口还导出 `Conv2d`、`LayerNorm`、`Flatten` 与 `BatchNorm`。卷积使用 NHWC 输入，`Flatten` 保留 batch 轴，`LayerNorm` 沿显式 `axis` 统计。

## 自动微分：valueAndGrad 与 Autograd

自动微分有两层入口。模型级入口是 `valueAndGrad(model, loss)`：闭包接收模型、返回一个 rank-zero 的损失张量，结果对象有 `value` 和 `grad` 两个字段。`value` 是损失张量，`grad` 是模型参数梯度，可直接交给优化器。

底层入口是 `Autograd<element: Number>()`：把普通张量注册成 `variable`，用普通张量运算组合损失，再调用 `tape.valueAndGrad(loss, variables)`。返回对象同样是 `value` 与 `grad`，其中 `grad` 是按传入变量顺序排列的梯度数组。

```el
import { Tensor } from "el:numerical-computing/index.el"
import { Autograd } from "el:neural-networks/index.el"

let Dense = Tensor<element: Number>
let tape = Autograd<element: Number>()
let x = tape.variable(Dense(@[1, 1], @[3]))
let loss = x.square().sum()
let step = tape.valueAndGrad(loss, @[x])

console.stdout.writeLine(step.value.scalar())   // 9
console.stdout.writeLine(step.grad[0].flat(0))  // 6
```

`x.square().sum()` 先逐元素平方，再把全部元素归约成 rank-zero 标量；`valueAndGrad` 要求损失张量是 rank-zero。`step.grad[0]` 与输入同形状，`flat(0)` 取展平后的第 0 个元素；这里 `3² = 9` 的导数就是 `2 × 3 = 6`。

`Autograd` 的 `variable` 是参数叶，`constant` 是不求导的输入；普通运算会记录到同一条 tape 上。模型级 `valueAndGrad` 的 `grad` 还带模型身份与参数修订号，只有同一模型、同一修订的梯度才能用于更新。

## 损失

回归损失没有单独的 `mse` 导出；惯用写法是 `(prediction - target).square().mean()`，与回归训练的写法一致。

分类损失用 `crossEntropy(logits, targets, axis: 1, policy: ...)`。`targets` 必须与 `logits` 同形状，是稠密的类别权重；`oneHot<element: Number>(labels, classes)` 把类别编号转成这种目标。

```el
import { Tensor } from "el:numerical-computing/index.el"
import { crossEntropy, oneHot } from "el:neural-networks/index.el"

let Dense = Tensor<element: Number>
let logits = Dense(@[1, 3], @[2, 1, 0])
let targets = oneHot<element: Number>(@[0], 3)
let loss = crossEntropy(logits, targets)

console.stdout.writeLine(loss.scalar())
```

`crossEntropy` 内部对 logits 做 `logSoftmax`，乘稠密目标后沿类别归约再取均值，所以结果是 rank-zero 标量。源码导出的损失还包括 `maeLoss`、`huberLoss`、`binaryCrossEntropy`、`nllLoss`、`classIndexCrossEntropy` 等；这些名字都能在 `el:neural-networks/index.el` 的重导出里找到。

## 优化器与训练循环

`SGD(rate: .01)` 只保存学习率，调用 `optimizer.update(model, step.grad)` 时把梯度应用到模型参数。学习率必须是有限非负数。

`AdamW<element: Number>` 接受 `rate`、`beta1`、`beta2`、`epsilon`、`weightDecay` 五个参数，默认分别是 `.9`、`.999`、`1e-8` 与 `.01`；矩状态保存在模型的参数状态里，以优化器身份区分。

```el
import { AdamW } from "el:neural-networks/index.el"

let Optimizer = AdamW<element: Number>
let optimizer = Optimizer(rate: .001, weightDecay: .01)
```

下面是一次完整的回归训练：准备输入与目标，循环前向、损失、反向和参数更新，并打印每轮损失。

```el
import { Tensor } from "el:numerical-computing/index.el"
import { Linear, ReLU, Sequential, SGD, valueAndGrad } from "el:neural-networks/index.el"

let Dense = Tensor<element: Number>
let Network = Sequential<element: Number>
let model = Network(@[Linear(1, 2), ReLU(), Linear(2, 1)], seed: 1)
let optimizer = SGD(rate: .01)
let x = Dense(@[2, 1], @[1, 2])
let y = Dense(@[2, 1], @[0, 0])

for (let iteration = 0; iteration < 10; iteration++) {
	let step = valueAndGrad(model, m => (m(x) - y).square().mean())
	optimizer.update(model, step.grad)
	console.stdout.writeLine(step.value.scalar())
}
```

闭包里的 `m(x)` 是一次前向，`(m(x) - y).square().mean()` 是均方损失。`valueAndGrad` 返回的 `step.grad` 交给 `SGD.update`；更新会递增模型修订号，旧梯度再更新会抛 `StaleGradient`。循环只打印损失，输入与目标保持不变。

把 `SGD(rate: .01)` 换成 `AdamW<element: Number>(rate: .001, weightDecay: .01)` 就能使用 AdamW，其余循环结构不变。

## 设备与 GPU

`TensorDevice<element: F32>` 创建一个固定格式的设备会话，`fromHost` 显式把主机张量上传进去。`DeviceTensor<element: F32>` 是设备存储类型，复制通过设备存储复制完成；`toHost()` 与 `scalar()` 是显式的设备到主机读回边界。

模型的 `storage` 类型参数写 `DeviceTensor<element: F32>`，构造时第三个参数用一个转换回调把主机权重上传到会话。

```el
import { BitFloat } from "el:number/index.el"
import { Tensor, DeviceTensor, TensorDevice } from "el:numerical-computing/index.el"
import { Linear, ReLU, Sequential, SGD, valueAndGrad } from "el:neural-networks/index.el"

let F32 = BitFloat<sign_bits: 1, fraction_bits: 23, exponent_bits: 8, exponent_bias: 127>
let Host = Tensor<element: F32>
let Values = DeviceTensor<element: F32>
let Device = TensorDevice<element: F32>
let Network = Sequential<element: F32, storage: Values>
let device = Device()
let model = Network(@[Linear(1, 2), ReLU(), Linear(2, 1)], 1, host => device.fromHost(host))
let x = device.fromHost(Host(@[2, 1], @[F32(1), F32(2)]))
let y = device.fromHost(Host(@[2, 1], @[F32(0), F32(0)]))
let optimizer = SGD(rate: .01)

for (let iteration = 0; iteration < 10; iteration++) {
	let step = valueAndGrad(model, m => (m(x) - y).square().mean())
	optimizer.update(model, step.grad)
	console.stdout.writeLine(step.value.scalar())
}
```

设备张量的算术按元素格式的 IEEE 合同执行；`step.value.scalar()` 是每轮显式读回主机的一个标量，不是自动隐式同步。

设备后端按平台目标选择：Windows 默认 D3D11，macOS 使用 Metal，Linux／FreeBSD／Android 使用 Vulkan，Windows 也可以显式选择 Vulkan。后端按数值格式、布局和驱动能力检查实际资源；平台或设备不可用时抛 `ExecutionError` 并给出原因。需要主机数据时必须显式调用 `toHost()` 或 `scalar()`，不存在隐式的设备到主机转换。

!!! note "实现状态"
    本页的公开入口来自 `el:neural-networks/index.el` 及其重导出的模块：`Sequential`、`Linear`、`ReLU`、`SGD`、`AdamW`、`valueAndGrad`、`Autograd`、损失与模型接口都能在源码中核对。能力清单把 CPU 精确 Number、四格式设备转换、卷积／attention、损失族、优化器族与 `DataLoader` 等列入已覆盖能力域，这是能力范围声明，不是逐平台运行验收证据。
    设备后端文档把 Windows D3D11、macOS Metal、Linux／FreeBSD／Android Vulkan 写成源码完成条件，并明确跨平台构建、运行、性能与设备验收仍需分别报告；语言模型示例的源码也注明尚未构建或执行。因此这些示例是对接口的写法说明，不要当作“已在当前版本跑通”或已在某块 GPU 上验收的保证。

## 数据与保存

`Dataset<sample: Number>(values)` 保存样本快照；`Sampler(size, seed:, shuffle:, rank:, world:, dropRemainder:)` 产生索引序列；`DataLoader<sample: Number>(dataset, sampler, batchSize:, dropLast:)` 按批调用 `next(collate)`，`collateTensors(element, samples)` 把同形状样本堆成带批次轴的张量。loader 的 `save()`／`restore()` 保存与恢复采样游标。

训练状态用 `TrainingCheckpoint<element: Number>()`：`save` 写参数、优化器状态、随机数与缓冲区，`restore` 通过显式的 `readHost`／`upload` 边界恢复。`StreamingTrainingCheckpoint` 提供分块读写。公开静态权重用 `SafeTensorFile`、`SafeTensorIndex` 与 `LlamaLoader` 读取；它们只读公开格式，不承担训练。需要并行预取时还有 `ParallelDataLoader` 与 `StreamDataset`。

## 继续阅读

- [数值与位类型](../language/numeric-types.md)：`Number`、`BitFloat` 与设备浮点元素的数值合同。
- [运算符与表达式](../language/operators.md)：矩阵乘、逐元素运算与广播的解析规则。
- [集合与文本](collections.md)：数组与样本容器的基本操作。
