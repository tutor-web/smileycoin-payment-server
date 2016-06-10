import subprocess
import time


if __name__ == '__main__':
    subprocess.call('./smileycoind --server &', shell=True)
    time.sleep(10)
    print subprocess.check_output('./smileycoind getnewaddress', shell=True)
