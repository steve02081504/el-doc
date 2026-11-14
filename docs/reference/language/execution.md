# 异常、效果与并发

| 需要做什么 | 写法 | 关键边界 |
| --- | --- | --- |
| 抛出、处理错误 | `throw error`、`catch (error: Error)` | 按类型从上到下选择第一个匹配的处理器 |
| 捕获任意异常值 | `catch (error)` 或 `catch { ... }` | 包括 `nil`、`void`；兜底处理器必须最后写 |
| 无论如何都清理 | `try { ... } finally { ... }` | 正常完成、异常和控制退出都经过必要清理 |
| 启动独立任务 | `spawn(() => expression)` | 立即返回 Promise，不等待任务完成 |
| 等待任务结果 | `promise.get()` | 成功返回值，失败抛出保存的异常 |
| 使用块形式启动与等待 | `async { ... }`、`await(promise)` | 标准库宏，分别生成启动和一次 `.get()` 调用 |
| 约束效果与调度 | `@effects(Family)`、`@sequence(Family)` | 副作用求值顺序与异步串行调度是两套独立约束 |

!!! note "验证边界"
    本页按语言规范和标准库声明静态核对；示例未编译、未执行。规范中的调度、取消、线程安全和清理合同不代表各目标后端均已通过运行验收。

## 捕获按源码顺序匹配异常类型

`throw` 可以抛出普通值；标准库错误通常继承 `Error`。带类型的 `catch` 匹配指定类及其子类，多个处理器按源码顺序检查，只进入第一个匹配者。因此应将需要单独处理的子类放在基类之前。

下面是完整的错误分类示例。缺少库存记录与负库存分别走不同处理分支；每次调用还执行一次 `finally` 中的记录。

```el
import { Error, StateError, RangeError } from "el:errors/"

fn checkedStock(stock) {
	if (stock is void_t) throw StateError("stock record missing")
	if (stock < 0) throw RangeError()
	return stock
}

fn showStock(stock) {
	try {
		console.stdout.writeLine("stock: ", checkedStock(stock))
	} catch (error: StateError) {
		console.stdout.writeLine("stock record unavailable")
	} catch (error: Error) {
		console.stdout.writeLine("invalid stock")
	} finally {
		console.stdout.writeLine("stock check finished")
	}
}

showStock(void)
showStock(-1)
showStock(12)
```

按合同，三次检查分别报告记录缺失、库存无效、库存为 12；每次最后都有 `stock check finished`。这只是静态推导的结果。

`catch (error: Error)` 不捕获所有异常值。需要接收任意载荷时，用 `catch (error)`，它等价于 `catch (error: any)`；不需要载荷时用 `catch { ... }`。这三种形式都必须位于最后。绑定只在对应处理体内可见，额外的错误码或值条件在处理体内部检查。

未匹配的异常保持原载荷向外传播。处理体再次执行 `throw error`，或抛出另一个错误时，由外层处理器接收，不会继续尝试同一 `try` 的后续 `catch`。函数只有在所有异常都被完全处理，而且处理体及必要清理也不抛错时，才能推断为对外不抛。

## `try` 可以产生值，`finally` 负责清理

`try` 是表达式：正常完成时取保护块的末尾结果；异常被处理时取实际执行的处理块结果。空块或无值末尾产生 `void`，不返回的分支不参与结果类型合并。`finally` 正常完成时，其普通结果被丢弃，不替换此前结果。

下面是完整的局部语义示例，用默认库存 0 处理记录缺失，并说明清理块中的 `99` 不成为查询结果。

```el
import { StateError } from "el:errors/"

let stock = try {
	throw StateError("stock record missing")
} catch (error: StateError) {
	0
} finally {
	99
}
console.stdout.writeLine(stock)
```

按合同，`stock` 为 0。正常离开、`return`、循环跳转、异常和取消都遵守统一清理规则；不要把 `finally` 中的新控制转移当作稳定的结果覆盖技巧，尤其跨层返回已有单独的控制边界限制。

资源可以用普通函数包装：在 `try` 中调用业务回调，在 `finally` 中调用资源的 `close()`。若 `close()` 挂起，普通调用会等待它完成；无需增加 `await` 关键字。实际资源的关闭后可用操作及错误应查对应 API。

清理也可能失败。析构主体失败后，仍要继续清理存活字段与基类；聚合错误用 `cause` 保存原始错误，用 `errors` 按清理启动顺序保存子错误，不按完成先后排序。构造失败只清理已完成构造且仍存活的部分，不向调用者交付半成品。异步清理没有隐式超时，必要清理完成前必须保留所需存储；显式强制退出进程则不保证清理完成。

## `Error` 保留错误来源与构建栈

`Error` 包含 `name`、`message`，以及可选源码位置、建议、参考链接与 `cause`；`errors` 默认是空数组。缺失的辅助字段为 `void`，而 `cause` 可以合法保存 `nil`。系统错误还需保留平台及原始系统错误码，不能仅凭数字推测跨平台含义。

