# EL 语言参考

本参考按主题列出 EL 的语言合同。语法摘要与例子依据 EL 规范；示例用于说明写法，不表示已编译或执行。规范合同与当前实现状态应分别查阅。

| 主题 | 参考条目 |
|---|---|
| 词法元素与字面量 | [词法元素](lexical.md) |
| 声明与绑定 | [声明与绑定](declarations.md) |
| 字段选择、默认值、嵌套与剩余项 | [解构绑定](destructuring.md) |
| 类型 | [类型](types.md) |
| 类型参数、值参数与候选约束 | [泛型与约束](generics.md) |
| 位置、消费与移动后的状态 | [左值、右值与亡值](value-categories.md) |
| 值对象、共享对象与引用参数 | [赋值、复制与共享](assignment-semantics.md) |
| 直接交付、临时对象与必要的复制 | [复制消除](copy-elision.md) |
| 隐式、显式与条件转换 | [类型转换](conversions.md) |
| 表达式与运算符 | [表达式与运算符](expressions.md) |
| 分支、循环与控制转移 | [控制流](control-flow.md) |
| 函数、lambda 与闭包 | [函数](functions.md) |
| 候选适用性与歧义 | [重载解析](overload-resolution.md) |
| 类、对象与生命周期 | [类与生命周期](classes.md) |
| 复制、借用、闭包与资源清理 | [生命周期](lifetimes.md) |
| 为什么没出作用域就析构了 | [激进生命周期与析构时机](aggressive-lifetimes.md) |
| `console` 等默认可见名字的定义 | [默认环境](../../stdlib/api/environment.md) |
| 模块与导入 | [模块与导入](modules.md) |
| 文本替换、条件选择与 include | [文件预处理](preprocessing.md) |
| 异常、效果与并发 | [执行与并发](execution.md) |
| 宏与元编程 | [宏与元编程](metaprogramming.md) |
| 原生声明、调用约定与回调 | [外部接口与 ABI](foreign.md) |

入门教程见[语言教程](../../language/index.md)。语言合同以[语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)及各页所列专题规范为准。
