# 分批筛选并导出实验数据

> 从实验 CSV 筛出 B 组采样，只导出样本名和温度。输入文件变大时，程序仍逐批处理。

!!! abstract "🎯 做完这页，你能"
    - 按记录读取 CSV，保留引号里的逗号和换行
    - 用 `where` 筛选每批记录，用 `select` 选择要保留的列
    - 将结果逐批写入另一份 CSV

    <span class="el-chip">⏱ 约 25 分钟</span> <span class="el-chip">前置：[Excel 分类导出 CSV](workbook-to-csv.md)</span>

!!! note "实现状态"
    示例需要 `openCSVRows`、`openCSVWriter` 和支持数组来源的 `query`，尚未经过 EL 编译和运行验证。

## 先筛选三条记录

在同一目录创建 UTF-8 文件 `experiment.csv`。每行是一次采样，时间用秒，温度用摄氏度。

```csv
sample,time_s,temperature_c
a-001,0,20.5
a-002,1,20.7
"b,003",2,21.1
```

把完整程序保存为 `filter.el`，运行 `el run filter.el`。程序会创建或覆盖同目录的 `selected.csv`。

```el
import { openCSVRows, openCSVWriter } from "el:formats/delimited-text/"
import { query } from "el:queries/"

fn validateSample(row: Text[]): Text[] {
	if (row.count != 3) throw "采样记录应有三列"
	return row
}

let source = openCSVRows("experiment.csv")
try {
	let header = source.readBatch(1)
	if (header.rows.count != 1) throw "缺少列名"
	let columns = header.rows[0]
	if (columns.count != 3 | columns[0] != "sample" | columns[1] != "time_s" | columns[2] != "temperature_c") throw "列名或单位不匹配"

	let destination = openCSVWriter("selected.csv")
	try {
		destination.writeBatch(@[@["sample", "temperature_c"]])
		while (t) {
			let batch = source.readBatch(2)
			let selected = query {
				from row in $(batch.rows)
				let sample = $(validateSample)(row)
				where sample[0].startsWith("b")
				select @[sample[0], sample[2]]
			}()
			destination.writeBatch(selected)
			if (batch.end) break
		}
	} finally {
		destination.close()
	}
} finally {
	source.close()
}
```

打开 `selected.csv`，预期内容如下。样本名包含逗号，所以写入器会为它加上引号。

```csv
sample,temperature_c
"b,003",21.1
```

??? question "先猜：一条记录的备注里有换行，能先按行切文件吗？"
    引号中的换行仍属于同一条记录。让 CSV 读取器识别记录边界，再逐列检查或转换数值。

## 循环只负责推进批次

`readBatch(2)` 每次交付至多两条完整记录。`query` 检查字段数，筛出样本名以 `b` 开头的记录，再取样本名和温度。写出本批后，循环才能读取下一批；没有匹配记录的批次不会写出数据行。

批大小限制的是记录条数。含长字段的一条记录仍可能占用大量内存。输入格式错误或写入失败时，输出文件可能已包含表头和部分数据。

`order by`、`group by` 或 `limit` 写在这个查询里会分别作用于每批。要对整个文件排序，可以先把记录导入数据库再排序。要限制整个文件的输出条数，可以在每次写出后更新剩余条数。

!!! example "动手检查边界"
    把 `b,003` 两边的引号删掉再运行。程序应报告列数错误。恢复引号后，把批大小从 2 改成 1，输出应相同。

## 下一站：[矩阵与数值脚本](numerics.md)

用校验后的两列数值做计算和绘图。
