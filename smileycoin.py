import subprocess


if __name__ == '__main__':
    subprocess.call('./smileycoind --server &', shell=True)
    print 'Weve called the smileycoind daemon to start'
    print subprocess.check_output('./smileycoind getnewaddress', shell=True)
