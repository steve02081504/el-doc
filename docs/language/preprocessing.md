# 文件预处理

> `#define COLOR blue` 之后，连字符串 `"COLOR"` 都会变成 `"blue"`：动手的不是词法分析，而是文件预处理。

!!! abstract "🎯 读完这页，你能"
    - 判断一行以 `#` 开头的内容是不是指令，并说出预处理在编译流程里的位置
    - 写出一段共享宏的 `#include`，并在需要模块边界时改用 `import`
    - 写出受限条件，用 `#else_if true` 兜底，并解释 `defined(...)` 与 `time(...)` 的边界

    <span class="el-chip">⏱ 约 12 分钟</span> <span class="el-chip">前置：[模块与包](modules.md)</span>

查询完整条件语法、集合 include 或预定义来源值，见[文件预处理参考](../reference/language/preprocessing.md)。

## 预处理在词法分析之前改一遍文本

每个源码模块先取得源文本快照，再依次经过文件预处理、普通词法、接口发现、源码宏展开与类型检查（语言规范的文件预处理部分）。
预处理是最早的一步，读的还是文本：只做确定的文本改写，不运行 EL。
它不是完整的 C 预处理：识别指令时感知 `//`、`/* ... */` 注释，以及字符串、模板文字、自定义原文字面量的定界符，既避免把注释或字面量里的 `#` 当成指令入口，也把指令参数里的注释当空白。
普通行的注释剥离和未闭合注释诊断仍归词法分析：active 普通行保留原有注释字符，替换后的文本再交给词法。

八条指令各占一条物理行：行首可有空格或制表符，`#` 后是完整指令名，名字后必须是空白或行尾。

| 指令 | 作用 |
| --- | --- |
| `#define NAME replacement` | 记录名字和这一行余下的替换文本 |
| `#undefine NAME` | 删除一个宏定义 |
| `#include "source-specifier"` | 把来源文本粘贴到当前位置 |
| `#if condition` | 开始一个条件区 |
| `#else_if condition` | 当前面条件未命中时再试一个条件 |
| `#end_if` | 结束条件区 |
| `#error "message"` | 报错并终止本次预处理 |
| `#warning 'message'` | 留下带位置的警告后继续处理 |

`#error` 与 `#warning` 的消息必须是字符串字面量，单引号、双引号或反引号都行，不接受裸文本或拼接。
拼写要照抄：是 `#undefine`、`#else_if`、`#end_if`，没有 `#undef`、`#else`、`#ifdef`、`#ifndef`；不认识的 `#name` 不归预处理，会留给原生或扩展词法。

## 替换是机械的，字符串也逃不掉

`#define` 只记录名字和这一行余下的原始替换文本。
名字与替换体间的空白只是分隔符，不属于替换体；替换体可以为空。
重复 define 会替换旧定义；`#undefine` 未定义的名字是无操作，预定义项不能被 define 或 undefine。

替换按完整名称匹配、区分大小写，不会在更长的名字或数字片段里替换子串，也不认识参数、类型、表达式或绑定。
没有函数式 define、`##`、C 的字符串化，也没有反斜杠续接；`#define COLOR blue` 只表示把独立的 `COLOR` 换成 `blue`。

```el
#define COLOR blue
let description = "COLOR"
let COLORFUL = 1
console.stdout.writeLine(description)
```

字符串里的 `COLOR` 也会被换掉，所以输出是 `blue` 不是 `COLOR`；`COLORFUL` 不在完整名称边界上，保持原样。
替换发生在 active 普通行的原文字上，包括字符串字面量、DSL 和保留的注释文字，不做智能转义、引号增删或类型适配。

!!! example "动手 30 秒"
    把 `#define COLOR blue` 改成 `#define COLOR red`，其余不动，再运行同一段。
    字符串仍写 `"COLOR"`，输出从 `blue` 变成 `red`，就说明替换发生在词法分析之前，且不认字符串边界。

