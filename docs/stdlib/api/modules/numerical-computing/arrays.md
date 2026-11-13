# numerical-computing/arrays.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值张量构造 {#api-1f6f5bf50fb9c02b3969}

源码：`src/stdlib/numerical-computing/arrays.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L7)

提供常用张量初始化、行列向量、采样点和列优先展开函数。

<span id="api-b98ba9e759d7eef8e401"></span>

## row~reshape {#api-9eb863b8b4a108974ea1}

源码：`src/stdlib/numerical-computing/arrays.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L30)

```el
export fn row(values)
```

将一维张量重塑为只有一行的二维张量。

**参数**：values rank-1 输入张量。

**返回值**：形状为 [1, count] 的重塑结果。

**失败与异常**：ShapeError 当输入不是 rank 1 时抛出。

### 示例：将向量转为行向量

```el
let values = row(vector)
```

<span id="api-583fcaa3af9e70e0647b"></span>

## col~reshape {#api-cc7a5482094f12f275cb}

源码：`src/stdlib/numerical-computing/arrays.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L40)

```el
export fn col(values)
```

将一维张量重塑为只有一列的二维张量。

**参数**：values rank-1 输入张量。

**返回值**：形状为 [count, 1] 的重塑结果。

**失败与异常**：ShapeError 当输入不是 rank 1 时抛出。

### 示例：将向量转为列向量

```el
let values = col(vector)
```

## linspace {#api-fca937978fc3c8b3c9c5}

源码：`src/stdlib/numerical-computing/arrays.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L52)

```el
export fn linspace(element: type, first, last, count: Number)
```

在首尾端点之间生成指定数量的等间距元素。

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

源码：`src/stdlib/numerical-computing/arrays.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/arrays.el#L86)

```el
export fn columnMajor(source)
```

按张量的列优先逻辑顺序展平为一维张量。

**参数**：source 待展开的张量。

**返回值**：元素次序不变、形状为 [source.count] 的张量。

### 示例：展开一个矩阵

```el
let values = columnMajor(@(1, 2; 3, 4))
```
