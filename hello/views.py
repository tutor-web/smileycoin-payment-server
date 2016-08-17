from django.shortcuts import render
from django.http import HttpResponse

from .models import PaymentRequest
from .models import Products

import requests
import subprocess
import time
import urlparse
from smileycoin import Smileycoin
from django.middleware import csrf

# Create your views here.
def index(request):
    # Greeting.objects.all().delete()
    # PaymentRequest.objects.all().delete()
    return render(request, 'index.html')

# Create your views here.
def product(request):
    # Greeting.objects.all().delete()
    # PaymentRequest.objects.all().delete()
    csrf.get_token(request)
    return render(request, 'product.html')
 

# Create your views here.
def checkout(request):
    response = request.body
    JSONResponse = '{\"message\": \"Were just testing right now\"}'
    resDict = urlparse.parse_qs(response) # this will put the key=value pairs of the parameters in a dictionary with ARRAY values
    # example: prodID=1&noItems=1&totPrice=50000 => {'totPrice': ['50000'], 'noItems': ['1'], 'prodID': ['1']}
    nItems = int(resDict['noItems'][0])
    prodID = resDict['prodID'][0]
    totPrice = int(resDict['totPrice'][0])

    message = ""
    message = message +"This is the price " + str(totPrice)
    message = message +"This is the calculated amount "+str(nItems*Products.objects.get(prodId = prodID).amount)
    # Check if what we are buying is in stock:
    inStock = isInStock(prodID, nItems)
    if(not inStock):
        message = message + "Error: Item out of stock \t"

    # Calculate the amount
    correctAmount = checkAmount(prodID, nItems, totPrice)
    if(not correctAmount): 
        message = message + "Error: Amount was incorrectly calculated"
    
    # Get the address we need to pay to
    if(inStock and correctAmount):
        address = generateAddress(request)
        message = "Success"
        reserveItems(prodID, nItems)
    else: 
        address = ""
    #data = request.body
    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\", \"amount\":\"',totPrice,'\"}'
    return HttpResponse(JSONResponse)

# =============================
# HELPER FUNCTIONS FOR CHECKOUT
# =============================

def isInStock(prodID, nItems):
    #Products.objects.get(prodId=payment['address'])
    nInStock = Products.objects.get(prodId = prodID).inStock
    return (nInStock >= nItems)

def checkAmount(prodID, nItems, totPrice):
    calculatedAmount = nItems*Products.objects.get(prodId = prodID).amount
    return (calculatedAmount == totPrice)

def reserveItems(prodID, nItems):
    if prodID is not None:
        currentAmount = Products.objects.filter(prodId=prodID).inStock
        afterReserve = currentAmount-nItems
        Products.objects.filter(prodId=prodID).update(inStock = afterReserve, reserved = nItems)

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

    return address

# 
def generateAddressBAK(request):
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

# =====================================================================================


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