栈在构建 `Error` 时捕获，复制、捕获绑定、重抛和异步交付保留原栈。重新构造包装错误会获得自己的构建栈，可通过 `cause` 保留原错误。捕获失败或资源不足时允许缺失或截断，但不能用伪造的完整空栈掩盖状态；普通非 `Error` 异常值也不会被强制包装。

栈踪展示的是可用执行信息。尾调用、内联及其他优化可能改变可见帧；物理帧、内联来源与逻辑异步边界需要区分，不能据帧数还原完整源码调用历史。

## 普通调用等待，独立任务需要显式启动

函数的异步属性沿实际调用自动推断。普通调用异步函数会等待该次调用结束；返回值如果恰好是 Promise，不会被递归展开。保存、传参或返回 Promise 都不触发等待，调用 `.get()` 才读取其结果。

下面是完整的并发计算示例。两个任务都在第一次等待前启动，等待点同时构成接收任务错误的边界。

```el
import { spawn } from "el:concurrency/"

let paperCost = spawn(() => 120 * 3)
let bindingCost = spawn(() => 120 * 2)
try {
	let totalCost = paperCost.get() + bindingCost.get()
	console.stdout.writeLine("total cost: ", totalCost)
} catch (error) {
	console.stdout.writeLine("cost calculation failed")
}
```

按合同，成功时总费用为 600。允许并发不保证两个任务在同一时刻运行；普通表达式中的数据依赖和等待规则仍然有效。某个 `.get()` 抛错也不会自动取消另一个任务。

`async` 与 `await` 从 `el:concurrency/` 具名导入。`async { return expression }` 把块交给 `spawn`，`await(promise)` 只生成一次 `promise.get()`；它们不是语言关键字，也不改变普通调用的自动等待合同。

多个等待者可以读取同一个 Promise。任务成功结果（包括 `void`）完成 Promise，未处理异常使其失败；`.get()` 在失败时抛出保存的载荷。只在启动操作外包一层 `try`，不能接住任务后来发生的错误，应把等待或错误接收边界放在实际读取结果的位置。

## 组合等待不自动取消其余任务

标准库的组合函数监听输入 Promise 并返回新的 Promise，不依次等待每个输入。

| 组合函数 | 成功与失败规则 | 空输入 |
| --- | --- | --- |
| `all` | 按输入位置收集全部成功值；首个失败使组合失败 | 立即成功，结果为空数组 |
| `race` | 接受首个完成，无论成功或失败 | 保持未完成 |
| `any` | 接受首个成功；全部失败时聚合错误 | 立即失败，错误集合为空 |

组合完成不取消尚未完成的输入任务。若业务只需要一个结果，其余活动的取消、等待和资源释放仍需显式管理。聚合错误按输入位置排列。

## 取消是协作式请求，作用域结束不等于取消

取消在自动等待的挂起点或显式检查点交付 `Cancelled`，随后执行 `finally` 与必要析构。清理期间暂缓重复取消；取消状态仍然持久，捕获后在下一普通检查点会再次抛出。没有等待或检查点的计算循环可能一直不响应取消。

普通父任务完成或局部作用域结束不会自动取消已启动子任务。顶层结束后，进程等待已启动活动自然结束；无限活动会使进程继续运行。候选模块初始化失败时取消其拥有活动并等待清理，是模块失败的专门合同，不能推广到所有作用域。

无人接收的后台失败交给可配置的未处理错误 hook；默认报告错误，其他活动继续，最终退出码非零。已登记的 `.get()` 或错误监听者接管错误，不能把丢弃 Promise 当作忽略失败的可靠方式。

## 副作用族决定求值约束，调度族不代替锁

`@effects(Family, ...)` 使用类身份标记副作用族。同族副作用在普通操作数和实参中按源码从左到右发生；没有同族约束时，求值顺序未定义，但数据依赖、短路、异常和析构仍限制合法执行。这种自由不自动授权多线程运行。

`@sequence(Family, ...)` 约束异步操作在同一调度上下文中的串行执行；族集合有交集就冲突，普通嵌套调用复用同一操作身份，不等待自身。`@parallel` 表示允许并发，不能抹掉实际调用继承的顺序族。

两类集合独立，同一个类可以分别用作两类标识。默认独立任务具有独立调度上下文，因此“同族”不是跨任务或进程级互斥。共享可变状态仍需 Atomic、显式异步锁或受检查的同步合同；共享赋值、引用计数和 `@sync` 都不能单独证明线程安全。

## 核对依据与相关条目

- [函数](functions.md)、[控制流](control-flow.md)：调用与控制退出。
- [执行模型规范](https://github.com/steve02081504/el/blob/master/docs/spec/07-execution-model.md)：异常、Promise、取消、族与跨任务共享合同。
- [函数与生命周期规范](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)：异常推断、清理与析构失败。
- [语法规范](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)：`try`、多个 `catch` 与表达式结果。
- [Promise 源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/promises.el)、[异步宏源码](https://github.com/steve02081504/el/blob/master/src/stdlib/concurrency/async.el)：实际导出与等待接口。
- [Error 源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/error.el)：错误字段、构建栈与格式化边界。
