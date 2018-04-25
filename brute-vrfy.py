#!/usr/bin/python
import sys
import socket
import getopt

appended=0
#check parameters 
if len(sys.argv) < 3: 
  print "Syntax: ./vrfy.py <hostname> <wordlist-file> --argument=string-to-expand"
  sys.exit(0)
# Create a Socket
opts, args = getopt.getopt(sys.argv[3:],"ha:",["append="])
for opt, arg in opts: 
  if opt in ("-a", "--append"):
    string_to_append = arg
    appended = 1 
if appended == 1:
  print "String to append:"+string_to_append

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
connect=s.connect((sys.argv[1],25))

# Receive the banner
banner=s.recv(1024)
print banner

# VRFY a user
f = open(str(sys.argv[2]), "r")
for line in f:
  if appended == 0:
    s.send('VRFY ' +line+'\r')
  else:
    s.send('VRFY ' +line+string_to_append+'\r')

  result=s.recv(1024)
  if result.startswith(('550')):
    continue 
  if result.startswith(('252')):
    print "OK - "+line
  if result.startswith(('502')):
    print "VRFY  doesn't seem to be supported by this server, Output: "+result
    sys.exit(0)
  if result.startswith(('502')):
    print "Address rejected - try --append option, Output: "+result
    sys.exit(0)
  
  if result.startswith(('504')):
    print "Server needs \"need fully-qualified address\", try --append=@domain option to add the @FQDN of the server"
    sys.exit(0)
  else: 
    print result
    sys.exit(0)

# Close the socket
s.close()
