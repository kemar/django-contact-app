# Debian slim variant.
# https://www.debian.org/releases/index.html
# https://hub.docker.com/_/python
FROM python:3.12.3-slim-bookworm

ENV PYTHONIOENCODING="UTF-8"
ENV PYTHONUNBUFFERED=1

ENV APP_DIR="/app"

# Add new user to run the whole thing as non-root.
RUN set -ex \
    && addgroup app \
    && adduser --ingroup app --home $APP_DIR --disabled-password app;

RUN set -ex; \
    if ! command -v gpg > /dev/null; then \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            gnupg \
            dirmngr \
        ; \
        rm -rf /var/lib/apt/lists/*; \
    fi

RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    sqlite3 \
    --no-install-recommends

RUN apt-get purge -y --auto-remove build-essential $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt \
    && rm -f /requirements.txt

COPY --chown=app:app . $APP_DIR

RUN chmod +x $APP_DIR/docker/django/entrypoint.sh

USER app

WORKDIR $APP_DIR

ENTRYPOINT ["./docker/django/entrypoint.sh"]
