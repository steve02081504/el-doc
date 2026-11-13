"""Build and preview the documentation site with its generated navigation and links."""

import argparse
import importlib.util
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


def build():
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    config["docs_dir"] = "docs"
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
    load_hook("code_links").link_site(site, ROOT / "docs")


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

