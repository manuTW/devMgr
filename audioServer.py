#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioCmd import *

class cAudioServer(cAudioCmd):
	def __init__(self, routine=None):
		self._proc=routine
		super(cAudioServer, self).__init__()

	#supposed to be called by server
	def server(self):
		while True:
			try:
				ppIn=open(self.PIPE_NAME, 'r')
				line=ppIn.readline()[:-1]
				ppIn.close()
				if self._proc: self._proc(line)
			except:
				print '\nProgram exits'
				break

