# 带单位算距离和速度

> 量了两段跑道，一段是 125 厘米，一段是 0.75 米。怎么把它们加起来，再用同一种单位报出总长？

!!! abstract "🎯 做完这页，你能"
    - 用米和厘米构造量值，把两段距离加起来
    - 用距离除以时间求速度，再换算成千米每小时
    - 判断哪些量值可以相加，哪些会触发量纲错误

    <span class="el-chip">⏱ 约 10 分钟</span> <span class="el-chip">前置：[重复的计算只写一次](../beginner/functions.md)</span>

!!! note "实现状态"
    示例按当前 `el:units/` 源码编写，尚未经过 EL 编译和运行验证。

## 先把两段距离加起来

把下面的代码存为 `units.el`。

```el
import { centimetre, hour, kilometre, metre, second } from "el:units/"
import /^operator / from "el:units/"
import { min, max, sum, sqrt } from "el:mathematics/"

let firstPart = 125centimetre
let secondPart = 0.75metre
let total = sum(firstPart, secondPart)
console.stdout.writeLine("总长 ", total.standardText())
console.stdout.writeLine("换成米 ", total.inUnit(metre).standardText())
console.stdout.writeLine("较短一段 ", min(firstPart, secondPart).valueIn(centimetre), " cm")
console.stdout.writeLine("较长一段 ", max(firstPart, secondPart).valueIn(centimetre), " cm")

let distance = 20metre
let duration = 2second
let speed = distance / duration
console.stdout.writeLine("平均速度 ", speed.valueIn(metre / second), " m/s")
console.stdout.writeLine("换成千米每小时 ", speed.valueIn(kilometre / hour), " km/h")
console.stdout.writeLine("正方形边长 ", sqrt(4metre^2).valueIn(metre), " m")
```

在文件所在目录运行：

```sh
el run units.el
```

预期输出：

```text
总长 200 cm
换成米 2 m
较短一段 75 cm
较长一段 125 cm
平均速度 10 m/s
换成千米每小时 36 km/h
正方形边长 2 m
```

程序用 `125centimetre` 和 `0.75metre` 保存两次测量。数字紧贴单位时会按乘法构造量值。米和厘米都描述长度，长度就是它们共同的**量纲**。`sum(firstPart, secondPart)` 等同于两段直接相加，`min` 和 `max` 按换算后的实际长度选出一段。

??? question "先猜：把 0.75 米放到加号左边，结果会用什么单位？"
    结果会用米。加法把右边换成左边的单位，再相加。两种写法得到的总长度都相同。

| 写法 | 得到什么 |
| --- | --- |
| `total.valueIn(metre)` | 数字 `2`。适合交给只收数字的接口 |
| `total.inUnit(metre)` | 仍然带单位的量值 `2 m`。可以继续参与单位运算 |
| `total.inUnit(metre).standardText()` | 用固定单位符号显示的文本 `2 m` |

!!! warning "长度加上时间会报错"
    把第二段改成 `0.75second`，求和时会抛出 `UnitError`。计算总长度时，两项都要是长度。

## 先组合单位，再换算速度

在另一项测量中，物体用 2 秒走完 20 米。`20metre / 2second` 得到 `10 m/s`。`metre / second` 和 `kilometre / hour` 描述同一种量纲，所以可以用 `speed.valueIn(kilometre / hour)` 取得 `36`。

可以用现有运算符写复合单位。`1metre / second^2` 表示 1 米每平方秒。裸写 `2m` 默认表示 2 分钟，写米时用 `2metre`。

`4metre^2` 表示 4 平方米，所以 `sqrt(4metre^2)` 得到 2 米。`(4metre)^2` 表示把 4 米整体平方，得到 16 平方米。`sqrt(1metre)` 的长度指数为奇数，会抛出 `UnitError`。

!!! example "把 2 秒改成 4 秒"
    修改 `2second` 为 `4second`，保持距离为 20 米。两行速度应变成 `5 m/s` 和 `18 km/h`。

??? note "可选 · 自定义单位和数值类型"
    从 `el:units/` 导入 `defineUnit`。用 `let step = defineUnit("step", metre, 3 / 4, "step")` 定义每步固定为四分之三米的单位。`4step` 换算成米应得 3。

    如果用 `Integer(3)` 构造 3 厘米，换成米时，原来的整数类型无法表示 0.03。可显式换用 `inUnit(metre, element: Number)`。当前实现会在运算时检查量纲，量值类型的参数指定保存数字的类型。

## 带走这三样

- 数字紧贴单位，例如 `2metre`。
- 加减要求量纲相同，乘除会组合量纲。
- `inUnit` 保留单位，`valueIn` 取指定单位下的数字。

## 下一站：[用带单位的量做物理计算](physics.md)

> 力朝两个方向施加时，怎样分别算出加速度？物体只沿一个方向移动时，哪部分力做了功？

想按学科查找扩展单位、定义常量和计算误差，可继续读[在不同领域选用常量](constants.md)。
