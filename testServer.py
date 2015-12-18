#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioServer import *

# return an object of
def routine(line):
	if line: print line
	return '{"success":1,"message":"in testing","data":""}'

auObj=cAudioServer(routine)
auObj.server()
