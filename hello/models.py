from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class PaymentRequest(models.Model):
    address = models.CharField(max_length=60)
    amount = models.DecimalField(decimal_places=2, max_digits=100, default=0.0)
    confirmation = models.BooleanField()
