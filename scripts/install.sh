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
INSTALL_BIN="${OKEPY_BIN:-pip}"

err() { echo "okepy: error: $*" >&2; exit 1; }

need() {
  command -v "$1" >/dev/null 2>&1 || err "'$1' is required but not found on PATH"
}

need curl
need python3

# Resolve the latest release tag via the GitHub API.
latest_tag() {
  curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
    | python3 - "$REPO" <<'PY'
import json, sys, urllib.error
repo = sys.argv[1]
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit("could not parse GitHub API response")
if "tag_name" not in data:
    sys.exit("no published release found for %s" % repo)
print(data["tag_name"])
PY
}

TAG="$(latest_tag)"
VERSION="${TAG#v}"

echo "okepy: latest release is ${TAG}"

# Locate the pure-python wheel asset for this release.
ASSET_URL="https://github.com/${REPO}/releases/download/${TAG}/okepy-${VERSION}-py3-none-any.whl"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

wheel="${tmp}/okepy-${VERSION}-py3-none-any.whl"
echo "okepy: downloading ${ASSET_URL}"
curl -fsSL "$ASSET_URL" -o "$wheel" \
  || err "failed to download wheel; the release may not publish a wheel asset"

echo "okepy: installing with ${INSTALL_BIN}"
"${INSTALL_BIN}" install "$wheel" \
  || err "installation failed; check your Python/pip environment"

echo "okepy: installed! Run it with: okepy create"
