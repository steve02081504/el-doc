# 工具链

`el` 是主入口，负责运行、构建、测试和工具调度。`elc` 是同一份发行里的独立编译器门面：它与 `el` 内部的编译器入口共用一条编译链和同一套参数，只是一个可以直接调用的可执行文件。日常开发用 `el` 就够；外部构建脚本、自举或排查编译链时才需要直接调用 `elc`。

## el 与 elc

- 同一发行、同一编译链。`elc` 的源码入口直接调用 compiler 命令模块的参数解析与编译实现，和 `el compiler` 是同一个入口，参数集与产物一致。
- `el` 自己就能编译。`el run`、`el build` 使用发行自带的编译器源码，不需要 `elc` 可执行文件。`el --compile-native ...`、`el compiler --compile-native ...` 与 `elc --compile-native ...` 三种写法的命令行参数相同。
- `elc` 适合外部工具或自举阶段直接调用；日常开发不必安装或寻找它，找不到 `elc` 不影响 `el run` 和 `el build`。
- `EL_ELC` 与 `el test --compiler PATH` 指定测试使用的工作编译器，默认是 `el` 自身；它们是测试选项，不是编译前提。
- `el` 的编译依赖发行内容完整：`src/` 里的编译器源码和 `lib/compiler-service.eir` 服务映像都要在，`EL_COMPILER_SERVICE` 可以把服务映像指到别处。只复制 `el` 一个文件不能编译，这与有没有 `elc` 无关。

## 命令总览

| 命令 | 作用 | 是否会运行程序 |
| --- | --- | --- |
| `el run ENTRY [ARGS...]` | 编译显式入口并立即运行，入口后的参数传给程序 | 是 |
| `el build ENTRY [-o OUT]` | 编译显式入口为宿主原生产物 | 否 |
| `el repl` | 交互式读取、编译、执行，状态在会话内保持 | 是 |
| `el test` | 增量运行项目测试或仓库验收 | 是 |
| `el formatter [--check\|--write]` | 检查或写回格式 | 否 |
| `el clean --repo ROOT` | 清理该根目录下可重建的产物与缓存 | 否 |
| `el compiler ...` | 直接调用编译器（参数同 `elc`） | 否 |
| `el shell SCRIPT` / `esh` | 编译并执行 `.esh` 脚本文件 | 是 |
| `el eir ...` | 编译 ABI EIR 或处理执行 profile | 否 |
| `el debug ...` | 检查并执行有界 ABI EIR | 视输入 |
| `el exec ...` | 启动外部程序 | 是 |
| `el publish SOURCE TARGET` | 发布已完成的候选文件 | 否 |

`el --help` 显示当前发行实际支持的子命令，`el` 不带参数时打印同一份摘要。未知子命令是用法错误，不做前缀猜测。

## 运行 EL 代码

`el run ENTRY` 编译显式入口并立即运行。产物是临时文件，程序退出后删除，不需要手工清理：

```sh
el run src/main.el
```

入口必须是文件路径，`.el` 与 `.els` 都接受。`el run` 不读项目文件里的 `entry` 找入口，项目里也要写出文件路径；`entry` 是规范给项目级命令的默认入口，当前发行仍要求显式文件，实际选项以 `el --help` 为准。

程序参数写在入口之后，原样传递：

```sh
el run src/main.el --verbose input.txt
```

`el` 自己的选项只有 `--debug`、`--release` 和 `--help`，并且要放在入口之前；入口之后的 `--release` 归程序。程序的退出码就是 `el run` 的退出码。

编译器仍会从入口位置向上查找 `package.eol`/`package.eod`，项目文件里的 `imports` 映射对运行与构建都生效。

## 编译为可执行文件

`el build ENTRY` 编译显式入口，不运行程序：

```sh
el build src/main.el -o build/app
```

`-o` 与 `--output` 是同一个选项，给一个输出路径，输出不能等于入口文件，也不能是目录。不给输出时，产物放在入口旁边：文件名沿用入口名，扩展名换成宿主可执行后缀，Windows 是 `.exe`，Linux 没有后缀。`-o` 给出的名字原样使用，不会自动补后缀。成功时 `el build` 把产物路径写到标准输出。

`el build` 只接受一个入口文件。构建失败返回非零，同一路径上已有的旧产物会保留，不会被失败的一轮覆盖。

### debug 与 release

默认是 debug：保留索引检查、范围检查、内部状态断言，以及更完整的诊断。显式选择 release：

