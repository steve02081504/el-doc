# 模块与包

> 一个只做两件事的 `main.els`：导入 `a.el`，打印一句话。可 `a.el` 又导入了 `b.el`——程序到底从哪一行开始跑？

!!! abstract "🎯 读完这页，你能"
    - 用三种 `import` 写法从别的模块取名字，并解释为什么没有 `import *`
    - 用 `export` 和 `package.eol` 把脚本拆成几个模块，让 `el run` 找得到入口
    - 判断目录、`index.el`、`.el` 与 `.els` 在导入时分别意味着什么

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[函数与闭包](functions.md)</span>

## 模块就是一个文件

模块顶层可以写声明和普通语句：`let`、`const`、`fn`、`class`、`interface`、`import`、`export`。==只有标了 `export` 的声明能被别的模块看到==，没标的都是模块私有。

```el
// math.el
export fn double(value: Number) { return value * 2 }

fn helper(value: Number) { return value + 1 }   // 私有，外部看不到

export let version = 1
```

同一个模块来源在一次进程里只初始化一次，重复导入共享同一份模块状态（语言规范第 8 章）。这条规则让模块顶层成为放常量、配置表和一次性初始化的地方，而不是每次导入都执行一遍的脚本。

!!! example "动手 30 秒"
    把 `math.el` 里的 `export let version = 1` 改成 `let version = 1`，再在另一个文件里 `import { version }`。编译器报找不到导出；看到这个错误，就说明没有 `export` 的声明确实是模块私有的。

## `import` 必须写出你要哪些名字

导入必须写出你要哪些名字，这是 EL 与 JavaScript 最大的不同。

| 写法 | 绑定什么 | 典型用途 |
| --- | --- | --- |
| `import { a, b as c } from "..."` | 具名导入，`as` 在本模块换名 | 明确知道要哪几个名字 |
| `import /模式/ from "..."` | 名字匹配模式的全部导出，绑定名就是导出名 | 按前缀取一组名字 |
| `import /模式/ as m from "..."` | 编译期命名空间，用 `m.名字` 访问 | 保留来源、避免同名冲突 |

```el
// 1. 具名导入，b 在本模块叫 c
import { readTextFile, writeTextFile as write } from "el:filesystem/"

// 2. 正则导入：把名字匹配 /^parse/ 的导出全部绑定到当前作用域
import /^parse/ from "file:./formats.el"

// 3. 正则导入加命名空间：只在 text 上按这次选中的集合解析
import /.*/ as text from "file:./text.el"
```

模式是写在两个斜杠之间的正则字面量，只在 `import` 或 `export` 之后的名字位置成立；其它位置的 `/` 仍然是除号。名字没被任何一条 import 选中的导出，在模块外不可见。命名空间是编译期的，不是运行期对象：`text.count` 这类访问在编译期解析到具体导出，`m` 本身不能保存、传递或比较。

EL 不提供 `import *`，也不提供只执行、不绑定名字的副作用导入。需要“导入即执行”的效果时，导入那个模块导出的函数并显式调用，或者把初始化写在模块顶层，让真正导入其名字的模块在初始化时执行它。所有 import 写法引入的名字都是只读绑定，给导入名赋值是编译期错误；要修改模块状态，必须通过模块导出的函数或它交出的共享对象。

## `export` 可以加在任意顶层声明前

```el
export fn run() { console.stdout.writeLine("running") }

export let limit = 10

@assign(mode: "shared") export class Box { let value: Number = 0 }

export interface Named { fn name(): Text }
```

除了逐条标注，还可以把别处的导出转发出去，转发保持原声明身份和活绑定，不建立本模块的普通导入绑定：

```el
export { parse, format as render } from "file:./text.el"
export /.*/ from "file:./internal.el"
```

同名函数经多条路径到达时会合并成一个重载族；其它同名但不同声明的冲突在编译期报错，用 `as` 显式改名是解决冲突的标准手段。

