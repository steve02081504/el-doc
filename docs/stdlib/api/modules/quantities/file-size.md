# quantities/file-size.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/quantities.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标原生文件容量 {#api-6bf15639c9489ca03563}

源码：`src/stdlib/quantities/file-size.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/quantities/file-size.el#L1)

文件容量以目标原生数位表示，可在原生 I/O 边界换算为完整地址单元。

## FileSize {#api-0b1508ed7adb8c7aa82f}

源码：`src/stdlib/quantities/file-size.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/quantities/file-size.el#L35)

保存非负的精确整数目标数位数。dit、kd、md、gd、td、pd、ed 逐级按目标基数的十次方换算。
复合输入按单位降序排列，只有最后一项允许小数，结果必须为整数数位。
构造器接收数位数。fromAddressUnits 和 totalAddressUnits 用于原生 I/O，要求完整的地址单元。

```el-signature
@assign(mode: "copy")
@quantityDimension(numerator: @[DigitStorageDimension])
@quantityLiteral(suffixes: @["dit", "kd", "md", "gd", "td", "pd", "ed"])
export class FileSize extends TextOperand
```

### 示例：使用示例

```el
let capacity = FileSize.parse("2md512kd")
let digits = capacity.totalDits
let display = Text(capacity)
let position = FileSize.fromAddressUnits(4)
let index = position.totalAddressUnits
```
