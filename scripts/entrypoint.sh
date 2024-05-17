#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python ./src/manage.py'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

# echo 'Provisioning superuser...'
# $RUN_MANAGE_PY provisionsuperuser

cd src
exec poetry run gunicorn \
    --workers $((2 * $(getconf _NPROCESSORS_ONLN) + 1)) \
    --threads 4 \
    --bind 0.0.0.0:8000 \
    project.wsgi:application
