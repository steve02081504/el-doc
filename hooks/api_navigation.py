"""Keep generated API module pages reachable from the site's sidebar."""

from pathlib import Path


def expand_navigation(config):
	root = Path(config["docs_dir"]) / "stdlib/api/modules"
	categories = []
	for category in sorted((root.parent / "categories").glob("*.md")):
		modules = [
			{path.relative_to(root).with_suffix("").as_posix(): path.relative_to(config["docs_dir"]).as_posix()}
			for path in sorted(root.glob("*.md") if category.stem == "root" else (root / category.stem).rglob("*.md"))
		]
		categories.append({category.stem: [{"分类总览": category.relative_to(config["docs_dir"]).as_posix()}, *modules]})

	def expand(items):
		for item in items:
			if not isinstance(item, dict):
				continue
			for title, target in item.items():
				if target == "stdlib/api/index.md":
					item[title] = [{"分类总览": target}, {"默认环境": "stdlib/api/environment.md"}, {"类型定义": "stdlib/api/types.md"}, {"模块索引": "stdlib/api/modules.md"}, {"符号索引": "stdlib/api/symbols.md"}, *categories]
				elif isinstance(target, list):
					expand(target)

	expand(config["nav"])
	return config
