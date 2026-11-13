# Declarations and bindings

## Variable bindings

| Declaration | Contract |
|---|---|
| `let count = 0` | Mutable binding; it may be assigned another value and, absent a restricting annotation, another type version. |
| `let count: Number = 0` | The annotation is an upper bound. Assignments must remain within it; local value versions may refine or widen within that bound. |
| `const limit = 10` | Immutable binding slot with a required initializer. Reassignment and writes through a const access path that violate the const contract are undefined behavior. |
| `lazy let value = expression` | Runtime initialization occurs once on first read; this does not request compile-time evaluation. |

Same-scope duplicate declarations are binding errors. Inner scopes may shadow outer bindings. An annotation on a local `let` differs from annotations on parameters, fields, and container elements, which retain their declared constraints rather than flow-sensitive refinement.

## Destructuring

Object and array destructuring initializes independent bindings from one source evaluation. The syntax supports renaming, defaults, rest entries, nesting, and array skips. Initialization proceeds left to right; each extracted value follows its type's copy or shared assignment protocol.

## Attributes and exports

Attributes precede declarations and use `@name(...)`; attribute contracts are fixed protocols, not arbitrary metadata. Export declarations expose selected names. `export lazy let` exports a runtime-lazy binding. Class assignment and destruction attributes are covered in [Classes and lifecycle](classes.md).

## Boundaries

`const` does not mean global deep immutability: other legal aliases are governed by their own access paths and sharing contracts. `lazy` does not promise that the first read succeeds; initialization failures and import-time behavior have separate rules.

## Related entries

- [Types](types.md)
- [Functions](functions.md)
- [Syntax standard §12.4.1](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#1241-变量)
- [Core semantics §3.1](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md#31-绑定与闭包)
- [Deferred bindings and imports](https://github.com/steve02081504/el/blob/master/docs/spec/deferred-bindings-and-imports.md)
