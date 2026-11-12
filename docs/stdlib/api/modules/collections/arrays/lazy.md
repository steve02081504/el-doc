# collections/arrays/lazy.el

本页由源码注释生成；示例未运行验证。

## 惰性数组字面量语法 {#api-c2573eed21092f759bde}

源码：`src/stdlib/collections/arrays/lazy.el:1` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/lazy.el#L1)

将 lazy @[...] 字面量展开为按需产生元素的 Sequence。

## lazy {#api-864acf7ffaa705bfbfc8}

源码：`src/stdlib/collections/arrays/lazy.el:29` · [在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/collections/arrays/lazy.el#L29)

```el
export syntax lazy
```

将数组形状的代码块转为惰性 Sequence；元素表达式在迭代请求时才求值。

### 示例：延迟构造并只消费前两项

```el
let numbers = lazy @[1, 2, 3, 4]
console.stdout.writeLine(numbers.take(2).collect().join(", "))
```
