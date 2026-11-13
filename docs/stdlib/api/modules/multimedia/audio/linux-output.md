# multimedia/audio/linux-output.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [PcmOutput.enqueue](#api-a4541dd8879f0ac94c1d)
- [PcmOutput.finish](#api-2c4c730664ab8d398430)
- [PcmOutput.idle](#api-9c4aeae8f2aae4510c1b)
- [PcmOutput.clear](#api-a4ef6b8c6e52a3dea8f4)
- [PcmOutput.close](#api-d0948c04bf83f86cfcdb)

## PcmOutput {#api-9f5da8fa68d02b9e4158}

源码：`src/stdlib/multimedia/audio/linux-output.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L47)

```el
export @assign(mode: "shared") class PcmOutput
```

拥有单线程有界 PCM16 设备队列；入队时复制音频块，队列满时立即返回假。

**参数**：format 固定的 PCM16 音频格式。

**参数**：queueChunks 设备队列容量，范围 1 到 16。

**参数**：maximumFrames 每个块允许的最大帧数，范围 1 到 1048576。

**失败与异常**：设备不可用、参数无效或原生初始化失败时抛出 CaptureError。

### 示例：创建播放器并提交一块

```el
let output = PcmOutput(audio.format, 4, 1024)
let accepted = output.enqueue(audio)
```

## PcmOutput.enqueue {#api-a4541dd8879f0ac94c1d}

源码：`src/stdlib/multimedia/audio/linux-output.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L87)

```el
fn enqueue(audio: PcmAudio): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

尝试提交音频块；样本在返回前复制，队列无空槽时不等待并返回假。

**参数**：audio 帧数与格式符合构造配置的 PCM 音频块。

**返回值**：接受块时为真，队列饱和时为假。

**失败与异常**：格式或长度不匹配、设备关闭或写入失败时抛出 CaptureError。

### 示例：向设备提交音频

```el
if (!output.enqueue(chunk)) sleep(2)
```

## PcmOutput.finish {#api-2c4c730664ab8d398430}

源码：`src/stdlib/multimedia/audio/linux-output.el:120` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L120)

```el
fn finish()
```

提交 OSS 输出中尚未提交的尾块；不等待设备完成播放。

### 示例：提交尾块后轮询完成状态

```el
output.finish()
while (!output.idle()) sleep(2)
```

## PcmOutput.idle {#api-9c4aeae8f2aae4510c1b}

源码：`src/stdlib/multimedia/audio/linux-output.el:132` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L132)

```el
fn idle(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

检查设备是否已播放完所有已提交样本。

**返回值**：设备缓冲区完全空闲时为真。

### 示例：等待输出排空

```el
while (!output.idle()) sleep(2)
```

## PcmOutput.clear {#api-a4ef6b8c6e52a3dea8f4}

源码：`src/stdlib/multimedia/audio/linux-output.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L145)

```el
fn clear()
```

清除设备当前排队的音频块。

### 示例：停止待播音频

```el
output.clear()
```

## PcmOutput.close {#api-d0948c04bf83f86cfcdb}

源码：`src/stdlib/multimedia/audio/linux-output.el:155` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L155)

```el
fn close()
```

停止播放并释放设备队列及原生句柄。

### 示例：关闭音频输出

```el
output.close()
```
