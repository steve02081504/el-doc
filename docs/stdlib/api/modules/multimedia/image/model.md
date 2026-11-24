# multimedia/image/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 图像格式与像素模型 {#api-778bba25e6854d6a4a14}

源码：`src/stdlib/multimedia/image/model.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/model.el#L1)

声明格式标识、图像选项和 RGBA8 像素存储。

## ImageFormat {#api-03af9bd9ab3a0721c70a}

源码：`src/stdlib/multimedia/image/model.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/model.el#L20)

选择 PNG、JPEG 或 AVIF 图像家族。

```el-signature
export enum ImageFormat
```

### 示例：选择 PNG

```el
import { ImageFormat } from "el:multimedia/image/"
let format = ImageFormat.Png
```
