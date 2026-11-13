# multimedia/audio/music.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 音频合成与播放 {#api-e33a9bf98fb80b944c00}

源码：`src/stdlib/multimedia/audio/music.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L7)

将单声道公式采样转换为 PCM16 音频，通过有界设备队列异步播放短提示音或较长片段。

## MusicPlayer {#api-dd93e8dfc04fdbadfcb9}

源码：`src/stdlib/multimedia/audio/music.el:47` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L47)

```el
export @assign(mode: "shared") class MusicPlayer
```

管理短提示音使用的非等待播放队列；队列饱和时拒绝新提示音。

### 示例：播放提示音并显式释放

```el
let player = MusicPlayer()
let accepted = player.play(440)
player.close()
```

## MusicPlayer.formula {#api-baf68ca88eb889649eb3}

源码：`src/stdlib/multimedia/audio/music.el:60` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L60)

```el
fn formula(sample, milliseconds: Number = 80, gain: Number = 0.12): Bool
```

将一段公式音频作为短提示音提交到非等待队列。

**参数**：sample 接收秒数并返回 -1 到 1 之间有限数值的回调。

**参数**：milliseconds 正时长，最多一秒。

**参数**：gain 振幅比例，范围 0 到 1。

**返回值**：队列接受时为真，队列繁忙时为假。

### 示例：合成短提示音

```el
let accepted = player.formula(seconds => sin(seconds * 880 * 6.283185307179586), 120)
```

## MusicPlayer.play {#api-acd751dc2f58267cd866}

源码：`src/stdlib/multimedia/audio/music.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L79)

```el
fn play(frequency: Number, milliseconds: Number = 80, gain: Number = 0.12): Bool
```

将三角波音调作为短提示音提交到非等待队列。

**参数**：frequency 有效范围为大于 0 且小于 12000 Hz。

**参数**：milliseconds 正时长，最多一秒。

**参数**：gain 振幅比例，范围 0 到 1。

**返回值**：队列接受时为真，队列繁忙时为假。

### 示例：播放提示音

```el
let accepted = player.play(660, 70)
```

## MusicPlayer.stop {#api-878b318a6d2c1a57a85e}

源码：`src/stdlib/multimedia/audio/music.el:89` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L89)

```el
fn stop()
```

清除当前排队的提示音，但保留播放器供后续复用。

### 示例：停止排队中的声音

```el
player.stop()
```

## MusicPlayer.close {#api-74a7a57af495951c63ea}

源码：`src/stdlib/multimedia/audio/music.el:96` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L96)

```el
fn close()
```

关闭底层设备并释放资源；重复调用安全。

### 示例：释放提示音播放器

```el
player.close()
```

## playPitch {#api-14ec176406410644f42a}

源码：`src/stdlib/multimedia/audio/music.el:117` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L117)

```el
export fn playPitch(frequency: Number, milliseconds: Number = 80, gain: Number = 0.12)
```

在独立任务中播放三角波音调，持续时间以毫秒计，频率以 Hz 计。

**参数**：frequency 有效范围为大于 0 且小于 12000 Hz。

**参数**：milliseconds 正时长，最长 1000 毫秒。

**参数**：gain 有限振幅比例，范围为 0 到 1。

**返回值**：播放任务句柄。

**失败与异常**：参数无效或设备不可用时抛出错误。

### 示例：播放 440 Hz 音调

```el
let task = playPitch(440, 250, 0.1)
```

## playFormula {#api-dd17e7a0384ee0e866a0}

源码：`src/stdlib/multimedia/audio/music.el:132` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/music.el#L132)

```el
export fn playFormula(sample, milliseconds: Number = 80, gain: Number = 0.12)
```

在独立任务中按公式逐样本合成音频，并以有界块队列提交给设备。

**参数**：sample 接收秒数、返回范围 -1 到 1 的有限样本值的回调。

**参数**：milliseconds 正时长；公式播放可超过一秒。

**参数**：gain 有限振幅比例，范围为 0 到 1。

**返回值**：播放任务句柄。

**失败与异常**：公式返回非有限或超范围样本，以及设备或参数错误时抛出。

### 示例：合成正弦音

```el
let task = playFormula(seconds => sin(seconds * 440 * 2 * pi), 500)
```
