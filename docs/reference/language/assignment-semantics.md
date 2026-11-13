# 赋值、复制与共享

赋值后改一个对象，会不会影响另一个名字看到的内容？先看类型的赋值策略，再看这次传递有没有移动或借用。

| 策略或方式 | 普通值传递得到什么 | 改动的影响 |
| --- | --- | --- |
| `copy` 类型 | 独立的值对象；复制深度由复制协议决定 | 独立对象的自身修改互不替代；其中共享的成员仍可能指向同一对象 |
| `shared` 类型 | 指向同一对象的共享引用 | 经一个引用修改对象，其他引用可观察到；重绑一个名字不会重绑其他名字 |
| `ref` 参数 | 调用者槽位的借用 | 给参数赋值会写回调用者槽位 |
| `take` 参数 | 按接管协议转移来源 | 提交后原来源为亡值，接收方负责取得的值 |

## 类型策略和参数模式是两层规则

具名用户类声明时必须选 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`。普通值参数和返回值遵循这个类型策略：前者按值复制，后者传递共享引用；符合条件的最后使用可以移动。`Number`、`Bool` 和 `Text` 采用 copy 值语义，数组和对象字面量采用 shared。不可变内部存储可以共享，不改变 copy 的值语义。

下面的类声明是语义示例；字段和构造写法见[类](classes.md)：

```el
@assign(mode: "copy")
class Point {
	let x = 0
}

@assign(mode: "shared")
class Settings {
	let volume = 0
}
```

普通传递 `Point` 时，必要的复制产生独立对象；普通传递 `Settings` 时，得到同一对象的另一个共享引用。默认复制逐字段遵守各字段自己的复制或共享协议，所以 copy 并不自动意味着递归深复制。实际可省略的中间复制见[复制消除](copy-elision.md)。

默认环境已经提供 `assign`，上例可以直接使用该属性，不需要每次定义类都写一条导入。

## 借用槽位和共享对象不同

```el
fn reset(ref count: Number) {
	count = 0
}
let count = 3
reset(count)
```

这个语义片段中，`reset` 借用 `count` 所在的可写槽位，赋值写回该槽位。普通值参数则拥有局部绑定，重绑参数不改调用者的绑定。即使值是 shared，普通参数共享的也是对象，不是调用者保存引用的槽位。

`rvalue` 参数限制调用处的值类别，`take` 表达接管；它们都不能仅从类的 copy／shared 策略推断。返回的借用也不会自动延长来源寿命，使用时来源必须仍有效。参见[左值、右值与亡值](value-categories.md)和[生命周期](lifetimes.md)。

## 常见误解

- “copy 一定深复制”：字段可有自己的共享语义，用户复制构造也决定具体复制方式。
- “shared 等于 `ref`”：共享的是对象；`ref` 借用的是可写槽位，允许重绑调用者的位置。
- “shared 自动线程安全”：共享引用不提供并发写入同步。
- “复制类型一定很慢”：临时复制可被消除，最后使用也可能移动；性能仍须测量。

相关内容：[类型](types.md)、[类型转换](conversions.md)、[函数](functions.md)和[重载解析](overload-resolution.md)。

??? note "核对依据"
    [对象与类型规范：赋值策略与复制构造](https://github.com/steve02081504/el/blob/master/docs/spec/05-objects-and-types.md)

    [函数与生命周期规范：参数、借用和移动](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)
