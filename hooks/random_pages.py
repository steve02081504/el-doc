"""Publish the list of content pages used by the footer's random-page button.

The button needs the site's page URLs relative to the site root. Collecting
them while pages render keeps the list in sync with the navigation without a
second source of truth.
"""

import json
import os

_pages: set[str] = set()


def on_config(config):
    _pages.clear()
    return config


def on_page_context(context, *, page, config, nav):
    if page.file.src_uri != "404.md":
        _pages.add(page.url)
    return context


def on_post_build(config):
    assets = os.path.join(config["site_dir"], "assets")
    os.makedirs(assets, exist_ok=True)
    path = os.path.join(assets, "random-pages.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(sorted(_pages), handle, ensure_ascii=False, separators=(",", ":"))
