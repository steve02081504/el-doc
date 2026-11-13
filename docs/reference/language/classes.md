# 类、对象与生命周期

## 类声明

```el
import { assign } from "el:language/contracts.el"

@assign(mode: "copy")
class Point {
	let x = 0
	constructor(x: Number) { this.x = x }
}
```

用户类型必须明确选择 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，没有默认赋值模式。此例从 `el:language/contracts.el` 导入 `assign` 属性绑定。类可声明字段、方法、构造器、析构器和运算符。继承用 `extends`，接口使用结构匹配；`implements` 可声明完整契约断言。普通字段在构造时确定类型，动态类则通过 `@dynamic` 采用专门的动态字段操作。

## 构造与分派

具名类通过调用类名构造实例。构造器默认只参与显式构造；`implicit constructor` 可成为符合规则的隐式目标转换候选。虚方法显式标记 `virtual`，覆盖必须写 `override`。运算符重载可在类内或满足关联规则的类外声明。

## 析构与清理

类声明可用 `@destruct(mode: "scope")` 或 `@destruct(mode: "aggressive")` 选择析构策略；未标注时为 aggressive。实际具体类自己的设置决定策略。析构失败、异步清理及构造失败时的部分对象清理由生命周期合同规定；控制转移也必须履行清理义务。

赋值模式属性是必需的。经 const 访问路径的写入受限，但不会冻结所有别名。构造失败后的部分初始化清理有独立规则。

## 相关条目

- [类型](types.md)
- [声明与绑定](declarations.md)
- [对象与类型规范](https://github.com/steve02081504/el/blob/master/docs/spec/05-objects-and-types.md)
- [函数与生命周期规范](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
