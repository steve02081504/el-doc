# control/selection/policies.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/control.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 候选选择策略 {#api-bcd44b42e72ee695bca8}

源码：`src/stdlib/control/selection/policies.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/control/selection/policies.el#L1)

根据候选目录及已提交的选择历史计算下一项，提供顺序、随机、避免重复及带权策略。

## Sequential {#api-c22f8460d04e3408b529}

源码：`src/stdlib/control/selection/policies.el:20` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/control/selection/policies.el#L20)

依目录顺序选择候选项的策略常量。

```el-signature
export const Sequential = SelectionPolicy.Sequential
```

### 示例：选择顺序策略

```el
let policy = Sequential
```
示例展示接口用法；未运行验证。
