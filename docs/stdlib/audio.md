# 声音与音频

这一页讲怎么用标准库直接发出声音：按频率播放一个音、用公式合成自己的波形、读写 WAV 文件，以及三个桌面平台各自的后端与限制。读完你能写出几行的提示音、一段自定义音色，并把它们保存成 `.wav`。

## 两个播放入口

声音入口都在 `el:multimedia/audio/` 里：

```el
import { playPitch, playFormula } from "el:multimedia/audio/"
```

| 入口 | 参数 | 返回 |
| --- | --- | --- |
| `playPitch(frequency, milliseconds = 80, gain = 0.12)` | 频率 Hz、时长 ms、增益 | 播放任务 |
| `playFormula(sample, milliseconds = 80, gain = 0.12)` | 公式函数、时长 ms、增益 | 播放任务 |

参数有几条硬约束，违反时调用直接报错：频率要满足 `0 < frequency < 12000`；时长必须为正，内部按 24000 Hz 单声道合成，帧数是 `floor(milliseconds * 24)`，短于一帧就报错；增益必须在 `0..1` 之间；公式接收以秒为单位的整曲时间（`Number<epsilon: 0.000000001>`），必须返回有限且落在 `-1..1` 的样本。`playPitch` 内部用三角波，源码里叫 `triangle`，不是正弦波；要别的音色就写公式。两个入口都会在整曲首尾各 120 帧（24000 Hz 下约 5 毫秒）淡入淡出，避免爆音。

### 正弦音

```el
import { playFormula } from "el:multimedia/audio/"
import { sin } from "el:mathematics/"

// 440 Hz 正弦，持续 1 秒：sin(2πft)
let note = playFormula((seconds) => sin(seconds * 440 * 6.283185307179586), 1000)
discard(note.get())
```

`discard(note.get())` 等播放真正结束。不等待时程序可能先退出，声音只播出一部分。

## 任务、取消与设备释放

`playPitch` 与 `playFormula` 返回的是 `spawn` 启动的普通任务，不是设备句柄。

- 任务逐块合成（每块最多 2048 帧），通过一个有界原生队列提交；队列满时任务异步等待，已经合成的块不会重新求值公式。
- 公式的时间与相位跨块连续，每个样本恰好调用一次公式。
- 正常完成要等设备队列真的播完才释放资源，所以 `get()` 返回的时刻就是声音结束的时刻。
- `cancel()` 取消播放任务；取消和错误都会释放这次播放自己持有的设备。
- GUI 事件回调里不要 `get()`，那会卡住界面；保留任务，在窗口关闭时 `cancel()`。

```el
let long = playFormula((seconds) => sin(seconds * 440 * 6.283185307179586), 30000)
// ... 播放期间做别的事
discard(long.cancel())
```

## 短提示音：MusicPlayer 与 SoundPlayer

`MusicPlayer` 面向短提示音，构造不需要参数，输出设备在第一次播放时才打开。

| 成员 | 说明 |
| --- | --- |
| `play(frequency, milliseconds = 80, gain = 0.12)` | 三角波提示音，返回 `Bool` |
| `formula(sample, milliseconds = 80, gain = 0.12)` | 自定义公式提示音，返回 `Bool` |
| `stop()` | 清空这个播放器的队列 |
| `close()` | 清空并释放设备，析构时也会调用 |

提交不等待：返回 `Bool` 表示这次提交是否被接受，队列忙时返回 `nil`，调用方决定丢弃还是稍后重试。提示音最长 1 秒（24000 帧），更长的声音用包级的 `playFormula`。

GUI 程序用 `el:user-interface/` 导出的 `SoundPlayer`，它由窗口拥有，内部就是一个 `MusicPlayer`。`SoundPlayer(window)` 的 `cue(name, value = 0, maximum = 1)` 按名字发提示音，名字有 `"drag"`、`"exchange"`、`"increase"`、`"decrease"`、`"disappear"`、`"engine"`、`"celebrate"`；`tryCue(...)` 在底层报 `CaptureError` 时返回 `nil`；`loop("engine")` 循环发引擎音，`engine(speed)` 设置 0..1 的速度，`stop()` 停止，`close()` 释放。

## WAV 读写

`wav.el` 导出经典 RIFF/WAVE 整数 PCM16 的读写：

| 入口 | 说明 |
| --- | --- |
| `readWav(path, maxFrames = 16777216)` | 读成 `PcmAudio` |
| `writeWav(path, audio)` | 把整个 `PcmAudio` 写成 WAV |
| `encodeWav(audio): Number[]` | 编码成字节数组，上限 64 MiB |
| `decodeWav(bytes, maxFrames = 16777216)` | 从字节数组解码 |
| `WavWriter(path, format = AudioFormat())` | 增量写入：`append(audio)`、`frames`、`close()` |

