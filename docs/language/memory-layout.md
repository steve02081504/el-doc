# 内存布局与 GC 钩子

这一页讲清楚 EL 类的载荷如何排布、`@layout` 如何改写它，以及 `@builtin:vome:on:collect` 在什么时候被调用；读完你能预测常见类的字段偏移与大小、写出可验证的自定义布局，并判断哪些回收行为可以依赖。

下面的代码块按顺序放进同一个文件，后面的块继续使用前面的声明。

## 默认布局：字段顺序与对齐

每个普通类都由编译器建立一份载荷布局。显式 RIS 定宽整数、浮点和原始指针按目标宽度占位，其他普通值保留通用值表示；布局只安排载荷，生命周期头、引用计数、基类视图、动态记录等管理字节由编译器另外拥有，所以 `bytes`/`alignment` 查到的不是总分配大小。

没有 `@layout` 时，当前默认提供者 `automaticClassLayout` 调用 `compact`：把本层字段与冻结的基类区域按对齐从大到小稳定排序，同对齐保持输入顺序，再逐个向上对齐放置；整体大小向上取整到最大对齐。默认布局因此不保证声明顺序，需要固定顺序时用下一节的 `layouts(@[...])`。

字段的自然对齐来自它的表示：RIS 定宽标量用目标宽度，对齐量最多到 8；通用值用通用槽的宽度与对齐。基类区域也参与同一轮排序，默认算法可能把它放在字段之间；区域起点由外层决定，区域内部的偏移是冻结的。共享子对象由完整根单独拥有一个区域，嵌在派生类里的基类区域只包含它的独占部分。

派生类会为基类产生一个 `base` 区域，按基类载荷的 `size`/`align` 参与排序；外层规划器只决定这个区域从哪里开始，区域内部的字段偏移沿用基类结果，验证器不允许外层改写它。所以 `bytes(Derived)` 包含嵌在派生类里的基类区域；共享基类子对象由完整根另外拥有，不塞进这段载荷。`input.field(name)` 只解析本层直接字段。

`bytes`/`alignment` 是编译期折叠的布局查询：`@builtin:vome:size:of`、`@builtin:vome:align:of` 修饰只带 `(T: type)` 一个参数、无函数体的声明，结果按目标指针宽度的无符号整数落地，不产生运行期查询；参数不是类型值或布局不确定时报错。标准库的公开入口是 `sizeof`/`alignof`（`el:platform/target.el`，返回 `AllocationSize`）；下面按布局用例的写法声明本地 `bytes`/`alignment`，返回一个本地尺寸类型。

```el
import { layouts, LayoutInput, LayoutContext, LayoutPlan } from "el:language/layout/index.el"

@builtin:vome:unsigned:integer(bits: 8) class U8 {}
@builtin:vome:unsigned:integer(bits: 32) class U32 {}
@builtin:vome:unsigned:integer(bits: 64) class U64 {}
@builtin:vome:size:integer class LayoutSize {}
@builtin:vome:size:of fn bytes(T: type): LayoutSize {}
@builtin:vome:align:of fn alignment(T: type): LayoutSize {}

@assign(mode: "shared")
class CompactRecord {
	let tag: U8
	let timestamp: U64
	let flags: U8
	let count: U32
	constructor() { init this.tag(1); init this.timestamp(2); init this.flags(3); init this.count(4) }
}

console.stdout.writeLine("size: ", Number(bytes(CompactRecord)), " align: ", Number(alignment(CompactRecord)))
```

`CompactRecord` 的字段按默认算法排成 `timestamp`、`count`、`tag`、`flags`：偏移依次是 0、8、12、13，范围到 14，向上取整到 16，最大对齐是 8。因此查询结果是 16 和 8；布局行为用例对同一组字段给出同样的两个数。

!!! note "实现状态"
    规范只要求默认布局由普通源码算法完成并经同一个验证器检查，没有固定默认算法的名字；`automaticClassLayout → compact` 是当前实现的选择，跨发行版依赖具体偏移前先在目标上核对。

## 声明式布局：`@layout(using: layouts(...))`

`layouts(@["field", ...], options)` 接受完整的直接字段清单，按清单顺序排字段，再把剩余基类区域追加在后面；名字未知、重复或遗漏都诊断。选项 `align` 指定最低整体对齐，`size` 指定精确载荷大小（不得小于自然结果，且必须是 `align` 的整数倍），`fixed` 按字段名指定固定偏移；未知选项、固定偏移冲突或与顺序冲突都会诊断。

```el
@layout(using: layouts(@["tag", "payload"], @{ align: 64, fixed: @{ payload: 16 } }))
@assign(mode: "shared")
class Header {
	let tag: U8
	let payload: U64
	constructor() { init this.tag(7); init this.payload(8) }
}

console.stdout.writeLine("size: ", Number(bytes(Header)), " align: ", Number(alignment(Header)))
```

