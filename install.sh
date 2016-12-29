#!/bin/sh
set -ex

TARGETUSER=""
TARGETHOME="/srv/smileycoin-payment-server"
TARGETBIN="${TARGETHOME}/bin/gunicorn"
TARGETDB="${TARGETHOME}/db/db.sqlite3"
TARGETSECRET="${TARGETHOME}/secret-key.txt"
TARGETUSER="smileycoin-payment-server"
TARGETGROUP="nogroup"

# ---------------------------

id "${TARGETUSER}" 2>/dev/null || adduser --system \
    --home "${TARGETHOME}" --no-create-home \
    --disabled-password \
    ${TARGETUSER}

mkdir -p "$(dirname ${TARGETDB})"
chown -R ${TARGETUSER}:${TARGETGROUP} -p "$(dirname ${TARGETDB})"

[ -e "${TARGETSECRET}" ] || python -c 'import random; import string; print "".join([random.SystemRandom().choice(string.digits + string.letters + string.punctuation) for i in range(100)])' > "${TARGETSECRET}"

cat <<EOF > /etc/systemd/system/smileycoin-payment-server.service
[Unit]
Description=smileycoin-payment-server
After=network.target

[Service]
WorkingDirectory=${TARGETHOME}
ExecStart=${TARGETBIN} gettingstarted.wsgi --log-file -
User=${TARGETUSER}
Group=${TARGETGROUP}

[Install]
WantedBy=multi-user.target
EOF
systemctl enable smileycoin-payment-server.service
systemctl start smileycoin-payment-server.service

sleep 1
systemctl status smileycoin-payment-server.service

cat <<EOF > /etc/nginx/sites-available/smileycoin-payment-server
upstream app_server {
  server 127.0.0.1:8000;
}

server {
  listen 80;
  server_name smly.is www.smly.is;

  keepalive_timeout 5;

  root ${TARGETHOME}/hello/static/;

  location /static {
    alias ${TARGETHOME}/hello/static/;
  }

  location / {
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host \$server_name;
    # enable this if and only if you use HTTPS
    # proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Host \$http_host;
    # we don't want nginx trying to do something clever with
    # redirects, we set the Host: header above already.
    proxy_redirect off;
    proxy_pass http://app_server;
  }

  error_page 500 502 503 504 /500.html;
  location = /500.html {
    root ${TARGETHOME}/hello/static/;
  }
}
EOF
ln -fs /etc/nginx/sites-available/smileycoin-payment-server /etc/nginx/sites-enabled/smileycoin-payment-server
nginx -t
/etc/init.d/nginx reload
