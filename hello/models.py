from django.db import models

# This is a dummy model, removing it should be ok
# class Greeting(models.Model):
#    when = models.DateTimeField('date created', auto_now_add=True)

# We need
#	- A table that has our 'stock' of items that we sell
#		* This table should be prodId - prodName - inStock - reserved
#	- A table that has a list of transactions, txID only? Maybe more?
#	- Obviously, payment request needs to be here still
#	How will the server handle purchase request? The client will send something
#   like "I want to purchase 2 tickets" and the server needs to respond with "well 2 tickets, that will be
#   100.000 SMLY to address XXXXXXXXX, please".
#	The server can do this by talking directly with the stock table and payment request table.

class Products(models.Model):
	prodId = models.IntegerField(default=0)
	prodName = models.CharField(max_length=60)
	amount = models.IntegerField(default=0)
	inStock = models.IntegerField(default=0)
	reserved = models.IntegerField(default=0)

class PaymentRequest(models.Model):
    address = models.CharField(max_length=60)
    amount = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    confirmations = models.IntegerField(default=0)

class Transaction(models.Model):
    txID = models.CharField(max_length=60)
