from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import requests
import subprocess
import time

# Create your views here.
def index(request):
    # ORIGINAL
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')
    #r = requests.get('http://httpbin.org/status/418')
    #print r.text
    #return HttpResponse('<pre>' + r.text + '</pre>')


def generateAddress(request):
    subprocess.call('./smileycoind --server &', shell=True)
    time.sleep(0.05)
    output = subprocess.check_output('./smileycoind getnewaddress', shell=True)
    return HttpResponse('{address:' +output+'}')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

