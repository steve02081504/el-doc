# 声明与绑定

## 变量绑定

| 声明 | 合同 |
|---|---|
| `let count = 0` | 可写绑定，可赋新值；无注解时值版本可改变类型。 |
| `let count: Number = 0` | 注解是上界；局部值版本可在上界内细化或加宽，不能越界赋值。 |
| `const limit = 10` | 不可重绑，必须初始化；违规写入属于未定义行为。 |
| `lazy let value = expression` | 运行期首次读取时初始化一次，不表示编译期求值。 |

同一作用域内重复声明是绑定错误，内层作用域可以遮蔽外层名字。局部 `let` 的上界内流敏感细化不推广到函数参数、字段或容器元素注解。

## 解构、属性与导出

对象和数组解构从源表达式中按从左到右的顺序初始化独立绑定，源表达式只求值一次。语法支持重命名、默认值、剩余项、嵌套和数组跳项；各值遵循其类型的复制或共享协议。

默认值的触发条件、剩余容器与来源的关系，以及循环中的用法见[解构绑定](destructuring.md)。

属性写在声明之前，使用 `@name(...)`，其参数形状由固定属性协议定义。`export` 使顶层声明可被其他模块导入；`export lazy let` 导出运行期惰性绑定。

`const` 限制经该绑定访问的写操作，不等于对所有别名做全局深冻结。`lazy` 是运行期绑定初始化机制，不会免除初始化异常或模块语义。

## 相关条目

- [类型](types.md)
- [函数](functions.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [核心语义](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [惰性绑定与导入](https://github.com/steve02081504/el/blob/master/docs/spec/deferred-bindings-and-imports.md)
