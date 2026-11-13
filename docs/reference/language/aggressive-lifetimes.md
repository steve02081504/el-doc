# 激进生命周期与析构时机

EL 默认不等变量离开作用域才清理对象：当对象的所有使用者都不再需要它时，默认的 `aggressive` 策略会在最后使用处析构。需要等名称作用域结束时，可以给具体类选择 `scope` 策略。

| 策略 | 对具名对象的影响 |
| --- | --- |
| 默认 `aggressive` | 没有剩余使用者时尽早析构，可能早于作用域结束 |
| `@destruct(mode: "scope")` | 至少等所属名称作用域结束，仍有使用者时还须继续保活 |

下列完整示例的输出按语言规范推导，尚未运行。`assign` 和 `destruct` 由默认预导入提供，通常无需为声明类单独导入。

## 从未使用的对象可以在声明后析构

```el
@assign(mode: "shared")
class Notice {
	destructor() { console.stdout.writeLine("析构") }
}

let notice = Notice()
console.stdout.writeLine("后续语句")
```

预期输出：

```text
析构
后续语句
```

`notice` 构造之后没有任何使用者需要它，因此析构可以紧接声明发生，不必等模块结束。析构是可观察的动作，不只是回收内存。

## 最后一次使用后，作用域可能还没结束

```el
@assign(mode: "shared")
class Notice {
	let value = 0
	fn use() {
		console.stdout.writeLine("使用")
		this.value = 1
	}
	destructor() { console.stdout.writeLine("析构，value = ", this.value) }
}

fn run() {
	let notice = Notice()
	notice.use()
	console.stdout.writeLine("仍在函数中")
}

run()
console.stdout.writeLine("函数已返回")
```

预期输出：

```text
使用
析构，value = 1
仍在函数中
函数已返回
```

`use` 先输出，再写入对象字段；析构读取的 `value` 因而是 `1`。完成这些实际使用后，没有其他持有者需要对象，下一条输出也不再使用它，所以可以先析构，再输出“仍在函数中”。名称还在作用域里，不代表对象必须一直活着。

## 改用 `scope` 会改变顺序

把上一个完整示例的类声明前增加一行 `@destruct(mode: "scope")`，其余代码不变：

```el
@destruct(mode: "scope")
@assign(mode: "shared")
class Notice {
	let value = 0
	fn use() {
		console.stdout.writeLine("使用")
		this.value = 1
	}
	destructor() { console.stdout.writeLine("析构，value = ", this.value) }
}

fn run() {
	let notice = Notice()
	notice.use()
	console.stdout.writeLine("仍在函数中")
}

run()
console.stdout.writeLine("函数已返回")
```

预期输出：

```text
使用
仍在函数中
析构，value = 1
函数已返回
```

这里 `notice` 的名称作用域在 `run` 退出时结束，所以析构不早于函数内的后一条输出。`scope` 是最低保留时间；如果其他使用者仍需要对象，也不能因作用域结束而提前析构。

## 判断最后使用要看所有持有者和借用

文本里一个名字最后出现，并不证明对象已经无人使用。共享引用可以由另一个绑定、返回值或逃逸闭包持有；仍会使用的借用也要求其来源保持有效。只有所有使用者都不再需要对象时，才可以析构；共享对象只析构一次。借用不会凭空延长来源的合法寿命，悬垂借用的使用属于未定义行为，详见[生命周期、借用与清理](lifetimes.md)。

当多个对象恰好在同一个析构点可以清理时，按相关绑定的声明逆序清理；这不是全程序统一的逆序规则。若较早声明的对象在更早的位置已无使用者，默认策略可以先清理它，而不用等后来声明但仍在使用的对象。共享对象的排序依据是最后释放它的绑定。

策略由对象的实际具体类决定，不沿继承链继承：派生类没有标注时采用默认 `aggressive`，即使基类选择了 `scope`；通过基类视图访问也不会改写实际具体类的策略。

## 常见误解

- “离开大括号才会析构”：默认策略可以在作用域内的最后使用处析构。
- “名字最后出现就是对象最后使用”：还要考虑其他持有者、实际借用和控制流。
- “输出语句里读取对象，析构一定在输出之后”：实参先求值，若该读取已是最后使用，对象可能在实参求值后、输出调用之前析构。要判断顺序，需要看实际求值和使用。
- “析构就代表内存立刻归还系统”：对象清理和存储回收是不同事件。

相关内容：[左值、右值与亡值](value-categories.md)、[赋值、复制与共享](assignment-semantics.md)、[类](classes.md)和[函数](functions.md)。

??? note "核对依据"
    [函数与生命周期规范：析构策略、最后使用与清理顺序](https://github.com/steve02081504/el/blob/master/docs/spec/06-functions-and-lifetimes.md)

    [析构时机测试用例：未使用的对象在后续输出前析构](https://github.com/steve02081504/el/blob/master/tests/cases-control-and-types.el)
