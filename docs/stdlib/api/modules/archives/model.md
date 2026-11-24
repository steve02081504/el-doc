# archives/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/archives.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 归档数据模型 {#api-9569ac1126abcec5d820}

源码：`src/stdlib/archives/model.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/model.el#L1)

定义归档条目、格式选项和资源预算。

## ArchiveOptions {#api-fb8f27ddabacf5633ba8}

源码：`src/stdlib/archives/model.el:85` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/archives/model.el#L85)

选择数位归档配置

```el-signature
export @assign(mode: "copy") class ArchiveOptions
```

### 示例：按基数二编码

```el
import { ArchiveOptions } from "el:archives/"
let options = ArchiveOptions(radix: 2)
```
