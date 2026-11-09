# 外部接口与 ABI

这一页讲 EL 怎么把原生 C 符号声明进来、怎么把自己的函数发布成 C 入口，以及中间的 ABI 选择与回调边界；读完你能判断什么时候该用 `import extern`、什么时候该用 `export extern fn`，并知道当前目标支持到哪一步。

## 先声明，再在 unsafe 里调用

普通 EL 代码不直接读机器内存，原生边界必须显式声明签名。`import extern` 描述外部库、符号名和参数形状，调用点用 `unsafe { ... }` 标出越过检查的边界；声明本身不是调用，不会加载库或执行代码。

以 Linux x64 的 libc 为例，最小可用的一段是：

```el
import { NativeSignedInteger as Integer } from "el:platform/machine/integer.el"
@builtin:vome:signed:integer(bits: 32) class Pid {}
import extern { getpid(): Pid } from "libc.so.6"

unsafe {
	let pid = Number(Integer(getpid()))
	console.stdout.writeLine("pid: ", pid)
}
```

`Pid` 是本文件声明的 RIS 原生整数类，`bits: 32` 把它的机器宽度固定为 32 位；`Integer(...)` 把它转成目标最快整数，`Number(...)` 再转成普通 `Number` 供输出。普通 `Number` 是精确值，没有固定位宽，不能直接充当 C 的整数参数或返回值。标准库平台模块也会导出具名的同类本机整数类型；这里就地声明，是为了让宽度与符号一眼可见。

`unsafe` 不是“关掉检查”的开关：它只表示这一段代码接受原生侧的前提（地址有效、调用签名一致、资源配对释放），语言层面仍然检查类型、生命周期与清理。

## import extern 的写法

整组导入与单个导入是同一入口的两种写法：

```el
@builtin:vome:unsigned:integer(bits: 64) class Size {}
@builtin:vome:signed:integer(bits: 32) class Pid {}
import extern {
	strlen(text: ptr): Size as native_strlen,
	getpid(): Pid as native_getpid
} from "libc.so.6"
```

单个符号可以省略花括号；无法写成 EL 标识符的原生符号用文本字面量写名字，并必须用 `as` 给出本地绑定，例如 `import extern { "stat$INODE64"(path: ptr, result: ptr): NativeInt as native_stat } from "/usr/lib/libSystem.B.dylib"`。整组写法把多个签名放在花括号里，用逗号或换行分隔；`as` 只改本地绑定名，不改变真实符号。

签名规则可以归纳成几条：

- 参数和结果可以是 `ptr`、位宽明确的 RIS 标量，或布局已由 `@layout` 受检确定的记录；外部整数必须来自完整位宽的有符号或无符号 8／16／32／64 位类型（或 `BitInteger<bits: …>` 的布局参数），普通 `Number` 的业务子范围不决定 ABI 宽度；外部浮点只接受与目标一致的 binary32／binary64 布局。
- 返回类型可以省略；省略表示这个 C 函数没有结果。`: void` 也只作返回类型，不表示一个可用的值。
- 库身份来自 `from` 后面的来源，不能按符号名猜库；同名符号的机器 ABI 必须一致，冲突声明直接诊断。
- 来自 `"runtime"` 的导入可以省略签名，形状取自运行时已验证的外部声明；其它来源必须逐个写签名。
- 单个签名前可以堆叠适用于外部函数的声明属性；没有签名的名单条目不能挂逐函数属性。
- 返回类型写 `: Never` 表示外部实现被信任为不返回：它若正常返回就违反合同；编译器不按符号名猜这一事实。

调用 C 返回的错误码是普通返回值，不是 EL 异常。反过来，EL 的语言异常不能穿过 C ABI：如果包装函数要抛错，它必须自己在调用后检查返回码、错误槽或空指针，再决定 `throw`。

## 导出 C 入口

需要让 C 宿主按名字找到并调用你写的 EL 函数时，用 `export extern fn`；只在 EL 模块之间共享函数时，用普通 `export fn`。它把一个模块级函数发布为精确、无名字修饰的 C 符号，和 EL 模块可见性是两种不同的承诺。

```el
export extern fn echo(value: ptr): ptr { return value }
```

这条声明按共享库产物合同会以精确符号 `echo` 发布，而函数体仍是普通 EL：参数与结果经过独立的受检 ABI 桥，不能把内部闭包、隐藏的 lease／error 参数或托管对象的地址直接贴上这个符号。产物只公开显式出口表里列出的符号，未列出的内部 helper 即使可达也不进入动态符号表；符号名必须非空、无 NUL 并满足目标格式。

