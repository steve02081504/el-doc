# time/calendar.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 公历换算 {#api-80c19ac225f896c0dad2}

源码：`src/stdlib/time/calendar.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L1)

提供公历字段、Unix 时间和时区偏移之间的换算。

## leapYear {#api-ad84a9fa89b0aa136c8f}

源码：`src/stdlib/time/calendar.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L19)

```el
export fn leapYear(year: Number): Bool
```

**返回类型**：[`Bool`](../language/values.md#api-3f0af31783849ef30c6e)

按公历 400 年规则判断指定年份是否为闰年。

**参数**：year 公历年份。

### 示例：检查闰年

```el
import { leapYear } from "el:time/calendar.el"
leapYear(2000)
```
预期结果：真。

**返回值**：Bool。

## monthDays {#api-e4a535b45fe088abf757}

源码：`src/stdlib/time/calendar.el:33` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L33)

```el
export fn monthDays(year: Number, month: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

返回该年月的天数；二月按闰年规则处理。

**参数**：year 公历年份。

**参数**：month 月份编号。

**注意**：本函数不校验年月；2 月返回 28 或 29，4、6、9、11 月返回 30，其他月份值均返回 31。

### 示例：取得闰年二月的天数

```el
import { monthDays } from "el:time/calendar.el"
monthDays(2024, 2)
```
预期结果：29。

**返回值**：月份天数。

## epochDay {#api-950b85c66afa43590243}

源码：`src/stdlib/time/calendar.el:53` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L53)

```el
export fn epochDay(year: Number, month: Number, day: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

将公历年月日换算为自 1970-01-01 起的日数。

**参数**：year 公历年份。

**参数**：month 月份编号。

**参数**：day 当月日期。

**注意**：本函数不校验年月日字段；调用者应传入有效的公历日期。

### 示例：换算纪元日

```el
import { epochDay } from "el:time/calendar.el"
epochDay(1970, 1, 2)
```
预期结果：1。

**返回值**：相对 1970-01-01 的日数。

## yearAtSeconds {#api-0924938c7200fc49f4ca}

源码：`src/stdlib/time/calendar.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L75)

```el
export fn yearAtSeconds(seconds: Number): Number
```

**返回类型**：[`Number`](../number/number.md#api-3cc24d3ef702e8652fb4)

返回 Unix 秒数对应 UTC 日期所在的公历年份。

**参数**：seconds Unix 时间秒数。

**注意**：调用者应传入有限整数秒；本函数不校验输入。

### 示例：取得 Unix 时间对应年份

```el
import { yearAtSeconds } from "el:time/calendar.el"
yearAtSeconds(0)
```
预期结果：1970。

**返回值**：UTC 公历年份。

## calendarAt {#api-3adcdd1b11385bb4eac1}

源码：`src/stdlib/time/calendar.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L138)

```el
export fn calendarAt(nanoseconds: Number, offset: TimeDiff = TimeDiff()): CalendarTime
```

**返回类型**：[`CalendarTime`](../../types.md#api-3e2d30f2355f28e55020)

把 Unix 纳秒和偏移量分解为公历字段。

**参数**：nanoseconds Unix 时间纳秒。

**参数**：offset 加到时间值上的偏移。

**失败与异常**：纳秒值非有限或非整数、或换算日期超出 CalendarTime 支持范围时抛 RangeError。

### 示例：换算 Unix 纳秒时间

```el
import { calendarAt } from "el:time/calendar.el"
calendarAt(0).year
```
预期结果：1970。

**返回值**：CalendarTime；要求时间字段位于其支持范围。

## offsetText {#api-77dcea13bebddbd7baf5}

源码：`src/stdlib/time/calendar.el:166` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L166)

```el
export fn offsetText(offset: TimeDiff): Text
```

**返回类型**：[`Text`](../text/text.md#api-6116e54b075df026a90a)

将偏移量格式化为带符号的时区偏移文本。

**参数**：offset 要格式化的偏移。

### 示例：格式化时区偏移

```el
import { offsetText } from "el:time/calendar.el"
import { TimeDiff } from "el:time/diff.el"
offsetText(TimeDiff.seconds(19800))
```
预期结果：+05:30。

**返回值**：带符号的时区偏移文本。
