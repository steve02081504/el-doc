# numerical-computing/device-value.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 设备张量值 {#api-3e44b19315248867cc5a}

源码：`src/stdlib/numerical-computing/device-value.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/device-value.el#L1)

设备张量值相关接口。

## DeviceTensor {#api-572c72917d65007ba8a7}

源码：`src/stdlib/numerical-computing/device-value.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/device-value.el#L79)

按元素类型和精度生成设备张量值类型，设备分配的生命周期由其租约管理。

```el-signature
export fn DeviceTensor(element: type, precision: Text = ""): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
import { DeviceTensor } from "el:numerical-computing/device-value.el"
let Values = DeviceTensor<element: Number>
```
