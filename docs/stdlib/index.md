# 标准库总览

> 标准库里没有必须背下来的东西，只有必须找得到的东西。这一页负责让你在 30 秒内找到它。

!!! abstract "🎯 这一章能帮你"
    - 按“我要做什么”而不是按模块名找到对应页面
    - 知道每个模块最小的可用入口长什么样
    - 分清哪些能力已经能用、哪些还带“实现状态”标注

    <span class="el-chip">⏱ 约 5 分钟</span> <span class="el-chip">前置：[语言基础](../language/index.md)</span>

## 按任务找

已知道函数或模块名？直接查[标准库 API 参考](api/index.md)，阅读由源码注释生成的签名、参数、异常与具体示例。侧边栏「API 参考」下可直接进入各模块，当前只列出已补文档的接口。

| 我想…… | 去这里 | 最小入口 |
| --- | --- | --- |
| 打印一行字、记一条结构化日志 | [Console 与日志](console.md) | `console.stdout.writeLine(...)` |
| 处理数组、键值表、文本 | [集合与文本](collections.md) | `@[...]`、`.map(...)`、`.join(...)` |
| 读文件、写文件、发 HTTP 请求 | [文件与网络](files-network.md) | 模块导入后调用文件／网络设施 |
| 打开一个系统窗口，用 EL 画界面 | [图形界面](gui.md) | GUI 应用入口与 Canvas 绘制 |
| 播放声音、生成音调 | [声音与音频](audio.md) | `SoundPlayer`、`MusicPlayer` |
| 训练一个小神经网络 | [神经网络](neural-networks.md) | 网络与层的构造 |
| 给代码补测试 | [测试](testing.md) | `el test` 与测试声明 |

## 每个模块一句话

<div class="el-grid" markdown>
<div class="el-card" markdown>
### [Console 与日志](console.md)
三种输出：文字走 `stdout`，日志分等级，结构化值用 `.value` 展示。
<span class="el-card__meta">8 分钟 · 必读</span>
</div>
<div class="el-card" markdown>
### [集合与文本](collections.md)
`Array`、`Map`、`Set`、`BitSet`、惰性 `Sequence` 与 `Text` 的常用操作。
<span class="el-card__meta">12 分钟 · 必读</span>
</div>
<div class="el-card" markdown>
### [文件与网络](files-network.md)
把程序接到外面的世界：路径、读写、网络、失败处理。
<span class="el-card__meta">12 分钟 · 必读</span>
</div>
<div class="el-card" markdown>
### [图形界面](gui.md)
同一份 GUI 代码既能开系统窗口，也能出单文件网页，界面由 EL 自绘。
<span class="el-card__meta">15 分钟 · 看兴趣</span>
</div>
<div class="el-card" markdown>
### [声音与音频](audio.md)
生成音调、播放提示音、读写 WAV。也可以当并发与设备释放的练习。
<span class="el-card__meta">10 分钟 · 看兴趣</span>
</div>
<div class="el-card" markdown>
### [神经网络](neural-networks.md)
用 EL 直接搭网络、训练小模型，不依赖外部框架。
<span class="el-card__meta">15 分钟 · 看兴趣</span>
</div>
<div class="el-card" markdown>
### [测试](testing.md)
`el test`、测试文件布局、断言与失败信息。
<span class="el-card__meta">8 分钟 · 建议读</span>
</div>
</div>

## 读法建议

- **先读三页。** Console、集合与文本、文件与网络覆盖了绝大多数日常代码；其余按项目需要挑。
- **每一页都从最小例子开始。** 标准库页面按“入口 → 参数 → 边界”排列，赶时间只看每节第一段和代码。
- **实现状态要看。** 标了“实现状态”的能力，先在最小片段里确认一次再写进项目，参考[规范与实现边界](../appendix/implementation-status.md)。
- **不要背方法名。** 记住模块负责什么，写代码时用搜索或本页的表格找回来。

!!! tip "标准库和语言的分界线"
    语言部分讲“语法允许你写什么”，标准库讲“发行里实际给你什么”。两者的排序不总一样：有些语法特性要靠标准库宏实现（比如 `async`/`await`），所以读[错误处理与异步](../language/errors-async.md)时，别忘了它其实是在用标准库。

## 下一站

- [Console 与日志](console.md)：从最小的输出系统开始，也是调试其他一切的基础。
- 想先做东西：[命令行工具](../practice/cli-tool.md)：把文件与网络、参数、退出码串成一个工具。
