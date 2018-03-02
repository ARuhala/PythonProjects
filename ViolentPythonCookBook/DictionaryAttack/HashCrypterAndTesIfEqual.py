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
# import crypt # only on unix, doesnt work on windows
'''
crypt is the basic hash function used by unix to encrypt passwords
so they may be stored in a file
crypt function defaults to DES but can be made to use SHA-252 etc.
'''
# i couldn't find a basic library for DES hashes so we are using sha-252
import hashlib
# hash = hashlib.sha256("Egg".encode() ).hexdigest() # 37c50c935cd2a9ad065faec4824b7484acfd2b235c52368ccdb05d1f50240af0

def testPass(cryptPass): # we are going with known salt since it's hard to see it from the sha-256 hash
    dictFile = open('dictionary.txt','r')
    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = hashlib.sha256(word.encode()).hexdigest()
        if (cryptWord == cryptPass ):
            print ("[+] Found Password: " + word + "\n")
            return
    print ("[-] Password not found.")
    return


def main():
    passFile = open('passwords.txt')
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip()
            print("[*] Cracking Password For: " + user)
            testPass(cryptPass)

if __name__ == "__main__":
    main()