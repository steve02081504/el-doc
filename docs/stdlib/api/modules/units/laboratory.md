# units/laboratory.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/units.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 实验室常量 {#api-83fb041388a0595b5e61}

源码：`src/stdlib/units/laboratory.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L1)

实验中心参考值、标准不确定度和精确导出关系。

## electronvolt {#api-63dc6f1929648a03c447}

源码：`src/stdlib/units/laboratory.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L22)

电子伏特，精确等于 1.602176634 × 10⁻¹⁹ 焦耳。

```el-signature
@quantityDimension(numerator: @[MassDimension, LengthDimension, LengthDimension], denominator: @[DurationDimension, DurationDimension])
export let electronvolt = defineUnit("electronvolt", joule, 1.602176634e-19, "eV")
```

### 示例：使用示例

```el
import { electronvolt } from "el:units/"
let value = electronvolt
```

## electronMass {#api-1fee048d090370a89429}

源码：`src/stdlib/units/laboratory.el:32` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L32)

电子质量的 中心参考值。

```el-signature
export let electronMass = 9.1093837139e-31 * (kilogram)
```

### 示例：使用示例

```el
import { electronMass } from "el:units/"
let value = electronMass
```

## electronMassStandardUncertainty {#api-a530a4a8619a509374b2}

源码：`src/stdlib/units/laboratory.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L41)

电子质量的 标准不确定度，以一个标准差表示。

```el-signature
export let electronMassStandardUncertainty = 2.8e-40 * (kilogram)
```

### 示例：使用示例

```el
import { electronMassStandardUncertainty } from "el:units/"
let value = electronMassStandardUncertainty
```

## protonMass {#api-b0867cfddf3df0f25be3}

源码：`src/stdlib/units/laboratory.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L50)

质子质量的 中心参考值。

```el-signature
export let protonMass = 1.67262192595e-27 * (kilogram)
```

### 示例：使用示例

```el
import { protonMass } from "el:units/"
let value = protonMass
```

## protonMassStandardUncertainty {#api-c38af6c5a892a7c553a5}

源码：`src/stdlib/units/laboratory.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L59)

质子质量的 标准不确定度，以一个标准差表示。

```el-signature
export let protonMassStandardUncertainty = 5.2e-37 * (kilogram)
```

### 示例：使用示例

```el
import { protonMassStandardUncertainty } from "el:units/"
let value = protonMassStandardUncertainty
```

## neutronMass {#api-9b86ac228b02bb5897e4}

源码：`src/stdlib/units/laboratory.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L68)

中子质量的 中心参考值。

```el-signature
export let neutronMass = 1.67492750056e-27 * (kilogram)
```

### 示例：使用示例

```el
import { neutronMass } from "el:units/"
let value = neutronMass
```

## neutronMassStandardUncertainty {#api-e9b32e31057aa5ac7e7c}

源码：`src/stdlib/units/laboratory.el:77` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L77)

中子质量的 标准不确定度，以一个标准差表示。

```el-signature
export let neutronMassStandardUncertainty = 8.5e-37 * (kilogram)
```

### 示例：使用示例

```el
import { neutronMassStandardUncertainty } from "el:units/"
let value = neutronMassStandardUncertainty
```

## atomicMassConstant {#api-218575b2b2590a31e0f1}

