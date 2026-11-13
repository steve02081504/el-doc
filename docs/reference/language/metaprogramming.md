# Macros and metaprogramming

## Source macros

Macros operate during compilation and expand syntax or provide compile-time forms under their declared contracts. Macro imports, aliases, and shadowing follow ordinary name binding. A macro name is not automatically a keyword: `async`, `await`, and `typeof` are standard macros rather than reserved language words.

## Literal and syntax expansion

Literal providers may define how supported literal forms become values. Syntax-oriented facilities operate on syntax objects and must preserve binding identity and control targets where required. File preprocessing is a separate earlier phase; it handles directives before lexical analysis and is not a source macro.

## Function AST operations

An existing function AST can be read and copied but not mutated in place. The editing flow is to copy into an editable AST, make changes, check names/types/scopes/lifetimes, explicitly compile, and use the resulting function value. New captures must be supplied explicitly; they are not discovered by searching the expansion site.

## Boundaries

Macro expansion does not waive type, effect, lifetime, or control-flow checks. Text-based generation is not equivalent to arbitrary runtime evaluation. The specification describes contracts; it does not imply that every metaprogramming API is implemented in every compiler path.

## Related entries

- [Lexical elements](lexical.md)
- [Expressions and operators](expressions.md)
- [Preprocessing tutorial](../../language/preprocessing.md)
- [Syntax standard §12.14](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#1214-字面量展开)
- [Core semantics §3.1](https://github.com/steve02081504/el/blob/master/docs/spec/03-core-semantics.md#31-绑定与闭包)
- [Preprocessing specification](https://github.com/steve02081504/el/blob/master/docs/spec/preprocessing.md)
