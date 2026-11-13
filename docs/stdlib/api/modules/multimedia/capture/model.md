# multimedia/capture/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [PcmAudio.sample](#api-8a550e9ca9ac7d948cde)
- [PcmAudio.setSample](#api-5d599038539e68d30f37)

## 音视频捕获模型 {#api-318c16b07ac1855df25d}

源码：`src/stdlib/multimedia/capture/model.el:10` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/model.el#L10)

定义采集设备、音频格式以及供音频输入输出共用的 PCM 缓冲区。

## AudioFormat {#api-36f185417f0702feae38}

源码：`src/stdlib/multimedia/capture/model.el:72` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/model.el#L72)

```el
export @assign(mode: "copy") class AudioFormat
```

声明整数 PCM16 音频的采样率和声道数，并提供每帧字节数。

**参数**：sampleRate 每秒采样帧数，范围 1000 到 384000。

**参数**：channels 声道数，支持 1 或 2。

**失败与异常**：参数超出支持范围时抛出 CaptureError。

### 示例：创建 48 kHz 立体声格式

```el
let format = AudioFormat(48000, 2)
```

## PcmAudio {#api-cb1ec5de04201d03778d}

源码：`src/stdlib/multimedia/capture/model.el:121` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/model.el#L121)

```el
export @assign(mode: "shared") class PcmAudio
```

拥有交错有符号 PCM16 小端样本的共享缓冲区，可按帧和声道读取或写入。

**参数**：frames 音频帧数，范围 0 到 16777216。

**参数**：format PCM 音频格式。

**参数**：timestamp 非负有限时间戳。

**失败与异常**：帧数、时间戳或缓冲区状态无效时抛出 CaptureError。

### 示例：写入一个单声道样本

```el
let audio = PcmAudio(1, AudioFormat(24000, 1))
audio.setSample(0, 0, 12000)
```

## PcmAudio.sample {#api-8a550e9ca9ac7d948cde}

源码：`src/stdlib/multimedia/capture/model.el:154` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/model.el#L154)

```el
fn sample(frame: Number, channel: Number = 0): Number
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)

读取指定帧和声道的有符号 PCM16 整数样本。

**参数**：frame 零起始帧索引。

**参数**：channel 零起始声道索引，默认读取第一个声道。

**返回值**：范围 -32768 到 32767 的整数样本。

### 示例：读取第一个样本

```el
let value = audio.sample(0)
```

## PcmAudio.setSample {#api-5d599038539e68d30f37}

源码：`src/stdlib/multimedia/capture/model.el:173` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/capture/model.el#L173)

```el
fn setSample(frame: Number, channel: Number, value: Number)
```

设置指定帧和声道的有符号 PCM16 整数样本。

**参数**：frame 零起始帧索引。

**参数**：channel 零起始声道索引。

**参数**：value 范围 -32768 到 32767 的整数样本。

**失败与异常**：帧、声道或样本值越界，以及缓冲区已关闭时抛出错误。

### 示例：将第一个样本设为静音

```el
audio.setSample(0, 0, 0)
```
