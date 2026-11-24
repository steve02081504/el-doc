# 用带单位的量做物理计算

> 水下 2 米比水面多多少压力？给小车斜着施力时，怎样算出两个方向各自的变化？

!!! abstract "🎯 做完这页，你能"
    - 给定水的密度、重力加速度和深度，分别算出压力增量与绝对压力
    - 用带单位的向量计算小车的加速度、冲量和做功
    - 从电压与电阻算出电流，并读懂正负号

    <span class="el-chip">⏱ 约 20 分钟</span> <span class="el-chip">前置：[带单位算距离和速度](units.md)</span>

!!! note "实现状态"
    示例按当前 `el:units/` 和 `el:physics/` 源码编写，尚未经过 EL 编译和运行验证。

## 先算水下 2 米的压力

把[完整示例 `physics.el`](fixtures/physics.el)保存到本地，在文件所在目录运行：

```sh
el run physics.el
```

预期输出：

```text
压力增量 19620 Pa
绝对压力 119620 Pa
纵向加速度 2 m/s²
冲量分量 6, 8 N·s
做功 6 J
电流 -2 A
```

示例给水的密度 `1000 kg/m³`、重力加速度的大小 `9.81 m/s²`、水面下深度 `2 m`。`hydrostaticPressureIncrease(density, gravity, depth)` 把这三个量相乘，得到 `19620 Pa`，也就是 `19.62 kPa`。

??? question "先猜：把深度改成 0，绝对压力是多少？"
    压力增量变为 `0 Pa`。绝对压力等于你传入的液面压力，示例中是 `100000 Pa`。`hydrostaticAbsolutePressure` 以这个压力为基准，再加上水造成的增量。

!!! example "把深度加倍"
    把 `depth` 从 2 米改成 4 米。前两行应变成 `39240 Pa` 和 `139240 Pa`。两个函数都要求深度非负，深度沿液面向下量。

## 给推力的两个方向各写一个分量

示例用 `World` 标记小车所在的坐标系，约定第一个轴朝右，第二个轴朝前。`QuantityVector<frame: World, dimensions: 2>` 声明一个二维量值向量类型。构造它时，两个分量要有相同量纲，程序会换算到第一个分量使用的单位。

推力 `thrust` 含两个分量，朝右 `3 N`、朝前 `4 N`。小车质量是 `2 kg`。

| 在程序中找 | 怎么算 | 怎样核对 |
| --- | --- | --- |
| `acceleration(thrust, mass)` | 每个推力分量除以质量 | `accelerationVector[1]` 是第二个分量，等于 `2 m/s²` |
| `constantForceImpulse(thrust, duration)` | 每个推力分量乘以恒力持续的 2 秒 | `impulse[0]` 和 `impulse[1]` 分别是 `6 N·s` 和 `8 N·s` |
| `thrust.dot(displacement)` | 点乘把同方向的分量分别相乘再求和 | 小车只朝右移 2 米，做功等于 `3 × 2 + 4 × 0 = 6 J` |

??? question "先猜：小车如果改成只朝前移 2 米，推力做多少功？"
    得到 `8 J`。把位移分量从 `(2, 0)` 米改成 `(0, 2)` 米，此时只有第二个方向贡献做功。

??? note "可选 · 坐标系和近似长度"
    向量加减和点乘要求分量数与坐标系一致。局部坐标和世界坐标之间可以用 `RigidTransform` 转换。`applyVector` 只旋转力或位移，`applyPoint` 还会平移位置。两个同坐标系的点相减得到位移。

    `approximateMagnitude()` 返回带单位的近似长度，开方使用 `WorkingFloat`。`quadraticDrag` 用物体相对流体的速度求阻力，也用到这个近似长度，结果方向与相对速度相反。

## 用欧姆定律读出电流方向

`ohmicCurrent(voltage, resistance)` 用电压除以电阻。给定 `-12 V` 和 `6 Ω`，得到 `-2 A`。负号表示电流与选定的正方向相反。只改电压为 `12 V`，末行就应变为 `2 A`。

!!! warning "由电压反求电流时，电阻必须大于零"
    把 `ohm.of(6)` 改成 `ohm.of(0)` 会抛出 `UnitError`。先检查输入电阻的数值和单位。

## 带走这三样

- 算绝对压力时，要给出作为基准的液面压力。
- 向量带着坐标系和单位，点乘把同方向分量配对。
- 模型会检查量纲和输入范围，例如深度非负、反求电流时电阻严格为正。

## 下一站：[矩阵与数值脚本](numerics.md)

> 一次实验如果采了很多组数据，怎样把它们排成矩阵并画出变化曲线？
