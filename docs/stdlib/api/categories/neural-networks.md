# neural-networks

[标准库分类](../index.md) · [模块索引](../modules.md) · [符号索引](../symbols.md)

本页按源码模块组织已标注接口；未标注部分不在此列表中。

| 模块 | 接口 |
| --- | --- |
| [neural-networks/adamw.el](../modules/neural-networks/adamw.md) | [AdamW](../modules/neural-networks/adamw.md#api-72ebca138f336dfe1a20)、[AdamW.update](../modules/neural-networks/adamw.md#api-221135265f4603f4a498) |
| [neural-networks/autograd.el](../modules/neural-networks/autograd.md) | [Autograd](../modules/neural-networks/autograd.md#api-fe9b9dee2c2f03ef38d0)、[Autograd.square](../modules/neural-networks/autograd.md#api-c7cdb29630ea7e9ca4c3)、[Autograd.sum](../modules/neural-networks/autograd.md#api-4c5a860a89bb4e088fe1)、[Autograd.mean](../modules/neural-networks/autograd.md#api-31175d2b66a5ce9e4d5f)、[Autograd.variable](../modules/neural-networks/autograd.md#api-ab3276f9117e60133442)、[Autograd.valueAndGrad](../modules/neural-networks/autograd.md#api-2c37c8b473d37f9243b7) |
| [neural-networks/data/index.el](../modules/neural-networks/data/index.md) | [DataLoader](../modules/neural-networks/data/index.md#api-e8831068236aaaf353d3)、[DataLoader.hasNext](../modules/neural-networks/data/index.md#api-58e98b45921aef94fd81)、[DataLoader.save](../modules/neural-networks/data/index.md#api-e9c87836c8629fb1669a)、[DataLoader.restore](../modules/neural-networks/data/index.md#api-45d2fb6c47561221639f)、[DataLoader.next~collate](../modules/neural-networks/data/index.md#api-d4dc9ac658fe6e9c968a)、[DataLoader.next~samples](../modules/neural-networks/data/index.md#api-4232412f3e2beb1e4a64) |
| [neural-networks/functional.el](../modules/neural-networks/functional.md) | [softmax](../modules/neural-networks/functional.md#api-b4b475e208e3fc45c7a0)、[logSoftmax](../modules/neural-networks/functional.md#api-1764884006cd0be44f7e)、[crossEntropy](../modules/neural-networks/functional.md#api-6cc740068d672b42626f)、[oneHot](../modules/neural-networks/functional.md#api-956d05922bbc9c543e7d) |
| [neural-networks/index.el](../modules/neural-networks/index.md) | 模块说明 |
| [neural-networks/losses/index.el](../modules/neural-networks/losses/index.md) | [reduceLoss](../modules/neural-networks/losses/index.md#api-a63260eef4f189bf2f49)、[maeLoss](../modules/neural-networks/losses/index.md#api-cc55a668339edc941395)、[huberLoss](../modules/neural-networks/losses/index.md#api-86753a5a07c600430493) |
| [neural-networks/model.el](../modules/neural-networks/model.md) | [Linear](../modules/neural-networks/model.md#api-f9616a28e08030b55cfb)、[ReLU](../modules/neural-networks/model.md#api-f46f2b7a970cd6420534)、[Sequential](../modules/neural-networks/model.md#api-3de3a8b723127e06dd74)、[Sequential.forward](../modules/neural-networks/model.md#api-daa36f8828e242c94dc1)、[valueAndGrad](../modules/neural-networks/model.md#api-74a208b8786c54fae08b) |
| [neural-networks/optimizer.el](../modules/neural-networks/optimizer.md) | [SGD](../modules/neural-networks/optimizer.md#api-6d3c31621381d78a2d47)、[SGD.update](../modules/neural-networks/optimizer.md#api-fda9885666e0c1fb1e9b) |
| [neural-networks/text/config.el](../modules/neural-networks/text/config.md) | [DecoderConfig](../modules/neural-networks/text/config.md#api-421a6ec1d0a5c1f04046) |
| [neural-networks/text/data.el](../modules/neural-networks/text/data.md) | [LanguageModelWindows](../modules/neural-networks/text/data.md#api-0a1a45f6971031715620) |
| [neural-networks/text/decoder.el](../modules/neural-networks/text/decoder.md) | [CausalLanguageModel](../modules/neural-networks/text/decoder.md#api-f1bfef9fe7b41a7e212c) |
| [neural-networks/text/generation.el](../modules/neural-networks/text/generation.md) | [GenerationOptions](../modules/neural-networks/text/generation.md#api-2303e0907642e9bc866e) |
| [neural-networks/text/index.el](../modules/neural-networks/text/index.md) | [generateText](../modules/neural-networks/text/index.md#api-4cef645bf57c84498b12) |
| [neural-networks/text/package.el](../modules/neural-networks/text/package.md) | [LanguageModelPackage](../modules/neural-networks/text/package.md#api-a8856762f284ccee6452) |
| [neural-networks/text/tokenizer.el](../modules/neural-networks/text/tokenizer.md) | [trainBytePairTokenizer](../modules/neural-networks/text/tokenizer.md#api-408a7f0e6aa9d7ecfdf8) |
