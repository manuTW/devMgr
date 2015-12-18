#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import sys, os, time, json

class cAudioCmd(object):
	WPIPE_NAME='/tmp/.auwpp'              #client's direction
	RPIPE_NAME='/tmp/.aurpp'
	LOCK_NAME='/tmp/.lock.aupp'

	# create pipe if not yet
	def __init__(self):
		if not os.path.exists(self.WPIPE_NAME):
			os.mkfifo(self.WPIPE_NAME)
			os.mkfifo(self.RPIPE_NAME)
			os.chmod(self.WPIPE_NAME, 0o777)
			os.chmod(self.RPIPE_NAME, 0o777)

	# todo, time limit, say if server doesn't exist
	def _acquire(self):
		acquired=False
		myID=str(os.getpid())
		while not acquired:
			if not os.path.exists(self.LOCK_NAME):
				os.system('echo '+myID+' >'+self.LOCK_NAME)
				os.chmod(self.LOCK_NAME, 0o777)
			with open(self.LOCK_NAME, 'r') as rfd:
				ownerID=rfd.readline().strip()
				if ownerID == myID:
					acquired=True
				else:
					if not os.path.exists('/proc/'+ownerID):
						os.system('rm -f '+self.LOCK_NAME)
				rfd.close()

	def _release(self):		
		os.system('rm -f '+self.LOCK_NAME)

	# sending command to server
	# todo, it blocks if server not present
	def command(self, cmd=None):
		self._acquire()
		#access pipe
		try:
			ppOut=open(self.WPIPE_NAME, 'wt')
			ppOut.writelines('%s\n' %cmd)
			ppOut.close()
			ppIn=open(self.RPIPE_NAME, 'r')
			#format = success:[0|1], message:<mesg string>, data:<data object>
			ret=ppIn.readline()
			ppIn.close()
			data=json.loads(ret)
			if data['success']: print 'Success'
			else:
				print 'Fail: '+data['message']
				print 'Data: '+data['data']
		except:
			pass
		self._release()

#[ {"cmd":"add", } ]

if __name__ == '__main__':
	obj=cAudioCmd()
	if len(sys.argv) > 1:
		obj.command(sys.argv[1])
	else:
		obj.command('add')


