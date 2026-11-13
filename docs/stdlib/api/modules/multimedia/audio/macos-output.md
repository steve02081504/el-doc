# multimedia/audio/macos-output.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [PcmOutput.enqueue](#api-f7fc20d16cdc9fcf6a7f)
- [PcmOutput.finish](#api-a9232d52a82db940d1c1)
- [PcmOutput.idle](#api-252297757c2e3d93dbbb)
- [PcmOutput.clear](#api-022cec408375d7d0fe85)
- [PcmOutput.close](#api-098b06b79bc52eca15af)

## PcmOutput {#api-07a36f3fcbe4431833df}

源码：`src/stdlib/multimedia/audio/macos-output.el:54` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L54)

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

## PcmOutput.enqueue {#api-f7fc20d16cdc9fcf6a7f}

源码：`src/stdlib/multimedia/audio/macos-output.el:103` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L103)

```el
fn enqueue(audio: PcmAudio): Bool
```

**返回类型**：`Bool`

尝试提交音频块；样本在返回前复制，队列无空槽时不等待并返回假。

**参数**：audio 帧数与格式符合构造配置的 PCM 音频块。

**返回值**：接受块时为真，队列饱和时为假。

**失败与异常**：格式或长度不匹配、设备关闭或写入失败时抛出 CaptureError。

### 示例：向设备提交音频

```el
if (!output.enqueue(chunk)) sleep(2)
```

## PcmOutput.finish {#api-a9232d52a82db940d1c1}

源码：`src/stdlib/multimedia/audio/macos-output.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L137)

```el
fn finish()
```

标记不再提交新块；设备继续播放已经提交的音频。

### 示例：提交完成后等待设备空闲

```el
output.finish()
while (!output.idle()) sleep(2)
```

## PcmOutput.idle {#api-252297757c2e3d93dbbb}

源码：`src/stdlib/multimedia/audio/macos-output.el:145` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L145)

```el
fn idle(): Bool
```

**返回类型**：`Bool`

检查音频队列中的所有缓冲区是否已完成。

**返回值**：没有待播放缓冲区时为真。

### 示例：等待输出排空

```el
while (!output.idle()) sleep(2)
```

## PcmOutput.clear {#api-022cec408375d7d0fe85}

源码：`src/stdlib/multimedia/audio/macos-output.el:160` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L160)

```el
fn clear()
```

清除设备当前排队的音频块。

### 示例：停止待播音频

```el
output.clear()
```

## PcmOutput.close {#api-098b06b79bc52eca15af}

源码：`src/stdlib/multimedia/audio/macos-output.el:176` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/macos-output.el#L176)

```el
fn close()
```

停止播放并释放设备队列及原生句柄。

### 示例：关闭音频输出

```el
output.close()
```