源码：`src/stdlib/units/laboratory.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L86)

原子质量常量的 中心参考值。

```el-signature
export let atomicMassConstant = 1.66053906892e-27 * (kilogram)
```

### 示例：使用示例

```el
import { atomicMassConstant } from "el:units/"
let value = atomicMassConstant
```

## atomicMassConstantStandardUncertainty {#api-fb432911d058df37bd02}

源码：`src/stdlib/units/laboratory.el:95` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L95)

原子质量常量的 标准不确定度，以一个标准差表示。

```el-signature
export let atomicMassConstantStandardUncertainty = 5.2e-37 * (kilogram)
```

### 示例：使用示例

```el
import { atomicMassConstantStandardUncertainty } from "el:units/"
let value = atomicMassConstantStandardUncertainty
```

## fineStructureConstant {#api-c4a3ef28c891d7519bcf}

源码：`src/stdlib/units/laboratory.el:104` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L104)

精细结构常量的 中心参考值。

```el-signature
export let fineStructureConstant = 7.2973525643e-3 * (one)
```

### 示例：使用示例

```el
import { fineStructureConstant } from "el:units/"
let value = fineStructureConstant
```

## fineStructureConstantStandardUncertainty {#api-46b18134f230bb649f54}

源码：`src/stdlib/units/laboratory.el:113` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L113)

精细结构常量的 标准不确定度，以一个标准差表示。

```el-signature
export let fineStructureConstantStandardUncertainty = 1.1e-12 * (one)
```

### 示例：使用示例

```el
import { fineStructureConstantStandardUncertainty } from "el:units/"
let value = fineStructureConstantStandardUncertainty
```

## bohrRadius {#api-09dae4f6ba8de23d2053}

源码：`src/stdlib/units/laboratory.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L122)

玻尔半径的 中心参考值。

```el-signature
export let bohrRadius = 5.29177210544e-11 * (metre)
```

### 示例：使用示例

```el
import { bohrRadius } from "el:units/"
let value = bohrRadius
```

## bohrRadiusStandardUncertainty {#api-042ecf59a3fbe0274f1d}

源码：`src/stdlib/units/laboratory.el:131` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L131)

玻尔半径的 标准不确定度，以一个标准差表示。

```el-signature
export let bohrRadiusStandardUncertainty = 8.2e-21 * (metre)
```

### 示例：使用示例

```el
import { bohrRadiusStandardUncertainty } from "el:units/"
let value = bohrRadiusStandardUncertainty
```

## rydbergConstant {#api-8395f7b805f70a4109bb}

源码：`src/stdlib/units/laboratory.el:140` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L140)

里德伯常量的 中心参考值。

```el-signature
export let rydbergConstant = 10973731.568157 * (one / metre)
```

### 示例：使用示例

```el
import { rydbergConstant } from "el:units/"
let value = rydbergConstant
```

## rydbergConstantStandardUncertainty {#api-5132990bb0667abf6b43}

源码：`src/stdlib/units/laboratory.el:149` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L149)

里德伯常量的 标准不确定度，以一个标准差表示。

```el-signature
export let rydbergConstantStandardUncertainty = 0.000012 * (one / metre)
```

### 示例：使用示例

```el
import { rydbergConstantStandardUncertainty } from "el:units/"
let value = rydbergConstantStandardUncertainty
```

## hartreeEnergy {#api-b60b00e3aa7560740590}

源码：`src/stdlib/units/laboratory.el:158` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L158)

哈特里能量的 中心参考值。

```el-signature
export let hartreeEnergy = 4.3597447222060e-18 * (joule)
```

### 示例：使用示例

```el
import { hartreeEnergy } from "el:units/"
let value = hartreeEnergy
```

## hartreeEnergyStandardUncertainty {#api-cd04838e72dbb6e1f68c}

