import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from stdlib_docs import DocumentationError, collect, extract, render, write_pages


DOCUMENT = '''/// @api increment
/// Add one.
/// @param value Input number.
/// @returns The incremented number.
/// @example Increment a number
/// ```el
/// console.stdout.writeLine(increment(2))
/// ```
/// ```text
/// 3
/// ```
export fn increment(value: Number): Number => value + 1
'''


class ExtractionTests(unittest.TestCase):
	def test_module_documentation(self):
		entry, = extract("//! @module Math\n//! Number utilities.\n", "math.el")
		self.assertEqual(entry["kind"], "module")
		self.assertEqual(entry["id"], "math")
		with self.assertRaisesRegex(DocumentationError, "use //!"):
			extract("/// @module Math\n/// Number utilities.\n", "math.el")

	def test_signature_and_example(self):
		entry, = extract(DOCUMENT, "math.el")
		self.assertEqual(entry["signature"], "export fn increment(value: Number): Number")
		self.assertEqual(entry["id"], "math::increment")
		self.assertEqual(entry["declaration_line"], 12)
		self.assertEqual(entry["sections"][-1]["expected_stdout"], "3\n")
		self.assertEqual(entry["sections"][-1]["verification"], "not-run")

	def test_literals_and_ordinary_comments_are_not_documentation(self):
		for source in [
			'let text = "/// @api fake"',
			'let text = ##"\n/// @api fake\n"##',
			'/*\n/// @api fake\n*/',
			'let text = `\n/// @api fake\n${`nested ${"text"}`}\n`',
			'export /[///]+/ from "file:./other.el"',
			'fn f() {} /// @api fake',
		]:
			with self.subTest(source=source):
				self.assertEqual(extract(source, "sample.el"), [])

	def test_multiline_signature_with_attributes_and_defaults(self):
		source = DOCUMENT.replace("export fn increment(value: Number): Number => value + 1", '@bounded(time: "O(1)")\nexport fn increment(\n\tvalue = @{ number: 2 }\n): Number { return value.number + 1 }')
		entry, = extract(source, "math.el")
		self.assertTrue(entry["signature"].endswith("): Number"))
		self.assertIn('@bounded(time: "O(1)")', entry["signature"])

	def test_syntax_declaration(self):
		source = DOCUMENT.replace("export fn increment(value: Number): Number => value + 1", 'export syntax increment { category: Expr }')
		entry, = extract(source, "syntax.el")
		self.assertEqual(entry["signature"], "export syntax increment")

	def test_bad_comments_fail_with_location(self):
		for source in [DOCUMENT.replace("@returns", "@returnz"), DOCUMENT.replace("/// Add one.", "///"), DOCUMENT[:DOCUMENT.index("export fn")], DOCUMENT.replace("/// @api increment", "/// missing marker"), DOCUMENT.replace("/// ```text", "/// ```unknown")]:
			with self.subTest(source=source), self.assertRaisesRegex(DocumentationError, "math.el:1:"):
				extract(source, "math.el")

	def test_preprocessing_is_rejected(self):
		with self.assertRaisesRegex(DocumentationError, "preprocessed"):
			extract("#if FLAG\n" + DOCUMENT + "#endif\n", "math.el")

	def test_mismatched_name_is_rejected(self):
		with self.assertRaisesRegex(DocumentationError, "does not match"):
			extract(DOCUMENT.replace("@api increment", "@api missing"), "math.el")

	def test_cannot_bind_across_other_statements(self):
		for prefix in ('export import { x } from "x"\n', 'other()\n'):
			with self.subTest(prefix=prefix), self.assertRaises(DocumentationError):
				extract(DOCUMENT.replace("export fn", prefix + "export fn"), "math.el")

	def test_unterminated_block_cannot_create_docs(self):
		with self.assertRaisesRegex(DocumentationError, "block comment"):
			extract("/*\n" + DOCUMENT, "math.el")

	def test_example_tags_are_literal_inside_fences(self):
		entry, = extract(DOCUMENT.replace("/// console.stdout", "/// @unknown\n/// console.stdout"), "math.el")
		self.assertIn("@unknown", entry["sections"][-1]["code"])


class GenerationTests(unittest.TestCase):
	def setUp(self):
		self.temporary = tempfile.TemporaryDirectory()
		self.addCleanup(self.temporary.cleanup)
		self.root = Path(self.temporary.name)
		self.stdlib = self.root / "src/stdlib"
		self.stdlib.mkdir(parents=True)
		(self.stdlib / "math.el").write_text(DOCUMENT, encoding="utf-8")
		self.output = self.root / "docs"

	def test_determinism_check_and_stale_cleanup(self):
		pages = render(collect(self.root))
		write_pages(self.output, pages)
		mtime = (self.output / "api.json").stat().st_mtime_ns
		write_pages(self.output, render(collect(self.root)))
		self.assertEqual((self.output / "api.json").stat().st_mtime_ns, mtime)
		write_pages(self.output, pages, check=True)
		(self.output / "handwritten.md").write_text("keep")
		with self.assertRaisesRegex(DocumentationError, "stale"):
			write_pages(self.output, {}, check=True)
		write_pages(self.output, {})
		self.assertFalse((self.output / "api.json").exists())
		self.assertTrue((self.output / "handwritten.md").exists())

	def test_protect_edited_generated_file(self):
		pages = render(collect(self.root))
		write_pages(self.output, pages)
		(self.output / "index.md").write_text("hand edit")
		with self.assertRaisesRegex(DocumentationError, "was edited"):
			write_pages(self.output, pages)

	def test_protect_unowned_file(self):
		self.output.mkdir()
		(self.output / "index.md").write_text("handwritten")
		with self.assertRaisesRegex(DocumentationError, "unowned"):
			write_pages(self.output, render(collect(self.root)))

	def test_manifest_cannot_escape_output(self):
		self.output.mkdir()
		(self.output / ".generated.json").write_text(json.dumps({"../outside": "abc"}))
		with self.assertRaisesRegex(DocumentationError, "unsafe"):
			write_pages(self.output, {})

	def test_duplicates_and_unresolved_references(self):
		path = self.stdlib / "math.el"
		path.write_text(DOCUMENT + DOCUMENT)
		with self.assertRaisesRegex(DocumentationError, "duplicate"):
			collect(self.root)
		path.write_text(DOCUMENT.replace("/// @param", "/// @see missing::symbol\n/// @param"))
		with self.assertRaisesRegex(DocumentationError, "unknown @see"):
			collect(self.root)

	def test_cross_module_reference_and_overload(self):
		(self.stdlib / "nested").mkdir()
		(self.stdlib / "nested/other.el").write_text(DOCUMENT.replace("@api increment", "@api increment~number").replace("/// @param", "/// @see math::increment\n/// @param"))
		model = collect(self.root)
		self.assertEqual(model["coverage"]["documented_apis"], 2)
		page = render(model)["modules/nested/other.md"]
		self.assertIn("../math.md#api-", page)

	def test_github_source_links(self):
		model = collect(self.root)
		page = render(model)["modules/math.md"]
		self.assertIn("[在 GitHub 查看源码](https://github.com/steve02081504/el/blob/master/src/stdlib/math.el#L12)", page)
		page = render(model, "https://github.com/example/el/blob/review/src/stdlib/")["modules/math.md"]
		self.assertIn("https://github.com/example/el/blob/review/src/stdlib/math.el", page)


if __name__ == "__main__":
	unittest.main()
