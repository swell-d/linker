FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SQLITE_PATH=/data/db.sqlite3

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

# Static files are baked in because the root filesystem is read-only at runtime.
# This key only lets settings load during the build; it is not kept in the image's environment.
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

# /app stays owned by root, so the app can write to /data only.
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser \
    && install -d -o appuser -g appuser -m 700 /data
USER 10001:10001

EXPOSE 8090
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn linker.wsgi:application --bind 0.0.0.0:8090 --workers 2 --no-control-socket"]
