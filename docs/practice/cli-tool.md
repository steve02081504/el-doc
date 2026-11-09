# 实战：命令行工具

这一页从空目录开始写一个统计文本行数与词数的命令行程序；读完你能自己建项目、读参数、读写文件，并用退出码向调用者报告结果。

## 目标

程序叫 `words`，接受一个文件路径：

```text
words <文件>
```

它读取文件，输出行数与词数；文件读不到或参数不对时，打印原因并以非零退出码结束。行数按换行符分隔计数，词数按空白分隔的片段计数，中文文本没有空格时整段算一个词。

```text
words/
├── package.eol
└── src/
    └── main.el
```

`package.eol` 声明项目入口，`el test` 等按项目工作的子命令靠它定位项目根。项目文件必须是 `package.eol` 或 `package.eod`，从当前目录向上查找最近的一份，同一目录里两种并存按歧义报错。

```eol
@{
	entry: "src/main.el"
}
```

## 读取命令行参数

参数入口是 `el:operating-system/arguments/index.el` 的 `command_arguments()`，返回 `Text[]`：下标 0 是程序自身路径，其余是用户给的参数，次序原样保留。带引号的参数由平台层拆好，程序拿到的是已经切分的文本数组。

```el
import { command_arguments } from "el:operating-system/arguments/index.el"
import { exit } from "el:operating-system/processes/index.el"

let argv = command_arguments()
if (Number(argv.size) != 2) {
	console.stderr.writeLine("usage: words FILE")
	exit(2)
}
let path = argv[1]
```

`exit(code)` 的类型是 `Never`，调用后不会继续执行后面语句；成功退出码是 0，参数用法错误按约定用 2。参数数量先查再用下标，别先取 `argv[1]` 再判断。

需要 `--verbose` 这类选项时，用同一个模块的 `parse_arguments(args, options)` 与 `ArgumentOption` 声明：名字不带横线，长短写法归一，重复与缺值会写进 `parsed.error`，不会猜缩写或前缀。解析器只负责把文本拆成结果对象，不执行程序、不决定业务字段。

!!! note "实现状态"
    规范第 11 章把运行期参数列为普通库的 `arguments()`；当前检出的公开导出是 `command_arguments()`，两个名字不并存。按源码写 `command_arguments()`，拿到的是完整 `argv`。

## 读取文件

文本读取用 `el:filesystem/index.el` 的 `readTextFile(reference)`，返回解码后的 `Text`；可选的第二个参数是最大字节数，超过上限抛错而不是截断。相对路径按当前工作目录解析，需要显式确认时用 `currentDirectory()`。

```el
import { readTextFile } from "el:filesystem/index.el"

let source = ""
try { source = readTextFile(path) }
catch (error) {
	console.error.value(error)
	exit(1)
}
```

先在 `try` 外声明 `source`，捕获后它仍在作用域里；`catch (error)` 绑定异常对象，`console.error.value(error)` 把这个值作为结构化记录写到 stderr。文件不存在、没有权限、不是合法 UTF-8 都会走到这里，程序以 1 退出。

## 统计

```el
fn countLines(text: Text): Number {
	if (text == "") return 0
	return Number(text.split("\n").count)
}

fn countWords(text: Text): Number {
	let total = 0
	for let line in text.replaceAll("\r", "").split("\n") {
		for let chunk in line.split("\t") {
			for let word in chunk.split(" ") {
				if (word != "") total++
			}
		}
	}
	return total
}
```

`Text.split(pattern)` 接收文本模式并返回 `Text[]`，`count` 是元素个数。先用 `replaceAll("\r", "")` 去掉 Windows 换行里的回车，再按 `\n` 拆行，这样行尾的 `\r` 不会混进词里。词数按空格、制表符和换行切分，空片段跳过；它统计的是空白分隔的片段，不是语言学意义上的词。

空文件单独返回 0，避免把一串空片段当成一行。文本的 `count` 与数组的 `count` 都是 `Integer`，参与 `Number` 运算前显式调用 `Number(...)` 最稳。

## 输出结果

```el
console.stdout.writeLine("lines: ", countLines(source), "  words: ", countWords(source))
```

`console.stdout.writeLine(...values)` 接受多个参数，逐个做普通 `Text(value)` 转换后顺序写出，最后追加 LF；参数之间不会自动加分隔符，空格要自己写在字符串里。要在一行内分多次写，用 `console.stdout.write(...)`。

需要展示对象、数组、错误值这类结构时，用等级对象的 `.value(value)`；日志默认去 stderr，要把结构化记录写到标准输出，给 `.value` 传第二个参数 `stdoutChannel`。程序自身的正常输出留在 stdout，诊断信息留在 stderr，调用方用管道接数据时不会混入噪声。

## 错误与退出码

