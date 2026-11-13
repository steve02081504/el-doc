# user-interface/window.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/user-interface.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 原生窗口 {#api-1c0e1a4b5f5d4b810589}

源码：`src/stdlib/user-interface/window.el:11` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L11)

将界面定义或数据视图挂接到宿主窗口，并提供事件循环入口；具体绘制由当前平台后端完成。

## installWindowThemes {#api-9b300e6c002e44fe8077}

源码：`src/stdlib/user-interface/window.el:50` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L50)

```el
export fn installWindowThemes(window, root: Definition, environment = void, loader: (fn(any): Theme) | void_t = void, loaderRevision: (fn(): Number) | void_t = void, prepare: (fn(Bool): void_t) | void_t = void)
```

将主题加载与刷新生命周期绑定到窗口；窗口关闭时刷新控制器随 View 释放。

**参数**：window 已创建的原生窗口。

**参数**：root 窗口视图的根定义。

**参数**：environment 可选的主题环境。

**参数**：loader 可选的主题加载回调。

**参数**：loaderRevision 可选的加载器修订号回调，用于判断缓存是否过期。

**参数**：prepare 可选的刷新前准备回调。

**返回值**：已安装主题刷新的窗口。

### 示例：用默认主题打开定义

```el
let window = showWindow(element("label", "欢迎"))
runWindow(window)
```

<span id="api-3906d489e4796caf3b0c"></span>

## showWindow~definition {#api-7620d642b498e399181d}

源码：`src/stdlib/user-interface/window.el:114` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L114)

```el
export fn showWindow(definition: Definition, title: Text = "EL", width: Number = 480, height: Number = 360)
```

根据界面定义创建并显示原生窗口，安装默认主题刷新。

**参数**：definition 窗口根定义。

**参数**：title 窗口标题。

**参数**：width 初始宽度。

**参数**：height 初始高度。

**返回值**：新建窗口句柄。

**失败与异常**：当前目标没有原生窗口实现或窗口创建失败时抛出错误。

### 示例：显示一个简单窗口

```el
let window = showWindow(element("label", "欢迎"), "问候", 480, 320)
runWindow(window)
```

## showWindow~data {#api-e81851aac339b39d7c75}

源码：`src/stdlib/user-interface/window.el:130` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L130)

```el
export fn showWindow(source, title: Text = "EL", width: Number = 480, height: Number = 360)
```

将网格或受支持的数据源包装为数据视图后创建原生窗口。

**参数**：source 由 dataView 支持的数据源。

**参数**：title 窗口标题。

**参数**：width 初始宽度。

**参数**：height 初始高度。

**返回值**：新建窗口句柄。

### 示例：显示网格数据

```el
let window = showWindow(rows, "数据")
runWindow(window)
```

## showWindow~description {#api-a2854832980685a2c064}

源码：`src/stdlib/user-interface/window.el:148` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L148)

```el
export fn showWindow(description: Text, title: Text = "EL", width: Number = 480, height: Number = 360)
```

将受限的界面描述文本解析为对象图，再创建原生窗口。

**参数**：description 界面描述文本，不会作为 EL 源码求值。

**参数**：title 窗口标题。

**参数**：width 初始宽度。

**参数**：height 初始高度。

**返回值**：新建窗口句柄。

**失败与异常**：描述格式错误或窗口创建失败时抛出错误。

### 示例：从描述创建窗口

```el
let window = showWindow("column { label: \\\"你好\\\" }", "问候")
runWindow(window)
```

## showWindow~description-data {#api-a2a3a0d3094ea4e44215}

源码：`src/stdlib/user-interface/window.el:165` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/user-interface/window.el#L165)

```el
export fn showWindow(description: Text, source, width: Number = 480, height: Number = 360)
```

将描述文本解析为对象图，并把数据源作为描述中的显式绑定。

**参数**：description 界面描述文本。

**参数**：source 绑定到描述中的数据视图数据源。

**参数**：width 初始宽度。

**参数**：height 初始高度。

**返回值**：新建窗口句柄。

### 示例：在描述窗口中绑定数据

```el
let window = showWindow("column { grid: $0 }", rows)
runWindow(window)
```