`AudioFormat(sampleRate = 48000, channels = 1)` 的采样率限制在 1000..384000 Hz、声道数 1..2，`blockAlign` 是声道数乘 2 字节。`PcmAudio(frames, format = AudioFormat(), timestamp = 0)` 是交错的 PCM16 缓冲，`sample(frame, channel)` 读、`setSample(frame, channel, value)` 写，值域 `-32768..32767`。

```el
import { AudioFormat, PcmAudio, writeWav } from "el:multimedia/audio/"
import { floor, sin } from "el:mathematics/"

fn writeTone(path: Text) {
	let format = AudioFormat(24000, 1)
	let frames = 12000
	let audio = PcmAudio(frames, format)
	try {
		for (let frame = 0; frame < frames; frame++) {
			let seconds = Number(frame) / 24000
			audio.setSample(frame, 0, floor(sin(seconds * 440 * 6.283185307179586) * 24000))
		}
		writeWav(path, audio)
	} finally {
		audio.close()
	}
}

writeTone("file:./tone.wav")
```

`readWav`/`writeWav` 失败时抛 `CaptureError`（来自 `el:multimedia/capture/`），`failure` 字段给出 `InvalidInput`、`UnsupportedFormat`、`LimitExceeded` 等分类。只支持整数 PCM16；其它编码、重复块、截断和超出 `maxFrames` 都会明确报错。

### 从 WAV 播放

没有“播放一个 wav 文件”的一行入口：要播放 `readWav` 得到的数据，得自己按块提交给 `PcmOutput`。`PcmOutput(format, queueChunks = 4, maximumFrames = 4096)` 是平台后端的公共包装，`enqueue(audio)` 在返回前复制样本，队列满时返回 `nil`。

```el
import { PcmAudio, PcmOutput, readWav } from "el:multimedia/audio/"
import { sleep } from "el:concurrency/"

fn playWav(path: Text) {
	let source = readWav(path)
	try {
		let output = PcmOutput(source.format, 4, 1024)
		try {
			let offset = 0
			while (offset < source.frames) {
				let count = source.frames - offset
				if (count > 1024) count = 1024
				let chunk = PcmAudio(count, source.format)
				try {
					for (let frame = 0; frame < count; frame++) {
						for (let channel = 0; channel < source.format.channels; channel++) {
							chunk.setSample(frame, channel, source.sample(offset + frame, channel))
						}
					}
					while (!output.enqueue(chunk)) sleep(2)
				} finally {
					chunk.close()
				}
				offset += count
			}
			output.finish()
			while (!output.idle()) sleep(2)
		} finally {
			output.close()
		}
	} finally {
		source.close()
	}
}

playWav("file:./tone.wav")
```

`finish()` 在 Linux OSS 上发 `SNDCTL_DSP_POST` 提交最后一段不完整的片段，在 Windows 与 macOS 上是空操作；`idle()` 在设备队列真正排空后返回真，Windows 与 macOS 分别用 `WHDR_DONE` 和 AudioQueue 的完成回调判断。

## 平台后端与限制

后端在 `output.el` 里按目标平台选择，都给调用方一个有界队列，都只做 PCM16，不向用户代码暴露设备回调。`PcmOutput` 的队列块数限制在 1..16，每块帧数上限 1048576。

| 平台 | 后端 | 关键限制 |
| --- | --- | --- |
| Windows | `winmm.dll` 的 waveOut | 需要 64 位、8 位地址单元 ABI；完成状态看每个缓冲区的 `WHDR_DONE` |
| macOS | AudioToolbox 的 AudioQueue | 需要 64 位 Darwin ABI；完成状态来自每个缓冲区的回调标记 |
| Linux | OSS `/dev/dsp` | 只支持 GNU/Musl 环境；直接开设备，不经 ALSA/PulseAudio，也没有外部播放器回退；设备必须精确接受 PCM16 格式，队列容量超过请求上限就拒绝 |
| 其它目标 | 不可用后端 | 构造 `PcmOutput` 时抛 `CaptureError(CaptureFailure.Unavailable)` |

`playPitch`/`playFormula` 自己管理设备，所以在没有后端的平台上同样失败，错误会出现在播放任务的 `get()` 里。

!!! note "实现状态"
    当前没有把 WAV 直接交给播放器的一行接口：要播放就先 `readWav`，再按块提交给 `PcmOutput`。

## 继续阅读

- [Console 与日志](console.md)：把播放状态和错误按等级写出去。
- [图形界面](gui.md)：`SoundPlayer` 由窗口拥有，和控件、定时器一起使用。
- [集合与文本](collections.md)：处理样本数组与音频元数据。
