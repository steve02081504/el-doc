# formats/text-format.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/formats.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 文本格式 {#api-4debf16b1bb002d0eda7}

源码：`src/stdlib/formats/text-format.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/text-format.el#L1)

提供文本格式的读取、编码与字符转换协议。

## TextFormat {#api-5d821ca4f8d541863abb}

源码：`src/stdlib/formats/text-format.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/text-format.el#L22)

创建文本格式对象，按需解码文本，并可选提供反向编码器。

```el-signature
export fn TextFormat(output: type, input: type = output): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

**参数**：output 解码后的值类型。

**参数**：input 可编码输入类型，默认与 output 相同。

**返回值**：支持 inputByteLimit、decode 与可选 encode 的格式对象类型。

### 示例：创建按原样读取的文本格式

```el
import { TextFormat } from "el:formats/"
import { JsonLimits } from "el:formats/json/"
let plainFormat = TextFormat<output: Text>((source: Text, limits: JsonLimits) => source)
```
