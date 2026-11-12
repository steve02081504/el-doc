# random/bits.el

本页由源码注释生成；示例未运行验证。

## 随机种子的定宽位表示 {#api-9048b7e7469dca7c1a6f}

源码：`src/stdlib/random/bits.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/bits.el)

提供整数校验与种子转换，将非负种子转换为固定 64 位字表示；无论宿主原生整数宽度如何，逻辑位宽都保持一致。

## require_integer {#api-21225a9e4f0be10c5008}

源码：`src/stdlib/random/bits.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/bits.el)

```el
export fn require_integer(value: Number)
```

检查数值是否有限且为整数。需要拒绝小数、无穷值和 NaN 的整数运算可先调用此函数；不符合条件时抛出范围错误。

**参数**：value 要检查的数值。

**返回值**：无返回值；输入为有限整数时正常返回。

**失败与异常**：RangeError 当输入不是有限整数时抛出。

### 示例：校验整数后转换为定宽字

```el
import { Number } from "file:../number/number.el"
import { require_integer, seed_bits } from "file:./bits.el"
require_integer(42)
let seed = seed_bits(42)
console.stdout.writeLine(Number(seed))
```
预期标准输出：
```text
42
```

## seed_bits {#api-26c100bd4eb558e472c0}

源码：`src/stdlib/random/bits.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/bits.el)

```el
export fn seed_bits(seed: Number): Word64
```

校验数值种子并将其转换为库的无符号 64 位字类型。取值范围为包含零、不包含 2^64，与宿主原生整数宽度无关。

**参数**：seed 范围为 0 <= seed < 2^64 的有限整数种子。

**返回值**：以固定宽度 Word64 表示的种子。

**失败与异常**：RangeError 当种子不是有限整数、为负数或大于等于 2^64 时抛出。

### 示例：转换种子并取回数值

```el
import { Number } from "file:../number/number.el"
import { seed_bits } from "file:./bits.el"
let seed = seed_bits(42)
console.stdout.writeLine(Number(seed))
```
预期标准输出：
```text
42
```
