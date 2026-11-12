# user-interface/sound.el

本页由源码注释生成；示例未运行验证。

## 界面提示音 {#api-3f30a95ee9b027857187}

源码：`src/stdlib/user-interface/sound.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L5)

将短促音效、循环引擎音和停止操作绑定到窗口生命周期。

## SoundPlayer {#api-7444e7a247962761e044}

源码：`src/stdlib/user-interface/sound.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L17)

```el
export @assign(mode: "shared") class SoundPlayer
```

播放界面提示音并可管理循环音效；通常由窗口作用域持有并在窗口关闭时释放。

### 示例：播放一个提示音并关闭播放器

```el
let sound = SoundPlayer(window)
discard(sound.cue("increase"))
sound.close()
```

## SoundPlayer.cue {#api-a832a21f3fe936cbb93d}

源码：`src/stdlib/user-interface/sound.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L35)

```el
fn cue(name: Text, value: Number = 0, maximum: Number = 1): Bool
```

尝试将命名提示音加入短音效队列，不等待播放完成。

**参数**：name 支持 drag、exchange、increase、decrease、disappear、engine、celebrate。

**参数**：value exchange 音效的当前数值。

**参数**：maximum exchange 音效的最大数值，须为正数。

**返回值**：队列接受音效时为真，队列繁忙时为假。

**失败与异常**：音效名称或 exchange 数值无效，以及设备错误时抛出。

### 示例：播放增加提示音

```el
let accepted = sound.cue("increase")
```

## SoundPlayer.engine {#api-e28773542d6de5c25c75}

源码：`src/stdlib/user-interface/sound.el:62` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L62)

```el
fn engine(speed: Number)
```

设置循环引擎声的速度，并在需要时启动循环音效。

**参数**：speed 有限速度值，范围 0 到 1。

**失败与异常**：速度超出范围或设备操作失败时抛出错误。

### 示例：设置引擎转速

```el
sound.engine(0.6)
```

## SoundPlayer.tryCue {#api-bdf8aa6e71523e364ba2}

源码：`src/stdlib/user-interface/sound.el:73` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L73)

```el
fn tryCue(name: Text, value: Number = 0, maximum: Number = 1): Bool
```

尝试播放提示音，并将捕获设备错误转换为未接受状态。

### 示例：容错地请求提示音

```el
let accepted = sound.tryCue("celebrate")
```

## SoundPlayer.loop {#api-12729f274be6bb28fd2c}

源码：`src/stdlib/user-interface/sound.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L85)

```el
fn loop(name: Text = "engine")
```

启动指定的循环音效；当前支持 engine，并通过窗口定时器重复播放。

**参数**：name 循环音效名称，当前仅支持 engine。

### 示例：启动并停止循环声

```el
sound.loop("engine")
sound.stop()
```

## SoundPlayer.stop {#api-38b098ba7017124aed8a}

源码：`src/stdlib/user-interface/sound.el:97` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L97)

```el
fn stop()
```

取消循环定时器并清除播放器中排队的声音。

### 示例：停止提示音

```el
sound.stop()
```

## SoundPlayer.close {#api-27a2cdf8d9f4095bd7b5}

源码：`src/stdlib/user-interface/sound.el:108` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/sound.el#L108)

```el
fn close()
```

停止循环播放并释放底层音频设备。

### 示例：关闭界面提示音播放器

```el
sound.close()
```