```sh
el build src/main.el --release -o build/app
```

对 `run`，模式选项同样放在入口之前：

```sh
el run --release src/main.el
```

两种模式共用一条优化流水线。release 省去的是标准库中仅用于防止违反调用前提的运行期安全检查；类型、借用、所有权、生命周期检查和接口明确承诺的失败不会因为 release 消失。`--release` 与 `--debug` 互斥。

## 为其他系统生成可执行文件

`el run`、`el build` 按宿主目标编译，`el build` 没有 `--target`。为其他系统生成产物要直接调用编译器入口；`el` 会把首个参数命中编译器选项的调用转发给编译器，所以下面三种写法是同一个入口：

```sh
el --compile-native input.el out.elf --target linux-x64
el compiler --compile-native input.el out.elf --target linux-x64
elc --compile-native input.el out.elf --target linux-x64
```

`--compile-native INPUT OUTPUT` 是编译器操作及其两个操作数；`--target TARGET` 选择目标，省略时用宿主目标；`--no-cache` 关掉这一轮的缓存读写，`--diagnostics=json` 输出结构化诊断。输出文件名由输出参数决定，扩展名不参与目标选择。

当前原生产物路径覆盖 `windows-x64` 与 `linux-x64`。`wasm32-browser` 未接入，目标检查会明确拒绝；其他目标名以实际编译诊断为准。跨目标编译只负责生成目标格式的产物，产物能否在目标机器上运行取决于该目标后端与所用标准库设施。GUI 的网页产物在同一个 wasm 目标上，形态见[图形界面](stdlib/gui.md)。

项目文件可以写 `targets` 分区（规范 PROJ-5：目标以具名对象表达，共用项先读取、目标项显式覆盖，列表整体替换）。当前发行读项目文件时接受这个字段，但 `el build` 不按它切换目标，产物路径也不随目标变化；选目标仍靠 `--target`。

规范里 `el compile`、`el docs` 等命令也带 `--target`，当前发行没有这两个子命令，目标相关的操作以本页命令与 `el --help` 为准。

### 平台相关的模块来源

目标键也用于选择平台相关的模块来源：

```el
import /.*/ as backend from @{
	windows-x64: "./backend/win.el";
	linux-x64: "./backend/linux.el"
}
```

平台映射没命中当前目标时是编译错误，并会列出已有键。

## 项目配置

项目由项目文件声明。文件名固定为 `package.eol`（文本）或 `package.eod`（二进制），同一个目录里两者都存在时按歧义报错。

```eol
@{
	entry: "src/main.el",
	imports: {
		"app/": "./src/"
	},
	tests: {
		include: ["tests/**/*.test.el"],
		sources: ["src/**/*.el", "src/**/*.els"]
	}
}
```

- `entry`：规范约定的默认入口。当前发行里 `el run`/`el build` 不读它，仍要求显式入口文件。
- `imports`：说明符前缀到目录的映射。路径相对**项目根**，不是进程 cwd；编译器从入口位置向上找到项目文件后就应用这份映射。
- `tests`：测试发现范围，字段含义见[测试](stdlib/testing.md)。
- `dependencies`、`targets`、`updates`、`cache`、`permissions`：规范定义的依赖、目标、更新策略、缓存与权限分区。当前构建路径不用 `targets` 切换目标；未知字段会定位报错，不静默忽略。
- 内部格式不加版本号，也不读旧格式。项目文件是数据，不是 EL 源码。

`el test` 等需要项目上下文的命令从当前目录向上查找最近的 `package.eol`/`package.eod` 确定项目根。找不到时明确报错，不猜入口文件名。`el run` 与 `el build` 使用显式入口文件，同时编译器会从入口位置向上读取项目文件的 `imports` 映射。

## 测试与格式化

测试默认增量执行：按完整输入内容、工具与依赖身份重跑受影响的文件，复用的成功结果会明确标记。强制全量：

```sh
el test --full
```

测试写法见[测试](stdlib/testing.md)。

格式化器默认只检查，不写回：

```sh
el formatter --check src
el formatter --write src
```

- 不给路径时检查当前目录；目录按字典序递归收集 `.el`，跳过 `build` 和以 `.` 开头的目录。
- 代码行缩进只能用制表符；模块源文件不得超过 1500 行；目录命名与冗余判断另有规则。这些属于检查报告，不都由 `--write` 自动改。
- `--write` 只应用可证明保持语义的改写，例如可省略的分号。
- `--full` 关闭按上次结果跳过的优化；`--state PATH` 换一份状态文件。
- 退出码：`--check` 无待处理内容为 0，有待处理或规则违规为 1，用法/路径错误或无法安全扫描为 2。

