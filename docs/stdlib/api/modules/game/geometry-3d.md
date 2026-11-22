# game/geometry-3d.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/game.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 三维几何 {#api-130e3be7c8786ad9286c}

源码：`src/stdlib/game/geometry-3d.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/game/geometry-3d.el#L1)

三维几何相关接口。

## Vec3 {#api-c2b766897515d547b014}

源码：`src/stdlib/game/geometry-3d.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/game/geometry-3d.el#L16)

三维有限坐标向量，支持向量运算。

```el-signature
export @assign(mode: "copy") class Vec3
```

**失败与异常**：坐标不是有限值时抛出错误。

### 示例：使用示例

```el
import { Vec3 } from "el:game/geometry-3d.el"
let vector = Vec3(1, 2, 3)
let squaredLength = vector.dot(vector)
```

## Rotation {#api-1aec5f9ef54dd1da4110}

源码：`src/stdlib/game/geometry-3d.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/game/geometry-3d.el#L61)

用非零四元数表示三维旋转。

```el-signature
export @assign(mode: "copy") class Rotation
```

**失败与异常**：输入不有限或四元数全为零时抛出错误。

### 示例：使用示例

```el
import { Rotation, Vec3 } from "el:game/geometry-3d.el"
let rotation = Rotation(0, 0, 0, 1)
let point = rotation.rotate(Vec3(1, 2, 3))
```

## Pose {#api-eb5bcee154da09e0a13a}

源码：`src/stdlib/game/geometry-3d.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/game/geometry-3d.el#L99)

表示位置和方向，可变换局部点。

```el-signature
export @assign(mode: "copy") class Pose
```

### 示例：使用示例

```el
import { Pose, Vec3 } from "el:game/geometry-3d.el"
let pose = Pose(Vec3(1, 0, 0))
let worldPoint = pose.transform(Vec3(2, 0, 0))
```

## Ray {#api-e4b1fff82bc09b6b9e5d}

源码：`src/stdlib/game/geometry-3d.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/game/geometry-3d.el#L122)

保存射线的原点和非零方向；方向不自动归一化。

```el-signature
export @assign(mode: "copy") class Ray
```

**失败与异常**：方向为零向量时抛出错误。

### 示例：使用示例

```el
import { Ray, Vec3 } from "el:game/geometry-3d.el"
let ray = Ray(Vec3(0, 0, 0), Vec3(0, 0, 1))
```