`tag` 放在 0；`payload` 固定到 16，正好落在 8 字节对齐上；范围到 24，`align: 64` 把整体对齐抬到 64，大小也取到 64。查询结果是 64 和 64，布局用例对同样的声明也期望这两个数。`@layout` 只改载荷布局，方法表、动态键表和 GC 登记不受影响。

## 自己写布局规划器

`@layout(using: function)` 接受普通编译期函数 `(LayoutInput, LayoutContext) -> LayoutPlan`。`LayoutInput.regions` 包含本层字段和冻结的基类区域，`fields`、`bases` 是其中的子集；`input.field(name)` 按名字取直接字段。`LayoutContext.plan(input)` 建一个空计划，`plan.place(region, at: offset)` 放入区域，`plan.finish(size:, align:)` 提交载荷范围；`LayoutPlan.finish` 还有可选的 `pack:` 参数。这些布局名字都由默认标准库导入提供，定义在 `el:language/layout/index.el`。

区域是本次请求独有的身份句柄，`place` 必须使用当前输入拿到的区域；拿拷贝的数值身份或内容相等的新对象冒充会被验证器当成外来区域拒绝。

```el
fn wide(input: LayoutInput, context: LayoutContext): LayoutPlan {
	let plan = context.plan(input)
	plan.place(input.field("tag"), at: 0)
	plan.place(input.field("timestamp"), at: 16)
	plan.place(input.field("flags"), at: 24)
	plan.place(input.field("count"), at: 32)
	return plan.finish(size: 128, align: 64)
}

@layout(using: wide)
@assign(mode: "shared")
class WideRecord {
	let tag: U8
	let timestamp: U64
	let flags: U8
	let count: U32
	constructor() { init this.tag(1); init this.timestamp(2); init this.flags(3); init this.count(4) }
}

console.stdout.writeLine("size: ", Number(bytes(WideRecord)), " align: ", Number(alignment(WideRecord)))
```

规划器返回后，编译器验证器会重新检查：每个区域恰好覆盖一次、偏移是目标可表示的整数、区域在提交大小内、满足自然对齐、整体对齐整除、区域之间不重叠；回调失败、清理失败、预算耗尽或返回非法结果都会诊断，不会退回另一种布局。把同一组字段全放在 0 的重叠计划会被拒绝，布局用例对它的期望错误正是 `layout regions overlap`。

`WideRecord` 查询得到 128 和 64；`timestamp` 在 16 满足 8 字节对齐，`count` 在 32 满足 4 字节对齐，四个区域互不重叠。

## packed 布局的限制

选项 `@{pack: n}` 或 `finish(..., pack: n)` 把每个区域所需的对齐上限压到 `n`：`n` 必须是目标允许的正二次幂，0（或省略）表示不限制；每个区域只要求 `min(区域对齐, n)`，整体对齐仍可能被 `align` 选项抬高。验证器会再检查 `pack` 的二次幂与所有区域的最终对齐。

packed 布局有两个硬限制：全部区域都必须是本层直接字段（没有基类子对象），并且每个字段都是固定 RIS 标量或原始指针（有符号/无符号/尺寸/偏移整数、浮点、指针）；通用值字段会被诊断 `packed layouts require fixed RIS scalar or pointer fields without base subobjects`。相关标量的读写按对齐 1 生成，管理区仍按自己的对齐单独安排。

```el
@layout(using: layouts(@["tag", "timestamp"], @{ pack: 1 }))
@assign(mode: "shared")
class PackedHeader {
	let tag: U8
	let timestamp: U64
	constructor() { init this.tag(1); init this.timestamp(2) }
}

console.stdout.writeLine("size: ", Number(bytes(PackedHeader)), " align: ", Number(alignment(PackedHeader)))
```

两个字段紧挨着排：`tag` 在 0，`timestamp` 在 1，大小 9，对齐 1。这个例子只用了固定 RIS 字段，也没有基类，满足 packed 的准入条件。

!!! note "实现状态"
    `pack` 选项在标准库与编译器里有实现（`el:language/layout/index.el` 的 `@{pack: n}` 与 `LayoutPlan.finish` 的 `pack:`，编译器做上述准入检查），但规范 LAYOUT-4 只列出 `align`、`size`、`fixed`；把它当当前实现的扩展，跨发行版前先用最小片段确认。布局行为用例没有覆盖 `pack:`，其余布局路径有覆盖。

## GC 钩子：`@builtin:vome:on:collect`

