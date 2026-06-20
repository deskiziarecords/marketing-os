# Marketing OS — start both servers
# Usage: .\start.ps1
# Stop both: Ctrl+C in each window, or close the windows

$ROOT = $PSScriptRoot

# Django (backend) — new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
  Set-Location '$ROOT'
  Write-Host '--- Django API (http://localhost:8000) ---' -ForegroundColor Cyan
  & '$ROOT\.venv\Scripts\python.exe' manage.py runserver --settings=config.settings.local
"@

# Next.js (frontend) — new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
  Set-Location '$ROOT\frontend'
  Write-Host '--- Next.js UI (http://localhost:3000) ---' -ForegroundColor Green
  `$env:NODE_OPTIONS = '--use-system-ca'
  node node_modules\next\dist\bin\next dev --port 3000
"@

Write-Host ""
Write-Host "Both servers starting in separate windows." -ForegroundColor Yellow
Write-Host "  API  -> http://localhost:8000" -ForegroundColor Cyan
Write-Host "  UI   -> http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Close those windows (or Ctrl+C inside them) to stop." -ForegroundColor Gray
