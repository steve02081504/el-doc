# operating-system/paths/path.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/operating-system.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 原生路径 {#api-cf10f19bd39a545017c3}

源码：`src/stdlib/operating-system/paths/path.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/paths/path.el#L1)

提供原生文件系统路径表示和操作。

## Path {#api-c0394889c4c86e2384bc}

源码：`src/stdlib/operating-system/paths/path.el:177` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/paths/path.el#L177)

表示原生文件系统路径；支持查询父路径、名称及使用 / 拼接路径。

```el-signature
@assign(mode: "copy")
export class Path extends TextOperand
```

### 示例：用法

```el
let path = Path("reports") / "result.txt"
let name = path.name
```
