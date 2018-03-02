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

def extractFile(zFile, password):

    try:
        zFile.extractall(pwd=password.encode())
        # the extractall method "expected bits" and got "str",
        # so we have to encode
        return password
    except: # incorrect password throws an exception
        return

def main():
    zFile = zipfile.ZipFile('Evil.zip')
    passFile = open('dictionary.txt')
    for line in passFile.readlines():
        password = line.strip('\n')
        guess = extractFile(zFile, password) # our function
        if guess:
            print( '[+] Password = ' + password + '\n')
            exit(0)
if __name__ == "__main__":
    main()
