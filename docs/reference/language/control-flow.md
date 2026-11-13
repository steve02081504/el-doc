# 控制流

## 条件表达式

`if condition { consequent } else { alternative }` 是表达式，值来自被选中块；省略 `else` 且条件为假时结果为 `void`。条件外层括号可省略。`switch (value) { case pattern => expression; default => expression }` 只求值一次 selector，分支不会贯穿。

## 循环

| 形式 | 行为 |
|---|---|
| `while condition { body }` | 每轮开始前判断条件。 |
| `do { body } while (condition)` | 执行循环体后判断，因此至少执行一次。 |
| `for (init; condition; step) body` | C 风格计数循环，括号必需。 |
| `for (let item in iterable) body` | 遍历元素；此形式的头部括号可省略。 |

循环结果为最后执行语句的值；零次迭代为 `void`。带标签的 `break` 可退出目标循环或块，带标签的 `continue` 只用于循环。在 C 风格循环中，`continue` 先完成清理，再执行步进表达式并检查条件。

`return` 离开函数；没有显式 `return` 时函数体返回最后执行语句的值。`throw` 进入异常处理。标签使用独立于普通名字的控制目标命名空间，跳转不能跨函数边界。`goto` 受区域入口、初始化与清理义务约束，不能指向任意语句。

## 相关条目

- [表达式与运算符](expressions.md)
- [函数](functions.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [范围循环与迭代器](https://github.com/steve02081504/el/blob/master/docs/spec/17-range-loops-and-iterators.md)
