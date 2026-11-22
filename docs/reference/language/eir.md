# EIR 与底层源码块

EIR 是 EL 使用的中间表示，也是需要明确表达底层操作时的源码入口。普通应用通常调用 EL 库；实现运行时、平台原语或设备访问时可使用 `eir` 块。语言合同、内部表示和目标后端的支持范围需要分别判断。

## 区分源码接口与内部表示

| 名称 | 用途与边界 |
| --- | --- |
| `eir` 源码块 | 写在 EL 函数内的底层操作，遵循语言的类型、生命周期和清理合同 |
| `.eir` 文件与 `eir-abi` | 当前运行时等使用的内部 ABI 记录；不是源码块语法，也不承诺跨编译器版本兼容 |
| 语义、通用底层和机器 EIR | 编译器设计中不同层次的表示；阶段设计不代表所有功能已实现或验收 |

原来的 `asm` 源码块已移除，没有兼容别名。内部对象 ID 和打印视图也不是稳定的公共源码格式。

## 表达式块与输入

下面是局部示意：`UnsignedInteger` 是已绑定到合适原始整数表示的类型，实际导入由使用环境提供。

```el
fn double(value: UnsignedInteger): UnsignedInteger {
	return eir (input = value): UnsignedInteger {
		result = add.wrap input, input
		ret result
	}
}
```

输入表达式按书写顺序各求值一次，然后执行块体；外围运行期值必须通过输入列表传入。操作结果是 SSA 名字，只能定义一次，使用必须受定义支配。`ret` 结束 EIR 表达式块，不退出外围函数，也不跳过外围清理。所有正常出口必须返回匹配结果类型的值；无结果时使用不带操作数的 `ret`。

操作有各自的类型，宽度或表示变化要显式转换。`pred` 是谓词类型，`i1` 不是它的别名；常量需要声明或上下文提供类型，不能假定默认是 `i64`。`add.wrap` 表示环绕加法，不承诺生成特定机器指令。

语句形式可以写回已声明的普通可写绑定：

```el
// @external value
let result: UnsignedInteger
eir (in:source=value; out:result) {
	result = copy source
}
```

输出必须在所有正常出口定义，块操作完成后才写回；输入与输出使用不同的 SSA 名字。写回仍遵守外围作用域、借用和赋值规则。

## 机器指令与设备访问

确需指定机器指令时，显式使用 `eir(mode:machine; ...)` 并声明适用的输入、输出和效果。目标与 ABI 默认来自编译目标，显式指定时必须相符。验证器检查支持的指令及相关操作数、寄存器、标志和内存合同；未知指令不会自动当作宿主汇编执行。当前实现支持的机器指令和目标有限，不能从语言合同推断任意目标已可用。

`eir(mode:opaqueFunction, target:..., abi:...)` 表达带完整函数合同的精确原始机器单元。它要求 `unsafe` 直接调用，提供者承担 ABI、地址和资源责任；精确字节合同不等于编译器证明机器代码安全。

MMIO、共享内存原子操作和屏障有不同效果：MMIO 访问不自动提供原子性、读改写或硬件排序；原子顺序也不能代替设备协议。设备地址窗口与对齐检查不证明硬件存在或访问已获授权。它们不能在编译期执行中触碰内存或设备。

## 工具与执行边界

`el eir` 处理内部 ABI EIR 输入，可选择入口、目标和输出，也提供 profile 操作；参数以 `el eir --help` 为准。插桩 profile 需要单线程执行，并由使用者收集和填入计数，命令不会自动从产物提取计数。`el debug` 以文件读取 ABI EIR，可使用显式指令、调用深度和存储预算检查执行；标准输入用于调试请求。它们消费内部记录，不是把上面的内联源码块直接保存成文件的通用接口。

编译期参考执行器与原生代码生成是不同路径。参考执行器验证模块，执行已支持的类型化操作；未授权的外部调用或尚未实现的操作在实际到达时失败。验证通过不等于所有操作都可执行，更不证明目标机器代码或设备行为已验收。

!!! note "实现状态"
    编译器源码包含 Windows x64 和 Linux x64 原生生成路径，但目标、ABI、运行时功能和完整程序覆盖须分别验证。执行器也有目标内存模型和外部能力限制；自举、完整发行及特定设备的运行不能由局部源码或测试推断。

## 核对依据

- [EIR 源码块语言合同](https://github.com/steve02081504/el/blob/master/docs/spec/20-language-targets.md#101-eir-源码块与机器合同)
- [源码块实现与机器模式限制](https://github.com/steve02081504/el/blob/master/docs/implementation/ir/source-blocks.md)
- [共享 typed-IR 执行范围](https://github.com/steve02081504/el/blob/master/docs/implementation/ir/ir-execution.md)
- [IR 与原生后端设计及状态](https://github.com/steve02081504/el/blob/master/docs/implementation/ir/ir.md)
- [工具链命令](../../toolchain.md)
