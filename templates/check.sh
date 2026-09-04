#!/usr/bin/env bash
set -euo pipefail

SKIP_FRONTEND=0
SKIP_BACKEND=0
SKIP_DOCKER=0

for arg in "$@"; do
  case "$arg" in
    --skip-frontend) SKIP_FRONTEND=1 ;;
    --skip-backend) SKIP_BACKEND=1 ;;
    --skip-docker) SKIP_DOCKER=1 ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

step() {
  echo
  echo "==> $1"
}

has_command() {
  command -v "$1" >/dev/null 2>&1
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$SKIP_FRONTEND" -eq 0 && -f "frontend/package.json" ]]; then
  step "Frontend install check"
  if [[ ! -d "frontend/node_modules" ]]; then
    if [[ -f "frontend/package-lock.json" ]]; then
      (cd frontend && npm ci)
    else
      (cd frontend && npm install)
    fi
  fi

  step "Frontend format check"
  (cd frontend && npm run format:check --if-present)

  step "Frontend lint"
  (cd frontend && npm run lint --if-present)

  step "Frontend type check"
  (cd frontend && npm run typecheck --if-present)

  step "Frontend tests"
  (cd frontend && npm test --if-present)

  step "Frontend build"
  (cd frontend && npm run build --if-present)
fi

if [[ "$SKIP_BACKEND" -eq 0 && -f "backend/pyproject.toml" ]]; then
  if has_command ruff; then
    step "Backend ruff format check"
    (cd backend && ruff format --check .)

    step "Backend ruff lint"
    (cd backend && ruff check .)
  else
    echo "Skip backend ruff checks: ruff is not installed."
  fi

  if has_command pytest; then
    step "Backend tests"
    (cd backend && pytest)
  else
    echo "Skip backend tests: pytest is not installed."
  fi

  if [[ -f "backend/alembic.ini" ]] && has_command alembic; then
    step "Backend alembic check"
    (cd backend && alembic check)
  else
    echo "Skip alembic check: alembic.ini or alembic is missing."
  fi
fi

if [[ "$SKIP_DOCKER" -eq 0 && -f "compose.yaml" ]] && has_command docker; then
  step "Docker compose config"
  docker compose config --quiet
fi

step "Sensitive file check"
FORBIDDEN_FILES="$(find . \
  \( -path './.git' -o -path './frontend/node_modules' -o -path './backend/.venv' -o -path './.venv' \) -prune -o \
  -type f \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.sqlite' -o -name '*.db' -o -name '*.log' \) \
  -print | grep -v '^\./\.env\.example$' || true)"

if [[ -n "$FORBIDDEN_FILES" ]]; then
  echo "$FORBIDDEN_FILES"
  echo "Found forbidden local files. Remove or ignore them before commit." >&2
  exit 1
fi

echo
echo "All available checks passed."
