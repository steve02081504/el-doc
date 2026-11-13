# Functions

## Declarations and lambdas

```el
fn add(left: Number, right: Number) { left + right }
let increment = (value) => value + 1
```

Named declarations use `fn name(parameters) { ... }` or the expression body form `fn name(parameters) => expression`. Anonymous functions use `fn(parameters) ...`; arrow lambdas use `(parameters) => ...`. Return types may be inferred or written explicitly. Parameters can have type annotations and supported binding modifiers such as `take`.

## Return values and capture

Absent explicit `return`, the last executed statement is the result. `return void` explicitly returns no value; `return nil` returns the false-like nil value. Lambdas capture lexical bindings according to the capture and lifetime rules. Returning or retaining a closure is subject to those same lifetime and ownership contracts.

`return value from outerFunction` is a directed return to an enclosing function boundary where permitted; it is distinct from an ordinary return. Function AST values may be read and copied, but editing requires an editable copy followed by explicit compilation and checks.

## Asynchrony

There are no `async` or `await` keywords. Asynchronous behavior is inferred from effects; ordinary calls automatically wait where the contract requires. `spawn` explicitly starts an independent task and returns a Promise; waiting uses its `.get()` operation. The standard library's `async { ... }` and `await(p)` are macros, not language keywords.

## Related entries

- [Control flow](control-flow.md)
- [Effects and concurrency](execution.md)
- [Syntax standard §12.4.2](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#1242-函数)
- [Functions and lifetimes](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)
