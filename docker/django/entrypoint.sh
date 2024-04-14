#!/bin/sh
set -e

django-admin migrate
django-admin runserver 0.0.0.0:8000

exec "$@"
