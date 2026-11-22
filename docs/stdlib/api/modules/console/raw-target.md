# console/raw-target.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/console.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 原始控制台目标 {#api-bf96377017c7c9e52e4f}

源码：`src/stdlib/console/raw-target.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/raw-target.el#L1)

原始控制台目标相关接口。

## rawStdout {#api-ca81568025084c9c0796}

源码：`src/stdlib/console/raw-target.el:67` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/raw-target.el#L67)

直接写入操作系统标准输出的原始目标，不经过任务路由。

```el-signature
export const rawStdout = RawConsoleTarget(stdoutChannel)
```

**类型**：[`RawConsoleTarget`](../../types.md#api-cc1b45f887ff9dda12c5)

**失败与异常**：句柄无效或发生短写时抛出 ConsoleWriteError。

### 示例：使用示例

```el
import { rawStdout } from "el:console/"
rawStdout.writeLine("Hello")
```
