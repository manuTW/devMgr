#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import sys, os, time

ppName='pipe_test'
lockName='./lock'

def client(string=None):
	acquired=False
	while not acquired:
		if not os.path.exists(lockName):
			os.system('echo '+string+' >'+lockName)
			with open(lockName, 'r') as rfd:
				line=rfd.readline().strip()
				if line == string: acquired=True
		else: time.sleep(1)
	'''
	ppOut=os.open(ppName, os.O_WRONLY)
	string='hello '+string
	print 'sending '+string
	os.write(ppOut, string)
	os.close(ppOut)
	'''
	ppOut=open(ppName, 'w')
	ppOut.writelines('hello %s\n' %string)
	ppOut.close()
	rfd.close()
	os.system('rm '+lockName)

def server():
	print 'In server'
	while True:
		ppIn=open(ppName, 'r')
		line=ppIn.readline()[:-1]
		print line+' from client'
		ppIn.close()

if not os.path.exists(ppName):
	os.mkfifo(ppName)

if len(sys.argv) > 1:
	if sys.argv[1] == 's':
		server()
	else: client(sys.argv[1])
