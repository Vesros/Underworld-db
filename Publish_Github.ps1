$ErrorActionPreference = "Stop"
$ver = python build_manifest.py
git add manifest.json "cdn/$ver"
git commit -m "db $ver"
git tag "db-$ver" -f
git push origin main --tags
Write-Host "Done."
Write-Host "Stable manifest URL:"
Write-Host "https://cdn.jsdelivr.net/gh/<your-github-user>/Underworld-db@main/manifest.json"
