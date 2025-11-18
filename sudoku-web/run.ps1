# ...existing code...
param()

# Load .env into environment (simple parser; ignore comments/blank lines)
if (Test-Path .\.env) {
  Get-Content .\.env |
    Where-Object { $_ -and ($_ -notmatch '^\s*#') } |
    ForEach-Object {
      $parts = $_ -split '=', 2
      if ($parts.Count -eq 2) {
        [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim())
      }
    }
}

# Prefer waitress on Windows (gunicorn is not supported on Windows)
$waitress = Get-Command waitress-serve -ErrorAction SilentlyContinue

if ($null -ne $waitress) {
  Write-Host "Starting app with waitress on 127.0.0.1:8000"
  & waitress-serve --listen=127.0.0.1:8000 src.app.main:app
} else {
  Write-Host "waitress not found; running Flask dev server (not for production)."
  python src/app/main.py
}