限制来自入口的性质：只能声明模块级、无捕获的具体函数；不允许方法、构造器、析构器、未实例化泛型、默认实参、参数包或隐式接收者。签名按声明模块中的真实类型身份解析，`ptr` 按目标指针宽度传递，固定 RIS 数值按显式位宽与符号解释，普通 `Number`／`Text`／`Array` 不会因为跨了边界就获得 C 布局。

导出的函数若抛出语言异常，不能直接越过 C 边界：编译器为导出生成 checked 伴随入口，用状态码与错误槽报告失败；原始 C 入口还需要构建方为每个符号提供显式失败值，宿主读取状态或错误句柄后自行释放。`__el_` 前缀为伴随符号保留。

运行时按每次入口管理租约与线程上下文：先取得映像调用租约，再附着或借用当前线程的 runtime 上下文，在任何分配与安全点之前登记输入、返回值、错误与租约根，返回或失败时恢复原上下文与根。通用入口不把调用自动搬到专属线程；Windows 上还要保留并恢复调用者的 last-error，TLS 恢复失败不能声明为已恢复。宿主停止派发并等待所有在途入口实际返回之后，才能运行关闭与卸载。

!!! note "实现状态"
    共享库产物的源码接线与 Windows x64 PE 路径已经存在，但现有实施记录明确不声称已经生成并加载过可用的 EL DLL；Windows x86、ARM64 与 ELF／Mach-O 共享库产物仍是独立工作。普通 EL 模块与操作系统动态库也不能与这个产物混为一谈。

## ABI 选择：声明、目标事实、调用桥

整条链路分三层：源码里的 `import extern` 声明形状，ABI 描述对象与目标事实选择实际约定，最后生成受检的调用帧计划交给后端。

普通情况不需要写选择：未写任何 ABI 属性时使用目标默认，当前 Windows x64 使用 Microsoft x64 C ABI，Linux x64 使用对应的 System V AMD64 约定。需要覆盖时，`@abi(descriptor)` 可以加在整条 `import extern` 上作为组默认，也可以加在单个函数签名前覆盖组默认；模块级默认写 `@module(abi: descriptor)`。优先级是单函数显式属性、组默认、模块默认、目标默认，重复声明同一位置会报错。

规范给出的覆盖写法是：

```el
@abi(abi.system)
import extern { Ping(): void } from @{ windows-x64: "https://cdn/a.dll"; linux-x64: "./a.so" }
```

`@{ ... }` 是平台映射，只决定取哪个来源；`@abi(abi.system)` 选择当前系统后端提供的 ABI 对象。映射未命中任何键会在编译期报错，不会静默回落到某一项。ABI 选择在编译期完成并随声明保存；运行期动态加载只决定符号地址，不会重选 ABI，未知签名也不能从符号名猜出来。

标准库把 ABI 描述对象放在外部接口模块里：常见入口有 `abi.system`、`abi.windows64`、`abi.sysv.amd64`、`abi.x86.cdecl`／`stdcall`／`fastcall`、`abi.aapcs32`／`aapcs32Vfp`／`aapcs64`，以及按目标事实选择对象的 `abi.forTarget(facts)`。

```el
import { abi, TargetFacts, AbiTarget } from "el:foreign-functions/index.el"

let facts = TargetFacts(AbiTarget.WindowsX64, 8, 64)
let descriptor = abi.forTarget(facts)
```

`TargetFacts(target, addressUnitBits, pointerBits, littleEndian = t)` 检查目标、地址单元位宽、指针位宽和字节序；当前编码器要求八位地址单元与小端，x86／ARM32 目标必须是 32 位指针，x64／AArch64 目标必须是 64 位指针，否则构造时直接抛错。`abi.forTarget` 只按这些事实返回具体对象，不猜 ARM 的浮点变体。

`AbiDescriptor.plan(signature, facts)` 把 `ForeignSignature` 变成 `CallFramePlan`。计划会检查类型布局、参数与返回的碎片、寄存器与栈位置、栈清理、变参边界、调用方向和目标能力；描述对象与目标事实不匹配、签名超出支持域、或者方向不允许时都会拒绝，而不是退回默认约定。寄存器、栈偏移这些机器细节属于编译器与后端，不是用户要手写的 API；调用方只需要选对描述对象并给出正确签名。

描述对象本身也是普通 EL 值：`AbiDescriptor(...)` 可以配允许域、参数规则、清理、分类函数或完整 planner；`with` 生成保留来源的新对象，只替换明确槽位，不用覆盖顺序解决冲突。分类函数可以委托基础分类器，完整 planner 必须返回类型化计划，编译器仍会验证布局、参数碎片、栈清理、变参与方向，不会因为写了 `pure`、换了名字或换了库路径就放行。

