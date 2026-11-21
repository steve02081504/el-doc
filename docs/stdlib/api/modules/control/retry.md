# control/retry.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/control.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## until {#api-047fe3a9b4d31df55152}

源码：`src/stdlib/control/retry.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/control/retry.el#L30)

执行块直到成功，并返回成功那次的结果。匹配的 catch 执行完后重试；未匹配的异常或处理器抛出的异常向外传播。
可以省略 catch，此时块只执行一次。

```el
export syntax until
```

### 示例：读取指定范围内的整行整数

```el
let value = until {
	console.stdin.readLineAs(parsers.integer(min: 80, max: 560))
} catch (error: RangeError) {
	console.stderr.writeLine("请输入 80 到 560 之间的整数")
}
```
