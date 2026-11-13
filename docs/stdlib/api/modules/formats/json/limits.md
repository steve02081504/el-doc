# formats/json/limits.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## JSON 解码限制 {#api-66f30aa8740c6156fc1a}

源码：`src/stdlib/formats/json/limits.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/limits.el#L1)

定义完整 JSON 输入解析的字节、步骤与递归资源限制。

## JsonLimits {#api-0b8ce6a01434f6c89e99}

源码：`src/stdlib/formats/json/limits.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/json/limits.el#L17)

```el
export class JsonLimits
```

配置 JSON 文本的最大字节数、解析限制和重复键策略。

### 示例：设置输入字节上限

```el
import { JsonLimits } from "el:formats/json/"
let limits = JsonLimits(@{ bytes: 1048576 })
```
