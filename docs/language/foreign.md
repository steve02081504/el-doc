# 外部接口与 ABI

> 在 EL 里不能直接写 `getpid()`：得先声明它的签名，再用 `unsafe` 划出原生边界。

!!! abstract "🎯 读完这页，你能"
    - 判断什么时候真的需要 `import extern`，什么时候标准库够用
    - 声明一个 libc 函数并调用，说清为什么参数和结果要换成原生整数
    - 认出 `export extern fn`、回调与 ABI 最容易错的地方

    <span class="el-chip">⏱ 约 18 分钟</span> <span class="el-chip">前置：[数值与位类型](numeric-types.md)、[函数与闭包](functions.md)</span>

这页可以跳过。只有要接原生库、导出 C 入口，或把 EL 函数交给 C 调用时才需要。

按声明形式、ABI 优先级或借用合同查询，见[外部接口与 ABI 参考](../reference/language/foreign.md)。

## 最小的一步：声明并调用 `getpid`

普通 EL 代码不直接读机器内存：`import extern` 描述库、符号名和参数形状，调用点用 `unsafe { ... }` 标出原生边界。导入不调用声明的函数，但可能加载动态库并解析符号；块内导入在执行到该位置时完成这些动作，库不可用或符号缺失可在此处抛 `ImportError`。

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

`Pid` 是本文件声明的 RIS 原生整数类，`bits: 32` 把它的机器宽度固定为 32 位；`Integer(...)` 把它转成目标最快整数，`Number(...)` 再转成普通 `Number` 供输出。普通 `Number` 是精确值，没有固定位宽，不能直接充当 C 的整数参数或返回值；标准库平台模块也会导出具名的同类本机整数类型，这里就地声明是为了让宽度与符号一眼可见。

`unsafe` 不是“关掉检查”：它只表示这段代码接受原生侧的前提（地址有效、签名一致、资源配对释放），语言仍然检查类型、生命周期与清理。

??? question "先猜：为什么不直接写 `let pid = getpid()`？"
    因为 EL 不按名字猜原生函数：库身份、符号名和参数形状都要显式声明；C 的整数也没有固定位宽，调用还要放进 `unsafe`。

## `import extern` 只声明，不调用

整组导入与单个导入是同一入口的两种写法：

```el
@builtin:vome:unsigned:integer(bits: 64) class Size {}
@builtin:vome:signed:integer(bits: 32) class Pid {}
import extern {
	strlen(text: ptr): Size as native_strlen,
	getpid(): Pid as native_getpid
} from "libc.so.6"
```

单个符号可以省略花括号；无法写成 EL 标识符的原生符号用文本字面量写名字，并必须用 `as` 给出本地绑定，例如 `import extern { "stat$INODE64"(path: ptr, result: ptr): NativeInt as native_stat } from "/usr/lib/libSystem.B.dylib"`。`as` 只改本地绑定名，不改变真实符号。

签名本身有几条硬规则：参数和结果可以是 `ptr`、位宽明确的 RIS 标量，或布局已由 `@layout` 受检确定的记录；外部整数必须来自完整位宽的有符号或无符号 8／16／32／64 位类型（或 `BitInteger<bits: …>` 的布局参数），普通 `Number` 的业务子范围不决定 ABI 宽度。返回类型可以省略，省略表示这个 C 函数没有结果；`: void` 也只作返回类型，不表示一个可用的值。

调用 C 返回的错误码是普通返回值，不是 EL 异常。反过来，EL 的语言异常不能穿过 C ABI：如果包装函数要抛错，它必须自己在调用后检查返回码、错误槽或空指针，再决定 `throw`。

## `export extern fn`：把 EL 函数发布成 C 符号

需要让 C 宿主按名字找到并调用你写的 EL 函数时，用 `export extern fn`；只在 EL 模块之间共享函数时，用普通 `export fn`。前者把模块级函数发布为精确、无名字修饰的 C 符号，与 EL 可见性是两种承诺。

```el
export extern fn echo(value: ptr): ptr { return value }
```

这条声明会以精确符号 `echo` 发布，函数体仍是普通 EL，参数与结果经过独立的受检 ABI 桥。

导出的函数若抛出语言异常，不能直接越过 C 边界：编译器为导出生成 checked 伴随入口，用状态码与错误槽报告失败；宿主读取状态或错误句柄后自行释放。`__el_` 前缀为伴随符号保留。

!!! note "实现状态"
    共享库产物的源码接线与 Windows x64 PE 路径已经存在，但现有实施记录明确不声称已经生成并加载过可用的 EL DLL；Windows x86、ARM64 与 ELF／Mach-O 共享库产物仍是独立工作。普通 EL 模块与操作系统动态库也不能与这个产物混为一谈。

