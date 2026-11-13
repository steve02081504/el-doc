# 宏与元编程

## 源码宏

宏在编译期按其声明合同展开语法或提供编译期形式。宏名遵循名字绑定、导入、重命名与遮蔽规则，不会仅因名字而成为关键字。`async`、`await` 和 `typeof` 是标准环境提供的宏，不是核心关键字。

## 字面量与语法展开

字面量提供者可定义受支持字面量如何产生值。语法级机制操作语法对象，并在适用位置保留绑定身份与控制目标。文件预处理是更早的独立阶段，在词法分析前处理指令，不等同于源码宏。

## 函数 AST

已有函数 AST 可读取和复制，不可原地修改。编辑流程是复制为可编辑 AST、修改、检查名字/类型/作用域/生命周期，再显式编译成新函数值。新增捕获必须显式提供绑定；不会从生成位置搜索局部变量。

宏展开不免除类型、效果、生命周期或控制流检查。文本生成不等于任意运行期求值。规范说明合同，不据此推断所有元编程 API 已在每条编译器路径中实现。

## 相关条目

- [词法元素](lexical.md)
- [表达式与运算符](expressions.md)
- [文件预处理参考](preprocessing.md)
- [预处理教程](../../language/preprocessing.md)
- [语法标准](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [核心语义规范](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [预处理规范](https://github.com/steve02081504/el/blob/master/docs/spec/preprocessing.md)
