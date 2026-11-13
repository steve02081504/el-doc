# numerical-computing/reductions.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值张量归约 {#api-87971c168de59c1f7b6a}

源码：`src/stdlib/numerical-computing/reductions.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/reductions.el#L11)

提供张量求和、均值、乘积、极值与布尔归约。

## sum~all {#api-d58fd8966d5de0726a4a}

源码：`src/stdlib/numerical-computing/reductions.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/reductions.el#L39)

```el
export fn sum(values)
```

对张量的全部元素求和；空张量返回加法单位元 0。

**参数**：values 待归约张量。

**返回值**：元素类型对应的总和。

### 示例：对矩阵全部元素求和

```el
let total = sum(@(1, 2; 3, 4))
```

## sum~axis {#api-da20ccaa7740d44e7fec}

源码：`src/stdlib/numerical-computing/reductions.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/reductions.el#L53)

```el
export fn sum(values, axis: Number)
```

沿指定轴求和，并将该轴长度保留为 1。

**参数**：values 待归约张量。

**参数**：axis 要归约的轴编号。

**返回值**：归约轴长度为 1 的张量。

**失败与异常**：ShapeError 当轴不是有效维度时抛出。

### 示例：沿第 0 轴求和

```el
let totals = sum(@(1, 2; 3, 4), 0)
```

## mean~all {#api-1b092a7a4f6058d36233}

源码：`src/stdlib/numerical-computing/reductions.el:66` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/reductions.el#L66)

```el
export fn mean(values)
```

对张量全部元素求算术平均值。

**参数**：values 非空待归约张量。

**返回值**：全部元素的算术平均值。

**失败与异常**：EmptyReduction 当张量为空时抛出。

### 示例：计算矩阵平均值

```el
let average = mean(@(1, 2; 3, 4))
```

## mean~axis {#api-f52f0b1491a320de2f06}

源码：`src/stdlib/numerical-computing/reductions.el:81` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/reductions.el#L81)

```el
export fn mean(values, axis: Number)
```

沿指定轴求算术平均值，并将该轴长度保留为 1。

**参数**：values 待归约张量。

**参数**：axis 要归约的轴编号。

**返回值**：归约轴长度为 1 的张量。

**失败与异常**：EmptyReduction 当归约轴长度为零时抛出。

### 示例：沿第 0 轴取均值

```el
let averages = mean(@(1, 2; 3, 4), 0)
```
