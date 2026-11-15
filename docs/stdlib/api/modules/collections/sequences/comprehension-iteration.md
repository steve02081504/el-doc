# collections/sequences/comprehension-iteration.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 类型化惰性迭代组合 {#api-62cf195a08f1a0efe0f4}

源码：`src/stdlib/collections/sequences/comprehension-iteration.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension-iteration.el#L1)

用普通工厂和游标组合单值、条件与有序展平，保留元素类型；也是推导宏的实现基础。
返回值支持普通 for 遍历及 collect()，不承诺提供 Sequence 的其他链式方法。原生执行尚未验收。

## singleton {#api-e9c1a017b7d3372054d3}

源码：`src/stdlib/collections/sequences/comprehension-iteration.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension-iteration.el#L75)

构造只产出一个值的惰性可迭代对象。

```el
export fn singleton(producer)
```

**参数**：producer 无参数工厂；每个游标的首次 next 才调用一次。

**返回值**：元素类型来自工厂返回类型的可重开对象；collect() 将元素收集为数组。

**失败与异常**：工厂异常正常传播；失败后的游标保持结束状态。

**注意**：提前关闭尚未读取的游标不会调用工厂。重新迭代会再次计算，不缓存上次结果。

### 示例：延迟一次计算

```el
import { singleton } from "el:collections/sequences/comprehension-iteration.el"
let calls = 0
let values = singleton(() => { calls++; return 7 })
// calls 为 0。
let result = values.collect() // @[7]；calls 为 1。
```

## guarded {#api-e493441f4d4d0b54d914}

源码：`src/stdlib/collections/sequences/comprehension-iteration.el:151` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension-iteration.el#L151)

按需检查条件，条件成立时才打开下游来源。

```el
export fn guarded(conditionFactory, outputFactory)
```

**参数**：conditionFactory 无参数条件工厂；每个游标首次 next 时调用一次。

**参数**：outputFactory 无参数可迭代来源工厂；条件为真时才调用一次。

**返回值**：保留下游元素类型的可重开可迭代对象；条件为假时该次迭代为空。

**失败与异常**：条件、来源和游标异常正常传播；已有错误与清理错误同时发生时保留原因并聚合清理错误。

**注意**：取得游标不调用两个工厂；已打开的游标关闭后才释放它对应的来源对象。

### 示例：条件为假时不创建下游

```el
import { guarded, singleton } from "el:collections/sequences/comprehension-iteration.el"
let opened = 0
let values = guarded(() => nil, () => { opened++; return singleton(() => 7) })
let result = values.collect() // @[]；opened 仍为 0。
```

## flatMap {#api-c361b1582755a3fc1e51}

源码：`src/stdlib/collections/sequences/comprehension-iteration.el:244` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension-iteration.el#L244)

按来源顺序为每个元素打开一个下游可迭代值，并依次产出其全部元素。

```el
export fn flatMap(sourceFactory, expand)
```

**参数**：sourceFactory 无参数可迭代来源工厂；每个游标首次 next 时调用一次。

**参数**：expand 接收一个来源元素，返回对应的下游可迭代值；每个实际访问的来源元素调用一次。

**返回值**：保留下游元素类型的可重开可迭代对象，提供 iterator() 与 collect()。

**失败与异常**：来源、展开函数和游标异常正常传播；已有错误与清理错误同时发生时保留原始原因并按清理顺序聚合。

**注意**：先耗尽当前下游再请求下一个来源元素；无限下游可能阻止后续来源元素被访问，不提供公平搜索。

**注意**：提前关闭按内游标、内来源、外游标、外来源的顺序清理；来源值一直保留到其游标关闭之后。

### 示例：顺序展平两个范围

```el
import { flatMap } from "el:collections/sequences/comprehension-iteration.el"
let values = flatMap(() => ..3, count => 0..count)
let result = values.collect() // @[0, 0, 1]。
```