回收钩子写在类的实例方法上：`@builtin:vome:on:collect fn maintain() { ... }`。它只接受无显式参数的实例方法，不能放在模块级、静态方法、构造器或析构器上；方法名任意，编译器按声明身份登记，不按名字查找。实例完成构造后登记，析构开始前撤销，登记不强持有接收者；撤销后尚未开始的处理器会跳过。

一轮 GC 先确定可达性，再执行仍存活、可达且已登记实例的处理器：同一个处理器每轮至多一次，顺序不保证；新登记下一轮生效。处理器造成的引用变化要重新追踪后才允许清扫，所以处理器可以改字段或分配新对象，但不能依赖“本轮已经扫完”的假设。处理器同步执行、可以普通分配，不能挂起，也不能抛异常；抛异常会按协议失败处理，不会变成普通可捕获的业务异常。释放文件、锁这类显式资源的责任仍在析构器，不在回收钩子。

用 `gc_collect()` 主动请求一轮，返回值是这一轮清扫掉的受管理载荷字节数（不含分配头、引用计数单独释放的存储和仍存活对象）；没有可回收存储、或请求与进行中的回收合并时返回 0。`gc_set_threshold(n)` 设置触发安全点回收的分配欠债阈值：0 表示每个启用回收的安全点都可能请求，负值拒绝，平台启动配置的阈值优先。两者都由默认标准库导入提供，实现在 `el:memory/garbage-collection/control.el`（标准库根重导出）。

```el
gc_set_threshold(2147483647)
let rounds = 0

@assign(mode: "shared")
class Watched {
	@builtin:vome:on:collect fn maintain() { rounds += 1 }
}

let owner = Watched()
gc_collect()
console.stdout.writeLine("first round: ", rounds)
gc_collect()
console.stdout.writeLine("second round: ", rounds)
console.stdout.writeLine("alive: ", owner is Watched)
```

把阈值调得足够大是为了排除自动回收的干扰。第一次 `gc_collect()` 后 `rounds` 是 1，第二次是 2，对象一直存活；处理器是每轮存活维护，不是只跑一次的终结器。把对象放进局部作用域，对象销毁时析构器先撤销登记再执行，之后即使析构器里再 `gc_collect()` 也不会调用它。

```el
gc_set_threshold(2147483647)
let hits = 0

@assign(mode: "shared")
class Tracked {
	@builtin:vome:on:collect fn maintain() { hits += 1 }
	destructor() { gc_collect(); console.stdout.writeLine("in destructor: ", hits) }
}

{
	let local = Tracked()
	gc_collect()
	console.stdout.writeLine("in scope: ", hits, " ", local is Tracked)
}
gc_collect()
console.stdout.writeLine("after scope: ", hits)
```

第一个 `gc_collect()` 让 `hits` 变成 1；对象销毁时析构器先撤销登记再执行，所以析构器里那次 `gc_collect()` 和之后的 `gc_collect()` 都不会再增加它。`hits` 在析构器里和离开作用域后都保持 1。

模块用 `@module(gc: nil)` 关闭 GC 时，构造带回收钩子的实例会编译报错，不会静默启用 GC。

## 与 `@dynamic` 的关系

`@dynamic` 只改运行期字段的存放：类自己声明的固定字段仍有固定槽和上面算出的布局，`new` 出来的字段放在独立键表里，不改变 `bytes`/`alignment`，也不参与布局规划器的区域集合。删字段只移除引用，不等于释放资源。

## 实现状态

- 已验收：默认布局、`layouts(...)` 的 `align`/`fixed`、自定义规划器、重叠拒绝、`bytes`/`alignment` 查询由 `tests/class-layout/` 行为用例覆盖；GC 钩子的登记时机、每轮一次、重入回收、下一轮生效、析构前撤销和抛错即协议失败由行为用例覆盖。
- 仅源码依据：`layouts` 的 `size`、`pack` 选项与 `gc_set_threshold` 的阈值语义由实现或规范描述，但布局用例没有覆盖 `size`/`pack`，GC 用例只把阈值设大来抑制自动回收，没有单独断言阈值触发；跨发行版依赖前先按最小片段确认。
- 目标合同：增量标记、有界标记暂停和完整的闲置小步回收还在目标合同里；当前回收轮次仍可能以完整停机开始，不能把 `gc_collect()` 当成可抢占的小步。
- 实现扩展：`pack` 与规范 LAYOUT-4 的差距见上一节的实现状态说明。

## 继续阅读

- [类与对象](classes.md)：`@assign`、构造与析构、`@dynamic` 的完整规则。
- [值与类型](values.md)：固定位宽数值与普通 `Number` 的表示差异。
- [规范与实现边界](../appendix/implementation-status.md)：行为用例、目标合同与发行版差距。
