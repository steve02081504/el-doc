# errors/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/errors.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 标准错误 {#api-55b7298932f4cac87b98}

源码：`src/stdlib/errors/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/index.el#L1)

汇集常用错误类型。

## RangeError {#api-390eebbefb11a3fdc270}

源码：`src/stdlib/errors/index.el:24` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/index.el#L24)

表示值超出允许范围的错误。

```el-signature
@assign(mode: "copy")
export class RangeError extends Error
```

### 示例：用法

```el
let error = RangeError()
```
