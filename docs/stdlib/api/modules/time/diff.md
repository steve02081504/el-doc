# time/diff.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间差 {#api-47aaf27b8c898de3f07b}

源码：`src/stdlib/time/diff.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/diff.el#L1)

表示固定时长和日历月差，并提供与时间单位的转换。

## TimeDiff {#api-b00bf50a6dead7622a2a}

源码：`src/stdlib/time/diff.el:27` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/diff.el#L27)

表示固定时长或日历月差；日历月只有结合日期和时区才能解析为固定时长。

```el-signature
export class TimeDiff extends TextOperand
```

**参数**：nanoseconds 固定纳秒分量。

**参数**：calendarMonths 日历月分量。

### 示例：创建固定时长

```el
import { TimeDiff } from "el:time/diff.el"
let delay = 5s
console.stdout.writeLine(delay.totalSeconds)
```
