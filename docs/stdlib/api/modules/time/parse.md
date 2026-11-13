# time/parse.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间文本解析 {#api-aea21d0748edb0785cdf}

源码：`src/stdlib/time/parse.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/parse.el#L1)

解析常见时间文本并返回结构化字段。

## parseTime {#api-d1e2465e19b2276f6ee0}

源码：`src/stdlib/time/parse.el:86` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/parse.el#L86)

解析时间文本并返回字段、偏移和解析状态。

```el
export fn parseTime(source: Text, standard: Bool): ParsedTime
```

**返回类型**：[`ParsedTime`](../../types.md#api-0d1958b2407e78d1230d)

**参数**：source 要解析的时间文本。

**参数**：standard 是否要求标准时间格式。

**失败与异常**：格式无效时抛 InvalidTimeText；小数精度超过九位时抛 TimePrecisionExceedsNanoseconds；缺少标准格式要求的偏移时抛 TimeRequiresExplicitOffset；未知零偏移时抛 UnknownTimeOffset；偏移或日期字段越界时抛 RangeError。

### 示例：解析带 UTC 偏移的时间

```el
import { parseTime } from "el:time/parse.el"
import { t } from "el:language/values.el"
parseTime("1970-01-01T00:00:00Z", t).calendar.year
```
预期结果：1970。

**返回值**：ParsedTime，包含解析所得的 calendar 和 hasOffset。
