# theme/model.el

本页由源码注释生成；示例未运行验证。

## 主题模型 {#api-86ff18a8894db178fcbf}

源码：`src/stdlib/theme/model.el:5` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/model.el#L5)

描述界面主题角色、按父主题继承计算的上下文，以及主题计算和解析结果的数据类型。

## ThemeValues {#api-a5393d1df1641800ca1f}

源码：`src/stdlib/theme/model.el:46` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/model.el#L46)

```el
export @assign(mode: "shared") class ThemeValues
```

从动态字段集合构造并校验显式主题角色值；只接受已知颜色或度量角色。

**参数**：values 角色名到普通 Number 的映射。

**失败与异常**：遇到未知角色、冲突别名或超范围数值时抛出 ThemeError。

### 示例：创建局部主题值

```el
let values = ThemeValues(@{base100: 0x191B20; primary: 0x80A7F0})
```

## ThemeContext {#api-49fc863aa032653764b7}

源码：`src/stdlib/theme/model.el:100` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/model.el#L100)

```el
export @assign(mode: "shared") class ThemeContext
```

向主题计算回调提供外部环境值以及可选的父级解析主题。

### 示例：为主题计算创建空上下文

```el
let context = ThemeContext()
```

## Theme {#api-2f8f76e6db4068dfe678}

源码：`src/stdlib/theme/model.el:113` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/theme/model.el#L113)

```el
export @assign(mode: "shared") class Theme
```

表示显式角色值或按 ThemeContext 计算角色值的主题；计算结果在解析时校验。

### 示例：定义局部主题计算

```el
let theme = Theme(fn(context: ThemeContext) => @{base100: 0x191B20; primary: 0x80A7F0})
```
