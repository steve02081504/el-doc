# 从遍历到函数组合

> 数正数、数负数，再取较大值：能不能让重复的处理只写一次，连比较里的零也只写一次？

!!! abstract "🎯 读完这页，你能"
    - 用循环、过滤和批量表达式写出同一个统计任务
    - 用 `over` 提取两条分支共有的处理
    - 分清源码只写一次、函数只调用一次和数组只遍历一次

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[函数与闭包](../language/functions.md)、[集合与文本](collections.md)</span>

这一页处理整数数组：忽略零，分别数出正数和负数的数量，返回两者中较大的一个。输入 `@[-3, -1, 0, 2, 4, 7]` 时，负数有 2 个、正数有 3 个，答案是 3。空数组和全零数组的答案都是 0。

!!! note "实现状态"
    本页依据当前标准库源码与语言合同讲解。函数组合、比较包装器及数组 batch/keep 已有源码，目标写法尚未经过编译和实际运行验收；seed 的相关宏接口也未构建验证。以下结果是按合同推导的预期结果，不是执行记录。后面的遍历融合是优化目标，标记为未实现。

## 先用 for 把事情说清楚

将下面的完整程序保存为 `maximum-count.el`。准备好配套 EL 工具后，可用 `el run maximum-count.el` 运行；如果当前工具还不支持后面的宏写法，先阅读其逐步展开的含义。

```el
fn maximumCount(a) {
	let positives = 0
	let negatives = 0
	for (let value in a) {
		if (value > 0) positives++
		else if (value < 0) negatives++
	}
	return max(positives, negatives)
}

console.stdout.writeLine(maximumCount(@[-3, -1, 0, 2, 4, 7]))
```

预期输出：

```text
3
```

循环逐个读取元素，两个变量负责累计数量，零不会增加任何一个计数。这个版本只遍历一次数组，也不创建过滤后的数组。

`max(left, right)` 返回较大值，`min(left, right)` 返回较小值。两者都是默认前导导入的标准库函数。把最后一行改成 `min(positives, negatives)`，这组输入的结果就是 2。

后续代码块都是这个函数的替换版本：每次保留一个 `maximumCount` 定义，底部的调用不变。

## 用 filter 描述要保留哪些值

`filter` 接收一个判断函数，返回满足条件的元素组成的新数组；读取它的长度，就得到了数量。

```el
fn maximumCount(a) {
	let positives = a.filter(value => value > 0).count
	let negatives = a.filter(value => value < 0).count
	return max(positives, negatives)
}
```

第一条过滤得到 `@[2, 4, 7]`，第二条得到 `@[-3, -1]`。它们的长度分别是 3 和 2。

如果这两个中间名字没有提供额外信息，也可以直接写：

```el
fn maximumCount(a) {
	return max(
		a.filter(=> it > 0).count,
		a.filter(=> it < 0).count
	)
}
```

`=> it > 0` 是匿名函数，也叫 lambda。这里的 `it` 指该判断函数收到的当前元素，等价于上一版的 `value`。

??? question "先猜：数组长度是 6，两个 count 会不会都得到 6？"
    不会。这里先过滤，再取长度，得到 3 和 2。若先把每个元素映射成真假值而不丢弃任何元素，结果数组仍有 6 项，取长度才会得到 6。

这版表达了两次独立过滤。仅仅省略中间变量，不会自动变成单次遍历。

## 用 batch 和 keep 合在一处描述批量处理

`batch` 是标准库宏。它把块内用到的外部数组绑定投影到对应元素，让普通表达式逐元素执行；这里块内的 `a` 表示当前元素。

```el
fn maximumCount(a) {
	return max(
		(batch { keep(a > 0) }).count,
		(batch { keep(a < 0) }).count
	)
}
```

`keep` 是 batch 元素函数内的局部宏。条件不成立就丢弃当前元素，并结束这次元素处理。条件涉及的展开来源只有 `a`，所以通过时 keep 的值就是当前 `a` 元素；batch 把这些值收集成过滤后的数组。

这里有两个层次：keep 的一次调用产生元素值，整个 batch 产生数组。括号只是为了让读者看清 `.count` 作用于哪个结果。

!!! warning "常见坑：比较出了真假，却没有过滤"
    `(batch { a > 0 }).count` 对这组输入得到 6。比较改变了每个位置上的值，却没有减少位置数量。要统计满足条件的元素，使用 keep 过滤后再取长度。

keep 条件同时涉及两个不同的展开绑定时，不会猜该返回哪一个；条件通过时它的正常值是 `void`。需要输出哪个值，就显式写在后面。例如下面是一个独立的过滤片段：

```el
let a = @[1, 5, 3]
let b = @[2, 4, 3]
let selected = batch {
	keep(a > b)
	a
}
```

预期 `selected` 为 `@[5]`。同一绑定在条件里出现两次仍算一个来源；两个不同绑定则算两个，不根据它们是否指向同一对象改变返回类型。

## 把共同的处理提取为一个函数

两条分支的共同部分是“根据某种比较过滤，然后取长度”；真正不同的只有比较方向。可以把比较函数传进去：

