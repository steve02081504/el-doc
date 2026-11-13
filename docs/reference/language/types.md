# 类型

| 查询 | 规则 |
| --- | --- |
| 局部注解 | `let` 注解是值版本的上界 |
| 联合 | `T | U` 表示类型联合 |
| 普通隐式转换 | 每条路径最多一层用户隐式转换 |
| 缺失 | `void` 与 `nil` 不同，条件中缺失按假处理 |

## 类型表达式

类型注解写作 `name: Type`。类型语法包括函数类型、泛型实参、联合类型、元组与类型查询。泛型实参通常必须写出形参名；仅当实参列表恰有一个参数且声明的首个形参是类型参数时，允许省略名称，例如 `Array<Point>`。

```el
let point: Point = origin
let maybeText: Text | void_t = void
```

这里仅展示注解写法。类型位置的 `|` 表示联合类型；表达式中的同一符号按表达式上下文解释。

## 推断、约束与数值

省略注解时，类型由初始化值和使用推断。局部 `let` 上的显式注解是上界，允许值版本在范围内细化或加宽；参数、字段和容器元素注解不采用这一流敏感规则。固定宽度或长度约束不能通过运行期加宽越过。

普通源码使用 `Number` 及其类型参数表达数值约束。机器整数表示属于显式底层边界，不替代语言层数值类型。

`any` 表示动态类型存储。`t_t`、`nil_t`、`void_t` 是标准环境提供的普通类型，不是编译器内建类。`nil` 与 `void` 是不同的值；缺失结果与假值不同，但条件中缺失按假值处理。

`Bool` 是 `t_t | nil_t` 的类型别名，布尔值本来就是这两种类型之一，不需要再转换成该联合。不要把值名字 `t`、`nil` 与类型名字混写成 `t | nil`。`Bool(value)` 是同名的条件求值函数，按输入返回 `t` 或 `nil`；相关例子见[条件转换](conversions.md#conditions)。

## 相关条目

- [左值、右值与亡值](value-categories.md)
- [赋值、复制与共享](assignment-semantics.md)
- [复制消除](copy-elision.md)

- [类型转换](conversions.md)
- [重载解析](overload-resolution.md)

- [声明与绑定](declarations.md)
- [表达式与运算符](expressions.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [核心语义](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [数值语义](https://github.com/steve02081504/el/blob/master/docs/spec/04-numbers.md)
