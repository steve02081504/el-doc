"""Link highlighted EL names to source-generated reference entries.

This is a conservative documentation lookup, not a compiler name resolver.
Local declarations suppress automatic links; unknown receiver types stay plain.
"""

from collections import defaultdict
from dataclasses import dataclass
import hashlib
from html import escape, unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from mkdocs.utils import get_relative_url
from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, Keyword, Name, String, Text, Whitespace

from scripts.stdlib_docs import DocumentationError, tokens as source_tokens


def anchor(identity):
	return "api-" + hashlib.sha256(identity.encode()).hexdigest()[:20]


LANGUAGE = {
	"fn": "functions", "return": "functions", "class": "classes",
	"constructor": "classes", "destructor": "lifetimes", "extends": "classes",
	"implements": "classes", "interface": "types", "let": "declarations",
	"const": "declarations", "import": "modules", "export": "modules",
	"from": "modules", "as": "modules", "lazy": "modules", "extern": "foreign",
	"if": "control-flow", "else": "control-flow", "for": "control-flow",
	"while": "control-flow", "do": "control-flow", "switch": "control-flow",
	"case": "control-flow", "break": "control-flow", "continue": "control-flow",
	"throw": "execution", "try": "execution", "catch": "execution",
	"finally": "execution", "ref": "assignment-semantics", "rvalue": "value-categories",
	"take": "lifetimes", "implicit": "conversions", "operator": "overload-resolution",
	"virtual": "classes", "override": "classes", "is": "expressions", "isnot": "expressions",
	"get": "classes", "set": "classes", "syntax": "metaprogramming", "any": "types",
	"@assign": "assignment-semantics", "@destruct": "lifetimes",
	"@module": "modules", "@runtime": "modules",
}


@dataclass(frozen=True)
class Target:
	path: str
	fragment: str = ""
	label: str = ""
	value_type: str | None = None


class Catalog:
	def __init__(self, model):
		self.entries = {entry["id"]: entry for entry in model["entries"] if entry["kind"] == "api"}
		self.names = defaultdict(list)
		self.modules = defaultdict(dict)
		self.defaults = {}
		for entry in self.entries.values():
			self.names[entry["name"].split("~")[0]].append(entry)
		for entry in self.entries.values():
			name = entry["name"].split("~")[0]
			if "." not in name:
				self.modules[entry["source"].removesuffix(".el")][name] = self.named(name, entry["source"])
		for binding in model.get("environment", []):
			entry = self.entries.get(binding.get("id"))
			target = self.named(entry["name"].split("~")[0], entry["source"]) if entry else None
			if target is None and binding.get("source"):
				target = self.named(binding["name"], binding["source"])
			if target is None:
				target = Target("stdlib/api/environment.md", anchor(binding["name"]), binding["name"], binding.get("value_type"))
			self.defaults[binding["name"]] = target
			# A documented original binding can also be imported from its source.
			if binding.get("source"):
				self.modules[binding["source"].removesuffix(".el")].setdefault(binding["name"], target)
		for module, bindings in model.get("exports", {}).items():
			for name, identity in bindings.items():
				entry = self.entries.get(identity)
				if entry:
					self.modules[module][name] = self.named(entry["name"].split("~")[0], entry["source"])

	def named(self, name, source=None):
		entries = [entry for entry in self.names.get(name, []) if source is None or entry["source"] == source]
		if not entries or len({entry["source"] for entry in entries}) != 1:
			return None
		entry = entries[0]
		identity = entry["id"].split("~")[0] if len(entries) > 1 else entry["id"]
		return Target("stdlib/api/modules/" + entry["source"].removesuffix(".el") + ".md",
			anchor(identity), name, entry.get("value_type") or entry.get("return_type"))

	def member(self, receiver, name):
		if receiver and receiver.value_type:
			return self.named(receiver.value_type + "." + name)
		return None

	def imported(self, uri, name):
		if not uri.startswith("el:"):
			return None
		module = uri[3:]
		module = (module + "index" if module.endswith("/") else module).removesuffix(".el")
		if module in ("", "index"):
			return self.defaults.get(name)
		return self.modules.get(module, {}).get(name)