替换不是在 `#define` 时提前做完的，而是每次引用时在当时环境里递归展开：先 `#define A B` 再 `#define B 2`，之后引用 `A` 得到 `2`。
之后重新 `#define B`，下一次引用 `A` 也跟着变；直接或间接递归会给出带位置的诊断并列出展开链，不会留下半展开 token 或无限循环。
替换结果不会被重新识别成指令。

**三个来源文本值也走机械替换。**
`__BUILTIN_FILEPATH__` 是当前引用点源 URI 的带引号且正确转义的 EL 字符串字面量。
`__BUILTIN_LINENUMBER__` 是引用点从 1 起的物理行号；include 文本里取 include 文件行号，不是 define 定义行。
`__EVIL_EDITION__` 是当前编译器产物构建时间的 Unix 整数秒，不是语言版本，也不是编译你程序时的当前时间。
机械替换不因名字落在字符串里就自动去引号：

```el
let path = __BUILTIN_FILEPATH__
let line = "__BUILTIN_LINENUMBER__"
let bad = "__BUILTIN_FILEPATH__"   // 会再嵌一层引号，通常是词法错误
```

第一行得到来源文本值；第二行把数字嵌进现有字符串；第三行嵌套引号，通常是词法错误。
要保留名字本身就把拼写拆开，例如 `"__BUILTIN_" + "FILEPATH__"`；旧拼写 `__BUILTIN_LINENUMER__` 不提供别名。

??? note "可选 · 深入：`__BUILTIN_FUNCTION_INFO__` 与几条边界"
    `__BUILTIN_FUNCTION_INFO__` 不是文本替换项，而是保留的原生表达式，文件阶段把它原样留给后面的正常函数语义。
    它产生一个位置快照对象，字段是 `name`、`kind`、`module`、`file`、`line`、`column`；`name` 是当前词法函数的声明名，匿名函数为空，`kind` 是 `function` 或 `lambda`，位置指向声明头。
    它不能在模块顶层使用；写在字符串里时只是字符串内容，没有插值。

    默认实现把展开、include 与条件表达式的嵌套深度限制在 128，一次模块的替换次数限制为 1,000,000，展开后的 Unicode 标量数限制为 67,108,864，越界会给出明确诊断，不静默截断。
    每个文件的条件必须在该文件闭合，`#include` 不跨文件关闭条件区。
    替换产物的主诊断指向引用点并附定义点，include 里的普通文本指向 include 文件及其调用链；模块归属不因诊断位置改变。

## 条件不是 EL 表达式

`#if` 和 `#else_if` 后面的条件语言不运行 EL，也不调用用户函数、getter、宏展开器或 I/O。
支持的东西只有这些：

- 十进制整数、正负号，以及 `true`／`false`（`t`／`nil` 等价）；整数零为假，其余为真。
- `defined('NAME')`、`defined("NAME")`，也可以不写引号写成 `defined(NAME)`。
- `time('timestamp')` 或双引号形式，返回精确的 Unix 秒常量。
- 比较 `== != < <= > >=`、括号、`!`、`&`、`|`，优先级从高到低是括号与前缀、比较、`&`、`|`。

条件里没有算术、字符串比较、连锁比较或一般函数调用，也没有 C 的 `&&`／`||`。
未知的裸名字不按零猜测，active 条件里直接报诊断。

??? question "先猜：条件里的宏名都会先被展开吗？"
    不是。
    普通宏会先在条件里机械展开，但 `defined(...)` 和 `time(...)` 的操作数是字面内容，不先做宏替换；`defined` 只接受单个未转义的宏名。

`time` 接受 `YYYY-MM-DD`（该日 UTC 午夜）或带显式偏移的 `YYYY-MM-DDTHH:MM:SS[.fraction](Z|±HH:MM)`，最多九位小数秒。
它按前推 Gregorian 日历处理 0001–9999 年，验证月日、时分秒与偏移，拒绝闰秒 60、`-00:00`、无时区完整日期时间、locale 格式和尾随字符。
不同偏移表示同一时刻时比较相等；它不读当前时间、环境时区或夏令时数据库，所以条件是确定的。

