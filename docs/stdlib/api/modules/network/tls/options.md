# network/tls/options.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/network.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## TLS 配置 {#api-1bd3cf77cda715824641}

源码：`src/stdlib/network/tls/options.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/tls/options.el#L1)

描述 TLS 信任来源与握手资源限制。

## TlsOptions {#api-d66684475437485e3301}

源码：`src/stdlib/network/tls/options.el:21` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/network/tls/options.el#L21)

配置 TLS 信任来源和证书、链及握手数据的可选资源上限。

```el-signature
export class TlsOptions
```

**参数**：changes 以字段名提供选项；trustAnchors 会在构造时复制。

**失败与异常**：资源上限不是非负整数，或显式信任锚超出字节上限时抛出 NetworkError。

### 示例：限制证书链长度

```el
import { TlsOptions } from "el:network/tls/options.el"
let tls = TlsOptions(@{ maximumChainLength: 8 })
console.stdout.writeLine(tls.maximumChainLength)
```
