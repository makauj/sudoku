#!/usr/bin/env bash
set -euo pipefail

# change to repo root (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# load .env if present (simple, ignores comments and blank lines)
if [ -f .env ]; then
  while IFS='=' read -r key val; do
    # skip comments and blank lines
    [[ "$key" =~ ^\s*# ]] && continue
    [ -z "$key" ] && continue
    # trim whitespace
    key="$(echo -n "$key" | awk '{$1=$1};1')"
    val="$(echo -n "${val:-}" | sed -e 's/^["'\'']//;s/["'\'']$//')"
    export "$key=$val"
  done < <(grep -v '^\s*$' .env | grep -v '^\s*#' || true)
fi

# defaults
APP_HOST="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-8000}"
GUNICORN_WORKERS="${GUNICORN_WORKERS:-3}"
GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-30}"
APP_MODULE="${APP_MODULE:-src.app.main:app}"

# start gunicorn bound to localhost so a reverse proxy can front it
echo "Starting gunicorn on ${APP_HOST}:${APP_PORT} (workers=${GUNICORN_WORKERS})"
gunicorn --chdir "$SCRIPT_DIR" --bind "${APP_HOST}:${APP_PORT}" "$APP_MODULE" \
  --workers "$GUNICORN_WORKERS" --worker-class gthread --timeout "$GUNICORN_TIMEOUT" &

GUNICORN_PID=$!

# if nginx is available, try to start (foreground). otherwise wait on gunicorn.
if command -v nginx >/dev/null 2>&1 && [ -f deploy/nginx.conf ]; then
  echo "nginx detected; launching nginx (proxy/static)."
  sudo cp deploy/nginx.conf /etc/nginx/nginx.conf
  nginx -g 'daemon off;'
  # nginx runs in foreground; when it exits, kill gunicorn
  kill "$GUNICORN_PID" 2>/dev/null || true
else
  echo "nginx not found or no deploy/nginx.conf; running gunicorn only."
  # wait for gunicorn to exit
  wait "$GUNICORN_PID"
fi