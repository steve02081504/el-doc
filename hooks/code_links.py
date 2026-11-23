"""Check and link highlighted EL names using the source-generated API catalog."""

from bisect import bisect_right
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
from pygments.token import Comment, Keyword, Name, Number, String, Text, Whitespace

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


COMPREHENSION_REFERENCE = "reference/language/comprehensions.md"
BUILTIN_TYPES = {"type": "types", "any": "types", "ptr": "foreign"}


@dataclass(frozen=True)
class Target:
	path: str
	fragment: str = ""
	label: str = ""
	value_type: str | None = None


def example_key(code):
	return "\n".join(line.strip() for line in code.strip().splitlines())


class Catalog:
	def __init__(self, model):
		self.entries = {entry["id"]: entry for entry in model["entries"] if entry["kind"] == "api"}
		self.names = defaultdict(list)
		self.modules = model.get("exports", {})
		self.library_exports = {}
		for module in self.modules.values():
			for name, binding in module.items():
				previous = self.library_exports.get(name)
				if previous is None or not (previous.get("id") or previous.get("documented")):
					self.library_exports[name] = binding
		self.environment = {binding["name"]: binding for binding in model.get("environment", [])}
		self.defaults = {}
		self.signature_types = {}
		self.value_hints = _source_docs.documented_value_types(self.entries.values())
		module_entries = defaultdict(list)
		for entry in self.entries.values():
			module_entries[entry["source"]].append(entry)
		self.module_hints = {path: _source_docs.documented_value_types(items) for path, items in module_entries.items()}
		for path, returns in model.get("module_return_types", {}).items():
			self.module_hints.setdefault(path, {}).update(returns)
		self.types = defaultdict(list)
		for definition in model.get("types", ()):
			self.types[definition["name"]].append(definition)
		self.constructors = set(self.types)
		self.example_setups = defaultdict(set)
		setups = _source_docs.class_example_setups(self.entries.values())
		for entry in self.entries.values():
			name = entry["name"].split("~")[0]
			self.names[name].append(entry)
			for section in entry.get("sections", ()):
				if section["tag"] == "example":
					setup = setups.get((entry["source"], entry.get("owner")), "")
					self.example_setups[(entry["source"], example_key(section["code"]))].add(setup)
			if "signature" in entry:
				display = entry["signature"]
				if entry.get("initializer") is not None:
					display += " = " + entry["initializer"]
				self.signature_types.setdefault(display, []).append(entry)
				concise = _source_docs.readable_signature(display)
				if concise != display:
					self.signature_types.setdefault(concise, []).append(entry)
		for name, binding in self.environment.items():
			target = self.binding_target(binding)
			self.defaults[name] = target or Target(
				"stdlib/api/environment.md", anchor(name), name, binding.get("value_type"))

	def binding_target(self, binding):
		entry = self.entries.get(binding.get("id"))
		if entry:
			return self.named(entry["name"].split("~")[0], entry["source"])
		return None

	def named(self, name, source=None):
		entries = [entry for entry in self.names.get(name, []) if source is None or entry["source"] == source]
		if not entries or len({entry["source"] for entry in entries}) != 1:
			return None
		entry = entries[0]
		identity = entry["id"].split("~")[0] if len(entries) > 1 else entry["id"]
		types = {entry.get("value_type") or entry.get("return_type") for entry in entries}
		value_type = types.pop() if len(types) == 1 else None
		return Target("stdlib/api/modules/" + entry["source"].removesuffix(".el") + ".md",
			anchor(identity), name, value_type)

	def member(self, receiver, name):
		if receiver and (owner := _source_docs.nominal_type(receiver.value_type)):
			return self.named(owner + "." + name)
		return None

	def external_type(self, name, source):
		if name in BUILTIN_TYPES:
			return Target("reference/language/" + BUILTIN_TYPES[name] + ".md", label=name)
		definitions = self.types.get(name, ())
		sources = {definition["source"] for definition in definitions}
		if source not in sources:
			source = next(iter(sources)) if len(sources) == 1 else None
		if source is None:
			return None
		if target := self.named(name, source):
			return target
		definitions = [definition for definition in definitions if definition["source"] == source]
		if len(definitions) == 1:
			return Target("stdlib/api/types.md", anchor(source.removesuffix(".el") + "::" + name), name)
		return None

	def module(self, uri):
		path = uri.removeprefix("el:")
		if not path or path in ("/", "index.el"):
			return self.environment
		directory = path.endswith("/") or not path.endswith(".el")
		path = posixpath.normpath(path)
		module = posixpath.join(path, "index") if directory else path.removesuffix(".el")
		return self.modules.get(module)

	def example_setup(self, source, code):
		setups = self.example_setups.get((source, example_key(code)), ())
		return next(iter(setups)) if len(setups) == 1 else ""

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


