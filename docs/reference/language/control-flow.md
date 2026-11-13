# Control flow

## Conditional forms

`if condition { consequent } else { alternative }` is an expression. Its value is the selected block's value; without `else`, an unselected path yields `void`. Conditions may omit grouping parentheses. `switch (value) { case pattern => expression; default => expression }` evaluates the selector once and does not fall through.

## Loops

| Form | Behavior |
|---|---|
| `while condition { body }` | Tests before each iteration. |
| `do { body } while (condition)` | Tests after the body, which therefore runs at least once. |
| `for (init; condition; step) body` | C-style counted loop; parentheses are required. |
| `for (let item in iterable) body` | Iterates values; this header may omit parentheses. |

Loops produce the last executed statement value; zero iterations produce `void`. A labeled `break` exits its target loop or block. A labeled `continue` targets a loop. In a C-style loop, `continue` performs cleanup and then the step before retesting.

## Transfers and labels

`return` exits a function; without an explicit return, the function body returns its final executed statement value. `throw` transfers control to exception handling. Labels occupy a separate target namespace and cannot cross function boundaries. `goto` is restricted to valid region entries and must preserve initialization and cleanup obligations.

## Related entries

- [Expressions and operators](expressions.md)
- [Functions](functions.md)
- [Syntax standard §12.7 and §12.10](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md)
- [Range loops and iterators](https://github.com/steve02081504/el/blob/master/docs/spec/17-range-loops-and-iterators.md)
