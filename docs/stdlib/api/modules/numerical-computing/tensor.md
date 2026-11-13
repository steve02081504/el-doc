# numerical-computing/tensor.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值张量 {#api-0c5b8f6b01bf3f9f281e}

源码：`src/stdlib/numerical-computing/tensor.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L28)

提供带元素类型、形状、广播与线性代数运算的多维稠密张量。

## Tensor {#api-7c7e7cebd20d307966e1}

源码：`src/stdlib/numerical-computing/tensor.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L41)

```el
export fn Tensor(element: type): type
```

创建指定元素类型的张量类型；实例由形状和按列优先排列的元素构成。

**参数**：element 张量元素类型。

**返回值**：可构造该元素类型张量的类型。

### 示例：创建一个 2×2 Number 张量

```el
let Dense = Tensor<element: Number>
let matrix = Dense(@[2, 2], @[1, 2, 3, 4])
```
示例展示接口用法；未运行验证。

## Tensor.rank {#api-8989b012c5ff4897d155}

源码：`src/stdlib/numerical-computing/tensor.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L118)

```el
get rank(): Number
```

返回张量的轴数；标量张量的 rank 为 0。

**返回值**：形状数组中的维度数。

### 示例：查询张量阶数

```el
let dimensions = tensor.rank
```

## Tensor.count {#api-8f71ce2d0b728ce22cc4}

源码：`src/stdlib/numerical-computing/tensor.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L138)

```el
get count(): Number
```

返回张量包含的逻辑元素数。

**返回值**：所有轴长度的乘积；标量张量为 1。

### 示例：查询张量元素总数

```el
let elements = tensor.count
```

## Tensor.extent {#api-38b5b9e81e2498a3e6bb}

源码：`src/stdlib/numerical-computing/tensor.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L148)

```el
fn extent(axis: Number): Number
```

返回指定轴的长度。

**参数**：axis 轴编号，从 0 开始。

**返回值**：指定轴的元素数。

**失败与异常**：ShapeError 当轴超出 rank 范围时抛出。

### 示例：查询矩阵列数

```el
let columns = matrix.extent(1)
```

## Tensor.shape {#api-8a47192a9a127d6b6d2b}

源码：`src/stdlib/numerical-computing/tensor.el:156` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L156)

```el
fn shape(): Number[]
```

返回描述各轴长度的独立数组快照。

**返回值**：按轴编号排列的长度数组。

### 示例：读取张量形状

```el
let dimensions = tensor.shape()
```

## Tensor.flat {#api-825767ce76fe7eef8efd}

源码：`src/stdlib/numerical-computing/tensor.el:166` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L166)

```el
fn flat(index: Number): element
```

按列优先线性索引读取一个元素。

**参数**：index 零基逻辑元素索引。

**返回值**：对应位置的元素值。

**失败与异常**：ShapeError 当 index 超出元素范围时抛出。

### 示例：读取展平后的首个元素

```el
let first = tensor.flat(0)
```

## Tensor.select {#api-d8dd2e62324729c9b49e}

源码：`src/stdlib/numerical-computing/tensor.el:220` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L220)

```el
@optimize(data: @{ reorder: reorderSelect })
		fn select(selectors: Selector[]): Value
```

按每个轴的标量或选择器抽取张量；标量选择会移除对应结果轴，范围选择保留该轴。

**参数**：selectors 按轴顺序提供、长度等于 rank 的选择器数组。

**返回值**：选取所得的新张量。

**失败与异常**：ShapeError 当选择器数量或范围与张量形状不匹配时抛出。

### 示例：用范围保留矩阵的列轴

```el
let selected = matrix.select(@[1, 0..3])
```

## Tensor.transpose {#api-7e4fb4ba61b8777c2bf6}

源码：`src/stdlib/numerical-computing/tensor.el:282` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L282)

```el
@optimize(data: @{ reorder: reorderTranspose })
		fn transpose(): Value
