from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from .models import Payment

import requests
import subprocess
import time
from smileycoin import Smileycoin

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
        '''
        payment = Payment(userID=userID, address=address)
        payment.save()'''

    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\", \"address\":\"',userID,'\"}'
    return HttpResponse(JSONResponse)

def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    # payments = Payment.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

