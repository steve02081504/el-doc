# 实战：命令行工具

> 一个四十行的程序，凭什么算“完整项目”？因为它要把参数、文件、标准输出和退出码一次接对——后面所有工具都是这个骨架。

!!! abstract "🎯 做完这个项目，你能"
    - 从空目录建出 `package.eol` 与 `src/main.el`，用 `el run` 跑出第一行输出
    - 用 `command_arguments()` 读参数，数量不对就以 2 退出
    - 用 `readTextFile` 读文件，读不到就把错误写进 stderr 并以 1 退出

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">用到的知识：[Console](../stdlib/console.md)、[文件与网络](../stdlib/files-network.md)、错误处理</span>

## 目标与边界

要写的程序叫 `words`，接受一个文件路径，打印行数与词数：

```text
words <文件>
```

行数按换行符分隔计数，词数按空白分隔的片段计数；中文文本没有空格时整段算一个词。参数不对或文件读不到时，打印原因并以非零退出码结束。

最终验收标准是四条：

- `el run src/main.el sample.txt` 打印一行 `lines: 3  words: 4`
- 不带参数运行，打印 `usage: words FILE`，退出码是 2
- 指向不存在的文件，stderr 上出现错误，退出码是 1
- `el build src/main.el` 产出的可执行文件，不装 `el` 也能跑出同样的结果

不做的部分：递归目录、编码探测、JSON 输出，都留给“改成你自己的”。

## 第一步：先让一个空项目跑起来

项目文件固定叫 `package.eol` 或 `package.eod`，声明入口；`el test` 一类子命令靠它定位项目根：从当前目录向上找最近一份，同目录两种并存按歧义报错。

```text
words/
├── package.eol
└── src/
    └── main.el
```

```eol
@{
	entry: "src/main.el"
}
```

`src/main.el` 先只打一行字，确认工具链通了：

```el
console.stdout.writeLine("words ready")
```

在项目根目录执行：

```text
el run src/main.el
```

```text
words ready
```

`el run` 把入口编译到临时产物、启动它，退出后删掉临时文件；程序的标准输出与标准错误直接出现在终端，退出码原样返回给 `el`。

!!! success "检查点"
    - [ ] `el run src/main.el` 输出 `words ready`
    - [ ] 把 `writeLine` 的参数换成你的名字，输出跟着变

## 第二步：参数不对，在读文件之前就退出

参数入口是 `el:operating-system/arguments/index.el` 的 `command_arguments()`，返回 `Text[]`：下标 0 是程序自身路径，其余是用户参数，次序原样保留，引号由平台层拆好。

```el
import { command_arguments } from "el:operating-system/arguments/index.el"
import { exit } from "el:operating-system/processes/index.el"

let argv = command_arguments()
if (Number(argv.size) != 2) {
	console.stderr.writeLine("usage: words FILE")
	exit(2)
}
let path = argv[1]
console.stdout.writeLine("file: ", path)
```

先查数量再用下标。`exit(code)` 的类型是 `Never`，调用后不会继续往后执行；成功退出码是 0，用法错误按约定用 2。

```text
$ el run src/main.el sample.txt
file: sample.txt
$ el run src/main.el
usage: words FILE
$ echo $?
2
```

Windows PowerShell 用 `$LASTEXITCODE` 查看上一条命令的退出码。

!!! note "实现状态"
    规范第 11 章把运行期参数列为普通库的 `arguments()`；当前检出的公开导出是 `command_arguments()`，两个名字不并存。按源码写 `command_arguments()`，拿到的是完整 `argv`。

需要 `--verbose` 这类选项时，用同一个模块的 `parse_arguments(args, options)` 与 `ArgumentOption`：名字不带横线，长短写法归一，重复与缺值会写进 `parsed.error`，不猜缩写或前缀。解析器只把文本拆成结果对象，不执行程序、不决定业务字段。

!!! success "检查点"
    - [ ] 带一个参数运行，看到 `file: ` 加你给的路径
    - [ ] 不带参数运行，看到 `usage: words FILE`，退出码是 2

## 第三步：文件读不到，就以 1 退出

文本读取用 `el:filesystem/index.el` 的 `readTextFile(reference)`，返回解码后的 `Text`；可选的第二个参数是最大字节数，超过上限抛错而不是截断。相对路径按当前工作目录解析，需要显式确认时用 `currentDirectory()`。

