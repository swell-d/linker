# linker

URL shortener behind linker24.de: Django and gunicorn in a locked-down container, with nginx on the host in front.

## Deploy

    git clone git@github.com:swell-d/linker.git /var/www/linker24.de
    cd /var/www/linker24.de

    echo "SECRET_KEY=$(openssl rand -hex 50)" > .env
    chmod 600 .env

    # The container runs as uid 10001 and can write only to ./data
    sudo install -d -o 10001 -g 10001 -m 700 data

    docker compose up -d --build
    docker compose exec web python manage.py createsuperuser

Migrations run when the container starts. Static files are built into the image and served by WhiteNoise.

`unable to open database file` or `attempt to write a readonly database` in `docker compose logs` means `data/` or the database file is not owned by uid 10001.

## Update

    git pull
    docker compose up -d --build

## nginx

    server {
        server_name linker24.de;

        location / {
            proxy_pass http://127.0.0.1:8090;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

`X-Forwarded-Proto` is required: without it Django treats every request as plain HTTP and keeps redirecting it to HTTPS.

## Moving from the old `docker run` setup

The old directory stays in place as a backup until you delete it.

    docker rm -f linker24
    mv /var/www/linker24.de /var/www/linker24.de.old

    git clone git@github.com:swell-d/linker.git /var/www/linker24.de
    cd /var/www/linker24.de

    echo "SECRET_KEY=$(openssl rand -hex 50)" > .env
    chmod 600 .env

    sudo install -d -o 10001 -g 10001 -m 700 data
    sudo cp ../linker24.de.old/db.sqlite3 data/
    sudo chown 10001:10001 data/db.sqlite3

    docker compose up -d --build

Then replace the nginx config with the one above, dropping the old `location /static/` block, and reload nginx. Changing `SECRET_KEY` logs everyone out of the admin; no other data is affected.
