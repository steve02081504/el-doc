# 异常、效果与并发

## 异常

`throw` 抛出异常。`try`、`catch` 与 `finally` 分别用于保护、处理和清理；离开保护区域时执行清理。返回、循环跳转等控制退出也遵守统一清理次序。构造器、析构器和异步清理失败按执行模型中的异常合同处理。

## 效果与求值顺序

效果描述可观察行为，约束表达式求值、重排和调用。`@effects(...)` 声明效果族，序列约束使用相应的族协议。这些标注是受检查的合同，不是注释，也不代表所有目标后端均已具备实现。

## 任务与等待

`spawn(() => expression)` 显式启动独立任务并返回 Promise；`.get()` 等待结果。普通异步调用在语言合同要求的位置自动等待。`async { ... }` 与 `await(p)` 是标准库宏，不是关键字。

跨任务共享状态需要对应的转移或线程安全合同；任务边界不会自动使可变数据安全。取消与进程生命周期也有明确语义。

## 相关条目

- [函数](functions.md)
- [控制流](control-flow.md)
- [执行模型规范](https://github.com/steve02081504/el/blob/master/docs/spec/07-execution-model.md)
- [核心语义规范](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [属性合同](https://github.com/steve02081504/el/blob/master/docs/spec/attribute-contracts.md)
