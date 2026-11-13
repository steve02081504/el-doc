# 工具链

本页按命令、参数、配置和诊断组织。实际发行支持的选项以 `el --help` 为准；语言合同见[工具链规范](https://github.com/steve02081504/el/blob/master/docs/spec/11-build-and-toolchain.md)，实现与验收的区别见[规范与实现边界](appendix/implementation-status.md)。

## 先查这张表：五条命令，各管一件事

| 我想…… | 敲这条 | 会运行程序吗 |
| --- | --- | --- |
| 改完立刻看结果 | `el run src/main.el` | 是 |
| 做一个能交给别人的文件 | `el build src/main.el -o build/app` | 否 |
| 试一个表达式 | `el repl` | 是 |
| 跑项目里写好的测试 | `el test` | 是 |
| 检查格式与可简化写法 | `el formatter --check src` | 否 |

`el --help` 显示当前发行支持的子命令；`el` 不带参数打印同一份摘要。未知子命令是用法错误，不猜前缀。

## `el` 和 `elc` 不是两套工具链

`el` 自带编译器源码，`el run` 和 `el build` 不依赖 `elc` 可执行文件。`elc` 只是同一编译器的单独入口，外部构建脚本、自举或排查编译链时才直接调用它。

- 同一发行、同一编译链：`elc` 的源码入口直接调用 compiler 命令模块的参数解析与编译实现，和 `el compiler` 是同一个入口，参数集与产物一致。
- `EL_ELC` 与 `el test --compiler PATH` 指定测试使用的工作编译器，默认是 `el` 自身；它们是测试选项，不是编译前提。

## 运行：`el run` 编译完立刻执行

`el run ENTRY` 编译显式入口并立即运行，临时产物在程序退出后删除：

```sh
el run src/main.el
```

入口必须是文件路径，`.el` 与 `.els` 都接受。==`el run` 不读项目文件里的 `entry`==：项目里也要写出路径；`entry` 只是规范给项目级命令的默认入口，实际选项以 `el --help` 为准。

程序参数写在入口之后，原样传递：

```sh
el run src/main.el --verbose input.txt
```

`el` 自己的选项只有 `--debug`、`--release` 和 `--help`，且要放在入口之前；入口之后的 `--release` 归程序。程序的退出码就是 `el run` 的退出码。

!!! warning "常见坑：`--release` 写在了入口后面"
    现象：`el run src/main.el --release` 不报错，程序却收到了一个 `--release` 参数。`el` 只认入口之前的选项，入口之后的内容全部原样交给程序。

## 构建：`el build` 只产出文件，不运行

`el build ENTRY` 编译显式入口，不运行程序；成功时把产物路径写到标准输出：

```sh
el build src/main.el -o build/app
```

`-o` 与 `--output` 是同一个选项；输出不能等于入口文件，也不能是目录。不给输出时，产物放在入口旁边：文件名沿用入口名，扩展名换成宿主可执行后缀（Windows 是 `.exe`，Linux 没有后缀）；`-o` 的名字原样使用，不自动补后缀。`el build` 只接受一个入口文件，失败返回非零，同路径旧产物保留。

### 默认 debug，`--release` 只关掉运行期检查

默认是 debug，保留索引检查、范围检查、内部状态断言与更完整的诊断；`--debug` 与 `--release` 互斥，`run` 的选项也放在入口之前：

```sh
el build src/main.el --release -o build/app
el run --release src/main.el
```

两种模式共用一条优化流水线，release 只省去标准库中防止违反调用前提的运行期安全检查，类型、借用、所有权、生命周期检查与接口承诺的失败仍在。

## 跨平台：`el build` 没有 `--target`

`el run`、`el build` 按宿主目标编译。为其他系统生成产物要直接调用编译器入口；`el` 把首个参数命中编译器选项的调用转发给编译器，所以下面三种写法是同一个入口：

```sh
el --compile-native input.el out.elf --target linux-x64
el compiler --compile-native input.el out.elf --target linux-x64
elc --compile-native input.el out.elf --target linux-x64
```

`--compile-native INPUT OUTPUT` 是编译器操作及其两个操作数；`--target TARGET` 选目标（省略用宿主），`--no-cache` 关掉这一轮缓存读写，`--diagnostics=json` 输出结构化诊断。输出文件名由输出参数决定，扩展名不参与目标选择。

当前原生产物路径覆盖 `windows-x64` 与 `linux-x64`；`wasm32-browser` 未接入，目标检查会明确拒绝，其他目标名以实际编译诊断为准。跨目标编译只生成目标格式的产物，能否运行取决于后端与标准库设施；GUI 网页产物在同一个 wasm 目标上，见[图形界面](stdlib/gui.md)。

### 模块来源也能按目标选

```el
import /.*/ as backend from @{
	windows-x64: "./backend/win.el";
	linux-x64: "./backend/linux.el"
}
```

平台映射没命中当前目标时是编译错误，并会列出已有键。

## 项目配置：一个 `package.eol` 说清入口、导入和测试

项目文件名固定为 `package.eol`（文本）或 `package.eod`（二进制），同一目录里两者都有时按歧义报错。

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

- `entry`：规范约定的默认入口（当前发行不读，见上）。
- `imports`：说明符前缀到目录的映射，路径相对**项目根**而非进程 cwd；编译器从入口位置向上找到项目文件后应用。
- `tests`：测试发现范围，见[测试](stdlib/testing.md)。
- `dependencies`、`targets`、`updates`、`cache`、`permissions`：规范定义的依赖、目标、更新策略、缓存与权限分区；当前构建路径不用 `targets` 切换目标，未知字段定位报错。
- 内部格式不加版本号，也不读旧格式；项目文件是数据，不是 EL 源码。

`el test` 等命令从当前目录向上查找最近的 `package.eol`/`package.eod` 确定项目根；找不到时明确报错，不猜入口文件名。

## 测试与格式化：默认只做增量与检查

`el test` 默认增量执行：按完整输入内容、工具与依赖身份重跑受影响的文件，复用的成功结果会明确标记；`--full` 强制全量。格式化器默认只检查，不写回；不给路径时检查当前目录，目录按字典序递归收集 `.el`，跳过 `build` 和以 `.` 开头的目录：

```sh
el formatter --check src
el formatter --write src
```

- 格式规则还包括缩进只能用制表符、模块源文件不超过 1500 行、目录命名与冗余判断——这些只报告，不都由 `--write` 自动改。
- `--write` 只应用可证明保持语义的改写，例如可省略的分号；`--full` 关闭按上次结果跳过的优化，`--state PATH` 换一份状态文件。
- 格式化器复用编译器语义分析，对规范归给 `elf` 的确定违规（例如对 `const` 槽位重赋）报错；`elc` 不保证为这些违规报错。
- 退出码：`--check` 无待处理内容为 0，有待处理或规则违规为 1，用法/路径错误或无法安全扫描为 2。

## 缓存与清理：删缓存只丢复用，删编译器才危险

编译缓存默认开启。`el run`/`el build` 使用发行根目录下的 `.el/local/compiler/cache`；直接调用编译器入口（`el compiler`、`elc`）时默认落在当前目录下的同名路径。`ELC_CACHE_DIR` 可统一指到别处。缓存按内容寻址，删除只损失复用机会，不影响源码正确性。

```sh
ELC_CACHE=0 el run src/main.el                   # 本次运行禁用缓存读写
ELC_CACHE_DIR=/tmp/el-cache el run src/main.el   # 换缓存目录
```

清理发行目录里可重建的内容：

```sh
el clean --repo . --dry-run
el clean --repo .
```

当前发行要求显式 `--repo ROOT`（含 `build/`、`bin/`、`.el/` 的发行根或开发检出根）。默认清 `build/` 下可重建的产物，并让过期缓存载荷（默认 90 天）失效，保留工作编译器与未过期缓存这两项最贵的东西。`--all` 才会连缓存、`build/elc/` 与 `bin/` 一起收；`--keep-cache`/`--keep-compiler` 与 `--all` 同用是用法错误。`--max-age-days N` 改缓存期限，`0` 表示不看年龄；删除失败返回非零。

## 诊断与退出码：诊断进 stderr，stdout 留给程序

诊断写到 stderr，程序自己的 stdout 不被污染。默认退出码：

| 码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 编译失败、运行失败、测试失败 |
| 2 | 用法错误或配置错误 |
| 3 | 工具内部错误 |

工具专属退出码不会被默认值覆盖。编译器入口（`el compiler`、`elc`）支持 `--diagnostics=json`，输出带 code、severity、message、source、span、notes 的结构化诊断；文本诊断给出文件、起始行列、期望元素与实际 token。

## 其余子命令：不常用，但都要认识

| 命令 | 作用 |
| --- | --- |
| `el clean --repo ROOT` | 清理该根目录下可重建的产物与缓存 |
| `el compiler ...` | 直接调用编译器（参数同 `elc`） |
| `el shell SCRIPT` / `esh` | 编译并执行 `.esh` 脚本文件 |
| `el eir ...` | 编译 ABI EIR 或处理执行 profile |
| `el debug ...` | 检查并执行有界 ABI EIR |
| `el exec ...` | 启动外部程序 |
| `el publish SOURCE TARGET` | 发布已完成的候选文件 |

`el debug` 是否运行程序视输入而定；`el shell`/`esh` 会执行脚本，`el exec` 启动外部程序，其余不运行程序。`el shell` 与 `esh` 是同一套 shell 前端的两个入口，加载同一模块，不是第二套工具链；`.esh` 与普通 `.el`/`.els` 语法域分开，当前只接文件入口，交互式输入尚未接入。

扩展名约定：`.el` 源码模块，`.els` 可执行脚本，`.eol`/`.eod` 对象图的文本／二进制形式（项目配置同名），`.eir` 低层 EIR 源码，`.edb` 数据库文件，`*.test.el` 测试源码。工具源码随发行提供，调用子命令时才编译加载，不预编成另一组对外工具。

## 出问题时

| 你看到的 | 原因 | 怎么改 |
| --- | --- | --- |
| `el: command not found` | 发行目录没进 `PATH`，或终端是加 `PATH` 之前的进程 | 重开终端 |
| 找不到项目 | `el test` 等命令从当前目录向上找 `package.eol`/`package.eod` | 补项目文件；`el run`/`el build` 必须显式给入口，不猜入口名 |
| 缺少编译服务 | `el run`/`el build` 需要 `src/` 与 `lib/compiler-service.eir` | 重新解压完整发行，或用 `EL_COMPILER_SERVICE` 指向现成映像；只复制 `el` 一个文件不能编译 |
| 改了源码但行为没变 | 缓存没失效，或导入了别的同名模块 | 先 `ELC_CACHE=0` 重跑，再检查导入来源 |

## 相关指南

- [第一个程序](getting-started.md)：准备工具并运行源码。
- [命令行工具](practice/cli-tool.md)：组织可交付项目。
- [测试](stdlib/testing.md)：项目配置与断言。
