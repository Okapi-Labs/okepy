#!/usr/bin/env bash
#
# okepy installer — fetches the latest GitHub release and installs it via pip.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Okapi-Labs/okepy/main/scripts/install.sh | bash
#
# The script downloads the latest release wheel from GitHub and installs it
# into the active Python environment with pip. It is a thin convenience
# wrapper around `pip install`; prefer `pip install okepy` or `uvx okepy`
# when you have network access to PyPI.

set -euo pipefail

REPO="${OKEPY_REPO:-Okapi-Labs/okepy}"

err() { echo "okepy: error: $*" >&2; exit 1; }

need() {
  command -v "$1" >/dev/null 2>&1 || err "'$1' is required but not found on PATH"
}

need curl
need python3

# Pick an install backend. pipx is preferred (it isolates the CLI in its own
# venv and works on externally-managed Python installs, e.g. PEP 668). Override
# with OKEPY_BIN="pip" or "uv pip" if you know what you are doing.
if [ -n "${OKEPY_BIN:-}" ]; then
  INSTALL_BIN="$OKEPY_BIN"
elif command -v pipx >/dev/null 2>&1; then
  INSTALL_BIN="pipx"
else
  INSTALL_BIN="pip"
fi

# Resolve the latest released version. Prefer the GitHub releases API; fall
# back to the PyPI JSON API so an API hiccup (rate limit, empty body) never
# blocks installation. Prints the bare version (e.g. "0.2.1") and returns 0,
# or returns 1 if BOTH sources fail.
API_HDR=(-H "User-Agent: okepy-installer")
latest_version() {
  local body
  # 1) GitHub releases/latest
  if body="$(curl -fsSL "${API_HDR[@]}" "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null)"; then
    python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(d["tag_name"].lstrip("v"))' "$body" 2>/dev/null && return 0
  fi
  # 2) PyPI JSON API
  echo "okepy: GitHub API unavailable, querying PyPI" >&2
  if body="$(curl -fsSL "${API_HDR[@]}" "https://pypi.org/pypi/okepy/json" 2>/dev/null)"; then
    python3 -c 'import json,sys; print(json.loads(sys.argv[1])["info"]["version"])' "$body" 2>/dev/null && return 0
  fi
  return 1
}

VERSION="$(latest_version)" || err "could not resolve the latest okepy version (GitHub and PyPI both unreachable)"
TAG="v${VERSION}"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

wheel="${tmp}/okepy-${VERSION}-py3-none-any.whl"

# Prefer the GitHub release wheel; fall back to the PyPI wheel so the
# installer works even when a release has no attached assets.
ASSET_URL="https://github.com/${REPO}/releases/download/${TAG}/okepy-${VERSION}-py3-none-any.whl"
PYPI_URL="https://files.pythonhosted.org/packages/py3/o/okepy/okepy-${VERSION}-py3-none-any.whl"

echo "okepy: latest version is ${TAG}"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

wheel="${tmp}/okepy-${VERSION}-py3-none-any.whl"

# Prefer the GitHub release wheel; fall back to the PyPI wheel so the
# installer works even when a release has no attached assets.
ASSET_URL="https://github.com/${REPO}/releases/download/${TAG}/okepy-${VERSION}-py3-none-any.whl"
PYPI_URL="https://files.pythonhosted.org/packages/py3/o/okepy/okepy-${VERSION}-py3-none-any.whl"

echo "okepy: downloading release wheel"
if curl -fsSL "${API_HDR[@]}" "$ASSET_URL" -o "$wheel"; then
  echo "okepy: using GitHub release asset"
elif curl -fsSL "${API_HDR[@]}" "$PYPI_URL" -o "$wheel"; then
  echo "okepy: using PyPI wheel"
else
  err "failed to download okepy ${VERSION} wheel from GitHub or PyPI"
fi

echo "okepy: installing with ${INSTALL_BIN}"
if [ "$INSTALL_BIN" = "pipx" ]; then
  pipx install "$wheel" \
    || err "pipx install failed; try 'OKEPY_BIN=pip pip install --user $wheel' or use a virtual environment"
else
  "${INSTALL_BIN}" install "$wheel" \
    || err "installation failed (externally-managed environment? use pipx, or OKEPY_BIN='pip install --break-system-packages')"
fi

echo "okepy: installed! Run it with: okepy create"
