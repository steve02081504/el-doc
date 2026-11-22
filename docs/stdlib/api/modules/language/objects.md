# language/objects.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 对象字段操作 {#api-4e15335b9f2ff6675736}

源码：`src/stdlib/language/objects.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/objects.el#L1)

提供自身字段枚举、读写、赋值及动态对象快照。

## ownKeyCount {#api-7f663edadbdc0b343c1b}

源码：`src/stdlib/language/objects.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/objects.el#L20)

返回自身字段数量，不先创建键数组，供有界枚举预留工作空间。

```el-signature
export fn ownKeyCount(value): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

### 示例：查询对象字段数

```el
import { ownKeyCount } from "el:language/objects.el"
console.stdout.writeLine(ownKeyCount(@{ name: "EL", version: "1" }))
```

## DynamicObject {#api-e3d29af11f62e4970b53}

源码：`src/stdlib/language/objects.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/objects.el#L69)

可在运行时添加动态字段的开放存储对象。

```el-signature
@assign(mode: "shared") @dynamic
export class DynamicObject
```

### 示例：创建对象

```el
let object = DynamicObject()
```
