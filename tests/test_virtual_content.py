import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("virtual_content", Path(__file__).resolve().parents[1] / "hooks/virtual_content.py")
virtual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(virtual)


class VirtualContentTests(unittest.TestCase):
	def test_large_page_bounds_initial_dom_and_preserves_content_and_fragments(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "index.html"
			sections = [f'<h2 id="type-{i}">Type &lt;{i}&gt;</h2><pre id="code-{i}"><code>class Type{i}</code></pre>' for i in range(160)]
			html = '<nav class="md-nav--secondary"><nav>nested</nav>TOC</nav><article><h1>Types</h1>' + ''.join(sections) + '</article><footer>End</footer>'
			path.write_text(html, encoding="utf-8")
			self.assertEqual(virtual.virtualize_page(path), 160)
			result = path.read_text(encoding="utf-8")
			self.assertNotIn('<pre', result)
			self.assertNotIn('md-nav--secondary', result)
			self.assertIn('<footer>End</footer>', result)
			self.assertEqual(set(virtual.Ids(html).ids), set(virtual.Ids(result).ids))
			self.assertEqual((path.parent / 'full.html').read_text(encoding="utf-8"), html)
			chunks = list(path.parent.glob('content-*.json'))
			chunks.remove(path.parent / 'content-index.json')
			self.assertEqual(len(chunks), 4)
			self.assertEqual({section for chunk in chunks for section in json.loads(chunk.read_text(encoding="utf-8"))}, set(sections))
			index = json.loads((path.parent / 'content-index.json').read_text(encoding="utf-8"))
			self.assertEqual(index[-1], {"id": "type-159", "title": "Type <159>"})

	def test_small_page_unchanged(self):
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / 'index.html'
			html = '<article><h2 id="one">One</h2><p>content</p></article>'
			path.write_text(html, encoding="utf-8")
			self.assertEqual(virtual.virtualize_page(path), 0)
			self.assertEqual(path.read_text(encoding="utf-8"), html)

	def test_long_table_and_list_load_valid_batches(self):
		for tag in ('table', 'ul', 'ol'):
			with self.subTest(tag=tag), tempfile.TemporaryDirectory() as directory:
				path = Path(directory) / 'index.html'
				rows = ''.join(f'<tr><td>Symbol{i}</td></tr>' if tag == 'table' else f'<li>Symbol{i}</li>' for i in range(160))
				block = '<table><thead><tr><th>Name</th></tr></thead><tbody>' + rows + '</tbody></table>' if tag == 'table' else f'<{tag}>' + rows + f'</{tag}>'
				path.write_text('<article><h1>Symbols</h1>' + block + '<p>After list</p></article>', encoding='utf-8')
				self.assertEqual(virtual.virtualize_page(path), 161)
				index = json.loads((path.parent / 'content-index.json').read_text(encoding='utf-8'))
				self.assertIn('Symbol159', index[-2]['title'])
				contents = [part for chunk in path.parent.glob('content-*.json') if chunk.name != 'content-index.json' for part in json.loads(chunk.read_text(encoding='utf-8'))]
				self.assertIn('After list', ''.join(contents))
				for part in contents:
					self.assertLessEqual(part.count('<' + tag + '>'), 1)
					self.assertEqual(part.count('<' + tag + '>'), part.count('</' + tag + '>'))
				self.assertTrue(set(item['id'] for item in index).issubset(set(virtual.Ids(''.join(contents)).ids)))
