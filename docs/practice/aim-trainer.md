# 三维瞄准练习器

> 把鼠标转向、移动和跳跃拆成固定步长的模拟，再记录每次点击有没有选中屏幕里的虚拟目标。

!!! abstract "🎯 做完这页，你能"
    - 用标准库的三维位姿和射线检查虚拟目标
    - 为镜头、移动、跳跃和回合统计建立可独立验证的规则

    <span class="el-chip">⏱ 约 30 分钟</span> <span class="el-chip">前置：[二维乒乓球](paddle-game.md)</span>

!!! note "实现状态"
    当前 `el:game/three-dimensional.el` 导出 `Vec3`、`Rotation`、`Pose` 和 `Ray`。示例使用这层三维几何，尚未编译或运行。完整场景渲染、第一人称输入与游戏宿主仍需要接通。

## 先让测试射线选中一个球形目标

把完整程序保存为 `target.el`，运行 `el run target.el`。约定世界的 Y 轴向上，镜头本地的 +Z 朝前。

```el
import { Vec3, Pose, Ray } from "el:game/three-dimensional.el"

fn hits(ray: Ray, center: Vec3, radius: Number): Bool {
	let offset = center - ray.origin
	let direction = ray.direction
	let projection = offset.dot(direction) / direction.dot(direction)
	let closest = ray.origin + direction * (if (projection < 0) 0 else projection)
	let delta = center - closest
	return delta.dot(delta) <= radius * radius
}

let camera = Pose(Vec3(0, 1, 0))
let ray = Ray(camera.position, camera.orientation.rotate(Vec3(0, 0, 1)))
if (!hits(ray, Vec3(0, 1, 5), 1)) throw "应当选中前方目标"
if (hits(ray, Vec3(0, 1, -5), 1)) throw "不应选中背后目标"
if (hits(ray, Vec3(2, 1, 5), 1)) throw "不应选中侧面目标"
console.stdout.writeLine("三个目标检查通过")
```

`projection` 是目标中心在射线方向上的投影参数。把负投影限制到零后，再比较最近点与目标中心的距离，可以处理起点已经在球内的情况。场景有多个目标时，可求各个球的非负入交参数并选择最小者。有遮挡物时，场景查询还要比较遮挡物与目标的距离。

## 给镜头和角色接输入

| 需求 | 每步如何更新 | 检查 |
| --- | --- | --- |
| 左顾右盼 | 水平鼠标位移累加到偏航，垂直位移累加到俯仰。限制俯仰接近上下直视时的范围，按偏航、俯仰的顺序组合旋转 | 左转后镜头前方向左，向上抬头时镜头不会翻转 |
| 前后左右 | 用偏航旋转得到水平前向和右向，映射 WASD。合并斜向输入后限制长度，再乘速度和步长 | 按住前和右一秒，水平总位移等于只按前一秒 |
| 跳跃 | 地面上收到跳跃边沿时设定上升速度。每步先加重力再积分高度，触地时归零垂直速度 | 保持跳跃键不会连跳，单跳能回到地面 |
| 点击目标 | 从相机位置沿当前前向发出射线。每次输入边沿记录一次点击，命中才替换目标 | 错过时目标保留，命中一次只生成一个新目标 |

回合时钟和移动统一使用模拟步长。窗口失焦时清空已按住的按键，暂停计时；恢复后从原状态继续。用同一个种子生成目标序列，用录制的输入验证不同帧率下的结果一致。

## 用固定步长检查移动和落地

把下面完整程序另存为 `move.el`，运行 `el run move.el`。它用三维方向更新水平位移，用明确的地面高度处理一次跳跃。示例朝向绕 Y 轴转了四分之一圈，所以前进沿 +X。步长取 0.1 秒，方便手算核对。

```el
import { Vec3, Rotation, Pose } from "el:game/three-dimensional.el"

let yaw = Rotation(0, 1, 0, 1)
let forward = yaw.rotate(Vec3(0, 0, 1))
let right = yaw.rotate(Vec3(1, 0, 0))
let horizontal = forward * 1 + right * 0
let step = 1 / 10
let feet = Vec3(0, 0, 0)
let vertical = 4
let high = 0
for (let frame = 0; frame < 10; frame++) {
	vertical -= 10 * step
	let moved = feet + horizontal * (2 * step)
	let height = moved.y + vertical * step
	if (height <= 0) {
		height = 0
		vertical = 0
	}
	if (height > high) high = height
	feet = Vec3(moved.x, height, moved.z)
}
let camera = Pose(feet + Vec3(0, 1, 0), yaw)
if (feet.x != 2 | feet.y != 0 | feet.z != 0 | high != 3 / 5) throw "移动或跳跃和预期不符"
console.stdout.writeLine("前进 2 米，跳跃后触地，相机离地 ", camera.position.y, " 米")
```

把向右输入从 0 改为 1，再按前面的斜线规则归一化。浮点归一化可用平方距离和误差范围验收。要在屏幕上显示目标，用 `camera.inverseTransform(center)` 求相机坐标，筛掉深度小于近平面的目标，再用 `x / z`、`y / z` 计算屏幕位置。先用网格或画布显示目标中心，再接真正场景、深度遮挡与连续鼠标输入。

## 让结算页读得出进步

记录回合编号、练习时长、点击数、命中数、每次目标出现到命中的毫秒数。结算显示命中率、每分钟命中数、反应时间中位数与第 90 百分位。零点击或零命中时显示对应指标为“暂无”。保存最近 20 局，按时间画命中率和中位反应时间两条曲线，保留原始回合记录供复查。

!!! example "先核对一局的统计"
    模拟一局 30 秒、10 次点击、7 次命中。结算应显示 70% 命中率和每分钟 14 次命中。重开时本局计数清零，历史记录仍可读取。

## 下一站：[用随机地形训练步态](train-walker.md)

把键盘输入换成模型输出，继续复用固定步长、种子和统计的做法。
