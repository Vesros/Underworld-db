$ErrorActionPreference = "Stop"

function Run-Py {
  param($Args)
  $candidates = @("py -3","py","python3","python")
  foreach ($c in $candidates) {
    try {
      $out = & $c @Args 2>$null
      if ($LASTEXITCODE -eq 0) { return ,$out }
    } catch {}
  }
  throw "Python 3 not found. Install from https://python.org and re-run."
}

$ver = (Run-Py @("build_manifest.py"))[0].Trim()
if (-not (Test-Path "manifest.json")) { throw "manifest.json was not generated." }
if (-not (Test-Path "cdn/$ver")) { throw "cdn/$ver not found." }

git add "manifest.json" "cdn/$ver"
try { git commit -m "db $ver" } catch { Write-Host "Nothing to commit" }
git tag -f "db-$ver"
git push origin main --tags

Write-Host "OK"
Write-Host "Stable manifest:"
Write-Host "https://cdn.jsdelivr.net/gh/Vesros/Underworld-db@main/manifest.json"
Write-Host "Tag-pinned example file:"
Write-Host "https://cdn.jsdelivr.net/gh/Vesros/Underworld-db@db-$ver/cdn/$ver/GameData.json"
