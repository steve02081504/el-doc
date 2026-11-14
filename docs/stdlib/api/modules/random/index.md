# random/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/random.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [Random.seed](#api-f67e41d7ecf4e4cd8c79)
- [Random.reseed](#api-b10f87f55955d4297680)
- [Random.nextWord](#api-792c160b0802c5d93977)
- [Random.nextBits](#api-dc108d59626669d79b43)
- [Random.between](#api-cc4a8e461bbf2f97ad80)
- [Random.betweenExclusive](#api-e99cb6140b0881ce2db8)
- [Random.unit](#api-3bd6f39bf7301f499820)
- [Random.realBetween](#api-d06ddbd268a99ed5151c)
- [Random.boolean](#api-6e4a27bee2d63ff38225)
- [Random.pick](#api-3277706d087c8d369660)
- [Random.bytes](#api-ced6c72398fdb237f1e5)
- [Random.shuffle](#api-2622caa6ab97ff7091e9)

## 随机数 {#api-dc3aa6c88fb0f8bdec24}

源码：`src/stdlib/random/index.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L17)

提供可播种的随机数生成器，以及由共享随机流支持的 rand 入口。

## Random {#api-b2206be230690600dd8e}

源码：`src/stdlib/random/index.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L41)

创建独立的可播种伪随机数流；复制实例会复制当前生成状态。

```el
@assign(mode: "copy")
export class Random
```

**参数**：seed 初始整数种子；省略时使用自动种子。

**失败与异常**：RangeError 当显式种子不满足非负整数范围时抛出。

**失败与异常**：EntropyUnavailable 当系统自动种子来源不可用且省略了种子时抛出。

### 示例：创建可重现的随机数流

```el
import { Random } from "el:random/index.el"
let random = Random(72)
let value = random.between(1, 6)
```
示例展示接口用法；未运行验证。

## Random.seed {#api-f67e41d7ecf4e4cd8c79}

源码：`src/stdlib/random/index.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L77)

返回构造或最近一次 reseed 使用的原始种子。

```el
get seed(): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**返回值**：当前流记录的种子值。

### 示例：查看随机流的种子

```el
let seed = Random(72).seed
```

## Random.reseed {#api-b10f87f55955d4297680}

源码：`src/stdlib/random/index.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L86)

将生成器状态重置为指定种子对应的初始状态。

```el
fn reseed(seed: Number)
```

**参数**：seed 新的有限非负整数种子。

### 示例：重置随机流

```el
let random = Random(1)
random.reseed(72)
```

## Random.nextWord {#api-792c160b0802c5d93977}

源码：`src/stdlib/random/index.el:103` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L103)

从随机流生成一个 8、16 或 32 位无符号字值。

```el
@optimize(data: @{ sortingScalar: "finiteInteger" })
	fn nextWord(width: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：width 允许的输出宽度：8、16 或 32。

**返回值**：对应宽度范围内的非负整数。

**失败与异常**：RangeError 当 width 不是支持的宽度时抛出。

### 示例：生成一个 16 位字

```el
let word = Random(72).nextWord(16)
```

## Random.nextBits {#api-dc108d59626669d79b43}

源码：`src/stdlib/random/index.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L137)

从随机流取得指定数量的随机位，并按高位优先累积为 Number。

```el
fn nextBits(bitCount: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：bitCount 非负整数位数；零返回零。

**返回值**：范围为 0 至 2^bitCount - 1 的整数。

**失败与异常**：RangeError 当位数为负数或非整数时抛出。

### 示例：生成八个随机位

```el
let bits = Random(72).nextBits(8)
```

## Random.between {#api-cc4a8e461bbf2f97ad80}

源码：`src/stdlib/random/index.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L167)

在两个整数端点之间均匀抽取整数，端点均包含且次序可互换。

```el
fn between(minimum: Number, maximum: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：minimum 第一个有限整数端点。

**参数**：maximum 第二个有限整数端点。

**返回值**：闭区间内的整数。

**失败与异常**：RangeError 当任一端点不是有限整数时抛出。

### 示例：掷一个六面骰

```el
let die = Random(72).between(1, 6)
```

## Random.betweenExclusive {#api-e99cb6140b0881ce2db8}

源码：`src/stdlib/random/index.el:192` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L192)

在两个整数端点之间抽取整数，包含较小端点但排除较大端点。

```el
@optimize(data: @{ sortingScalar: "finiteInteger", lengthRange: @{ firstArgument: 0, secondArgument: 1 } })
	fn betweenExclusive(minimum: Number, maximum: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：minimum 第一个有限整数端点。

**参数**：maximum 第二个有限整数端点；端点次序可互换。

**返回值**：对应半开区间中的整数。

**失败与异常**：RangeError 当端点非法或两端相等时抛出。

### 示例：抽取 0 到 5 的整数

```el
let index = Random(72).betweenExclusive(0, 6)
```

## Random.unit {#api-3bd6f39bf7301f499820}

源码：`src/stdlib/random/index.el:213` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L213)

在二进制网格上抽取 [0, 1) 内的数；inclusive 为真时包含 1。

```el
fn unit(bitCount: Number = Number(53), inclusive: Bool = nil): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：bitCount 网格精度，必须为正整数，默认 53。

**参数**：inclusive 是否允许结果等于 1，默认否。

**返回值**：网格上的单位区间样本。

**失败与异常**：RangeError 当 bitCount 非正或非整数时抛出。

### 示例：生成单位区间样本

```el
let sample = Random(72).unit()
```

## Random.realBetween {#api-d06ddbd268a99ed5151c}

源码：`src/stdlib/random/index.el:232` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L232)

在两个有限实数端点之间按指定二进制网格精度抽样。

```el
fn realBetween(minimum: Number, maximum: Number, bitCount: Number = Number(53), inclusive: Bool = nil): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

**参数**：minimum 第一个有限端点。

**参数**：maximum 第二个有限端点；端点次序可互换。

**参数**：bitCount 正整数网格位数，默认 53。

**参数**：inclusive 是否允许达到上端点，默认否。

**返回值**：网格上的区间样本。

**失败与异常**：RangeError 当端点非有限或 bitCount 非正整数时抛出。

### 示例：抽取两个实数之间的值

```el
let sample = Random(72).realBetween(-1, 1)
```

## Random.boolean {#api-6e4a27bee2d63ff38225}

源码：`src/stdlib/random/index.el:249` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L249)

从随机流抽取一个布尔值。

```el
fn boolean(): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：以随机位决定的真或假。

### 示例：抛一次随机硬币

```el
let heads = Random(72).boolean()
```

## Random.pick {#api-3277706d087c8d369660}

源码：`src/stdlib/random/index.el:259` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L259)

从非空、可按整数索引读取的集合中均匀选择一个元素。

```el
fn pick(values)
```

**参数**：values count 为正数且支持零基索引的集合。

**返回值**：被选中的元素。

**失败与异常**：RangeError 当集合为空时抛出。

### 示例：从候选值中抽样

```el
let choice = Random(72).pick(@["red", "blue"])
```

## Random.bytes {#api-ced6c72398fdb237f1e5}

源码：`src/stdlib/random/index.el:273` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L273)

生成指定长度、每项取值 0 到 255 的随机字节数组。

```el
@optimize(data: @{ sortingResult: @{ fresh: t, element: "finiteInteger", minimum: 0, maximum: 255, lengthArgument: 0 } })
	fn bytes(count: Number): Array<element: Number>
```

**返回类型**：[`Array`](../../types.md#api-02f04934b15030edb96d)<element: [`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)>

**参数**：count 非负整数数组长度。

**返回值**：新建的字节值数组。

**失败与异常**：RangeError 当 count 为负数或非整数时抛出。

### 示例：生成四个随机字节

```el
let data = Random(72).bytes(4)
```

## Random.shuffle {#api-2622caa6ab97ff7091e9}

源码：`src/stdlib/random/index.el:290` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L290)

原地随机打乱可读写、支持 count 和整数索引的集合。

```el
fn shuffle(values)
```

**参数**：values 要被修改的集合。

**返回值**：无返回值；集合本身被重排。

### 示例：打乱数组中的项目

```el
let values = @[1, 2, 3]
Random(72).shuffle(values)
```

## rand {#api-0e70a2dfa7186c77e160}

源码：`src/stdlib/random/index.el:377` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/index.el#L377)

共享的线程安全随机数流；各调用按同一状态序列消耗随机值。

```el
export lazy let rand: SharedRandom = SharedRandom()
```

**类型**：[`SharedRandom`](../../types.md#api-ce68e64dbdcc8304c331)

### 示例：从默认随机流抽取整数

```el
import { rand } from "el:random/index.el"
let value = rand.between(1, 6)
```
示例展示接口用法；未运行验证。
