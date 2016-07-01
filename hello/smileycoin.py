import uuid
import subprocess
import time
import json

class Smileycoin():

    # Starts the daemon if it isn't already up.
    # Runs the getnewaddress command on the smileycoin daemon.
    def getAddress(self):
        # Check if smileycoind is running and start it if it isnt
        try:
            print "pgrepping for smileycoin daemon"
            print subprocess.check_output('pgrep smileycoind', shell=True)
            print "seems the daemon is already running, continue ..."
        except subprocess.CalledProcessError, e:
            print "CalledProcessError occurred, starting smileycoind ..."
            # Confirmed to be the correct way to call daemon for wallet notify
            subprocess.call('./smileycoind --server &', shell=True)
            print "Smileycoin daemon started"
        finally:
            # After smileycoind has started, get 10 tries to generate an address
            # We might need multiple tries because if smileycoind was not running, it
            # might take a while to start up
            print "take 10 tries to get the new address"
            numTries = 10
            output = 0
            while(numTries >= 0):
                try:
                    print "trying to get new address ..."
                    output = subprocess.check_output('./smileycoind getnewaddress airlineAccount', shell=True)
                    print "output before: ", output
		    print "output length: ", len(output)
                    output = output[:-1]
                    print "output after:  ", output
		    print "output length: ", len(output)
                    break
                except subprocess.CalledProcessError, e:
                    print "Getnewaddress failed. Trying again after 50 ms, ", numTries, " left."
                    numTries = numTries-1
                    time.sleep(0.05)

            print "While loop finished, returning ..."
            return output

    def getUserID(self):
        return str(uuid.uuid4())

    def getPaymentById(self, txid):
    	try:
            print "pgrepping for smileycoin daemon"
            print subprocess.check_output('pgrep smileycoind', shell=True)
            print "seems the daemon is already running, continue ..."
        except subprocess.CalledProcessError, e:
            print "CalledProcessError occurred, starting smileycoind ..."
            # Confirmed to be the correct way to call daemon for wallet notify
            subprocess.call('./smileycoind --server &', shell=True)
            print "Smileycoin daemon started"
        finally:
            # After smileycoind has started, get 10 tries to generate an address
            # We might need multiple tries because if smileycoind was not running, it
            # might take a while to start up
            print "take 10 tries to get the transaction"
            numTries = 10
            txJSON = 0
            while(numTries >= 0):
                try:
                    print "trying to get transaction information ..."
                    txJSON = subprocess.check_output('./smileycoind gettransaction '+txid, shell=True)[:-1]
                    break
                except subprocess.CalledProcessError, e:
                    print "gettransaction failed. Trying again after 50 ms, ", numTries, " left."
                    numTries = numTries-1
                    time.sleep(0.05)

            print "While loop finished, parsing json ..."
            # JSON will look like this:
	    	#
	    	# 	amount
	    	# 	confirmation
	    	# 	txid
	    	# 	time
	    	# 	details
	    	#		account
	    	#		address
	    	#		category
	    	#		amount
	    	#		fee
            
            if( txJSON != 0 ): 
		print "THIS IS THE JSON"
		print txJSON
                txObj = json.loads(txJSON)
                amount = txObj["amount"]
		expectedAmount = 1.0
                address = txObj["details"][0]["address"]
		paymentJSON = '{"address" :"'+ address+'", "confirmation" : "'+str(amount >= expectedAmount)+'", "message" : "Payment of '+str(amount)+' paid to address '+address+'"}'
		print "PAYMENT JSON: ", paymentJSON
                return json.loads(paymentJSON)
            else:
                return None
            


























