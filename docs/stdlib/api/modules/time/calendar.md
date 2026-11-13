# time/calendar.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 公历换算 {#api-80c19ac225f896c0dad2}

源码：`src/stdlib/time/calendar.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L1)

提供公历字段、Unix 时间和时区偏移之间的换算。

## leapYear {#api-ad84a9fa89b0aa136c8f}

源码：`src/stdlib/time/calendar.el:18` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L18)

```el
export fn leapYear(year: Number): Bool
```

按公历 400 年规则判断指定年份是否为闰年。

**参数**：year 公历年份。

### 示例：示例

```el
import { leapYear } from "el:time/calendar.el"
leapYear(2000)
```
预期结果：真。

## monthDays {#api-e4a535b45fe088abf757}

源码：`src/stdlib/time/calendar.el:31` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L31)

```el
export fn monthDays(year: Number, month: Number): Number
```

返回该年月的天数；二月按闰年规则处理。

**参数**：year 公历年份。

**参数**：month 月份编号。

**注意**：本函数不校验年月；除二月和四个 30 天月份外，其他月份值均按 31 天处理。

### 示例：示例

```el
import { monthDays } from "el:time/calendar.el"
monthDays(2024, 2)
```
预期结果：29。

## epochDay {#api-950b85c66afa43590243}

源码：`src/stdlib/time/calendar.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L50)

```el
export fn epochDay(year: Number, month: Number, day: Number): Number
```

将公历年月日换算为自 1970-01-01 起的日数。

**参数**：year 公历年份。

**参数**：month 月份编号。

**参数**：day 当月日期。

**注意**：本函数不校验年月日字段；调用者应传入有效的公历日期。

### 示例：示例

```el
import { epochDay } from "el:time/calendar.el"
epochDay(1970, 1, 2)
```
预期结果：1。

## yearAtSeconds {#api-0924938c7200fc49f4ca}

源码：`src/stdlib/time/calendar.el:71` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L71)

```el
export fn yearAtSeconds(seconds: Number): Number
```

返回 Unix 秒数对应 UTC 日期所在的公历年份。

**参数**：seconds Unix 时间秒数。

**注意**：调用者应传入有限整数秒；本函数不校验输入。

### 示例：示例

```el
import { yearAtSeconds } from "el:time/calendar.el"
yearAtSeconds(0)
```
预期结果：1970。

## calendarAt {#api-3adcdd1b11385bb4eac1}

源码：`src/stdlib/time/calendar.el:133` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L133)

```el
export fn calendarAt(nanoseconds: Number, offset: TimeDiff = TimeDiff()): CalendarTime
```

把 Unix 纳秒和偏移量分解为公历字段。

**参数**：nanoseconds Unix 时间纳秒。

**参数**：offset 加到时间值上的偏移。

**失败与异常**：纳秒值非有限或非整数、或换算日期超出 CalendarTime 支持范围时抛 RangeError。

### 示例：示例

```el
import { calendarAt } from "el:time/calendar.el"
calendarAt(0).year
```
预期结果：1970。

## offsetText {#api-77dcea13bebddbd7baf5}

源码：`src/stdlib/time/calendar.el:160` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/calendar.el#L160)

```el
export fn offsetText(offset: TimeDiff): Text
```

将偏移量格式化为带符号的时区偏移文本。

**参数**：offset 要格式化的偏移。

### 示例：示例

```el
import { offsetText } from "el:time/calendar.el"
import { TimeDiff } from "el:time/diff.el"
offsetText(TimeDiff.seconds(19800))
```
预期结果：+05:30。
