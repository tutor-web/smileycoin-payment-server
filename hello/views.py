from django.shortcuts import render
from django.http import HttpResponse

from .models import PaymentRequest
from .models import Products
from .models import Transaction

import requests
import subprocess
import time
import urlparse
import json
from smileycoin import Smileycoin
from datetime import datetime, timedelta
from django.middleware import csrf

def _getAvailableProducts():
    '''Fetch all possible products for the dropdown menu'''
    return (Products.objects
        .filter(reserved=False)
        .values('prodId', 'prodName')
        .distinct()
        .order_by('prodId'))

# Create your views here.
def index(request):
    # Greeting.objects.all().delete()
    # PaymentRequest.objects.all().delete()
    return render(request, 'index.html', { 'availableProducts': _getAvailableProducts() })

# Create your views here.
def product(request):
    prodID = request.GET.get('prodID', '1')

    # When someone enters our page, we make sure to free all products
    # that were reserved more than 10 minutes ago.
    freeReserved()

    # HAVE TO MAKE SURE ITS NOT OUT OF STOCK!!!
    matchingProducts = Products.objects.filter(prodId=prodID, reserved=False)
    productStock = matchingProducts.count()
    if(productStock <= 0): return render(request, 'outOfStock.html')

    productName = matchingProducts[0].prodName
    productPrice = matchingProducts[0].amount

    # Greeting.objects.all().delete()
    # PaymentRequest.objects.all().delete()
    csrf.get_token(request)
    return render(request, 'product.html', { 'availableProducts': _getAvailableProducts(), 'prodID': prodID, 'productName': productName, 'productPrice': productPrice, 'productStock': productStock})
 
def freeReserved():
    now = datetime.now()
    tenMinutesAgo = now - timedelta(minutes=10)
    Products.objects.filter(reserved=True, timestamp__lt=tenMinutesAgo).update(reserved=False) # Update all reserved from 10 minutes ago

# Create your views here.
def checkout(request):
    # =================
    # For checkout request to be successful, we need to create a
    # payment request of this form:
    # PaymentRequest(userToken_csrf, generatedAddress, totalAmount, JSON describing cart content)
    # =================

    response = request.body
    resDict = urlparse.parse_qs(response) # this will put the key=value pairs of the parameters in a dictionary with ARRAY values
    # example: prodID=1&noItems=1&totPrice=50000 => {'totPrice': ['50000'], 'noItems': ['1'], 'prodID': ['1']}
    
    # SESSION TOKEN
    csrfToken = request.COOKIES.get('csrftoken') 

    # Extract data from request body    
    nItems = int(resDict['noItems'][0])
    prodID = resDict['prodID'][0]
    totPrice = int(resDict['totPrice'][0])

    message = ""

    # Check if what we are buying is in stock:
    inStock = isInStock(prodID, nItems)
    if(not inStock):
        message = message + "Error: Product out of stock. Please try again later."
    else:
        # AMOUNT
        # Calculate the amount
        correctAmount = checkAmount(prodID, nItems, totPrice)
        if(not correctAmount): 
            message = message + "Error: We received a wrong amount for this product."
    
    # ADDRESS
    # Get the address we need to pay to
    if(inStock and correctAmount):
        address = generateAddress(request)
        message = "Success"
        reserveItems(prodID, nItems)
    else: 
        address = ""
    

    # CART JSON
    cartContentsAsJson = createCartJson(prodID, nItems);

    # CREATE THE PAYMENT REQUEST!
    paymentReq = PaymentRequest(sessionToken=csrfToken, status="UNPAID", address=address, cost=totPrice, amount=0.0, cartJSON=cartContentsAsJson) #EDIT THIS LINE session - address - amount - cartJson
    paymentReq.save()



    JSONResponse = '{\"message\":\"',message,'\", \"address\":\"',address,'\", \"amount\":\"',totPrice,'\"}'
    return HttpResponse(JSONResponse)

# =============================
# HELPER FUNCTIONS FOR CHECKOUT
# =============================

def generateAddress(request):
    sc = Smileycoin()
    address = sc.getAddress()
    message = ""

    if( address==0 ):
        message = "Error"
    else:
        message = "Success"

    return address


# Later on, when the site will be adapted to hold multiple
# products, this needs to be written so that it can accept an array
# of product id's and their totals. This will do for now.
# The JSON should be of the form:
# {1: {product: prodID, howMany: n}, 2: {product: prodID, howMany: n}, 3: {product: prodID, howMany: n}, ...}
def createCartJson(prodId, total):
    return '{"1": { "product": "'+str(prodId)+'", "nItems": "'+str(total)+'" }}'



def isInStock(prodID, nItems):
    #Products.objects.get(prodId=payment['address'])
    nInStock = Products.objects.filter(prodId=prodID, reserved=False).count()
    return (nInStock >= nItems)

def checkAmount(prodID, nItems, totPrice):
    calculatedAmount = nItems*Products.objects.filter(prodId = prodID)[0].amount
    return (calculatedAmount == totPrice)