导出侧的更多运行时细节，展开下面这一节。

??? note "可选 · 深入：导出入口的限制与运行时上下文"
    这条声明按共享库产物合同以精确符号 `echo` 发布：不能把内部闭包、隐藏的 lease／error 参数或托管对象地址直接贴上这个符号。产物只公开显式出口表里列出的符号，未列出的内部 helper 即使可达也不进入动态符号表；符号名必须非空、无 NUL 并满足目标格式。

    导出的函数若抛出语言异常，不能直接越过 C 边界：编译器为导出生成 checked 伴随入口，用状态码与错误槽报告失败；原始 C 入口还需要构建方为每个符号提供显式失败值，宿主读取状态或错误句柄后自行释放。`__el_` 前缀为伴随符号保留。

    限制来自入口的性质：只能声明模块级、无捕获的具体函数；不允许方法、构造器、析构器、未实例化泛型、默认实参、参数包或隐式接收者。签名按声明模块中的真实类型身份解析，`ptr` 按目标指针宽度传递，固定 RIS 数值按显式位宽与符号解释，普通 `Number`／`Text`／`Array` 不会因为跨了边界就获得 C 布局。

    运行时按每次入口管理租约与线程上下文：先取得映像调用租约，再附着或借用当前线程的 runtime 上下文，在任何分配与安全点之前登记输入、返回值、错误与租约根，返回或失败时恢复原上下文与根。通用入口不把调用自动搬到专属线程；Windows 上还要保留并恢复调用者的 last-error，TLS 恢复失败不能声明为已恢复。宿主停止派发并等待所有在途入口实际返回之后，才能运行关闭与卸载。

## ABI：默认通常够用，需要时再选

整条链路分三层：源码里的 `import extern` 声明形状，ABI 描述对象与目标事实选择实际约定，最后生成受检的调用帧计划交给后端。普通情况不需要写选择：未写任何 ABI 属性时使用目标默认，Windows x64 用 Microsoft x64 C ABI，Linux x64 用 System V AMD64 约定。

需要覆盖时，`@abi(descriptor)` 可以加在整条 `import extern` 上作为组默认，也可以加在单个函数签名前覆盖组默认；模块级默认写 `@module(abi: descriptor)`。优先级是单函数显式属性、组默认、模块默认、目标默认，重复声明同一位置会报错。

```el
@abi(abi.system)
import extern { Ping(): void } from @{ windows-x64: "https://cdn/a.dll"; linux-x64: "./a.so" }
```

平台映射只决定取哪个来源；`@abi(abi.system)` 选择当前系统后端的 ABI 对象，未命中会在编译期报错、不静默回落。ABI 在编译期选定并随声明保存；运行期动态加载只决定符号地址，不会重选 ABI，也不能从符号名猜签名。

标准库把 ABI 描述对象放在外部接口模块里：`abi.system`、`abi.windows64`、`abi.sysv.amd64`、`abi.x86.cdecl` 等，以及按目标事实选择的 `abi.forTarget(facts)`。调用方选对描述对象并给出正确签名即可；布局、方向或目标能力不匹配时会拒绝，而不是退回默认约定。

## 回调：地址可以交给 C，生命周期不能

把 EL 函数交给 C 调用，不能把闭包或托管对象的地址当成 C 函数指针。标准库提供回调跳板：`callback_address(callback)` 为同步回调生成真实地址，`release_callback(address)` 在所有原生调用返回后释放；`async_callback_address` 用于原生创建、拥有独立栈的线程或 fiber 入口。这些入口都要求 `unsafe`，因为分配与释放属于原生资源。

在 Linux x64 上用 libc `qsort` 排序两个整数（Windows 换 `msvcrt.dll`）；回调只读指针里的机器整数，不保存指针：

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

`release_callback` 只能在所有在途原生调用都返回、且原生方已取消登记之后调用，否则会释放仍在使用的跳板。回调不能保存传入的借用指针，也不能假定同步回调可以挂起；桥接若可能挂起会被编译拒绝，需另写投递型桥接。回调里的 EL 异常不能越过 C ABI；同步回调在调用者线程借用当前运行时上下文，原生创建独立栈的线程或 fiber 入口用 `async_callback_address`。

需要把登记、取消和排空包成对象时用 `CallbackHandle`；按完整签名生成原生函数类型用 `NativeFunction`；动态装载走 `el:operating-system/libraries.el`，裸地址要变成受检签名才能调用。

