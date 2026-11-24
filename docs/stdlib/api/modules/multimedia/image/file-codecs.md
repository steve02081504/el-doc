# multimedia/image/file-codecs.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 图像文件格式对象 {#api-acceb7255d418c94bef9}

源码：`src/stdlib/multimedia/image/file-codecs.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/file-codecs.el#L1)

为通用文件读写构造图像配置。

## nativeImageFileCodec {#api-e08c79e02f406f3b3231}

源码：`src/stdlib/multimedia/image/file-codecs.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/file-codecs.el#L21)

创建读写均使用所选数位配置的图像文件格式对象。

```el-signature
export fn nativeImageFileCodec(format: ImageFormat, decoding: ImageDecodeOptions = ImageDecodeOptions())
```

### 示例：用法

```el
let format = nativeImageFileCodec(ImageFormat.Png)
```

## standardImageFileCodec {#api-6676145ad12ed3113070}

源码：`src/stdlib/multimedia/image/file-codecs.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/image/file-codecs.el#L38)

显式创建使用固定 PNG、JPEG 或 AVIF 协议的文件格式对象。

```el-signature
export fn standardImageFileCodec(format: ImageFormat, decoding: ImageDecodeOptions = ImageDecodeOptions())
```

### 示例：用法

```el
let format = standardImageFileCodec(ImageFormat.Png)
```