## 预导入（prelude）：不用写 import 的默认名字

每个模块默认导入标准库的 prelude，不需要写 `import`。基础值 `t`、`nil`、`void`，文本与集合 `Text`、`Array`、`Map`、`Set`、`BitSet`、`Sequence`，输出入口 `console`，以及 `typeof`、`assert`、`formats`、`spawn`、`parseJSON`、`readFileAs` 这些常用名字都在里面。

prelude 是普通模块，显式导入和本模块自己的声明优先，可以遮盖同名 prelude 绑定；未被遮盖的 prelude 名字同样是只读导入绑定。要关掉当前模块的默认导入，写模块属性 `@module(prelude: nil)`；关掉之后 `t`、`nil`、`void` 和常用类型都需要显式导入或自行定义，否则在用到的地方报编译错误。

??? note "可选 · 深入：关掉 prelude 的两种层级"
    `@runtime(prelude: nil)` 是程序级关闭，它只能出现在编译根模块上，并作为硬上限：被它关掉的项没有任何模块能再打开。`@module(prelude: nil)` 只影响当前模块。两者都写在模块属性位置，不是普通语句。

## 来源写法：导入的内容从哪里来

```el
import /.*/ from "file:./util.el"                 // 相对：以引用它的模块文件为基准
import /.*/ from "https://example.com/lib.el"     // HTTPS 来源
import /.*/ from "el:filesystem/"                 // 标准库来源
```

`file:` 相对路径以引用它的模块文件所在目录解析，不受进程工作目录影响。`el:` 是标准库前缀，背后是一张统一的来源映射表（项目配置的 `imports` 可以覆盖它），并不给标准库任何类型或初始化特权。

`file:` 来源指向一个目录时，等价于该目录下的 `index.el`：`import /.*/ from "file:./physics"` 与 `import /.*/ from "file:./physics/index.el"` 是同一个模块。目录里没有 `index.el` 时报读不到并给出它找的路径。

按平台选择不同来源时，把映射直接写在说明符位置，键是 `os-arch` 或目标三元组：

```el
import /.*/ as backend from @{ windows-x64: "file:./backend-win.el"; linux-x64: "file:./backend-linux.el" }
```

未命中任何键会在编译期报错并列出映射里已有的键，不会静默挑一项。

## `lazy import`：用到才装载

如果一个模块很大、或者只在少数路径上需要，可以用 `lazy import { renderReport } from "file:./report.el"` 推迟装载。`lazy import` 只能写非空的名字表，不支持正则形式；它按编译期真实的名字需求打开来源模块，只有真的用到选中名字时才装载。模块属性 `@module(gc: nil)` 关闭当前模块的 GC，只影响本模块，生命周期改走非 GC 路径。

## 模块没有 `main`：顶层代码就是入口

模块没有 `main` 函数。导入一个模块时，它的顶层语句按源码顺序逐条执行；执行到某条 `import` 时先递归初始化目标模块，目标完成后才回到当前位置继续（语言规范第 8 章）。入口模块也一样。

```el
// main.els
import { greeting } from "file:./a.el"

console.stdout.writeLine(greeting())
```

导入 `a.el` 时先执行它的顶层语句；`a.el` 里的 import 又先执行 `b.el`，如此深度优先，回到 `main.els` 后才轮到那行 `writeLine`。程序的入口由项目配置的 `entry` 或 `el run` 的参数指定；顶层结束后进程还会等待已经启动的异步活动自然结束。

??? question "先猜：`a.el` 和 `b.el` 互相导入时，还能读对方顶层声明的 `let` 吗？"
    不能依赖它已经初始化。循环导入只允许在函数层面安全使用：互相导入的模块可以提前登记对方的函数，任何一方在初始化期间直接读取对方还没初始化的 `let` 都会抛模块初始化错误。让顶层只放声明，把读写推迟到函数里，顺序就不影响结果。

## `package.eol`：项目配置