```el
import { readTextFile } from "el:filesystem/index.el"

let source = ""
try { source = readTextFile(path) }
catch (error) {
	console.error.value(error)
	exit(1)
}
console.stdout.writeLine("chars: ", source.count)
```

先在项目根目录建一个 `sample.txt`，内容两行、末尾留一个换行：

```text
EL 是一门精确的编程语言。
hello world
```

先在 `try` 外声明 `source`，捕获后它仍在作用域里；`catch (error)` 绑定异常对象，`console.error.value(error)` 把这个值作为结构化记录写到 stderr。文件不存在、没有权限、不是合法 UTF-8 都会走到这里，程序以 1 退出。这一步打印字符数只是探针。

```text
$ el run src/main.el sample.txt
chars: 27
$ el run src/main.el missing.txt
…（stderr 上的错误记录）
$ echo $?
1
```

!!! success "检查点"
    - [ ] 读一个存在的文件，看到 `chars: ` 加一个正整数
    - [ ] 读一个不存在的文件，退出码是 1，错误出现在 stderr 而不是 stdout

## 第四步：数行数与词数

```el
fn countLines(text: Text) {
	if (text == "") return 0
	return Number(text.split("\n").count)
}

fn countWords(text: Text) {
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

`Text.split(pattern)` 接收文本模式并返回 `Text[]`，`count` 是元素个数。先用 `replaceAll("\r", "")` 去掉 Windows 换行的回车再按 `\n` 拆行，行尾的 `\r` 就不会混进词里。词数按空格、制表符和换行切分，空片段跳过，统计的是空白分隔的片段而非语言学意义上的词。

空文件单独返回 0，免得把一串空片段当成一行。文本与数组的 `count` 都是 `Integer`，参与 `Number` 运算前显式调用 `Number(...)` 最稳。

??? question "先猜：两行的文件，`lines:` 会打印 2 吗？"
    会打印 3。`split` 在末尾的换行之后还留一个空片段，`count` 数的是片段数；文件末尾没有换行时才是 2。

`words` 对 `sample.txt` 的统计结果是 `lines: 3  words: 4`：两行加末尾空片段共三段，四个词（`EL`、`是一门精确的编程语言。`、`hello`、`world`）。

!!! success "检查点"
    - [ ] `sample.txt` 末尾留换行时，`countLines` 得到 3；去掉末尾换行后得到 2
    - [ ] `countWords` 得到 4，中文那句整体算一个词
    - [ ] 空文件返回 0 而不是 1

## 第五步：把结果、诊断和退出码分开

```el
console.stdout.writeLine("lines: ", countLines(source), "  words: ", countWords(source))
```

`console.stdout.writeLine(...values)` 接受多个参数，逐个做普通 `Text(value)` 转换后顺序写出，最后追加 LF；参数之间不会自动加分隔符，空格要自己写进字符串。一行内分多次写用 `console.stdout.write(...)`。

需要展示对象、数组、错误值这类结构时用等级对象的 `.value(value)`；日志默认去 stderr，要写进标准输出就给 `.value` 传第二个参数 `stdoutChannel`。数据留在 stdout、诊断留在 stderr，管道才不会混进噪声。

退出码只有三种含义：0 表示统计成功；1 表示读取或运行失败，错误已写到 stderr；2 表示参数用法错误。

异常只在这里当控制流用一次：`catch` 里报告并 `exit`；其余位置让异常继续向上抛，由 `el` 报告。为了“看起来干净”把异常吞掉再返回 0，会让脚本和 CI 分不清成功与失败。

!!! success "检查点"
    - [ ] 成功运行时整行输出只有一个 `lines: …  words: …`，没有多余空行
    - [ ] `el run src/main.el sample.txt > out.txt` 之后，`out.txt` 里没有错误文本

## 第六步：构建成可交付的产物

```text
el build src/main.el
```

只编译不运行，默认输出到入口文件旁边并换成平台可执行后缀，命令把产物绝对路径写到标准输出。Windows 得到 `src\main.exe`，Linux 与 macOS 得到 `src/main`。构建完成后直接运行产物：

```text
src\main.exe sample.txt
el build -o build/words.exe src/main.el
el build --release src/main.el
```

`-o` 与 `--output` 指同一个选项；`--release` 关闭只在 debug 保留的数组、文本与视图边界检查，默认是 debug。release 不会改变语言行为，越界访问在 release 下属于调用方违约，不保证抛错。

!!! success "检查点"
    - [ ] `el build src/main.el` 在标准输出打印产物的绝对路径
    - [ ] 直接运行产物、不经过 `el`，得到同样的 `lines: …  words: …`

## 再往前一步：让工具去调用别的程序

真实工具很少只靠自己。要把 `git`、编译器或别的命令行程序接进来，用库里的 `shell` 块：块里直接写命令，不必先拼字符串再交给进程 API。

```el
import { shell } from "el:shell/index.el"

