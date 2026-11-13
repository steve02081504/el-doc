# errors/assertions.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/errors.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 成员总览

- [AssertionError.reason](#api-870d60eb5f4f1d987a9e)

## 断言错误 {#api-c4ee9f181a993c384404}

源码：`src/stdlib/errors/assertions.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/assertions.el#L1)

提供条件断言及其专用失败异常。

## AssertionError {#api-2e44ae11e3d03832b03e}

源码：`src/stdlib/errors/assertions.el:12` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/assertions.el#L12)

```el
export @assign(mode: "shared") class AssertionError extends Error
```

表示 assert 条件失败的异常，并保留调用方提供的失败原因。

### 示例：捕获断言错误

```el
try { assert(nil, "value required") }
catch (error: AssertionError) { console.stderr.writeLine(error.reason) }
```

## AssertionError.reason {#api-870d60eb5f4f1d987a9e}

源码：`src/stdlib/errors/assertions.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/assertions.el#L19)

```el
let reason: Text
```

**类型**：`Text`

断言失败时提供的说明文本。

### 示例：输出断言原因

```el
console.stderr.writeLine(error.reason)
```

## assert {#api-e12e696f440288d77038}

源码：`src/stdlib/errors/assertions.el:34` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/errors/assertions.el#L34)

```el
export @pure fn assert(condition: Bool, reason: Text): Bool
```

**返回类型**：`Bool`

检查条件为真；条件为假时以给定原因抛出 AssertionError。

**参数**：condition 要求为真的条件。

**参数**：reason 断言失败时显示的原因。

**返回值**：成功时返回真。

**失败与异常**：condition 为假时抛 AssertionError。

### 示例：检查集合不为空

```el
import { assert } from "el:tools/testing/index.el"
assert(values.count > 0, "values must not be empty")
```
