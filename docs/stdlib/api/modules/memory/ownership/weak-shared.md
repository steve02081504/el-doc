# memory/ownership/weak-shared.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 共享对象弱引用 {#api-68d0290fe276cdac004a}

源码：`src/stdlib/memory/ownership/weak-shared.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/ownership/weak-shared.el#L1)

共享对象弱引用相关接口。

## WeakShared {#api-4d13a5e69bf02df13422}

源码：`src/stdlib/memory/ownership/weak-shared.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/ownership/weak-shared.el#L28)

生成共享对象的弱引用类型；lock 在对象仍存活时取得拥有引用，否则返回 nil。构造时无法创建令牌会抛出 WeakReferenceError。

```el-signature
export fn WeakShared(element: type): type
```

**返回类型**：[`type`](../../../../../reference/language/types.md)

### 示例：用法

```el
import { WeakShared } from "el:memory/ownership/weak-shared.el"
fn makeWeak(value) {
	let Weak = WeakShared<element: typeof(value)>
	return Weak(value)
}
```
