# tools/formatter/scan.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/tools.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 格式化器词法扫描 {#api-b37144e092daada0aa82}

源码：`src/stdlib/tools/formatter/scan.el:7` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/formatter/scan.el#L7)

扫描源码并收集格式化所需的词法事实与属性诊断。

## scan {#api-e0817f615a6c850f7872}

源码：`src/stdlib/tools/formatter/scan.el:312` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/tools/formatter/scan.el#L312)

单遍扫描源码，收集可省略分号、缩进信息及 ELF 属性问题。

```el-signature
export fn scan(text: Text): ScanResult
```

**返回类型**：[`ScanResult`](../../../types.md#api-13baaffc4f0518d9606f)

**参数**：text 待扫描的 EL 源码文本。

**返回值**：扫描结果；遇到未闭合字面量时以 truncated 标记不完整结果。

### 示例：扫描一段源码

```el
let result = scan("let value = 1\\n")
```