```el
fn maximumCount(a) {
	let countBy = fn(compare) => (batch {
		keep(compare(a, 0))
	}).count
	return max(countBy(greater), countBy(less))
}
```

`countBy` 捕获外面的数组，接收一个二元比较函数。调用 `countBy(greater)` 时，条件相当于 `a > 0`；传入 `less` 时则相当于 `a < 0`。

现在 batch、keep、count 和零都只写了一次。函数仍调用两次，但它的定义不必复制两份。

标准库提供六种比较包装器，它们直接调用对应运算符，保留运算符自己的结果与效果：

| 函数 | 对应表达式 |
| --- | --- |
| `greater(left, right)` | `left > right` |
| `less(left, right)` | `left < right` |
| `greaterEqual(left, right)` | `left >= right` |
| `lessEqual(left, right)` | `left <= right` |
| `equal(left, right)` | `left == right` |
| `notEqual(left, right)` | `left != right` |

它们是普通函数，可以像其他值一样传递，不是关键字。对于整数，把比较函数换成 `greaterEqual` 会把零算进去，因此会改变本题要求。

## 用 over 表达“两边同样处理，再合并”

`over(merge, transform)` 返回一个二元函数。调用这个新函数时，它依次变换两个实参，再把两个结果交给合并函数。

下面是调用顺序的示意：

```text
over(merge, transform)(left, right)

先得到 transformedLeft  = transform(left)
再得到 transformedRight = transform(right)
最后得到 merge(transformedLeft, transformedRight)
```

所以前一版函数的最后一行可以改成：

```el
return over(max, countBy)(greater, less)
```

这行代码中，两个输入是比较函数，变换是过滤并计数，合并是取较大值。把只用一次的 `countBy` 放回调用处，就得到完整版本：

```el
fn maximumCount(a) {
	return over(max, fn(compare) => (batch {
		keep(compare(a, 0))
	}).count)(greater, less)
}
```

最后，把匿名函数参数改用 `it`，省略这里不需要的括号：

```el
fn maximumCount(a) {
	return over(max, => batch {
		keep(it(a, 0))
	}.count)(greater, less)
}
```

==这个 it 表示传进来的比较函数，而不是数组元素。== batch 不会用隐藏参数覆盖调用方的 it；数组元素由块内的 a 表示。第一次调用该 lambda，it 是 greater；第二次是 less。

??? question "先猜：batch 只写了一次，会只执行一次吗？"
    不会。over 的 transform 按左、右顺序调用两次，所以这个 lambda 里的 batch 也执行两次。左侧处理失败时不会执行右侧处理或最后的合并。

over 不局限于这道题。下面是一个独立片段，分别求两个数组的长度再取较小值：

```el
let shorterLength = over(min, => it.count)(@[1, 2, 3], @[4, 5])
```

预期 `shorterLength` 为 2。它返回长度，不返回较短的原数组。

## 写得简洁与运行得高效可以分别考虑

| 写法 | 直接执行时的遍历 | 中间过滤数组 |
| --- | --- | --- |
| for 加两个计数器 | 一次 | 不需要 |
| 两次 filter 后取长度 | 两次过滤遍历 | 有 |
| 两次 batch/keep 后取长度 | 两次批量遍历 | 有 |
| over 复用批量计数 | 两次 transform | 与变换函数有关，本例有 |

四种写法解决同一个问题。循环版本明确指定累计过程；后几种更直接表达“筛选、计数、组合”。选择时可以考虑读者是否容易看出意图，以及这段逻辑是否需要复用。

!!! note "未实现：将多次遍历优化到单次遍历的水平"
    EL 编译器的目标是在大部分可证明安全的常见场景下，把这种多次遍历优化到单次遍历的水平：消除只为计数而创建的中间数组，并把同一输入上的多路统计合并成一次扫描。本例中的整数比较与计数属于目标场景。目前尚未实现和验证，不能把上面的 over 版本当成已经获得了手写循环的性能。

优化必须保留程序合同。如果比较函数会输出日志、可能抛异常，或者数组读取本身有副作用，交错两条分支的执行就可能改变结果。编译器需要足够证据才可融合，不能仅凭函数名做替换；用户写出的等价普通函数也应有机会获得相同优化。

!!! example "动手：改数据，再预测结果"
    保留同一份函数定义，把底部输入改为 `@[0, 0, 0]`，预期结果为 0；改为 `@[-5, -2, 0, 1]`，预期结果为 2。再把合并函数从 max 改成 min，第二组输入的结果应变成 1。配套工具支持后，可以在同一个文件中运行核对。

## 带走这三样

- 过滤后取长度才是条件计数；布尔数组的长度仍是总元素数。
- keep 可从唯一展开来源取得默认元素值，多个来源时显式选择输出。
- over 复用两边相同的处理；只写一次不代表只调用一次，也不保证只遍历一次。

## 下一站：[性能与底层优化](../language/performance.md)

> 编译器能把哪些中间步骤消掉，又必须保留哪些可观察行为？

- 主推进：[性能与底层优化](../language/performance.md)：区分表达方式、优化依据与实际测量。
