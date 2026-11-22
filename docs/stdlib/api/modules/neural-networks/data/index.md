# neural-networks/data/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [DataLoader.hasNext](#api-58e98b45921aef94fd81)
- [DataLoader.save](#api-e9c87836c8629fb1669a)
- [DataLoader.restore](#api-45d2fb6c47561221639f)
- [DataLoader.next~collate](#api-d4dc9ac658fe6e9c968a)
- [DataLoader.next~samples](#api-4232412f3e2beb1e4a64)

## 神经网络数据加载 {#api-5723adb17123dbcbdba2}

源码：`src/stdlib/neural-networks/data/index.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L6)

提供数据集快照、采样器、批次整理与可保存游标的数据加载器。

## Dataset {#api-3357d451b8096d9150b6}

源码：`src/stdlib/neural-networks/data/index.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L36)

创建拥有样本快照的数据集类型；map 在被请求时执行变换。

```el-signature
export fn Dataset(sample: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：sample 每个样本的类型。

**返回值**：可通过 count、at 与 map 访问的数据集类型。

### 示例：创建并读取一个数值数据集

```el
let Data = Dataset<sample: Number>
let dataset = Data(@[0, 1])
let first = dataset.at(0)
```
示例展示接口用法；未运行验证。

## Sampler {#api-4b5c3036774cf3474e52}

源码：`src/stdlib/neural-networks/data/index.el:80` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L80)

创建可复现的样本索引采样器，支持打乱、分布式分片和游标快照。

```el-signature
export @assign(mode: "copy") class Sampler
```

**参数**：size 数据集样本数。

**参数**：seed 随机种子。

**参数**：shuffle 是否按种子与 epoch 打乱索引。

**参数**：rank 当前分片编号；必须小于 world。

**参数**：world 分片总数。

**参数**：dropRemainder 是否丢弃无法均匀分片的尾部索引。

**返回值**：可迭代索引并保存或恢复游标的采样器。

### 示例：创建顺序采样器并读取首个索引

```el
let sampler = Sampler(2, shuffle: f)
let first = sampler.peek()
```
示例展示接口用法；未运行验证。

## DataLoader {#api-e8831068236aaaf353d3}

源码：`src/stdlib/neural-networks/data/index.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L140)

创建按 Sampler 索引批次读取 Dataset 的数据加载器类型。

```el-signature
export fn DataLoader(sample: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：sample 每个数据样本的类型。

**返回值**：可构造带 hasNext、next、save 和 restore 操作的加载器类型。

### 示例：从数据集分批读取样本

```el
import { Dataset, Sampler, DataLoader } from "el:neural-networks/data/index.el"
let Data = Dataset<sample: Number>
let Loader = DataLoader<sample: Number>
let dataset = Data(@[10, 20, 30])
let loader = Loader(dataset, Sampler(3, shuffle: f), batchSize: 2)
let firstBatch = loader.next()
```
示例展示接口用法；未运行验证。

## DataLoader.hasNext {#api-58e98b45921aef94fd81}

源码：`src/stdlib/neural-networks/data/index.el:159` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L159)

指示是否还有满足 dropLast 设置的数据可组成下一批。

```el-signature
get hasNext(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：存在下一批时为真。

### 示例：在耗尽前读取批次

```el
// @external consumeBatch: fn(Number[]): nil_t
while (loader.hasNext) consumeBatch(loader.next())
```

## DataLoader.save {#api-e9c87836c8629fb1669a}

源码：`src/stdlib/neural-networks/data/index.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L167)

返回可用于恢复当前采样进度的状态快照。

```el-signature
fn save(): SamplerState
```

**返回类型**：[`SamplerState`](../../../types.md#api-807b03f6837422f1581d)

**返回值**：SamplerState 快照。

### 示例：保存加载器游标

```el
let state = loader.save()
```

## DataLoader.restore {#api-45d2fb6c47561221639f}

源码：`src/stdlib/neural-networks/data/index.el:177` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L177)

将加载器游标恢复到兼容的采样状态。

```el-signature
fn restore(state: SamplerState)
```

**参数**：state 此加载器对应的采样状态。

**失败与异常**：InvalidDataState 当状态与采样配置不兼容时抛出。

### 示例：恢复已保存的进度

```el
let state = loader.save()
loader.restore(state)
```

<span id="api-06111c27e3c8c37e67a6"></span>

## DataLoader.next~collate {#api-d4dc9ac658fe6e9c968a}

源码：`src/stdlib/neural-networks/data/index.el:188` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L188)

读取下一批样本，先交给 collate 整理；整理成功后才前进采样游标。

```el-signature
fn next(collate)
```

**参数**：collate 接收样本数组并返回批次值的回调。

**返回值**：collate 返回的批次值。

**失败与异常**：InvalidDataState 当已无下一批时抛出。

### 示例：用默认张量整理器外的简单回调读取一批

```el
let batch = loader.next(samples => samples)
```

## DataLoader.next~samples {#api-4232412f3e2beb1e4a64}

源码：`src/stdlib/neural-networks/data/index.el:204` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/data/index.el#L204)

读取下一批样本并直接返回样本数组，不执行自定义整理。

```el-signature
fn next(): sample[]
```

**返回类型**：[`sample`](../../../types.md#api-1cf8247e11d20756443f)[]

**返回值**：下一批原始样本数组。

**失败与异常**：InvalidDataState 当已无下一批时抛出。

### 示例：读取原始样本批次

```el
let samples = loader.next()
```
