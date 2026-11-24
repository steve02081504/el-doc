# multimedia/image/files.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 图像文件读写 {#api-e56918903e01dbd9300e}

源码：`src/stdlib/multimedia/image/files.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/files.el#L1)

读写选定数位配置或标准协议的图像文件。

## readStandardImage {#api-daab2a7b5b399b519a17}

源码：`src/stdlib/multimedia/image/files.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/files.el#L23)

显式读取标准协议图像，按文件签名选择 PNG、JPEG 或 AVIF。

```el-signature
export fn readStandardImage(path, options: ImageDecodeOptions = ImageDecodeOptions()): RgbaImage
```

**返回类型**：[`RgbaImage`](../../../types.md#api-747cff86c10f647bf741)

### 示例：用法

```el
scope let image = readStandardImage("exchange.png")
```

## readImage {#api-02c43208de8a6f510847}

源码：`src/stdlib/multimedia/image/files.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/files.el#L47)

按所选的基数配置读取数位图像。

```el-signature
export fn readImage(path, options: ImageDecodeOptions = ImageDecodeOptions()): RgbaImage
```

**返回类型**：[`RgbaImage`](../../../types.md#api-747cff86c10f647bf741)

### 示例：用法

```el
scope let image = readImage("photo.png")
```

## inspectImageFile {#api-2654a5ecb339f5011269}

源码：`src/stdlib/multimedia/image/files.el:57` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/files.el#L57)

校验数位图像文件并返回格式、尺寸和帧数。

```el-signature
export fn inspectImageFile(path, options: ImageDecodeOptions = ImageDecodeOptions()): ImageInfo
```

**返回类型**：[`ImageInfo`](../../../types.md#api-e25ec990dc1cf12364ab)

### 示例：用法

```el
let info = inspectImageFile("photo.png")
```

## writeImage {#api-87b76e06cc8ca0f1ad9d}

源码：`src/stdlib/multimedia/image/files.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/files.el#L68)

以所选的数位格式标识写出无损 RGBA8 图像。

```el-signature
export fn writeImage(path, image: RgbaImage, format: ImageFormat, options: ImageEncodeOptions = ImageEncodeOptions())
```

### 示例：用法

```el
// @external image: RgbaImage
writeImage("photo.png", image, ImageFormat.Png)
```
