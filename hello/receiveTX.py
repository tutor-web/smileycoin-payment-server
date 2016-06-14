#!/usr/bin/python

import sys
from .models import PaymentRequest

print 'CALLING PYTHON!!!!! BO-OOM!'
paymentReq = PaymentRequest(userID="THIS IS JUST FOR TESTING", address=sys.argv[1])
paymentReq.save()
