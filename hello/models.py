from django.db import models


class Products(models.Model):
	prodId = models.IntegerField(default=0)
	prodName = models.CharField(max_length=60)
	sellerId = models.CharField(max_length=60)
	amount = models.IntegerField(default=0)
	couponCode = models.CharField(max_length=60, default="0000000")
	reserved = models.BooleanField(default=False)

# A Payment request is created when the user requests to pay for
# his products.
# Payment request should have the address that was generated for the payment
# and the total amount.
class PaymentRequest(models.Model):
	sessionToken = models.CharField(max_length=60)
	status = models.CharField(max_length=60) # Should be one of Unpaid, Paid, Complete. Never give out coupons for payment requests that have been completed.
	address = models.CharField(max_length=60)
	cost = models.IntegerField(default=0)
	amount = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
	cartJSON = models.CharField(max_length=300) # Describes the content of the cart as JSON, so : {"prodId1": "1", "prodId2" : "1"}

class Transaction(models.Model):
    txID = models.CharField(max_length=60)
    confirmations = models.IntegerField(default=0)
