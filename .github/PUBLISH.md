# Publishing Guide

This document describes how to publish Ableton MCP to PyPI and the MCP Registry.

## Prerequisites

- PyPI account (https://pypi.org/account/register/)
- GitHub token (for releases)
- `build` and `twine` packages installed

## Step 1: Version & Git Tagging

```bash
# Verify version in pyproject.toml is updated
cat pyproject.toml | grep "^version"

# Update version if needed
# Edit pyproject.toml and update the version field

# Create a git tag for the release
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag
git push origin v1.0.0
```

## Step 2: Build Distribution

```bash
# Install build tools
pip install build twine

# Build wheels and source distribution
python -m build

# Verify builds
ls dist/
# Should show:
#   ableton_mcp-1.0.0-py3-none-any.whl
#   ableton_mcp-1.0.0.tar.gz
```

## Step 3: Check Before Publishing

```bash
# Check long description (README) renders correctly
twine check dist/*

# Verify package contents
tar -tzf dist/ableton_mcp-1.0.0.tar.gz | head -20
```

## Step 4: Publish to PyPI

### Option A: Using Credentials

```bash
# Publish to PyPI
twine upload dist/*

# When prompted, enter:
#   Username: __token__
#   Password: pypi-YOUR_API_TOKEN
```

### Option B: Using .pypirc (Recommended)

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: __token__
password: pypi-YOUR_API_TOKEN
```

Then publish:

```bash
twine upload dist/*
```

### Verify Publication

```bash
# Check PyPI
pip install --upgrade ableton-mcp

# Verify it installs from PyPI
python -c "import ableton_mcp; print(ableton_mcp.__version__)"
```

## Step 5: Register with MCP Registry

The MCP Registry is a community registry at https://registry.modelcontextprotocol.io/

### Option A: Manual Registration (If Registry Accepts)

1. Visit https://registry.modelcontextprotocol.io/
2. Click "Add a Server"
3. Fill in the form:
   - **Name**: ableton-mcp
   - **Repository**: https://github.com/Amanbatra03/ableton-mcp
   - **Command**: `uvx ableton-mcp` (or `pip install ableton-mcp && ableton-mcp`)
   - **Description**: "Intelligent MCP server for controlling Ableton Live mixing via Claude"

### Option B: Via GitHub Discussion

If a registry doesn't exist yet:

1. Post in Claude community forums
2. Reference this project as a notable MCP server

## Step 6: Create GitHub Release

```bash
# Create release notes from CHANGELOG.md
gh release create v1.0.0 \
  --title "v1.0.0: Production-Ready Release" \
  --notes "$(cat <<'EOF'
55 tools for controlling Ableton Live via Claude

## What's New
- 49 Ableton control tools (Phase 0-4)
- 6 music generation tools
- 35 device parameter mappings
- Pure Python music theory library
- GitHub Actions CI/CD
- Comprehensive documentation

## Features
- ✅ 80-90% mixing automation capability
- ✅ Intelligent device control by parameter name
- ✅ Chord/scale/progression builders
- ✅ Drum pattern generation
- ✅ Batch mixing workflows

## Installation
pip install ableton-mcp

## Documentation
- README.md: Quick start and examples
- INSTALL.md: Setup instructions
- CONTRIBUTING.md: Development guide
- CHANGELOG.md: Full version history

See https://github.com/Amanbatra03/ableton-mcp for more.
EOF
)"
```

## Step 7: Update Documentation Sites

If you maintain a portfolio or website:

```markdown
## Ableton MCP Server

An intelligent MCP server that enables Claude to control Ableton Live mixing.

**Status**: Production-Ready (v1.0.0)
**Repository**: https://github.com/Amanbatra03/ableton-mcp
**PyPI**: https://pypi.org/project/ableton-mcp/

- 55 tools for music production automation
- 35 device parameter mappings
- Music theory library (chords, scales, progressions)
- 80-90% mixing automation capability

[Install →](https://github.com/Amanbatra03/ableton-mcp/blob/main/INSTALL.md)
```

## Post-Release Checklist

- [ ] Verify PyPI package installs: `pip install ableton-mcp`
- [ ] Verify MCP server starts: `ableton-mcp`
- [ ] Test tools in Claude Desktop
- [ ] GitHub release created
- [ ] MCP Registry registered (if applicable)
- [ ] Documentation updated
- [ ] Portfolio updated (if applicable)
- [ ] Release announcement posted (Twitter, etc.)

## Troubleshooting

### "403 Forbidden" when uploading to PyPI

- **Check credentials**: Verify API token is correct
- **Check version**: Ensure version doesn't already exist on PyPI
- **Use `__token__` as username**: Not your actual username

### "Invalid distribution" warnings

- **Check README**: Ensure README.md is valid Markdown
- **Check version**: Ensure semantic versioning (X.Y.Z)
- **Run twine check**: `twine check dist/*`

### Package not found after upload

- **Wait a few minutes**: PyPI takes time to index new packages
- **Check PyPI directly**: https://pypi.org/project/ableton-mcp/
- **Try pip cache clear**: `pip cache purge` then `pip install ableton-mcp`

## Future Releases

For subsequent releases, follow this simplified workflow:

```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md with new features
# 3. Commit and tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# 4. Build and publish
python -m build
twine upload dist/*

# 5. Create GitHub release
gh release create vX.Y.Z ...
```

## Questions?

See `CONTRIBUTING.md` for development info or file an issue on GitHub.
