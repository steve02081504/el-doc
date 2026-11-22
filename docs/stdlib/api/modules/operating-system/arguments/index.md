# operating-system/arguments/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/operating-system.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 命令行参数 {#api-eead0cf4005284c85ab4}

源码：`src/stdlib/operating-system/arguments/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/arguments/index.el#L1)

命令行参数相关接口。

## command_arguments {#api-63581d2f8e010264bb14}

源码：`src/stdlib/operating-system/arguments/index.el:12` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/arguments/index.el#L12)

读取平台提供的当前进程命令行参数。

```el-signature
export fn command_arguments(): Text[]
```

**返回类型**：[`Text`](../../text/text.md#api-6116e54b075df026a90a)[]

### 示例：使用示例

```el
import { command_arguments } from "el:operating-system/arguments/"
let arguments = command_arguments()
```
