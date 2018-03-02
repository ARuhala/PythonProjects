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

# this program scans TCP ports and checks if they react to
# random garbage data sent to them
# we are looking for listening TCP ports

import optparse

from socket import *

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)  # AF_INET takes ip, port
        connSkt.connect((tgtHost, tgtPort))     # SOCK_STREAM means its a tcp socket
        connSkt.send('EXAMPLESTRING\r\n')
        results = connSkt.recv(100)
        print ('[+]%d/tcp open'% tgtPort)
        print ('[+] ' + str(results))
        connSkt.close()
    except:
        print ('[-]%d/tcp closed'% tgtPort)

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host")%tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan Results for:" + tgtName[0])
    except:
        print("\n[+] Scan results for: " + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print("Scanning port " + tgtPort)
        connScan(tgtHost, int(tgtPort))

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

# example terminal run
# attacker$ python portscanner.py -H 192.168.1.37 -p 21, 22, 80
# [+] Scan Results for: 192.168.1.37
# Scanning port 21
# [+] 21/tcp open [+] 220 FreeFloat Ftp Server (Version 1.00).

