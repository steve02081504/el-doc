# tools/testing/declarations.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/tools.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 测试声明语法 {#api-c3b5570499ded5141ba0}

源码：`src/stdlib/tools/testing/declarations.el:6` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/declarations.el#L6)

将测试声明体转换为测试注册集合，并提供按类型注册的测试语法。

## tests {#api-6f26c498861625049404}

源码：`src/stdlib/tools/testing/declarations.el:17` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/testing/declarations.el#L17)

将花括号中的声明体收集为测试注册作用域。

```el-signature
export syntax tests
```

### 示例：声明一个测试集合

```el
tests {
	check(1 + 1 == 2)
}
```
