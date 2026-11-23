# shell/syntax.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/shell.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## Shell 语法 {#api-fa51939e0932dd3328e2}

源码：`src/stdlib/shell/syntax.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/shell/syntax.el#L1)

Shell 语法相关接口。

## shell {#api-6cfa26a5700765b0f4d6}

源码：`src/stdlib/shell/syntax.el:218` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/shell/syntax.el#L218)

在块中使用 shell 风格的命令和表达式语法。

```el-signature
export syntax shell
```

### 示例：使用示例

```el
import { shell } from "el:shell/"
let result = shell { 1 + 2 }
```
