# 外部接口与 ABI

本页按规范描述语言合同；示例仅静态核对，未进行 EL 编译或原生运行验证。

## 声明形式

| 写法 | 含义 |
| --- | --- |
| `import extern { name(parameters): Result } from "library"` | 从原生库引入带显式签名的符号 |
| `import extern name(parameters): Result from "library"` | 单个符号，可省略花括号 |
| `import extern { name } from "runtime"` | 从已验证的运行时 EIR 外部声明取得签名 |
| `export extern fn name(parameters): Result { body }` | 请求发布精确、无名字修饰的 C ABI 入口 |

原生库来源必须非空，非 `"runtime"` 来源必须逐个给出签名；不能从导出表或符号名字推断参数、返回值或位宽。`as` 只改变本地绑定名。无法写成 EL 标识符的符号可用文本字面量，此时必须指定本地别名：

```el
import extern {
	"stat$INODE64"(path: ptr, result: ptr): NativeInt as native_stat
} from "/usr/lib/libSystem.B.dylib"
```

这是声明形状示例，`NativeInt` 须另行定义为符合真实原生签名的类型；它不证明该库在当前目标存在。省略返回类型表示没有 C 结果，`: void` 也只表示无结果。

## 原生类型与布局

签名依据解析后的真实类型身份、显式 RIS 标量合同或受检布局确定表示，不按类型名字猜测 ABI。普通 `Number`、`Text`、`Array` 不会自动获得 C 标量或结构体布局。

```el
@builtin:vome:signed:integer(bits: 32) class NativeResult {}
import extern { getpid(): NativeResult } from "libc.so.6"
```

此例声明 Linux libc 的 32 位有符号结果。这里的 RIS 类属于显式底层表示协议，按 RIS-11 已具有既定布局与复制语义，不要求普通用户类的 `@assign`／`@destruct`；普通用户类仍须显式声明赋值策略。调用者仍须核对实际平台和库签名。机器整数要明确完整的有符号或无符号位宽；业务子范围不决定存储宽度。`BitInteger<bits: …>` 的布局参数也可明确位宽。`BitFloat` 只接受与目标一致、受支持的 binary32/binary64 布局。

按值对象须有明确布局；`@layout(using: function)` 选择编译期布局函数，返回字段偏移、大小与对齐计划并统一验证。没有独立的 `repr` 属性或 C 字符串布局模式。固定数组只作为明确结构体字段或指针加长度传递，不能假定 C 数组按值传递。变参须由显式声明和所选 ABI 支持，C 变参执行默认提升；未支持的类型、目标或调用方向应定位拒绝。

## ABI 描述对象与选择优先级

`@abi(descriptor)` 接收普通 EL ABI 描述对象，可放在整条 `import extern` 前作为组默认，也可放在名单中的单个函数签名前。标准库实际导出 `abi`：

```el
import { abi } from "el:foreign-functions/index.el"

@abi(abi.system)
import extern { Ping(): void } from "library.dll"
```

这是 ABI 属性位置示例，不是可直接运行的库调用。选择优先级为：单函数显式属性、所属导入组默认、模块默认、目标默认。模块默认写作 `@module(abi: descriptor)`；同一属性位置重复声明报错，普通源码 `import` 不接受原生 ABI 属性。

ABI 属性在定义的词法环境中，依赖与目标确定后各求值一次，保存不可变描述对象及其身份；别名、重导出保留选择。动态装载和符号解析可以在运行期发生，但不会重选 ABI。平台来源映射只选择库来源，不替代 ABI 属性；显式 ABI 与已验证的运行时机器声明冲突时拒绝。

ABI 描述对象最终生成统一的调用帧计划，由编译器验证布局、寄存器、栈、隐藏参数、变参和方向等约束。描述对象不能证明第三方二进制实际遵守声明。

## `ptr`、`unsafe` 与借用

`ptr` 按目标指针宽度保存原生地址，不携带所有权、有效期或解引用证明。声明指针类型、构造空指针、保存或传递已有指针，以及空指针身份比较，本身不访问存储，不因此要求 `unsafe`。裸指针解引用、未经证明的地址构造和带分配／释放／重分配属性的调用必须在 `unsafe` 中；原生调用的前提也须由调用者承担。

外部函数接收借用指针时，必须声明不留存契约，否则拒绝该借用调用：

