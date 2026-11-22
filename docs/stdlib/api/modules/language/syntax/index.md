# language/syntax/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/language.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 语法对象 {#api-ebef0086d921da7e84a9}

源码：`src/stdlib/language/syntax/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/syntax/index.el#L1)

语法对象相关接口。

## UncheckedSyntax {#api-3628c09626a9be6ba1ba}

源码：`src/stdlib/language/syntax/index.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/language/syntax/index.el#L122)

表示尚未检查的语法对象，持有不透明的会话句柄；句柄不能伪造、跨会话使用或在失效后使用。

```el-signature
@assign(mode: "shared")
export class UncheckedSyntax
```

### 示例：用法

```el
import { UncheckedSyntax } from "el:language/syntax/index.el"
fn syntaxKind(node: UncheckedSyntax) { return node.kind() }
```
