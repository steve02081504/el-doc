# desktop-automation/launch.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/desktop-automation.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## desktop-automation/launch {#api-7ef9fa443bf6d31c3eb9}

源码：`src/stdlib/desktop-automation/launch.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/launch.el#L1)

通过当前桌面环境打开原生文件路径或带明确 scheme 的 URI。
本地文件应使用绝对 `Path`；`file:` URI 由 `openDesktopPath` 处理，避免路径歧义。

## openDesktopUri {#api-e5eb95e09b6d21180866}

源码：`src/stdlib/desktop-automation/launch.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/desktop-automation/launch.el#L37)

请求桌面环境打开 URI。URI 必须包含明确 scheme 且不得含空白/控制字符；Windows 上拒绝单字母盘符形式，`file:` scheme 应改用 `openDesktopPath`。

```el-signature
export fn openDesktopUri(uri: Text)
```

**参数**：uri 含 scheme 的 URI 文本。

### 示例：打开 HTTPS 地址

```el
openDesktopUri("https://example.com")
```
