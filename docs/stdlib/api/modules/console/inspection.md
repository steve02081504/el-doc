# console/inspection.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/console.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## console/inspection {#api-c6f66ef1b07c378f72d8}

源码：`src/stdlib/console/inspection.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/inspection.el#L1)

为控制台输出提供有界、脱离原对象的结构化观察快照；观察过程不调用源码对象的 getter、转换或迭代器。
示例：`let snapshot = consoleSnapshot(@{ count: 3 })`，随后由控制台渲染器格式化快照。

## consoleSnapshot {#api-910227c7fc3db0f2df0b}

源码：`src/stdlib/console/inspection.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/console/inspection.el#L39)

在给定节点、深度、字段及字节预算内观察值并生成展示快照。

```el-signature
export fn consoleSnapshot(borrow value, maxNodes: Integer = Integer(256), maxDepth: Integer = Integer(8), maxFields: Integer = Integer(1024), maxBytes: Integer = Integer(65536)): ConsoleValueSnapshot
```

**返回类型**：[`ConsoleValueSnapshot`](../../types.md#api-e7de35ba94b9edf48d4d)

**参数**：value 要观察的值。

**返回值**：不保留原值的结构化快照。

### 示例：捕获结构化快照

```el
import { consoleSnapshot } from "el:console/"
let snapshot = consoleSnapshot(@{ count: 3 })
```