def code_targets(code, catalog):
	"""Return source offsets for names whose documentation target is known.

	Bindings declared anywhere in a fragment suppress default lookup throughout
	that fragment. This deliberately forgoes some valid links in nested scopes.
	"""
	try:
		opaque = [(start, end) for kind, _, start, end in source_tokens(code) if kind in ("literal", "comment", "doc")]
	except DocumentationError:
		return {}
	tokens = [(offset, kind, value) for offset, kind, value in get_lexer_by_name("el").get_tokens_unprocessed(code)
		if kind not in Comment and kind not in Whitespace and not (kind in Text and value.isspace())]
	bindings = dict(catalog.defaults)
	local_types = defaultdict(set)
	structure = " ".join(value if kind not in String else "STRING" for _, kind, value in tokens)
	if re.search(r"@(module|runtime)\s*\([^)]*\bprelude\s*:\s*nil\b", structure):
		bindings.clear()
	imports = set()
	declarations = set()
	parameter_depth = 0
	parameter_mode = False
	for index, (_, kind, value) in enumerate(tokens):
		if value == "import":
			end = next((position for position in range(index + 1, len(tokens)) if tokens[position][2] == "from"), None)
			if end is None or end + 1 >= len(tokens) or tokens[end + 1][1] not in String:
				continue
			uri = tokens[end + 1][2][1:-1]
			names = tokens[index + 1:end]
			if not any(item[2] == "{" for item in names):
				# Namespace and pattern imports need compiler export information.
				for position, (_, token_kind, token_value) in enumerate(names):
					if token_value == "as" and position + 1 < len(names):
						bindings[names[position + 1][2]] = None
				continue
			position = 0
			while position < len(names):
				offset, token_kind, original = names[position]
				if token_kind in Name:
					alias = original
					if position + 2 < len(names) and names[position + 1][2] == "as":
						alias = names[position + 2][2]
						imports.add(names[position + 2][0])
						position += 2
					bindings[alias] = catalog.imported(uri, original)
					local_types[alias].add(None)
					imports.add(offset)
				position += 1
		if value in ("let", "const", "fn", "class", "interface", "enum", "get", "set", "syntax") and index + 1 < len(tokens):
			next_offset, next_kind, next_value = tokens[index + 1]
			if next_kind in Name:
				bindings[next_value] = None
				declarations.add(next_offset)
				type_name = None
				if value in ("let", "const") and index + 4 < len(tokens) and tokens[index + 2][2] == ":" and tokens[index + 4][2] == "=":
					type_name = tokens[index + 3][2]
				local_types[next_value].add(type_name)
		# Suppress parameter names (including lambdas) rather than guess scopes.
		if value == "fn":
			parameter_mode = True
		elif parameter_mode and value == "(":
			parameter_depth += 1
		elif parameter_mode and value == ")":
			parameter_depth -= 1
			if parameter_depth == 0:
				parameter_mode = False
		elif parameter_mode and parameter_depth == 1 and kind in Name:
			previous = tokens[index - 1][2] if index else ""
			if previous in ("(", ",", "ref", "borrow", "rvalue", "take"):
				bindings[value] = None
				local_types[value].add(None)
				declarations.add(tokens[index][0])
	# An arrow's bare identifier or parenthesized parameters can shadow defaults.
	for index, (_, _, value) in enumerate(tokens):
		if value != "=>" or index == 0:
			continue
		position = index - 1
		if tokens[position][1] in Name:
			bindings[tokens[position][2]] = None
			local_types[tokens[position][2]].add(None)
			declarations.add(tokens[position][0])
		elif tokens[position][2] == ")":
			depth = 1
			while position > 0 and depth:
				position -= 1
				depth += (tokens[position][2] == ")") - (tokens[position][2] == "(")
			for current in range(position + 1, index - 1):
				if tokens[current][1] in Name and tokens[current - 1][2] in ("(", ",", "ref", "borrow", "take", "rvalue"):
					bindings[tokens[current][2]] = None
					local_types[tokens[current][2]].add(None)
					declarations.add(tokens[current][0])
	result = {}
	resolved = {}
	for index, (offset, kind, value) in enumerate(tokens):
		if offset in declarations or any(start <= offset < end for start, end in opaque):
			continue
		previous = tokens[index - 1][2] if index else ""
		following = tokens[index + 1][2] if index + 1 < len(tokens) else ""
		target = None
		is_introducer = value in ("get", "set", "syntax") and index + 1 < len(tokens) and tokens[index + 1][1] in Name
		if (kind in Keyword or kind in Name.Decorator or is_introducer) and value in LANGUAGE:
			target = Target("reference/language/" + LANGUAGE[value] + ".md", label=value)
		elif kind in Name or kind in Keyword.Constant:
			if previous in (".", "?."):
				target = catalog.member(resolved.get(index - 2), value)
			elif following != ":" or previous in ("let", "const"):
				target = bindings.get(value)
				if target is None and len(local_types.get(value, ())) == 1:
					target = Target("", value_type=next(iter(local_types[value])))
		resolved[index] = target
		if target and target.path:
			result[offset] = (len(value), target)
	return result


