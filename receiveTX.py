#!/usr/bin/python

import sys
from hello.models import PaymentRequest

print 'CALLING PYTHON!!!!! BO-OOM!'
paymentReq = PaymentRequest(userID="THIS IS JUST FOR TESTING", address="afraid that sysargv[1] would do some damage")
paymentReq.save()
