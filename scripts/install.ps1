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

# Resolve the latest release tag via the GitHub API.
try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Repo/releases/latest" -UseBasicParsing
} catch {
    Fail "could not reach GitHub API: $_"
}

if (-not $release.tag_name) {
    Fail "no published release found for $Repo"
}

$Tag = $release.tag_name
$Version = $Tag -replace '^v', ''
Write-Host "okepy: latest release is $Tag"

$AssetUrl = "https://github.com/$Repo/releases/download/$Tag/okepy-$Version-py3-none-any.whl"

$tmp = New-Item -ItemType Directory -Path (Join-Path $env:TEMP "okepy-install")
$whell = Join-Path $tmp.FullName "okepy-$Version-py3-none-any.whl"

Write-Host "okepy: downloading $AssetUrl"
try {
    Invoke-WebRequest -Uri $AssetUrl -OutFile $wheel -UseBasicParsing
} catch {
    Fail "failed to download wheel; the release may not publish a wheel asset"
}

Write-Host "okepy: installing with $InstallBin"
try {
    & $InstallBin install $wheel
    if ($LASTEXITCODE -ne 0) { Fail "installation failed; check your Python/pip environment" }
} finally {
    Remove-Item -Recurse -Force $tmp.FullName -ErrorAction SilentlyContinue
}

Write-Host "okepy: installed! Run it with: okepy create"
