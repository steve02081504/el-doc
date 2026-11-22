# numerical-computing/errors.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/numerical-computing.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 数值计算错误 {#api-55fb5bc66730cc7fcaf0}

源码：`src/stdlib/numerical-computing/errors.el:4` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/errors.el#L4)

定义数值张量和求解器操作报告的错误类型。

## ShapeError {#api-bd68270a10229244e32a}

源码：`src/stdlib/numerical-computing/errors.el:12` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/errors.el#L12)

表示张量形状或秩不满足操作要求。

```el-signature
export @assign(mode: "copy") class ShapeError extends Error
```

### 示例：抛出形状错误

```el
throw ShapeError()
```

## NumericallySingular {#api-99d3f54ceeeb870fa5cb}

源码：`src/stdlib/numerical-computing/errors.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/numerical-computing/errors.el#L20)

表示数值求解遇到奇异或无法稳定求解的系统。

```el-signature
export @assign(mode: "copy") class NumericallySingular extends Error
```

### 示例：抛出奇异系统错误

```el
throw NumericallySingular()
```
