#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioServer import *

class cTestServer(cAudioServer):
	# Convert a line (json array) to list for processing
	# return a response dict with keys
	#	'success': true/false
	#	'message':<string>
	#	'data':json object (python <dict>
	# Ret : dict type
	def _process(self, line):
		obj=super(cTestServer, self)._process(line)
		if not obj: return self.FORMAT_ERR_RESULT
		print 'Command: '+obj[0]
		if obj[1]:
			print 'Arg: '
			for key in obj[1].keys():
				print '\t'+key+': '+str(obj[1][key])
		else:
			print 'Arg: null'
		print ''
		return self.SUCCESS_RESULT

	def __init__(self):
		super(cTestServer, self).__init__()

obj=cTestServer()
obj.server()
