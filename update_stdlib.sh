#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$repo_dir/scripts/stdlib_docs.py" --el-root "$repo_dir/../el" "$@"
