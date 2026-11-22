# console/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/console.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 控制台记录模型 {#api-6aa5796291bac47b4e3c}

源码：`src/stdlib/console/model.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/model.el#L1)

控制台记录模型相关接口。

## stdoutChannel {#api-52fbcf8e92e35a2e0242}

源码：`src/stdlib/console/model.el:59` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/model.el#L59)

标准输出的逻辑通道；通道标识目的地，不表示日志级别。

```el-signature
export const stdoutChannel = ConsoleChannel("stdout")
```

**类型**：[`ConsoleChannel`](../../types.md#api-014dddb6e6d5af8b8537)

### 示例：使用示例

```el
import { stdoutChannel } from "el:console/"
let name = stdoutChannel.name
```

## ConsoleLevel {#api-bcca0db28d7f511b4f1f}

源码：`src/stdlib/console/model.el:69` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/model.el#L69)

控制台记录的日志等级，从 None 到 Fatal。

```el-signature
export enum ConsoleLevel
```

### 示例：选择信息等级

```el
import { ConsoleLevel } from "el:console/"
let level = ConsoleLevel.Info
```
