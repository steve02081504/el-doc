from html import unescape
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import unittest

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hooks.el_lexer
from hooks.code_links import Catalog, CodeLinker, anchor, code_targets, validate_site


def entry(name, value_type=None, return_type=None, source="console/facade.el"):
	return {"kind": "api", "id": source.removesuffix(".el") + "::" + name,
		"name": name, "source": source, "value_type": value_type, "return_type": return_type}


def catalog():
	return Catalog({"entries": [entry("console", "ConsoleFacade"),
		entry("ConsoleFacade.stdout", return_type="ConsolePort"),
		entry("ConsoleFacade.info", return_type="ConsoleLevelPort"),
		entry("ConsolePort.writeLine", return_type="Number"),
		entry("ConsoleLevelPort.value~snapshot"), entry("ConsoleLevelPort.value~value"),
		entry("capture")], "environment": [
		{"name": "console", "id": "console/facade::console", "source": "console/facade.el"},
		{"name": "Number", "id": None, "source": "numerics/number.el", "value_type": None},
		{"name": "unknown", "id": None, "source": None}],
		"exports": {
			"console/facade": {"console": {"id": "console/facade::console"}},
			"console/index": {"console": {"id": "console/facade::console"},
				"capture": {"id": "console/facade::capture"}, "silent": {"id": None, "source": "console/facade.el", "line": 10}}}})


