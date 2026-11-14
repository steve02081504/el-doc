# memory/allocation/pressure.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/memory.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 成员总览

- [ReclaimRegistration.close](#api-d88d4fd3c0806624a27d)
- [MemoryPressure.install](#api-bd17e2436ac452296350)
- [MemoryPressure.register_reclaimer](#api-d793fcf9bb26d2c0a1b1)
- [MemoryPressure.needs_refill](#api-5170bd3e63658901a65d)
- [MemoryPressure.refill](#api-afd4944353952e9a493a)
- [MemoryPressure.reclaim](#api-23f93e549cc1866c7906)
- [MemoryPressure.close](#api-0c5a84044c0742c3b9ba)

## 内存压力回收服务 {#api-f8fe06c86c7b49b05e3e}

源码：`src/stdlib/memory/allocation/pressure.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L1)

显式安装回收服务并管理回调和储备；导入本模块不会安装服务。

## MemoryPressureStateError {#api-37be22995aa184e8d4db}

源码：`src/stdlib/memory/allocation/pressure.el:28` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L28)

压力服务处于无效状态时抛出的错误。

```el
export @assign(mode: "copy") class MemoryPressureStateError extends Error
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
pressure.close()
```

## ReclaimRegistration {#api-66b03d8c0b1ef268ec44}

源码：`src/stdlib/memory/allocation/pressure.el:61` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L61)

回收回调的共享注册句柄；close 或析构取消注册。

```el
export @assign(mode: "shared") class ReclaimRegistration
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let registration = pressure.register_reclaimer(fn(bytes) { return nil })
registration.close()
pressure.close()
```

## ReclaimRegistration.close {#api-d88d4fd3c0806624a27d}

源码：`src/stdlib/memory/allocation/pressure.el:75` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L75)

取消注册；重复调用无操作。

```el
fn close()
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let registration = pressure.register_reclaimer(fn(bytes) { return nil })
registration.close()
pressure.close()
```

## MemoryPressure {#api-3cf76fe53a08ce9b879e}

源码：`src/stdlib/memory/allocation/pressure.el:94` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L94)

显式构造的压力服务；可安装进程回调、保留储备并登记回收器，使用后调用 close。

```el
export @assign(mode: "shared") class MemoryPressure
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
pressure.install()
pressure.close()
```

## MemoryPressure.install {#api-bd17e2436ac452296350}

源码：`src/stdlib/memory/allocation/pressure.el:143` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L143)

安装进程压力回调；已关闭、正在关闭、已安装或安装失败时抛出 MemoryPressureStateError。

```el
fn install()
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
pressure.install()
pressure.close()
```

## MemoryPressure.register_reclaimer {#api-d793fcf9bb26d2c0a1b1}

源码：`src/stdlib/memory/allocation/pressure.el:167` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L167)

注册接收请求字节数并返回是否取得进展的回调；保留返回的注册句柄以维持注册。回调异常记录在 last_failure。

```el
fn register_reclaimer(callback: fn(bytes: Integer): Bool): ReclaimRegistration
```

**返回类型**：[`ReclaimRegistration`](pressure.md#api-66b03d8c0b1ef268ec44)

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let registration = pressure.register_reclaimer(fn(bytes) { return nil })
registration.close()
pressure.close()
```

## MemoryPressure.needs_refill {#api-5170bd3e63658901a65d}

源码：`src/stdlib/memory/allocation/pressure.el:217` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L217)

查询储备是否需要且可以尝试补充。

```el
fn needs_refill(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let needed = pressure.needs_refill()
pressure.close()
```

## MemoryPressure.refill {#api-afd4944353952e9a493a}

源码：`src/stdlib/memory/allocation/pressure.el:232` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L232)

尝试补充一个储备块；成功返回 t，无法补充时返回 nil。

```el
fn refill(): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let added = pressure.refill()
pressure.close()
```

## MemoryPressure.reclaim {#api-23f93e549cc1866c7906}

源码：`src/stdlib/memory/allocation/pressure.el:275` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L275)

释放至多一个储备块并依次调用当前登记的回收器；任一操作有进展时返回 t。回调异常记录在 last_failure。

```el
fn reclaim(bytes: Integer): Bool
```

**返回类型**：[`Bool`](../../language/values.md#api-3f0af31783849ef30c6e)

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
let progress = pressure.reclaim(1024)
pressure.close()
```

## MemoryPressure.close {#api-0c5a84044c0742c3b9ba}

源码：`src/stdlib/memory/allocation/pressure.el:327` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/memory/allocation/pressure.el#L327)

卸载进程回调、等待进行中的回收或补充并释放储备和注册；重复调用无操作。在自身回收回调中调用会抛出 MemoryPressureStateError。

```el
fn close()
```

### 示例：使用示例

```el
import { MemoryPressure } from "el:memory/allocation/pressure.el"
let pressure = MemoryPressure()
pressure.close()
```