def comprehension_offsets(tokens):
	"""Find `for let` suffixes within an array or parenthesized expression."""
	delimiters = []
	closing = {"(": ")", "[": "]", "{": "}"}
	previous = ("", "", 0, 0)
	for index, token in enumerate(tokens):
		kind, value, start, _ = token
		if kind == "code":
			if value in closing:
				array = value == "[" and previous[1] == "@" and previous[3] == start
				delimiters.append((closing[value], value == "(" or array))
			elif value in (")", "]", "}"):
				if delimiters and delimiters[-1][0] == value:
					delimiters.pop()
				else:
					delimiters.clear()
			elif value == "for" and delimiters and delimiters[-1][1] and previous[1] not in ("(", "[", ",", ";"):
				if index + 1 < len(tokens) and tokens[index + 1][1] == "let":
					yield start
		previous = token


BUILTIN_NAMES = {"type", "any", "ptr", "this", "super", "it", "void",
	"__BUILTIN_FILEPATH__", "__BUILTIN_LINENUMBER__", "__BUILTIN_LINE_CONTENT__",
	"__BUILTIN_FILE_CONTENT__", "__BUILTIN_FUNCTION_INFO__", "eir"}


def export_problem(binding, name, context):
	if binding is None:
		return f"{name!r} is not exported by {context}"
	if not (binding.get("id") or binding.get("documented")):
		location = f" ({binding['source']}:{binding['line']})" if binding.get("source") and binding.get("line") is not None else ""
		return f"{name!r} is exported by {context} but has no API documentation{location}"
	return None


def check_delimiters(stream, report):
	closing = {"(": ")", "[": "]", "{": "}"}
	stack = []
	for kind, value, start, _ in stream:
		if kind != "code":
			continue
		if value in closing:
			stack.append((closing[value], start))
		elif value in closing.values():
			if not stack or value != stack[-1][0]:
				report(start, f"unexpected {value!r}")
				return
			stack.pop()
	if stack:
		expected, start = stack[-1]
		report(start, f"missing {expected!r}")


@dataclass(frozen=True)
class Import:
	start: int
	end: int
	uri: str | None
	names: tuple = ()
	pattern: str | None = None
	namespace: str | None = None


def code_imports(stream):
	code = [token for token in stream if token[0] in ("code", "literal")]
	for index, (_, value, _, end) in enumerate(code):
		if value not in ("import", "export") or index + 1 >= len(code):
			continue
		position = index + 1
		kind, prefix, start, _ = code[position]
		names = []
		pattern = namespace = None
		if prefix == "{":
			position += 1
			while position < len(code) and code[position][1].isidentifier():
				_, name, offset, _ = code[position]
				position += 1
				alias = name
				if position + 1 < len(code) and code[position][1] == "as":
					alias = code[position + 1][1]
					position += 2
				names.append((name, alias, offset))
				if position >= len(code) or code[position][1] != ",":
					break
				position += 1
			if position >= len(code) or code[position][1] != "}":
				continue
			position += 1
		elif kind == "literal" and prefix.startswith("/"):
			pattern = prefix[1:-1]
			position += 1
			if position + 1 < len(code) and code[position][1] == "as":
				namespace = code[position + 1][1]
				position += 2
		else:
			continue
		if position + 1 >= len(code) or code[position][1] != "from":
			continue
		kind, path, _, end = code[position + 1]
		uri = path[1:-1] if kind == "literal" and path.startswith(('"', "'")) else None
		yield Import(start, end, uri, tuple(names), pattern, namespace)



