# platform/build.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/platform.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 构建事实 {#api-c5946abbe985eaf8c368}

源码：`src/stdlib/platform/build.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/build.el#L6)

提供从当前所选构建产物读取的静态构建配置。

## debug_mode {#api-6627dfa1f08b2c8d69e4}

源码：`src/stdlib/platform/build.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/platform/build.el#L17)

查询所选构建产物是否启用了调试模式。

```el-signature
export fn debug_mode()
```

**返回值**：构建描述符中的调试标志；不读取进程环境。

### 示例：查询调试构建标志

```el
let enabled = debug_mode()
```
