# 类与对象

`class` 用来定义有身份、有字段、有方法的具名类型；对象字面量用来快速造一个匿名的轻量对象。这一页讲清类的声明、复制与共享、继承和分派，以及动态字段与构造析构的职责。

## 声明一个类

```el
@assign(mode: "copy")
class Point {
	let x: Number = 0
	let y: Number = 0

	constructor(x: Number = 0, y: Number = 0) {
		init this
		this.x = x
		this.y = y
	}

	fn squaredLength(): Number => x * x + y * y
	fn describe(): Text => `(${Text(x)}, ${Text(y)})`
}

let p = Point(3, 4)

console.stdout.writeLine(p.squaredLength())   // 25
console.stdout.writeLine(p.describe())        // (3, 4)
```

- 每个具名类都必须在声明前写 `@assign(mode: "copy")` 或 `@assign(mode: "shared")`，明确普通赋值是复制还是共享；没有默认值，缺了会被拒绝。
- 字段用 `let` 或 `const` 在类体里声明；`init this` 执行尚未初始化字段的声明初值，构造器随后给字段赋值。
- 字段在构造时赋值之后类型固定，只有显式声明为 `any` 的字段例外；固定类型不表示固定值，同类型的后续赋值仍然允许。
- 每条正常构造出口都必须能证明所有字段已初始化；构造器里的裸 `return` 是提前完成构造，不允许返回替代值。
- 实例用 `Point(3, 4)` 创建，不用 `new`。
- 方法声明与普通函数相同；读字段、调用同类方法时可以省略 `this.`，参数或局部变量与字段同名时会给出定位警告，显式写 `this.x` 消歧。

## copy 与 shared

```el
let a = Point(1, 2)
let b = a
b.x = 9

console.stdout.writeLine(a.x)   // 1：copy 类型，b 是独立对象
```

```el
@assign(mode: "shared")
class Counter {
	let #count: Number = 0

	constructor(start: Number = 0) {
		init this
		this.#count = start
	}

	fn increment() {
		this.#count += 1
		this.#count
	}

	fn value(): Number => this.#count
}

let c1 = Counter(0)
let c2 = c1
c2.increment()

console.stdout.writeLine(c1.value())   // 1：shared，两个名字指向同一对象
```

- copy 类型的赋值产生独立对象，具体复制深度由该类型的复制构造决定，不承诺默认深拷贝。
- shared 类型赋值复制引用；所有使用者都不再需要时才析构一次。
- 两种模式同样作用于普通参数传递与返回值；显式 `take` 仍按接管协议处理。

## 私有成员

```el
@assign(mode: "shared")
class Account {
	let #balance: Number = 0

	fn deposit(amount: Number) {
		this.#balance += amount
	}

	fn balance(): Number => this.#balance
}

let account = Account()
account.deposit(50)
console.stdout.writeLine(account.balance())   // 50
// account.#balance                           // 编译错误：声明类之外不能访问
```

- 成员默认公开；以 `#` 开头的字段、方法和访问器是私有成员，只有声明它的类内部可以访问。
- 子类不能访问父类的私有槽；同名私有成员按声明类区分，公开 `x` 与私有 `#x` 可以共存。
- `account["#balance"]` 是普通的动态字符串键访问，不访问私有槽。

## 继承、virtual 与 override

```el
@assign(mode: "copy")
class Shape {
	virtual fn area(): Number => 0
}

@assign(mode: "copy")
class Square extends Shape {
	let side: Number = 3

	override fn area(): Number => side * side
}

let shape: Shape = Square()
console.stdout.writeLine(shape.area())   // 9：virtual 按实际对象分派
```

- 继承写 `class Child extends Parent { ... }`；多继承用逗号列出多个基类，菱形默认保留独立的基类子对象。
- 方法默认是静态分派：没有 `virtual` 时按静态接收者类型选实现，派生类的同名方法不会自动变成虚调用。
- 覆盖虚方法必须写 `override`；参数列表必须与基声明逐参数相同，返回类型可以是基声明返回类型的名义子类。
- 构造共享基类用 `super<Base>(args)`；只有一个直接基类时可以写 `super(args)`。
- 接口是编译期结构匹配：成员形状与效果合同符合就满足，不要求显式写 `implements`。

静态分派的反例：

```el
@assign(mode: "copy")
class A {
	fn name(): Text => "A"
}

@assign(mode: "copy")
class B extends A {
	fn name(): Text => "B"
}

let a: A = B()
console.stdout.writeLine(a.name())   // A：没有 virtual，按静态接收者分派
```

## 运算符重载

运算符写在类内，用 `operator` 加符号声明，函数体用块：

