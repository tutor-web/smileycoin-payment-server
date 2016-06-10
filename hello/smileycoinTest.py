import subprocess


if __name__ == '__main__':
    print subprocess.check_output('./smileycoind getnewaddress', shell=True)
