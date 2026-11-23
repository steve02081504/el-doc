# documents/workbook.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/documents.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 电子表格工作簿 {#api-41dc4debb27c3a58ee10}

源码：`src/stdlib/documents/workbook.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/workbook.el#L1)

电子表格工作簿相关接口。

## CellValue {#api-57d8ceae315b6bd851bf}

源码：`src/stdlib/documents/workbook.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/workbook.el#L23)

单元格值的变体，包括空值、文本、数值、布尔值、日期时间文本和错误文本。

```el-signature
export data CellValue
```

### 示例：使用示例

```el
import { CellValue } from "el:documents/"
let value = CellValue.Numeric(42)
```

## Worksheet {#api-b2648c721d49c3944436}

源码：`src/stdlib/documents/workbook.el:51` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/workbook.el#L51)

按一基行列坐标保存稀疏单元格；缺失单元格读取为空值。

```el-signature
export @assign(mode: "shared") class Worksheet
```

### 示例：使用示例

```el
import { Worksheet, CellValue } from "el:documents/"
let sheet = Worksheet("Data")
sheet.set(1, 1, CellValue.Text("Name"))
let value = sheet.get(1, 1)
```

## readWorkbook {#api-f1dc94bd466a32e95591}

源码：`src/stdlib/documents/workbook.el:270` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/documents/workbook.el#L270)

读取 XLSX 或 ODS 文件并解析为工作簿。

```el-signature
export fn readWorkbook(path: Text): Workbook
```

**返回类型**：[`Workbook`](../../types.md#api-1c744dd545a81af88249)

**失败与异常**：文件读取、包格式或不支持的表格内容出错时传播错误。

### 示例：使用示例

```el
import { readWorkbook } from "el:documents/"
let workbook = readWorkbook("report.xlsx")
```
