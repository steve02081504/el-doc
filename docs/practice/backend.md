# 实战：搭建本机 HTTP 服务

> 在两个终端发出相同的 HTTP 请求。第一次返回 `v1`，第二次返回 `v2`，两次请求使用同一个监听器。

!!! abstract "🎯 做完这页，你能"
    - 用 EL 接受浏览器或 curl 发来的 HTTP 请求
    - 写出注册、登录、会话验证与数据库的接口合同
    - 核对监听器存活时处理器替换对新请求和在途请求的影响

    <span class="el-chip">⏱ 约 40 分钟</span> <span class="el-chip">前置：[文件与网络](../stdlib/files-network.md)</span>

!!! note "实现状态"
    下方例子使用 TCP 监听和现有 HTTP 行读取器，尚未编译或运行。公共 HTTP 服务端与运行时应用模块热更新仍待接通。这里的闭包替换演示同一进程的路由切换。

## 先让 HTTP 客户端收到响应

把完整程序保存为 `server.el`。它只接受回环请求、只处理 `GET /health`、每次响应后关闭该连接。读完两个连接后退出。读取请求头有整块长度和超时预算，例子不将请求正文交给业务代码。

```el
import { listenTcp } from "el:network/"
import { encodeUtf8 } from "el:network/bytes.el"
import { HttpWireReader } from "el:network/http/wire.el"

fn response(status: Text, body: Text): Number[] {
	let payload = encodeUtf8(body)
	return encodeUtf8("HTTP/1.1 " + status + "\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + Text(payload.count) + "\r\nConnection: close\r\n\r\n" + body)
}

let listener = listenTcp("127.0.0.1", 8765)
let health: fn(): Text = fn(): Text { return "v1\n" }
try {
	console.stdout.writeLine("http://127.0.0.1:8765/health")
	for (let request = 0; request < 2; request++) {
		let connection = listener.accept()
		try {
			let reader = HttpWireReader(connection, 3000)
			let remaining = 8192
			let requestLine = reader.line(remaining)
			remaining -= Number(requestLine.count) + 2
			while (t) {
				let line = reader.line(remaining)
				remaining -= Number(line.count) + 2
				if (line == "") break
			}
			let current = health
			if (requestLine == "GET /health HTTP/1.1" | requestLine == "GET /health HTTP/1.0") {
				connection.send(response("200 OK", current()))
			} else connection.send(response("404 Not Found", "unknown route\n"))
			health = fn(): Text { return "v2\n" }
		} finally {
			connection.close()
		}
	}
} finally {
	listener.close()
}
```

在第一扇终端运行 `el run server.el`。看到地址后，在第二扇终端连续运行下面两次。Windows PowerShell 可用 `curl.exe`。

```sh
curl -i http://127.0.0.1:8765/health
curl -i http://127.0.0.1:8765/health
```

两次状态都是 `200 OK`，正文分别为 `v1` 和 `v2`。若先打开浏览器，它可能额外请求站点图标，占用本例的第二个连接。验收顺序用 curl 固定。

## 再给账户操作划清事务边界

| 路由 | 读写与验证 | 核对响应 |
| --- | --- | --- |
| `POST /register` | 校验用户名，生成随机盐，保存密码派生结果及参数。在事务内检查唯一用户名并插入 | 新用户返回 201；重复用户名返回 409 |
| `POST /login` | 按用户名取盐和派生参数，重新计算并用常数时间比较。通过后保存新的随机会话凭据摘要和过期时间 | 正确凭据返回 200 并设置会话 Cookie；错误凭据返回通用 401 |
| `GET /me` | 读取 Cookie、匹配会话摘要，检查用户、过期时间和撤销状态，再读取账户资料 | 有效会话返回 200；缺失、过期或撤销返回 401 |
| `POST /logout` | 使服务端会话失效，并清除 Cookie | 退出后拿旧 Cookie 访问 `/me` 得到 401 |

