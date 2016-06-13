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
    # Check if smileycoind is running and start it if it isnt
    try:
        # pgrep for the smileycoin daemon to see if its
        # already running, if not, this issues a CalledProcessError
        subprocess.check_output('pgrep smileycoind', shell=True)
    except CalledProcessError, e:
        # Smileycoin is not already running!
        print "Starting smileycoind..."
        subprocess.call('./smileycoind --server &', shell=True)
    finally:
        # After smileycoind has started, get 10 tries to generate an address
        # We might need multiple tries because if smileycoind was not running, it
        # might take a while to start up
        numTries = 10
        while(numTries >= 0):
            try:
                output = subprocess.check_output('./smileycoind getnewaddress', shell=True)[:-1]
                return HttpResponse('{\"address\":\"'+output+'\"}')
            except CalledProcessError, e:
                print "Trying again after 50 ms, "+numTries+" left."
                numTries = numTries-1
                time.sleep(0.05)
    return HttpResponse('{\"address\":\"We couldnt find you an address at this time\"')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

