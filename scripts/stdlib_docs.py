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
	return {"source_digest": digest, "files": [file for file in files if file['path'] in documented], "entries": entries, "coverage": {"source_files": len(files), "documented_files": len(documented), "documented_apis": sum(entry['kind'] == 'api' for entry in entries)}}


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
	labels = {"param": "参数", "returns": "返回值", "throws": "失败与异常", "complexity": "复杂度", "note": "注意", "example": "示例"}
	for source, entries in grouped.items():
		path = page_path(source)
		index.append(f"- [{source}]({path})")
		lines = [f"# {source}", "", "本页由源码注释生成；示例未运行验证。", ""]
		for entry in entries:
			line = entry.get("declaration_line", entry["line"])
			url = source_url.rstrip("/") + "/" + quote(source, safe="/") + f"#L{line}"
			lines += [f"## {entry['name']} {{#{anchor(entry['id'])}}}", "", f"源码：`src/stdlib/{source}:{line}` · [在 GitHub 查看源码]({url})", ""]
			if "signature" in entry:
				lines += ["```el", entry["signature"], "```", ""]
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
