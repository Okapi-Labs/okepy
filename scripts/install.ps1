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
$InstallBin = if ($env:OKEPY_BIN) { $env:OKEPY_BIN } else { "pip" }

function Fail($msg) {
    Write-Error "okepy: error: $msg"
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "python is required but not found on PATH"
}

# Resolve the latest released version. Prefer the GitHub releases API; fall
# back to the PyPI JSON API so an API hiccup never blocks installation.
$Version = $null
try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
    if ($release.tag_name) { $Version = $release.tag_name -replace '^v', '' }
} catch {
    Write-Host "okepy: GitHub API unavailable, querying PyPI" -ForegroundColor Yellow
}
if (-not $Version) {
    try {
        $pypi = Invoke-RestMethod -Uri "https://pypi.org/pypi/okepy/json" -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
        $Version = $pypi.info.version
    } catch {
        Fail "could not resolve the latest okepy version (GitHub and PyPI both unreachable)"
    }
}
$Tag = "v$Version"
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
    Write-Host "okepy: no release asset; downloading from PyPI"
    try {
        Invoke-WebRequest -Uri $PypiUrl -OutFile $wheel -Headers @{"User-Agent"="okepy-installer"} -UseBasicParsing
    } catch {
        Fail "failed to download okepy $Version wheel from GitHub or PyPI"
    }
}

Write-Host "okepy: installing with $InstallBin"
try {
    & $InstallBin install $wheel
    if ($LASTEXITCODE -ne 0) { Fail "installation failed; check your Python/pip environment" }
} finally {
    Remove-Item -Recurse -Force $tmp.FullName -ErrorAction SilentlyContinue
}

Write-Host "okepy: installed! Run it with: okepy create"