BINDING_MODIFIERS = {"ref", "borrow", "rvalue", "take"}


def paired_tokens(tokens, ignored):
	closing = {"(": ")", "[": "]", "{": "}", "@{": "}", "@[": "]", "@(": ")"}
	stack = []
	pairs = {}
	for index, (offset, _, value) in enumerate(tokens):
		if offset in ignored:
			continue
		if value in closing:
			stack.append((closing[value], index))
		elif stack and value == stack[-1][0]:
			_, opening = stack.pop()
			pairs[opening] = index
			pairs[index] = opening
	return pairs


def binding_indices(tokens, pairs, start, end, *, object_pattern=False):
	"""Yield parameter or destructuring positions, skipping default expressions."""
	index = start
	while index < end:
		while index < end and tokens[index][2] in BINDING_MODIFIERS | {"..", ".", ",", ";"}:
			index += 1
		if index >= end:
			break
		if tokens[index][1] in Name or tokens[index][1] in Keyword.Constant:
			if object_pattern and index + 1 < end and tokens[index + 1][2] == ":":
				index += 2
			else:
				yield index
		if index in pairs and tokens[index][2] in ("{", "["):
			stop = pairs[index]
			yield from binding_indices(tokens, pairs, index + 1, stop, object_pattern=tokens[index][2] == "{")
			index = stop + 1
		elif object_pattern and index < end and tokens[index - 1][2] == ":" and tokens[index][1] in Name:
			yield index
		while index < end and tokens[index][2] not in (",", ";"):
			index = max(index, pairs.get(index, index)) + 1


def local_declarations(code, tokens, ignored, pairs):
	for index, (offset, kind, value) in enumerate(tokens):
		if offset in ignored or index + 1 >= len(tokens):
			continue
		following = tokens[index + 1][2]
		if value in ("let", "const", "fn", "class", "interface", "enum", "data", "get", "set", "syntax", "extern") and tokens[index + 1][1] in Name:
			type_name = None
			if value in ("let", "const") and index + 4 < len(tokens) and tokens[index + 2][2] == ":" and tokens[index + 4][2] == "=":
				type_name = tokens[index + 3][2]
			yield index + 1, type_name
		if value in ("let", "const") and following in ("[", "{") and index + 1 in pairs:
			end = pairs[index + 1]
			pattern = following == "[" or end + 1 < len(tokens) and tokens[end + 1][2] in ("=", "in")
			if pattern:
				for parameter in binding_indices(tokens, pairs, index + 2, end, object_pattern=following == "{"):
					yield parameter, None
			else:
				position = index + 2
				while position < end:
					if tokens[position][1] in Name and tokens[position + 1][2] in ("=", ":"):
						if position == index + 2 or tokens[position - 1][2] == ";" or "\n" in code[tokens[position - 1][0]:tokens[position][0]]:
							yield position, None
					position = max(position, pairs.get(position, position)) + 1
		if value == "lazy" and following == "(" and pairs.get(index + 1) == index + 3 and tokens[index + 2][1] in Name:
			yield index + 2, None
		if value in ("fn", "constructor", "init", "catch", "operator", "extern", "get", "set"):
			position = index + 1
			while position < len(tokens) and "\n" not in code[offset:tokens[position][0]] and tokens[position][2] not in ("(", "{", "=", ";"):
				position += 1
			if position in pairs and tokens[position][2] == "(":
				for parameter in binding_indices(tokens, pairs, position + 1, pairs[position]):
					yield parameter, None
		if value == "extern" and index and tokens[index - 1][2] == "import":
			start = index + (2 if following == "{" else 1)
			end = pairs.get(index + 1, len(tokens)) if following == "{" else len(tokens)
			for current in range(start, end):
				if tokens[current][2] == "from":
					break
				if tokens[current][2] == "as" and current + 1 < end:
					yield current + 1, None
				if tokens[current][1] in Name and current + 1 in pairs and tokens[current + 1][2] == "(":
					yield current, None
					for parameter in binding_indices(tokens, pairs, current + 2, pairs[current + 1]):
						yield parameter, None
		if value in ("goto", "break", "continue") and tokens[index + 1][1] in Name:
			if "\n" not in code[offset:tokens[index + 1][0]]:
				yield index + 1, None
		if value == "=>" and index:
			previous = index - 1
			annotation_end = previous
			while annotation_end > 0 and tokens[annotation_end][2] in ("]", "?"):
				annotation_end = pairs.get(annotation_end, annotation_end) - 1
			if tokens[annotation_end][1] in Name and annotation_end and tokens[annotation_end - 1][2] == ":":
				previous = annotation_end - 2
			if previous in pairs and tokens[previous][2] == ")":
				for parameter in binding_indices(tokens, pairs, pairs[previous] + 1, previous):
					yield parameter, None
			elif previous == index - 1 and tokens[previous][1] in Name:
				yield previous, None
		if value in ("data", "enum"):
			for opening in range(index + 2, len(tokens)):
				if tokens[opening][2] == "{" and opening in pairs:
					end = pairs[opening]
					current = opening + 1
					while current < end:
						if tokens[current][1] in Name and (current == opening + 1 or tokens[current - 1][2] in (";", ",")
								or "\n" in code[tokens[current - 1][0]:tokens[current][0]]):
							yield current, None
							if current + 1 in pairs and tokens[current + 1][2] == "(":
								for parameter in binding_indices(tokens, pairs, current + 2, pairs[current + 1]):
									yield parameter, None
						current = max(current, pairs.get(current, current)) + 1
					break
				if tokens[opening][2] in (";", "}"):
					break


