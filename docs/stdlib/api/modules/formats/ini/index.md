# formats/ini/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## INI {#api-5b373451fbea9ce8c4c7}

源码：`src/stdlib/formats/ini/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/ini/index.el#L1)

解析本模块定义的轻量 INI 方言。

## parseINI {#api-e4172fc09fb95d53c347}

源码：`src/stdlib/formats/ini/index.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/ini/index.el#L27)

解析此模块支持的 INI 方言，生成嵌套动态对象，键和值均保持文本。

```el
export fn parseINI(source: Text, limits: JsonLimits = JsonLimits()): any
```

**返回类型**：[`any`](../../../../../reference/language/types.md)

**参数**：source 完整 INI 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：根对象；节名映射到节对象，键映射到文本值。

**失败与异常**：语法无效、标量与节冲突或超出限制时抛出解析异常。

### 示例：读取 INI 节

```el
import { parseINI } from "el:formats/ini/"
let settings = parseINI("[server]\nport=8080")
```
