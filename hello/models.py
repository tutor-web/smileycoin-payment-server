from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class PaymentRequest(models.Model):
    userID = models.CharField(max_length=60)
    address = models.CharField(max_length=60)

class Transaction(models.Model):
    txID = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    amount = models.CharField(max_length=30)
