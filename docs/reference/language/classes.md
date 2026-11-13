# Classes, objects, and lifecycle

## Class declarations

Every user type declares assignment semantics explicitly:

```el
@assign(mode: "copy")
class Point {
	let x = 0
	constructor(x: Number) { this.x = x }
}
```

Use `@assign(mode: "shared")` for shared assignment. Classes can define fields, methods, constructors, destructors, and operators; inheritance uses `extends`, while interfaces are structurally satisfied unless an `implements` assertion is written. Fields normally acquire a fixed type during construction. Dynamic classes use `@dynamic` and have separate field creation and deletion operations.

## Construction and dispatch

Named classes are constructed by calling the class name. Constructors are explicit by default; `implicit constructor` makes eligible conversions candidates without changing constructor identity. Virtual methods are marked `virtual`, and overrides must say `override`. Operator overloads can be declared inside a class or as eligible class-external functions.

## Destruction and cleanup

Destruction policy is selected on the class declaration with `@destruct(mode: "scope")` or `@destruct(mode: "aggressive")`; the default is aggressive. The concrete runtime class's own setting controls destruction. Destructors may participate in cleanup and can fail or be asynchronous under the lifecycle contract; exits and control transfers must honor cleanup.

## Boundaries

The assignment attribute is mandatory. A const access path constrains writes through that path but does not freeze all aliases. Construction failure and partially initialized object cleanup have their own rules; see the object specification.

## Related entries

- [Types](types.md)
- [Declarations and bindings](declarations.md)
- [Objects and types](https://github.com/steve02081504/el/blob/master/docs/spec/05-objects-and-types.md)
- [Functions and lifetimes](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)
- [Syntax standard §12.4.3](https://github.com/steve02081504/el/blob/master/docs/spec/12-syntax.md#1243-类与接口)
