    cd /var/www/
    mkdir linker24.de
    cd linker24.de/
    git clone git@github.com:swell-d/linker.git .
    python3 -m venv venv
    source venv/bin/activate
    python manage.py collectstatic --noinput
    python run_full.py
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
    
    docker build -t linker24 .
    docker run -d --restart unless-stopped --name linker24 -p 8090:8090 -v /var/www/linker24.de/db.sqlite3:/app/db.sqlite3 linker24
