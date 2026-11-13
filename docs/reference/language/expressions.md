# Expressions and operators

## Expression forms

Expressions include literals, names, calls, member and index access, construction, lambdas, conditional expressions, and operator applications. Blocks and control constructs also produce values. The final executed statement supplies a block's value; an empty block yields `void`.

## Operators

| Operator family | Notation and notes |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/`, `%`; exponentiation is `^`. |
| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`. |
| Logic | `!`, `&`, `|`; `&&` and `||` are not EL operators. |
| Assignment | `=`, compound assignment, and prefix/postfix updates as defined by the grammar. |
| Range | `a..b` and `a..|b` denote the range forms used by iteration. |
| Conditional | `if ... { ... } else { ... }`; there is no `?:` operator. |

The grammar specifies precedence and associativity. Operators may be overloaded through class or eligible class-external declarations. Overload selection uses applicability; import order does not grant a candidate priority.

## Evaluation and results

Operands are evaluated under the language's sequencing and effect rules. Some expression contexts permit implementation freedom only where the specification says so. `&` and `|` have type-sensitive contracts and must not be assumed to be boolean short-circuit operators in every context. Calls can await asynchronous results automatically; explicit task creation is described in [Effects and concurrency](execution.md).

## Boundaries

EL does not use C-style `&&`, `||`, `**`, or ternary `?:`. The token `=` is assignment, while `==` is comparison. A type's overload declarations determine custom operator behavior; the spelling alone does not promise a built-in numeric operation.

## Related entries

- [Control flow](control-flow.md)
- [Types](types.md)
- [Syntax standard §12.6](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#126-表达式)
- [Core semantics §3.3 and §3.11](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md)