- 0：统计成功。
- 1：读取或运行失败，已把错误写到 stderr。
- 2：参数用法错误。

异常只在这里当控制流用一次：`try` 包住读文件，`catch` 里报告并 `exit`。其余位置让异常继续向上抛，由 `el` 报告；不要为了“看起来干净”把异常吞掉再返回 0，那会让脚本和 CI 分不清成功与失败。

## 完整源码

`src/main.el`：

```el
import { command_arguments } from "el:operating-system/arguments/index.el"
import { readTextFile } from "el:filesystem/index.el"
import { exit } from "el:operating-system/processes/index.el"

fn countLines(text: Text): Number {
	if (text == "") return 0
	return Number(text.split("\n").count)
}

fn countWords(text: Text): Number {
	let total = 0
	for let line in text.replaceAll("\r", "").split("\n") {
		for let chunk in line.split("\t") {
			for let word in chunk.split(" ") {
				if (word != "") total++
			}
		}
	}
	return total
}

let argv = command_arguments()
if (Number(argv.size) != 2) {
	console.stderr.writeLine("usage: words FILE")
	exit(2)
}
let path = argv[1]
let source = ""
try { source = readTextFile(path) }
catch (error) {
	console.error.value(error)
	exit(1)
}
console.stdout.writeLine("lines: ", countLines(source), "  words: ", countWords(source))
```

## 运行

在项目根目录执行，入口文件之后的内容会原样传给你的程序：

```text
el run src/main.el docs/index.md
```

`el run` 把入口编译到临时产物、启动它，退出后删掉临时文件；程序的标准输出与标准错误直接出现在终端，退出码原样返回给 `el`。示例输出：

```text
lines: 83  words: 412
```

参数给错时：

```text
$ el run src/main.el
usage: words FILE
$ echo $?
2
```

Windows PowerShell 用 `$LASTEXITCODE` 查看上一条命令的退出码。

## 构建

```text
el build src/main.el
```

只编译不运行，默认输出到入口文件旁边并换成平台可执行后缀，命令把产物绝对路径写到标准输出。Windows 得到 `src\main.exe`，Linux 与 macOS 得到 `src/main`。构建完成后直接运行产物：

```text
src\main.exe docs\index.md
el build -o build/words.exe src/main.el
el build --release src/main.el
```

`-o` 与 `--output` 指同一个选项；`--release` 关闭只在 debug 保留的数组、文本与视图边界检查，默认是 debug。release 不会改变语言行为，越界访问在 release 下属于调用方违约，不保证抛错。

## 调用外部程序：`shell { ... }`

真实工具很少只靠自己。要把 `git`、编译器或别的命令行程序接进来，用库里的 `shell` 块；块里直接写命令，不必先拼字符串再交给进程 API。

```el
import { shell } from "el:shell/index.el"

let result = shell { git status --short }
console.stdout.writeLine(Text(result))
```

`shell { ... }` 直接返回 `ShellResult`，块本身就是输出、退出码与状态的收集边界。`Text(result)` 是受检的文本投影，只取标准输出，不混入 stderr 和消息等级；没有明确文本目标时，结果仍然是 `ShellResult`。

```el
let branch: Text = shell { git branch --show-current }
let diff = shell { git diff --quiet }
if (diff.exitCode != 0) console.stdout.writeLine("working tree has changes")
```

`ShellResult` 的主要字段：

- `.output` 是 `CapturedOutput`，保留通道、结构值与字节。
- `.exitCode` 是汇总退出码；非零退出不会自动变成异常，要自己判断。
- `.status` 区分成功、进程失败、启动失败、EL 异常、流失败与取消。
- `.stages` 保留每个阶段的原始退出码与 signal。
- `.completeness` 标明输出是完整、部分写入还是截断。

命令写法和普通程序调用接近：`git` 是程序名，后面的词是参数。若当前作用域里已有同名 EL 绑定，普通名字优先；要显式绕过绑定、强制找外部程序，写 `& git status`。块内可以声明普通变量和函数，也可以把 EL 值接到命令参数上；已绑定的结果不会被重复当输出打印。

需要后台执行时用同一模块的 `start` 语法声明。要单独导入它：`import /^start$/ as jobs from "el:shell/index.el"`，之后写 `let job = jobs.start { git status }`，拿到 `Job`，不阻塞当前流程，后续可以等待或终止这个作业。普通 `.el` 文件要像上面那样导入 `shell` 宏；`.esh` 文件的顶层本身就是 shell 语法域，不需要再包块。

## 继续阅读

- [工具链](../toolchain.md)：`el` 子命令、项目文件与缓存。
- [文件与网络](../stdlib/files-network.md)：文本读取、写入与请求。
- [图形程序](gui-app.md)：同一个项目骨架换成窗口界面。
