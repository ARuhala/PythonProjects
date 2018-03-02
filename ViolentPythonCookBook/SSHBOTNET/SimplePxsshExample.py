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
'''
pxssh contains methods login(), logout() and prompt()
'''
def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before)

def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print ('[-] Error Connecting')
        exit(0)

# s = connect('127.0.0.1', 'root', 'toor')
# send_command(s, 'cat /etc/shadow | grep root')