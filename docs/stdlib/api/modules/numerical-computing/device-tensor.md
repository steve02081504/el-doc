# numerical-computing/device-tensor.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 设备张量操作 {#api-1c00d19da8d93dca1521}

源码：`src/stdlib/numerical-computing/device-tensor.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/device-tensor.el#L1)

设备张量操作相关接口。

## TensorDevice {#api-6352f607871fe7944c1e}

源码：`src/stdlib/numerical-computing/device-tensor.el:79` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/device-tensor.el#L79)

按元素类型和精度生成设备张量操作类型。设备资源和实际执行依赖所用设备上下文。

```el-signature
export fn TensorDevice(element: type, precision: Text = ""): type
```

**返回类型**：[`type`](../../../../reference/language/types.md)

### 示例：用法

```el
import { TensorDevice } from "el:numerical-computing/device-tensor.el"
let FloatDevice = TensorDevice<element: Number>
```
