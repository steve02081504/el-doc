# logic/surface.el

本页由源码注释生成；示例未运行验证。

## 逻辑规则语法 {#api-8ed19a71b970b41fa647}

源码：`src/stdlib/logic/surface.el:22` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/surface.el#L22)

提供 rules 与 search 语法入口，将关系声明、逻辑变量和目标组合展开为普通 EL 逻辑库调用。

## rules {#api-bc0f4317802278bb03e0}

源码：`src/stdlib/logic/surface.el:1362` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/surface.el#L1362)

```el
export syntax rules
```

声明关系与规则的逻辑程序语法；关系体支持事实、规则、入口及逻辑目标。

### 示例：声明一个简单事实关系

```el
let people = rules { relation person(name) from @[@["Ada"]] }
```

## search {#api-ee82dd39cb36e9d1e6cc}

源码：`src/stdlib/logic/surface.el:1380` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/logic/surface.el#L1380)

```el
export syntax search
```

在逻辑程序中声明查询目标，并生成可枚举答案的搜索值。

### 示例：查询事实关系

```el
let people = rules { relation person(name) from @[@["Ada"]] }
let plan = search(limit: 100) {
    call people.relations.person(name)
    yield name as Text
}
```
