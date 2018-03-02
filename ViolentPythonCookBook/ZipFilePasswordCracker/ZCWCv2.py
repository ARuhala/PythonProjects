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

# this is a version of the ZipCrackerWithConcurrency
# where zipfiles name and the dictionarys name
# are parsed from the commandline
# example: programmer$ python unzip.py -f evil.zip -d dictionary.txt
import zipfile
import optparse
from threading import Thread

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password.encode())
        print('[+] Found password ' + password+ '\n')
    except:
        pass

def main():
    parser = optparse.OptionParser("usage%prog "+\
                                  "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',\
                      help='specify zip file')
    # after '-f' on command line, store it's destination as a string to parser

    parser.add_option('-d', dest='dname', type='string',\
                      help='specify dictionary file')
    # after '-d' store it's destination as a string to parser
    (options, args) = parser.parse_args() # arguments are stored in options, from parser

    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        # targets our function
        # passes zFile and password as arguments to the function
        t.start()
if __name__ == "__main__":
    main()