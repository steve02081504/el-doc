# tools/testing/check.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/tools.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [Checks.equal](#api-9bc8bfe594dbb59dd408)
- [Checks.same](#api-614ee7f25af8cfe5ae5c)
- [Checks.near](#api-5c82c4bd1b5ec6b37fdb)
- [Checks.throws](#api-8db3d707f3691300a2a5)
- [Checks.items](#api-e911952584eb01963356)
- [Checks.collect](#api-80bbd1f2ffdd433e943e)
- [Checks.snapshot](#api-a2dedfe1b1939a02b3e0)
- [Checks.compiles](#api-2e049b79fd2a4c6c9dcb)
- [Checks.diagnostic](#api-ca64dd756b7a7d68a372)

## 测试比较断言 {#api-f960aaa2ccb3388fd730}

源码：`src/stdlib/tools/testing/check.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L1)

提供带实际值、期望值与失败路径信息的测试比较接口。

## Checks.equal {#api-9bc8bfe594dbb59dd408}

源码：`src/stdlib/tools/testing/check.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L29)

```el
fn equal(borrow actual, borrow expected)
```

使用值相等语义比较实际值与期望值，失败时报告两侧快照。

**参数**：actual 实际值。

**参数**：expected 期望值。

**失败与异常**：值不相等时抛出 TestFailure。

### 示例：比较计算结果

```el
check.equal(2 + 2, 4)
```

## Checks.same {#api-614ee7f25af8cfe5ae5c}

源码：`src/stdlib/tools/testing/check.el:40` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L40)

```el
fn same(borrow actual, borrow expected)
```

使用身份相等比较两个值，而不比较其内容。

**参数**：actual 实际值。

**参数**：expected 期望的同一对象。

**失败与异常**：两者身份不同时时抛出 TestFailure。

### 示例：检查对象身份

```el
let value = @{}
check.same(value, value)
```

## Checks.near {#api-5c82c4bd1b5ec6b37fdb}

源码：`src/stdlib/tools/testing/check.el:52` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L52)

```el
fn near(actual: Number, expected: Number, absolute: Number, relative: Number)
```

按显式绝对与相对容差比较两个数值。

**参数**：actual 实际数值。

**参数**：expected 期望数值。

**参数**：absolute 非负有限绝对容差。

**参数**：relative 非负有限相对容差。

**失败与异常**：容差配置无效或数值差异超出容差时抛出异常。

### 示例：比较浮点结果

```el
check.near(0.1 + 0.2, 0.3, absolute: 0.000001, relative: 0)
```

## Checks.throws {#api-8db3d707f3691300a2a5}

源码：`src/stdlib/tools/testing/check.el:68` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L68)

```el
fn throws(expected: type, body)
```

断言回调抛出指定类型的异常，并返回捕获到的异常值。

**参数**：expected 预期异常类型。

**参数**：body 要调用的无参回调。

**返回值**：捕获的预期异常。

**失败与异常**：回调未抛异常或抛出其他类型时抛出 TestFailure。

### 示例：检查缺失键错误

```el
check.throws(MissingKeyError, () => scores["missing"])
```

## Checks.items {#api-e911952584eb01963356}

源码：`src/stdlib/tools/testing/check.el:87` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L87)

```el
fn items(borrow actual, borrow expected)
```

按位置逐项比较两个有限序列，并报告长度或首个不同元素。

**参数**：actual 实际序列。

**参数**：expected 期望序列。

**失败与异常**：长度或任一元素不相等时抛出 TestFailure。

### 示例：比较数组内容

```el
check.items(@[1, 2], @[1, 2])
```

## Checks.collect {#api-80bbd1f2ffdd433e943e}

源码：`src/stdlib/tools/testing/check.el:104` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L104)

```el
fn collect(body)
```

执行一组比较并聚合其中的比较失败，结束后一次报告。

**参数**：body 要执行的无参比较回调。

**失败与异常**：聚合范围内存在失败时抛出 TestFailure；不允许嵌套收集。

### 示例：聚合多项检查

```el
check.collect(() => {
	check.equal(2 + 2, 4)
	check.same("x", "x")
})
```

## Checks.snapshot {#api-a2dedfe1b1939a02b3e0}

源码：`src/stdlib/tools/testing/check.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L122)

```el
fn snapshot(borrow value, key: Text, encode = defaultSnapshot)
```

将编码后的值按当前测试上下文中的键记录为快照。

**参数**：value 要快照的值。

**参数**：key 当前测试内稳定且唯一的快照键。

**参数**：encode 将值编码为文本的函数，默认使用 EOL。

**失败与异常**：不在测试上下文中调用时抛 TestConfigurationError。

### 示例：记录快照

```el
check.snapshot(@{ status: "ready" }, key: "response")
```

## Checks.compiles {#api-2e049b79fd2a4c6c9dcb}

源码：`src/stdlib/tools/testing/check.el:135` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L135)

```el
fn compiles(borrow result)
```

断言编译结果成功并生成产物。

**参数**：result compileFixture 返回的编译结果。

**失败与异常**：编译失败或没有产物时抛 TestFailure。

### 示例：检查源码可编译

```el
check.compiles(compileFixture("valid.el"))
```

## Checks.diagnostic {#api-ca64dd756b7a7d68a372}

源码：`src/stdlib/tools/testing/check.el:152` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L152)

```el
fn diagnostic(borrow result, phase: Text, code: Text, source: Text = "", line: Number = 0, column: Number = 0, marker: Text = "")
```

断言编译失败并包含指定阶段、诊断码与源码位置。

**参数**：result compileFixture 返回的编译结果。

**参数**：phase 预期诊断阶段。

**参数**：code 预期诊断码。

**参数**：source 可选的源码路径，默认使用入口文件。

**参数**：line 可选的源码行号。

**参数**：column 可选的列号；0 表示不检查列。

**参数**：marker 可选源码标记，优先由服务解析其位置。

**失败与异常**：诊断不匹配或缺少位置时抛出 TestFailure。

### 示例：检查私有访问诊断

```el
check.diagnostic(result, phase: "check", code: "EL.ACCESS.PRIVATE", marker: "denied")
```

## check {#api-b55c78812b9aee65b8c4}

源码：`src/stdlib/tools/testing/check.el:173` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/check.el#L173)

```el
export lazy let check = Checks()
```

**类型**：[`Checks`](../../../types.md#api-a49fc65730d49506a183)

提供比较断言入口；失败时抛出带结构化差异信息的 TestFailure。

### 示例：比较实际值与期望值

```el
import { check } from "el:tools/testing/index.el"
check.equal(2 + 2, 4)
```
