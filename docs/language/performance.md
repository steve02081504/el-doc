# 性能与底层优化

> `el build --release` 让你变快的那一下，关掉的不是语言检查，而是一批运行期安全检查；越过它们所保护前提的代码在 release 下会变成未定义行为。

!!! abstract "🎯 读完这页，你能"
    - 判断一次性能问题该先测什么，以及 debug 与 release 各自保留哪些检查
    - 写对 `@pure` 与 `@bounded`，并说清它们为什么不改变语义、也不保证提速
    - 认出 SIMD 与 GPU 的真实入口和准入条件，不把时间花在不会被采用的写法上

    <span class="el-chip">⏱ 约 15 分钟</span> <span class="el-chip">前置：[函数与闭包](functions.md)、[数值与位类型](numeric-types.md)</span>

这页可以跳过。先用普通写法把程序写对；等真的测出瓶颈，或者确实要上原生标量、设备时，再回来读对应小节。

## 先分清三层：默认优化、构建模式、显式请求

EL 的默认路径不要求手写优化：优化器与逐元素链融合在普通调用下工作。属性、执行策略和设备会话是知道瓶颈后的额外入口；混为一谈，就容易把“合同”当“开关”用。

| 层 | 你做什么 | 它改变什么 |
| --- | --- | --- |
| 默认优化 | 什么都不用做 | 逐元素链融合、复制消除、编译期求值 |
| 构建模式 | `el build --release` | 去掉 debug 保留的运行期安全检查 |
| 显式请求 | 属性、`map(policy:)`、`TensorDevice` | 给编译器信任合同、选执行候选、上设备 |

==先测量，再决定动哪一层；属性不改变类型或运行期语义。==

## `--release` 去掉检查，不改变语言语义

默认构建是 debug，保留标准库中防止违反调用前提的运行期检查：数组、文本、视图的索引与范围检查，内部存储状态断言，以及部分字节与租约的非法使用诊断。`el build --release` 去掉的正是这些检查；`el run --release` 对运行源码同理。

```sh
el build --release src/main.el -o build/app
```

release 不会关掉语言语义：类型、借用、所有权与生命周期检查在编译期完成，两种模式都执行；解析与编码失败、数值位宽与溢出策略、分配和系统 I/O 失败、schema、快照版本、来源、取消与并发状态合同，在 release 仍然生效。越过检查所保护的安全前置条件属于未定义行为：release 既不保证抛错，也不保证结果有效。

```el
if (debug_mode()) console.stdout.writeLine("debug build")
```

`debug_mode()` 是标准库的零参数查询，让库代码区分两种模式；模式事实由编译器传递并进入产物与缓存身份，库不自己读环境或命令行。先在 debug 下把索引与边界跑对，再用 release 测真实开销。

!!! warning "常见坑：release 下越界不再报错"
    debug 里越界会抛异常，`--release` 下同样的代码却照跑，结果甚至离谱——安全检查已被去掉，越界成了未定义行为。别用 release 来暴露边界错误；先在 debug 下跑对，再切 release 测性能。

## 属性是合同，不是性能开关

性能相关的属性写在声明或表达式位置上。它们不改变类型或运行期语义，要么给编译器一个受信任的合同，要么给检查器一份预算。

??? question "先猜：给一个函数加上 `@pure`，它会自动变快吗？"
    不会。`@pure` 是“我担保这次调用可以提前求值”的合同，不是优化开关；它既不会让编译器检查函数体，也不会自动把运行期调用变快。输入在编译期已知时它会要求求值并物化结果，否则照常在运行期执行。

### `@pure`：你担保这次调用可以提前求值

`@pure` 是**受信任的求值合同**：声明方允许编译器按依赖求值模型处理这次调用，在输入可静态确定时提前求值。它不是对函数体的检查，也不等于“无副作用”或“不抛错”：

```el
@pure
fn sumOfSquares(values: Number[]) {
	let total = 0
	for (let value in values) {
		total += value * value
	}
	total
}
```

显式标注后，调用所需输入全为编译期已知纯值时，这次调用必须完成编译期求值并物化结果；否则照常在运行时执行。函数里的 I/O 照常发生；抛错仍是函数结果的一种，可能抛错的调用不会因为返回值没人用就被删掉。

### `@bounded`：声明最坏情况预算

`@bounded(time: O(...), memory: O(...), sizes: {...})` 声明最坏情况预算，可覆盖函数、方法、构造器、extern 签名和 lambda。时间按最坏情况总工作量计，空间按本次调用新增的峰值存活存储计；省略的维度按 `O(n)` 检查：

