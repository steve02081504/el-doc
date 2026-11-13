# 模块与导入

## 模块身份与导出

EL 模块由解析后的源码来源确定身份。模块顶层允许执行代码，不要求 `main` 函数；依赖模块在进程内按模块初始化规则只初始化一次。导出名字供其他模块导入。

## 导入形式

下列各行展示独立形式，不应在同一模块重复导入相同绑定。

```el
import { run, helper as h } from "file:./tools.el"
import /^run/ from "file:./tools.el"
import /.*/ from "file:./tools.el"
import /.*/ as tools from "file:./tools.el"
```

每种普通导入都明确选择名字。以上分别展示具名导入、正则选择、全量选择和编译期命名空间。EL 没有 `import *`、副作用导入或运行期命名空间值。直接导入名是活绑定；保存下来的函数值保持其取得时的版本。

## 惰性具名导入

惰性导入必须列出非空具名表，可以逐项重命名。下列两行分别展示导入与重导出：

```el
lazy import { compute as calculate } from "file:./backend.el"
export lazy import { compute as calculate } from "file:./backend.el"
```

惰性导入不是运行期首次访问才打开模块；编译期名称解析实际选择某个导入绑定时，才按需打开来源模块并使其参与编译。运行期初始化仍遵守模块初始化规则。没有被引用的名字不会触发来源模块。惰性重导出保留延迟关系，消费者实际引用转发名时需求才传递到来源。

`lazy import` 和 `export lazy import` 禁止正则名字选择，即使正则只匹配单个名称也不例外；这是明确的设计限制。普通 `import /pattern/` 与普通正则重导出仍可用。

## 相关条目

- [声明与绑定](declarations.md)
- [模块教程](../../language/modules.md)
- [模块规范](https://github.com/steve02081504/el/blob/master/docs/spec/08-modules.md)
- [惰性绑定与导入](https://github.com/steve02081504/el/blob/master/docs/spec/deferred-bindings-and-imports.md)