源码：`src/stdlib/units/laboratory.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L167)

哈特里能量的 标准不确定度，以一个标准差表示。

```el-signature
export let hartreeEnergyStandardUncertainty = 4.8e-30 * (joule)
```

### 示例：使用示例

```el
import { hartreeEnergyStandardUncertainty } from "el:units/"
let value = hartreeEnergyStandardUncertainty
```

## vacuumElectricPermittivity {#api-cc727ed99670de84eff1}

源码：`src/stdlib/units/laboratory.el:176` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L176)

真空介电常量的 中心参考值。

```el-signature
export let vacuumElectricPermittivity = 8.8541878188e-12 * (farad / metre)
```

### 示例：使用示例

```el
import { vacuumElectricPermittivity } from "el:units/"
let value = vacuumElectricPermittivity
```

## vacuumElectricPermittivityStandardUncertainty {#api-f928712dd7bf8ed5a3e5}

源码：`src/stdlib/units/laboratory.el:185` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L185)

真空介电常量的 标准不确定度，以一个标准差表示。

```el-signature
export let vacuumElectricPermittivityStandardUncertainty = 1.4e-21 * (farad / metre)
```

### 示例：使用示例

```el
import { vacuumElectricPermittivityStandardUncertainty } from "el:units/"
let value = vacuumElectricPermittivityStandardUncertainty
```

## vacuumMagneticPermeability {#api-264fa10cf49093be2e97}

源码：`src/stdlib/units/laboratory.el:194` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L194)

真空磁导率的 中心参考值。

```el-signature
export let vacuumMagneticPermeability = 1.25663706127e-6 * (newton / (ampere ^ 2))
```

### 示例：使用示例

```el
import { vacuumMagneticPermeability } from "el:units/"
let value = vacuumMagneticPermeability
```

## vacuumMagneticPermeabilityStandardUncertainty {#api-f859ae9181e98d23acb4}

源码：`src/stdlib/units/laboratory.el:203` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L203)

真空磁导率的 标准不确定度，以一个标准差表示。

```el-signature
export let vacuumMagneticPermeabilityStandardUncertainty = 2.0e-16 * (newton / (ampere ^ 2))
```

### 示例：使用示例

```el
import { vacuumMagneticPermeabilityStandardUncertainty } from "el:units/"
let value = vacuumMagneticPermeabilityStandardUncertainty
```

## vonKlitzingConstant {#api-15d26fb433a2e854eb6f}

源码：`src/stdlib/units/laboratory.el:212` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L212)

冯克利青常量 h/e²，精确导出值。

```el-signature
export let vonKlitzingConstant = planckConstant / (elementaryCharge ^ 2)
```

### 示例：使用示例

```el
import { vonKlitzingConstant } from "el:units/"
let value = vonKlitzingConstant
```

## magneticFluxQuantum {#api-eff093474e8a8e4445c8}

源码：`src/stdlib/units/laboratory.el:221` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L221)

磁通量子 h/(2e)，精确导出值。

```el-signature
export let magneticFluxQuantum = planckConstant / (2 * elementaryCharge)
```

### 示例：使用示例

```el
import { magneticFluxQuantum } from "el:units/"
let value = magneticFluxQuantum
```

## josephsonConstant {#api-710d931251ade76fabe6}

源码：`src/stdlib/units/laboratory.el:230` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L230)

约瑟夫森常量 2e/h，精确导出值。

```el-signature
export let josephsonConstant = 2 * elementaryCharge / planckConstant
```

### 示例：使用示例

```el
import { josephsonConstant } from "el:units/"
let value = josephsonConstant
```

## conductanceQuantum {#api-cb48d3c373198c7d352c}

源码：`src/stdlib/units/laboratory.el:239` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L239)

电导量子 2e²/h，精确导出值。

```el-signature
export let conductanceQuantum = 2 * (elementaryCharge ^ 2) / planckConstant
```

### 示例：使用示例

```el
import { conductanceQuantum } from "el:units/"
let value = conductanceQuantum
```

## secondRadiationConstant {#api-959e015dfecfa7e7f86e}

源码：`src/stdlib/units/laboratory.el:248` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L248)

第二辐射常量 hc/k，精确导出值。

```el-signature
export let secondRadiationConstant = planckConstant * speedOfLight / boltzmannConstant
```

### 示例：使用示例

```el
import { secondRadiationConstant } from "el:units/"
let value = secondRadiationConstant
```

## stefanBoltzmannConstant {#api-357002d8bd6fe84b3b34}

源码：`src/stdlib/units/laboratory.el:257` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/units/laboratory.el#L257)

计算 σ = 2π⁵k⁴/(15h³c²)。epsilon 是以 W·m⁻²·K⁻⁴ 计的有限正最大绝对计算误差。

```el-signature
export fn stefanBoltzmannConstant(epsilon: Number)
```

### 示例：使用示例

```el
import { stefanBoltzmannConstant } from "el:units/"
let value = stefanBoltzmannConstant(1e-20)
```
