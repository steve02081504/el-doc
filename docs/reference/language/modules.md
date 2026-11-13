# Modules and imports

## Module identity and exports

An EL module is a source module with an identity determined by its resolved source. Exported names are visible to importers; module top-level code is allowed, so no `main` function is required. A dependency module is initialized once per process according to module initialization rules.

## Import forms

```el
import { run, helper as h } from "file:./tools.el"
import /^run/ from "file:./tools.el"
import /.*/ from "file:./tools.el"
import /.*/ as tools from "file:./tools.el"
```

Imports explicitly state which names are selected. The forms cover named imports, regex-selected imports, and compile-time namespace access. There is no `import *`, side-effect-only import, or runtime namespace value. Direct imported names follow updates; a saved function value retains the version it captured.

## Resolution and lazy forms

Source resolution, package configuration, caching, and hot-update policy are specified in the module contract. Lazy bindings initialize at runtime on first read. **Regex imports are deliberately not allowed to be lazy**; this is an intentional design restriction documented in [Deferred bindings and imports](https://github.com/steve02081504/el/blob/master/docs/spec/deferred-bindings-and-imports.md#惰性导入的有意限制). This reference preserves that restriction.

## Related entries

- [Declarations and bindings](declarations.md)
- [Module tutorial](../../language/modules.md)
- [Modules specification](https://github.com/steve02081504/el/blob/master/docs/spec/08-modules.md)
- [Deferred bindings and imports](https://github.com/steve02081504/el/blob/master/docs/spec/deferred-bindings-and-imports.md)
