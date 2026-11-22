# execution/plans/policy.el

本页由源码注释生成；示例未运行验证。

[库分类](../../../categories/execution.md) · [模块索引](../../../modules.md) · [符号索引](../../../symbols.md)

## 执行计划策略 {#api-1a808f7c3c5411419010}

源码：`src/stdlib/execution/plans/policy.el:8` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/execution/plans/policy.el#L8)

定义执行候选的优先级策略及常用执行方式。

## ordered {#api-6f698621dbbade2900eb}

源码：`src/stdlib/execution/plans/policy.el:19` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/execution/plans/policy.el#L19)

按传入顺序拼接多个策略中的执行候选。

```el-signature
export fn ordered(policies: ExecutionPolicy[]): ExecutionPolicy
```

**返回类型**：[`ExecutionPolicy`](../../../types.md#api-c4e22112663baf382e33)

**参数**：policies 按优先顺序排列的执行策略。

**返回值**：候选依次来自各策略的新策略。

### 示例：先尝试原生执行，再尝试普通执行

```el
let policy = ordered(@[native, normal])
```

## normal {#api-6cb84250e3385e250faf}

源码：`src/stdlib/execution/plans/policy.el:30` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/execution/plans/policy.el#L30)

选择普通 EL 执行候选。

```el-signature
export const normal = ExecutionPolicy(@[ExecutionCandidate("normal")])
```

### 示例：使用普通执行策略

```el
let policy = normal
```

## native {#api-ead5f19b82668f54a168}

源码：`src/stdlib/execution/plans/policy.el:37` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/execution/plans/policy.el#L37)

选择原生执行候选。

```el-signature
export const native = ExecutionPolicy(@[ExecutionCandidate("native")])
```

### 示例：使用原生执行策略

```el
let policy = native
```

## simd {#api-4c151a1c2a977576eed9}

源码：`src/stdlib/execution/plans/policy.el:45` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/execution/plans/policy.el#L45)

选择 SIMD 执行候选。

```el-signature
export const simd = ExecutionPolicy(@[ExecutionCandidate("simd")])
```

### 示例：使用 SIMD 执行策略

```el
let policy = simd
```
