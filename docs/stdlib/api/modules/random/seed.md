# random/seed.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/random.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 随机种子 {#api-d7616efa16378f16436e}

源码：`src/stdlib/random/seed.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/seed.el#L1)

从平台熵源或墙上时间取得随机数生成器种子。

## generateSeed {#api-36d3ff723851611bfabb}

源码：`src/stdlib/random/seed.el:23` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/seed.el#L23)

```el
export fn generateSeed(): Number
```

从当前平台的系统熵来源取得随机种子。

### 示例：读取系统随机种子

```el
import { generateSeed } from "el:random/seed.el"
let seed = generateSeed()
```
预期结果：取得一个种子数值；系统熵不可用时抛 EntropyUnavailable。

**返回值**：Number。

## automaticSeed {#api-4425691b7b12732b9f8a}

源码：`src/stdlib/random/seed.el:35` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/random/seed.el#L35)

```el
export fn automaticSeed(): Number
```

优先取得系统随机种子；熵不可用时使用当前墙上时间纳秒构造种子。

### 示例：取得自动种子

```el
import { automaticSeed } from "el:random/seed.el"
let seed = automaticSeed()
```
预期结果：取得一个种子数值。

**返回值**：Number。

**失败与异常**：系统种子失败且错误并非 EntropyUnavailable 时，原错误向调用者传播。
