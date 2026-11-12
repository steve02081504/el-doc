# 零花钱还剩多少

> 你有 20 元，买了 3 本笔记本，每本 4 元。回家前想核对一下：应该剩多少钱？

!!! abstract "🎯 读完这页，你能"
    - 用有名字的数字记录预算、单价和数量
    - 打印带单位的总价与余额
    - 修改一项购物数据，并核对新结果

    <span class="el-chip">建议分两次练习</span> <span class="el-chip">前置：[运行第一个程序](../getting-started.md)</span>

## 先算一遍，再让电脑算

3 本，每本 4 元，总价是 `4 × 3 = 12` 元。余额是 `20 − 12 = 8` 元。这两个数字就是我们用来检查程序的答案。

新建 `budget.el`，把下面的**完整内容**保存进去。怎样保存和运行文件，可以回看[第一个程序](../getting-started.md)。

```el
let budget = 20
let price = 4
let quantity = 3
let cost = price * quantity
let remaining = budget - cost

console.stdout.writeLine("总价：", cost, " 元")
console.stdout.writeLine("余额：", remaining, " 元")
```

在这个文件所在的文件夹里打开终端，输入命令：

```sh
el run budget.el
```

预期输出：

```text
总价：12 元
余额：8 元
```

## 给数字起名字，就不用到处找数字

`let budget = 20` 的意思是：创建一个叫 `budget` 的变量，先记住数字 `20`。**变量**可以理解为程序里有名字的一份记录。这里的 `budget` 是预算，`price` 是单价，`quantity` 是数量，`cost` 是总价，`remaining` 是余额。

`=` 在这里表示把右边的结果存到左边。电脑从上往下执行：先记住数据，再计算总价，最后计算余额。`*` 表示乘法，`-` 表示减法。

`console.stdout.writeLine(...)` 负责显示一行结果。括号里的内容用英文逗号分开，按顺序显示；双引号包住的是照原样显示的文字，没加引号的 `cost` 会取出这个变量记住的数字。

不用背下输出指令的每个词。先保留整句写法，改括号里的内容。

## 你来改一处：笔记本涨到 5 元

只把 `let price = 4` 改成 `let price = 5`，保存。**运行前先算：总价和余额会是多少？**

??? question "核对答案"
    总价 `15` 元，余额 `5` 元。程序用的是 `price * quantity`，所以改了单价，后面的计算也会采用新单价。

再运行 `el run budget.el`。如果仍然看到旧结果，先检查文件是否已经保存，以及终端运行的是不是同一个文件。

## 你来补一步：再买一块橡皮

回到每本 4 元、买 3 本的原始数据。再买一块 2 元的橡皮，希望输出余额 `6` 元。把原程序计算余额的那一行换成下面两行，`___` 是留给你填的地方，不能原样运行：

```text
let eraserPrice = 2
let remaining = budget - cost - ___
```

??? tip "提示"
    余额要再减去橡皮的价格。这个价格已经记在 `eraserPrice` 里。

??? success "参考答案"
    填 `eraserPrice`。原始数据下计算过程是 `20 - 12 - 2 = 6`。

## 一个容易误会的地方：结果不会自动重算

下面是另一个完整小实验，可以另存为 `price-change.el`：

```el
let price = 4
let quantity = 3
let cost = price * quantity
price = 5
console.stdout.writeLine(cost)
cost = price * quantity
console.stdout.writeLine(cost)
```

输出是先 `12`，再 `15`，各占一行。`cost` 记住的是计算当时的结果；后来改了 `price`，需要再次计算并赋给 `cost`，它才会更新。这里的变量不是电子表格里的自动更新公式。

## 收起例子，自己做一张车费账单

你有 30 元，每次坐车 2 元，计划坐 4 次。新建 `bus.el`，输出总车费和余额，分别应是 `8` 元与 `22` 元。可以给变量换名字，只要含义清楚、前后一致。

!!! success "检查点"
    - [ ] 能说出总价为什么用乘法、余额为什么用减法
    - [ ] 把坐车次数改成 5，总车费变为 10 元，余额变为 20 元
    - [ ] 能解释 `"cost"` 和 `cost` 显示的内容有什么不同

## 带走这三样

- `let` 给数据起名字，名字要能说明用途。
- 计算按代码顺序发生，已算出的结果不会自动更新。
- 先手算一个答案，再核对程序输出。

## 下一站：[钱够不够买](decisions.md)

如果要花 24 元，手里只有 20 元，程序能主动提醒你吗？
