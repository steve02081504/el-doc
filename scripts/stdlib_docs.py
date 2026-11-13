"""Extract explicit EL documentation comments into portable data and Markdown.

No compiler, imports, macros or examples are executed. Run --help for usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
import tempfile
from urllib.parse import quote


SOURCE_URL = "https://github.com/steve02081504/el/blob/master/src/stdlib"
DECLARATIONS = {"fn", "class", "interface", "let", "const", "get", "set", "constructor", "destructor", "operator", "syntax", "enum", "data"}


class DocumentationError(ValueError):
	pass


def tokens(source):
	"""Yield (kind, text, start, end); keep literals opaque and comments distinct."""
	pattern = re.compile(r'\s+|//[^\n]*|/\*[\s\S]*?\*/|(?P<raw>#+)"|[\w]+|.', re.UNICODE)
	position = 0
	previous = ""
	while position < len(source):
		match = pattern.match(source, position)
		text = match.group()
		end = match.end()
		kind = "code"
		if source.startswith("/*", position) and not text.startswith("/*"):
			raise DocumentationError("unterminated block comment")
		if text.isspace():
			kind = "space"
		elif text.startswith("//"):
			kind = "doc" if text.startswith(("///", "//!")) and not source[source.rfind("\n", 0, position) + 1:position].strip() else "comment"
		elif text.startswith("/*"):
			kind = "comment"
		elif match.group("raw"):
			closing = '"' + match.group("raw")
			last = source.find(closing, end)
			if last < 0:
				raise DocumentationError("unterminated raw string")
			end = last + len(closing)
			kind = "literal"
		elif text in ('"', "'", "`"):
			end = quoted_end(source, position)
			kind = "literal"
		elif text == "/" and previous in ("import", "export"):
			in_class = False
			while end < len(source):
				char = source[end]
				end += 1
				if char == "\\":
					end += 1
				elif char == "[":
					in_class = True
				elif char == "]":
					in_class = False
				elif char == "/" and not in_class:
					break
			else:
				raise DocumentationError("unterminated import regex")
			kind = "literal"
		if kind not in ("space", "comment", "doc"):
			previous = text
		yield kind, source[position:end], position, end
		position = end


def quoted_end(source, start):
	quote = source[start]
	position = start + 1
	while position < len(source):
		char = source[position]
		if char == "\\":
			position += 2
			continue
		if char == quote:
			return position + 1
		if quote == "`" and source.startswith("${", position):
			# Tokenize interpolation so nested strings/templates cannot close the outer one.
			depth = 1
			for kind, text, _, end in tokens(source[position + 2:]):
				if kind == "code" and text in ("{", "}"):
					depth += 1 if text == "{" else -1
					if depth == 0:
						position += 2 + end
						break
			else:
				raise DocumentationError("unterminated template interpolation")
			continue
		position += 1
	raise DocumentationError("unterminated string")


def signature(source, stream, start):
	position = start
	while position < len(stream) and stream[position][0] == "space":
		position += 1
	if position == len(stream):
		raise DocumentationError("@api must precede a declaration")
	first = stream[position][2]
	if stream[position][1] not in DECLARATIONS | {"@", "export", "static", "virtual", "override", "implicit"}:
		raise DocumentationError("@api must immediately precede a supported declaration")
	depth = []
	seen_declaration = False
	for kind, text, begin, end in stream[position:]:
		if kind in ("doc", "comment"):
			raise DocumentationError("place @api directly before its declaration, including attributes")
		if kind == "code":
			if text == "import" and not depth and not seen_declaration:
				raise DocumentationError("@api cannot bind across an import")
			if text in DECLARATIONS and not depth:
				seen_declaration = True
			if text in ("{", "=", ";") and not depth and seen_declaration:
				return source[first:begin].strip(), source.count("\n", 0, first) + 1
			if text in ("(", "["):
				depth.append(text)
			elif text in (")", "]"):
				if not depth or depth.pop() != {")": "(", "]": "["}[text]:
					raise DocumentationError("unbalanced declaration")
		if kind == "space" and "\n" in text and seen_declaration and not depth:
			return source[first:begin].strip(), source.count("\n", 0, first) + 1
	raise DocumentationError("unsupported or incomplete declaration after @api")


def initializer_expression(sig, source, line, name):
	"""Read a balanced top-level variable initializer without evaluating it."""
	if "." in name or not re.search(r"\b(?:let|const)\s+\w+(?:\s*:[^=]+)?$", sig):
		return None
	start_line = sum(len(part) for part in source.splitlines(keepends=True)[:line - 1])
	start = source.find(sig, start_line)
	if start < 0:
		return None
	position = start + len(sig)
	while position < len(source) and source[position] in " \t": position += 1
	if position >= len(source) or source[position] != "=" or source[position:position + 2] in ("==", "=>"):
		return None
	position += 1
	while position < len(source) and source[position] in " \t": position += 1
	begin = position
	stack = []
	last = None
	pairs = {")": "(", "]": "[", "}": "{"}
	for kind, text, offset, end in tokens(source[begin:]):
		if kind == "space" and "\n" in text and not stack:
			break
		if kind in ("comment", "doc") and not stack:
			break
		if kind == "code":
			if text in ("(", "[", "{"): stack.append(text)
			elif text in pairs:
				if not stack or stack.pop() != pairs[text]: return None
			elif text in (";", ",") and not stack:
				if text == ",": return None
				break
		if kind not in ("space", "comment", "doc"):
			last = (text, end)
	if stack or not last or last[0] in ("+", "-", "*", "/", ".", "=", "&", "|", "^", ":", "?", "<", ">", "!"):
		return None
	result = source[begin:begin + last[1]].strip()
	# A following operator can continue an expression across a newline.
	rest = source[begin + last[1]:].lstrip()
	if not rest.startswith(("//", "/*")) and rest.startswith((".", "+", "-", "*", "/", "&", "|", "^")):
		return None
	return result or None


def declaration_metadata(sig, source, declaration_line, name):
	"""Extract only simple lexical types; this is not semantic type inference."""
	owner = name.split("~")[0].rpartition(".")[0] or None
	value_type = None
	return_type = None
	binding = re.search(r"\b(?:let|const)\s+\w+\s*:\s*([^=\n]+)$", sig)
	if binding:
		value_type = binding.group(1).strip()
	elif re.search(r"\b(?:let|const)\s+\w+\s*$", sig):
		line = source.splitlines()[declaration_line - 1]
		match = re.search(r"\b(?:let|const)\s+\w+\s*=\s*([A-Za-z_]\w*)\s*\([^()]*\)\s*;?\s*$", line)
		if match:
			value_type = match.group(1)
	# Inspect only the declaration's outer parameter list, not callback parameters.
	decl = re.search(r"\b(fn|operator|get)\s*(?:[A-Za-z_]\w*)?", sig)
	if decl:
		tail = sig[decl.end():]
		if decl.group(1) == "get":
			match = re.fullmatch(r"\s*(?:\(\s*\))?\s*:\s*(.+)", tail, re.S)
		else:
			match = None
			start = tail.find("(")
			if start >= 0:
				depth = 0
				for kind, text, _, end in tokens(tail[start:]):
					if kind != "code": continue
					if text == "(": depth += 1
					elif text == ")":
						depth -= 1
						if depth == 0:
							match = re.fullmatch(r"\s*:\s*(.+)", tail[start + end:], re.S)
							break
		if match:
			return_type = match.group(1).strip()
	return {"value_type": value_type, "owner": owner, "return_type": return_type}


def prelude_environment(stdlib, entries):
	"""Follow explicit file re-export name lists without evaluating modules."""
	by_identity = {(e["source"], e["name"]): e for e in entries if e["kind"] == "api" and "." not in e["name"] and "~" not in e["name"]}
	cache = {}
	def module(path):
		if path in cache:
			return cache[path]
		file = stdlib / path
		if not file.is_file() or not file.resolve().is_relative_to(stdlib.resolve()):
			return {}, {}
		text = file.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
		stream = list(tokens(text))
		if any(kind == "code" and token == "#" and not text[text.rfind("\n", 0, start) + 1:start].strip() for kind, token, start, _ in stream):
			cache[path] = ({}, {})
			return cache[path]
		# Only top-level code participates; literals and comments are never parsed as exports.
		code = [(k, t, start, end) for k, t, start, end in stream if k not in ("space", "comment", "doc")]
		stream_positions = {token[2]: i for i, token in enumerate(stream)}
		exports, declarations = {}, {}
		depth = 0
		for i, (kind, token, start, end) in enumerate(code):
			if kind != "code":
				continue
			if depth == 0 and token == "export":
				match = re.match(r'export\s+(?:(?:lazy\s+)?import\s*)?\{([^{}]*)\}\s*from\s*"(file:[^"\n]+)"', text[start:])
				if match:
					target = posixpath.normpath(posixpath.join(posixpath.dirname(path), match[2][5:]))
					if not (stdlib / target).resolve().is_relative_to(stdlib.resolve()):
						target = '../__outside_stdlib__'
					elif not target.endswith('.el'):
						if (stdlib / (target + '.el')).is_file(): target += '.el'
						elif (stdlib / target / 'index.el').is_file(): target += '/index.el'
					for item in match[1].split(','):
						part = re.fullmatch(r'\s*(\w+)(?:\s+as\s+(\w+))?\s*', item)
						if part:
							exports.setdefault(part[2] or part[1], []).append((target, part[1]))
				else:
					# Skip attributes, then capture a straightforward exported declaration.
					match = re.match(r'export\s+(?:@\w+(?:\([^\n]*?\))?\s+)*(?:fn|class|interface|let|const|syntax|enum|data)\s+(\w+)', text[start:])
					if match:
						name = match[1]
						try:
							sig, line = signature(text, stream, stream_positions[start])
						except DocumentationError:
							continue
						metadata = declaration_metadata(sig, text, line, name)
						declarations.setdefault(name, []).append((line, sig, metadata["value_type"]))
			if token == "{": depth += 1
			elif token == "}": depth = max(0, depth - 1)
		cache[path] = exports, declarations
		return exports, declarations
	def resolve(path, name, seen):
		if (path, name) in seen:
			return None
		exports, declarations = module(path)
		candidates = []
		local = declarations.get(name, [])
		if local:
			# Same-module declarations form an overload/type family, not ambiguous imports.
			entry = by_identity.get((path, name))
			line = entry["declaration_line"] if entry else local[0][0]
			sig = entry["signature"] if entry else "\n".join(item[1] for item in local)
			value_types = {item[2] for item in local}
			value_type = next(iter(value_types)) if len(value_types) == 1 else None
			candidates.append((entry["id"] if entry else None, path, line, sig, value_type))
		for target, original in exports.get(name, []):
			resolved = resolve(target, original, seen | {(path, name)})
			if resolved is None: return None
			candidates.append(resolved)
		unique = list(dict.fromkeys(candidates))
		return unique[0] if len(unique) == 1 else None
	exports, _ = module("index.el")
	result = []
	for name in sorted(exports, key=str.casefold):
		resolved = resolve("index.el", name, set())
		if resolved:
			identity, source, line, sig, value_type = resolved
		else:
			identity, source, line, sig, value_type = None, None, None, None, None
		result.append({"name": name, "id": identity, "source": source, "line": line, "signature": sig, "value_type": value_type})
	public_exports = {}
	for file in sorted(stdlib.rglob("*.el")):
		path = file.relative_to(stdlib).as_posix()
		reexports, declarations = module(path)
		names = set(reexports) | set(declarations)
		resolved_names = {}
		for name in sorted(names):
			resolved = resolve(path, name, set())
			if resolved and resolved[0]:
				resolved_names[name] = resolved[0]
		if resolved_names:
			public_exports[path.removesuffix(".el")] = resolved_names
	return result, public_exports


def type_index(stdlib, entries):
	"""Index lexical type declarations and resolve names in their defining module."""
	documented = {}
	for e in entries:
		if e["kind"] != "api": continue
		name = e["name"].split("~")[0]
		kind_match = re.search(r"\b(class|interface|enum|data|fn|let|const)\s+" + re.escape(name) + r"\b", e["signature"])
		if kind_match: documented.setdefault((e["source"], name, kind_match[1]), []).append(e["id"])
	modules, definitions = {}, []
	for file in sorted(stdlib.rglob("*.el")):
		path = file.relative_to(stdlib).as_posix()
		text = file.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
		stream = list(tokens(text))
		if any(k == "code" and t == "#" and not text[text.rfind("\n", 0, a) + 1:a].strip() for k,t,a,_ in stream):
			continue
		local, imports, reexports, exported = {}, {}, {}, set()
		depth = 0
		for i, (kind, token, start, end) in enumerate(stream):
			if kind != "code": continue
			if depth == 0 and token in ("import", "export"):
				pattern = r'(?:export\s+(?:(?:lazy\s+)?import\s*)?|import\s+)\{([^{}]*)\}\s*from\s*"(file:[^"\n]+)"'
				match = re.match(pattern, text[start:])
				if match:
					target = posixpath.normpath(posixpath.join(posixpath.dirname(path), match[2][5:]))
					if not (stdlib / target).resolve().is_relative_to(stdlib.resolve()): continue
					if not target.endswith(".el"):
						if (stdlib / (target + ".el")).is_file(): target += ".el"
						elif (stdlib / target / "index.el").is_file(): target += "/index.el"
					for item in match[1].split(","):
						part = re.fullmatch(r'\s*(\w+)(?:\s+as\s+(\w+))?\s*', item)
						if part:
							mapping = reexports if token == "export" else imports
							mapping.setdefault(part[2] or part[1], []).append((target, part[1]))
			if depth == 0 and token in ("class", "interface", "enum", "data", "fn", "let", "const"):
				try: sig, line = signature(text, stream, i)
				except DocumentationError: continue
				match = re.match(r'(?:class|interface|enum|data|fn|let|const)\s+(\w+)', sig)
				if not match: continue
				name = match[1]
				metadata = declaration_metadata(sig, text, line, name)
				if token in ("fn", "let", "const") and (metadata["return_type"] if token == "fn" else metadata["value_type"]) != "type": continue
				initializer = initializer_expression(sig, text, line, name)
				ids = documented.get((path, name, token), [])
				definition = {"name": name, "source": path, "line": line, "signature": sig, "id": ids[0] if len(ids) == 1 else None, "initializer": initializer}
				local.setdefault(name, []).append(definition)
				definitions.append(definition)
				# Export may precede attributes on the same line.
				prefix = text[text.rfind("\n", 0, start) + 1:start]
				if re.search(r'\bexport\b', prefix): exported.add(name)
			if token == "{": depth += 1
			elif token == "}": depth = max(0, depth - 1)
		modules[path] = (local, imports, reexports, exported, bool(re.search(r'@module\s*\(\s*prelude\s*:\s*nil', text)))
	def exported_resolve(path, name, seen):
		if (path, name) in seen or path not in modules: return None
		local, _, reexports, exported, _ = modules[path]
		found = []
		if name in exported: found.extend(local.get(name, []))
		for target, original in reexports.get(name, []):
			item = exported_resolve(target, original, seen | {(path, name)})
			if item is None: return None
			found.append(item)
		# Type binding is preferable to same-named type factory, e.g. Bool.
		bindings = [x for x in found if re.match(r'(?:let|const)\b', x["signature"])]
		if bindings: found = bindings
		unique = {(x["source"], x["line"]): x for x in found}
		return next(iter(unique.values())) if len(unique) == 1 else None
	def resolve(path, name):
		if path not in modules: return None
		local, imports, _, _, disabled = modules[path]
		found = local.get(name, [])
		bindings = [x for x in found if re.match(r'(?:let|const)\b', x["signature"])]
		if bindings: found = bindings
		if found: return found[0] if len(found) == 1 else None
		if name in imports:
			resolved = [exported_resolve(target, original, set()) for target, original in imports[name]]
			if any(x is None for x in resolved): return None
			unique = {(x["source"], x["line"]): x for x in resolved}
			return next(iter(unique.values())) if len(unique) == 1 else None
		return None if disabled else exported_resolve("index.el", name, set())
	builtins = {"type": "reference/language/types.md", "any": "reference/language/types.md", "ptr": "reference/language/foreign.md"}
	for entry in entries:
		if entry["kind"] != "api": continue
		refs = {}
		for field in ("value_type", "return_type"):
			expression = entry.get(field)
			if not expression: continue
			items = []
			for match in re.finditer(r'[A-Za-z_]\w*', expression):
				name = match.group()
				if expression[match.end():].lstrip().startswith(":"): continue
				target = resolve(entry["source"], name)
				if target:
					identity = target["source"].removesuffix(".el") + "::" + target["name"]
					location = {"type": "definition", "source": target["source"], "name": target["name"], "id": target["id"], "path": page_path(target["source"]) if target["id"] else "types.md", "fragment": anchor(target["id"] or identity)}
				elif name in builtins:
					location = {"type": "builtin", "source": None, "name": name, "id": None, "path": builtins[name], "fragment": None}
				else:
					location = None
				items.append({"name": name, "start": match.start(), "end": match.end(), "target": location})
			refs[field] = items
		entry["type_references"] = refs
	return definitions


def parse_comment(lines):
	first = re.fullmatch(r"@(module|api)\s+(.+)", lines[0])
	if not first:
		raise DocumentationError("documentation starts with @module title or @api name")
	kind, name = first.groups()
	if kind == "api" and not re.fullmatch(r"[^\s/\\:#]+(?:~[\w-]+)?", name):
		raise DocumentationError("invalid API name; use a qualified name and optional ~overload label")
	sections = [{"tag": "description", "value": "", "lines": []}]
	fence = None
	for line in lines[1:]:
		marker = re.match(r"^(`{3,}|~{3,})(.*)$", line)
		if marker:
			if fence is None:
				fence = marker[1]
			elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
				fence = None
		if line.startswith("@") and fence is None:
			tag, _, value = line[1:].partition(" ")
			if tag not in ("param", "returns", "throws", "complexity", "note", "example", "see"):
				raise DocumentationError(f"unknown documentation tag @{tag}")
			if not value.strip():
				raise DocumentationError(f"@{tag} requires text")
			sections.append({"tag": tag, "value": value.strip(), "lines": []})
		else:
			sections[-1]["lines"].append(line)
	if fence:
		raise DocumentationError("unclosed Markdown fence")
	for section in sections:
		section["markdown"] = "\n".join(section.pop("lines")).strip()
		if section["tag"] == "example":
			blocks = re.findall(r"^```([^\n]*)\n(.*?)^```[ \t]*$", section["markdown"], re.M | re.S)
			if [language for language, _ in blocks] not in (["el"], ["el", "text"]):
				raise DocumentationError("@example requires one ```el block and an optional ```text expected-output block")
			section.update(code=blocks[0][1], expected_stdout=blocks[1][1] if len(blocks) == 2 else None, verification="not-run")
	if not sections[0]["markdown"]:
		raise DocumentationError("a description is required")
	if kind == "api" and not any(section["tag"] == "example" for section in sections):
		raise DocumentationError("each API requires a concrete @example")
	return {"kind": kind, "name": name, "sections": sections}


def extract(source, path):
	if "///" not in source and "//!" not in source:
		return []
	stream = list(tokens(source))
	if not any(token[0] == "doc" for token in stream):
		return []
	# Preprocessing needs target/compiler context; never publish inactive branches as APIs.
	if any(kind == "code" and text == "#" and not source[source.rfind("\n", 0, start) + 1:start].strip() for kind, text, start, _ in stream):
		raise DocumentationError(f"{path}: preprocessed files require the future compiler-backed extractor")
	entries = []
	index = 0
	while index < len(stream):
		kind, text, start, _ = stream[index]
		if kind != "doc":
			index += 1
			continue
		line = source.count("\n", 0, start) + 1
		marker = text[:3]
		lines = [text[3:].removeprefix(" ")]
		index += 1
		while index + 1 < len(stream) and stream[index][0] == "space" and stream[index][1].count("\n") == 1 and stream[index + 1][0] == "doc" and stream[index + 1][1].startswith(marker):
			lines.append(stream[index + 1][1][3:].removeprefix(" "))
			index += 2
		try:
			entry = parse_comment(lines)
			if (entry["kind"] == "module") != (marker == "//!"):
				raise DocumentationError("use //! for module documentation and /// for declarations")
			entry.update(source=path, line=line)
			if entry["kind"] == "api":
				entry["signature"], entry["declaration_line"] = signature(source, stream, index)
				declared = re.search(r"\b(?:fn|class|interface|let|const|get|set|syntax|enum|data)\s+(\w+)", entry["signature"])
				if declared and declared[1] != entry["name"].split("~")[0].split(".")[-1]:
					raise DocumentationError("@api name does not match the following declaration")
				entry["id"] = path.removesuffix(".el") + "::" + entry["name"]
				entry.update(declaration_metadata(entry["signature"], source, entry["declaration_line"], entry["name"]))
				entry["initializer"] = initializer_expression(entry["signature"], source, entry["declaration_line"], entry["name"])
			else:
				entry["id"] = path.removesuffix(".el")
			entries.append(entry)
		except DocumentationError as error:
			raise DocumentationError(f"{path}:{line}: {error}") from error
	return entries


def collect(root):
	stdlib = root / "src" / "stdlib"
	if not stdlib.is_dir():
		raise DocumentationError(f"missing source directory: {stdlib}")
	entries = []
	files = []
	for path in sorted(stdlib.rglob("*.el")):
		data = path.read_bytes()
		relative = path.relative_to(stdlib).as_posix()
		files.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest()})
		entries.extend(extract(data.decode("utf-8-sig").replace("\r\n", "\n"), relative))
	identities = set()
	for entry in entries:
		if entry["id"] in identities:
			raise DocumentationError(f"duplicate documentation id: {entry['id']}")
		identities.add(entry["id"])
	for entry in entries:
		for section in entry["sections"]:
			if section["tag"] == "see" and section["value"] not in identities:
				raise DocumentationError(f"{entry['source']}:{entry['line']}: unknown @see {section['value']}")
	documented = {entry['source'] for entry in entries}
	digest = hashlib.sha256(json.dumps(files, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
	environment, exports = prelude_environment(stdlib, entries)
	types = type_index(stdlib, entries)
	return {"environment": environment, "exports": exports, "types": types, "source_digest": digest, "files": [file for file in files if file['path'] in documented], "entries": entries, "coverage": {"source_files": len(files), "documented_files": len(documented), "documented_apis": sum(entry['kind'] == 'api' for entry in entries)}}


def anchor(identity):
	return "api-" + hashlib.sha256(identity.encode()).hexdigest()[:20]


def page_path(source):
	return "modules/" + source.removesuffix(".el") + ".md"


def render(model, source_url=SOURCE_URL):
	pages = {}
	grouped = {}
	by_id = {entry["id"]: entry for entry in model["entries"]}
	for entry in model["entries"]:
		grouped.setdefault(entry["source"], []).append(entry)
	index = ["# 标准库 API 参考", "", "由 EL 源码中的文档注释生成。仅列出已标注接口；示例预期结果由作者提供，尚未运行验证。", "", "[结构化文档数据](api.json)", ""]
	coverage = model["coverage"]
	index += [f"已标注文档的文件：{coverage['documented_files']} / {coverage['source_files']}；API 条目：{coverage['documented_apis']}。此比例不是公开 API 覆盖率。", ""]
	index += ["[按模块查找](modules.md) · [按符号查找](symbols.md) · [默认环境](environment.md) · [类型定义](types.md)", "", "## 按库分类", "", "| 库 | 已标注模块 | API 条目 |", "| --- | ---: | ---: |"]
	categories = {}
	for source, entries in grouped.items():
		categories.setdefault(source.split('/')[0] if '/' in source else 'root', {})[source] = entries
	module_index = ["# 标准库模块索引", "", "按源码路径排列，仅包含已标注文档的模块。[按库分类](index.md) · [符号索引](symbols.md)", ""]
	for category, modules in sorted(categories.items()):
		count = sum(entry['kind'] == 'api' for entries in modules.values() for entry in entries)
		index.append(f"| [{category}](categories/{category}.md) | {len(modules)} | {count} |")
		category_lines = [f"# {category}", "", "[标准库分类](../index.md) · [模块索引](../modules.md) · [符号索引](../symbols.md)", "", "本页按源码模块组织已标注接口；未标注部分不在此列表中。", "", "| 模块 | 接口 |", "| --- | --- |"]
		module_index += [f"## {category}", ""]
		for source, entries in sorted(modules.items()):
			path = page_path(source)
			apis = [entry for entry in entries if entry['kind'] == 'api']
			links = '、'.join(f"[{entry['name']}](../{path}#{anchor(entry['id'])})" for entry in apis) or '模块说明'
			category_lines.append(f"| [{source}](../{path}) | {links} |")
			module_index.append(f"- [{source}]({path})（{len(apis)} 个 API）")
		module_index.append("")
		pages[f"categories/{category}.md"] = '\n'.join(category_lines) + '\n'
	symbols = ["# 标准库符号索引", "", "按文档名字排序；成员使用限定名，重载保留标签。索引只覆盖已标注接口，不代表编译器解析后的全部导出集合。", "", "[库分类](index.md) · [模块索引](modules.md)", "", "| 符号 | 模块 |", "| --- | --- |"]
	for entry in sorted((entry for entry in model['entries'] if entry['kind'] == 'api'), key=lambda entry: (entry['name'].casefold(), entry['source'])):
		symbols.append(f"| [{entry['name']}]({page_path(entry['source'])}#{anchor(entry['id'])}) | `{entry['source']}` |")
	pages['modules.md'] = '\n'.join(module_index) + '\n'
	pages['symbols.md'] = '\n'.join(symbols) + '\n'
	environment = ["# 默认环境", "", "由标准库入口显式重导出名字表生成；仅按词法解析 file: 路径，不执行模块。未解析或有歧义的来源留空。", "", "按名称首字母分组；声明签名和类型为词法提取结果，不代表编译器的语义分析。", ""]
	current_initial = None
	for item in model.get("environment", []):
		initial = item["name"][0].upper() if item["name"][0].isalpha() else "#"
		if initial != current_initial:
			environment += [f"## {initial}", "", "| 名字 | 声明 | 说明 |", "| --- | --- | --- |"]
			current_initial = initial
		entry = by_id.get(item["id"])
		if entry:
			declaration = f"[{item['source']}:{item['line']}]({page_path(item['source'])}#{anchor(item['id'])})"
			summary = entry["sections"][0]["markdown"].replace("\n", " ").replace("|", "\\|")
		elif item["source"]:
			url = source_url.rstrip("/") + "/" + quote(item["source"], safe="/") + f"#L{item['line']}"
			declaration = f"[{item['source']}:{item['line']}]({url})"
			summary = "未标注文档"
			if item.get("value_type"):
				summary += f"；词法类型：`{item['value_type']}`"
		else:
			declaration, summary = "—", "来源未解析或有歧义"
		signature_text = (item["signature"] or "").replace("`", "\\`").replace("|", "\\|").replace("\n", " ")
		if signature_text:
			declaration += f"<br>`{signature_text}`"
		environment.append(f"| <span id=\"{anchor(item['name'])}\"></span>`{item['name']}` | {declaration} | {summary} |")
	pages["environment.md"] = "\n".join(environment) + "\n"
	type_groups = {}
	for definition in model.get("types", []):
		type_groups.setdefault((definition["source"], definition["name"]), []).append(definition)
	type_lines = ["# 类型定义索引", "", "由源码声明词法提取；类型工厂及绑定分别列出。未执行或验证类型表达式。", ""]
	for (source, name), group in sorted(type_groups.items()):
		identity = source.removesuffix(".el") + "::" + name
		type_lines += [f"## {name} · {source} {{#{anchor(identity)}}}", ""]
		for definition in group:
			url = source_url.rstrip("/") + "/" + quote(source, safe="/") + f"#L{definition['line']}"
			type_lines += [f"[源码 {source}:{definition['line']}]({url})", "", "```el", definition["signature"] + (" = " + definition["initializer"] if definition["initializer"] is not None else ""), "```", ""]
			if definition["id"]:
				type_lines += [f"[API 文档]({page_path(source)}#{anchor(definition['id'])})", ""]
		for entry in model["entries"]:
			if entry["source"] != source or entry["kind"] != "api" or entry["name"].split("~")[0] != name:
				continue
			if any(item["id"] == entry["id"] for item in group): continue
			if not re.search(r"\bfn\s+" + re.escape(name) + r"\b", entry["signature"]): continue
			type_lines += [f"[同名函数 API]({page_path(source)}#{anchor(entry['id'])})", "", "```el", entry["signature"], "```", ""]
	pages["types.md"] = "\n".join(type_lines)
	labels = {"param": "参数", "returns": "返回值", "throws": "失败与异常", "complexity": "复杂度", "note": "注意", "example": "示例"}
	for source, entries in grouped.items():
		path = page_path(source)
		lines = [f"# {source}", "", "本页由源码注释生成；示例未运行验证。", ""]
		category = source.split('/')[0] if '/' in source else 'root'
		links = [f"[{title}]({posixpath.relpath(target, posixpath.dirname(path))})" for title, target in (("库分类", f"categories/{category}.md"), ("模块索引", "modules.md"), ("符号索引", "symbols.md"))]
		lines += [' · '.join(links), ""]
		members = [entry for entry in entries if entry.get("owner")]
		if members:
			lines += ["## 成员总览", ""]
			for entry in members:
				lines.append(f"- [{entry['name']}](#{anchor(entry['id'])})")
			lines.append("")
		families = {}
		for entry in entries:
			if entry["kind"] == "api" and "~" in entry["name"]:
				families.setdefault(entry["id"].split("~")[0], []).append(entry)
		emitted = set()
		for entry in entries:
			family = entry["id"].split("~")[0]
			if family in families and family not in emitted and family not in by_id:
				lines += [f'<span id="{anchor(family)}"></span>', ""]
				emitted.add(family)
			line = entry.get("declaration_line", entry["line"])
			url = source_url.rstrip("/") + "/" + quote(source, safe="/") + f"#L{line}"
			lines += [f"## {entry['name']} {{#{anchor(entry['id'])}}}", "", f"源码：`src/stdlib/{source}:{line}` · [在 GitHub 查看源码]({url})", ""]
			if "signature" in entry:
				display = entry["signature"]
				if entry.get("initializer") is not None:
					display += " = " + entry["initializer"]
				lines += ["```el", display, "```", ""]
			for field, label in (("value_type", "类型"), ("return_type", "返回类型")):
				expression = entry.get(field)
				if not expression: continue
				pieces, offset, unresolved = [], 0, []
				for ref in entry.get("type_references", {}).get(field, []):
					pieces.append(expression[offset:ref["start"]])
					target = ref["target"]
					if target:
						if target["type"] == "builtin":
							link = posixpath.relpath("../../" + target["path"], posixpath.dirname(path))
						else:
							link = posixpath.relpath(target["path"], posixpath.dirname(path))
						if target["fragment"]: link += "#" + target["fragment"]
						pieces.append(f"[`{ref['name']}`]({link})")
					else:
						pieces.append(f"`{ref['name']}`")
						unresolved.append(ref["name"])
					offset = ref["end"]
				pieces.append(expression[offset:])
				lines += [f"**{label}**：" + "".join(pieces), ""]
				if unresolved: lines += ["未解析：" + "、".join(f"`{name}`" for name in dict.fromkeys(unresolved)), ""]
			for section in entry["sections"]:
				tag, value = section["tag"], section["value"]
				if tag == "see":
					target = by_id[value]
					# Relative links work both in MkDocs and standalone Markdown.
					link = posixpath.relpath(page_path(target["source"]), posixpath.dirname(path))
					lines += [f"参见：[{value}]({link}#{anchor(value)})", ""]
				elif tag == "example":
					lines += [f"### 示例：{value}", ""]
				elif tag != "description":
					lines += [f"**{labels[tag]}**：{value}", ""]
				if section["markdown"]:
					lines += [section["markdown"], ""]
		pages[path] = "\n".join(lines).rstrip() + "\n"
	pages["index.md"] = "\n".join(index) + "\n"
	pages["api.json"] = json.dumps(model, ensure_ascii=False, indent="\t") + "\n"
	return pages


def write_pages(output, pages, check=False):
	"""Own only manifest-listed files; refuse overwriting handwritten content."""
	manifest = output / ".generated.json"
	previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
	for name, digest in previous.items():
		path = output / name
		if Path(name).is_absolute() or ".." in Path(name).parts or not path.resolve().is_relative_to(output.resolve()):
			raise DocumentationError("unsafe generated manifest path")
		if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
			raise DocumentationError(f"generated file was edited: {path}")
	changed = set(previous) != set(pages)
	for name, content in pages.items():
		path = output / name
		if not path.resolve().is_relative_to(output.resolve()):
			raise DocumentationError(f"output escapes destination: {path}")
		if path.exists() and name not in previous:
			raise DocumentationError(f"refusing to overwrite unowned file: {path}")
		changed |= not path.exists() or path.read_bytes() != content.encode()
	if check:
		if changed:
			raise DocumentationError("generated documentation is stale; regenerate it")
		return
	for name, content in pages.items():
		path = output / name
		if not path.exists() or path.read_bytes() != content.encode():
			atomic_write(path, content)
	for name in previous.keys() - pages.keys():
		(output / name).unlink(missing_ok=True)
	digests = {name: hashlib.sha256(content.encode()).hexdigest() for name, content in pages.items()}
	atomic_write(manifest, json.dumps(digests, indent="\t") + "\n")


def atomic_write(path, content):
	path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
		temporary.write(content.encode("utf-8"))
		temporary_path = Path(temporary.name)
	try:
		temporary_path.replace(path)
	finally:
		temporary_path.unlink(missing_ok=True)


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--el-root", type=Path, required=True, help="EL checkout containing src/stdlib")
	parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "docs/stdlib/api")
	parser.add_argument("--check", action="store_true", help="check generated files without writing")
	parser.add_argument("--source-url", default=SOURCE_URL, help="GitHub blob URL prefix for src/stdlib (default: EL master)")
	args = parser.parse_args()
	try:
		model = collect(args.el_root.resolve())
		if not model["entries"]:
			raise DocumentationError("no documentation comments found")
		write_pages(args.output.resolve(), render(model, args.source_url), args.check)
		print(json.dumps(model["coverage"], ensure_ascii=False))
	except (DocumentationError, OSError, UnicodeError) as error:
		print(error, file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