def reserveItems(prodID, nItems):
    ids = Products.objects.filter(prodId=prodID).values_list('id', flat=True)

    if prodID is not None:
        for i in range(0, nItems):
            product = Products.objects.filter(prodId=prodID, reserved=False, id=ids[i]).update(reserved=True, timestamp=datetime.now())

def freeItems(prodID, nItems):
    ids = Products.objects.filter(prodId=prodID).values_list('id', flat=True)

    if prodID is not None:
        for i in range(0, nItems):
            Products.objects.filter(prodId=prodID, reserved=True, id=ids[i]).update(reserved=False)

# =====================================================================================


def db(request):

    paymentReqs = PaymentRequest.objects.all()
    return render(request, 'db.html', {'paymentReqs': paymentReqs})

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
         print PaymentRequest.objects.filter(address=payment['address']).update(amount = float(currAmount)+float(payment['amount']))
         print payment['confirmations']
         # Also update Transaction table, add new entry for the txID if necessary, or just update
         # confirmations on the existing one:
         matchingTransactions = Transaction.objects.filter(txID = txId)
         if(matchingTransactions.count() <= 0):
            transaction = Transaction(txID = txId, confirmations = payment['confirmations'])
            transaction.save()
         else:
            transaction = Transaction.objects.filter(txID = txId).update(confirmations = payment['confirmations'])
    
    return HttpResponse("TRANSACTION POSTED with address %s, amount %s and confirmations %s", payment['address'], payment['amount'], payment['confirmations'])   


def getToken(request):
    token = csrf.get_token(request)
    return HttpResponse(token)

def verifyPayment(request):
    # Get the users payment request from the database by his token
    addressFromUser = request.body
    csrfToken = request.COOKIES.get('csrftoken') 
    matchingPayments = PaymentRequest.objects.filter(sessionToken=csrfToken, address=addressFromUser).exclude(status="COMPLETE")

    if len(matchingPayments) is not 0:
        payment = matchingPayments[0]
    else:
        return HttpResponse('{"Error: ": We found no payment matching your query. Please send an e-mail to educationinasuitcase@gmail.com if you paid for your product but didn\'t receive any.')

    fullyPaid = False
    # Our response should depend on whether or not the payment has been completed successfully:
    requiredAmount = payment.cost
    paidAmount = payment.amount

    if(requiredAmount <= paidAmount): 
        fullyPaid = True
        PaymentRequest.objects.filter(sessionToken=csrfToken, address=addressFromUser).update(status="PAID")

    if(fullyPaid): 
        prodsJSON = getProducts(payment.cartJSON) # This is a json of the coupons that we will add in the other json
        verificationJSON = '{"status": "PAID", "address": "'+str(payment.address)+'", "amount": "'+str(payment.amount)+'", "coupon": '+prodsJSON+'}' 
        PaymentRequest.objects.filter(sessionToken=csrfToken, address=addressFromUser).update(status="COMPLETE")
    else:
        verificationJSON = '{"status": "UNPAID", "address": "'+str(payment.address)+'", "amount": "'+str(payment.amount)+'"}'

    if payment is not None:
        return HttpResponse(verificationJSON)
    else:
        return HttpResponse('{"Error: ": "We couldn\'t verify your payment at this time. Please send an e-mail to educationinasuitcase@gmail.com if the problem persists."}')




# Getting products from database
# cartJsonString looks like this: {1: {product: prodID, nItems: n}, 2: {product: prodID, nItems: n}, 3: {product: prodID, howMany: n}, ...}
# coupons will be {1: {prodName: name, code: couponcode}, 2: ...}
def getProducts(cartJsonString):
    prodJson = '{'
    codeList = []

    jobj = json.loads(cartJsonString)
    for key in jobj:
        nOfProd = jobj[key]["nItems"]

        # We need to get nOfProd coupons of type 'product'
        for i in range(0,int(nOfProd)):
            prodID = jobj[key]["product"]
            reservedItems = Products.objects.filter(prodId = prodID, reserved=True)
            
            # If the user made it to this page but session expired even though they already 
            # paid the amount (this should only happen if user takes more than 10 minutes to pay)
            if(reservedItems.count() <= 0): 
                if(isInStock(prodID, 1)):
                    reserveItems(prodID, 1)
                    reservedItems = Products.objects.filter(prodId = prodID, reserved=True)
                else:    
                    smallJson = '"'+str(i)+'": {"product": "Product Out of Stock", "code": "Please Contact Education in a Suitcase"}'
                    codeList.append(smallJson)
                    break;

            product = reservedItems[0].prodName
            code = reservedItems[0].couponCode
            smallJson = '"'+str(i)+'": {"product": "'+product+'", "code": "'+code+'"}'
            codeList.append(smallJson)
            Products.objects.filter(couponCode = code).delete()



    for i in range(0, len(codeList)):
        prodJson += codeList[i]
        if(i < len(codeList)-1): prodJson += ', '

    return prodJson+'}';