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
    Greeting.objects.all().delete()
    PaymentRequest.objects.all().delete()
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
        paymentReq = PaymentRequest(userID=userID, address=address)
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
    print "WALLETNOTIFY: We just got notified of transaction with id ", request.body
    return HttpResponse('Raw data is %s' % request.body)   


def getToken(request):
    token = csrf.get_token(request)
    return HttpResponse(token)









