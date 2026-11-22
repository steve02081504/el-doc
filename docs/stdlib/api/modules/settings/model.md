# settings/model.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/settings.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## 设置快照与补丁模型 {#api-d7eaf383cbb133161af5}

源码：`src/stdlib/settings/model.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/settings/model.el#L1)

提供不可变设置快照、字段候选和约束模型；按字段路径合并候选值并生成可检测并发冲突的补丁，数据以无代码纯数据形式处理。

## resolveSettingsPatch {#api-c80ade34e4e649b1dbff}

源码：`src/stdlib/settings/model.el:261` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/settings/model.el#L261)

先合并带来源的字段候选，再验证完整候选快照并生成补丁。基线中的已有值视为低于显式候选的取值；仅缺失字段采用默认值。

```el-signature
export fn resolveSettingsPatch(base: SettingsSnapshot, rules: SettingsFieldRule[], values: SettingsValue[], defaults: SettingsValue[]): SettingsPatch
```

**返回类型**：[`SettingsPatch`](../../types.md#api-16f01e4f88e27e324f6b)

### 示例：对空快照解析无字段补丁（需调用方提供对象或绑定）

```el
let patch = resolveSettingsPatch(SettingsSnapshot(), @[], @[], @[])
```
