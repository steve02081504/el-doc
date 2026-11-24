# platform/target-units.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/platform.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 目标计数单位 {#api-05c3e321304123dbda40}

源码：`src/stdlib/platform/target-units.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/target-units.el#L1)

编译目标的基本数位基数和地址单元大小。

## dit_radix {#api-92bbb4a4021817785b4e}

源码：`src/stdlib/platform/target-units.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/target-units.el#L16)

编译目标的每个基本数位可表示的状态数。二进制目标返回 2，三进制目标返回 3。

```el-signature
export fn dit_radix(): Integer
```

**返回类型**：[`Integer`](machine/integer.md#api-45690472287900730a5f)

### 示例：查询目标基数

```el
import { dit_radix } from "el:platform/target.el"
let radix = dit_radix()
```
