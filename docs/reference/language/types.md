# Types

## Type expressions

Type annotations use `name: Type`. Function types, generic arguments, unions, intersections, tuples, and type queries have grammar-defined forms. Generic arguments use named parameters; the name may be omitted only for a single argument when it supplies the declaration's first type parameter, as in `Array<Point>`.

```el
let point: Point = origin
let maybeText: Text | void_t = void
```

The examples show notation only. `|` in a type expression denotes a union; its expression-level meaning depends on operand types and context.

## Inference and constraints

An omitted annotation is inferred from the initializer and later use. For a local `let`, an explicit annotation is an upper bound, permitting value-version refinement or widening within that bound. Parameters, fields, and container element annotations do not use that local flow-sensitive rule. A fixed-width or fixed-length bound cannot be crossed by runtime widening.

EL uses `Number` and its type parameters for ordinary numeric constraints; machine integer representations are explicit low-level boundaries, not ordinary language types. See [numeric types](../../language/numeric-types.md).

## Runtime values and special types

`any` permits dynamically typed storage under its contract. `t_t`, `nil_t`, and `void_t` are ordinary source-defined types available through the standard environment, not compiler-intrinsic classes. `nil` and `void` are distinct values; a missing result is not automatically false.

## Related entries

- [Declarations and bindings](declarations.md)
- [Expressions and operators](expressions.md)
- [Syntax standard §12.5](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#125-类型)
- [Core semantics §3.2 and §3.4–3.8](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
- [Numbers](https://github.com/steve02081504/el/blob/master/docs/spec/04-numbers.md)
