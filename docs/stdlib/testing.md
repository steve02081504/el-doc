# 测试

> 给一个已经能跑的函数补第一个测试，通常只要十行。真正要学的是三件事：测试文件放哪、断言失败长什么样、以及怎么让它在 CI 里可靠地失败。

!!! abstract "🎯 读完这页，你能"
    - 给一个普通函数补上第一个 `test`，并用 `el test` 跑出退出码
    - 选出合适的断言：相等、近似、抛错，还是一组比较一起收集
    - 把测试放在项目正确的位置，让默认发现规则找到它
    - 在 CI 里用 `--full` 跑出与本地缓存无关的结果

    <span class="el-chip">⏱ 约 8 分钟</span> <span class="el-chip">前置：[文件与网络](files-network.md)</span>

`el test` 会找到项目里的测试文件，在独立的文件进程里执行它们，并按结果给出退出码。下面按“第一次补测试”的顺序走。

## 30 秒：给一个函数补上第一个测试

被测模块先是一个普通模块：

```el
// src/math.el
export fn double(value: Number) { return value * 2 }

export fn average(values: Number[]) {
	if (!values.count) throw StateError("empty input")
	let total = 0
	for (let value in values) total += value
	return total / Number(values.count)
}
```

测试文件用 `file:` 相对路径导入它，测试入口从 `el:tools/testing/index.el` 导入。`test(name, body)` 注册一个行为用例，`body` 是无参 lambda，也可以接收一个测试上下文参数：

```el
// tests/math.test.el
import { test, check } from "el:tools/testing/index.el"
import { average } from "file:../src/math.el"

test("平均值", () => {
	check.equal(average(@[1, 2, 3]), 2)
})

test("空输入被拒绝", () => {
	let empty: Number[] = @[]
	let error = check.throws(StateError, () => average(empty))
	check.equal(error.message, "empty input")
})
```

运行：

```text
el test tests/math.test.el
```

成功时退出码是 0；失败时报告会带实际值、期望值和路径。看到退出码 0，第一个测试就算补上了。

!!! example "动手 30 秒"
    把 `check.equal(average(@[1, 2, 3]), 2)` 的期望值改成 `3` 再跑。测试失败，报告里实际值与期望值都在；把 `2` 改回来，退出码回到 0。

## 测试文件放哪里，怎么被发现

测试写成普通的 `.el` 文件，放在项目 `tests/` 目录下，后缀用 `.test.el`。默认发现范围是 `tests/**/*.test.el`，不需要额外配置。

```text
my-app/
	package.eol
	src/math.el
	tests/math.test.el
```

项目配置里可以改写范围：

```eol
@{
	tests: {
		include: ["tests/**/*.test.el"],
		sources: ["src/**/*.el"],
		exclude: [],
		inputs: []
	}
}
```

- `include` 是测试文件范围，`exclude` 从中排除；
- `sources` 是源码内 `tests` 声明所在的范围；
- `inputs` 是额外参与增量判断的输入文件。

`el test` 从当前目录向上找最近的 `package.eol`/`package.eod` 来确定项目根，配置里的路径以项目根为基准。

测试文件顶层只做声明与注册：`import`、`test(...)` 调用，真正的工作放进 `body`。注册阶段结束后清单就冻结，不能在用例执行时再注册新用例。

## 断言：从 `check.equal` 开始

最基本的是 `assert(condition, reason)`，条件为假时抛 `AssertionError`。测试里更常用 `check` 提供的比较入口，失败报告会带上实际值、期望值和路径。

| 写法 | 语义 |
| --- | --- |
| `check.equal(actual, expected)` | 用 `==` 比较 |
| `check.same(actual, expected)` | 用 `===` 比较身份 |
| `check.near(actual, expected, absolute: ..., relative: ...)` | 数值近似，必须显式给容差 |
| `check.throws(ErrorType, body)` | body 必须抛该类型，返回实际错误 |
| `check.items(actual, expected)` | 逐项比较有限序列，报告首个不同下标与长度 |
| `check.collect(() => { ... })` | 聚合一组比较失败，而不是遇到第一个就停 |
| `check.snapshot(value, key: "...")` | 与审阅过的快照比较 |

```el
test("浮点结果", () => {
	check.near(0.1 + 0.2, 0.3, absolute: 0.000001, relative: 0)
})
```

默认遇到第一个断言失败就结束当前用例，执行清理后继续跑其他用例。要一次看全部比较结果时，把比较包进 `check.collect`。

## 先猜：测试文件能访问模块私有函数吗？

??? question "先猜：`tests/math.test.el` 能直接调用 `src/math.el` 里没 `export` 的函数吗？"
    不能。外部 `*.test.el` 仍然只能访问公开导出。要测内部辅助函数，就把 `tests { ... }` 写进原模块，它保留该模块的词法作用域；类内部的 `tests` 还能访问私有成员。

## 白盒：把 `tests` 块写进原模块

模块内部的辅助函数不需要为了测试而导出。在原模块里写 `tests { ... }`：

```el
// src/format.el
import { tests, test, check } from "el:tools/testing/index.el"

fn trim(value: Text) { return value.trimEndChars(" ") }

export fn tag(value: Text) { return "[" + trim(value) + "]" }

tests {
	test("内部 trim", () => {
		check.equal(trim("x  "), "x")
	})
}
```

