#!/bin/sh
set -e

# Wait for DB if it's Postgres
if echo "\" | grep -q "postgres"; then
  echo "Waiting for Postgres..."
  until pg_isready -h \ -p 5432 >/dev/null 2>&1; do
    sleep 1
  done
  echo "Postgres is ready"
  alembic upgrade head || true
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
