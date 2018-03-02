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
import sys
'''
sys is used to parse commandline arguments at runtime

> programmer$ python vuln-scanner.py vuln-banners.txt
sys.argv[0] == vuln-scanner.py
sys.argv[1] == vuln-banners.txt
'''
import os
'''
os is used for filepath management and checking rights
'''
if len(sys.argv) == 2:
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print( '[-]' + filename + ' does not exist.') # in this directory
        exit(0)
    if not os.access(filename, os.R_OK):    # checks if user had READ rights to the file
                                            # Chmod 000 filename.txt    # for setting the rights on unix
        print( '[-]' + filename + ' access denied.')
        exit(0)

    print ("[+] Reading Vulnerabilities From: " + filename)
