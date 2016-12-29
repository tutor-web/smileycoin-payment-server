# Smileycoin Payment server

This is a django app that can sell voucher codes for SMLY

## Installation

Make sure you have done ``apt-get install python-dev``.

```
virtualenv .
./bin/pip install -r requirements.txt
```

Get a copy of ``db.sqlite3`` if appropriate.

### Production deployment

The ``install.sh`` script will, if run as root:-

* Generate a random secret key
* Create a user to run as
* Create a systemd unit to run it
* Start it up
* Create an NGINX site config file
* Add it to NGINX config
* Reload NGINX

### Development

If just developing, you don't need to install, however you will still need a secret key
of some kind:

```
echo "verysecretkeyguv" > secret-key.txt
```

Also add the smileycoin RPC password:

```
echo "myrpcpassword" > coin-rpc-pass.txt
```

Run the server with:

```
./bin/gunicorn gettingstarted.wsgi --log-file -
```

It should now be listening on port 8000.
