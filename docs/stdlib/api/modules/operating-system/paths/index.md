# operating-system/paths/index.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/operating-system.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 原生路径操作 {#api-6e634356471b2db68c06}

源码：`src/stdlib/operating-system/paths/index.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/paths/index.el#L1)

原生路径操作相关接口。

## make_directories {#api-e01bd63582a195d4241c}

源码：`src/stdlib/operating-system/paths/index.el:39` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/paths/index.el#L39)

请求创建路径及其父目录并返回原路径；实际操作使用当前平台实现。

```el-signature
@discardable export fn make_directories(path: Path): Path
```

**返回类型**：[`Path`](path.md#api-c0394889c4c86e2384bc)

### 示例：用法

```el
import { Path, make_directories } from "el:operating-system/paths/index.el"
let directory = make_directories(Path("output/reports"))
```
