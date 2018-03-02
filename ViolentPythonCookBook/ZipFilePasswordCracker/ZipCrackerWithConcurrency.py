'''
This file is part of examples shown in a book
"Violent Python Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers"
Most of the code is copied as is, or with minor changes to make naming easier to understand and some
comments may have been added where i explain to myself how everything works ( the code is not just blindly copied ).
The purpose of these files is for me to understand how the code works and become better at the security field.
------------
Antti Ruhala, Tampere University of Technology
------------
'''
import zipfile
from threading import Thread
def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password.encode())
        print('[+] Found password ' + password+ '\n')
    except:
        pass

def main():
    zFile = zipfile.ZipFile('Evil.zip')
    passFile = open('dictionary.txt')

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        # targets our function
        # passes zFile and password as arguments to the function
        t.start()
if __name__ == "__main__":
    main()