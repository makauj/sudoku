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
  $env:FLASK_ENV = "development"

  # Change to the src directory to ensure 'app' is treated as a package
  Push-Location "src"

  # Try to use waitress if available, otherwise fallback to Flask dev server
  try {
    python -m waitress --help > $null 2>&1
    $waitressAvailable = $true
  } catch {
    $waitressAvailable = $false
  }

  if ($waitressAvailable) {
    python -m waitress --listen=0.0.0.0:5000 app.main
  } else {
    python -m app.main
  }

  Pop-Location
}
