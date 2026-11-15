# 用推导式列出组合

> 两个开关各有“关、开”两种状态，怎样一次列出所有组合，再选出状态相同的组合？

!!! abstract "🎯 读完这页，你能"
    - 用两个 `for let` 子句列出两位二进制的四种组合
    - 用 `if` 选出需要的结果，用 `any/all` 判断条件
    - 判断一段生成式何时开始计算

    <span class="el-chip">⏱ 约 10 分钟</span> <span class="el-chip">前置：[控制流](../language/control-flow.md) · [集合与文本](collections.md)</span>

这一页使用 `0` 表示关、`1` 表示开；`left` 和 `right` 分别表示左、右开关。`..2` 依次给出 `0`、`1`，不包括 `2`。

!!! note "实现状态"
    当前源码已经接入下述语法，但尚未完成现代 EL 编译与原生执行验收。这里的结果是按规范和源码静态核对的预期行为，不代表现有发行工具已经支持。需要支持该语法的编译器才能跟做；完整合同见[推导式参考](../reference/language/comprehensions.md)。

## 先列出四种组合

把下面的完整程序保存为 `switches.el`；编译器支持该语法时，用 `el run switches.el` 运行。

```el
let pairs = @[@[left, right] for let left in ..2 for let right in ..2]
for (let pair in pairs) {
	console.stdout.writeLine(pair[0], " ", pair[1])
}
```

预期输出：

```text
0 0
0 1
1 0
1 1
```

最前面的 `@[left, right]` 决定每项结果长什么样。后面的两个 `for let` 负责取值：先固定左开关，再让右开关走完 `0`、`1`；然后左开关换到下一个值。这就是两组取值的全部组合，也叫笛卡尔积。

??? question "先猜：两个 for 会只得到 0 0 和 1 1 吗？"
    会得到四项。两个 `for` 表示嵌套遍历，右侧变量变化最快；它们不表示把两份数据按位置配对。

## 把筛选条件写在 if 后面

在第一个程序里，只替换 `pairs` 的初始化，保留打印循环：

```el
let pairs = @[@[left, right] for let left in ..2 for let right in ..2 if left == right]
```

预期输出变成：

```text
0 0
1 1
```

`if` 只保留条件成立的组合，最前面的表达式仍然决定输出。假如把最前面改成 `left + right`，得到的就是 `@[0, 2]`，而不是两对开关。

!!! example "动手 30 秒"
    把条件改成 `left != right`。预期只打印 `0 1` 和 `1 0`：这表示筛选条件选中了两个开关状态不同的组合。

不要把 `some` 放进生成子句来表示筛选。选出所有满足条件的结果用 `if`；判断是否至少有一个满足条件，用下面的 `any`。

## any 问有没有，all 问是不是全部

下面是另一份完整程序，可以保存为 `check-switches.el`。

```el
import { any, all } from "el:collections/arrays/operations.el"

let exists = any(left == right for let left in ..2 for let right in ..2)
let universal = all(left == right for let left in ..2 for let right in ..2)
console.stdout.writeLine("存在相等组合：", if (exists) "是" else "否")
console.stdout.writeLine("全部组合相等：", if (universal) "是" else "否")
```

预期输出：

```text
存在相等组合：是
全部组合相等：否
```

两个函数都返回真假值：这里 `exists` 为 `t`，`universal` 为 `nil`。`any` 看到首个真值就停止；`all` 看到首个假值就停止。它们不返回满足条件的变量组合。

显式导入很重要：默认环境里的裸 `any/all` 用于 Promise 组合。这里选择的是可迭代值归约函数，也可以用默认环境中的 `arrayAny/arrayAll` 别名。

来源为空时，没有成立的项，所以 `any` 返回 `nil`；也没有反例，所以 `all` 返回 `t`。下面是独立片段，包含所需导入：

```el
import { any, all } from "el:collections/arrays/operations.el"
let exists = any(value > 0 for let value in 0..0) // nil
let universal = all(value > 0 for let value in 0..0) // t
```

## 换成括号，等到需要时再计算

`@[...]` 会立即生成数组；括号中的生成式只创建一个可迭代值。下面的完整程序用计数记录来源何时被调用：

```el
let calls = 0
fn source() { calls++; return ..2 }
let values = (value * 10 for let value in source())
console.stdout.writeLine(calls)
let first = values.collect()
console.stdout.writeLine(calls, ": ", first.join(", "))
let second = values.collect()
console.stdout.writeLine(calls, ": ", second.join(", "))
```

预期输出：

```text
0
1: 0, 10
2: 0, 10
```

创建生成式和取得游标都不会执行来源、条件或投影；首次请求元素才开始。`collect()` 请求全部元素并收集成数组。再次迭代会重新调用来源，结果没有自动缓存。

调用实参中的生成式采用同一套惰性规则。因此 `any(条件 for let ...)` 可以提前停止，无需先构造完整数组。生成式可传给普通函数，消费者不限定为这两个名字；返回对象提供遍历和 `collect()`，其他方法要查实际接口，不把它当作完整的 `Sequence` API。

## 后面的来源可以依赖前面的值

下面的独立片段列出每个 `count` 对应的较小数字：

```el
let values = @[value for let count in ..3 for let value in 0..count]
// count 为 0：没有元素；为 1：产出 0；为 2：产出 0、1。
// values 为 @[0, 0, 1]。
```

也可以在两个 `for` 之间写 `if`。条件不成立时，后面的来源根本不会打开。绑定只在该推导式内有效；当前写法接受单个名字，尚不接受 `for let [left, right] in ...` 这样的解构绑定。

如果要把生成结果和普通项混在一个数组里，显式展开括号生成式：

```el
let values = @[-1, ...(value for let value in ..2), 2] // @[-1, 0, 1, 2]
```

直接写 `@[(value for let value in ..2)]` 会得到只含一个可迭代对象的数组，括号内的对象不会自动展开。更多作用域、异常和清理规则放在[推导式参考](../reference/language/comprehensions.md)。

## 带走这三样

- 最前面的表达式决定输出，`for let` 决定取值，`if` 决定保留哪些组合。
- `any/all` 判断真假，显式导入数组操作库即可选择这里的归约函数。
- 数组形式立即收集；括号和调用实参形式按需计算，重新迭代会重新计算。

## 下一站：从遍历到函数组合

> 当处理只有一份来源时，推导式和 map、filter 各自适合什么场景？

- 主推进：[从遍历到函数组合](function-composition.md)：把统计任务拆成筛选、变换与组合。
