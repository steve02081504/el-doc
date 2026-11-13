# Exceptions, effects, and concurrency

## Exceptions

`throw` raises an exception. `try` with `catch` handles matching failures; `finally` runs cleanup on exits from the protected region. Cleanup ordering applies to returns, loop transfers, and other control exits as well. Constructor, destructor, and asynchronous cleanup failures follow the execution and object lifecycle contracts.

## Effects

Effects describe observable behavior and constrain when expressions may be evaluated or reordered. Effect families are declared through the language's attribute protocols, such as `@effects(...)`; sequencing constraints use the corresponding sequence-family contracts. These declarations are checked contracts, not comments and not a guarantee that every planned backend facility is implemented.

## Tasks and waiting

`spawn(() => expression)` starts an independent task and yields a Promise. `.get()` waits for its result. Ordinary asynchronous calls may wait automatically; explicit concurrency uses `spawn`. The library macros `async { ... }` and `await(p)` do not add keywords to the language.

Sharing state across tasks requires the relevant transfer or thread-safety contract. A task boundary does not make mutable data safe to share automatically. Cancellation and process lifetime also have specified behavior.

## Related entries

- [Functions](functions.md)
- [Control flow](control-flow.md)
- [Execution model §7.1, §7.4, §7.6, §7.8](https://github.com/steve02081504/el/blob/master/docs/spec/07-execution-model.md)
- [Core semantics §3.10](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md#310-并行与内存序)
- [Attribute contracts](https://github.com/steve02081504/el/blob/master/docs/spec/attribute-contracts.md)
