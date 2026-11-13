# time/instant.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间点 {#api-873001e83818aa3e9184}

源码：`src/stdlib/time/instant.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/instant.el#L1)

表示 Unix 纳秒时间点，并提供文本、日历和时区转换。

## TimeResolution {#api-9d758eb17ca9b412a29d}

源码：`src/stdlib/time/instant.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/instant.el#L31)

```el
export enum TimeResolution
```

选择本地时间映射到多个或零个时间点时的处理策略。

### 示例：示例

```el
import { TimeResolution } from "el:time/instant.el"
TimeResolution.Earlier
```
预期结果：选择较早的候选时间点。

## MonthOverflow {#api-759d477c1154e5461c89}

源码：`src/stdlib/time/instant.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/instant.el#L40)

```el
export enum MonthOverflow
```

选择按日历月移动时目标月份没有原日期的处理策略。

### 示例：示例

```el
import { MonthOverflow } from "el:time/instant.el"
MonthOverflow.Clamp
```
预期结果：将日期限制为目标月最后一天。
