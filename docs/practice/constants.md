# 在不同领域选用常量

> `299792458`、`9.80665` 和实验测得的引力常数，都是数字；它们代表的确定程度却不同。

!!! abstract "🎯 做完这页，你能"
    - 按用途找到天文、地球测量、化学、电子学、热学和数学常量
    - 分清定义值、约定值、测量值和可控误差的计算结果
    - 给近似计算选一个有单位含义的 `epsilon`

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[带单位算距离和速度](units.md)</span>

!!! note "源码与验证状态"
    名称依据 `el:units/` 与 `el:mathematics/` 的标准库导出。示例按源码接口静态核对，尚未用 EL 工具链编译或运行。

## 先按领域挑单位

单位是量值的尺度与量纲；它们本身不表示一次测量有多准确。单位按定义比例换算，例如天文单位按固定米数定义；天文观测得到的距离仍可能带测量误差。下面列出各领域的常用入口；完整符号与合同见对应 API 页：

| 领域 | 单位 | 常见用途 |
| --- | --- | --- |
| 天文学与地球测量 | `astronomicalUnit`、`lightYear`、`julianYear`、`parsec(epsilon)`、`wgs84SemiMajorAxis`、`nominalSolarLuminosity` | 行星／恒星距离、天文时间、地球参考椭球和太阳名义光度；[天文 API](../stdlib/api/modules/units/astronomy.md) |
| 声学 | `standardTuningA4`、`hertz` | A4 标准音高及频率；[参考量 API](../stdlib/api/modules/units/references.md) |
| 实验室日常单位 | `litre`、`millilitre`、`tonne`、`hectare` | 体积、质量、面积；[常用单位 API](../stdlib/api/modules/units/everyday.md) |
| 百分比与比例 | `percent`、`basisPoint` | 比例与基点；[常用单位 API](../stdlib/api/modules/units/everyday.md) |
| 字节量 | `byte`、`kibibyte`、`mebibyte`、`gibibyte`、`tebibyte`、`pebibyte`、`exbibyte` | 固定比例的普通带单位量；[基础单位 API](../stdlib/api/modules/units/builtins.md) |
| 目标数位容量 | `dit`、`kd`、`md`、`gd`、`td`、`pd`、`ed` | 编译目标基数相关的容量单位，也用于 `FileSize`；[目标数位 API](../stdlib/api/modules/units/dits.md) |
| 粒子与热学 | `electronvolt`、`electronMass`、`electronMassStandardUncertainty`、`stefanBoltzmannConstant(epsilon)` | 能量、粒子质量、辐射计算；[实验室常量 API](../stdlib/api/modules/units/laboratory.md) |

单位可参与乘除和换算，例如光年可以转换成米；不要把“单位换算精确”误当作“原始观测精确”。

## 常量分为四类

### 定义值与约定值

有些数值由定义固定，例如 `speedOfLight`（米每秒）和 `planckConstant`（焦耳秒）；`standardGravity` 是规定的标准重力加速度。`standardAtmosphericPressure` 是标准大气压，`standardStatePressure` 是标准状态压强。它们适合定义清楚、可复现的换算或基准。

### 测量参考值

`gravitationalConstant` 是实验测量参考值，标准不确定度另由 `gravitationalConstantStandardUncertainty` 给出。新版接口还提供 `electronMass` 与 `electronMassStandardUncertainty`，以及随 `epsilon` 返回的 `stefanBoltzmannConstant(epsilon)`。这些名字表达的确定程度不同；写科学计算时应保留来源、误差和模型假设，不能只打印更多小数位来声称更准确。

### 公式计算值

`reducedPlanckConstant(epsilon)`、`planckLength(epsilon)`、`planckTime(epsilon)`、`planckMass(epsilon)` 和 `planckTemperature(epsilon)` 根据其他常量计算。它们的 `epsilon` 代表调用方允许的最大绝对计算误差，并使用结果相应的单位：例如 `planckTime` 用秒，`planckLength` 用米。公式输入中的实验不确定度仍需单独考虑；计算误差上限不会消除输入数据的不确定性。

### 数学近似值

数学模块提供 `eulerNumber(epsilon)`、`tau(epsilon)`、`goldenRatio(epsilon)`、`sqrtTwo(epsilon)`、`lnTwo(epsilon)`、`standardNormalDensityAtZero(epsilon)` 和 `equalTemperedSemitoneRatio(epsilon)`。它们都是无量纲数值，`epsilon` 是最大绝对误差；同样的 `epsilon` 用在不同尺度的计算中，代表不同的相对精度。完整列表见[数学常量 API](../stdlib/api/modules/mathematics/functions/constants.md)。

## `epsilon` 是精度要求，不是测量误差

```el
import { eulerNumber, sqrtTwo } from "el:mathematics/"

let looseEstimate = eulerNumber(1e-6)
let tighterEstimate = eulerNumber(1e-12)
let diagonalRatio = sqrtTwo(1e-12)
console.stdout.writeLine("e 的近似值：", looseEstimate)
console.stdout.writeLine("更紧的 e 近似值：", tighterEstimate)
console.stdout.writeLine("单位正方形对角线比值：", diagonalRatio)
```

`epsilon` 越小，调用方要求的计算误差上限越严格；它不是输出的小数位数，也不是实验测量的不确定度。对于有单位的计算，先读对应 API 条目：例如 `parsec(epsilon)` 的误差以米计，而数学常量的误差没有物理单位。给不合适的误差单位或超过工具可表达的精度时，调用可能失败，具体条件以该 API 的参数与异常合同为准。

!!! warning "算得更细，不等于知道得更准"
    如果输入是带测量误差的数据，先用 `Measured` 和 `measured` 表达已知输入误差；`epsilon` 只约束计算过程新增的误差。结果报告应把两者分开。

## 继续查阅

- [单位 API](../stdlib/api/modules/units/astronomy.md)：天文、地理、实验室、日常和参考单位的分类入口。
- [物理常量 API](../stdlib/api/modules/units/constants.md) 与[实验室常量 API](../stdlib/api/modules/units/laboratory.md)：查询常量公式、参数误差单位和失败条件。
- [带单位算距离和速度](units.md)：学习量值、单位换算与量纲。
- [用带单位的量做物理计算](physics.md)：把量值用于压力、向量和电路示例。
