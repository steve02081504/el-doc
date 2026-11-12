# multimedia/audio/windows-output.el

本页由源码注释生成；示例未运行验证。

## PcmOutput {#api-3405bba76a30486bbb83}

源码：`src/stdlib/multimedia/audio/windows-output.el:54` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L54)

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

## PcmOutput.enqueue {#api-5372746934d5b8e5c997}

源码：`src/stdlib/multimedia/audio/windows-output.el:97` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L97)

```el
fn enqueue(audio: PcmAudio): Bool
```

尝试提交音频块；样本在返回前复制，队列无空槽时不等待并返回假。

**参数**：audio 帧数与格式符合构造配置的 PCM 音频块。

**返回值**：接受块时为真，队列饱和时为假。

**失败与异常**：格式或长度不匹配、设备关闭或写入失败时抛出 CaptureError。

### 示例：向设备提交音频

```el
if (!output.enqueue(chunk)) sleep(2)
```

## PcmOutput.finish {#api-df13597f5e16ed137856}

源码：`src/stdlib/multimedia/audio/windows-output.el:118` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L118)

```el
fn finish()
```

兼容其他平台的结束调用；Windows waveOut 队列无需额外提交尾块。

### 示例：完成提交后等待播放

```el
output.finish()
while (!output.idle()) sleep(2)
```

## PcmOutput.idle {#api-70c6bd7ef71832546cf8}

源码：`src/stdlib/multimedia/audio/windows-output.el:126` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L126)

```el
fn idle(): Bool
```

检查设备队列是否已完成所有已提交块。

**返回值**：没有待播放块时为真。

### 示例：等待队列排空

```el
while (!output.idle()) sleep(2)
```

## PcmOutput.clear {#api-573c3b322bc864f723be}

源码：`src/stdlib/multimedia/audio/windows-output.el:137` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L137)

```el
fn clear()
```

清除设备当前排队的音频块。

### 示例：停止待播音频

```el
output.clear()
```

## PcmOutput.close {#api-5ea91df086c9987b32dd}

源码：`src/stdlib/multimedia/audio/windows-output.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/windows-output.el#L148)

```el
fn close()
```

停止播放并释放设备队列及原生句柄。

### 示例：关闭音频输出

```el
output.close()
```