PROOF_WORDS = {"admit", "all", "by", "exact", "generalizing", "induction", "refl", "reverse", "rewrite", "simp"}
GRAMMAR_WORDS = {"rule", "skip", "start", "token"}



def embedded_words(tokens, pairs, local_names):
	"""Recognize the syntax and binding boundaries of built-in and library blocks."""
	dialects = {"shell", "eir", "prove", "calc", "grammar", "rules", "search", "query", "rowQuery", "batch"}
	for index, (_, _, value) in enumerate(tokens[:-1]):
		if value == "@bounded" and index + 1 in pairs and tokens[index + 1][2] == "(":
			for position in range(index + 2, pairs[index + 1]):
				if tokens[position][2] == "O" and position + 1 in pairs and tokens[position + 1][2] == "(":
					for term in range(position, pairs[position + 1] + 1):
						yield term, False
		if value not in dialects or value in local_names:
			continue
		opening = index + 1
		if opening in pairs and tokens[opening][2] == "(":
			end = pairs[opening]
			if value in ("query", "rowQuery"):
				for parameter in binding_indices(tokens, pairs, opening + 1, end):
					yield parameter, True
			if value == "eir":
				for position in range(opening + 1, end):
					if tokens[position][1] in Name and tokens[position + 1][2] == "=":
						yield position, False
			opening = end + 1
			if value == "eir" and opening < len(tokens) and tokens[opening][2] == ":":
				opening += 1
				while opening < len(tokens) and tokens[opening][2] not in ("{", ";", "}"):
					opening += 1
		if opening not in pairs or tokens[opening][2] != "{":
			continue
		body = range(opening + 1, pairs[opening])
		if value in ("shell", "eir"):
			for position in body:
				yield position, False
		elif value in ("rules", "search"):
			position = body.start
			while position < body.stop:
				word = tokens[position][2]
				if word == "$" and position + 1 in pairs and tokens[position + 1][2] == "(":
					position = pairs[position + 1] + 1
					continue
				if position == body.start or tokens[position - 1][2] != "as":
					yield position, False
				position += 1
		elif value == "batch":
			for position in body:
				if tokens[position][2] == "keep" and tokens[position + 1][2] == "(":
					yield position, False
		elif value in ("query", "rowQuery"):
			for position in body:
				if tokens[position][2] in ("where", "select", "orderBy", "groupBy"):
					yield position, False
				if tokens[position][2] == "from" and position + 2 in body and tokens[position + 2][2] == "in":
					yield position + 1, True
		elif value in ("prove", "calc"):
			for position in body:
				word = tokens[position][2]
				if word in PROOF_WORDS or tokens[position - 1][2] == "?":
					yield position, False
				if word != "case":
					continue
				binder = position + 2
				while binder + 1 in body and tokens[binder][2] == ".":
					binder += 2
				while binder in body and tokens[binder][2] != "{":
					if tokens[binder][1] in Name:
						yield binder, True
					binder += 1
		elif value == "grammar":
			for position in body:
				word = tokens[position][2]
				if word in GRAMMAR_WORDS:
					yield position, False
				if word in ("rule", "token") and position + 1 in body and tokens[position + 1][1] in Name:
					yield position + 1, True



