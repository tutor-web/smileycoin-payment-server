#!/usr/bin/python

import sys
from models import PaymentRequest

print 'CALLING PYTHON!!!!! BO-OOM!'
paymentReq = PaymentRequest(userID="THIS IS JUST FOR TESTING", address="This is also just for testing")
paymentReq.save()
