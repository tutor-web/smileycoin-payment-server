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
    userID = sc.getUserID()
    message = ""

    if( address==0 ):
        message = "Error"
    else:
        message = "Success"
        paymentReq = PaymentRequest(userID=userID, address=address, confirmation="false")
        paymentReq.save()

    # Send csrf as a cookie with the request so the user can be authenticated.
    csrf.get_token(request) 
    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\", \"userID\":\"',userID,'\"}'
    return HttpResponse(JSONResponse)

def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    paymentReqs = PaymentRequest.objects.all()
    return render(request, 'db.html', {'greetings': greetings, 'paymentReqs': paymentReqs})

def postTX(request):
    response = request.body
    if(len(response) > 500): res = "Error"
    else: res = request.body
    print "WALLET NOTIFY: ", res

    txId = request.body
    sc = Smileycoin()
    # payment is a json string of the form {"address" : address, "confirmation" : true/false}
    payment = sc.getPaymentById(txId)
    # Update the database with true or false depending on whether this payment is confirmed
    if payment is not None:
        PaymentRequest.objects.get(address=payment['address']).update(confirmation=payment['confirmation'])
    
    return HttpResponse(str('Raw data is %s' % res))   


def getToken(request):
    token = csrf.get_token(request)
    return HttpResponse(token)









