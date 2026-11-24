# formats/delimited-text/stream.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/formats.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 流式 CSV 读取 {#api-0620f11e3929da4a8f1f}

源码：`src/stdlib/formats/delimited-text/stream.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/stream.el#L1)

流式 CSV 读取相关接口。

## openCSVRows {#api-6f7101cca85917c43295}

源码：`src/stdlib/formats/delimited-text/stream.el:146` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/formats/delimited-text/stream.el#L146)

打开 CSV 文件并返回分批读取行的读取器。

```el-signature
export fn openCSVRows(path: Text): CsvRowReader
```

**返回类型**：[`CsvRowReader`](../../../types.md#api-d1a32b0db6f02835cc7e)

**注意**：读取器拥有文件，使用后应关闭；解析和读取错误会传播。

### 示例：使用示例

```el
import { openCSVRows } from "el:formats/delimited-text/"
let reader = openCSVRows("input.csv")
try {
	let batch = reader.readBatch(100)
} finally { reader.close() }
```
