#!/usr/bin/env bash
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_ROOT/.." && pwd)"

echo "[reset] stopping backend server"
pkill -f "uvicorn app.main:app" >/dev/null 2>&1 || true

echo "[reset] stopping Ollama"
pkill -f "ollama serve" >/dev/null 2>&1 || true

echo "[reset] stopping frontend"
pkill -f "npm run dev" >/dev/null 2>&1 || true

echo "[reset] removing data directory"
rm -rf "$REPO_ROOT/backend/data"

echo "[reset] restarting backend server"
cd "$REPO_ROOT/backend"
nohup ./.venv/bin/uvicorn app.main:app --reload --port 8000 > "$REPO_ROOT/backend/server.log" 2>&1 &

echo "[reset] restarting frontend server"
cd "$REPO_ROOT/frontend"
nohup npm run dev -- --host 0.0.0.0 --port 5173 > "$REPO_ROOT/frontend/dev.log" 2>&1 &

echo "[reset] done"