`@abi` 在规范的产生式里属于 `import extern` 属性的位置；`export extern fn` 没有对应的逐函数 ABI 属性，导出侧的约定由目标与产物选择，不要照搬导入侧的写法。

!!! note "实现状态"
    ABI 规划与目标对象生成覆盖 x86、ARM 等对象文件，但这些对象文件是给对应目标链接器用的；当前 x64 EL 进程不加载也不用它们执行 x86／ARM 代码。显式 `@abi` 的语法与描述对象已在规范与标准库中给出，但标准库源码目前主要依赖目标默认，没有找到使用 `@abi` 的内建用例，具体组合仍应以目标与产物验收为准。

## 回调、动态装载与函数指针

把 EL 函数交给 C 调用，不能把闭包或托管对象的地址当成 C 函数指针。标准库提供回调跳板入口：`callback_address(callback)` 为同步回调生成一个真实地址，`release_callback(address)` 在所有原生调用返回后释放；`async_callback_address` 用于由原生创建、拥有独立栈的线程或 fiber 入口。这些入口都要求 `unsafe`，因为分配与释放属于原生资源。

下面的例子在 Linux x64 上用 libc `qsort` 排序两个整数（Windows 上换成 `msvcrt.dll`）；回调只读取指针里的机器整数，不保存指针：

```el
import { NativeSignedInteger as Integer } from "el:platform/machine/integer.el"
import { heap_alloc, heap_free } from "el:memory/allocation/heap.el"
import { scalar_load, scalar_store } from "el:memory/storage/raw.el"
import { callback_address, release_callback } from "el:foreign-functions/callbacks.el"

@builtin:vome:signed:integer(bits: 32) class CompareResult {}
@builtin:vome:unsigned:integer(bits: 64) class NativeSize {}
import extern {
	qsort(base: ptr<noescape>, count: NativeSize, width: NativeSize, compare: ptr<noescape>)
} from "libc.so.6"

fn compare(left: ptr, right: ptr): CompareResult {
	unsafe { return CompareResult(scalar_load(left, Integer(0)) - scalar_load(right, Integer(0))) }
}

unsafe {
	let buffer = heap_alloc(8)
	let entry = callback_address(compare)
	try {
		scalar_store(buffer, Integer(0), Integer(2))
		scalar_store(buffer, Integer(4), Integer(1))
		qsort(buffer, NativeSize(2), NativeSize(4), entry)
		console.stdout.writeLine(Number(Integer(scalar_load(buffer, Integer(0)))))
	} finally {
		release_callback(entry)
		heap_free(buffer)
	}
}
```

回调的生命周期由“原生方何时还会调用”决定：`release_callback` 只能在所有在途原生调用都返回、且原生方已经取消登记之后调用；否则会释放仍在使用的跳板。回调本身不能保存传入的借用指针，也不能假定同步回调可以挂起；桥接若可能挂起会被编译拒绝，需另写投递型桥接。回调里抛出的 EL 异常不能越过 C ABI。同步回调在调用者线程上借用当前运行时上下文，不自动切换线程；由原生创建、拥有独立栈的线程或 fiber 入口用 `async_callback_address`。

需要把回调登记、取消和排空包装成一个对象时，用 `CallbackHandle`。它的构造接收回调、原生函数原型、外部取消订阅函数和排空函数，`.address` 给出注册地址，`.close()` 依次取消订阅、排空在途回调、释放跳板；析构时若关闭失败会走 trap，而不是假装已释放。取消订阅与排空属于外部注册协议，必须由原生方提供，EL 内部计数器不能证明跳板已经没人使用。

```text
CallbackHandle(callback, prototype, unsubscribe, drain, owner?)
	.address   注册地址，close 前有效
	.close()   取消订阅 → 排空在途回调 → 释放跳板
```

`NativeFunction` 是另一个方向的边界：`NativeFunction(signature)` 是按完整函数签名生成的类型工厂，生成类的实例用真实原生函数值构造，保存地址与经编译器检查的 ABI 身份，并暴露 `.callable`、`.abiIdentity`、`.address`。它不接受无类型地址，也不能按名字重建 ABI；从动态装载拿到的裸地址只是地址，调用它仍要通过受检函数类型或对应的原生调用原语，不能按任意签名直接调用。

