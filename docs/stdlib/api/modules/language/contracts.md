# language/contracts.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/language.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 语言合同属性 {#api-3d44080cdfa13dcb6627}

源码：`src/stdlib/language/contracts.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/contracts.el#L1)

语言合同属性相关接口。

## assign {#api-7df99f92d8ed036a4e2a}

源码：`src/stdlib/language/contracts.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/contracts.el#L16)

声明类型的赋值与所有权模式；这是编译器识别的属性声明，不是运行期函数。

```el-signature
export @builtin:khaz:attribute:assign fn assign()
```

### 示例：用法

```el
import { assign } from "el:language/contracts.el"
@assign(mode: "copy")
class Point { let x: Number = 0 }
```

## sync {#api-dedb92c7de9674b67da2}

源码：`src/stdlib/language/contracts.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/contracts.el#L30)

声明可调用值的同步合同；这是编译器识别的属性声明。

```el-signature
export @builtin:khaz:attribute:sync fn sync()
```

### 示例：用法

```el
import { sync } from "el:language/contracts.el"
@sync fn identity(value: Number): Number { return value }
```
