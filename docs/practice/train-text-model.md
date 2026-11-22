# 从一小段语料训练文字模型

> 训练完成后先别看生成得像不像人话。用同一个提示词和随机种子，检查保存前后能不能生成同样的文本。

!!! abstract "🎯 做完这个项目，你能"
    - 在内嵌语料上训练分词器和文字模型，再改用文本数据集
    - 把权重、配置和分词器一起保存，再加载做一次生成对照
    - 区分用于生成的模型包和用于续训的检查点

    <span class="el-chip">⏱ 约 25 分钟</span> <span class="el-chip">前置：[神经网络](../stdlib/neural-networks.md)</span>

!!! note "实现状态"
    示例采用 EL 仓库 `examples/nn/language-model.el` 的主机训练路径，尚未编译或运行。它使用小到能读完的语料和只有一层的模型。

## 用同一模型包核对保存与加载

在空目录把程序存为 `train.el`，运行 `el run train.el`。训练输出每个有效批次的损失，接着输出一段生成文本。两次生成相同则最后一行是 `模型往返一致`。目录中应出现 `tiny.elm`，可以用下面的加载调用重建模型。

```el
import { DitFloat } from "el:number/dit-float.el"
import { Tensor } from "el:numerical-computing/tensor.el"
import { AdamW } from "el:neural-networks/index.el"
import { DecoderConfig, CausalLanguageModel, LanguageModelPackage, trainBytePairTokenizer, LanguageModelWindows, GenerationOptions, generateText } from "el:neural-networks/text/index.el"

let F32 = DitFloat<sign_dits: 1, fraction_dits: 23, exponent_dits: 8, exponent_bias: 127>
let Host = Tensor<element: F32>
let Model = CausalLanguageModel<element: F32>
let Package = LanguageModelPackage<element: F32>
let upload = fn(value: Host): Host { return value }
let corpus = "春天种豆。雨后看苗。春天种豆，秋天收豆。"
let tokenizer = trainBytePairTokenizer(@[corpus], 288)
let config = DecoderConfig(tokenizer.vocabularySize, width: 8, layers: 1, heads: 2, hidden: 16, context: 24, keyValueHeads: 1)
let model = Model(config, upload, 17)
let windows = LanguageModelWindows(tokenizer.encode(corpus, t, t), config.context, config.vocabulary, tokenizer.padId)
let optimizer = AdamW<element: F32>(rate: .001, epsilon: .000001)
for (let epoch = 0; epoch < 2; epoch++) {
	for (let first = 0; first < windows.count; first += 2) {
		let batch = windows.batch(first, 2)
		if (batch.validTokens == 0) continue
		let step = model.valueAndGrad(batch.inputIds, batch.targetIds, batch.shape[0], batch.shape[1], batch.lossMask)
		optimizer.update(model.weights, step.grad)
		console.stdout.writeLine(step.value.scalar())
	}
}

let readChunk = fn(borrow value: Host, offset: Number, count: Number): Host {
	let values: F32[] = @[]
	for (let index = 0; index < count; index++) values.push(value.flat(offset + index))
	return Host(@[count], values)
}
let package = Package()
package.save(config, tokenizer, model.weights, @[], readChunk, "tiny.elm", "tiny.elm.tmp")
let loaded = package.load("tiny.elm", upload)
let restored = Model(loaded.config, loaded.weights, upload, loaded.adapters)
let options = GenerationOptions(maxNewTokens: 8, contextLimit: config.context, temperature: .8, topK: 20, topP: .9, randomState: 19)
let before = generateText(model, tokenizer, "春天", upload, options)
let after = generateText(restored, loaded.tokenizer, "春天", upload, options)
if (before.text != after.text) throw "Model output changed after reload"
console.stdout.writeLine(after.text)
console.stdout.writeLine("模型往返一致")
```

分词器把文字变成编号。窗口把一串编号切成训练段，并把输入向右错开一格生成预测目标。补齐位置不会计入损失。保存时按块把主机张量交给模型包，加载后再用保存的配置和权重构造解码器。

??? question "先猜：重新加载后马上继续训练，会和从未关掉程序一样吗？"
    需要额外恢复优化器统计、分片位置和随机状态。这里的模型包负责恢复生成所需的数据。要验证续训，记录下一批输入，并比较恢复前后各走一步所得的参数。

## 换成训练集与验证集

准备两个 UTF-8 文本文件 `train.txt` 和 `validation.txt`，每份可以包含多篇文本。按原始文档拆分训练集与验证集，把同一篇文章的重复版本留在同一份。先用短语料核对训练、生成和文件保存，再把程序中的语料改为：

```el
import { readTextFile } from "el:filesystem/"
```

把导入放在文件顶部，把 `let corpus = …` 替换为 `let corpus = readTextFile("train.txt")`。分词器只在训练集上拟合。验证时复用同一个分词器，把验证文本编码为新窗口，只读损失且不更新权重；用有效 token 数加权汇总各批损失。文本较多时，按源文档分片，明确段落之间的分隔符，记录数据版本、分片顺序、随机种子、上下文长度和模型配置。整文件读取示例适合小规模试跑，大数据训练需要分片数据读取和明确的检查点。

!!! example "检查数据确实参与了训练"
    保留固定的验证集，用两份不同的训练文本各跑一次。核对训练窗口数和模型包能成功生成，再记录各自的验证集损失。把验证样本混进训练文本会破坏这个比较。

## 下一站：[在随机三维场景中训练小人走路](train-walker.md)

把文本窗口换成环境步进，分别核对模型、环境和随机种子的恢复。
