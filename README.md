# Smileycoin Payment server

This is a django app that can sell voucher codes for SMLY

## Installation

Make sure you have done ``apt-get install python-dev``.

```
virtualenv .
./bin/pip install -r requirements.txt
```

Get a copy of ``db.sqlite3``, and put it in a ``db`` directory. This should be owned
by the user which will run uWSGI.

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

## Adding items into the database

The ``hello_products`` table contains all available voucher codes for purchase. You can
add some via. the following:

```
sqlite3 db/db.sqlite3
sqlite> INSERT INTO hello_products
    (prodId, prodName, reserved, amount, couponCode, sellerId, timestamp)
    VALUES
    ('0', 'Test purchase', 0, 2, 'ABC-DEF-123', 'FI', '2016-12-29 00:00:00');
```

Note that ``prodId`` / ``prodName`` should be identical for every matching coupon code,
rather than being unique for each line in the table.
