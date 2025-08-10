#!/usr/bin/env bash
set -euo pipefail
ver=$(python3 build_manifest.py)
git add manifest.json "cdn/$ver"
git commit -m "db $ver"
git tag "db-$ver" -f
git push origin main --tags
echo "Done."
echo "Stable manifest URL:"
echo "https://cdn.jsdelivr.net/gh/<your-github-user>/Underworld-db@main/manifest.json"
