    cd /var/www/
    mkdir linker24.de
    cd linker24.de/
    git clone git@github.com:swell-d/linker.git .
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py collectstatic --noinput
    python manage.py makemigrations main
    python manage.py migrate
    python manage.py createsuperuser
    
    server {
        server_name linker24.de;
    
        location / {
            proxy_pass http://127.0.0.1:8090;
        }
    
        location /static/ {
            alias /var/www/linker24.de/staticfiles/;
            expires 7d;
            add_header Cache-Control "public";
            try_files $uri =404;
        }
    }
    
    python manage.py runserver 0.0.0.0:8090
    deactivate

    rm -r venv
    
    docker build -t linker24 .
    find . -mindepth 1 -maxdepth 1 -not -name 'db.sqlite3' -not -name 'staticfiles' -exec rm -rf {} +
    docker run -d --restart unless-stopped --name linker24 -p 8090:8090 -v /var/www/linker24.de/db.sqlite3:/app/db.sqlite3 linker24
