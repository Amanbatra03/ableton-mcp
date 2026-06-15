# PyPI Upload — Step-by-Step Guide

## Step 1: Get Your PyPI API Token

1. Visit https://pypi.org/account/
2. Log in or create an account
3. Navigate to **API tokens** in the left menu
4. Click **Add API token**
5. Name it: `ableton-mcp-release`
6. **Copy the full token** (starts with `pypi-`)
   - **KEEP THIS SAFE** — Don't share or commit it!

Example token format: `pypi-AgEIcHlwaS5vcmc...`

## Step 2: Upload to PyPI

Run this command in the `ableton-mcp` directory:

```bash
python -m twine upload dist/*
```

When prompted:
```
Uploading ableton_mcp-1.0.0-py3-none-any.whl
Username: __token__
Password: [paste your token here]

Uploading ableton_mcp-1.0.0.tar.gz
...
```

**Expected output:**
```
Uploading ableton_mcp-1.0.0-py3-none-any.whl ... ✓
Uploading ableton_mcp-1.0.0.tar.gz ... ✓

View at: https://pypi.org/project/ableton-mcp/1.0.0/
```

## Step 3: Verify on PyPI

Wait 2-3 minutes, then visit:
```
https://pypi.org/project/ableton-mcp/
```

You should see v1.0.0 listed.

## Step 4: Test Installation

```bash
pip install --upgrade ableton-mcp

# Verify it works
python -c "import ableton_mcp; print('Success!')"

# Or run the CLI
ableton-mcp --help
```

## Step 5: Create GitHub Release

```bash
gh release create v1.0.0 \
  --title "v1.0.0: Production-Ready Release" \
  --notes "See https://pypi.org/project/ableton-mcp/1.0.0/ for details"
```

## Done! ✅

Your package is now:
- ✅ Published on PyPI
- ✅ Installable via `pip install ableton-mcp`
- ✅ Released on GitHub
- ✅ Ready for use in production

## Troubleshooting

### "403 Forbidden"
- Check your token is correct
- Check username is `__token__` (not your username)
- Ensure token hasn't expired

### "Invalid distribution"
- Run `python -m twine check dist/*` first
- Verify pyproject.toml version is 1.0.0

### "Package already exists"
- If version already on PyPI, you need a new version number
- Update `pyproject.toml` to 1.0.1, rebuild, and re-upload

### "Not found on PyPI after upload"
- Wait 5-10 minutes for indexing
- PyPI sometimes takes time to propagate

## Next Steps

1. ✅ Upload to PyPI (you're here)
2. Register with MCP Registry: https://registry.modelcontextprotocol.io/
3. Update your portfolio with the published package
4. Share the release on social media/communities

---

**Ready?** Get your PyPI API token and run:
```bash
python -m twine upload dist/*
```