let result = shell { git status --short }
console.stdout.writeLine(Text(result))
```

`shell { ... }` 直接返回 `ShellResult`：块本身就是输出、退出码与状态的收集边界。`Text(result)` 是受检的文本投影，只取标准输出，不混入 stderr；没有明确文本目标时，结果仍是 `ShellResult`。

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

命令写法和普通程序调用接近：`git` 是程序名，后面的词是参数。作用域里已有同名 EL 绑定时普通名字优先，要强制找外部程序就写 `& git status`。块内可以声明变量和函数，也可以把 EL 值接到参数上；已绑定的结果不会被重复打印。

需要后台执行时用同一模块的 `start`：`import /^start$/ as jobs from "el:shell/index.el"`，再写 `let job = jobs.start { git status }`，拿到一个不阻塞当前流程的 `Job`，后续可以等待或终止它。普通 `.el` 文件要导入 `shell` 宏；`.esh` 的顶层本身就是 shell 语法域，不必再包块。

## 完整源码

`src/main.el` 与 `package.eol` 放在一起，就是这个项目的全部：

```el
import { command_arguments } from "el:operating-system/arguments/index.el"
import { readTextFile } from "el:filesystem/index.el"
import { exit } from "el:operating-system/processes/index.el"

fn countLines(text: Text) {
	if (text == "") return 0
	return Number(text.split("\n").count)
}

fn countWords(text: Text) {
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

## 改成你自己的

三个由易到难的改造任务，只给方向和验收标准。

1. **接受多个文件。** 参数检查放宽到“至少两个”，用 `for` 遍历 `argv[1..]`，每个文件输出一行 `文件名: lines: …  words: …`；某个文件读不到就报告后继续，最后以非零码退出。验收：三个文件里中间那个不存在，仍看到另外两份的统计。
2. **加一个真正的选项。** 用 `parse_arguments` 与 `ArgumentOption` 支持 `--lines-only`：只输出行数。验收：选项生效、未知选项时 `parsed.error` 非空并退出 2、位置参数仍然可用。
3. **统计整个仓库。** 用 `shell { git ls-files }` 拿到文件列表，逐个累加行数与词数，最后打印总计。验收：`ShellResult.exitCode` 非零时你能打印原因而不是照样输出 0，且总数与逐个运行 `words` 一致。

## 卡住了？

- **现象：明明传了文件，还是打印 `usage: words FILE`。** 路径里的空格没加引号，被拆成两个参数，`argv.size` 变成 3。检查：打印 `Number(argv.size)` 和 `argv`。
- **现象：`lines:` 比编辑器里看到的行数多 1。** 文件末尾有换行，`split` 留下一个空片段。检查：把末尾换行删掉再跑一次，数字应当减一。
- **现象：重定向输出之后，看不到任何错误。** 错误走 stderr，被 `>` 只截走了 stdout。检查：`el run src/main.el missing.txt 2>&1 > out.txt`，或直接看终端。
- **现象：`el build` 的产物在别的目录运行时报找不到文件。** 相对路径按当前工作目录解析，不是按产物位置。检查：用 `currentDirectory()` 打印工作目录，或改传绝对路径。

## 带走这三样

- 一个项目的最小形状：`package.eol` 声明入口，`src/main.el` 是顶层代码。
- 三种退出码的分工：0 成功、1 运行失败、2 用法错误；诊断走 stderr，数据走 stdout。
- `el run` 与 `el build` 的区别：一个编译到临时产物跑完就删，一个留下能交付的原生可执行文件。

## 下一站：[图形程序](gui-app.md)

> 终端里的一切都能用文本和退出码交代清楚，那窗口里的按钮、状态和定时器又该怎么组织？

- 主推进：[图形程序](gui-app.md)：同一个项目骨架换成三个文件的原生窗口应用。
- 想先补基础：[工具链](../toolchain.md)：`el` 子命令、项目文件与缓存的完整说明。
