#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

from audioServer import *

def routine(line):
	if line:
		print line

auObj=cAudioServer(routine)
auObj.server()
