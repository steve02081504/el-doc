# Lexical elements and literals

## Source form

EL source uses UTF-8. Whitespace separates tokens where needed; line and block comments are discarded before parsing. File preprocessing occurs before ordinary lexical analysis and is specified separately.

| Form | Summary |
|---|---|
| Identifier | Identifier spelling and contextual keyword rules are defined in §12.2.3. |
| Integer and real | Numeric tokens support the radix and exponent forms in §12.2.4; numeric meaning is supplied by the number model and literal providers. |
| String | Quoted strings support the escapes and interpolation boundaries in §12.2.5. |
| Array | `@[first, second]` |
| Matrix | `@(1, 2; 3, 4)` |
| Object | `@{ name: "value" }` |
| Regular expression | `/pattern/` is a literal form with its own delimiters and escape rules. |

Object literal shorthand `@{ name }` uses the in-scope `name` as both key and value. Explicit string keys use a colon and value. Literal expansion and provider behavior are described by the syntax and literal contracts.

## Separators and comments

Newlines and semicolons can terminate statements in the contexts specified by the grammar. A semicolon is not interchangeable with a comma: commas separate parameters, arguments, and literal entries. Comments do not nest unless the lexical specification explicitly permits it.

## Boundaries

Preprocessing directives such as `#include` and conditional directives are handled before normal tokenization; they are not ordinary expression syntax. Whether a literal is accepted and what type it denotes can depend on an available provider. The syntax alone does not establish that a backend or provider implements every form.

## Related entries

- [Expressions and operators](expressions.md)
- [Declarations and bindings](declarations.md)
- [Syntax standard §12.2](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#122-词法)
- [Numbers](https://github.com/steve02081504/el/blob/master/docs/spec/04-numbers.md)
- [Preprocessing](https://github.com/steve02081504/el/blob/master/docs/spec/preprocessing.md)