项目根用一个配置文件描述入口、来源映射与测试范围，文件名固定为 `package.eol`，二进制形式是 `package.eod`。两者同时出现在同一目录会按歧义报错。

```eol
@{
	entry: "src/main.els",
	imports: { "app/": "./src/" },
	tests: {
		include: ["tests/**/*.test.el"],
		sources: ["src/**/*.el", "src/**/*.els"],
		exclude: [],
		inputs: []
	}
}
```

配置分区是 `entry`、`imports`、`dependencies`、`targets`、`updates`、`cache`、`permissions`、`tests`，未知字段直接报错。配置里的路径以项目根为基准，不是进程工作目录。`el run`、`el build`、`el test`、`el docs` 会从当前目录向上找最近的 `package.eol`／`package.eod` 来确定项目根。

`.el` 是普通源码模块，后缀在 import 里必须显式写出来。`.els` 是执行入口使用的同一 EL 语言，执行命令同样接受它；import 的文件仍然只认 `.el`，目录仍然展开 `index.el`。把入口写成 `.els` 只是一种约定，方便宿主做双击执行的文件关联，它不改变语言语义。

## 目录怎么摆：一个入口，若干模块

```text
my-app/
	package.eol
	src/main.els
	src/math.el
	src/text/index.el
	src/text/format.el
	tests/math.test.el
```

几条经验：一个目录对外只通过 `index.el` 暴露入口；目录里不要让超过三个 `.el` 文件共享同一个首词或末词（格式化器会把这种情况报出来，建议改成子目录）；跨模块只通过 `export` 交流，不要靠导入顺序碰运气。

## 完整例子：两个模块相互导入

`a.el` 导出 `name` 和 `greeting`，`b.el` 导出 `welcome`，两者互相导入，但顶层只放声明。

```el
// b.el
import { name } from "file:./a.el"

export fn welcome() {
	return "i am b"
}

export fn describe() {
	return welcome() + ", " + name()
}

// a.el
import { welcome } from "file:./b.el"

export fn name() {
	return "a"
}

export fn greeting() {
	return welcome() + " 看到 " + name()
}
```

```el
// main.els
import { greeting } from "file:./a.el"

console.stdout.writeLine(greeting())
```

输出是 `i am b 看到 a`。两个模块在顶层都没有读取对方的变量，只登记了函数，因此初始化顺序不影响结果；真正调用发生在 `main.els` 的顶层语句里，这时两边都已经初始化完成。

!!! warning "常见坑：四个导入期的错误"
    - **写 `import *`。** EL 没有这个写法，按正则全量导入要写 `import /.*/ from "..."`；只想执行不绑定名字的副作用导入也没有。
    - **目录少 `index.el`。** 导入目录会报读不到，并在错误里给出它找的路径；补上 `index.el`，或把说明符写成完整文件名。
    - **把 `.els` 写进 import。** import 只认 `.el`；`.els` 只是入口约定，不改变语言语义，也不能被导入。
    - **把命名空间当值。** `m` 是编译期命名空间，不能保存、传递或比较；需要传递行为时传导出的函数或对象。

## 带走这三样

- 一个模块就是一个文件，只有 `export` 的名字对外可见；模块来源每进程只初始化一次。
- 三种 import 都要写出拿哪些名字；命名空间只在编译期存在，没有 `import *`。
- `package.eol` 的 `entry` 决定入口，`imports` 决定来源映射；`file:` 相对路径以模块文件为基准，目录自动找 `index.el`。

## 下一站：Shell 语法

> 代码已经能拆成模块了，那 EL 能不能直接当 shell 脚本用，把命令、管道和退出码也写进同一份源码？

- 主推进：[Shell 语法](shell.md)：把 EL 当脚本语言用，直接执行命令、接管道、读退出码。
- 想先练手：[命令行工具](../practice/cli-tool.md)：用模块和 `package.eol` 组织一个能跑的小项目。
