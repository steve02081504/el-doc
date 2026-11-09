# 工具链

`el` 是主入口，负责运行、构建、测试和工具调度；`elc` 是底层编译器。日常开发只和 `el` 打交道，构建链路、缓存和诊断都由它组织。

## 命令总览

| 命令 | 作用 | 是否会运行程序 |
| --- | --- | --- |
| `el repl` | 交互式读取、编译、执行，状态在会话内保持 | 是 |
| `el run ENTRY [ARGS...]` | 编译源码并立即运行，入口后的参数传给程序 | 是 |
| `el build ENTRY [-o OUT]` | 把源码编译为原生产物 | 否 |
| `el test` | 增量运行项目测试 | 是 |
| `el formatter [--check\|--write]` | 检查或写回格式 | 否 |
| `el clean` | 清理可重建的产物与缓存 | 否 |
| `el compile` | 单次编译，不查项目、不运行产物 | 否 |
| `el docs` | 生成文档内容对象与 reader 产物 | 否 |
| `el eir` | 读取 EIR 文本并生成原生产物 | 否 |
| `el shell` / `esh` | 原生 shell 前端，处理 `.esh` 输入 | 视输入 |

`el --help` 显示当前发行实际支持的子命令。未知子命令是用法错误，不做前缀猜测。

## 运行与构建

运行一个入口：

```sh
el run src/main.el
```

把参数传给程序，写在入口之后：

```sh
el run src/main.el --verbose input.txt
```

`run` 会编译后立即执行，不把中间产物留成需要你处理的状态；程序退出后临时产物会被清理。入口之后的参数原样传给程序，不会被 `el` 当成自己的选项。

构建产物：

```sh
el build src/main.el -o build/app.exe
```

Windows 上默认后缀是 `.exe`，Linux 上无后缀。不给 `-o` 时产物默认放在入口旁边。`build` 只编译、不执行；失败返回非零，不生成半成品冒充成功。

### 两种构建模式

默认是 debug：保留索引检查、范围检查、内部状态断言，以及更完整的诊断。显式选择 release：

```sh
el build src/main.el --release -o build/app.exe
```

对 `run`，模式选项放在入口之前：

```sh
el run --release src/main.el
```

两种模式共用一条优化流水线。release 省去的是标准库中仅用于防止违反调用前提的运行期安全检查；类型、借用、所有权、生命周期检查和接口明确承诺的失败不会因为 release 消失。`--release` 与 `--debug` 互斥。

### 目标与平台

目标用 `os-arch` 或目标三元组标识，例如 `windows-x64`、`linux-aarch64`。项目可以在 `package.eol` 里声明多个具名目标，共用项先读取、目标项显式覆盖。`el compile` 与 `el docs` 支持显式 `--target`；不可用的目标会明确报错，不会静默回退到宿主。

平台相关的模块来源也使用同一套键：

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

- `entry`：默认入口。项目级命令使用它；`el run`/`el build` 本身以显式入口文件为准。
- `imports`：说明符前缀到目录的映射。路径相对**项目根**，不是进程 cwd。
- `tests`：测试发现范围，字段含义见[测试](stdlib/testing.md)。
- `dependencies`、`targets`、`updates`、`cache`、`permissions`：依赖、目标、更新策略、缓存与权限配置。未知字段会定位报错，不静默忽略。
- 内部格式不加版本号，也不读旧格式。项目文件是数据，不是 EL 源码。

`el test`、`el docs` 等项目级命令从当前目录向上查找最近的 `package.eol`/`package.eod` 确定项目根。找不到时明确报错，不猜入口文件名。`el run` 与 `el build` 当前使用显式入口文件；把入口路径写在项目文件里供其他命令使用。

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

编译缓存默认开启，位于当前项目的 `.el/local/compiler/cache`。缓存按内容寻址，删除只损失复用机会，不影响源码正确性。

```sh
# 本次运行禁用缓存读写
ELC_CACHE=0 el run src/main.el

# 换缓存目录
ELC_CACHE_DIR=/tmp/el-cache el run src/main.el
```

清理可重建内容：

```sh
el clean --dry-run
el clean
```

默认清 `build/` 下可重建的产物和过期缓存，保留工作编译器与缓存载荷这两项最贵的东西。只有显式 `--all` 才会包含缓存、`build/elc/` 与 `bin/`。`--max-age-days N` 改缓存期限，`0` 表示不看年龄；`--keep-cache`/`--keep-compiler` 与 `--all` 同时给出是用法错误。删除失败返回非零。

## 诊断与退出码

诊断写到 stderr，程序自己的 stdout 不被污染。默认退出码：

| 码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 编译失败、运行失败、测试失败 |
| 2 | 用法错误或配置错误 |
| 3 | 工具内部错误 |

工具专属的退出码不会被这套默认值覆盖。`el` 与编译子命令支持 `--diagnostics=json`，输出带 code、severity、message、source、span、notes 的结构化诊断；普通文本诊断会给出文件、起始行列、期望元素与实际遇到的 token。

## elc 与其他入口

`elc` 是底层编译器，通常由 `el` 通过编译服务调用。需要排查编译链或做底层构建时才直接使用它：

```sh
# 让 el test 使用指定的编译器产物
EL_ELC=./path/to/elc el test

# 使用显式编译服务映像
EL_COMPILER_SERVICE=./lib/compiler-service.eir el run src/main.el
```

`el build`、`el run` 和源码工具优先使用编译服务；缺少服务时明确报错，不会偷偷启动另一个旧编译器。默认编译程序是 `el` 自身。

`el shell` 与 `esh` 是同一套 shell 前端的两个入口，加载同一模块，不是第二套工具链。`.esh` 是原生 shell 前端输入，与普通 `.el`/`.els` 语法域区分开；日常写 EL 程序不需要它。

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
    `el run` 不带入口时会向上查找 `package.eol`/`package.eod`。确认你在项目目录内，或直接给入口文件。

!!! warning "缺少编译服务"
    `el run` / `el build` 需要可用的编译服务映像。完整发行会带齐；只复制了 `el` 一个文件时会出现这个错误。重新安装完整发行，或显式设置 `EL_COMPILER_SERVICE`。

!!! warning "改了源码但行为没变"
    先确认缓存身份是否失效：设置 `ELC_CACHE=0` 重跑一次。仍不对，再检查导入的是不是你改的那个文件，以及是否有多个同名模块来源。

## 继续阅读

- [测试](stdlib/testing.md)：`*.test.el`、项目测试配置与断言。
- [命令行工具](practice/cli-tool.md)：把这里的命令用在一个完整项目上。
- [规范与实现边界](appendix/implementation-status.md)：哪些工具行为是目标合同，哪些仍随发行版本变化。