```el
@bounded(time: O(n), memory: O(1))
fn maximum(values: Number[]) {
	let best = values[0]
	for (let value in values) {
		if (value > best) best = value
	}
	best
}
```

成本表达式只接受 `1`、规模变量、`log(变量)`、括号、加法和乘法；`O` 不是普通绑定。默认规模变量 `n` 是入口可用输入的总结构规模，其他变量要用 `sizes` 绑定来源，例如 `@bounded(sizes: {v: graph.vertexCount, e: graph.edgeCount}, time: O(v + e))`。

属性不改变生成代码，也不能把声明变成证明：证明不足只报 warning，标注、预算耗尽和未知调用都不算证明。

### `@optimize`：库作者的改写接口

`@optimize(using: rewrite, data: @{ ... })` 在类或函数上注册普通 EL 源码函数作为编译期改写策略。它是给库作者的接口：标准库用它做 Number 的代数分组、Array 链融合、排序与编解码重排；普通应用代码不需要写处理器。

??? note "可选 · 深入：属性与优化器的完整规则"
    **`@pure` 的边界。** `@pure` 也能标在 `class` 上，给构造、复制、移动、析构、方法和运算符提供纯性默认值；普通立即绑定可以写 `@pure let`，当前要求普通立即初始化器，它不是 `const` 的另一种写法。标注错误是语义违约，编译器按合同信任它，不会把错误标注降级成提示。

    **`@bounded` 的实现状态。** 当前证明片段只覆盖能证到常数时间与常数空间的封闭直接调用图；带循环的 `O(n)` 预算只会留下待证警告，不代表通过证明。循环、递归与类型化规模关系的完整分析仍在实现中。

    **`@optimize` 的处理器协议。** `using` 与 `data` 可以省略其中一个，但至少要有一项；`using` 必须解析到身份唯一的模块函数，可用导入别名或限定导入；只有 `data` 时仅登记可供其他策略读取的元数据。

    ```el
    import { OptimizationInput, OptimizationContext, UncheckedSyntax } from "el:optimization/index.el"

    fn keepLeft(input: OptimizationInput, context: OptimizationContext): UncheckedSyntax {
    	let expression = input.expression()
    	if (Text(expression.kindView()) == "add") return expression.child("a")
    	expression
    }

    @optimize(using: keepLeft, data: @{ rule: "keep-left" })
    @assign(mode: "copy")
    class Boxed {
    	let value: Number = 0
    }
    ```

    处理器必须恰好有两个显式标注的参数，类型是标准库协议 `OptimizationInput` 与 `OptimizationContext`，返回 `UncheckedSyntax`。它读取本次声明相关的表达式入口，用普通 EL 判断是否匹配；返回原输入表示不匹配，返回新语法则当场替换，新语法仍要经过普通类型、所有权、借用、清理与控制流检查。未知属性参数、重复注册、歧义处理器和错误签名会被定位拒绝；示例只演示接口形状，真实策略的领域等价由定义它的库负责。

    策略在编译期由共享 typed-IR 执行器执行，不运行目标程序的操作数或回调，也不获得文件、网络、时间等宿主能力；会话句柄不能作为运行期数据逃逸。注册顺序即执行顺序，没有收益投票或失败回退；运行失败、未完整发布、非法语法或结果类型改变都是编译错误。编译器不证明改写前后的数值、输出或异常时机相同。

## 默认优化：逐元素链不会物化中间数组

普通 Array 的连续逐元素调用按融合后的逐元素顺序执行，中间阶段不物化数组。`map(A).map(B)` 的顺序是 A1、B1、A2、B2、A3、B3；`filter` 拒绝后跳过后续阶段，`take` 耗尽后不再索取上游，短路阶段提前结束时上游副作用也停止。链返回时最终数组已完成，不对外引入惰性求值。

当前没有用户可写的 SIMD 内建或属性：没有 `@simd`，也没有 intrinsics 函数。用户能请求向量执行的地方是数组 `map` 的策略参数：

```el
import { normal, ordered, simd } from "el:execution/index.el"
import { NativeFloat } from "el:platform/machine/float.el"

let values = @[NativeFloat(1), NativeFloat(2)]
let transform = (value: NativeFloat): NativeFloat => value + value
let doubled = values.map(transform, policy: ordered(@[simd, normal]))
console.stdout.writeLine(doubled[0])
```

策略是不可变描述：`ordered` 按列表依次准入，第一个可用候选执行；`simd` 要求这次调用确实发出向量算术，完全标量化时拒绝；`normal` 是显式写进列表的普通顺序候选。省略 `policy` 的 `map` 仍只走普通顺序入口；`auto` 在允许集合内按估计成本挑候选，估计不是实测性能。

