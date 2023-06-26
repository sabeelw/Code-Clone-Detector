import subprocess
import sys

def install_requirements():
    subprocess.check_call(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call(["./joern/joern-install.sh"])
if __name__ == '__main__':
    install_requirements()

