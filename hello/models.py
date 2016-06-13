from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Payment(models.Model):
	userId = models.CharField(max_length=30)
	address = models.CharField(max_length=30)