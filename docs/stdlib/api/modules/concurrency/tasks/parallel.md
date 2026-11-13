# concurrency/tasks/parallel.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/concurrency.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 并行任务 {#api-a4a2f674987a607fa6aa}

源码：`src/stdlib/concurrency/tasks/parallel.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/tasks/parallel.el#L1)

提供有界并行映射与二分递归求解工具。

## parallel_map {#api-ff4dc52370410fcff59a}

源码：`src/stdlib/concurrency/tasks/parallel.el:78` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/tasks/parallel.el#L78)

```el
export fn parallel_map(values, transform, limit: Number = 0, minimum: Number = 32)
```

对可计数序列的元素应用变换，并按输入顺序收集结果。

**参数**：values 输入序列。

**参数**：transform 每个元素调用一次的变换函数。

**参数**：limit 最大参与并行预算，0 表示使用可用预算；预算包含调用方。

**参数**：minimum 只有元素数达到该阈值时才尝试并行。

**返回值**：与输入顺序对应的变换结果数组。

**失败与异常**：参数范围无效或变换/工作线程失败时传播错误；已启动的项目会完成。

**注意**：共享捕获需要调用方同步；嵌套调用和低于阈值的工作会串行执行。

### 示例：并行映射一组数

```el
import { parallel_map } from "el:concurrency/tasks/parallel.el"
let squares = parallel_map(@[1, 2, 3], value => value * value, 2, 1)
```

## parallel_divide {#api-dac72591c8ac45297242}

源码：`src/stdlib/concurrency/tasks/parallel.el:131` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/tasks/parallel.el#L131)

```el
export fn parallel_divide(problem, is_leaf, solve, split, merge, limit: Number = 0)
```

递归拆分问题，求解叶节点，并按子问题顺序合并两个结果。

**参数**：problem 当前问题值。

**参数**：is_leaf 判断问题是否已可直接求解。

**参数**：solve 求解叶问题的函数。

**参数**：split 将非叶问题拆为恰好两个子问题。

**参数**：merge 按左、右顺序合并两个子结果。

**参数**：limit 并行预算，0 表示使用可用预算。

**返回值**：根问题对应的合并结果。

**失败与异常**：拆分结果不是两个元素、预算无效或回调失败时传播错误。

### 示例：求和分治

```el
import { parallel_divide } from "el:concurrency/tasks/parallel.el"
let total = parallel_divide(4, value => value <= 1, value => value, value => @[value / 2, value / 2], (left, right) => left + right, 2)
```
