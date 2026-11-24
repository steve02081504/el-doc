# multimedia/audio/wav.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## WAV 音频文件 {#api-6c6898f38da97ddd876e}

源码：`src/stdlib/multimedia/audio/wav.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L14)

WAV 默认采用目标数位编码。固定 RIFF/WAVE 入口读入整数 PCM 与 IEEE 浮点音频，并写出 PCM16。

## RiffWavWriter {#api-bea3f561ed00bf54407d}

源码：`src/stdlib/multimedia/audio/wav.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L41)

以增量方式写入经典 RIFF/WAVE PCM16 文件；追加失败后写入器不可继续使用。

```el-signature
export @assign(mode: "shared") class RiffWavWriter
```

**参数**：path 目标文件路径。

**参数**：format 固定的音频格式，后续追加必须保持一致。

### 示例：分块写入 WAV

```el
// @external audio: PcmAudio
import { Path } from "el:operating-system/paths/"
let writer = RiffWavWriter(Path("song.wav"), audio.format)
writer.append(audio)
writer.close()
```

## writeRiffWav {#api-fac4d1614d4af2124793}

源码：`src/stdlib/multimedia/audio/wav.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L88)

将一段 PCM 音频写入 WAV 文件。

```el-signature
export fn writeRiffWav(path: Path, audio: PcmAudio)
```

**参数**：path 目标文件路径。

**参数**：audio 要写入的 PCM16 音频。

### 示例：保存合成音频

```el
// @external audio: PcmAudio
import { Path } from "el:operating-system/paths/"
writeRiffWav(Path("tone.wav"), audio)
```

## encodeRiffWav {#api-f503b0e0b37e373e0ae0}

源码：`src/stdlib/multimedia/audio/wav.el:103` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L103)

将 PCM 音频编码为包含 RIFF/WAVE 头部的字节数组。

```el-signature
export fn encodeRiffWav(audio: PcmAudio): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

**参数**：audio 要编码的 PCM16 音频。

**返回值**：WAV 文件字节数组。

**失败与异常**：音频数据超过经典 RIFF 格式大小时抛出 CaptureError。

### 示例：编码一段音频

```el
// @external audio: PcmAudio
let bytes = encodeRiffWav(audio)
```

## decodeRiffWav {#api-5e56441d53eeafffdf94}

源码：`src/stdlib/multimedia/audio/wav.el:229` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L229)

从内存中的字节数组解析经典整数 PCM 或 IEEE 浮点 WAV，输出 PCM16 样本。

```el-signature
export fn decodeRiffWav(bytes: Number[]): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

**参数**：bytes WAV 文件字节，元素必须是 0 到 255 的整数。

**返回值**：拥有解码样本的新 PcmAudio。

**失败与异常**：输入损坏或格式不支持时抛出 CaptureError。

### 示例：解码 WAV 数据

```el
// @external wavFileBytes: Number[]
let audio = decodeRiffWav(wavFileBytes)
```

## readRiffWav {#api-89a3767ee47dde4b8ba6}

源码：`src/stdlib/multimedia/audio/wav.el:246` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/wav.el#L246)

从文件读取并解析经典整数 PCM 或 IEEE 浮点 WAV，拒绝带额外尾随数据的文件。

```el-signature
export fn readRiffWav(path: Path): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

**参数**：path WAV 文件路径。

**返回值**：拥有解码样本的新 PcmAudio。

**失败与异常**：文件 I/O 或输入格式错误时抛出 CaptureError。

### 示例：读取音频文件

```el
import { Path } from "el:operating-system/paths/"
let audio = readRiffWav(Path("tone.wav"))
```
