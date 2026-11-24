# multimedia/video/mjpeg.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## MJPEG 视频帧 {#api-5106bc402baf65e9b526}

源码：`src/stdlib/multimedia/video/mjpeg.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/mjpeg.el#L1)

编解码数位帧和标准 JPEG 帧。

## encodeMjpeg {#api-977aec81f8b95a10a76a}

源码：`src/stdlib/multimedia/video/mjpeg.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/mjpeg.el#L68)

把单帧 RGBA 编码为无损数位 MJPEG。

```el-signature
export fn encodeMjpeg(image: RgbaImage, options: ImageEncodeOptions = ImageEncodeOptions()): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：用法

```el
// @external image: RgbaImage
let data = encodeMjpeg(image)
```

## decodeMjpeg {#api-1a5fd749892e976fa974}

源码：`src/stdlib/multimedia/video/mjpeg.el:80` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/mjpeg.el#L80)

按所选的基数配置解码单帧数位 MJPEG。

```el-signature
export fn decodeMjpeg(data: Number[], options: ImageDecodeOptions = ImageDecodeOptions()): RgbaImage
```

**返回类型**：[`RgbaImage`](../../../types.md#api-747cff86c10f647bf741)

### 示例：用法

```el
// @external data: Number[]
scope let image = decodeMjpeg(data)
```
