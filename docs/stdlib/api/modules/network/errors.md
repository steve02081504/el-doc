# network/errors.el

本页由源码注释生成；示例未运行验证。

## 网络错误 {#api-3210950d25b55d7d79be}

源码：`src/stdlib/network/errors.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/errors.el#L1)

定义网络操作失败及带操作、细节与平台代码的错误信息。

## NetworkError {#api-31d4ba2d25e2222391e9}

源码：`src/stdlib/network/errors.el:16` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/errors.el#L16)

```el
export class NetworkError extends Error
```

表示网络连接、协议或平台网络操作失败。

### 示例：捕获网络请求错误

```el
try { request("https://example.com/") }
catch (error: NetworkError) { console.stderr.writeLine(error.operation, ": ", error.detail) }
```

## NetworkError.operation {#api-53e0c3fc1ec8e63196e5}

源码：`src/stdlib/network/errors.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/errors.el#L23)

```el
let operation: Text
```

发生失败的网络操作名称。

### 示例：输出错误操作

```el
console.stderr.writeLine(error.operation)
```

## NetworkError.detail {#api-bba6955c6787070c5b63}

源码：`src/stdlib/network/errors.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/errors.el#L30)

```el
let detail: Text
```

描述失败原因的文本。

### 示例：输出错误原因

```el
console.stderr.writeLine(error.detail)
```

## NetworkError.code {#api-0daf359682bcfc8d6e85}

源码：`src/stdlib/network/errors.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/errors.el#L37)

```el
let code: Number
```

平台提供的可选错误代码；无特定代码时为 0。

### 示例：查看平台错误码

```el
console.stderr.writeLine(error.code)
```
