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
Examine the function connect().
This function takes a username, hostname, and password and returns
an SSH connection resulting in an SSH spawned connection.
Utilizing the pexpect library, it then waits for an expected output. 
Three possible expected outputs can occur—a timeout,
a message indicating that the host has a new public key,
or a password prompt. If a timeout occurs, then the session.expect() method 
returns to zero. The following selection statement notices this and prints 
an error message before returning. If the child.expect() method catches
the ssh_newkey message, it returns a 1. This forces the function to send
a message ‘yes’ to accept the new key. Following this, the function waits
for the password prompt before sending the SSH password.
'''
import pexpect
PROMPT = ['#','>>>','> ','\$']

def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, \
                        '[P|p]assword:']) # the argument is a pattern list
    if ret == 0: # timeout occurred
        print ('[-] Error Connecting')
        return
    if ret == 1: # child.expect catched ssh_newkey
        child.sendline('yes')
    ret = child.expect([pexpect.timeout, \
                        '[P|p]assword:']) # we wait for the password prompt
    if ret == 0:
        print('[-] Error Connecting')
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print (child.before)    # class attribute .before is all data received
                            # up until this point

def main():
    host = 'localhost'
    user = 'root'
    password = 'toor'
    child = connect(user, host, password)
    send_command(child, 'cat /etc/shadow | grep root')  # this returns the hashed
                                                        # password of "root"