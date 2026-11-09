# 安装与第一个程序

读完这一页，你能运行第一个 EL 程序、用 REPL 试写法、把项目编译成原生可执行文件，并为其他系统生成产物。

这一页假设你已经拿到 EL 的发行内容：主入口 `el`，以及同一份发行里的独立编译器 `elc`。两者共用一条编译链，`el` 自己就能运行和编译源码；`elc` 只是编译器的单独命令行入口，日常用 `el` 就够，不需要先找到或安装 `elc`。

## 确认安装

把发行包解压到一个固定目录，并将该目录加入 `PATH`。Windows 上可以在 PowerShell 里检查：

```powershell
el --help
```

Linux 和 macOS 上相同：

```sh
el --help
```

能看到子命令列表就说明安装好了。如果提示找不到命令，重新打开终端让 `PATH` 生效，或检查你加入的是不是含 `el` 可执行文件的目录。

本教程的命令在三个桌面平台上写法一致。当前发行验证以 Windows x64 与 Linux x64 为主；其他目标的支持范围以发布说明为准。

!!! tip "`el` 与 `elc` 的关系"
    `elc` 不是 `el` 的前置依赖。`el` 在发行里带着编译器源码，`el run` 和 `el build` 自己就能编译；`elc` 是同一编译器的独立可执行入口，适合外部构建脚本或排查编译链。需要直接调编译器时，`el --compile-native ...` 与 `elc --compile-native ...` 接受同一套参数，细节见[工具链](toolchain.md)。

## 第一个程序

新建 `hello.el`：

```el
// hello.el
console.stdout.writeLine("Hello, EL")
```

运行：

```sh
el run hello.el
```

输出：

```text
Hello, EL
```

三件事值得注意：

1. **没有 `main` 函数。** 模块顶层的代码就是入口，按书写顺序执行。
2. **输出走 console。** 文字用 `console.stdout.write`（不换行）或 `writeLine`（追加 LF）；结构化值用等级对象的 `.value(...)`。
3. **不需要 import `console`。** 预导入（prelude）默认提供 `console`、`Text`、`Array`、`t`/`nil`/`void`、`assert` 等基础名字。

### 写一个函数

```el
fn greet(name: Text = "world") => "hello, " + name

console.stdout.writeLine(greet())
console.stdout.writeLine(greet("Ada"))
```

`fn name(...) => expression` 是表达式体函数；不写 `return` 时返回最后一条语句的值。参数默认值在实参省略或为 `void` 时生效，`nil` 不触发默认值。

### 用循环和集合

```el
let names = @["Ada", "Grace", "Linus"]

for (let name in names) {
	console.stdout.writeLine(`hello, ${name}`)
}
```

反引号字符串支持 `${...}` 插值，从左到右求值。`@[...]` 是数组字面量；`for (let name in names)` 逐个取元素，循环体里 `name` 是当前元素的绑定。

## 运行 EL 代码

`el run ENTRY` 编译入口并立即执行。编译产物是临时文件，程序结束就删除，源码旁边不会留下可执行文件；入口写文件路径，`.el` 与 `.els` 都接受。

```sh
el run hello.el
```

项目里也一样，入口要显式写出来：

```sh
el run src/main.el
```

`el run` 不会从 `package.eol` 的 `entry` 猜入口；`entry` 是规范给项目级命令的默认入口，当前发行仍要求你给出文件路径，实际行为以 `el --help` 为准。

### 把参数传给程序

`command_arguments()` 返回完整的 `Text[]`，第 0 项是程序自身，真正的参数从索引 1 开始：

```el
// greet.el
import { command_arguments } from "el:operating-system/arguments"

let args = command_arguments()
if (args.count < 2) {
	console.stdout.writeLine("usage: greet <name>")
} else {
	console.stdout.writeLine("hello, ", args[1])
}
```

入口之后的参数原样交给程序：

```sh
el run greet.el Ada
```

`el` 自己的选项要写在入口之前；入口之后即使长得像选项也归程序：

```sh
el run --release greet.el Ada
```

上面这行里 `--release` 在入口之前，是构建模式；写成 `el run greet.el --release` 时，`--release` 会作为参数传给程序。`el run` 的退出码取自被运行的程序，编译失败时不会执行同名的旧产物。

## REPL

不想为每次试验新建文件时，用交互式会话：

```sh
el repl
```

```text
> let x = 1 + 2
> console.stdout.writeLine("x = ", x)
x = 3
> fn twice(value) => value * 2
> twice(21)
42
```

绑定和状态在同一次会话里保持。交互终端下 `Ctrl+C` 结束当前输入，空输入时退出；`Ctrl+D` 或输入流结束也会退出。非交互输入（管道、重定向）同样能驱动 REPL，读到 EOF 退出。

## 项目结构

单文件脚本可以直接运行。稍微大一点的项目用项目文件描述导入映射和测试范围。在项目根目录放 `package.eol`：

```eol
@{
	entry: "src/main.el",
	imports: {
		"app/": "./src/"
	},
	tests: {
		include: ["tests/**/*.test.el"],
		sources: ["src/**/*.el"]
	}
}
```

- `entry` 是规范约定的默认入口。当前发行里 `el run` 与 `el build` 不读它，仍要求显式入口文件。
- `imports` 把说明符前缀映射到目录；`"app/"` 开头的来源会解析到 `./src/` 下。路径相对**项目根**，不是进程的当前目录。
- `tests` 描述测试发现范围。

