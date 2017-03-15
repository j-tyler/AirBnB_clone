#!/usr/bin/env bash
# Set the static site live
sudo apt-get -y install nginx
mkdir -p /data/web_static/releases/test
mkdir /data/web_static/shared
echo 'Testing...' > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test  /data/web_static/current
chown -R ubuntu:ubuntu /data/
echo 'user www-data;
worker_processes 4;
pid /run/nginx.pid;

events {
        worker_connections 768;
}

http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        gzip on;
        gzip_disable "msie6";

    server {
        listen 80;
        server_name localhost;
        location / {
            root /home;
        }
        location /hbnb_static/ {
            alias /data/web_static/current/; 
	   } 
        error_page 404 /404.html;
        location = /404.html {
            root /home;
        }
        location /redirect_me {
            rewrite ^/redirect_me http://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;
        }
    }
}' | sudo tee /etc/nginx/nginx.conf > /dev/null
sudo service nginx restart
