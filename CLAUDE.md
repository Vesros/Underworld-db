# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Underworld-db repository, a database management system for the Underworld game that uses Netlify CMS for content management and publishes data to a CDN via GitHub releases. The system manages game configuration data including GameData (version info, build metadata) and BalanceData (gameplay modifiers).

## Development Workflow

### Building and Publishing
- **Pack CMS data to JSON**: `python tools/pack_cms.py`
  - Converts individual JSON files from `cms/` folders into consolidated arrays in `db_src/`
  - Must be run after making changes in Netlify CMS before publishing
- **Build manifest**: `python build_manifest.py`
  - Creates timestamped version in `cdn/` folder with SHA256 hashes
  - Updates `manifest.json` with CDN URLs and file metadata
- **Publish to GitHub** (Bash): `./Publish_Github.sh`
- **Publish to GitHub** (PowerShell): `.\Publish_Github.ps1`
  - Commits changes, creates git tag, pushes to GitHub
  - Publishes to jsDelivr CDN automatically

### Python Requirements
The PowerShell script automatically detects Python installations in this order: `py -3`, `py`, `python3`, `python`. If none found, install from python.org.

## Architecture

### Data Flow
1. **Content Management**: Edit data via Netlify CMS admin interface (`/admin/`)
2. **Data Processing**: Run `pack_cms.py` to convert CMS files to database format
3. **Manifest Generation**: `build_manifest.py` creates versioned distribution files
4. **Publishing**: Git automation scripts deploy to CDN via GitHub releases

### File Structure
- `cms/`: Netlify CMS source files (individual JSON objects)
  - `GameData/Global.json`: Version, patch date, build type
  - `BalanceData/Global.json`: Gameplay balance modifiers
- `db_src/`: Consolidated JSON arrays (generated from cms/)
- `cdn/[version]/`: Timestamped distribution files with CDN URLs
- `admin/`: Netlify CMS configuration and admin interface
- `tools/pack_cms.py`: CMS-to-database conversion utility

### Data Schema
**GameData fields**: Id, Version, LastPatchDate, BuildType
**BalanceData fields**: Id, GlobalExpGainModifier, GlobalDamageCausedModifier

## Netlify CMS Integration
- Admin interface: `/admin/` (requires Netlify Identity authentication)
- Configuration: `admin/config.yml`
- Backend: git-gateway with main branch
- Only "Global" records are supported (enforced by CMS validation)

## CDN Distribution
Published data is available via jsDelivr:
- **Stable manifest**: `https://cdn.jsdelivr.net/gh/Vesros/Underworld-db@main/manifest.json`
- **Versioned files**: `https://cdn.jsdelivr.net/gh/Vesros/Underworld-db@db-[version]/cdn/[version]/[filename].json`