按“用户名 → 盐、算法参数和密码派生结果”“会话摘要 → 用户名、过期时间和撤销状态”建两张表。仓库里的 [数据库重开夹具](https://github.com/steve02081504/el/blob/master/tests/database/integration/open-insert-query.el) 示范 `openDatabase`、`DbTableDefinition`、`table.get` 以及关闭后重开检查。用户名可以直接作为主键。`put` 走插入路径。事务在主键上加排他锁并拒绝重复行。处理冲突时区分已确认提交、重复主键和提交结果未知，避免把未确认的请求当注册成功。

标准库导出 `pbkdf2_sha256`、`secure_random_bytes` 和 `constant_time_equal`。为密码派生保存每人的随机盐、算法版本、迭代数和摘要长度，按部署环境校准代价。拒绝登录日志中的密码、Cookie 和原始会话令牌。浏览器接真实账户前要使用 HTTPS、`Secure` 与 `HttpOnly` Cookie，按站点交互设计 `SameSite` 和跨站请求防护，并限制登录尝试。正文接入受限的 HTTP 服务端，统一处理消息定界、内容类型和连接超时。

## 先在本地验证密码派生和数据库重开

在空目录保存 `account-store.el`，运行 `el run account-store.el`。下面的完整程序只使用教学口令，首次运行创建账户，再关闭数据库并重新打开验证。再次练习时另选空目录，以免重复创建同一张表。迭代数 1000 仅供这个可快速执行的夹具使用。

```el
import { Path, make_directories } from "el:operating-system/paths/"
import { DbEngineOptions, openDatabase, DbColumnDefinition, DbTableDefinition, dbTextType, dbNumberType, DbRow } from "el:database/"
import { secure_random_bytes, text_bytes, pbkdf2_sha256, hex_of, hex_bytes, constant_time_equal } from "el:cryptography/"

let path = make_directories(Path("accounts-demo"))
let options = DbEngineOptions(@{node: "account-demo"})
let first = openDatabase(path, options)
try {
	let users = first.createTable(DbTableDefinition("users", @[
		DbColumnDefinition("name", dbTextType()),
		DbColumnDefinition("salt", dbTextType()),
		DbColumnDefinition("iterations", dbNumberType()),
		DbColumnDefinition("derived", dbTextType())
	], @["name"]))
	let salt = secure_random_bytes(16)
	let iterations = 1000
	let derived = pbkdf2_sha256(text_bytes("practice-only"), salt, iterations, 32)
	let receipt = users.put(@["demo", hex_of(salt), iterations, hex_of(derived)])
	if (!receipt.confirmed()) throw "注册提交没有确认"
} finally {
	first.close()
}

let reopened = openDatabase(path, options)
try {
	let users = reopened.table("users")
	let account = users.get(@["demo"])
	if (account isnot DbRow) throw "重开后没有找到账户"

	let salt = hex_bytes(Text(account.value(users.schema.findColumn("salt"))))
	let iterations = Number(account.value(users.schema.findColumn("iterations")))
	let expected = hex_bytes(Text(account.value(users.schema.findColumn("derived"))))
	let actual = pbkdf2_sha256(text_bytes("practice-only"), salt, iterations, expected.count)
	let wrong = pbkdf2_sha256(text_bytes("incorrect"), salt, iterations, expected.count)
	if (!constant_time_equal(actual, expected)) throw "正确口令应通过"
	if (constant_time_equal(wrong, expected)) throw "错误口令应拒绝"
	console.stdout.writeLine("重开后正确口令通过，错误口令拒绝")
} finally {
	reopened.close()
}
```

接到路由时，注册分支返回提交结果，登录分支通过后再为会话表生成独立令牌。先在内存或临时数据库检查失效分支，再用 HTTP 客户端跑整条路径。

!!! example "验证竞争注册和重启"
    同时提交两个同名测试账户的注册。只能成功一次。重启后调用登录，成功账户的凭据仍有效，失败账户的凭据不能覆盖它。再撤销会话，确认同一 Cookie 只能得到 401。

## 把同进程切换换成语言的模块热更新

把监听器、数据库放在长期运行的宿主模块，把可修改的路由策略放进独立模块。在每次分发处经导入入口调用。保存下来的普通函数值会固定旧版本，像例子中的 `current` 一样。需要保留模块内状态时用双方都声明的同一 `@preserve` ID，并遵守类型与析构合同。[模块与导入](../reference/language/modules.md)

1. 让一个同步调用停在旧处理器内。记下监听端口和进程标识。
2. 发布接口兼容的候选版本，用同一地址发送新请求，预期得到新版本结果。
3. 放行旧调用，确认它完成旧版本响应。另单独测异步函数恢复后再次经动态入口调用的行为。
4. 发布不兼容候选。检查入口仍使用上一版本，并核对数据库里已提交的记录。候选初始化阶段避免向共享保留状态写入，如此才能让拒绝发布时同时保住入口和业务数据。

??? question "先猜：只用一对请求能证明在途请求按旧逻辑完成吗？"
    只能看到两次串行调用命中了不同处理器。需要给旧调用设置可控的暂停点和独立的新请求，才会覆盖真正的并发切换。

## 下一站：[联动的 EL GUI](shared-frontend.md)

让服务返回可核对的应用状态，再选择适合宿主的界面呈现方式。
