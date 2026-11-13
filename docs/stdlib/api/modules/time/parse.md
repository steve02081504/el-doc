# time/parse.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/time.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 时间文本解析 {#api-aea21d0748edb0785cdf}

源码：`src/stdlib/time/parse.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/parse.el#L1)

解析常见时间文本并返回结构化字段。

## parseTime {#api-d1e2465e19b2276f6ee0}

源码：`src/stdlib/time/parse.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/time/parse.el#L85)

```el
export fn parseTime(source: Text, standard: Bool): ParsedTime
```

解析时间文本并返回字段、偏移和解析状态。

**参数**：source 要解析的时间文本。

**参数**：standard 是否要求标准时间格式。

**失败与异常**：文本结构无效、精度超过纳秒、偏移缺失/未知/越界或日历字段无效时抛出相应解析错误或 RangeError。

### 示例：示例

```el
import { parseTime } from "el:time/parse.el"
import { t } from "el:language/values.el"
parseTime("1970-01-01T00:00:00Z", t).calendar.year
```
预期结果：1970。