推荐的布局：

```text
my-app/
  package.eol
  src/
    main.el
  tests/
    main.test.el
```

模块之间的相对导入相对于**引用它的模块文件**解析，不是相对于启动时的 cwd。把每个目录的入口写成 `index.el`，就可以直接导入目录：`import /.*/ from "file:./physics"` 等价于导入 `physics/index.el`。

## 编译为可执行文件

`el build ENTRY` 只编译、不运行：

```sh
el build hello.el
```

不给输出路径时，产物写在入口旁边：文件名沿用入口名，扩展名换成宿主可执行后缀。Windows 上是 `hello.exe`，Linux 上是没有后缀的 `hello`。用 `-o`（或 `--output`）指定输出路径：

```sh
el build hello.el -o build/hello
```

`-o` 给出的名字原样使用，不会自动补后缀；扩展名也不影响目标平台。成功时 `el build` 把产物路径打印到标准输出。构建失败返回非零；同一路径上已有的旧产物会保留，不会被失败的一轮覆盖。

### debug 与 release

默认构建 debug，保留索引检查、范围检查与内部状态断言。显式选择 release：

```sh
el build hello.el --release -o build/hello
```

两种模式共用一条优化流水线，不是两套语言。release 省去的是标准库中仅用于防止违反调用前提的运行期安全检查；类型、借用、所有权和生命周期检查不会因为 release 关闭，接口明确承诺的失败也不会消失。`--debug` 与 `--release` 互斥，显式写 `--debug` 就是默认的 debug 构建。

## 为其他系统生成可执行文件

`el run` 与 `el build` 按宿主目标编译，`el build` 没有 `--target` 参数。要为其他系统生成产物，直接调用编译器入口；`el` 会把首个参数命中编译器选项的调用转发给编译器，所以下面两种写法接受同一套参数：

```sh
el --compile-native input.el out.elf --target linux-x64
elc --compile-native input.el out.elf --target linux-x64
```

`--compile-native INPUT OUTPUT` 是编译器操作及其两个操作数，`--target` 选择目标；省略 `--target` 时用宿主目标。输出文件名由你决定，扩展名不参与目标选择。加 `--no-cache` 可以关掉这一轮的缓存读写。

当前原生产物路径覆盖 `windows-x64` 与 `linux-x64`。`wasm32-browser` 未接入，会在参数检查时明确拒绝；其他目标名以实际编译诊断为准。跨目标编译只负责生成目标格式的产物，产物能否在目标机器上运行取决于该目标后端和所用标准库设施，先在目标环境里验证最小程序。

项目文件里的 `targets` 分区用于给具名目标覆盖构建配置（规范 PROJ-5、PROJ-6）。当前发行读项目文件时会接受这个字段，但 `el build` 不按它切换目标；选目标仍靠 `--target`。

## 常用命令

| 命令 | 作用 |
| --- | --- |
| `el run ENTRY [ARGS...]` | 编译并运行源码入口，入口之后的参数传给程序 |
| `el build ENTRY [-o OUT]` | 编译为宿主的原生产物，不运行 |
| `el --compile-native IN OUT --target T` | 直接调用编译器，为目标平台生成产物 |
| `el repl` | 交互式读取、编译、执行，状态在会话内保持 |
| `el test` | 增量运行项目测试 |
| `el formatter --check` | 检查格式与可简化写法 |
| `el clean --repo ROOT` | 清理该根目录下可重建的产物和缓存 |
| `el --help` | 查看当前发行实际支持的子命令与选项 |

完整的工具链、缓存、退出码和跨平台说明见[工具链](toolchain.md)。

## 常见问题

!!! warning "程序没有输出"
    `el run` 能启动但没有打印，先确认输出走的是 `console.stdout.write` / `writeLine`。日志等级的消息默认走 stderr，重定向 stdout 时看不到它们；要进 stdout 的数据用 `console.stdout.write`。

!!! warning "`elc` 找不到"
    `el` 不依赖 `elc`：`el run` 与 `el build` 使用发行自带的编译器源码。只有直接调用 `elc` 的脚本才需要这个文件。如果 `el` 报缺少编译服务映像，说明发行解压不完整，重新取完整发行，而不是另外去找 `elc`。

!!! warning "找不到文件"
    EL 的来源相对路径相对于**引用它的模块**解析，不是相对于你执行命令的目录。`package.eol` 里的路径相对于项目根。把这两个基准分清，大多数“文件不存在”都会消失。

!!! warning "import 报错"
    EL 没有 `import * as m`，也没有只执行副作用的 `import "./x.el"`。每次导入都要写出名字：`import /.*/ from "..."`、`import /.*/ as m from "..."` 或 `import { a, b as c } from "..."`。

!!! warning "GUI 没有窗口"
    GUI 需要真实图形宿主。无终端、headless 或全部流被重定向的环境不会自动弹窗；GUI console 也只在可用时参与展示。目标不支持时应当报错，而不是假装成功。

## 继续阅读

- [语言速览](tour.md)：用一个小程序把主要语法串起来。
- [工具链](toolchain.md)：`el` / `elc`、构建模式、缓存与退出码。
- [值与类型](language/values.md)：从变量、数字和文本开始系统学习。
