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

# this program scans TCP ports and checks if they react
# we are looking for listening TCP ports

# This is a Connect-scan
# it basically does the 3 way handshake until the end
# which means it's quite easy to get caught if it is used

# SYN, ACK etc scans require python NMAP to be installed
#  http://xael.org/norman/ python/python-nmap

# each port lookup has been threaded for faster scanning speed

import optparse
from threading import Thread, Semaphore
from socket import *


screenLock = Semaphore(value=1) # this is a threading lock
                                # that allows just one thread to advance
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)  # AF_INET takes ip, port
        connSkt.connect((tgtHost, tgtPort))     # SOCK_STREAM means its a tcp socket
        connSkt.send('EXAMPLESTRING\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        print ('[+]%d/tcp open'% tgtPort)
        print ('[+] ' + str(results))
    except:
        screenLock.acquire()
        print ('[-]%d/tcp closed'% tgtPort)
    finally:                                    # this is ran ALWAYS no matter what happens
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost) #returns IPv4 addr
    except:
        print("[-] Cannot resolve '%s': Unknown host")%tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP) # returns hostname, aliaslist, ipaddrlist
        print("\n[+] Scan Results for:" + tgtName[0])
    except:
        print("\n[+] Scan results for: " + tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser = optparse.OptionParser("usage%prog "+\
                      "-H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string', \
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', \
                      help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print ('[-] You must specify a target host and port[s].')
        exit(0)
    portScan(tgtHost, tgtPorts)

# attacker:∼# python portScan.py -H 10.50.60.125 -p 21, 1720
# [+] Scan Results for: 10.50.60.125
# [+] 21/tcp open
# [+] 220- Welcome to this Xitami FTP server
# [-] 1720/tcp closed