??? note "可选 · 深入：SIMD 准入条件与向量化写法"
    想让 `simd` 候选通过，代码要满足这些条件：

    - 接收者是默认动态 `Array`，元素类型与 `transform` 返回类型相同；定长数组、视图和自定义序列不进入加速候选，策略里要显式保留 `normal` 才能继续执行。
    - 元素是受检的原生标量，例如 `NativeFloat` 与原生定宽整数。普通 `Number`、`BitFloat`／`BitInteger` 对象当前没有受检对象桥接，加速候选会明确拒绝。
    - `transform` 是单一表达式、参数带显式标量注解、返回同一名义类型、无捕获、无自定义构造／复制／析构／字段／基类、无默认参数和参数包；表达式深度上限 64，内部后缀上限 8192 标量。
    - 原生计划要求 x64 目标、非空输入至少两个元素、总字节不超过 2147480000；奇数尾部由协调者按普通回调补算一次。
    - 没有合规向量计划时 `simd` 候选被拒绝并带原因；`ordered` 全部不可用时抛 `ExecutionNoViablePlan`，不会静默改用 CPU。

    短直线、无分支、无未知调用的逐元素表达式最容易被向量化：进入内核前一次性转成原生标量，别让 `Number` 与原生浮点混在回调里。规范不要求向量操作在源码或 IR 中紧邻，也不要求输入存放连续或逐标量浮点状态在中间步骤可观察。

## GPU：只在确实要在设备上算时

GPU 的常规入口是 `TensorDevice`：它打开设备会话，把宿主张量上传成设备驻留值，运算在设备上完成，回读是显式边界。设备缓冲、shader、队列和退役由会话管理。

```el
import { Tensor, TensorDevice } from "el:numerical-computing/index.el"
import { BitFloat } from "el:number/index.el"

let F32 = BitFloat<sign_bits: 1, fraction_bits: 23, exponent_bits: 8, exponent_bias: 127>
let Host = Tensor<element: F32>
let device = TensorDevice<element: F32>()
let left = device.fromHost(Host(@[2], @[F32(1), F32(2)]))
let right = device.fromHost(Host(@[2], @[F32(10), F32(20)]))
let total = left + right
console.stdout.writeLine(total.toHost().flat(0))
```

`TensorDevice<element: T>(deviceIndex: -1, portable: nil)` 的第一个参数选物理设备，`portable: t` 要求可移植驱动。后端由目标选择：Windows 默认 D3D11，`portable` 或显式设备索引走 Vulkan；Linux、FreeBSD、Android 用 Vulkan；macOS 用 Metal；没有适配器会明确抛错。

- `fromHost` 是同步上传；`toHost()` 是显式回读边界，`scalar()` 同样会等待并取回一个标量。设备张量在两次操作之间保持驻留，不要在每个小运算前后来回搬运。
- 存储精度用工厂参数声明，例如 `precision: "binary16"`；只接受 `binary16` 与 `bfloat16`，要求元素本身是 binary32 载体，存储 16 位、计算仍按 binary32。
- 没有匹配后端时构造会话就失败；GPU 候选在准入时检查元素格式、元素数量和设备能力，不能正确舍入的运算（例如当前的 GPU 除法）会被明确拒绝，而不是悄悄换成 CPU 或低精度实现。

??? note "可选 · 深入：GPU 的传输、内存与融合细节"
    批量或需要重叠的传输用 `fromHostAsync`：它返回一个单消费者上传对象，`event` 可等待，`wait()` 阻塞，`take()` 等待完成并接管设备缓冲；取出之后关闭上传不再影响这个张量。

    ```el
    let upload = device.fromHostAsync(Host(@[2], @[F32(1), F32(2)]))
    let resident = upload.take()
    console.stdout.writeLine(resident.toHost().flat(0))
    ```

    内存用量按 EL 会话显式持有的原生缓冲容量统计，不是整卡显存或进程内存：

    ```el
    device.resetMemoryPeaks()
    let usage = device.memoryUsage()
    console.stdout.writeLine(usage.allocatedBytes)
    console.stdout.writeLine(usage.peakAllocatedBytes)
    ```

    `GpuMemoryUsage` 还给出 `bufferCount`、`peakBufferCount`、`totalAllocatedBytes` 与 `totalAllocations`。D3D11 计入 storage 加同大小 staging，Vulkan 计实际注册的分配容量，Metal 计 `MTLBuffer.length`；三者的口径不同，不能跨平台比较，也不能当作物理显存占用。`resetMemoryPeaks()` 只重置两个峰值，不释放缓存、不等待设备。

    队列数量用 `queueCount` 查，`selectQueue(index)` 选队列，`recordEvent()` 与 `dependOn(event)` 表达跨队列依赖。设备时钟区间由 `beginTimestamp()` 返回，区间用 `end()` 收尾、用 `milliseconds()` 读取。张量本身的逐元素链可以用融合计划合并，减少中间值：

    ```el
    let plan = total.fusionPlan(inputCount: 1)
    plan.output(plan.relu(plan.binary("mul", plan.input(0), plan.input(0))))
    let fused = total.fuse(plan)
    ```

    再往下一层是类型化计算内核。`ComputeKernel` 是标准库内部的有界表达式表示（`el:execution/kernel.el`），`GpuExecution` 负责把内核准备成 shader 与缓冲绑定并分派；`el:execution/index.el` 公开 `buildKernel`、`prepareCompute` 和相关描述类型，`el:execution/graphics-processors/index.el` 公开各平台设备适配器。这一层是库作者接口：需要自定义内核时才从这里开始，普通张量程序用 `TensorDevice`。

    存储精度的片段沿用上面的 `F32`、`Host` 与 `device`：

    ```el
    let half = TensorDevice<element: F32, precision: "binary16">()
    let packed = half.fromHost(Host(@[3], @[F32(1), F32(-2), F32(3)]))
    console.stdout.writeLine(packed.storageBits)    // 16
    console.stdout.writeLine(packed.computeBits)    // 32
    ```

