# 解构绑定

解构从对象字段或数组位置建立一组新绑定。本页描述语言合同；代码已按规范与对应源码静态核对，未编译或执行。代码后的输出是按合同推导的预期结果。

| 查询 | 规则 |
| --- | --- |
| 对象取值 | `{ name: localName }` 按字段名选择，冒号后是新绑定 |
| 数组取值 | `[first, , third]` 按位置选择，空项跳过一个位置 |
| 默认值 | 只在项缺失或值为 `void` 时求值，`nil` 不触发 |
| 初始化顺序 | 来源只求值一次，绑定从左到右建立 |
| 剩余项 | `...rest` 必须最后，不能带默认值 |
| 值的关系 | 新绑定遵循字段或元素类型的复制／共享协议，不是来源槽的别名 |

## 字段名、绑定名与嵌套模式

下面是完整的采购记录示例。单价以元计，数量以件计；只取计算总价需要的字段。

```el
let order = @{ product: "铅笔", pricing: @{ unitPrice: 2, quantity: 3 } }
let { product: productName, pricing: { unitPrice, quantity } } = order
console.stdout.writeLine(productName)
console.stdout.writeLine(unitPrice * quantity)
```

预期 stdout：

```text
铅笔
6
```

`product: productName` 从来源的 `product` 字段建立 `productName`；不会额外声明名为 `product` 的局部变量。`unitPrice` 是同名简写，相当于 `unitPrice: unitPrice`。嵌套模式继续从选中的字段取值；本例不建立局部 `pricing`。

数组模式按位置选择，连续逗号可以跳项。以下是独立示例：

```el
let [monday, , wednesday] = @[12, 18, 15]
console.stdout.writeLine(monday + wednesday)
```

预期输出 `27`。数组字面量有 `@` 前缀，绑定模式没有；这里的方括号声明绑定，不是在创建数组或读取一个下标。

## 默认表达式按需执行，可以引用前序绑定

下例完整展示存在值、缺失项、`void` 和 `nil` 的区别：

```el
let settings = @{ minimum: 3, preferred: void, enabled: nil }
let { minimum = 1, preferred = minimum + 1, maximum = preferred + 1, enabled = t } = settings
console.stdout.writeLine(minimum)
console.stdout.writeLine(preferred)
console.stdout.writeLine(maximum)
console.stdout.writeLine(if (enabled) "开启" else "关闭")
```

预期 stdout：

```text
3
4
5
关闭
```

`minimum` 已有值，因此不执行默认表达式；`preferred` 是 `void`，使用前序绑定算出 `4`；缺失的 `maximum` 算出 `5`。`enabled` 的 `nil` 被保留。默认表达式只有在需要时才执行，其副作用和异常也只在那时发生。

没有默认值的必需项若缺失，静态可判定时编译拒绝，运行期才发现时抛异常。默认值不会吞掉读取过程中的任意异常；字段读取或默认表达式失败仍按普通异常规则传播，已发生的副作用不会回滚，已建立的值仍按正常规则清理。

## 剩余项建立新容器，元素仍按自身协议处理

数组剩余项是结构独立的新变长数组，保留未选位置的顺序；即使来源是固定长度数组，剩余项也可变长。以下是完整示例：

```el
let quantities: Number[] = @[1, 2, 3, 4]
let [first, , ...remaining] = quantities
remaining.push(5)
console.stdout.writeLine(first)
console.stdout.writeLine(remaining.count)
console.stdout.writeLine(quantities.count)
```

预期 stdout：

```text
1
3
4
```

跳过第二个位置后，`remaining` 初始为 `@[3, 4]`。追加元素只改变新数组的结构。若元素本身是共享对象，新旧数组仍可能持有同一对象；结构独立不代表深复制。

对象剩余项是新的 `shared` 动态对象，收集来源自身未选中的公开数据字段，包括公开声明字段与动态数据字段；不收集方法、私有字段或继承字段。已按来源字段名选中的项会被排除，即使它在模式中被重命名。每个字段值仍按自身类型复制或共享。

## 解构不会建立可写回来源的引用

给解构出的普通绑定重新赋值，只改变新绑定，不会把新值写回原字段。解构也不要求先复制整个来源对象再逐项读取。需要修改来源槽时，应使用正常成员赋值或明确的引用参数合同，见[赋值、复制与共享](assignment-semantics.md)。

`const` 解构使各个新绑定遵循 `const` 规则，不把共享对象深度冻结。重复绑定名是错误，即使重复出现在不同嵌套层中；剩余项后不能再接其他项，也不能写 `...rest = fallback`。

## 范围循环逐项建立绑定

范围循环复用同一套模式规则。下例是完整程序，每轮从一组宽、高取值，累计矩形面积：

```el
let totalArea = 0
for (let [width, height] in @[@[2, 3], @[4, 5]]) {
	totalArea += width * height
}
console.stdout.writeLine(totalArea)
```

预期输出 `26`。模式在取得每个元素后建立本轮绑定；解构失败仍须遵守循环退出时的游标关闭与异常清理合同，见[控制流](control-flow.md)和[异常、效果与并发](execution.md)。

## 相关条目与核对依据

- [声明与绑定](declarations.md)
- [左值、右值与亡值](value-categories.md)
- [赋值、复制与共享](assignment-semantics.md)
- [语法标准中的解构规则](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#128-模式is-判断的目标)
- [范围循环与迭代器合同](https://github.com/steve02081504/el/blob/master/docs/spec/17-range-loops-and-iterators.md)
- [解构默认值与剩余项回归源码](https://github.com/steve02081504/el/blob/master/tests/binding-patterns/defaults-rest.el)
- [解构绑定展开实现](https://github.com/steve02081504/el/blob/master/src/stdlib/compiler/bindings/binding-patterns.el)
