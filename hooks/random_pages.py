"""Publish the content page URLs used by the random-page button."""

import json
from pathlib import Path


def write_page_list(docs_dir, site_dir):
    docs_dir = Path(docs_dir)
    pages = []
    for source in docs_dir.rglob("*.md"):
        relative = source.relative_to(docs_dir)
        if relative.as_posix() == "404.md":
            continue
        url = relative.parent.as_posix() + "/" if relative.name == "index.md" else relative.with_suffix("").as_posix() + "/"
        pages.append("" if url == "./" else url)
    path = Path(site_dir) / "assets" / "random-pages.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(pages), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
