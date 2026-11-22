# multimedia/audio/linux-output.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [PcmOutput.enqueue](#api-a4541dd8879f0ac94c1d)
- [PcmOutput.finish](#api-2c4c730664ab8d398430)
- [PcmOutput.idle](#api-9c4aeae8f2aae4510c1b)
- [PcmOutput.clear](#api-a4ef6b8c6e52a3dea8f4)
- [PcmOutput.close](#api-d0948c04bf83f86cfcdb)

## Linux PCM 输出 {#api-1c422a1acecb36c31a5c}

源码：`src/stdlib/multimedia/audio/linux-output.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L1)

通过 OSS 设备提供有界 PCM16 输出队列。

## PcmOutput {#api-9f5da8fa68d02b9e4158}

源码：`src/stdlib/multimedia/audio/linux-output.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L50)

拥有单线程有界 PCM16 设备队列；入队时复制音频块，队列满时立即返回假。

```el-signature
export @assign(mode: "shared") class PcmOutput
```

**参数**：format 固定的 PCM16 音频格式。

**参数**：queueChunks 正整数设备队列容量。

**参数**：maximumFrames 每个块允许的最大帧数，正整数。

**失败与异常**：设备不可用、参数无效或原生初始化失败时抛出 CaptureError。

### 示例：创建播放器并提交一块（需调用方提供对象或绑定）

```el
// @external audio: PcmAudio
let output = PcmOutput(audio.format, 4, 1024)
let accepted = output.enqueue(audio)
```

## PcmOutput.enqueue {#api-a4541dd8879f0ac94c1d}

源码：`src/stdlib/multimedia/audio/linux-output.el:93` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L93)

尝试提交音频块；样本在返回前复制，队列无空槽时不等待并返回假。

```el-signature
fn enqueue(audio: PcmAudio): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**参数**：audio 帧数与格式符合构造配置的 PCM 音频块。

**返回值**：接受块时为真，队列饱和时为假。

**失败与异常**：格式或长度不匹配、设备关闭或写入失败时抛出 CaptureError。

### 示例：向设备提交音频

```el
// @external chunk: PcmAudio
if (!output.enqueue(chunk)) sleep(2)
```

## PcmOutput.finish {#api-2c4c730664ab8d398430}

源码：`src/stdlib/multimedia/audio/linux-output.el:126` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L126)

提交 OSS 输出中尚未提交的尾块；不等待设备完成播放。

```el-signature
fn finish()
```

### 示例：提交尾块后轮询完成状态（需调用方提供对象或绑定）

```el
output.finish()
while (!output.idle()) sleep(2)
```

## PcmOutput.idle {#api-9c4aeae8f2aae4510c1b}

源码：`src/stdlib/multimedia/audio/linux-output.el:138` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L138)

检查设备是否已播放完所有已提交样本。

```el-signature
fn idle(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

**返回值**：设备缓冲区完全空闲时为真。

### 示例：等待输出排空

```el
while (!output.idle()) sleep(2)
```

## PcmOutput.clear {#api-a4ef6b8c6e52a3dea8f4}

源码：`src/stdlib/multimedia/audio/linux-output.el:151` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L151)

清除设备当前排队的音频块。

```el-signature
fn clear()
```

### 示例：停止待播音频（需调用方提供对象或绑定）

```el
output.clear()
```

## PcmOutput.close {#api-d0948c04bf83f86cfcdb}

源码：`src/stdlib/multimedia/audio/linux-output.el:161` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/linux-output.el#L161)

停止播放并释放设备队列及原生句柄。

```el-signature
fn close()
```

### 示例：关闭音频输出

```el
output.close()
```
