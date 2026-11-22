# 分批读实验数据并显示为表格

> 打开一份记录了数百万次采样的 CSV，用同一份程序先检查前三条，再逐页查看结果。

!!! abstract "🎯 做完这页，你能"
    - 按记录读取 CSV，保留引号里的逗号和换行
    - 校验列名和记录宽度，输出分批对齐的终端表格
    - 为预览、汇总和随机跳页选择各自的读取方式

    <span class="el-chip">⏱ 约 25 分钟</span> <span class="el-chip">前置：[Excel 分类导出 CSV](workbook-to-csv.md)</span>

!!! note "实现状态"
    示例使用当前 EL 源码中的 CSV 流式读取器，尚未编译或运行。安装包里的标准库须包含 `openCSVRows`。

## 先检查三条记录

在同一目录创建 UTF-8 文件 `experiment.csv`。每行是一次采样，时间用秒，温度用摄氏度。

```csv
sample,time_s,temperature_c
a-001,0,20.5
a-002,1,20.7
"b,003",2,21.1
```

把完整程序保存为 `preview.el`，运行 `el run preview.el`。

```el
import { openCSVRows } from "el:formats/delimited-text/"

let source = openCSVRows("experiment.csv")
try {
	let header = source.readBatch(1)
	if (header.rows.count != 1) throw "缺少列名"
	let columns = header.rows[0]
	if (columns.count != 3) throw "需要三列"
	if (columns[0] != "sample" | columns[1] != "time_s" | columns[2] != "temperature_c") throw "列名或单位不匹配"

	console.stdout.writeLine("样本\t时间(s)\t温度(°C)")
	let seen = 0
	while (t) {
		let batch = source.readBatch(2)
		for (let row in batch.rows) {
			seen++
			if (row.count != 3) throw "采样记录应有三列：" + Text(seen)
			console.stdout.writeLine(row[0], "\t", row[1], "\t", row[2])
		}
		if (batch.end) break
	}
	console.stdout.writeLine("记录数：", seen)
} finally {
	source.close()
}
```

预期表格第三条记录的样本名是 `b,003`，温度是 `21.1`，末行显示 `记录数：3`。上例输出使用制表符，终端列宽取决于字段长度和终端设置。

??? question "先猜：一条记录的备注里有换行，能先按行切文件吗？"
    引号中的换行仍属于同一条记录。让 CSV 读取器识别记录边界，再逐列检查或转换数值。

## 换成大文件时控制读取量

- **快速预览。** 读一批，例如 100 条，渲染成界面上的表格，点“下一页”时继续读取。对自由文本列，把嵌入的换行转成可见标记，避免一条记录占用多行。
- **按实验组汇总。** 一批一批做单位校验和数值转换，每组只累加计数、和、最小值与最大值。若分组数随数据持续增长，把明细导入数据库并按页查询。
- **筛选与随机跳页。** 顺序 CSV 每次从上次的记录边界继续。需要任意排序或跳到远处时，把已校验记录分批入库，按唯一采样编号建立索引并维护稳定排序。
- **估算内存。** 批大小只限制条数。单条测量记录若含很大的文本或附件，仍可能消耗大量内存。展示层只保留当前页，输入错误要报告记录位置并停止或进入已约定的错误清单。

!!! example "动手检查边界"
    把 `b,003` 两边的引号删掉再运行。程序应报告第三条采样记录多出一列。恢复引号后，把批大小从 2 改成 1，三条数据及总数应相同。

## 下一站：[矩阵与数值脚本](numerics.md)

用校验后的两列数值做计算和绘图。
