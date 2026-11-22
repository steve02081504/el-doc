# operating-system/processes/exit.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/operating-system.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 进程退出 {#api-fcb610d49edd45d26f45}

源码：`src/stdlib/operating-system/processes/exit.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/processes/exit.el#L1)

提供经进程完成协调的退出操作。

## exit {#api-1b420f1036b55b10cf6b}

源码：`src/stdlib/operating-system/processes/exit.el:41` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/operating-system/processes/exit.el#L41)

以目标平台范围内的有限整数状态码结束进程；退出前运行进程完成协调。状态码无效、协调失败或退出被拒绝时抛出异常。

```el-signature
export fn exit(code: Number): Never
```

**返回类型**：[`Never`](../../../types.md#api-18b002790bd51c55d228)

### 示例：用法

```el
exit(0)
```
