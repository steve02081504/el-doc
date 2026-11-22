# numerical-computing/arrays.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值张量构造 {#api-1f6f5bf50fb9c02b3969}

源码：`src/stdlib/numerical-computing/arrays.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L7)

提供常用张量初始化、行列向量、采样点和列优先展开函数。

## ones {#api-24bc34d3ad4af842ed3e}

源码：`src/stdlib/numerical-computing/arrays.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L23)

创建形状指定且所有元素均为 1 的张量。

```el-signature
export fn ones(element: type, shape: Number[])
```

**参数**：element 张量元素类型，须能从数值 1 构造。

**参数**：shape 各轴长度；空数组表示标量张量。

**返回值**：由独立连续存储支持的张量。

### 示例：创建一个 2×2 的全一张量

```el
let values = ones<element: Number>(@[2, 2])
```

<span id="api-b98ba9e759d7eef8e401"></span>

## row~construct {#api-5c1c5315cba24f3b9d0c}

源码：`src/stdlib/numerical-computing/arrays.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L37)

将输入值转换为指定元素类型，并构造成单行二维张量。

```el-signature
export fn row(element: type, values)
```

**参数**：element 输出张量的元素类型。

**参数**：values 按顺序转换并放入行中的值。

**返回值**：形状为 [1, values.count] 的张量。

### 示例：从两个数构造一行

```el
let values = row<element: Number>(@[2, 3])
```

## row~reshape {#api-9eb863b8b4a108974ea1}

源码：`src/stdlib/numerical-computing/arrays.el:49` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L49)

将一维张量重塑为只有一行的二维张量。

```el-signature
export fn row(values)
```

**参数**：values rank-1 输入张量。

**返回值**：形状为 [1, count] 的重塑结果。

**失败与异常**：ShapeError 当输入不是 rank 1 时抛出。

### 示例：将向量转为行向量（需调用方提供对象或绑定）

```el
// @external sourceVector: Tensor<element: Number>
let values = row(sourceVector)
```

<span id="api-583fcaa3af9e70e0647b"></span>

## col~reshape {#api-cc7a5482094f12f275cb}

源码：`src/stdlib/numerical-computing/arrays.el:60` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L60)

将一维张量重塑为只有一列的二维张量。

```el-signature
export fn col(values)
```

**参数**：values rank-1 输入张量。

**返回值**：形状为 [count, 1] 的重塑结果。

**失败与异常**：ShapeError 当输入不是 rank 1 时抛出。

### 示例：将向量转为列向量

```el
// @external columnInput: Tensor<element: Number>
let values = col(columnInput)
```

## linspace {#api-fca937978fc3c8b3c9c5}

源码：`src/stdlib/numerical-computing/arrays.el:72` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L72)

在首尾端点之间生成指定数量的等间距元素。

```el-signature
export fn linspace(element: type, first, last, count: Number)
```

**参数**：element 输出元素类型。

**参数**：first 起始端点。

**参数**：last 结束端点；count 为 1 时唯一元素取此端点。

**参数**：count 输出元素数，必须是非负整数。

**返回值**：形状为 [count] 的一维张量。

### 示例：生成五个采样点

```el
let points = linspace<element: Number>(0, 1, 5)
```

## columnMajor {#api-56f1a6c6f3a062e45618}

源码：`src/stdlib/numerical-computing/arrays.el:106` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L106)

按张量的列优先逻辑顺序展平为一维张量。

```el-signature
export fn columnMajor(source)
```

**参数**：source 待展开的张量。

**返回值**：元素次序不变、形状为 [source.count] 的张量。

### 示例：展开一个矩阵

```el
let values = columnMajor(@(1, 2; 3, 4))
```
