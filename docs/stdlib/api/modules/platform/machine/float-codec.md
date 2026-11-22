# platform/machine/float-codec.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/platform.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 目标原生浮点载体 {#api-8aab127d25505dc30c8e}

源码：`src/stdlib/platform/machine/float-codec.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/machine/float-codec.el#L1)

声明目标相关的浮点存储载体和可选编解码器描述接口。

## NativeFloatExponent5 {#api-f145036e3b661f9b51a3}

源码：`src/stdlib/platform/machine/float-codec.el:13` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/machine/float-codec.el#L13)

表示存储指数位数为 5 的目标原生浮点数载体；具体格式由目标编解码器决定。

```el-signature
export @builtin:vome:float:number(exponent: 5) class NativeFloatExponent5
```

### 示例：选择五位指数浮点载体

```el
let Carrier: type = NativeFloatExponent5
```
