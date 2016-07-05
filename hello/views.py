from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import PaymentRequest

import requests
import subprocess
import time
from smileycoin import Smileycoin
from django.middleware import csrf

# Create your views here.
def index(request):
    # Greeting.objects.all().delete()
    # PaymentRequest.objects.all().delete()
    return render(request, 'index.html')
 
# 
def generateAddress(request):
    sc = Smileycoin()
    address = sc.getAddress()
    message = ""

    if( address==0 ):
        message = "Error"
    else:
        message = "Success"
        paymentReq = PaymentRequest(address=address, amount=0.0, confirmation=False)
        paymentReq.save()

    # Send csrf as a cookie with the request so the user can be authenticated.
    csrf.get_token(request) 
    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\"}'
    return HttpResponse(JSONResponse)

def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    paymentReqs = PaymentRequest.objects.all()
    return render(request, 'db.html', {'greetings': greetings, 'paymentReqs': paymentReqs})

def postTX(request):
    txId = request.body
    sc = Smileycoin()
    # payment is a json string of the form {"address" : address, "confirmation" : true/false}
    payment = sc.getPaymentById(txId)
    # Update the database with true or false depending on whether this payment is confirmed
    if payment is not None:
         print PaymentRequest.objects.filter(address=payment['address']).update(amount = payment['amount'], confirmation=payment['confirmation'])
         print payment['confirmation']
    
    return HttpResponse("TRANSACTION POSTED (unless some error occurred...) with address %s, amount %s and confirmation status %s", payment['address'], payment['amount'], payment['confirmation'])   


def getToken(request):
    token = csrf.get_token(request)
    return HttpResponse(token)

def verifyPayment(request):
    address = request.body
    payment = PaymentRequest.objects.filter(address=address)
    if payment is not None:
        return HttpResponse(payment)
    else:
        return HttpResponse('{"Error: ": "?"}')