class CodeLinkTests(unittest.TestCase):
	def setUp(self):
		self.catalog = catalog()

	def test_hook_loads_without_repository_on_python_path(self):
		script = '''import importlib.util, sys
spec = importlib.util.spec_from_file_location("standalone_code_links", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
'''
		with tempfile.TemporaryDirectory() as directory:
			result = subprocess.run([sys.executable, "-I", "-c", script,
				str(Path(__file__).resolve().parents[1] / "hooks/code_links.py")],
				cwd=directory, capture_output=True, text=True)
		self.assertEqual(result.returncode, 0, result.stderr)

	def names(self, code):
		return {code[offset:offset + length]: target for offset, (length, target) in code_targets(code, self.catalog).items()}

	def test_highlighting_reports_missing_and_undocumented_exports(self):
		code = ('import { absent, silent as quiet } from "el:console/"\n'
			'import /.*/ as outputs from "el:console/"\n'
			'console.stdout.writeLine(missing)\nNumber\noutputs.silent\n'
			'let local = 1\nlocal\nquiet\noutputs.capture')
		problems = []
		targets = code_targets(code, self.catalog, report=lambda offset, message: problems.append((offset, message)))
		self.assertEqual([code[offset:].split()[0].strip(",)") for offset, _ in problems],
			["absent", "silent", "missing", "Number", "silent"])
		self.assertIn("is not exported", problems[0][1])
		self.assertIn("has no API documentation (console/facade.el:10)", problems[1][1])
		self.assertIn("capture", {target.label for _, target in targets.values()})

	def test_directory_import_requires_a_real_directory_entry(self):
		for uri in ("el:console/", "el:console", "el:console/index.el"):
			with self.subTest(uri=uri):
				problems = []
				code_targets(f'import {{ capture }} from "{uri}"', self.catalog,
					report=lambda _, message: problems.append(message))
				self.assertEqual(problems, [])
		problems = []
		code_targets('import { console } from "el:console/facade/"', self.catalog,
			report=lambda _, message: problems.append(message))
		self.assertEqual(problems, ["standard library module 'el:console/facade/' does not exist in the API catalog"])

	def test_external_names_are_explicit_and_block_local(self):
		blocks = [
			'<pre class="language-el"><code>// @external SampleNat: type, sampleZero: SampleNat\nfn make(): SampleNat =&gt; sampleZero\nunknown</code></pre>',
			'<pre class="language-el"><code>SampleNat\n// @external SampleNat: type\nsampleZero</code></pre>',
		]
		problems = []
		CodeLinker("".join(blocks), self.catalog, lambda _: "", report=problems.append)
		self.assertEqual(len(problems), 4)
		self.assertIn("'unknown' is exported", problems[0])
		self.assertIn("leading // @external", problems[1])
		self.assertIn("'SampleNat' is not exported", problems[2])
		self.assertIn("'sampleZero' is not exported", problems[3])

	def test_external_diagnostic_requires_types(self):
		code = '// @external window, label\nwindow.every(1000, tick => label.text = "tick")'
		problems = []
		code_targets(code, self.catalog, report=lambda _, message: problems.append(message))
		self.assertIn("each external needs a type", problems[0])

	def test_external_types_can_contain_commas(self):
		code = '// @external dataset: Map<key: Text, value: Number>, formatRow: fn(Text, Number): Text\nformatRow(dataset, 1)'
		problems = []
		code_targets(code, self.catalog, report=lambda _, message: problems.append(message))
		self.assertEqual(problems, [])

	def test_external_type_links_and_members_follow_known_types(self):
		cursor = entry("SearchCursor", source="logic/search.el")
		next_method = entry("SearchCursor.next", source="logic/search.el")
		catalog = Catalog({"entries": [cursor, next_method],
			"types": [{"name": "SearchCursor", "source": cursor["source"], "id": cursor["id"]}]})
		html = '<pre class="language-el"><code><span class="c1">// @external cursor: SearchCursor&lt;element: SearchCursor&gt;</span>\ncursor.next()</code></pre>'
		result = CodeLinker(html, catalog, lambda target: "#" + target.fragment).render()
		self.assertEqual(result.count('>SearchCursor</a>'), 2)
		self.assertRegex(result, rf'href="#{anchor(next_method["id"])}"[^>]*>next</a>')
		self.assertNotIn('>cursor</a>', result)

	def test_discard_uses_standard_library_documentation(self):
		discard = entry("discard", source="language/value-operations.el")
		binding = {"name": "discard", "source": discard["source"], "line": 10}
		for documented in (False, True):
			with self.subTest(documented=documented):
				catalog = Catalog({"entries": [discard] if documented else [],
					"environment": [{**binding, "id": discard["id"] if documented else None}]})
				problems = []
				targets = code_targets("discard(1)", catalog, report=lambda _, message: problems.append(message))
				if documented:
					self.assertEqual(targets[0][1].fragment, anchor(discard["id"]))
					self.assertEqual(problems, [])
				else:
					self.assertEqual(problems, ["'discard' is exported by the standard library prelude but has no API documentation (language/value-operations.el:10)"])

	def test_type_guard_links_only_in_the_true_branch(self):
		error = entry("SearchInterrupted", source="logic/control.el")
		reason = entry("SearchInterrupted.reason", source=error["source"])
		catalog = Catalog({"entries": [error, reason], "environment": [{"name": error["name"], "id": error["id"]}]})
		for body in ("discard(error.reason)", "{ discard(error.reason); error = other; discard(error.reason) }"):
			with self.subTest(body=body):
				code = f"try {{ run() }} catch (error) {{ if (error is SearchInterrupted) {body} else discard(error.reason)\nerror.reason }}"
				targets = code_targets(code, catalog)
				self.assertEqual([offset for offset, (_, target) in targets.items() if target.label == reason["name"]],
					[code.index("reason")])

	def test_typed_catch_members_follow_each_handlers_annotation(self):
		first = entry("FirstError", source="errors.el")
		second = entry("SecondError", source="errors.el")
		first_reason = entry("FirstError.reason", source="errors.el")
		second_reason = entry("SecondError.reason", source="errors.el")
		catalog = Catalog({"entries": [first, second, first_reason, second_reason],
			"environment": [{"name": second["name"], "id": second["id"]}],
			"exports": {"errors": {"FirstError": {"id": first["id"]}}}})
		code = (
			'import { FirstError as NamedError } from "el:errors.el"\n'
			'try { error.reason }\n'
			'catch (error: NamedError) { error.reason }\n'
			'catch (error: SecondError) { error.reason }\n'
			'catch (error) { error.reason }\n'
			'finally { error.reason }\n'
			'error.reason')
		targets = code_targets(code, catalog)
		self.assertEqual(
			{offset: target.label for offset, (_, target) in targets.items() if target.label.endswith(".reason")},
			{code.index("reason", code.index("catch")): first_reason["name"],
				code.index("reason", code.index("catch (error: SecondError)")): second_reason["name"]})

	def test_externals_cannot_mask_exports_even_outside_the_prelude(self):
		code = '// @external silent: Text, capture: Text, Number: type\nlet value = 1'
		problems = []
		code_targets(code, self.catalog, report=lambda _, message: problems.append(message))
		self.assertEqual(problems, [
			"external name 'silent' conflicts with a standard library export (console/facade.el:10)",
			"external name 'capture' conflicts with a standard library export",
			"external name 'Number' conflicts with a standard library export",
		])

	def test_external_name_does_not_hide_unsupported_stdlib_import(self):
		code = '// @external missing: Number\nimport { missing } from "el:console/"\nmissing()'
		problems = []
		code_targets(code, self.catalog, report=lambda _, message: problems.append(message))
		self.assertEqual(problems, ["'missing' is not exported by el:console/"])

	def test_highlighting_reports_unbalanced_syntax(self):
		problems = []
		code_targets('console.stdout.writeLine("ignored )"', self.catalog,
			report=lambda _, message: problems.append(message))
		self.assertEqual(problems, ["missing ')'"])

	def test_highlighting_reports_invalid_binding_and_operator(self):
		problems = []
		code_targets('let = 1\n1 && 2', self.catalog, report=lambda _, message: problems.append(message))
		self.assertEqual(problems, ["'let' requires a binding before '='", "'&&' is not an EL operator; use '&'"])

	def test_embedded_rules_check_names_in_el_splices(self):
		code = "// @external rules: type\nlet table = rules {\n relation edge(source, target) from $(missing)\n}"
		problems = []
		code_targets(code, self.catalog, report=lambda _, message: problems.append(message))
		self.assertEqual(problems, ["'missing' is not exported by the standard library"])

	def test_factory_results_link_on_direct_calls_and_local_bindings(self):
		definition = entry("makePort", return_type="ConsolePort")
		definition["signature"] = "export fn makePort()"
		method = entry("ConsolePort.writeLine")
		model = {"entries": [definition, method], "environment": [{"name": "makePort", "id": definition["id"]}]}
		code = 'fn setup() => makePort()\nlet output = setup()\nsetup().writeLine("first")\noutput.writeLine("second")'
		links = code_targets(code, Catalog(model))
		self.assertEqual([code[start:start + size] for start, (size, target) in links.items() if target.label.endswith(".writeLine")],
			["writeLine", "writeLine"])

	def test_member_setup_is_scoped_to_the_class_documentation(self):
		owner = entry("Window", source="window.el")
		owner.update(signature="export class Window", sections=[{"tag": "example", "code": "let demoWindow = Window()\n"}])
		method = entry("Window.every", source="window.el")
		method.update(owner="Window", signature="fn every()", sections=[{"tag": "example", "code": "demoWindow.every()\nunused\n"}])
		model = {"entries": [owner, method], "types": [{"name": "Window"}], "environment": [{"name": "Window", "id": owner["id"]}]}
		html = '<pre class="language-el"><code>demoWindow.every()\nunused\n</code></pre>'
		problems = []
		result = CodeLinker(html, Catalog(model), lambda target: target.path, "window.el", problems.append).render()
		self.assertIn('>every</a>', result)
		self.assertNotIn('let demoWindow', result)
		self.assertEqual(problems, ["EL block 1:2:1: 'unused' is not exported by the standard library"])
		problems = []
		CodeLinker(html, Catalog(model), lambda _: "", "other.el", problems.append)
		self.assertIn("'demoWindow' is not exported", problems[0])

	def test_member_chain_uses_declared_types(self):
		targets = self.names('console.stdout.writeLine("hello")')
		self.assertEqual(set(targets), {"console", "stdout", "writeLine"})
		self.assertEqual(targets["stdout"].fragment, anchor("console/facade::ConsoleFacade.stdout"))
		self.assertEqual(targets["writeLine"].fragment, anchor("console/facade::ConsolePort.writeLine"))

	def test_overloads_link_to_family(self):
		targets = self.names('console.info.value(@{ count: 3 })')
		self.assertEqual(targets["value"].fragment, anchor("console/facade::ConsoleLevelPort.value"))

	def test_import_alias_uses_exact_module(self):
		code = 'import { console as output } from "el:console/facade.el"\noutput.stdout.writeLine("hello")'
		self.assertIn("writeLine", self.names(code))
		self.assertEqual(self.names(code)["output"].fragment, anchor("console/facade::console"))
		self.assertNotIn("output", self.names(code.replace("el:console/facade.el", "file:./mine.el")))
		self.assertIn("writeLine", self.names(code.replace("el:console/facade.el", "el:console/")))
		self.assertIn("capture", self.names('import { capture } from "el:console/"\ncapture(work)'))

	def test_shadowed_defaults_and_parameters_stay_plain(self):
		for code in [
			'let console = custom\nconsole.stdout.writeLine("hello")',
			'fn show(console) { console.stdout.writeLine("hello") }',
			'let show = console => console.stdout.writeLine("hello")',
			'let show = (console, other) => console.stdout.writeLine("hello")',
			'import { console } from "file:./mine.el"\nconsole.stdout.writeLine("hello")',
		]:
			with self.subTest(code=code):
				self.assertNotIn("console", self.names(code))
				self.assertNotIn("writeLine", self.names(code))

	def test_strings_comments_raw_and_templates_stay_plain(self):
		for code in ['"console.stdout.writeLine"', '// console.stdout.writeLine',
			'/* console.stdout.writeLine */', '##"raw "console.stdout.writeLine" text"##',
			'`console ${console.stdout.writeLine("hello")}`']:
			with self.subTest(code=code):
				self.assertNotIn("writeLine", self.names(code))

	def test_unknown_receivers_keys_and_disabled_prelude_stay_plain(self):
		self.assertNotIn("writeLine", self.names('object.writeLine("hello")'))
		self.assertNotIn("console", self.names('@{ console: "hello" }'))
		self.assertNotIn("console", self.names('@module(prelude: f)\nconsole.stdout.writeLine("hello")'))
		self.assertIn("Number", self.names("let count: Number = 3"))

	def test_keywords_link_to_reference_pages(self):
		self.assertEqual(self.names("if condition { return value }")["if"].path, "reference/language/control-flow.md")
		self.assertEqual(self.names('@assign(mode: "copy")')["@assign"].path, "reference/language/assignment-semantics.md")

	def test_for_links_follow_the_syntax_at_each_occurrence(self):
		code = """for let row in rows {
	let array = @[@[row, column] for let column in row
		for let value in column]
	let lazy = (row /* ] ) */ for let row in rows)
	consume(##"[( "for let ignored in fake"## for let row in rows)
}
fn show(rows) {
	for (let row in rows) {
		consume(row)
		for let item in row consume(item)
	}
}
consume(fn() { for let row in rows consume(row) })
"""
		targets = code_targets(code, self.catalog)
		self.assertEqual(
			[target.path for offset, (length, target) in targets.items() if code[offset:offset + length] == "for"],
			["reference/language/" + page + ".md" for page in (
				"control-flow", "comprehensions", "comprehensions", "comprehensions",
				"comprehensions", "control-flow", "control-flow", "control-flow")],
		)

	def test_signature_types_follow_defining_module_not_default_names(self):
		definition = entry("lookup", source="custom.el")
		definition.update(signature="fn lookup(): Number | ptr", return_type="Number | ptr", type_references={"return_type": [
			{"name": "Number", "start": 0, "end": 6, "target": {"type": "definition", "path": "types.md", "fragment": "custom-number"}},
			{"name": "ptr", "start": 9, "end": 12, "target": {"type": "builtin", "path": "reference/language/foreign.md", "fragment": None}}]})
		other = {**definition, "source": "other.el", "id": "other::lookup", "type_references": {"return_type": []}}
		model = {"entries": [definition, other], "environment": [{"name": "Number", "id": None, "source": None}]}
		catalog = Catalog(model)
		targets = code_targets(definition["signature"], catalog, "custom.el")
		self.assertEqual(targets[13][1].fragment, "custom-number")
		self.assertEqual(targets[22][1].path, "reference/language/foreign.md")

	def test_rendered_site_validator_checks_real_targets_and_fragments(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "index.html").write_text('<a href="type/#number">Number</a>', encoding="utf-8")
			(root / "type").mkdir()
			(root / "type/index.html").write_text('<h1 id="number">Number</h1>', encoding="utf-8")
			self.assertEqual(validate_site(root), 1)
			(root / "type/index.html").write_text('<h1 id="other">Other</h1>', encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "missing site anchor"):
				validate_site(root)

	def test_identical_member_signatures_share_only_identical_type_targets(self):
		one = entry("First.channel", source="ports.el")
		one.update(signature="get channel(): Channel", return_type="Channel", type_references={"return_type": [
			{"name": "Channel", "start": 0, "end": 7, "target": {"type": "definition", "path": "types.md", "fragment": "channel"}}]})
		two = {**one, "id": "ports::Second.channel", "name": "Second.channel"}
		catalog = Catalog({"entries": [one, two], "environment": []})
		self.assertEqual(code_targets(one["signature"], catalog, "ports.el")[15][1].fragment, "channel")
		two = {**two, "type_references": {"return_type": [{"name": "Channel", "start": 0, "end": 7, "target": None}]}}
		catalog = Catalog({"entries": [one, two], "environment": []})
		self.assertNotIn(15, code_targets(one["signature"], catalog, "ports.el"))

	def test_explicitly_typed_local_links_only_members(self):
		code = 'let output: ConsolePort = selected\noutput.writeLine("hello")'
		targets = self.names(code)
		self.assertNotIn("output", targets)
		self.assertEqual(targets["writeLine"].fragment, anchor("console/facade::ConsolePort.writeLine"))
		self.assertNotIn("writeLine", self.names(code + '\nfn test(output) { output.writeLine("hello") }'))
		self.assertNotIn("writeLine", self.names(code.replace("ConsolePort =", "ConsolePort | nil_t =")))

	def test_getter_declarations_do_not_link_to_same_named_defaults(self):
		self.assertNotIn("console", self.names("get console(): Text"))

	def test_highlighted_html_links_preserve_text_and_escaping(self):
		html = markdown.markdown('```el\nconsole.stdout.writeLine("<hello> & world")\n```',
			extensions=["pymdownx.superfences", "pymdownx.highlight"],
			extension_configs={"pymdownx.highlight": {"pygments_lang_class": True, "anchor_linenums": True}})
		linked = CodeLinker(html, self.catalog, lambda target: target.path + "#" + target.fragment).render()
		self.assertEqual(linked.count('class="el-code-link"'), 3)
		plain = lambda content: unescape(re.sub(r"<[^>]+>", "", content))
		self.assertEqual(plain(html), plain(linked))
		self.assertIn('&lt;hello&gt; &amp; world', linked)
		self.assertNotIn('<hello>', linked)
		self.assertEqual(CodeLinker(linked, self.catalog, lambda target: "wrong").render(), linked)

	def test_non_el_and_inline_code_are_unchanged(self):
		for html in ['<code>console.stdout</code>', '<div class="language-text"><pre><code>console.stdout</code></pre></div>',
			'<div class="language-eol"><pre><code>console.stdout</code></pre></div>']:
			self.assertEqual(CodeLinker(html, self.catalog, lambda target: "wrong").render(), html)

	def test_line_number_wrappers_and_multiple_blocks(self):
		html = '<div class="language-el"><pre><code><span id="line-1"><span class="n">console</span></span>.stdout.writeLine()</code></pre></div>'
		linked = CodeLinker(html + html, self.catalog, lambda target: "../api/#" + target.fragment).render()
		self.assertEqual(linked.count('class="el-code-link"'), 6)
		self.assertIn('id="line-1"', linked)


if __name__ == "__main__":
	unittest.main()