## 指针与布局：`unsafe` 只接受前提

`ptr` 是原生指针的显式类型：按目标指针宽度传递，保存地址但不提供所有权、有效期或解引用证明。声明 `ptr`、构造空指针、传递或比较已有指针不访问存储，不要求 `unsafe`；解引用、未经证明的偏移和带分配／释放属性的原生调用必须在 `unsafe` 中，越界写与失效指针仍是未定义行为。

原生函数接收借用指针时，必须声明它不会留存指针的参数契约，例如 `ptr<noescape>`；这个承诺不转移所有权，也不延长来源寿命。

按值传给原生的记录／结构体必须有已验证布局。`@layout(using: function)` 在编译期返回字段偏移、大小与对齐的计划并统一验证。

!!! warning "常见坑：把 C 的规则直接搬过来"
    **现象：** C 函数返回 `-1`，程序却照常往下跑。**原因：** C 错误码是普通返回值，不是 EL 异常。**改法：** 在包装层检查返回码、错误槽或空指针，再决定是否 `throw`。

    **现象：** 把普通 `Number` 直接传给 C 的 `int` 参数被拒绝。**原因：** `Number` 没有固定位宽；**改法：** 用声明过的 RIS 整数类型转换，宽度跟 C 签名一致。

    **现象：** 回调返回后程序崩溃。**原因：** 跳板被释放后原生方还可能调用它；**改法：** 等所有在途调用返回、原生方取消登记之后才 `release_callback`。

签名和布局的完整规则，展开下面这一节。

??? note "可选 · 深入：签名的完整规则、ABI 描述对象与表示"
    **签名规则补充。** 用户关心的库身份来自 `from` 后面的来源，不能按符号名猜库；同名符号的机器 ABI 必须一致，冲突声明直接诊断。外部浮点只接受与目标一致的 binary32／binary64 布局。来自 `"runtime"` 的导入可以省略签名，形状取自运行时已验证的外部声明；其它来源必须逐个写签名。单个签名前可以堆叠适用于外部函数的声明属性；没有签名的名单条目不能挂逐函数属性。返回类型写 `: Never` 表示外部实现被信任为不返回：它若正常返回就违反合同；编译器不按符号名猜这一事实。

    **目标事实。** `TargetFacts(target, addressUnitBits, pointerBits, littleEndian = t)` 检查目标、地址单元位宽、指针位宽和字节序；当前编码器要求八位地址单元与小端，x86／ARM32 目标必须是 32 位指针，x64／AArch64 目标必须是 64 位指针，否则构造时直接抛错。`abi.forTarget` 只按这些事实返回具体对象，不猜 ARM 的浮点变体。

    ```el
    import { abi, TargetFacts, AbiTarget } from "el:foreign-functions/index.el"

    let facts = TargetFacts(AbiTarget.WindowsX64, 8, 64)
    let descriptor = abi.forTarget(facts)
    ```

    **ABI 选择的边界。** `AbiDescriptor.plan(signature, facts)` 把 `ForeignSignature` 变成 `CallFramePlan`，检查类型布局、参数与返回的碎片、寄存器与栈位置、栈清理、变参边界、调用方向和目标能力；寄存器、栈偏移这些机器细节属于编译器与后端，不是用户要手写的 API。描述对象本身也是普通 EL 值：`AbiDescriptor(...)` 可以配允许域、参数规则、清理、分类函数或完整 planner；`with` 生成保留来源的新对象，只替换明确槽位，不用覆盖顺序解决冲突。分类函数可以委托基础分类器，完整 planner 必须返回类型化计划，编译器仍会验证布局、参数碎片、栈清理、变参与方向，不会因为写了 `pure`、换了名字或换了库路径就放行。`@abi` 在规范的产生式里属于 `import extern` 属性的位置；`export extern fn` 没有对应的逐函数 ABI 属性，导出侧的约定由目标与产物选择，不要照搬导入侧的写法。

    当前 ABI 规划与目标对象生成覆盖 x86、ARM 等对象文件，但这些对象文件是给对应目标链接器用的；当前 x64 EL 进程不加载也不用它们执行 x86／ARM 代码。显式 `@abi` 的语法与描述对象已在规范与标准库中给出，但标准库源码目前主要依赖目标默认，没有找到使用 `@abi` 的内建用例，具体组合仍应以目标与产物验收为准。

    **`CallbackHandle` 的形状。** 它的构造接收回调、原生函数原型、外部取消订阅函数和排空函数，`.address` 给出注册地址，`.close()` 依次取消订阅、排空在途回调、释放跳板；析构时若关闭失败会走 trap，而不是假装已释放。取消订阅与排空属于外部注册协议，必须由原生方提供，EL 内部计数器不能证明跳板已经没人使用。

    ```text
    CallbackHandle(callback, prototype, unsubscribe, drain, owner?)
    	.address   注册地址，close 前有效
    	.close()   取消订阅 → 排空在途回调 → 释放跳板
    ```

    **`NativeFunction` 与动态装载。** `NativeFunction(signature)` 是按完整函数签名生成的类型工厂，生成类的实例用真实原生函数值构造，保存地址与经编译器检查的 ABI 身份，并暴露 `.callable`、`.abiIdentity`、`.address`。它不接受无类型地址，也不能按名字重建 ABI；从动态装载拿到的裸地址只是地址，调用它仍要通过受检函数类型或对应的原生调用原语。

    动态装载走 `el:operating-system/libraries.el`：`open_library(name)` 每次成功打开拥有一份原生加载器引用，`library_symbol(handle, name)` 取到的符号地址借用该引用，`close_library(handle)` 关闭之后地址失效（关闭失败时所有权仍留给调用方）；`can_inspect_libraries()` 查询平台是否支持只读查看导出。Linux 与 Windows 各有实现，其它宿主会拒绝检查入口。

    规范还定义了 `@borrow`、`@transfer`、`@retain` 以及返回侧的 `@owned(release: ...)`／`@borrowed(owner: ...)` 所有权声明；本文没有找到这些属性的内建使用实例，实际写库时以当前编译器接受的签名检查为准。

    `@layout` 没有 `repr`、C mode 或字符串模式，ABI 消费这份布局而不是重排源码类型。`ptr<noescape_when_void: p>` 只在指定参数 `p` 可以证明为缺失值 `void` 时提供同一不留存承诺。`@representation` 讲的是受审计的逻辑模型，不是 C 布局，也不能替代 ABI、布局或证明。

    `@layout` 的用法示例：

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

    `@representation(model: ..., trusted: "...")` 把原生类或函数绑定到逻辑模型；类模型须是闭合数据类型，函数模型须符合由原签名投影出的完整 Π，报告会记录它的源内容与依赖。

