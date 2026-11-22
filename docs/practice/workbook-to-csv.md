# 实战：把成绩表分类并导出 CSV

> 把一份 XLSX 成绩表分成“达标”和“需补充”，得到可以用表格软件打开的 CSV 文件。

!!! abstract "🎯 做完这个项目，你能"
    - 从 XLSX 工作表读取文本和数字单元格
    - 按分数分类，并把结果写入新的 CSV 文件
    - 核对边界分数和输出行数

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：变量、循环、条件与函数</span>

## 目标与边界

下载[教学成绩表 scores.xlsx](fixtures/scores.xlsx)，把它放进一个新建的工作目录。表里有一张名为“成绩”的工作表，第一行是表头，后面三行是数据：

| 姓名 | 分数 |
| --- | ---: |
| 小林 | 85 |
| 小周 | 59 |
| 小陈 | 60 |

程序把大于等于 60 分的记录标记为“达标”，其余标记为“需补充”，并写入同目录下的 `classified.csv`。原始 XLSX 不会被修改。再次运行会覆盖已有的 `classified.csv`，请不要把自己的数据放在这个输出文件里。

!!! note "实现状态"
    下方代码的接口和写法已按当前源码静态核对，尚未经过 EL 编译和运行验证。需要可运行且包含 `el:documents/`、`el:formats/delimited-text/` 与 `el:filesystem/` 的 EL 工具链；如果工具链尚未准备好，先看[工具准备](../getting-started.md)。

## 第一步：准备文件和完整程序

在工作目录里新建 `classify.el`，把下面整段代码复制进去。运行命令的当前目录也要是这个工作目录：相对路径 `scores.xlsx` 和 `classified.csv` 都从这里解析。

```el
import { readWorkbook, CellValue } from "el:documents/"
import { writeCSV } from "el:formats/delimited-text/"
import { writeTextFile } from "el:filesystem/"

fn textCell(value: CellValue): Text {
	return match value {
		CellValue.Text(text) => text
		_ => throw "姓名必须是文本"
	}
}

fn numberCell(value: CellValue): Number {
	return match value {
		CellValue.Numeric(number) => number
		_ => throw "分数必须是数字"
	}
}

let book = readWorkbook("scores.xlsx")
if (book.sheets.count == 0) throw "工作簿没有工作表"
let sheet = book.sheets[0]
if (sheet.name != "成绩") throw "第一张工作表必须叫成绩"

let rows: Text[][] = @[@["姓名", "分数", "分类"]]
for (let cell in sheet.cells) {
	if (cell.column == 1 & cell.row > 1) {
		let name = textCell(cell.value)
		let score = numberCell(sheet.get(cell.row, 2))
		let category = if (score >= 60) "达标" else "需补充"
		rows.push(@[name, Text(score), category])
	}
}

discard(writeTextFile("classified.csv", writeCSV(rows)))
console.stdout.writeLine("已写入 classified.csv，数据行数：", rows.count - 1)
```

在这个目录打开终端，运行：

```sh
el run classify.el
```

按代码预期，终端显示：

```text
已写入 classified.csv，数据行数：3
```

用文本编辑器或表格软件打开新文件，预期内容如下；换行的具体显示方式由编辑器决定：

```text
姓名,分数,分类
小林,85,达标
小周,59,需补充
小陈,60,达标
```

!!! success "检查点"
    - [ ] 输出有一行表头和三行数据，`59` 分被标为“需补充”
    - [ ] `60` 分被标为“达标”，原来的 `scores.xlsx` 仍然存在

## 第二步：看懂程序怎样找到每行

`readWorkbook` 打开 XLSX，`book.sheets[0]` 取第一张工作表。数组下标从零开始，工作表的行号和列号则从一开始：姓名在第 1 列，分数在第 2 列。

工作表只保存实际存在的单元格。循环找到第 1 列中表头之后的每个单元格，再用同一行的第 2 列取分数。这个规则适合本例：每条记录都有姓名，姓名所在列没有额外说明。若某行姓名为空，循环不会把那行当成记录；处理自己的表之前，先确认这个假设。

`textCell` 和 `numberCell` 检查单元格的值类型。分数缺失或是文本时，程序会报错，而不是悄悄把它当成零。`writeCSV` 负责给包含逗号、引号或换行的内容正确加引号；`writeTextFile` 把结果写成 UTF-8 文本。

??? question "先猜：60 分属于哪一类？"
    属于“达标”。条件 `score >= 60` 包含等于 60 的情况，59 则不满足条件。

!!! example "改一个分数"
    用表格软件把小周的 59 改为 60 并保存，再运行程序。打开 `classified.csv`，小周应变成“达标”；数据行数仍是 3。

## 第三步：核对真实数据的形状

这个程序要求第一张表叫“成绩”，姓名是文本，分数是数字。它不自动寻找表头，也不计算公式；公式单元格只有文件中保存的缓存值可供读取。把真实文件交给程序之前，先复制原文件、确认表的位置和列的含义，再用几行已知结果核对。

!!! warning "找不到输入文件或看到类型错误"
    **找不到文件。** 检查终端当前目录是否同时包含 `classify.el` 和 `scores.xlsx`，并核对扩展名。

    **提示姓名或分数类型不对。** 检查姓名列是否为文本、分数列是否为数字，以及姓名行对应的分数是否为空。

    **打开的 CSV 中文乱码。** 用表格软件的导入功能选择 UTF-8 编码，不要直接假设系统默认编码。

## 完整文件清单

```text
工作目录/
  scores.xlsx       下载的教学输入
  classify.el       上面的完整程序
  classified.csv    运行后生成
```

当前 `readWorkbook` 和 `writeCSV` 使用整表／整份文本接口；本程序还会在内存里保存输出行。大文件不能据此认为能以固定内存处理：请先用小数据验证，关注可用内存，并等待流式工作簿读取能力经过实际验收后再用于大规模数据。

## 改成你自己的

1. 把达标线改成 80：小林达标，小周和小陈需要补充。
2. 加一条姓名包含逗号的记录：确认导出的 CSV 用引号保留它为一个单元格。
3. 在输出中加入一列，例如“备注”：先为每条输入准备明确的值，再确认每行都有四列。

## 带走这三样

- 工作表坐标从 1 开始；根据姓名列找到记录后，可以用同一行号读取分数。
- 判断条件决定分类，边界值要单独检查。
- CSV 编码交给 `writeCSV`，原始 XLSX 与输出文件分开保存。

## 下一站：[分批读取实验数据](experiment-table.md)

对已经是 CSV 的大文件，改用按记录读取和逐批预览。