没有 `#else`，默认分支写 `#else_if true`：`true` 恒真，它就是兜底。

??? question "先猜：`#if false` 里写一个指向不存在文件的 `#include`，编译会报错吗？"
    不会。
    inactive 区域只扫描条件指令来维护嵌套与文件闭合，不展开宏、不读 include、不做 import 发现，也不触发 `#error`／`#warning`；普通文本不必是合法 EL，但注释与条件嵌套结构仍要成立。
    已命中之后，`#else_if` 条件不再求值。

所以在 `#if false` 里能安全放置平台专用或尚未完成的代码。

!!! warning "常见坑：条件照 EL 写逻辑运算符"
    **现象：** 假设 `VERSION` 已定义成整数，写 `#if VERSION >= 7 && VERSION < 9`，条件处直接报诊断。

    条件不是 EL 表达式，`&&`、`||`、算术和连锁比较都不支持；布尔组合改用 `&`、`|`，每个比较单独写完整。

## include 是文本粘贴，import 才是模块边界

`#include` 是文本包含：内容粘贴到指令位置，不创建模块、初始化器或独立声明身份，粘进来的声明仍属宿主模块。
它与当前文件共用宏环境：include 里的 `#define` 从发生位置起影响后续 include 内容和返回后的当前文件；环境在模块预处理结束时销毁，不导出给导入者或兄弟模块。
活动 include 成环会被拒绝，没有 C 的 include guard 例外。

| 维度 | `#include` | 普通 `import` |
| --- | --- | --- |
| 语义 | 文本包含 | 模块加载 |
| 宏环境 | 与当前文件共用 | 从只含预定义项的新环境开始 |
| 声明归属 | 属于宿主模块 | 属于被导入模块 |
| 循环 | 活动 include 环被拒绝 | 按模块导入规则处理 |

普通 `import` 按模块加载，模块从只含预定义项的新宏环境开始，所以它的 define 不会漏进当前文件。
代码组织用 `import`；只有要把文本原样拼进当前文件时才用 `#include`。

`#include` 的来源经机械替换后必须恰好是一个字符串字面量：单引号、双引号或不带插值的反引号字符串都行，转义按 EL 字符串规则解码。
裸路径、尾随表达式、模板插值都不接受；字符串里的 `//` 是内容不是注释，不会被当成行注释截断。

本地来源的例子：

```el
// main.el
#define SIZE 3

#include "file:./parts/defines.el"

#if defined('SIZE') & SIZE == 4
console.stdout.writeLine("sized")
#end_if
```

```el
// parts/defines.el
#define SIZE 4
```

`file:` 的 `./`、`../` 相对引用以写下这条指令的文件位置为基准解析。
include 进来的 `#define SIZE 4` 覆盖原来的 3，条件命中，输出 `sized`；用 `import` 装载同一份文件时，那份文件的 define 只活在各自模块，当前 `SIZE` 仍是 3，不会输出 `sized`。

!!! note "实现状态"
    指令、本地 `file:` include 与预定义来源文本值已实现；`http:`／`https:` 映射和真实网络获取尚未验证，本页例子只用本地来源，不要假设跨网络 include 一定可用。

## 带走这三样

- 预处理在词法分析之前按物理行改写文本；它只负责指令和替换，注释剥离仍归词法。
- 替换只认完整名字，字符串和保留注释也逃不掉；递归展开在引用点发生，成环会报错。
- `#include` 共享当前宏环境、不创建模块身份，要隔离就用 `import`；条件不是 EL，默认分支写 `#else_if true`。

## 下一站：[Shell 语法](shell.md)

> 条件、文本都拼好了；EL 能不能直接当 shell 脚本，把命令、管道和退出码写进同一份源码？

- 主推进：[Shell 语法](shell.md)：把 EL 当脚本语言用，直接执行命令、接管道、读退出码。
