# 用 EL 做七道竞赛题

> 题目要求输出圆周率的第 20 个小数位。把一个近似值打印得更长，能保证最后一位正确吗？

!!! abstract "🎯 做完这个项目，你能"
    - 用两个变量计算第 `n` 个斐波那契数
    - 用上下界确认圆周率的一位小数
    - 实现前缀和、广搜、并查集、贪心和有限值域文件排序

    <span class="el-chip">⏱ 约 25 分钟</span> <span class="el-chip">前置：[循环](../beginner/lists.md)、[函数](../beginner/functions.md)</span>

!!! note "实现状态"
    本页按现有精确数值和数学库源码编写，代码尚未用 EL 工具链运行。大文件示例采用有限值域计数排序，小样本和 4 GiB 输入均待 EL 运行验收。

## 第 1 题：只记住相邻两项

约定第 0 项为 0，第 1 项为 1。把程序存为 `fib.el`，运行 `el run fib.el`，预期输出 `55`。

```el
fn fibonacci(index: Number): Number {
	if (index < 0 | index % 1 != 0) throw "Expected a nonnegative integer"
	let current = 0
	let next = 1
	for (let step = 0; step < index; step++) {
		let afterNext = current + next
		current = next
		next = afterNext
	}
	return current
}

console.stdout.writeLine(fibonacci(10))
```

循环进入第 `step` 步时，`current` 是第 `step` 项，`next` 是它的后一项。结束时 `step` 已走到目标。程序做 `n` 次大整数加法，整数随项数增长。

!!! example "动手 30 秒"
    依次输入 0、1、2，检查三次输出是否为 0、1、1。再输入 100，预期是 `354224848179261915075`。

## 第 2 题：让两个界给出同一个数字

把程序存为 `pi-digit.el`，运行 `el run pi-digit.el`。小数点后从 1 数起，第 20 位预期输出 `6`。

```el
import { PiRefinement, floor } from "el:mathematics/index.el"

fn piDigit(position: Number): Number {
	if (position < 1 | position % 1 != 0) throw "Expected a positive position"
	let scale = 10 ^ position
	let tolerance = 1 / (10 * scale)
	let pi = PiRefinement()
	while (t) {
		let bounds = pi.bounds(tolerance)
		let lower = floor(bounds.low * scale)
		let upper = floor(bounds.high * scale)
		if (lower == upper) return lower % 10
		tolerance /= 10
	}
}

console.stdout.writeLine(piDigit(20))
```

`10 ^ position` 把目标位移到个位。两个界乘上相同的倍数后向下取整，只要整数部分相同，夹在中间的真实值也有同一个整数部分。最后取余数得到个位。每次收紧容差时，`PiRefinement` 可以复用已有的计算状态。

??? question "先猜：两个界算出的个位一样，能直接返回吗？"
    要先比较整个整数部分。比如两个界取整后分别为 13 和 23，个位都是 3，中间仍跨过了其他数字。

## 第 3 至 6 题：用四组小输入检查不变量

把这四题存成 `algorithms.el`，运行 `el run algorithms.el`，应依次得到 `4`、`1`、`连通`、`3`。

```el
// 第 3 题：prefix[i] 是前 i 项之和，区间使用左闭右开。
let values = @[2, 7, -3, 4]
let prefix: Number[] = @[0]
for (let value in values) prefix.push(prefix[prefix.count - 1] + value)
console.stdout.writeLine(prefix[3] - prefix[1])

// 第 4 题：节点 0、1、2 互相连通，3 是孤立点。
let neighbors: Number[][] = @[@[1, 2], @[0, 2], @[0, 1], @[]]
let distance: Number[] = @[0, -1, -1, -1]
let queue: Number[] = @[0]
for (let head = 0; head < queue.count; head++) {
	let node = queue[head]
	for (let next in neighbors[node]) {
		if (distance[next] >= 0) continue
		distance[next] = distance[node] + 1
		queue.push(next)
	}
}
console.stdout.writeLine(distance[2])

// 第 5 题：用根节点表示连通分量，把小树接到大树。
let parent: Number[] = @[0, 1, 2, 3]
let size: Number[] = @[1, 1, 1, 1]
fn rootOf(node: Number): Number {
	let current = node
	while (parent[current] != current) {
		parent[current] = parent[parent[current]]
		current = parent[current]
	}
	return current
}
fn join(first: Number, second: Number) {
	let left = rootOf(first)
	let right = rootOf(second)
	if (left == right) return
	if (size[left] < size[right]) {
		parent[left] = right
		size[right] += size[left]
	} else {
		parent[right] = left
		size[left] += size[right]
	}
}
join(0, 1)
join(1, 2)
console.stdout.writeLine(if (rootOf(0) == rootOf(2)) "连通" else "不连通")

// 第 6 题：每次选结束最早、起点不早于上一场终点的活动。
let activities = @[@{start: 0, end: 4}, @{start: 1, end: 2}, @{start: 2, end: 3}, @{start: 3, end: 5}]
let ordered = activities.sort((first, second) => first.end < second.end)
let lastEnd: Number | nil_t = nil
let accepted = 0
for (let activity in ordered) {
	if (lastEnd is Number & activity.start < lastEnd) continue
	lastEnd = activity.end
	accepted++
}
console.stdout.writeLine(accepted)
```

