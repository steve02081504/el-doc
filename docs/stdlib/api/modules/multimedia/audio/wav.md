# multimedia/audio/wav.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## WAV 音频文件 {#api-6c6898f38da97ddd876e}

源码：`src/stdlib/multimedia/audio/wav.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L10)

读写经典 RIFF/WAVE 中的整数 PCM16；流式写入适合较大的音频，解码会执行大小与格式限制检查。

## WavWriter {#api-fccc5e339fd9a3fa8554}

源码：`src/stdlib/multimedia/audio/wav.el:36` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L36)

以增量方式写入经典 RIFF/WAVE PCM16 文件；追加失败后写入器不可继续使用。

```el
export @assign(mode: "shared") class WavWriter
```

**参数**：path 目标文件路径。

**参数**：format 固定的音频格式，后续追加必须保持一致。

### 示例：分块写入 WAV

```el
import { Path } from "el:operating-system/paths/"
let writer = WavWriter(Path("song.wav"), audio.format)
writer.append(audio)
writer.close()
```

## writeWav {#api-8708e42303b382c64743}

源码：`src/stdlib/multimedia/audio/wav.el:82` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L82)

将一段 PCM 音频写入 WAV 文件。

```el
export fn writeWav(path: Path, audio: PcmAudio)
```

**参数**：path 目标文件路径。

**参数**：audio 要写入的 PCM16 音频。

### 示例：保存合成音频

```el
import { Path } from "el:operating-system/paths/"
writeWav(Path("tone.wav"), audio)
```

## encodeWav {#api-90612d8b808b86560049}

源码：`src/stdlib/multimedia/audio/wav.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L96)

将 PCM 音频编码为包含 RIFF/WAVE 头部的字节数组。

```el
export fn encodeWav(audio: PcmAudio): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：audio 要编码的 PCM16 音频。

**返回值**：WAV 文件字节数组。

**失败与异常**：音频数据超过经典 RIFF 格式大小时抛出 CaptureError。

### 示例：编码一段音频

```el
let bytes = encodeWav(audio)
```

## decodeWav {#api-3ec25c2a0a628a314475}

源码：`src/stdlib/multimedia/audio/wav.el:144` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L144)

从内存中的字节数组解析经典 PCM16 WAV。

```el
export fn decodeWav(bytes: Number[]): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

**参数**：bytes WAV 文件字节，元素必须是 0 到 255 的整数。

**返回值**：拥有解码样本的新 PcmAudio。

**失败与异常**：输入损坏或格式不支持时抛出 CaptureError。

### 示例：解码 WAV 数据

```el
let audio = decodeWav(bytes)
```

## readWav {#api-f9e2d41c929d9370ea5e}

源码：`src/stdlib/multimedia/audio/wav.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L161)

从文件读取并解析经典 PCM16 WAV，拒绝带额外尾随数据的文件。

```el
export fn readWav(path: Path): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

**参数**：path WAV 文件路径。

**返回值**：拥有解码样本的新 PcmAudio。

**失败与异常**：文件 I/O 或输入格式错误时抛出 CaptureError。

### 示例：读取音频文件

```el
import { Path } from "el:operating-system/paths/"
let audio = readWav(Path("tone.wav"))
```
