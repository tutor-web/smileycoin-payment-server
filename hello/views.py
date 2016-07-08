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
        paymentReq = PaymentRequest(address=address, amount=0.0, confirmations=0)
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
 
    # Current amount of this address (in case customer pays in several transactions
    existingRequest = PaymentRequest.objects.get(address=payment['address'])
    if existingRequest is not None: currAmount = existingRequest.amount
    else: currAmount = 0.0

    # Update the database with true or false depending on whether this payment is confirmed
    if payment is not None:
         print PaymentRequest.objects.filter(address=payment['address']).update(amount = float(currAmount)+float(payment['amount']), confirmations=payment['confirmations'])
         print payment['confirmations']
    
    return HttpResponse("TRANSACTION POSTED (unless some error occurred...) with address %s, amount %s and confirmations %s", payment['address'], payment['amount'], payment['confirmations'])   


def getToken(request):
    token = csrf.get_token(request)
    return HttpResponse(token)

def verifyPayment(request):
    customerAddress = request.body
    print "CUSTOMER ADDRESS IS ", customerAddress
    payment = PaymentRequest.objects.get(address=customerAddress)
    print "PAYMENT IS ", payment
    if payment is not None:
	res = "Customer address was "+customerAddress+" and we received payment "+str(payment)
        return HttpResponse('{"address": "'+payment.address+'", "amount": "'+str(payment.amount)+'" }')
    else:
        return HttpResponse('{"Error: ": "?"}')






