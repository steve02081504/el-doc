# multimedia/audio/digit-wav.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/multimedia.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 数位 WAV {#api-b69712a18a3c3390ff91}

源码：`src/stdlib/multimedia/audio/digit-wav.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L1)

按数位配置保存 PCM 采样与时间。

## WavWriter {#api-9a5a13565e8fd848cb66}

源码：`src/stdlib/multimedia/audio/digit-wav.el:99` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L99)

增量写入数位 WAV。每次追加一块样本，关闭时写入终止符和校验。

```el-signature
export @assign(mode: "shared") class WavWriter
```

### 示例：用法

```el
// @external audio: PcmAudio
import { Path } from "el:operating-system/paths/"
scope let writer = WavWriter(Path("song.wav"), audio.format)
writer.append(audio)
```

## encodeWav {#api-e2ba5e3e339d142eb72a}

源码：`src/stdlib/multimedia/audio/digit-wav.el:142` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L142)

把 PCM16 样本及时间戳精确编码为数位 WAV。基数缺省为目标数位基数。

```el-signature
export fn encodeWav(audio: PcmAudio, radix: Number | nil_t = nil): Number[]
```

**返回类型**：[`Number`](../../number/number.md#api-3cc24d3ef702e8652fb4)[]

### 示例：用法

```el
// @external audio: PcmAudio
let data = encodeWav(audio)
```

## decodeWav {#api-02e9ff4d5ff9c586e3af}

源码：`src/stdlib/multimedia/audio/digit-wav.el:153` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L153)

读入数位 WAV，将各块样本依次拼接并保留首块时间戳。

```el-signature
export fn decodeWav(data: Number[], radix: Number | nil_t = nil): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

### 示例：用法

```el
// @external data: Number[]
scope let audio = decodeWav(data)
```

## readWav {#api-371aa876b2e8cf64bf5d}

源码：`src/stdlib/multimedia/audio/digit-wav.el:164` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L164)

按所选的基数配置读取数位 WAV 文件。

```el-signature
export fn readWav(path: Path, radix: Number | nil_t = nil): PcmAudio
```

**返回类型**：[`PcmAudio`](../capture/model.md#api-cb1ec5de04201d03778d)

### 示例：用法

```el
import { Path } from "el:operating-system/paths/"
scope let audio = readWav(Path("song.wav"))
```

## writeWav {#api-f23313baccba366e8607}

源码：`src/stdlib/multimedia/audio/digit-wav.el:174` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/multimedia/audio/digit-wav.el#L174)

按所选的基数配置写出数位 WAV 文件。

```el-signature
export fn writeWav(path: Path, audio: PcmAudio, radix: Number | nil_t = nil)
```

### 示例：用法

```el
// @external audio: PcmAudio
import { Path } from "el:operating-system/paths/"
writeWav(Path("song.wav"), audio)
```
