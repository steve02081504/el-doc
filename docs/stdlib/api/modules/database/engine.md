# database/engine.el

本页由源码注释生成；示例未运行验证。

[库分类](../../categories/database.md) · [模块索引](../../modules.md) · [符号索引](../../symbols.md)

## database/engine {#api-ad83373421b22cbf7008}

源码：`src/stdlib/database/engine.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/engine.el#L1)

提供持久数据库引擎的打开入口、引擎选项及事务/读取会话管理。
示例：`let db = openDatabase(Path("/data/app"), DbEngineOptions())`；普通打开会遵守恢复围栏并使用目录中的持久状态。

## DbEngineOptions {#api-a519c385d5e1dcf7f447}

源码：`src/stdlib/database/engine.el:46` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/engine.el#L46)

配置数据库目录、存储与日志、节点/目录标识、扫描边界、复制身份及显式恢复行为。
可选的 `journal` 是借用的持久事务日志；引擎不会关闭它。`restore_resume` 仅供显式恢复入口使用，普通打开仍拒绝带恢复围栏的目录。

```el-signature
export class DbEngineOptions
```

**参数**：changes 要覆盖的选项字段；未指定字段使用默认值。

### 示例：设置节点身份并打开目录

```el
let options = DbEngineOptions(@{ node: "node-a" })
let db = openDatabase(Path("/var/lib/app"), options)
```

## openDatabase {#api-e5ea93b339773da61f63}

源码：`src/stdlib/database/engine.el:1212` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/database/engine.el#L1212)

打开指定原生路径的数据库目录并构造引擎；目录及持久状态由引擎使用，已存在的不完整恢复目标会按选项拒绝。

```el-signature
export fn openDatabase(directory: Path, options: DbEngineOptions = DbEngineOptions()): DatabaseEngine
```

**返回类型**：[`DatabaseEngine`](../../types.md#api-108a100299f4ad577de0)

**参数**：directory 数据库目录路径。

**参数**：options 引擎选项；默认使用 `DbEngineOptions()`。

**返回值**：已打开的数据库引擎，调用方应在会话结束后关闭它。

### 示例：打开默认配置的数据库

```el
let db = openDatabase(Path("/var/lib/app"))
```
