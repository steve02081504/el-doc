from html import unescape
from pathlib import Path
import re
import sys
import unittest

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hooks.el_lexer
from hooks.code_links import Catalog, CodeLinker, anchor, code_targets


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
		"exports": {"console/index": {"console": "console/facade::console", "capture": "console/facade::capture"}}})


class CodeLinkTests(unittest.TestCase):
	def setUp(self):
		self.catalog = catalog()

	def names(self, code):
		return {code[offset:offset + length]: target for offset, (length, target) in code_targets(code, self.catalog).items()}

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
		self.assertNotIn("console", self.names('@module(prelude: nil)\nconsole.stdout.writeLine("hello")'))
		self.assertIn("Number", self.names("let count: Number = 3"))

	def test_keywords_link_to_reference_pages(self):
		self.assertEqual(self.names("if condition { return value }")["if"].path, "reference/language/control-flow.md")
		self.assertEqual(self.names('@assign(mode: "copy")')["@assign"].path, "reference/language/assignment-semantics.md")

	def test_explicitly_typed_local_links_only_members(self):
		code = 'let output: ConsolePort = selected\noutput.writeLine("hello")'
		targets = self.names(code)
		self.assertNotIn("output", targets)
		self.assertEqual(targets["writeLine"].fragment, anchor("console/facade::ConsolePort.writeLine"))
		self.assertNotIn("writeLine", self.names(code + '\nfn test(output) { output.writeLine("hello") }'))
		self.assertNotIn("writeLine", self.names(code.replace("ConsolePort =", "ConsolePort | void_t =")))

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
		self.assertIn('&quot;&lt;hello&gt; &amp; world&quot;', linked)
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
