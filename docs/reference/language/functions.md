# 函数

| 查询 | 规则 |
| --- | --- |
| 参数 | 位置实参在具名实参前；实参从左到右各求值一次 |
| 默认值 | 省略或传 `void` 触发；`nil` 不触发 |
| 函数名取值 | 保留重载集，具体调用或目标契约才选择候选 |
| 闭包 | 捕获逻辑绑定，逃逸时保持绑定有效 |

## 声明与 lambda

```el
fn add(left: Number, right: Number) { left + right }
let increment = (value) => value + 1
```

具名函数可写为 `fn name(parameters) { ... }` 或 `fn name(parameters) => expression`；匿名函数可用 `fn(parameters)`，箭头 lambda 可写 `(parameters) => expression`。返回类型可推断，也可显式声明。参数支持类型注解、默认值、位置与具名实参，以及参数包形式。

## 默认参数与变参

默认参数在调用时按从左到右初始化。省略实参或传入 `void` 会触发默认表达式，传入 `nil` 不触发。默认表达式可引用已初始化的前序参数与函数可见的外部绑定，不能引用尚未初始化的后续参数；其副作用、异常和异步行为参与函数属性推断。

参数包可为静态异构序列（逐项保留类型和数量），也可为元素类型已知而运行时数量通常未知的序列。两者不是隐藏数组。固定形参调用要求编译期能确定展开后的参数数量及各位置类型；可变尾部可接收运行时序列。实参按源码从左到右各求值一次。

具名实参写作 `f(1, right: 2)`；位置实参必须在具名实参之前。关键字名绑定声明参数，不会读取同名值。重复、未知或冲突绑定会诊断；具名参数不能绑定变参包。

## 重载与返回

函数名出现在取值位置时得到可调用体集合（重载集），不是立即选定单个函数。调用实参或具体目标函数类型提供足够信息时，才按候选适用程度选择唯一项；歧义会诊断。没有具体契约的传递或保存保留重载集，不随意选一个。

没有显式 `return` 时，函数返回最后执行语句的值。`return void` 明确返回无结果，`return nil` 返回 `nil`。闭包按词法绑定与生命周期规则捕获外部变量。

## 并发函数

EL 没有 `async`、`await` 关键字。异步属性由函数行为推断，普通调用在合同要求处自动等待。`spawn(() => expression)` 显式启动独立任务并返回 Promise；`.get()` 等待其结果。标准库的 `async { ... }` 和 `await(p)` 是宏。

## 相关条目

- [重载解析](overload-resolution.md)
- [生命周期、借用与清理](lifetimes.md)

- [控制流](control-flow.md)
- [执行与并发](execution.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [函数与生命周期](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)
- [核心语义](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
