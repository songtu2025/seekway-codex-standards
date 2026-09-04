param(
    [switch]$SkipFrontend,
    [switch]$SkipBackend,
    [switch]$SkipDocker
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "==> $Name"
    & $Command
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

if (-not $SkipFrontend -and (Test-Path "frontend/package.json")) {
    Invoke-Step "Frontend install check" {
        if (-not (Test-Path "frontend/node_modules")) {
            Push-Location "frontend"
            if (Test-Path "package-lock.json") {
                npm ci
            }
            else {
                npm install
            }
            Pop-Location
        }
    }

    Push-Location "frontend"
    Invoke-Step "Frontend format check" { npm run format:check --if-present }
    Invoke-Step "Frontend lint" { npm run lint --if-present }
    Invoke-Step "Frontend type check" { npm run typecheck --if-present }
    Invoke-Step "Frontend tests" { npm test --if-present }
    Invoke-Step "Frontend build" { npm run build --if-present }
    Pop-Location
}

if (-not $SkipBackend -and (Test-Path "backend/pyproject.toml")) {
    Push-Location "backend"

    if (Test-Command "ruff") {
        Invoke-Step "Backend ruff format check" { ruff format --check . }
        Invoke-Step "Backend ruff lint" { ruff check . }
    }
    else {
        Write-Host "Skip backend ruff checks: ruff is not installed."
    }

    if (Test-Command "pytest") {
        Invoke-Step "Backend tests" { pytest }
    }
    else {
        Write-Host "Skip backend tests: pytest is not installed."
    }

    if ((Test-Path "alembic.ini") -and (Test-Command "alembic")) {
        Invoke-Step "Backend alembic check" { alembic check }
    }
    else {
        Write-Host "Skip alembic check: alembic.ini or alembic is missing."
    }

    Pop-Location
}

if (-not $SkipDocker -and (Test-Path "compose.yaml") -and (Test-Command "docker")) {
    Invoke-Step "Docker compose config" { docker compose config --quiet }
}

Invoke-Step "Sensitive file check" {
    $forbidden = @(".env", ".env.*", "*.pem", "*.key", "*.p12", "*.sqlite", "*.db", "*.log")
    foreach ($pattern in $forbidden) {
        $matches = Get-ChildItem -Path . -Recurse -Force -File -Filter $pattern -ErrorAction SilentlyContinue |
            Where-Object {
                $_.FullName -notmatch "\\node_modules\\|\\.git\\" -and
                $_.Name -ne ".env.example"
            }
        if ($matches) {
            $matches | ForEach-Object { Write-Host $_.FullName }
            throw "Found forbidden local files. Remove or ignore them before commit."
        }
    }
}

Write-Host ""
Write-Host "All available checks passed."
