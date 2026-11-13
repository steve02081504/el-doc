"""Build and preview the documentation site with its generated navigation and links."""

import argparse
import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import yaml
import zensical

ROOT = Path(__file__).resolve().parents[1]


def load_hook(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "hooks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validate_snapshot(directory):
    directory = Path(directory).resolve()
    manifest = json.loads((directory / ".generated.json").read_text(encoding="utf-8"))
    for required in ("api.json", "index.md", "environment.md", "types.md"):
        if required not in manifest:
            raise ValueError(f"generated documentation manifest is missing {required}; regenerate the API snapshot")
    for name, expected in manifest.items():
        path = (directory / name).resolve()
        if not path.is_relative_to(directory):
            raise ValueError(f"generated documentation path escapes snapshot: {name}")
        if not path.is_file():
            raise ValueError(f"generated documentation is missing {name}; include the complete API snapshot")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"generated documentation differs from its manifest: {name}")


def build():
    validate_snapshot(ROOT / "docs/stdlib/api")
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    config["site_dir"] = "site"
    config["docs_dir"] = str(ROOT / "docs")
    load_hook("api_navigation").expand_navigation(config)
    config["docs_dir"] = "docs"
    load_hook("el_lexer")
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".yml", dir=ROOT, delete=False) as file:
        yaml.safe_dump(config, file, allow_unicode=True, sort_keys=False)
        config_path = Path(file.name)
    try:
        zensical.build(str(config_path), {"strict": True, "clean": True})
    finally:
        config_path.unlink()
    site = ROOT / "site"
    load_hook("random_pages").write_page_list(ROOT / "docs", site)
    result = load_hook("code_links").link_site(site, ROOT / "docs")
    print(f"Reference links: {result['linked_pages']} pages updated; {result['validated_links']} internal links verified.", flush=True)
    count = load_hook("virtual_content").virtualize_site(site)
    load_hook("code_links").validate_site(site)
    print(f"Virtual content: {count} entries loaded on demand.", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "serve"))
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    build()
    if args.command == "serve":
        print(f"Serving http://localhost:{args.port}/ (restart to rebuild)", flush=True)
        with ThreadingHTTPServer(("127.0.0.1", args.port), partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site"))) as server:
            server.serve_forever()


if __name__ == "__main__":
    main()

