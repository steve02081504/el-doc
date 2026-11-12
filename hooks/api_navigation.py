"""Keep generated API module pages reachable from the site's sidebar."""

from pathlib import Path


def on_config(config):
	root = Path(config["docs_dir"]) / "stdlib/api/modules"
	modules = [
		{path.relative_to(root).with_suffix("").as_posix(): path.relative_to(config["docs_dir"]).as_posix()}
		for path in sorted(root.rglob("*.md"))
	]

	def expand(items):
		for item in items:
			if not isinstance(item, dict):
				continue
			for title, target in item.items():
				if target == "stdlib/api/index.md":
					item[title] = [{"总览": target}, *modules]
				elif isinstance(target, list):
					expand(target)

	expand(config["nav"])
	return config
