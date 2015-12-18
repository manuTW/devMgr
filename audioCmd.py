#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import sys, os, time

class cAudioCmd(object):
	PIPE_NAME='/tmp/.aupp'
	LOCK_NAME='/tmp/.lock.aupp'

	# create pipe if not yet
	def __init__(self):
		if not os.path.exists(self.PIPE_NAME):
			os.mkfifo(self.PIPE_NAME)
			os.chmod(self.PIPE_NAME, 0o777)

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
			ppOut=open(self.PIPE_NAME, 'wt')
			ppOut.writelines('%s\n' %cmd)
			ppOut.close()
		except:
			pass
		self._release()

if __name__ == '__main__':
	obj=cAudioCmd()
	if len(sys.argv) > 1:
		obj.command(sys.argv[1])
	else:
		obj.command('add')


