# runtime/native-types.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/runtime.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 原生运行时数值类型 {#api-2d52deace4ea389a8ec2}

源码：`src/stdlib/runtime/native-types.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/runtime/native-types.el#L1)

原生运行时数值类型相关接口。

## NativeSignedWord {#api-b33b987a810fb17f83e0}

源码：`src/stdlib/runtime/native-types.el:25` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/runtime/native-types.el#L25)

目标原生字宽的有符号整数，用于运行时的机器字接口。

```el-signature
@builtin:vome:signed:integer(format: "native.word") export class NativeSignedWord
```

### 示例：用法

```el
import { NativeSignedWord } from "el:runtime/native-types.el"
let value = NativeSignedWord(1)
```

## NativeStorageSize {#api-56e936010cbf9fb04ba1}

源码：`src/stdlib/runtime/native-types.el:122` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/runtime/native-types.el#L122)

表示原生存储大小的整数类型。

```el-signature
@builtin:vome:size:integer export class NativeStorageSize
```

### 示例：用法

```el
import { NativeStorageSize } from "el:runtime/native-types.el"
let size = NativeStorageSize(8)
```