| 参数类型 | 合同 |
| --- | --- |
| `ptr<noescape>` | 不保存所指存储供调用返回后使用 |
| `ptr<noescape_when_void: parameter>` | 指定参数可证明为缺失值 `void` 时，才提供同一承诺 |

不留存承诺不转移所有权，也不延长来源寿命。原生 buffer 的长度、容量、可写性、同步和配对释放仍由接口合同约束。未经语言入口直接篡改 EL 托管对象、类型信息或运行时内部布局属于未定义行为。

规范还定义参数侧 `@borrow`、`@transfer`、`@retain` 与返回侧 `@owned(release: ...)`、`@borrowed(owner: ...)`。这些所有权合同不能替代借用指针的不留存证明；长期存活返回的所有权不明时，必须拒绝安全包装。此处列出规范合同，不声称每种组合均已通过当前编译器验收。

## 回调与异常边界

C 错误码、空指针与错误槽是普通返回数据，不自动变成 EL 异常。包装层检查后可按自身合同抛错；EL 异常不能穿过 C ABI，桥接应以显式状态码和错误槽交付失败。

同步原生回调不能无条件改成异步签名；可能挂起的同步回调须拒绝或由调用者另写投递桥接。标准库 `el:foreign-functions/callbacks.el` 导出 `callback_address(callback)`、`callback_address_for(callback, prototype)`、`async_callback_address(callback)` 和 `release_callback(address)`：前两者分别使用默认合同和既有原生函数原型所选的 ABI，异步入口只用于拥有独立栈的原生线程或 fiber。

回调地址的分配、释放经过内存效果边界，不能把普通闭包地址直接当 C 函数指针。释放前须让原生方取消登记并等待所有在途调用返回，同时保持回调及其依赖存活；`unsafe` 不免除这些责任。

## `export extern fn` 与共享库

```el
export extern fn echo(value: ptr): ptr { return value }
```

该声明请求以精确符号 `echo` 发布独立的受检 ABI 桥；普通 `export fn` 只控制 EL 可见性，不自动进入动态符号表。入口只允许模块级、无捕获的具体函数，不能是方法、构造／析构函数、未实例化泛型，也不能有默认实参、参数包或隐式接收者。

共享库合同还要求显式出口表、映像调用租约、线程上下文与根的登记恢复，以及异常的状态／错误槽桥接。关闭与卸载必须等待在途入口返回，不能仅凭函数返回了地址就推定地址可长期使用。声明合法、成功生成产物和宿主成功装载调用是不同验证阶段；本页未进行 EL 编译、共享库生成或宿主运行。

## 常见错误

| 现象或误用 | 应检查的合同 |
| --- | --- |
| 用普通 `Number` 代替 C `int` | 显式转换到与真实签名一致的机器标量，核对位宽与范围 |
| 只换库路径就假定 ABI 自动适配 | 来源选择与 ABI 选择独立，核对目标、签名及描述对象 |
| 传入临时借用指针却没有不留存契约 | 声明并满足 `noescape` 或条件契约，保证所有者覆盖调用期 |
| 释放跳板后原生方继续回调 | 先取消登记、排空在途调用，再释放 |
| 把 `export fn` 当作 C 符号导出 | 使用 `export extern fn` 并分别验证共享库产物与宿主调用 |

## 规范出处与相关条目

- [语法标准 12.4.4](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)：外部声明、符号别名、来源和标量签名。
- [执行模型 FFI-1 至 FFI-10](https://github.com/steve02081504/el/blob/master/docs/spec/07-execution-model.md)：ABI、布局、所有权、回调和异常边界。
- [核心语义 MEM-19 至 MEM-22](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)：指针、内存效果与借用不留存契约。
- [RIS 实施契约 RIS-11](https://github.com/steve02081504/el/blob/master/docs/spec/14-ris-contract.md)：底层表示声明与赋值策略属性的例外。
- [对象与类型 LAYOUT 规则](https://github.com/steve02081504/el/blob/master/docs/spec/05-objects-and-types.md)：编译期布局计划与验证。
- [原生函数导出与共享库](https://github.com/steve02081504/el/blob/master/docs/spec/native-libraries.md)：出口、生命周期与失败合同。
- [模块与导入](modules.md)、[类型](types.md)、[外部接口教程](../../language/foreign.md)。