`tests` 集合不会被生产构建选中，也不增加公开接口或实例布局。想访问类的私有字段，就把用例放进那个类的 `tests` 里。

## 多组输入用 test.each，预期错误用 check.throws

同一段逻辑要覆盖多组输入时用 `test.each`。每一行必须有稳定的 `name`，它会进入用例 ID 和报告：

```el
test.each("翻倍", @[
	@{ name: "zero", input: 0, expected: 0 },
	@{ name: "positive", input: 36, expected: 72 }
], (row) => check.equal(double(row.input), row.expected))
```

`check.throws(ErrorType, body)` 只执行一次 body，捕获匹配类型的错误并返回它；没有抛错或类型不符都算测试失败。它不吞掉框架自己的失败、取消与致命终止。

```el
test("越界下标", () => {
	let values = @[1, 2, 3]
	check.throws(RangeError, () => values[10])
})
```

编译错误不适合用运行时断言测。工具模块 `el:tools/testing/compiler.el` 提供 `compileFixture` 与配套的 `check.compiles`、`check.diagnostic`，用真实编译检查“这段源码应该被拒绝”。

```el
import { compileFixture } from "el:tools/testing/compiler.el"

test("私有访问被拒绝", () => {
	let result = compileFixture("tests/fixtures/private-denied.el")
	check.diagnostic(result, phase: "check", code: "EL.ACCESS.PRIVATE", marker: "denied")
})
```

## 运行测试：默认增量

```text
el test                        # 默认增量：只重跑受影响的文件
el test --full                 # 忽略成功记录，重跑所选行为用例
el test tests/math.test.el     # 只跑指定文件
el test --filter "tests/math.test.el::*"   # 按用例 ID 的 glob 过滤
el test --list                 # 只列出用例，不执行
el test --jobs 4               # 文件级有界并行
el test --mode release         # 用 release 构建模式
el test --bench                # 只跑基准用例
el test --allow-empty          # 允许零个用例
```

增量执行按内容与依赖记录判断，而不是时间戳：测试文件、实际依赖源码、项目配置、工具身份、构建模式与 `tests.inputs` 都参与判断。成功记录保存在项目本地的 `.el/local/test-state.eol`，不入库；失败、超时、中断与不完整执行不会登记为成功，`--full` 会忽略成功记录重新执行。零用例与过滤无匹配都返回非零，只有显式 `--allow-empty` 才放行。基准与快照更新始终实际执行，不复用旧测量值。

## 在 CI 里跑

CI 里用 `--full` 得到与上次记录无关的完整结果，并让退出码决定流水线成败：

```text
el test --full --jobs 4
```

`el test` 成功为 0，测试失败、构建失败、用例崩溃或超时都是非零（语言规范第 11 章）。CI 不要自动更新快照或基准，这两件事都应当是显式操作。需要性能数字时单独跑 `--bench`，并把机器、模式与输入规模记进报告。

## 可选 · 深入：隔离、超时与文件怎么组织

- 一个源文件配一个测试文件，命名和目录结构对齐，例如 `src/math.el` 对应 `tests/math.test.el`。
- 每个测试文件是一个隔离单位：文件内用例按注册顺序串行执行，共享该文件的模块初始化状态；依赖初始化状态的用例尽量拆到独立文件。
- 需要每条用例一个新进程时，给用例传 `TestOptions(isolation: "case")`；需要自定义超时用 `TestOptions(timeout: TimeDiff.seconds(10))`。
- 用例显式读取实时系统状态、未声明文件或外部服务时，用 `TestOptions(incremental: nil)` 关闭该文件的结果复用。
- 单条用例默认总期限 60 秒，包含夹具创建、主体、受管理任务等待和正常清理；超时会先请求取消，再终止该执行单元拥有的进程树。

!!! warning "常见坑：测试没跑、跑错或假装通过"
    - 测试文件没被发现：不在 `tests/`、后缀不是 `.test.el`，或命令跑在了错误的项目根。
    - 用例注册在 `body` 里：清单在注册阶段后冻结，运行时注册不生效。
    - CI 里“通过”只是因为缓存：用 `--full`，别依赖 `.el/local/test-state.eol`。
    - 零用例返回 0：默认不是这样，零用例与过滤无匹配都返回非零。

## 带走这三样

- 第一个测试只要一个导出函数、一个 `*.test.el`、一个 `check.equal`；外部测试只能碰公开导出。
- 要测私有实现就把 `tests { ... }` 写进原模块；要测“应该编译失败”用 `compileFixture` 与 `check.diagnostic`。
- 本地默认增量，CI 用 `--full`；退出码是唯一可靠的成败信号。

## 下一站：工具链

> 测试能跑了，构建、格式化、跨目标产物和发布怎么串成一条流水线？

- 主推进：[工具链](../toolchain.md)：`el` 子命令、构建模式、格式化与分发。
- 想先练手：[命令行工具](../practice/cli-tool.md)：把测试思路用在命令行程序上。
- 后面会用到：[模块与包](../language/modules.md)：`package.eol` 的 `tests` 分区与入口配置在同一张表里。
