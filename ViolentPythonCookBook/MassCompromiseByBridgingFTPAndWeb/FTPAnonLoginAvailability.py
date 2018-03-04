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

'''
FTP can be setup so that it's possible to make a connection anonymoysly
(without a username and a password)
instead of a password we give an email
'''

'''
This function determines if the anonymous login is available, and returns a boolean.
'''

import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print('\n[*] ' + str(hostname) +
              ' FTP Anonymous logon Succeeded')
        ftp.quit()
        return True
    except Exception as e:
        print('\n[-] ' + str(hostname) +
              ' FTP Anonymous Logon Failed.')
        return False

host = 'XXX.YYY.ZZZ.ABC'
anonLogin(host)