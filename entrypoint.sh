#!/bin/bash
set -e

echo "Running database migrations..."
python setup_database.py --tables-only

echo "Starting application..."
exec gunicorn -w 4 -b "0.0.0.0:${PORT:-8000}" app:app
