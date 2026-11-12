# tools/testing/registry.el

本页由源码注释生成；示例未运行验证。

## 测试注册表 {#api-9e23dc64691268adfbdb}

源码：`src/stdlib/tools/testing/registry.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/registry.el#L1)

在测试声明阶段登记用例，并在执行前冻结为稳定的测试清单。

## TestRegistrar.each {#api-e087607adc055d5b5e61}

源码：`src/stdlib/tools/testing/registry.el:88` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/registry.el#L88)

```el
fn each(name: Text, rows, body, options: TestOptions = TestOptions())
```

为具有稳定名称的行逐条注册测试用例。

**参数**：name 测试组名称。

**参数**：rows 每行须包含唯一稳定的 name 字段。

**参数**：body 接收当前行并执行断言的回调。

**参数**：options 每个注册用例使用的测试选项。

**失败与异常**：行没有名称或注册冲突时抛 TestConfigurationError。

### 示例：表驱动测试

```el
test.each("double", @[
	@{ name: "one", input: 1, expected: 2 },
	@{ name: "two", input: 2, expected: 4 }
], row => check.equal(double(row.input), row.expected))
```

## test {#api-4c6c984c48f4dee1a8af}

源码：`src/stdlib/tools/testing/registry.el:109` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/registry.el#L109)

```el
export lazy let test
```

注册一个测试用例；用例主体在测试执行阶段调用，可选择接收 TestContext。

### 示例：注册简单测试

```el
import { test, check } from "el:tools/testing/index.el"
test("加法", () => check.equal(2 + 2, 4))
```
