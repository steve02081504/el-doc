# multimedia/qr/encode.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 二维码编码 {#api-14bb3dc76765a0c1caa7}

源码：`src/stdlib/multimedia/qr/encode.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/qr/encode.el#L1)

生成二维码矩阵和图像。

## encodeQrImage {#api-47b93c43343b402a7dd5}

源码：`src/stdlib/multimedia/qr/encode.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/qr/encode.el#L118)

把二维码渲染为使用所选基数的数位 PNG 图像。

```el-signature
export fn encodeQrImage(text: Text, options: QrEncodeOptions = QrEncodeOptions(), scale: Number = 8, quietZone: Number = 4, radix: Number | nil_t = nil): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：用法

```el
let data = encodeQrImage("你好，EL！")
```
