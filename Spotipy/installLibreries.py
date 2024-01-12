import subprocess
import sys

from tqdm import tqdm

#Funzione per installare un package specifico
def install(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

#Funzione per installare le librerie necessarie
def installPackages():
    packages = []
    with open("requirements.txt", "r") as file:
        packages = file.readlines()
    print("Installing requirements")
    for package in tqdm(packages):
        install(package)

    print("Checking installed packages")
    for package in tqdm(packages):
        install(package)