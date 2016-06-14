import subprocess
import time

if __name__ == '__main__':
    # This is deprecated, for now we will not run this as a worker thread,
    # this function is called directly from views.py
    subprocess.call('./smileycoind --server &', shell=True)
    time.sleep(10)
    print subprocess.check_output('./smileycoind getnewaddress', shell=True)