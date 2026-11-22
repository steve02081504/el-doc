# shell/session.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/shell.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## Shell 会话 {#api-e7e2b0b3fc591de88cd7}

源码：`src/stdlib/shell/session.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/shell/session.el#L1)

Shell 会话相关接口。

## ShellSession {#api-ea8f0bd23e365543937b}

源码：`src/stdlib/shell/session.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/shell/session.el#L63)

保存 shell 的逻辑文件系统位置、环境和启动策略。

```el-signature
@assign(mode: "shared")
export class ShellSession
```

### 示例：使用示例

```el
import { ShellSession } from "el:shell/"
let session = ShellSession()
```
