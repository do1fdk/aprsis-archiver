#!/usr/bin/env python
import socket
import sys
import signal
import time
import bz2
from optparse import OptionParser

aprslog = None
aprssock = None

def cleanup():
    if aprssock:
        print "Closing telnet connection"
        try:
            aprssock.shutdown(0)
        except:
            pass
        try:
            aprssock.close()
        except:
            pass
 
    if aprslog:
        print "Closing APRS log file"
        aprslog.close()

def readlines(sock, recv_buffer=4096, delim='\r\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data
        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            line = line.rstrip('\r\n')
            yield line
    return

def handleSIGTERM(signum, frame):
    print "Catched SIGTERM, shutting down..."
    cleanup()
    sys.exit()

signal.signal(signal.SIGTERM, handleSIGTERM)

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
    help="write APRS log to FILE", metavar="FILE")
parser.add_option("-F", "--filter", dest="filter",
    help="APRS filter string")
# Server config
parser.add_option("-P", "--port", dest="port", type="int",
    help="Server post", default="10152")
parser.add_option("-H", "--host", dest="host",
    help="Server name", default="rotate.aprs2.net")
# User config
parser.add_option("-u", "--user", dest="user",
    help="Server user name", default="N0CALL")
parser.add_option("-p", "--passwd", dest="password",
    help="Server password (-1 for listening receiving)", default="-1")
# Program options
parser.add_option("-v", "--verbose", dest="verbose",
    action="store_true", default=False,
    help="Verbose output")
(options, args) = parser.parse_args()

if not options:
    print "ERROR: No options provided"
    sys.exit()

serverHost = options.host
serverPort = options.port
aprsUser = options.user
aprsPass = options.password 
serverPort = options.port
aprsfilter = options.filter
filename = options.filename

if options.verbose:
    print "Logging to %s" % (filename)
    print "APRS filter %s" % (aprsfilter)

try:
    #aprslog = open(filename, "w")
    aprslog = bz2.BZ2File(filename, "w")
    aprslog.write("# APRS filter: %s\r\n" % (aprsfilter))
    aprslog.write("# Logging start: %s\r\n" % (time.time()))
except IOError, e:
    print "ERROR: Error while creating logging file %s" % (filename), e
    cleanup()
    sys.exit(1)

try:
    aprssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aprssock.connect((serverHost, serverPort))

    if options.verbose:
        print "Connected to %s:%s" % (serverHost, serverPort)
        print "Using user=%s and password=%s" % (aprsUser, aprsPass)

    # Login
    if not aprsfilter:
        aprssock.send('user %s pass %s vers DO1FDK-Python 0.1\n' % (aprsUser, aprsPass))
    else:
        if options.verbose:
            print "Specifying filter %s" % (aprsfilter)
        aprssock.send('user %s pass %s vers DO1FDK-Python 0.1 filter %s\n' % (aprsUser, aprsPass, aprsfilter) )

    for line in readlines(aprssock):
        aprslog.write("%i " % (int(time.time())))
        aprslog.write(line)
        aprslog.write("\n")
except socket.error, msg:
    print "Error while connecting to APRS-IS network, ", msg
    cleanup()
    sys.exit(1);
finally:        
    cleanup()
