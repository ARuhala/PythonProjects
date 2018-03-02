'''
This is an introduction to nmap
it basically just shows that it's possible to easily index
the output
'''

import nmap # needs to be downloaded at http://xael.org/norman/ python/python-nmap
import optparse
def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print (" [*] " + tgtHost + " tcp/"+tgtPort +" "+state)


def main():
    parser = optparse.OptionParser('usage%prog '+\
            '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', \
             help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', \
             help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)


# attacker:∼# python nmapScan.py -H 10.50.60.125 -p 21, 1720
# [*] 10.50.60.125 tcp/21 open
# [*] 10.50.60.125 tcp/1720 filtered