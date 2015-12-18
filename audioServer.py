#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioCmd import *

class cAudioServer(cAudioCmd):
	RESULT='{"success":1,"message":"","data":""}'
	# In : routine - to process the input json and return the result in another json object
	#
	def __init__(self, routine=None):
		self._proc=routine
		super(cAudioServer, self).__init__()

	#supposed to be called by server
	def server(self):
		while True:
			try:
				ppIn=open(self.WPIPE_NAME, 'r')
				line=ppIn.readline()[:-1]
				ppIn.close()
				if self._proc:
					ret=self._proc(line)
				else: ret=self.RESULT
				ppOut=open(self.RPIPE_NAME, 'wt')
				ppOut.writelines('%s\n' %ret)
				ppOut.close()
			except:
				print '\nProgram exits'
				break