## 缓存与清理

编译缓存默认开启。`el run`/`el build` 使用发行根目录下的 `.el/local/compiler/cache`；直接调用编译器入口（`el compiler`、`elc`）时默认落在当前目录的同名路径。`ELC_CACHE_DIR` 可以把缓存统一指到别处。缓存按内容寻址，删除只损失复用机会，不影响源码正确性。

```sh
# 本次运行禁用缓存读写
ELC_CACHE=0 el run src/main.el

# 换缓存目录
ELC_CACHE_DIR=/tmp/el-cache el run src/main.el
```

清理发行目录里可重建的内容：

```sh
el clean --repo . --dry-run
el clean --repo .
```

当前发行要求显式 `--repo ROOT`，`ROOT` 是含 `build/`、`bin/`、`.el/` 的发行根或开发检出根。默认清 `build/` 下可重建的产物，并让过期缓存载荷（默认 90 天）失效，保留工作编译器与未过期缓存这两项最贵的东西。只有显式 `--all` 才会连缓存、`build/elc/` 与 `bin/` 一起收；`--keep-cache`/`--keep-compiler` 与 `--all` 同时给出是用法错误。`--max-age-days N` 改缓存期限，`0` 表示不看年龄。删除失败返回非零。

## 诊断与退出码

诊断写到 stderr，程序自己的 stdout 不被污染。默认退出码：

| 码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 编译失败、运行失败、测试失败 |
| 2 | 用法错误或配置错误 |
| 3 | 工具内部错误 |

工具专属的退出码不会被这套默认值覆盖。编译器入口（`el compiler`、`elc`）支持 `--diagnostics=json`，输出带 code、severity、message、source、span、notes 的结构化诊断；普通文本诊断会给出文件、起始行列、期望元素与实际遇到的 token。

## shell 入口

`el shell` 与 `esh` 是同一套 shell 前端的两个入口，加载同一模块，不是第二套工具链。`.esh` 是原生 shell 前端输入，与普通 `.el`/`.els` 语法域区分开；当前只接文件入口，交互式输入尚未接入。日常写 EL 程序不需要它。

## 文件与目录约定

| 扩展名 | 用途 |
| --- | --- |
| `.el` | 普通 EL 源码模块，默认用编辑器打开 |
| `.els` | EL 可执行脚本，面向直接运行与双击执行 |
| `.eol` / `.eod` | 对象图的文本／二进制形式；项目配置用 `package.eol` / `package.eod` |
| `.eir` | 低层 EIR 源码 |
| `.edb` | EL 数据库文件 |
| `*.test.el` | 测试源码 |
| `.esh` | 原生 shell 前端输入 |

发行面是单宿主加按需加载的工具源码：编译器、格式化器、EIR 工具随发行提供，在实际调用子命令时编译和加载，不预编成另一组对外工具。

## 出问题时

!!! warning "`el: command not found`"
    发行目录没有进 `PATH`，或当前终端还是加入 `PATH` 之前的进程。重新打开终端后再试。

!!! warning "找不到项目"
    `el test` 等需要项目上下文的命令会从当前目录向上查找 `package.eol`/`package.eod`。`el run` 与 `el build` 必须显式给入口文件；路径不存在时按给出的路径报错，不会猜入口文件名。

!!! warning "缺少编译服务"
    `el run` / `el build` 需要发行自带的编译器源码与服务映像。完整发行会带齐 `src/` 和 `lib/compiler-service.eir`；只复制了 `el` 一个文件时会出现这个错误。重新解压完整发行，或用 `EL_COMPILER_SERVICE` 指向现成的服务映像。这与有没有 `elc` 无关。

!!! warning "改了源码但行为没变"
    先确认缓存身份是否失效：设置 `ELC_CACHE=0` 重跑一次。仍不对，再检查导入的是不是你改的那个文件，以及是否有多个同名模块来源。

## 继续阅读

- [测试](stdlib/testing.md)：`*.test.el`、项目测试配置与断言。
- [命令行工具](practice/cli-tool.md)：把这里的命令用在一个完整项目上。
- [规范与实现边界](appendix/implementation-status.md)：哪些工具行为是目标合同，哪些仍随发行版本变化。