def external_names(stream, catalog, source, report):
	"""Read typed external bindings from the leading comments of this block."""
	names = {}
	annotations = []
	header = True
	for kind, value, start, _ in stream:
		if kind == "space":
			continue
		if kind not in ("comment", "doc"):
			header = False
			continue
		marker = _source_docs.EXTERNAL_DIRECTIVE.match(value)
		if not marker:
			continue
		try:
			if not header:
				raise DocumentationError("use a leading // @external comment")
			declared = _source_docs.external_declarations(marker[1])
		except DocumentationError as error:
			if report:
				report(start, str(error))
			continue
		for name, value_type, offset in declared:
			binding = catalog.library_exports.get(name) or catalog.environment.get(name)
			if binding is not None:
				if report:
					location = f" ({binding['source']}:{binding['line']})" if binding.get("source") and binding.get("line") else ""
					report(start, f"external name {name!r} conflicts with a standard library export{location}")
				continue
			names[name] = Target("", value_type=value_type)
			annotations.append((start + marker.start(1) + offset, value_type))
	targets = {}
	for start, expression in annotations:
		tokens = _source_docs.type_tokens(expression)
		for index, (kind, name, offset, end) in enumerate(tokens):
			if kind != "code" or not name.isidentifier():
				continue
			if index + 1 < len(tokens) and tokens[index + 1][1] == ":":
				continue
			if name in names or index and tokens[index - 1][1] in (".", "?."):
				continue
			if target := catalog.external_type(name, source):
				targets[start + offset] = (end - offset, target)
	return names, targets


