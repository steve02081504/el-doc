# 完成文具采购小助手

> 输入一份采购计划，让程序列出每项总价，再告诉你预算够不够。

!!! abstract "🎯 做完这个项目，你能"
    - 把函数、数组、循环和判断组合起来
    - 逐步核对小计、合计和预算提醒
    - 修改清单，做一份自己的采购计划

    <span class="el-chip">可以分三次完成</span> <span class="el-chip">前置：[采购总价函数](functions.md)</span>

## 先写验收答案

计划买 3 本 4 元的本子、5 支 2 元的铅笔，预算 30 元。程序应依次显示：

```text
第 1 项：12 元
第 2 项：10 元
合计：22 元
预算够，还剩 8 元
```

这里的“输入”是修改代码中的数据，还不用学习键盘输入。清单里的每项是**一类文具的小计**，不是一件文具的单价。程序也不处理付款和保存账单。

## 第一步：沿用已经会写的总价规则

新建 `shopping.el`，先只保存下面这段。不要急着加循环。

```el
fn purchaseCost(price: Number, quantity: Number): Number {
	return price * quantity
}

let costs = @[purchaseCost(4, 3), purchaseCost(2, 5)]
console.stdout.writeLine(costs[0])
console.stdout.writeLine(costs[1])
```

运行 `el run shopping.el`，应依次输出 `12` 和 `10`，各占一行。

这里新出现的 `costs[0]` 表示取清单第一项，`costs[1]` 表示第二项。这个位置号码叫作**下标**，EL 数组从 `0` 开始编号。先确认两项金额算对，再做合计。

## 第二步：换成循环，保留计算过程

保留函数和 `let costs = ...`，删除两行临时输出，换成下面这段：

```el
let total = 0
let itemNumber = 1

for (let cost in costs) {
	console.stdout.writeLine("第 ", itemNumber, " 项：", cost, " 元")
	total = total + cost
	itemNumber = itemNumber + 1
}

console.stdout.writeLine("合计：", total, " 元")
```

运行后应看到目标输出的前三行。`itemNumber` 是给人看的项目编号，从 1 开始；它没有用作数组下标。每轮显示后加 1，下一项就有新的编号。

## 第三步：自己接上预算提醒

在循环前定义预算 `budget` 为 `30`。在合计输出后增加判断：预算大于或等于合计时，显示余额；否则显示还差多少钱。需要帮助时，回看[钱够不够买](decisions.md)。

??? success "完整源码：尝试之后再核对"
    ```el
    fn purchaseCost(price: Number, quantity: Number): Number {
    	return price * quantity
    }

    let budget = 30
    let costs = @[purchaseCost(4, 3), purchaseCost(2, 5)]
    let total = 0
    let itemNumber = 1

    for (let cost in costs) {
    	console.stdout.writeLine("第 ", itemNumber, " 项：", cost, " 元")
    	total = total + cost
    	itemNumber = itemNumber + 1
    }

    console.stdout.writeLine("合计：", total, " 元")
    if (budget >= total) {
    	console.stdout.writeLine("预算够，还剩 ", budget - total, " 元")
    } else {
    	console.stdout.writeLine("还差 ", total - budget, " 元")
    }
    ```

## 用不同数据检查，而不是只看一次成功

每次只改表中指定的部分，保存后重新运行。先写下预计结果，再与实际输出对照。

| 改动 | 应有合计 | 最后一行 |
| --- | --- | --- |
| 原始清单，预算 30 | 22 元 | 预算够，还剩 8 元 |
| 只把预算改为 22 | 22 元 | 预算够，还剩 0 元 |
| 只把预算改为 20 | 22 元 | 还差 2 元 |
| 恢复预算 30，增加 `purchaseCost(3, 2)` | 28 元 | 预算够，还剩 2 元 |

增加项目时，在数组末尾加英文逗号和新的函数调用，放在 `]` 前面。循环不需要增加一份。

## 不对时，先看哪一步开始不同

| 现象 | 先检查 |
| --- | --- |
| 第一项不是 12 元 | 函数是否返回单价乘数量，调用是否为 `(4, 3)` |
| 每项对，合计错 | `total` 是否在循环外初始化、在循环内累加 |
| 合计对，提醒错 | 比较是否用 `>=`，差额的减法方向是否正确 |
| 改完结果没变 | 是否保存了 `shopping.el`，运行的路径是否指向它 |

先保留正确的部分，只改最早算错的一步，再运行。一次改很多地方，会更难知道是哪项改动起了作用。

## 做成自己的计划

收起完整源码，新建 `my-shopping.el`。选三类自己会买的物品，记录单价与数量，先在纸上算合计，再写程序。选择一个高于合计的预算、一个等于合计的预算和一个低于合计的预算，分别检查提醒。

!!! success "检查点"
    - [ ] 四行原始输出与目标一致
    - [ ] 验收表中的四种情况都已核对
    - [ ] 增加一项采购时没有复制循环和判断
    - [ ] 能解释每个变量的用途，并完成自己的三项清单

## 带走这三样

- 先把需求写成能检查的输出。
- 每完成一小步就运行，再接下一步。
- 数据变化时，通用的计算规则可以继续使用。

## 下一站：[值与类型](../language/values.md)

你已经用过数字和文字。接下来按需要查它们的详细规则；[语言总览](../language/index.md)能帮你选择章节，不必一口气读完。
