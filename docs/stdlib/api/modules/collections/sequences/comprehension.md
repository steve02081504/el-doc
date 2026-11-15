# collections/sequences/comprehension.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/collections.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 推导式 {#api-2137f1a24bf106e4191f}

源码：`src/stdlib/collections/sequences/comprehension.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension.el#L1)

用投影、顺序绑定和筛选构造保留元素类型的惰性可迭代值；数组形式立即收集结果。

## for {#api-cc9ca1586767db3090d8}

源码：`src/stdlib/collections/sequences/comprehension.el:63` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/sequences/comprehension.el#L63)

以 for let 子句枚举来源，用 if 子句筛选，并产出最前面的投影表达式。
后续来源和条件可以引用前序绑定，投影可以引用全部绑定；绑定只在本推导式内可见。

```el
export syntax for
```

**返回值**：括号和调用实参中的形式返回可重开的惰性可迭代值；直接数组形式立即收集成数组。

**失败与异常**：来源、条件、投影或游标操作的异常正常传播；已有错误与清理错误同时发生时聚合为 CleanupError。

**注意**：多个 for 子句按嵌套循环顺序展开，最右侧变量变化最快；if 可放在两个 for 之间以跳过后续工作。当前 binder 只接受单个名字。

**注意**：创建惰性值和取得游标不执行来源、条件或投影；next 才请求数据。重新迭代会重新求值来源，不缓存结果，也不重置调用方的一次性游标。

**注意**：数组推导式必须是唯一数组项。混合普通元素时显式展开括号生成式，例如 @[0, ...(x for let x in ..2)]。

**注意**：源码表达式在真实闭包中执行，普通 return 不透明退出调用者。当前实现尚未完成原生编译和执行验收，示例为静态核对后的预期行为。

### 示例：枚举两位二进制并筛选相等位

```el
let pairs = @[@[a, b] for let a in ..2 for let b in ..2]
let equalPairs = @[@[a, b] for let a in ..2 for let b in ..2 if a == b]
// pairs：@[@[0, 0], @[0, 1], @[1, 0], @[1, 1]]
// equalPairs：@[@[0, 0], @[1, 1]]
```

### 示例：按需判断是否存在相等组合

```el
import { any, all } from "el:collections/arrays/operations.el"
let exists = any(a == b for let a in ..2 for let b in ..2) // t
let universal = all(a == b for let a in ..2 for let b in ..2) // nil
```

参见：[collections/arrays/operations::any](../arrays/operations.md#api-1fff05563d7e913b33e0)

参见：[collections/arrays/operations::all](../arrays/operations.md#api-aac2646339bc62f9f5a9)