动态装载走 `el:operating-system/libraries.el`：`open_library(name)` 每次成功打开拥有一份原生加载器引用，`library_symbol(handle, name)` 取到的符号地址借用该引用，`close_library(handle)` 关闭之后地址失效（关闭失败时所有权仍留给调用方）；`can_inspect_libraries()` 查询平台是否支持只读查看导出。Linux 与 Windows 各有实现，其它宿主会拒绝检查入口。装载不等于调用：裸地址只是地址，要调用它仍必须先变成受检签名（例如 `NativeFunction`），不能按任意签名直接调用。

## 指针、布局与表示

`ptr` 是原生指针的显式类型：按目标指针宽度传递，保存地址但不提供所有权、有效期或解引用证明。声明 `ptr`、构造空指针、传递或比较已有指针不访问存储，因此不要求 `unsafe`；解引用、未经证明的偏移、以及调用带分配／释放属性的原生函数必须在 `unsafe` 中，越界写与失效指针仍是未定义行为。

原生函数接收借用指针时，必须声明它不会留存指针的参数契约，例如 `ptr<noescape>`；`ptr<noescape_when_void: p>` 只在指定参数 `p` 可以证明为缺失值 `void` 时提供同一承诺。这个承诺不转移所有权，也不延长来源寿命。规范还定义了 `@borrow`、`@transfer`、`@retain` 以及返回侧的 `@owned(release: ...)`／`@borrowed(owner: ...)` 所有权声明；本文没有找到这些属性的内建使用实例，实际写库时以当前编译器接受的签名检查为准。

按值传给原生的记录/结构体必须有已验证布局。EL 的入口是 `@layout(using: function)`：布局函数在编译期返回字段偏移、大小与对齐的计划，编译器统一验证；没有 `repr`、C mode 或字符串模式，ABI 消费这份布局而不是重排源码类型。

```el
import { layouts } from "el:language/layout/index.el"

@builtin:vome:unsigned:integer(bits: 8) class U8 {}
@builtin:vome:unsigned:integer(bits: 64) class U64 {}

@layout(using: layouts(@["tag", "payload"], @{ align: 64, fixed: @{ payload: 16 } }))
@assign(mode: "shared")
class Header {
	let tag: U8
	let payload: U64
	constructor() { init this.tag(7); init this.payload(8) }
}
```

`@representation` 讲的是逻辑表示，不是 C 布局：`@representation(model: ..., trusted: "...")` 把原生类或函数的实现绑定到一个逻辑模型上，作为需要审计的信任假设。它不是公理，不授权忽略原生效果或资源，也不能替代 ABI、布局或证明；类模型须是闭合数据类型，函数模型须符合由原签名投影出的完整 Π，报告会记录它的源内容与依赖。

## 安全与错误处理清单

- 原生调用、带内存属性函数的调用与裸指针访问放进 `unsafe`；块外出现会给出带位置的编译错误。
- C 的错误码、空指针与错误槽是返回值，不是 EL 异常；包装层先检查再 `throw`。
- EL 异常、清理异常与回调里的异常都不得越过 C ABI；反向入口用显式状态与错误槽交付失败。
- 不接受无签名、未知目标或未实现方向的“默认 ABI”，宁可定位拒绝。
- 不把托管对象、闭包或内部运行时布局的地址交给原生侧；回调用受检跳板与显式释放。
- 所有借用指针都要有 `noescape` 或等价的参数契约；未知所有权拒绝包装。

## 实现状态

!!! note "实现状态"
    当前整程序编译器、动态库宿主与带托管环境的 `NativeFunction`／`CallbackHandle` 限 Windows x64 与 Linux x64；原生调用在现有测试中覆盖 libc 与 kernel32 的声明、装载、符号解析与简单回调。x86／ARM 的 ABI 帧规划与目标文件生成是另一层能力，不能从 x64 的支持推导它们能在当前进程里加载执行。

!!! note "实现状态"
    `export extern fn` 的语法、检查与 Windows x64 共享库产物路径已在实施记录中接线，但不要据此断言已经生成过可加载的 EL DLL；宿主验收、重复装载／卸载、跨线程重入与错误注入仍属后续边界。`@representation` 与 `@layout` 是受检的声明能力，不是“运行期自动适配”的承诺。

## 继续阅读

- [数值与位类型](numeric-types.md)：`Number`、`BitInteger`、`BitFloat`、`NativeFloat` 各自表示什么，以及哪些位宽适合跨界。
- [错误处理与异步](errors-async.md)：异常、`try`／`finally` 与回调之间的错误路径。
- [模块与包](modules.md)：`import`／`export` 的名字绑定与来源规则。
- [规范与实现边界](../appendix/implementation-status.md)：如何区分规范写法与当前发行版的落地程度。
