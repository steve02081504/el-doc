# theme/resolve.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/theme.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 主题解析 {#api-fe678f4cb198fe141607}

源码：`src/stdlib/theme/resolve.el:3` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/resolve.el#L3)

将局部主题、父主题和默认值合成为完整角色表，并报告颜色对比度问题。

## resolveTheme {#api-f08855dc7eaf1293eeb0}

源码：`src/stdlib/theme/resolve.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/resolve.el#L35)

```el
export fn resolveTheme(theme: Theme, context: ThemeContext = ThemeContext()): ResolvedTheme
```

**返回类型**：`ResolvedTheme`

根据主题及可选父级上下文生成完整的解析主题，缺失角色使用生成值或基线值补齐。

**参数**：theme 要解析的主题。

**参数**：context 环境和可选父主题上下文。

**返回值**：包含完整角色值及对比度问题的 ResolvedTheme。

**失败与异常**：主题含无效角色或无效数值时抛出 ThemeError。

### 示例：解析一个局部主题

```el
let resolved = resolveTheme(Theme(@{base100: 0x191B20}))
let primary = resolved.value("primary")
```
