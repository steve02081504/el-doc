# formats/toml/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## TOML {#api-0c6ccd536b686ea05e79}

源码：`src/stdlib/formats/toml/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/toml/index.el#L1)

解析 TOML 文档并保留日期时间与表等类型信息。

## parseTOML {#api-3d751bf4576089574ccb}

源码：`src/stdlib/formats/toml/index.el:264` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/toml/index.el#L264)

```el
export fn parseTOML(source: Text, limits: JsonLimits = JsonLimits()): Toml
```

**返回类型**：`Toml`

解析 TOML 文档并保留 TOML 值种类，包括日期时间、数组和表。

**参数**：source 完整 TOML 文本。

**参数**：limits 输入与解析资源限制。

**返回值**：TOML 根表值。

**失败与异常**：TOML 语法无效或超出限制时抛出解析异常。

### 示例：解析 TOML 设置

```el
import { parseTOML } from "el:formats/toml/"
let settings = parseTOML("port = 8080")
```
