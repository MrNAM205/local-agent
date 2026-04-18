param(
    [switch]$Production
)

Write-Host "Building Electron GUI..." -ForegroundColor Cyan

Push-Location gui

if (!(Test-Path "package.json")) {
    Write-Error "No package.json found in gui/. Are you in the right project?"
    Pop-Location
    exit 1
}

if (!(Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

if ($Production) {
    Write-Host "Running production build..." -ForegroundColor Green
    npm run build
} else {
    Write-Host "Running dev build..." -ForegroundColor Green
    npm run dev
}

Pop-Location