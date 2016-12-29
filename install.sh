#!/bin/sh
set -ex

TARGETUSER=""
TARGETHOME="/srv/smileycoin-payment-server"
TARGETBIN="${TARGETHOME}/bin/gunicorn"
TARGETDB="${TARGETHOME}/db.sqlite3"
TARGETSECRET="${TARGETHOME}/secret-key.txt"
TARGETUSER="smileycoin-payment-server"
TARGETGROUP="nogroup"

# ---------------------------

id "${TARGETUSER}" 2>/dev/null || adduser --system \
    --home "${TARGETHOME}" --no-create-home \
    --disabled-password \
    ${TARGETUSER}

[ -e "${TARGETDB}" ] || touch -- "${TARGETDB}"
chown ${TARGETUSER}:${TARGETGROUP} "${TARGETDB}"

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