class CodeLinker(HTMLParser):
	def __init__(self, html, catalog, url_for):
		super().__init__(convert_charrefs=False)
		self.html = html
		self.catalog = catalog
		self.url_for = url_for
		self.lines = [0]
		self.lines.extend(match.end() for match in re.finditer("\n", html))
		self.stack = []
		self.code = None
		self.replacements = []
		self.feed(html)

	def raw_offset(self):
		line, column = self.getpos()
		return self.lines[line - 1] + column

	def handle_starttag(self, tag, attrs):
		classes = dict(attrs).get("class", "").split()
		is_el = any(value in ("language-el", "language-els", "language-evil") for value in classes)
		active = is_el or bool(self.stack and self.stack[-1][1])
		if tag not in ("br", "hr", "img", "input", "meta", "link", "wbr", "source"):
			self.stack.append((tag, active))
		if tag == "code" and active:
			self.code = {"text": "", "parts": [], "linked": False, "link_depth": 0}
		elif self.code is not None and tag == "a":
			self.code["link_depth"] += 1

	def handle_startendtag(self, tag, attrs):
		pass

	def handle_endtag(self, tag):
		if tag == "a" and self.code is not None:
			self.code["link_depth"] -= 1
		if tag == "code" and self.code is not None:
			if not self.code["linked"]:
				self.link_block()
			self.code = None
		for index in range(len(self.stack) - 1, -1, -1):
			if self.stack[index][0] == tag:
				del self.stack[index:]
				break

	def part(self, raw, decoded):
		if self.code is not None:
			if self.code["link_depth"] and decoded.strip():
				self.code["linked"] = True
			self.code["parts"].append((len(self.code["text"]), self.raw_offset(), raw, decoded))
			self.code["text"] += decoded

	def handle_data(self, data):
		self.part(data, data)

	def handle_entityref(self, name):
		raw = "&" + name + ";"
		self.part(raw, unescape(raw))

	def handle_charref(self, name):
		raw = "&#" + name + ";"
		self.part(raw, unescape(raw))

	def link_block(self):
		targets = code_targets(self.code["text"], self.catalog)
		for start, raw_start, raw, decoded in self.code["parts"]:
			pieces = []
			cursor = 0
			for offset, (length, target) in sorted(targets.items()):
				if start <= offset and offset + length <= start + len(decoded):
					local = offset - start
					pieces.append(escape(decoded[cursor:local], quote=False))
					url = escape(self.url_for(target), quote=True)
					label = escape("查看 " + target.label + " 的参考文档", quote=True)
					pieces.append(f'<a class="el-code-link" href="{url}" title="{label}">{escape(decoded[local:local + length])}</a>')
					cursor = local + length
			if pieces:
				pieces.append(escape(decoded[cursor:], quote=False))
				self.replacements.append((raw_start, raw_start + len(raw), "".join(pieces)))

	def render(self):
		result = self.html
		for start, end, replacement in reversed(sorted(self.replacements)):
			result = result[:start] + replacement + result[end:]
		return result


_catalog = None
_files = {}
_destinations = {}
_used_targets = set()


def on_files(files, config):
	global _catalog, _files, _destinations
	model = json.loads((Path(config["docs_dir"]) / "stdlib/api/api.json").read_text(encoding="utf-8"))
	_catalog = Catalog(model)
	_files = {file.src_uri: file.url for file in files}
	_destinations = {file.src_uri: file.abs_dest_path for file in files}
	_used_targets.clear()
	# Fail the build for stale reference destinations, including handwritten ones.
	for path in {"reference/language/" + name + ".md" for name in LANGUAGE.values()}:
		if path not in _files:
			raise ValueError(f"missing code reference destination: {path}")
	return files


def on_page_content(html, page, config, files):
	def url_for(target):
		_used_targets.add(target)
		url = get_relative_url(_files[target.path], page.url)
		return url + ("#" + target.fragment if target.fragment else "")
	return CodeLinker(html, _catalog, url_for).render()


class FragmentIndex(HTMLParser):
	def __init__(self, html):
		super().__init__()
		self.ids = set()
		self.feed(html)

	def handle_starttag(self, tag, attrs):
		identity = dict(attrs).get("id")
		if identity:
			self.ids.add(identity)


def on_post_build(config):
	"""Validate generated code links against the final HTML, including anchors."""
	fragments = {}
	for target in sorted(_used_targets, key=lambda item: (item.path, item.fragment)):
		if target.path not in fragments:
			fragments[target.path] = FragmentIndex(Path(_destinations[target.path]).read_text(encoding="utf-8")).ids
		if target.fragment and target.fragment not in fragments[target.path]:
			raise ValueError(f"missing code reference anchor: {target.path}#{target.fragment}")