def guarded_receivers(code, tokens, pairs, declaration_counts):
	"""Find receivers dominated by a simple positive type test."""
	guards = {}
	for index, (_, _, value) in enumerate(tokens):
		if value != "if" or pairs.get(index + 1) != index + 5 or index + 6 >= len(tokens):
			continue
		_, left_kind, name = tokens[index + 2]
		_, right_kind, _ = tokens[index + 4]
		if (tokens[index + 1][2] != "(" or tokens[index + 3][2] != "is"
				or left_kind not in Name or right_kind not in Name or declaration_counts[name] > 1):
			continue
		start = index + 6
		end = pairs.get(start) if tokens[start][2] == "{" else None
		if end is None:
			end = start
			while end < len(tokens) and tokens[end][2] not in ("else", ";", "}", ")", "]"):
				end = pairs.get(end, end) + 1
				if end < len(tokens) and "\n" in code[tokens[end - 1][0]:tokens[end][0]]:
					break
		for position in range(start, min(end, len(tokens) - 1)):
			_, _, spelling = tokens[position]
			following = tokens[position + 1][2]
			if spelling in ("fn", "class", "=>") or spelling == name and following in (
					"=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "??=", "++", "--"):
				break
			if spelling == name and following in (".", "?.") and tokens[position - 1][2] not in (".", "?."):
				guards[position] = index + 4
	return guards


def code_targets(code, catalog, source=None, *, report=None, setup=""):
	"""Return source offsets for names whose documentation target is known.

	Bindings declared anywhere in a fragment suppress default lookup throughout
	that fragment. This deliberately forgoes some valid links in nested scopes.
	"""
	try:
		stream = list(source_tokens(code))
		opaque = [(start, end) for kind, _, start, end in stream if kind in ("literal", "comment", "doc")]
	except DocumentationError as error:
		if report:
			report(0, str(error))
		return {}
	opaque_starts = [start for start, _ in opaque]

	def is_opaque(offset):
		index = bisect_right(opaque_starts, offset) - 1
		return index >= 0 and offset < opaque[index][1]

	if setup:
		header_end = next((start for kind, _, start, _ in stream if kind in ("code", "literal")), len(code))
		# The setup's own external declarations belong to its separately checked example.
		prefix = "\n".join(line for line in setup.splitlines() if not _source_docs.EXTERNAL_DIRECTIVE.match(line.lstrip()))
		insertion = "\n" + prefix + "\n"
		resume = header_end + len(insertion)

		def member_offset(offset):
			if offset < header_end:
				return offset
			return offset - len(insertion) if offset >= resume else None

		def member_report(offset, message):
			position = member_offset(offset)
			if position is not None:
				report(position, message)

		combined = code[:header_end] + insertion + code[header_end:]
		targets = code_targets(combined, catalog, source, report=member_report if report else None)
		return {position: target for offset, target in targets.items() if (position := member_offset(offset)) is not None}

	if report:
		check_delimiters(stream, report)
	tokens = [(offset, kind, value) for offset, kind, value in get_lexer_by_name("el").get_tokens_unprocessed(code)
		if kind not in Comment and kind not in Whitespace and not (kind in Text and value.isspace())]
	comprehensions = set(comprehension_offsets([token for token in stream if token[0] in ("code", "literal")]))
	bindings = dict(catalog.defaults)
	local_types = defaultdict(set)
	structure = " ".join(value if kind not in String else "STRING" for _, kind, value in tokens)
	prelude = not re.search(r"@(module|runtime)\s*\([^)]*\bprelude\s*:\s*f\b", structure)
	if not prelude:
		bindings.clear()
	externals, result = external_names(stream, catalog, source, report)
	bindings.update(externals)
	imported_bindings = {}
	namespaces = {}
	external_patterns = []
	declarations = set()
	declaration_counts = defaultdict(int)
	ignored = set()
	for specification in code_imports(stream):
		for offset, _, _ in tokens:
			if offset >= specification.end:
				break
			if offset >= specification.start:
				ignored.add(offset)
		uri = specification.uri
		standard_module = uri and uri.startswith("el:")
		module = catalog.module(uri) if standard_module else None
		if report and standard_module and module is None:
			report(specification.start, f"standard library module {uri!r} does not exist in the API catalog")
		for name, alias, offset in specification.names:
			binding = module.get(name) if module is not None else None
			bindings[alias] = catalog.binding_target(binding) if binding else None
			if report and module is not None:
				problem = export_problem(binding, name, uri)
				if problem:
					report(offset, problem)
		if specification.pattern is None:
			continue
		try:
			selector = re.compile(specification.pattern)
		except re.error:
			# EL regex syntax can differ from the Python pattern subset.
			if specification.namespace:
				bindings[specification.namespace] = None
			continue
		if specification.namespace:
			bindings[specification.namespace] = None
			if module is not None:
				namespaces[specification.namespace] = (uri, module, selector)
		elif module is not None:
			for name, binding in module.items():
				if selector.search(name):
					bindings[name] = catalog.binding_target(binding)
					imported_bindings[name] = (uri, binding)
		else:
			external_patterns.append(selector)
	ignored.update(offset for offset, _, _ in tokens if is_opaque(offset))
	for directive in re.finditer(r"(?m)^[ \t]*#[^\n]*", code):
		if is_opaque(directive.start()):
			continue
		ignored.update(offset for offset, _, _ in tokens if directive.start() <= offset < directive.end())
		definition = re.match(r"[ \t]*#define\s+(\w+)", directive[0])
		if definition:
			bindings[definition[1]] = None
	pairs = paired_tokens(tokens, ignored)
	for position, type_name in local_declarations(code, tokens, ignored, pairs):
		offset, _, name = tokens[position]
		bindings[name] = None
		if offset not in declarations:
			declaration_counts[name] += 1
		declarations.add(offset)
		local_types[name].add(type_name)
	for position, declaration in embedded_words(tokens, pairs, local_types):
		offset, _, name = tokens[position]
		ignored.add(offset)
		if declaration:
			bindings[name] = None
			local_types[name].add(None)
	type_stream = [token for token in stream if token[0] in ("code", "literal")]
	type_values = [value if kind == "code" else "" for kind, value, _, _ in type_stream]
	hints = {name: value for name, value in catalog.value_hints.items() if "." in name}
	for name, target in bindings.items():
		if target is None:
			continue
		if return_type := catalog.value_hints.get(target.label + "()"):
			hints[name + "()"] = return_type
		elif target.value_type:
			hints[name] = target.value_type
	for name, value_type in catalog.module_hints.get(source, {}).items():
		binding = name.removesuffix("()")
		if "." in name or binding not in bindings or binding in catalog.defaults and bindings[binding] is catalog.defaults[binding]:
			hints[name] = value_type

	constructors = {name for name in catalog.constructors if bindings.get(name) is not None}
	constructors.update(type_values[index + 1] for index, value in enumerate(type_values[:-1]) if value == "class")
	local_returns = _source_docs.simple_function_returns(code, type_stream, type_values, hints, constructors)
	for offset, name, value_type in _source_docs.inferred_bindings(code, type_stream, type_values, hints | local_returns, constructors):
		if offset in declarations and declaration_counts[name] == 1 and local_types[name] == {None}:
			local_types[name] = {value_type}

	guards = guarded_receivers(code, tokens, pairs, declaration_counts)
	resolved = {}
	for index, (offset, kind, value) in enumerate(tokens):
		if offset in declarations or offset in ignored:
			continue
		previous = tokens[index - 1][2] if index else ""
		following = tokens[index + 1][2] if index + 1 < len(tokens) else ""
		if value == ")" and index in pairs:
			opening = pairs[index]
			if opening and tokens[opening][2] == "(":
				callee = resolved.get(opening - 1)
				if callee and callee.value_type:
					resolved[index] = callee
		if report and value in ("&&", "||"):
			report(offset, f"{value!r} is not an EL operator; use {value[0]!r}")
		if report and value in ("let", "const") and following == "=":
			report(offset, f"{value!r} requires a binding before '='")
		target = None
		is_introducer = value in ("get", "set", "syntax") and index + 1 < len(tokens) and tokens[index + 1][1] in Name
		if (kind in Keyword or kind in Name.Decorator or is_introducer) and value in LANGUAGE:
			path = COMPREHENSION_REFERENCE if offset in comprehensions else "reference/language/" + LANGUAGE[value] + ".md"
			target = Target(path, label=value)
		elif (kind in Name and kind not in Name.Decorator) or kind in Keyword.Constant:
			if value in ("noescape", "noescape_when_void") and index >= 2 and previous == "<" and tokens[index - 2][2] == "ptr":
				continue
			if following == "-" and code[offset + len(value):].startswith("-"):
				if re.match(r"-\w+:\s*[\"']", code[offset + len(value):]):
					continue
			if previous in (".", "?."):
				receiver = tokens[index - 2][2] if index >= 2 else None
				if receiver in namespaces and receiver not in local_types:
					uri, module, selector = namespaces[receiver]
					binding = module.get(value) if selector.search(value) else None
					target = catalog.binding_target(binding) if binding else None
					problem = export_problem(binding, value, uri)
					if report and problem:
						report(offset, problem)
				else:
					target = catalog.member(resolved.get(index - 2), value)
			elif index and tokens[index - 1][1] in Number and tokens[index - 1][0] + len(previous) == offset:
				continue  # The spelling may be a quantity literal.
			elif following != ":" or previous in ("let", "const"):
				target = bindings.get(value)
				if value in local_types:
					if target is None and len(local_types[value]) == 1:
						value_type = local_returns.get(value + "()") if following == "(" else None
						target = Target("", value_type=value_type or next(iter(local_types[value])))
				elif report and value not in BUILTIN_NAMES:
					if value in imported_bindings:
						uri, binding = imported_bindings[value]
						problem = export_problem(binding, value, uri)
					elif prelude and value in catalog.environment and target is catalog.defaults[value]:
						problem = export_problem(catalog.environment[value], value, "the standard library prelude")
					elif value not in bindings and not any(selector.search(value) for selector in external_patterns):
						binding = catalog.library_exports.get(value)
						problem = export_problem(binding, value, "the standard library")
					else:
						problem = None
					if problem:
						report(offset, problem)
				if following == "(" and value not in local_types and (return_type := hints.get(value + "()")):
					if target is None:
						target = Target("", value_type=return_type)
					elif target.value_type != return_type:
						target = Target(target.path, target.fragment, target.label, return_type)
		if target:
			resolved[index] = target
		if index in guards:
			guard = resolved.get(guards[index])
			if guard and guard.path and guard.label in catalog.names:
				resolved[index] = Target("", value_type=guard.label)
		if target and target.path:
			result[offset] = (len(value), target)
	for offset, (length, target) in catalog.type_targets(code, source).items():
		if target:
			result[offset] = (length, target)
		else:
			result.pop(offset, None)
	return result


class CodeLinker(HTMLParser):
	def __init__(self, html, catalog, url_for, source=None, report=None):
		super().__init__(convert_charrefs=False)
		self.html = html
		self.catalog = catalog
		self.url_for = url_for
		self.source = source
		self.report = report
		self.block = 0
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
		language = next((value for value in classes if value in
			("language-el", "language-els", "language-evil", "language-el-signature")), None)
		active = language or (self.stack[-1][1] if self.stack else None)
		if tag not in ("br", "hr", "img", "input", "meta", "link", "wbr", "source"):
			self.stack.append((tag, active))
		if tag == "code" and active:
			self.block += 1
			self.code = {"text": "", "parts": [], "linked": False, "link_depth": 0, "language": active}
		elif self.code is not None and tag == "a":
			self.code["link_depth"] += 1

	def handle_startendtag(self, tag, attrs):
		pass

	def handle_endtag(self, tag):
		if tag == "a" and self.code is not None:
			self.code["link_depth"] -= 1
		if tag == "code" and self.code is not None:
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
		def report(offset, message):
			code = self.code["text"]
			line = code.count("\n", 0, offset) + 1
			column = offset - code.rfind("\n", 0, offset)
			self.report(f"EL block {self.block}:{line}:{column}: {message}")

		code = self.code["text"]
		setup = self.catalog.example_setup(self.source, code) if self.source else ""
		targets = code_targets(code, self.catalog, self.source, setup=setup,
			report=report if self.report and self.code["language"] != "language-el-signature" else None)
		if self.code["linked"]:
			return
		for start, raw_start, raw, decoded in self.code["parts"]:
			pieces = []
			cursor = 0
			for offset, (length, target) in sorted(targets.items()):
				if start <= offset and offset + length <= start + len(decoded):
					local = offset - start
					pieces.append(escape(decoded[cursor:local], quote=False))
					url = escape(self.url_for(target), quote=True)
					label = escape("查看 " + target.label + " 的参考文档", quote=True)
					pieces.append(f'<a class="el-code-link" href="{url}" aria-label="{label}">{escape(decoded[local:local + length])}</a>')
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
	_source_docs.validate_module_docs(model["entries"])
	_source_docs.validate_member_examples(model["entries"], model.get("types", []), model.get("module_return_types"))
	_catalog = Catalog(model)
	_files = {file.src_uri: file.url for file in files}
	_destinations = {file.src_uri: file.abs_dest_path for file in files}
	_used_targets.clear()
	# Fail the build for stale reference destinations, including handwritten ones.
	language_paths = {"reference/language/" + name + ".md" for name in LANGUAGE.values()}
	for path in language_paths | {COMPREHENSION_REFERENCE}:
		if path not in _files:
			raise ValueError(f"missing code reference destination: {path}")
	return files


def on_page_content(html, page, config, files, *, diagnostics=None):
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
	problems = [] if diagnostics is None else diagnostics
	result = CodeLinker(html, _catalog, url_for, source,
		lambda message: problems.append(f"{uri}: {message}")).render()
	if diagnostics is None and problems:
		raise DocumentationError("\n".join(problems))
	return result


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
	diagnostics = []
	for file in files:
		path = Path(file.abs_dest_path)
		original = path.read_text(encoding="utf-8")
		linked = on_page_content(original, SimpleNamespace(url=file.url, file=file), config, files, diagnostics=diagnostics)
		if linked != original:
			_source_docs.atomic_write(path, linked)
			changed += 1
	if diagnostics:
		raise DocumentationError("\n".join(diagnostics))
	on_post_build(config)
	return {"linked_pages": changed, "validated_links": validate_site(site_dir)}
