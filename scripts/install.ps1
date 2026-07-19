<#
.SYNOPSIS
    okepy installer for Windows — fetches the latest GitHub release and installs it via pip.

.DESCRIPTION
    Downloads the latest release wheel from GitHub and installs it into the
    active Python environment. Thin convenience wrapper around `pip install`.

.EXAMPLE
    irm https://raw.githubusercontent.com/Okapi-Labs/okepy/main/scripts/install.ps1 | iex
#>

$ErrorActionPreference = "Stop"

$Repo = if ($env:OKEPY_REPO) { $env:OKEPY_REPO } else { "Okapi-Labs/okepy" }
# Prefer pipx (isolates the CLI, avoids PEP 668 externally-managed errors).
# Override with $env:OKEPY_BIN = "pip" or "uv pip".
if ($env:OKEPY_BIN) {
    $InstallBin = $env:OKEPY_BIN
} elseif (Get-Command pipx -ErrorAction SilentlyContinue) {
    $InstallBin = "pipx"
} else {
    $InstallBin = "pip"
}

function Fail($msg) {
    Write-Error "okepy: error: $msg"
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "python is required but not found on PATH"
}

# Resolve the latest released version. Prefer the GitHub releases API; fall
# back to the PyPI JSON API so an API hiccup never blocks installation.
# Keep the raw tag (e.g. "0.2.0" or "v0.2.1") so the asset URL matches exactly.
$Tag = $null
try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
    if ($release.tag_name) { $Tag = $release.tag_name }
} catch {
    Write-Host "okepy: GitHub API unavailable, querying PyPI" -ForegroundColor Yellow
}
if (-not $Tag) {
    try {
        $pypi = Invoke-RestMethod -Uri "https://pypi.org/pypi/okepy/json" -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
        $Tag = "v" + $pypi.info.version
    } catch {
        Fail "could not resolve the latest okepy version (GitHub and PyPI both unreachable)"
    }
}
$Version = $Tag -replace '^v', ''
Write-Host "okepy: latest version is $Tag"

$AssetUrl = "https://github.com/$Repo/releases/download/$Tag/okepy-$Version-py3-none-any.whl"
$PypiUrl = "https://files.pythonhosted.org/packages/py3/o/okepy/okepy-$Version-py3-none-any.whl"

$tmp = New-Item -ItemType Directory -Path (Join-Path $env:TEMP "okepy-install")
$wheel = Join-Path $tmp.FullName "okepy-$Version-py3-none-any.whl"

Write-Host "okepy: downloading release wheel"
try {
    Invoke-WebRequest -Uri $AssetUrl -OutFile $wheel -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
    Write-Host "okepy: using GitHub release asset"
} catch {
    try {
        Invoke-WebRequest -Uri $PypiUrl -OutFile $wheel -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
        Write-Host "okepy: using PyPI wheel"
    } catch {
        Fail "failed to download okepy $Version wheel from GitHub or PyPI"
    }
}

Write-Host "okepy: installing with $InstallBin"
try {
    if ($InstallBin -eq "pipx") {
        pipx install $wheel
    } else {
        & $InstallBin install $wheel
    }
    if ($LASTEXITCODE -ne 0) { Fail "installation failed; try pipx, or use a virtual environment" }
} finally {
    Remove-Item -Recurse -Force $tmp.FullName -ErrorAction SilentlyContinue
}

Write-Host "okepy: installed! Run it with: okepy create"
