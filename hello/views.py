from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Payment

import requests
import subprocess
import time
from smileycoin import Smileycoin
from django.middleware import csrf

# Create your views here.
def index(request):
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
        payment = Payment(userID=userID, address=address)
        payment.save()

    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\", \"userID\":\"',userID,'\"}'
    return HttpResponse(JSONResponse)

def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    payments = Payment.objects.all()
    return render(request, 'db.html', {'greetings': greetings, 'payments': payments})

def postTX(request):
    if request.method == 'POST':
        return HttpResponse('Raw data is %s' % request.body)   
    if request.method == 'GET':
        return HttpResponse('You posted a get request')

def getToken(request):
    csrf.get_token(request)
    return HttpResponse('Check your cookies')















