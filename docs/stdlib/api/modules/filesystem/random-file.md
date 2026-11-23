# filesystem/random-file.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/filesystem.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 私有随机文件 {#api-1ad8ac08477cf0b9ea79}

源码：`src/stdlib/filesystem/random-file.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/random-file.el#L1)

提供私有文件所有者与可用于格式读写的隔离文件系统上下文。

## PrivateRandomFileSystem {#api-e1f95c660f660a0447cc}

源码：`src/stdlib/filesystem/random-file.el:44` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/filesystem/random-file.el#L44)

创建私有随机文件及其逻辑文件系统上下文。该上下文中的 data 位置由此对象独占。

```el-signature
export @assign(mode: "shared") class PrivateRandomFileSystem
```

**参数**：parent 可选的原生临时文件父级逻辑位置。

### 示例：通过逻辑写入接口改写一个私有文件

```el
import { PrivateRandomFileSystem } from "el:filesystem/random-file.el"
import { writeFileAs } from "el:filesystem/"
import { formats } from "el:formats/"
scope let scratch = PrivateRandomFileSystem()
discard(writeFileAs(formats.Text, scratch.context.resolve("data"), "scratch"))
```