最后，把上面的结论收成一份清单，并附上当前实现边界。

??? note "可选 · 深入：性能友好写法清单与当前实现边界"
    - **让数据同构且连续。** `simd` 与 `gpu` 候选只对默认动态数组和原生标量生效；矩阵优先用默认列优先的密集 Tensor，需要显式线性顺序时写 `columnMajor(A)`，不要靠转置与手工复制制造中间布局。
    - **保持驻留与批处理。** 上传一次、在设备上多做几步、一次回读；需要重叠时用 `fromHostAsync` 与事件，不要在循环里反复 `fromHost`／`toHost`。
    - **把数值边界留在边界上。** 日常计算用精确 `Number`；需要机器格式或设备准入时再显式转成 `NativeFloat` 或固定 `BitFloat`（布局参数见[数值与位类型](numeric-types.md)），半精度只在带宽／存储确实重要且精度可接受时使用。
    - **测你要比较的东西。** `auto` 的成本是未测启发式，`@bounded` 的预算也不是实测耗时；设备内存用量只统计 EL 自己持有的原生缓冲。

    | 能力 | 当前状态 |
    | --- | --- |
    | `@pure` | 语言合同，标准库大量使用；显式标注是信任边界，编译器不验证副作用 |
    | `@bounded` | 只覆盖能证到常数时间的封闭调用图；循环、递归、未知调用与类型化规模关系仍报警告 |
    | `@optimize` | 表达式级策略已用于 Number、Array 链、排序与编解码；跨 let、控制流与多消费者的传播仍是规范目标 |
    | SIMD | 只有 `map(policy:)` 入口；要求 x64 原生计划与实际向量发射，没有源码级 intrinsic |
    | GPU | 张量会话覆盖 D3D11、Vulkan 与 Metal；`map` 的加速矩阵以实现文档记录的 Windows D3D11 路径为准，其他平台按适配器能力报告 |
    | 加速元素 | 仅受检原生标量；普通 `Number`、`BitFloat`／`BitInteger` 对象、f8/f16/f128 不进入当前加速计划 |

    本页按语言规范与当前标准库导出编写。设备与后端能力随发行变化：具体支持矩阵、未完成项和验收状态以实现文档和实际发行诊断为准，不要从这一页推断某个平台已经通过性能验收；设备能力与产物能否在目标环境运行同样要实测。

## 带走这三样

- 先在 debug 下跑对边界，再切 `--release` 测真实开销；release 去掉的是安全检查，越过前提就是未定义行为。
- 默认路径已经会融合逐元素链、消除复制；`@pure`／`@bounded` 是合同与预算，用错不会提速，只会误导。
- SIMD 只有 `map(policy:)` 这个入口，GPU 只有 `TensorDevice` 这条常规路径；两者都有明确的准入条件，不满足时会拒绝而不是悄悄降级。

## 下一站：[外部接口与 ABI](foreign.md)

> 如果瓶颈不在 EL 代码里，而在必须调用的原生库或设备驱动上呢？

- 主推进：[外部接口与 ABI](foreign.md)：声明外部函数、导出 C 入口，以及什么时候值得跨过这道边界。
- 想先练手：[矩阵与数值脚本](../practice/numerics.md)：用 Tensor 和 `columnMajor` 写完整脚本，再回来测性能。
- 后面会用到：[工具链](../toolchain.md)：`el build --release`、构建模式与退出码。

