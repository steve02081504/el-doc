# 实战：把成绩表分类并导出 CSV

> 把一份 XLSX 成绩表分成“达标”和“需补充”，得到可以用表格软件打开的 CSV 文件。

!!! abstract "🎯 做完这个项目，你能"
    - 从 XLSX 工作表读取文本和数字单元格
    - 用 `query` 按分数分类，并把结果写入新的 CSV 文件
    - 核对边界分数和输出行数

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：数组、条件与函数</span>

## 目标与边界

下载[教学成绩表 scores.xlsx](fixtures/scores.xlsx)，把它放进一个新建的工作目录。表里有一张名为“成绩”的工作表，第一行是表头，后面三行是数据：

| 姓名 | 分数 |
| --- | ---: |
| 小林 | 85 |
| 小周 | 59 |
| 小陈 | 60 |

程序把大于等于 60 分的记录标记为“达标”，其余标记为“需补充”，并写入同目录下的 `classified.csv`。原始 XLSX 不会被修改。再次运行会覆盖已有的 `classified.csv`，请不要把自己的数据放在这个输出文件里。

!!! note "实现状态"
    示例需要支持数组来源的 `el:queries/` 以及工作簿和 CSV 标准库。示例尚未经过 EL 编译和运行验证。工具链的获取方式见[工具准备](../getting-started.md)。

## 第一步：准备文件和完整程序

在工作目录里新建 `classify.el`，把下面整段代码复制进去。运行命令的当前目录也要是这个工作目录：相对路径 `scores.xlsx` 和 `classified.csv` 都从这里解析。

```el
import { readWorkbook, CellValue, Worksheet } from "el:documents/"
import { writeCSV } from "el:formats/delimited-text/"
import { writeTextFile } from "el:filesystem/"
import { query } from "el:queries/"

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

let classify = query(input: Worksheet) {
	from cell in input.cells
	where cell.column == 1 & cell.row > 1
	let name = $(textCell)(cell.value)
	let score = $(numberCell)(input.get(cell.row, 2))
	let category = if (score >= 60) "达标" else "需补充"
	select @[name, Text(score), category]
}

let classified = classify.bind(@{ input: sheet })()
let rows: Text[][] = @[@["姓名", "分数", "分类"], ...classified]
discard(writeTextFile("classified.csv", writeCSV(rows)))
console.stdout.writeLine("已写入 classified.csv，数据行数：", classified.count)
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

`from` 指定要查的单元格，`where` 只保留姓名列中位于表头之下的单元格。两条 `let` 分别取姓名和同一行的分数，`select` 生成一条 CSV 记录。工作表缺少姓名单元格的行会被略过。

`query(input: Worksheet)` 定义一个可传入工作表的查询。调用 `.bind(@{ input: sheet })` 填入本次的工作表，末尾的 `()` 收集结果。`$(textCell)` 和 `$(numberCell)` 引用查询外定义的函数。分数缺失或类型错误时，`numberCell` 会报错。

`writeCSV` 给包含逗号、引号或换行的字段加引号，`writeTextFile` 把结果写成 UTF-8。

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

## 直接在 CSV 中查找需补充的学生

生成 `classified.csv` 后，把下面的完整程序保存为 `follow-up.el`，运行 `el run follow-up.el`。CSV 的每个字段都是文本，第一条记录也是普通数据。本例生成的表头第三列是“分类”，因此检查第三列是否等于“需补充”即可。

```el
import { readTextFile } from "el:filesystem/"
import { parseCSV } from "el:formats/delimited-text/"
import { query } from "el:queries/"

let names = query {
	from row in $(parseCSV(readTextFile("classified.csv")))
	where row[2] == "需补充"
	select row[0]
}()

console.stdout.writeLine(names.join("、"))
```

```text
小周
```

## 完整文件清单

```text
工作目录/
  scores.xlsx       下载的教学输入
  classify.el       上面的完整程序
  classified.csv    运行后生成
```

这两个程序会在内存中保存输入和查询结果。处理大 CSV 时，可以按批读取、查询和写出，见下一篇。

## 改成你自己的

1. 把达标线改成 80：小林达标，小周和小陈需要补充。
2. 加一条姓名包含逗号的记录：确认导出的 CSV 用引号保留它为一个单元格。
3. 在输出中加入一列，例如“备注”：先为每条输入准备明确的值，再确认每行都有四列。

## 带走这三样

- 工作表坐标从 1 开始；根据姓名列找到记录后，可以用同一行号读取分数。
- 判断条件决定分类，边界值要单独检查。
- CSV 编码交给 `writeCSV`，原始 XLSX 与输出文件分开保存。

## 下一站：[分批筛选并导出实验数据](experiment-table.md)

让同一个查询依次处理每批 CSV 记录。
