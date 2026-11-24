# multimedia/image/codec.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 图像编码接口 {#api-43ed239111585c1a03d8}

源码：`src/stdlib/multimedia/image/codec.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L1)

提供数位和标准图像编解码入口。

## imageCodecSupport {#api-eb24081bf335eaa45247}

源码：`src/stdlib/multimedia/image/codec.el:97` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L97)

报告所选图像格式的数位编码支持。

```el-signature
export fn imageCodecSupport(format: ImageFormat): ImageCodecSupport
```

**返回类型**：[`ImageCodecSupport`](../../../types.md#api-08a4b9b8e60e2f9a025a)

### 示例：用法

```el
let support = imageCodecSupport(ImageFormat.Png)
```

## detectImageFormat {#api-56a9120303e630c747c5}

源码：`src/stdlib/multimedia/image/codec.el:109` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L109)

从头部识别 EL 数位图像的格式。

```el-signature
export fn detectImageFormat(data: Number[]): ImageFormat
```

**返回类型**：[`ImageFormat`](model.md#api-03af9bd9ab3a0721c70a)

### 示例：用法

```el
// @external data: Number[]
let format = detectImageFormat(data)
```

## inspectImage {#api-f19d2a5d0c1f5c98e0d9}

源码：`src/stdlib/multimedia/image/codec.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L118)

校验数位图像并返回格式、尺寸和帧数。

```el-signature
export fn inspectImage(data: Number[], options: ImageDecodeOptions = ImageDecodeOptions()): ImageInfo
```

**返回类型**：[`ImageInfo`](../../../types.md#api-e25ec990dc1cf12364ab)

### 示例：用法

```el
// @external data: Number[]
let info = inspectImage(data)
```

## decodeImage {#api-06ca12845379a23a45c2}

源码：`src/stdlib/multimedia/image/codec.el:134` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L134)

按请求的基数配置读取数位图像，保留 RGBA8 通道值。

```el-signature
export fn decodeImage(data: Number[], options: ImageDecodeOptions = ImageDecodeOptions()): RgbaImage
```

**返回类型**：[`RgbaImage`](../../../types.md#api-747cff86c10f647bf741)

### 示例：用法

```el
// @external data: Number[]
scope let image = decodeImage(data)
```

## encodeImage {#api-83f1b4b6cacb666c10e8}

源码：`src/stdlib/multimedia/image/codec.el:146` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/codec.el#L146)

使用所选格式标识编码无损 RGBA8。基数缺省为目标数位基数。

```el-signature
export fn encodeImage(image: RgbaImage, format: ImageFormat, options: ImageEncodeOptions = ImageEncodeOptions()): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：用法

```el
// @external image: RgbaImage
let data = encodeImage(image, ImageFormat.Png)
```
