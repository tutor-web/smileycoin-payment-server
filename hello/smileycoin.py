import uuid
import subprocess

class Smileycoin():

	# Starts the daemon if it isn't already up.
	# Runs the getnewaddress command on the smileycoin daemon.
	def getAddress(self):
		# Check if smileycoind is running and start it if it isnt
	    try:
	        subprocess.check_output('pgrep smileycoind', shell=True)
	    except subprocess.CalledProcessError, e:
	        subprocess.call('./smileycoind --server &', shell=True)
	    finally:
	        # After smileycoind has started, get 10 tries to generate an address
	        # We might need multiple tries because if smileycoind was not running, it
	        # might take a while to start up
	        numTries = 10
	        output = 0
	        while(numTries >= 0):
	            try:
	                output = subprocess.check_output('./smileycoind getnewaddress', shell=True)[:-1]
	            except subprocess.CalledProcessError, e:
	                print "Trying again after 50 ms, ", numTries, " left."
	                numTries = numTries-1
	                time.sleep(0.05)

	        return output

	def getUserID(self):
		return uuid.uuid4()