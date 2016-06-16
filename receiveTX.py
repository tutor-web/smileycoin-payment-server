#!/usr/bin/python

import sys
from hello.models import PaymentRequest

print 'CALLING PYTHON!!!!! BO-OOM!'
paymentReq = PaymentRequest(userID="THIS IS JUST FOR TESTING", address="Test 2")
paymentReq.save()
