from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from api_navigation import on_config


class NavigationTests(unittest.TestCase):
	def test_nested_and_root_modules_are_reachable_once(self):
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for name in ("categories/root.md", "categories/text.md", "modules/value.md", "modules/text/nested/parser.md"):
				path = root / "stdlib/api" / name
				path.parent.mkdir(parents=True, exist_ok=True)
				path.write_text("# Reference\n", encoding="utf-8")
			config = {"docs_dir": str(root), "nav": [{"标准库": "stdlib/api/index.md"}]}
			on_config(config)
			def paths(items):
				for item in items:
					for target in item.values():
						if isinstance(target, list):
							yield from paths(target)
						else:
							yield target
			actual = list(paths(config["nav"]))
			self.assertEqual(len(actual), len(set(actual)))
			self.assertIn("stdlib/api/modules/value.md", actual)
			self.assertIn("stdlib/api/modules/text/nested/parser.md", actual)
			self.assertIn("stdlib/api/modules.md", actual)
			self.assertIn("stdlib/api/symbols.md", actual)
			self.assertIn("stdlib/api/types.md", actual)
			self.assertIn("stdlib/api/categories/text.md", actual)


if __name__ == "__main__":
	unittest.main()
