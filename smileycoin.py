import subprocess


if __name__ == '__main__':
    subprocess.call('./smileycoind --server &', shell=True)
    print subprocess.check_output('./smileycoind getnewaddress', shell=True)
