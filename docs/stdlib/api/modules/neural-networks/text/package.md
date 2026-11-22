# neural-networks/text/package.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/neural-networks.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 语言模型检查点 {#api-6918ee0061f44a3e53b4}

源码：`src/stdlib/neural-networks/text/package.el:15` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/package.el#L15)

提供结构化语言模型包的布局、流式写入与读取操作。

## LanguageModelPackage {#api-a8856762f284ccee6452}

源码：`src/stdlib/neural-networks/text/package.el:42` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/neural-networks/text/package.el#L42)

返回适用于因果语言模型的检查点操作类。包使用结构化 EL 数据格式保存配置、分词器、权重及适配器；它不序列化类实例，参数元素类型、存储和分块读取方式由调用方决定。

```el-signature
export fn LanguageModelPackage(element: type, storage: type = Tensor<element: element>): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

**参数**：element 权重元素类型。

**参数**：storage 权重存储类型，默认是相同元素类型的 `Tensor`。

**返回值**：提供检查点布局、读取和写入操作的包类型。

### 示例：选择 Number 权重的包实现

```el
import { LanguageModelPackage } from "el:neural-networks/index.el"
let Package = LanguageModelPackage<element: Number>
```
文件读写仍需调用返回类型提供的显式 I/O 回调；示例未执行 I/O。