??? note "可选 · 深入：安全清单与实现边界"
    - 原生调用、带内存属性函数的调用与裸指针访问放进 `unsafe`；块外出现会给出带位置的编译错误。
    - C 的错误码、空指针与错误槽是返回值，不是 EL 异常；包装层先检查再 `throw`。
    - EL 异常、清理异常与回调里的异常都不得越过 C ABI；反向入口用显式状态与错误槽交付失败。
    - 不接受无签名、未知目标或未实现方向的“默认 ABI”，宁可定位拒绝。
    - 不把托管对象、闭包或内部运行时布局的地址交给原生侧；回调用受检跳板与显式释放。
    - 所有借用指针都要有 `noescape` 或等价的参数契约；未知所有权拒绝包装。

    当前整程序编译器、动态库宿主与带托管环境的 `NativeFunction`／`CallbackHandle` 限 Windows x64 与 Linux x64；原生调用在现有测试中覆盖 libc 与 kernel32 的声明、装载、符号解析与简单回调。x86／ARM 的 ABI 帧规划与目标文件生成是另一层能力，不能从 x64 的支持推导它们能在当前进程里加载执行。`export extern fn` 的语法、检查与 Windows x64 共享库产物路径已在实施记录中接线，但不要据此断言已经生成过可加载的 EL DLL；宿主验收、重复装载／卸载、跨线程重入与错误注入仍属后续边界。`@representation` 与 `@layout` 是受检的声明能力，不是“运行期自动适配”的承诺。

## 带走这三样

- 原生调用要先 `import extern` 声明签名，再放进 `unsafe`；C 错误码是返回值，EL 异常不能穿过 C ABI。
- `export extern fn` 只发布模块级、无捕获的具体函数；导出侧要处理状态码与错误槽。
- 回调要用受检跳板并显式释放；`ptr` 不提供有效期，回调用 `noescape`，按值传结构体要有 `@layout`。

## 下一站：[标准库总览](../stdlib/index.md)

> 原生边界的规则这么细，日常要用的文件、网络、文本这些能力，标准库已经包好了吗？

- 主推进：[标准库总览](../stdlib/index.md)：看标准库把哪些系统能力包成了可直接调用的模块。
- 想先对照：[规范与实现边界](../appendix/implementation-status.md)：区分规范写法与当前发行版的落地程度。
- 后面会用到：[错误处理与异步](errors-async.md)：异常与回调之间的错误路径。

