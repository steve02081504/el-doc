# tools/testing/compiler.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/tools.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 编译夹具 {#api-3bdddcd69863e9b8252f}

源码：`src/stdlib/tools/testing/compiler.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/compiler.el#L1)

在测试上下文中编译指定源码入口并返回可供断言检查的结果。

## FixtureOptions {#api-2c4c4f04dba5902ef37e}

源码：`src/stdlib/tools/testing/compiler.el:14` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/compiler.el#L14)

```el
export class FixtureOptions
```

配置编译夹具的入口、目标、构建模式与超时。

### 示例：设置预期编译入口

```el
import { FixtureOptions } from "el:tools/testing/compiler.el"
let options = FixtureOptions("fixtures/valid.el", mode: "debug")
```

## compileFixture {#api-e87d6eec10bbd8634566}

源码：`src/stdlib/tools/testing/compiler.el:38` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/compiler.el#L38)

```el
export fn compileFixture(entry: Text, options: FixtureOptions = FixtureOptions(entry))
```

在当前测试服务中编译夹具入口，并返回编译结果供 check.compiles 或 check.diagnostic 检查。

**参数**：entry 夹具入口源码路径。

**参数**：options 可选编译目标、模式与超时配置。

**返回值**：编译服务产生的结果。

**失败与异常**：不在运行中的测试上下文调用时抛 TestConfigurationError。

### 示例：编译应当成功的夹具

```el
import { compileFixture } from "el:tools/testing/compiler.el"
let result = compileFixture("fixtures/valid.el")
check.compiles(result)
```