| 题目 | 不变量 | 再试一个输入 |
| --- | --- | --- |
| 3. 区间和 | 两个前缀和抵消查询起点之前的元素 | 查 `[2, 2)` 应为 0 |
| 4. 无权最短路 | 入队时就记录距离，每个节点入队一次 | 查节点 3 应为 -1 |
| 5. 连通性查询 | 有相同根的节点属于同一个分量 | 比较 0 与 3 应为“不连通” |
| 6. 最多能参加几场活动 | 选最早结束的一场，为后面的活动留下最多时间 | 只留一场活动，结果应为 1 |

## 第 7 题：给 4 GiB 的随机数排序

约定输入是小端无符号 32 位整数，范围为 0 到 65,535。4 GiB 对应 1,073,741,824 条记录。选计数排序，每个可能的值维护一个计数。文件以块读取，块尾不够四字节的数据留给下一块。输出时按计数从小到大重复写各个值。

把 `sort-file.el`、`input.bin` 放进一个空目录，执行 `el run sort-file.el`。示例使用同名练习输出文件，已有 `sorted.bin` 会被覆盖。

```el
import { openFileReader, openFileWriter } from "el:filesystem/"
import { append_u32le, read_u32le } from "el:cryptography/"

let counts: Number[] = @[]
for (let value = 0; value <= 65535; value++) counts.push(0)

let input = openFileReader("input.bin")
try {
	let pending: Number[] = @[]
	while (t) {
		let bytes = input.read(65536)
		if (bytes.count == 0) break
		for (let byte in bytes) {
			pending.push(byte)
			if (pending.count != 4) continue
			let value = read_u32le(pending, 0)
			if (value > 65535) throw "整数超出题目值域"
			counts[value]++
			pending = @[]
		}
	}
	if (pending.count != 0) throw "末尾记录不足四字节"
} finally {
	input.close()
}

let output = openFileWriter("sorted.bin")
try {
	let bytes: Number[] = @[]
	for (let value = 0; value <= 65535; value++) {
		for (let occurrence = 0; occurrence < counts[value]; occurrence++) {
			append_u32le(bytes, value)
			if (bytes.count == 65536) {
				discard(output.write(bytes))
				bytes = @[]
			}
		}
	}
	if (bytes.count != 0) discard(output.write(bytes))
	discard(output.flush())
} finally {
	output.close()
}
```

先用小样本验证。把下面的程序存成 `sample.el`，运行它生成输入：

```el
import { writeFileBytes } from "el:filesystem/"
import { append_u32le } from "el:cryptography/"

let bytes: Number[] = @[]
for (let value in @[7, 0, 65535, 7, 2]) append_u32le(bytes, value)
discard(writeFileBytes("input.bin", bytes))
```

排序后按相同编码读回，应是 `0, 2, 7, 7, 65535`，共 20 字节。把读取块大小从 65,536 改为 3，输出应一致。输入末尾追加一字节，程序应报告不完整记录。在 4 GiB 输入上执行前准备同等大小的输出空间，并用独立的流式检查确认长度、单调性和各值频次。这是教学实现，逐条数组操作的吞吐量需要实测。值域过大时改用分块排序与多路归并，每次归并只保留各输入块的当前头部。

## 下一站：[矩阵与数值脚本](numerics.md)

竞赛题通常给出固定输入和标准答案。换成实验数据，还需要检查数据的形状以及数值误差。
