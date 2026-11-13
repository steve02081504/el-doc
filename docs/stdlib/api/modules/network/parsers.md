# network/parsers.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/network.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 网络输入解析 {#api-418b4e53907f69a01725}

源码：`src/stdlib/network/parsers.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/parsers.el#L1)

提供网络表单与 URL 相关文本解析辅助接口。

## parseForm {#api-1f7812157bf2991a8b30}

源码：`src/stdlib/network/parsers.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/parsers.el#L56)

```el
export fn parseForm(source: Text): FormField[]
```

**返回类型**：`FormField[]`

解析 application/x-www-form-urlencoded 格式的字段序列。

**参数**：source 表单编码文本。

**返回值**：保留输入顺序的 FormField 数组。

**失败与异常**：百分号转义无效或文本解码失败时抛出解析异常。

### 示例：解析重复表单键

```el
import { parseForm } from "el:network/parsers.el"
let fields = parseForm("tag=el&tag=language")
```
