# 控制流

## 条件表达式

`if condition { consequent } else { alternative }` 是表达式，值来自被选中块；省略 `else` 且条件为假时结果为 `nil`。条件外层括号可省略。`switch (value) { case pattern => expression; default => expression }` 只求值一次 selector，分支不会贯穿。

## 控制头绑定

- `if let x = expression { ... }` 或 `if const x = expression { ... }`：只求值一次。结果不是 `nil` 时执行真分支并绑定 `x`；`f`、零和空文本仍是已有值。绑定在 `else` 与 `if` 之后不可见。
- `if (let x = initializer; condition) { ... } else { ... }`：先初始化一次，再判断条件。也可用 `const`，或用头部顶层换行替代分号。绑定在条件和两个分支中都可见，在整个 `if` 结束时清理。
- `switch let x = expression { case ... => ... }` 或 `switch const x = expression { case ... => ... }`：只求值一次，`x` 在各 `case` 检查和分支（包括 `default`）内可见。`nil` 也按普通 selector 匹配。 当前 ELC 的编译期条件导入不接受具名 selector。

以下写法先计算一次剩余库存，再用比较结果选分支。两个分支都能读取 `remaining`。

```el
let available = 3
let requested = 5
if (const remaining = available - requested; remaining >= 0) {
	console.stdout.writeLine("剩余 ", remaining)
} else {
	console.stdout.writeLine("缺少 ", -remaining)
}
```

输出为 `缺少 2`。

## 循环

| 形式 | 行为 |
|---|---|
| `while condition { body }` | 每轮开始前判断条件。 |
| `while let x = expression { body }` / `while const x = expression { body }` | 每轮求值一次；遇到 `nil` 结束，否则在本轮绑定 `x`。 |
| `do { body } while (condition)` | 执行循环体后判断，因此至少执行一次。 |
| `for (init; condition; step) body` | C 风格计数循环，括号必需。 |
| `for (let item in iterable) body` / `for (const item in iterable) body` | 遍历元素；此形式的头部括号可省略。`const` 禁止重绑本轮变量；结束由迭代器决定，而不是由元素是否为 `nil` 决定。 |

普通 `while` 的条件与循环体同一行时，写 `while (condition) body` 或 `while condition { body }`；也可以在条件后换行。

循环结果为最后执行语句的值；零次迭代为 `nil`。带标签的 `break` 可退出目标循环或块，带标签的 `continue` 只用于循环。在 C 风格循环中，`continue` 先完成清理，再执行步进表达式并检查条件。

`return` 离开函数；没有显式 `return` 时函数体返回最后执行语句的值。`throw` 进入异常处理。标签使用独立于普通名字的控制目标命名空间，跳转不能跨函数边界。`goto` 受区域入口、初始化与清理义务约束，不能指向任意语句。

## 相关条目

- [表达式与运算符](expressions.md)
- [函数](functions.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [范围循环与迭代器](https://github.com/steve02081504/el/blob/master/docs/spec/17-range-loops-and-iterators.md)