```

交换 rank-2 张量的两个轴并返回转置值。

**返回值**：行列交换后的新张量。

**失败与异常**：ShapeError 当输入不是 rank 2 时抛出。

### 示例：转置矩阵

```el
let transposed = matrix.transpose()
```

## Tensor.T {#api-fbb3a0168dd46111c500}

源码：`src/stdlib/numerical-computing/tensor.el:291` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L291)

```el
get T()
```

返回二维张量的转置；等价于调用 transpose()。

**返回值**：行列交换后的张量。

### 示例：使用 T 转置矩阵

```el
let transposed = matrix.T
```

## Tensor.matmul {#api-0cc7fa30cddda72138c2}

源码：`src/stdlib/numerical-computing/tensor.el:336` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L336)

```el
fn matmul(borrow other: Value)
```

执行张量矩阵乘法，包含批次轴时按广播后的批次形状计算。

**参数**：other 右操作数；收缩轴长度必须匹配。

**返回值**：矩阵乘积张量。

**失败与异常**：ShapeError 当两个操作数的矩阵维度不匹配时抛出。

### 示例：将系数矩阵乘以列向量

```el
let result = coefficients.matmul(vector)
```

## Tensor.slice {#api-9144b6f4fe4ac3b11647}

源码：`src/stdlib/numerical-computing/tensor.el:415` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L415)

```el
fn slice(axis: Number, start: Number, count: Number): Value
```

沿指定轴从 start 开始截取 count 个连续元素，其他轴保持不变。

**参数**：axis 要切片的轴。

**参数**：start 起始索引。

**参数**：count 切片长度。

**返回值**：切片所得的新张量。

**失败与异常**：ShapeError 当轴或切片范围越界时抛出。

### 示例：取矩阵的前两列

```el
let leading = matrix.slice(1, 0, 2)
```

## Tensor.scalar {#api-b1378abafa0ef3b02d23}

源码：`src/stdlib/numerical-computing/tensor.el:468` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L468)

```el
fn scalar(): element
```

读取 rank-zero 张量唯一的标量元素。

**返回值**：标量张量所含元素。

**失败与异常**：ShapeError 当张量 rank 不为 0 时抛出。

### 示例：读取已归约的损失值

```el
let lossValue = loss.scalar()
```

## Tensor.square {#api-3199e5962816d7efaa4d}

源码：`src/stdlib/numerical-computing/tensor.el:527` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L527)

```el
fn square(): Value
```

对张量逐元素平方。

**返回值**：与输入形状相同的平方结果。

### 示例：将误差张量逐元素平方

```el
let squared = error.square()
```

## Tensor.operator[] {#api-5fecdaf1aca28b5f3863}

源码：`src/stdlib/numerical-computing/tensor.el:617` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L617)

```el
operator[](...selectors: Selector)
```

用方括号按轴索引张量；标量下标移除对应轴，范围和冒号选择保留轴。

**参数**：selectors 按轴顺序给出的选择器。

**返回值**：所有轴都选为标量时返回元素，否则返回选取张量。

**失败与异常**：ShapeError 当下标数量或边界不合法时抛出。

### 示例：取矩阵一行并保留列轴

```el
let selected = matrix[1, 0..3]
```

## Tensor.operator+~tensor {#api-51f9006e889164679433}

源码：`src/stdlib/numerical-computing/tensor.el:649` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L649)

```el
operator +(other: Value)
```

对两个张量逐元素相加，形状按轴对齐的广播规则兼容。

**参数**：other 形状可广播的右操作数。

**返回值**：广播结果张量。

**失败与异常**：ShapeError 当形状不可广播时抛出。

### 示例：将偏置广播加到批次张量

```el
let shifted = batch + bias
```

## Tensor.operator+~scalar {#api-011941fe7f27cae1385a}

源码：`src/stdlib/numerical-computing/tensor.el:658` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L658)

```el
operator +(other)
```

将标量加到张量每个元素上，不改变张量形状。

**参数**：other 加数标量。

**返回值**：与接收者同形状的结果张量。

### 示例：给矩阵每个元素加一

```el
let shifted = matrix + 1
```

## Tensor.operator*~matmul {#api-86ecd494e284cf6ea6d2}

源码：`src/stdlib/numerical-computing/tensor.el:671` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L671)

```el
operator *(borrow other: Value)
```

两侧均为张量时执行矩阵乘法，而不是逐元素乘法。

**参数**：other 右矩阵或批次矩阵。

**返回值**：矩阵积。

**失败与异常**：ShapeError 当矩阵维度不匹配时抛出。

### 示例：矩阵向量乘法

```el
let result = coefficients * vector
```

## Tensor.operator*~scalar {#api-f516ec5297f69640fe7b}

源码：`src/stdlib/numerical-computing/tensor.el:680` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L680)

```el
operator *(other)
```

将标量乘到张量每个元素上，不执行矩阵乘法。

**参数**：other 缩放标量。

**返回值**：与接收者同形状的缩放结果。

### 示例：将矩阵缩放两倍

```el
let doubled = matrix * 2
```

## Tensor.operator.*~broadcast {#api-7c07d1978993329814a0}

源码：`src/stdlib/numerical-computing/tensor.el:691` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L691)

```el
operator .*(other: Value)
```

按广播规则逐元素相乘；与矩阵乘法运算符 * 区分。

**参数**：other 形状可广播的右操作数。

**返回值**：逐元素乘积张量。

**失败与异常**：ShapeError 当形状不可广播时抛出。

### 示例：计算逐元素平方

```el
let squares = values .* values
```

## Tensor.operator.*~scalar {#api-b9b6c6c9e508dff7f537}

源码：`src/stdlib/numerical-computing/tensor.el:700` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L700)

```el
operator .*(other)
```

将标量乘到张量每个元素上，保持逐元素运算写法。

**参数**：other 标量操作数。

**返回值**：与接收者同形状的结果张量。

### 示例：逐元素缩放矩阵

```el
let scaled = matrix .* 2
```

## Tensor.operator.^~scalar {#api-14a097654827e65155e7}

源码：`src/stdlib/numerical-computing/tensor.el:712` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/tensor.el#L712)

```el
operator .^(other)
```

对张量每个元素分别计算指定标量指数的幂。

**参数**：other 标量指数。

**返回值**：与接收者同形状的幂结果张量。

### 示例：对矩阵元素分别平方

```el
let squares = matrix .^ 2
```
