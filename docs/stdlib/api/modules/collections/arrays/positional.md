# collections/arrays/positional.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 逐位置类型数组 {#api-f348a771de91333cd731}

源码：`src/stdlib/collections/arrays/positional.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/positional.el#L1)

将封闭记录的字段次序作为固定位置存储；元素的声明类型不随数组视图擦除。

## positionalArray {#api-6bb9e0f6b72f22340b48}

源码：`src/stdlib/collections/arrays/positional.el:64` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/positional.el#L64)

创建固定长度、只读的数组；已知下标或下标范围的读取保留对应位置的类型联合。

```el
export syntax positionalArray
```

**参数**：values 按源码顺序各求值一次的元素表达式。

**返回值**：派生于 Array 的逐位置类型数组。

### 示例：创建逐位置类型数组

```el
import { positionalArray } from "el:collections/arrays/positional.el"
positionalArray(1, "two")
```
