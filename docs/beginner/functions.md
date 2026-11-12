# 重复的计算只写一次

> 买 3 本本子、买 5 支铅笔，都是“单价乘数量”。给这条规则起个名字，下次直接用。

!!! abstract "🎯 读完这页，你能"
    - 定义一个计算总价的函数
    - 把不同的单价和数量交给它
    - 区分返回计算结果和显示文字

    <span class="el-chip">先看两次调用，再读定义</span> <span class="el-chip">前置：[把阅读记录加起来](lists.md)</span>

## 规则相同，交进去的数据不同

**函数**是一段有名字、可以重复调用的代码。**调用**就是请它工作一次。新建 `cost.el`，保存完整内容：

```el
fn purchaseCost(price: Number, quantity: Number): Number {
	return price * quantity
}

let notebookCost = purchaseCost(4, 3)
let pencilCost = purchaseCost(2, 5)

console.stdout.writeLine("本子：", notebookCost, " 元")
console.stdout.writeLine("铅笔：", pencilCost, " 元")
console.stdout.writeLine("合计：", notebookCost + pencilCost, " 元")
```

运行 `el run cost.el`，预期输出：

```text
本子：12 元
铅笔：10 元
合计：22 元
```

## 从一次调用看懂函数

读 `purchaseCost(4, 3)` 时，先按位置对应：`4` 交给 `price`，`3` 交给 `quantity`。函数计算 `4 * 3`，再由 `return` 把 `12` 交回调用的位置，最后存入 `notebookCost`。

`price` 和 `quantity` 叫作**参数**：它们是函数为收到的数据起的名字。下一次调用 `purchaseCost(2, 5)` 时，这两个名字分别代表 `2` 和 `5`。

定义第一行的 `fn` 表示定义函数；`Number` 表示数字类型。参数后面的 `: Number` 说明这里收数字，右括号后面的 `: Number` 说明返回数字。**类型**说明一份数据属于哪一类，例如数字或文字；这页先照着写数字类型即可。

## `return` 负责交回结果，输出负责让人看见

上面的函数里没有 `writeLine`，它只负责算数。外面的代码拿到结果后，可以显示，也可以继续相加。

如果只写 `console.stdout.writeLine(price * quantity)`，屏幕虽然显示了总价，函数交回的却不是你要的总价。`writeLine` 本身返回的是写出的字节数，不能把它当成采购金额来加。

## 你来改一次调用

铅笔从 5 支改成 6 支，只改 `purchaseCost(2, 5)` 的第二个数字。先预测三行结果，再运行。

??? question "核对答案"
    本子仍是 `12` 元，铅笔变为 `12` 元，合计 `24` 元。函数定义不需要跟着改。

## 补一步：算出余额

在原程序后面增加下面的内容。填空部分不是合法代码，先补好再运行：

```text
let budget = 30
let remaining = budget - ___ - ___
console.stdout.writeLine("余额：", remaining, " 元")
```

??? success "参考答案"
    填 `notebookCost` 和 `pencilCost`。原始采购数量下余额是 `8` 元；若保留了刚才 6 支铅笔的改动，余额是 `6` 元。核对答案时也要核对输入。

## 收起例子，自己写一个车费函数

新建 `fare.el`，定义 `tripCost`，接收一次车费和乘坐次数，返回总车费。调用 `tripCost(2, 4)` 应得到 `8`，调用 `tripCost(3, 2)` 应得到 `6`。最后把两次结果相加并显示，合计应为 `14`。

??? tip "提示"
    先写函数定义里的计算和 `return`，再写两次调用，最后输出。不要把输出放进只负责计算金额的函数里。

!!! success "检查点"
    - [ ] 能指出参数、传入的数字和交回的结果
    - [ ] 改采购数量时没有修改函数定义
    - [ ] 车费函数的结果能继续用于加法

## 带走这三样

- 函数给一条可重复使用的规则起名字。
- 每次调用可以传入不同的数据。
- 返回结果后，调用者才能继续用它计算。

## 下一站：[完成文具采购小助手](shopping.md)

把采购清单、合计和预算提醒组合成一个完整作品。
