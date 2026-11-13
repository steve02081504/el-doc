"""Checks for generated navigation and random-page URLs."""

import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "hooks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SiteAssetsTest(unittest.TestCase):
    def test_incomplete_type_snapshot_fails_before_build(self):
        spec = importlib.util.spec_from_file_location("build_site", ROOT / "scripts/build_site.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            content = b"generated"
            manifest = {name: hashlib.sha256(content).hexdigest() for name in ("api.json", "index.md", "environment.md", "types.md")}
            (root / ".generated.json").write_text(json.dumps(manifest), encoding="utf-8")
            for name in ("api.json", "index.md", "environment.md"):
                (root / name).write_bytes(content)
            with self.assertRaisesRegex(ValueError, "missing types.md"):
                builder.validate_snapshot(root)
            (root / "types.md").write_bytes(content)
            builder.validate_snapshot(root)

    def test_random_page_urls_match_directory_urls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            docs = root / "docs"
            (docs / "guide").mkdir(parents=True)
            for path in ("index.md", "404.md", "guide/index.md", "guide/start.md"):
                (docs / path).write_text("# Page", encoding="utf-8")
            load("random_pages").write_page_list(docs, root / "site")
            pages = json.loads((root / "site/assets/random-pages.json").read_text(encoding="utf-8"))
            self.assertEqual(pages, ["", "guide/", "guide/start/"])

    def test_navigation_includes_generated_modules(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp)
            (docs / "stdlib/api/categories").mkdir(parents=True)
            (docs / "stdlib/api/modules/io").mkdir(parents=True)
            (docs / "stdlib/api/categories/io.md").touch()
            (docs / "stdlib/api/modules/io/file.md").touch()
            config = {"docs_dir": str(docs), "nav": [{"API": "stdlib/api/index.md"}]}
            load("api_navigation").expand_navigation(config)
            self.assertIn({"io/file": "stdlib/api/modules/io/file.md"}, config["nav"][0]["API"][-1]["io"])


if __name__ == "__main__":
    unittest.main()
