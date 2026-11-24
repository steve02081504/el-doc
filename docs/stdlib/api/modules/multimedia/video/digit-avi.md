# multimedia/video/digit-avi.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数位 AVI {#api-ecdc9b01d9ea4848e0cb}

源码：`src/stdlib/multimedia/video/digit-avi.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L1)

按帧保存带时间的数位视频。

## AviVideo {#api-f61f160b1acde4dc8291}

源码：`src/stdlib/multimedia/video/digit-avi.el:56` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L56)

保存解码出的 AVI 模式和帧。关闭视频会关闭它拥有的帧。

```el-signature
export @assign(mode: "shared") class AviVideo
```

### 示例：用法

```el
// @external data: Number[]
scope let video = decodeAvi(data)
let frames = video.frames.count
```

## AviWriter {#api-291a3c29de7c6ff84a3b}

源码：`src/stdlib/multimedia/video/digit-avi.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L118)

增量写入无损 RGBA 数位 AVI。未提供时间戳时由帧索引与帧率推导。

```el-signature
export @assign(mode: "shared") class AviWriter
```

### 示例：用法

```el
// @external image: RgbaImage
import { Path } from "el:operating-system/paths/"
scope let writer = AviWriter(Path("clip.avi"), CameraOptions(image.width, image.height))
writer.append(image)
```

## encodeAvi {#api-8a701b2b4bc5e865c4bd}

源码：`src/stdlib/multimedia/video/digit-avi.el:164` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L164)

编码数位 AVI，保留准确帧率、各帧时间戳和 RGBA 样本。

```el-signature
export fn encodeAvi(mode: CameraOptions, frames: VideoFrame[], radix: Number | nil_t = nil): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：用法

```el
// @external mode: CameraOptions
// @external frames: VideoFrame[]
let data = encodeAvi(mode, frames)
```

## decodeAvi {#api-8d2f0d7d71e67a9d584d}

源码：`src/stdlib/multimedia/video/digit-avi.el:175` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L175)

按所选数位配置解码 AVI；返回值拥有解码出的帧。

```el-signature
export fn decodeAvi(data: Number[], radix: Number | nil_t = nil, limits: ImageLimits = ImageLimits()): AviVideo
```

**返回类型**：[`AviVideo`](digit-avi.md#api-f61f160b1acde4dc8291)

### 示例：用法

```el
// @external data: Number[]
scope let video = decodeAvi(data)
```

## readAvi {#api-bd26b19ff3a04ef9a35d}

源码：`src/stdlib/multimedia/video/digit-avi.el:186` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L186)

按所选的基数配置读取数位 AVI 文件。

```el-signature
export fn readAvi(path: Path, radix: Number | nil_t = nil, limits: ImageLimits = ImageLimits()): AviVideo
```

**返回类型**：[`AviVideo`](digit-avi.md#api-f61f160b1acde4dc8291)

### 示例：用法

```el
import { Path } from "el:operating-system/paths/"
scope let video = readAvi(Path("clip.avi"))
```

## writeAvi {#api-54b24132bea93c7d46ce}

源码：`src/stdlib/multimedia/video/digit-avi.el:201` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/video/digit-avi.el#L201)

将帧按给定模式增量写入数位 AVI 文件。

```el-signature
export fn writeAvi(path: Path, mode: CameraOptions, frames: VideoFrame[], encoding: ImageEncodeOptions = ImageEncodeOptions())
```

### 示例：用法

```el
// @external mode: CameraOptions
// @external frames: VideoFrame[]
import { Path } from "el:operating-system/paths/"
writeAvi(Path("clip.avi"), mode, frames)
```
