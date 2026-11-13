"""Link highlighted EL names to source-generated reference entries.

This is a conservative documentation lookup, not a compiler name resolver.
Local declarations suppress automatic links; unknown receiver types stay plain.
"""

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import importlib.util
from html import escape, unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, Keyword, Name, String, Text, Whitespace

_source_spec = importlib.util.spec_from_file_location("el_doc_source", Path(__file__).resolve().parents[1] / "scripts/stdlib_docs.py")
_source_docs = importlib.util.module_from_spec(_source_spec)
_source_spec.loader.exec_module(_source_docs)
DocumentationError = _source_docs.DocumentationError
source_tokens = _source_docs.tokens


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
		self.signature_types = {}
		for entry in self.entries.values():
			self.names[entry["name"].split("~")[0]].append(entry)
			if "signature" in entry:
				display = entry["signature"]
				if entry.get("initializer") is not None:
					display += " = " + entry["initializer"]
				self.signature_types.setdefault(display, []).append(entry)
				concise = _source_docs.readable_signature(display)
				if concise != display:
					self.signature_types.setdefault(concise, []).append(entry)
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

	def type_targets(self, code, source=None):
		"""Use declaration-context references only for an exact generated signature."""
		result = {}
		matches = self.signature_types.get(code.strip(), [])
		if source is not None:
			matches = [entry for entry in matches if entry["source"] == source]
		if not matches:
			return result
		entry = matches[0]
		ambiguous = any(candidate.get("type_references") != entry.get("type_references") for candidate in matches[1:])
		signature = entry["signature"]
		if signature not in code:
			signature = _source_docs.readable_signature(signature)
		base = code.find(signature)
		for field, references in entry.get("type_references", {}).items():
			expression = entry.get(field)
			if not expression:
				continue
			start = signature.rfind(expression)
			if start < 0:
				continue
			for reference in references:
				target = None if ambiguous else reference["target"]
				# Explicitly unresolved names suppress default same-name lookup.
				location = None
				if target:
					path = target["path"] if target["type"] == "builtin" else "stdlib/api/" + target["path"]
					location = Target(path, target.get("fragment") or "", reference["name"])
				result[base + start + reference["start"]] = (reference["end"] - reference["start"], location)
		return result


def code_targets(code, catalog, source=None):
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
	for offset, (length, target) in catalog.type_targets(code, source).items():
		if target:
			result[offset] = (length, target)
		else:
			result.pop(offset, None)
	return result


class CodeLinker(HTMLParser):
	def __init__(self, html, catalog, url_for, source=None):
		super().__init__(convert_charrefs=False)
		self.html = html
		self.catalog = catalog
		self.url_for = url_for
		self.source = source
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
		targets = code_targets(self.code["text"], self.catalog, self.source)
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
		pieces = []
		cursor = 0
		for start, end, replacement in sorted(self.replacements):
			pieces.extend((self.html[cursor:start], replacement))
			cursor = end
		pieces.append(self.html[cursor:])
		return "".join(pieces)


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
		target_url = _files[target.path]
		parent = page.url if page.url.endswith("/") else posixpath.dirname(page.url)
		url = posixpath.relpath(target_url or ".", parent or ".")
		if (not target_url or target_url.endswith("/")) and not url.endswith("/"):
			url += "/"
		return url + ("#" + target.fragment if target.fragment else "")
	uri = getattr(getattr(page, "file", None), "src_uri", "")
	source = uri.removeprefix("stdlib/api/modules/").removesuffix(".md") + ".el" if uri.startswith("stdlib/api/modules/") else None
	return CodeLinker(html, _catalog, url_for, source).render()


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


class PageIndex(FragmentIndex):
	def __init__(self, html):
		self.links = []
		super().__init__(html)

	def handle_starttag(self, tag, attrs):
		super().handle_starttag(tag, attrs)
		attributes = dict(attrs)
		if tag == "a" and attributes.get("href"):
			self.links.append(attributes["href"])


def validate_site(site_dir):
	"""Check actual rendered internal hyperlinks, including generated type links."""
	site_dir = Path(site_dir).resolve()
	files = {path for path in site_dir.rglob("*") if path.is_file()}
	pages = {path: PageIndex(path.read_text(encoding="utf-8")) for path in files if path.suffix == ".html"}
	count = 0
	for path, page in pages.items():
		for href in page.links:
			url = urlsplit(href)
			if url.scheme or url.netloc or url.path.startswith("/"):
				continue
			target = Path(os.path.normpath(path.parent / unquote(url.path))) if url.path else path
			if target / "index.html" in pages:
				target /= "index.html"
			if not target.is_relative_to(site_dir) or target not in files:
				raise ValueError(f"missing site link: {path.relative_to(site_dir)} -> {href}")
			if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
				raise ValueError(f"missing site anchor: {path.relative_to(site_dir)} -> {href}")
			count += 1
	return count


def link_site(site_dir, docs_dir, *, use_directory_urls=True):
	"""Apply reference links to a built static site without builder plugin APIs."""
	site_dir, docs_dir = Path(site_dir).resolve(), Path(docs_dir).resolve()
	files = []
	for path in sorted(docs_dir.rglob("*.md")):
		uri = path.relative_to(docs_dir).as_posix()
		stem = uri.removesuffix(".md")
		if stem == "404" or not use_directory_urls:
			url = stem + ".html"
		elif path.name == "index.md":
			url = stem.removesuffix("index")
		else:
			url = stem + "/"
		destination = site_dir / (url + "index.html" if not url or url.endswith("/") else url)
		if destination.is_file():
			files.append(SimpleNamespace(src_uri=uri, url=url, abs_dest_path=str(destination)))
	config = {"site_dir": str(site_dir), "docs_dir": str(docs_dir)}
	on_files(files, config)
	changed = 0
	for file in files:
		path = Path(file.abs_dest_path)
		original = path.read_text(encoding="utf-8")
		linked = on_page_content(original, SimpleNamespace(url=file.url, file=file), config, files)
		if linked != original:
			_source_docs.atomic_write(path, linked)
			changed += 1
	on_post_build(config)
	return {"linked_pages": changed, "validated_links": validate_site(site_dir)}