```el
@assign(mode: "copy")
class Vec2 {
	let x: Number = 0
	let y: Number = 0

	constructor(x: Number = 0, y: Number = 0) {
		init this
		this.x = x
		this.y = y
	}

	operator +(rhs: Vec2): Vec2 {
		return Vec2(x + rhs.x, y + rhs.y)
	}

	operator ==(rhs: Vec2): Bool {
		return (x == rhs.x) & (y == rhs.y)
	}
}

let sum = Vec2(1, 2) + Vec2(3, 4)

console.stdout.writeLine(sum.x)                // 4
console.log.value(Vec2(1, 2) == Vec2(1, 2))    // t
```

- 类内运算符声明成成员，左侧接收者是 `this`，第一个参数是右侧操作数。
- `operator +`、`operator -`、`operator *`、`operator /`、`operator ^`、`operator ==`、`operator <` 等都可以重载；`===`/`!==` 的对象身份比较与 `is`/`isnot` 的类型判断不被重载改变。
- 运算符也可以在类外声明，第一个参数显式接收左操作数；候选按普通重载规则选择。
- `&`/`|` 的显式值重载会让源码短路变成普通 eager 调用，两侧都求值；分派细节按语言规范第 3 章核对。
- 完整的声明形式、转换与候选规则见[运算符与表达式](operators.md#operator-overloading)。

## `@dynamic` 与动态字段

```el
@assign(mode: "shared")
@dynamic
class Bag {
	let label: Text = ""
}

let bag = Bag()
new bag.weight = 3
new bag.note: Text = "fragile"

console.stdout.writeLine(bag.weight)   // 3
let removed = delete bag.weight
console.log.value(removed)             // t

// bag.weight                          // 运行时错误：字段不存在
// delete bag.label                    // 编译错误：声明字段不可删除
```

- 只有 `@dynamic` 类允许运行时增删字段；普通类新增或删除字段被拒绝。
- 动态字段只能用 `new` 创建；给缺失字段直接赋值会报错。
- `new record.field: any = 1` 可以显式指定字段类型，省略时按首个赋值的值推断。
- `delete` 返回 `Bool`：删除成功是 `t`，字段不存在是 `nil`；它只移除字段引用，不等于释放外部资源。
- `@dynamic` 类自己声明的字段仍有固定布局，不能删除。

## 类实例与对象字面量

```el
let p = Point(1, 2)                    // 具名类实例
let o = @{ name: "Ada", age: 36 }      // 匿名对象字面量

let q = o
q.age = 37

console.stdout.writeLine(o.age)        // 37：字面量默认 shared
// o.city = "London"                   // 编译错误：闭合对象没有这个字段
```

两者的区别：

- `Point(1, 2)` 是声明的类实例，拥有类的方法、继承关系与显式配置的 `@assign` 模式。
- `@{ name: "Ada" }` 创建匿名、封闭类的实例：默认 shared，有可观察身份，声明字段可写，但没有方法、没有继承，字段集合固定不能增删。
- 字面量内重复键是编译错误；裸标识符字段 `@{ name }` 等价于 `name: name`。
- 需要开放键表时使用 `@dynamic` 类，或标准库函数 `dynamicObject(source)` 创建动态对象的浅快照。

## 构造与析构的职责

```el
@assign(mode: "shared")
@destruct(mode: "scope")
class Session {
	let #id: Text = ""

	constructor(id: Text) {
		init this
		this.#id = id
	}

	fn id(): Text => this.#id

	destructor() {
		// 清理仍然持有的资源；已关闭的资源不能重复释放
	}
}
```

- 构造器必须自己完成全部正常出口的字段与基类初始化义务；部分构造失败时，按逆序清理已经成功完成的部分，不执行未完成整体的析构。
- 析构函数用 `destructor()` 声明，本身不带属性；析构策略标在类声明上，写作 `@destruct(mode: "scope")` 或 `@destruct(mode: "aggressive")`。
- 不写 `@destruct` 时默认是 aggressive：不再使用时就析构；`scope` 会等到名称作用域结束。
- 析构策略取实际具体类自己的声明，不沿继承链继承；派生类没有标注时仍按 aggressive。
- 外部资源（文件、连接、锁）必须有显式关闭方式，不能把自动回收当作确定性关闭。
- 禁止复活正在析构的对象，也不能把它的引用保存到析构过程之外继续使用。
- 没有自定义析构时，默认析构按构造逆序清理成员与基类；自定义析构主体不取消应执行的成员清理。

## 继续阅读

- [值与类型](values.md)：字段类型、`any` 与复制/共享背后的值规则。
- [生命周期与析构](lifetimes.md)：构造与析构的时机、`@destruct` 策略与借用来源。
- [内存布局与 GC 钩子](memory-layout.md)：字段偏移、`@layout` 与 `@builtin:vome:on:collect`。
- [函数与闭包](functions.md)：方法之外的普通函数、lambda 与默认参数。
- [错误处理与异步](errors-async.md)：构造与析构中的异常、任务与清理。
