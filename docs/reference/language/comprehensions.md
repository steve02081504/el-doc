# 推导式与惰性生成式

| 写法 | 结果与求值时机 |
|---|---|
| `@[expr for let name in source ...]` | 立即收集成数组 |
| `(expr for let name in source ...)` | 创建保留元素类型的惰性可迭代值 |
| `consume(expr for let name in source ...)` | 将惰性可迭代值作为普通实参传入 |
| `... if condition` | 条件成立时才执行后续子句和投影 |

!!! note "实现状态"
    语法、库实现及回归夹具已存在，现代 EL 的编译、原生执行和格式化验收尚未完成。独立 seed 的接口检查通过只证明宏源码接口可被发现，不证明生成式执行。本文示例为静态核对后的预期行为。

## 投影、绑定与筛选

```el
let pairs = @[@[a, b] for let a in ..2 for let b in ..2]
let equalPairs = @[@[a, b] for let a in ..2 for let b in ..2 if a == b]
// pairs：@[@[0, 0], @[0, 1], @[1, 0], @[1, 1]]
// equalPairs：@[@[0, 0], @[1, 1]]
```

投影在源码中写在最前面，但在全部绑定建立后解析。子句从左到右执行；多个 `for let` 表示嵌套遍历，最右侧变量变化最快，保留来源顺序与重复值，不隐式去重或逐项配对。

每个来源在相应外层组合进入时求值一次。来源表达式不能引用自己正在引入的绑定，后续来源可以引用此前绑定；同名名字按词法作用域遮蔽。条件只使用它所在位置已有的绑定，假时跳过后续子句和投影。当前库宏只接受单个名字 binder，不接受解构模式。

```el
let values = @[b for let a in ..3 if a != 1 for let b in 0..a]
// a 为 0 时内层为空；为 1 时被筛掉；为 2 时产出 0、1。
// values：@[0, 1]。
```

直接数组推导式必须是唯一数组项。混合普通项时写 `@[-1, ...(x for let x in ..2), 2]`；`@[(x for let x in ..2)]` 则包含一个可迭代对象。数组收集沿普通数组展开与字面量提供者合同处理，保留声明的元素类型。

## 惰性值可以传给普通消费者

创建惰性值或取得游标都不执行来源、条件和投影，首次 `next()` 才开始。每次取得游标独立遍历，重新求值来源；不缓存结果，不替调用方重置一次性游标。返回对象提供 `iterator()` 与 `collect()`，后者将所有元素收集成数组，不代表提供完整的 `Sequence` 方法集合。

调用可带其他位置实参或具名实参，也可以使用消费者别名或成员调用。编译器不按消费者的名字决定生成式含义。

```el
fn total(values): Number {
	let result = 0
	for (let value in values) result += value
	return result
}
let sum = total(a + b for let a in ..2 for let b in ..2) // 4
```

## any/all 返回真假值

```el
import { any, all } from "el:collections/arrays/operations.el"
let exists = any(a == b for let a in ..2 for let b in ..2) // t
let universal = all(a == b for let a in ..2 for let b in ..2) // f
```

数组操作库的 `some/any/none/all/every` 省略 predicate 时，判断每个元素本身的普通条件行为；显式 predicate 的原有调用形式仍可用。`any` 遇到首个真值短路，`all` 遇到首个假值短路；空来源分别返回 `f` 和 `t`。这些运行期结果不会生成证明层的 `forall` 命题或证明。

默认环境的裸 `any/all` 属于 Promise 组合。这里使用显式导入，或使用默认环境的 `arrayAny/arrayAll` 别名。函数详见[数组操作 API](../../stdlib/api/modules/collections/arrays/operations.md)。

量词嵌套顺序有意义：

```el
import { any, all } from "el:collections/arrays/operations.el"
let eachHasMatch = all(any(a == b for let b in ..2) for let a in ..2) // t
let oneMatchesAll = any(all(a == b for let a in ..2) for let b in ..2) // f
```

## 退出时关闭已打开的游标

提前停止、耗尽或失败时，已打开的游标按内到外关闭；来源对象保留到对应游标关闭之后。原错误与清理错误同时发生时按普通 `CleanupError` 合同保留原因及清理错误；只有一个关闭错误时原样传播。未打开的下游来源不因退出而打开。

普通复制、共享、借用与异常合同仍适用。源码表达式在真实闭包中执行，普通 `return` 不透明退出外围调用者。无限来源或无限内层可能使遍历不终止，普通有序生成式不承诺公平搜索。

## 宏入口与核对依据

`for` 是默认 prelude 导入的标准库表达式后缀宏，使用通用 `ExprSuffix` 接点，在完整绑定域内解析投影；类型化迭代组合负责按需遍历，不要求协程调度器。宏导入别名保持声明身份。

- [动手教程：用推导式列出组合](../../stdlib/comprehensions.md)
- [推导宏 API](../../stdlib/api/modules/collections/sequences/comprehension.md)
- [类型化惰性迭代组合 API](../../stdlib/api/modules/collections/sequences/comprehension-iteration.md)
- [EL 语法规范](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [范围与迭代协议](https://github.com/steve02081504/el/blob/master/docs/spec/17-range-loops-and-iterators.md)
