#!/share/CACHEDEV1_DATA/.qpkg/container-station/bin/python

import os, sys, re, argparse, glob, subprocess

g_tmp='/tmp/.udev.rules'
g_ruleFile='/lib/udev/rules.d/50-udev.rules'
g_db='/tmp/.au.db'
g_audTopDir='/sys/class/sound'

#todo a PROGRAM and return result
rule=(
  'ACTION=="add",KERNEL=="controlC0",PROGRAM="/share/Public/udev/mdev.py %p",NAME="snd0/%k",OPTIONS+="last_rule"',
  'ACTION=="add",KERNEL=="controlC1",PROGRAM="/share/Public/udev/mdev.py %p",NAME="snd1/%k",OPTIONS+="last_rule"',
)

class cAudio(object):
	def __init__(self, number):
		self._number=None
		self._classDir=None                  #/sys/class/sound
		self._deviceDir=None                 #/sys/devices/
		classDir=g_audTopDir+'/card'+number
		if not os.path.exists(classDir): return
		self._number=number
		#arrange path
		self._classDir=os.path.abspath(classDir)
		self._deviceDir=g_audTopDir+'/'+os.readlink(classDir)
		self._deviceDir=os.path.abspath(self._deviceDir)
		self._pnpNode=None
		self._devDir='/dev/snd'+self._number
		#get id, i.e. name
		p=subprocess.Popen(['cat '+self._deviceDir+'/id'],
			stdout=subprocess.PIPE, shell=True)
		self._id=p.stdout.read().strip()
		devPath=self._deviceDir
		#looking for remove node
		while True:
			dirName=os.path.dirname(devPath)
			devPath=os.path.basename(devPath)
			if os.path.exists(dirName+'/remove'):
				self._pnpNode=dirName+'/remove'
				break
			if dirName == '/': break
			devPath=dirName
		'''
		print self._id+' (card: '+str(self._number)+')'
		print self._classDir
		print self._deviceDir
		print self._pnpNode
		'''

	#return card#, id
	def getInfo(self):
		if self._number:
			return self._number, self._id

	# move device node between container and system path
	def toggle(self):
		if os.path.exists(self._devDir):
			print 'Move '+self._id+' to system'
			os.system('mv '+self._devDir+'/* /dev/snd')
			os.system('rm -rf '+self._devDir)
		else:
			print 'Move '+self._id+' to Container'
			os.system('mkdir '+self._devDir)
			os.system('mv -f /dev/snd/controlC'+self._number+' '+self._devDir)
			os.system('mv -f /dev/snd/pcmC'+self._number+'* '+self._devDir)
			os.system('mv -f /dev/snd/hwC'+self._number+'* '+self._devDir)
			os.system('mv -f /dev/snd/dsp'+self._number+' '+self._devDir)
			os.system('mv -f /dev/snd/adsp'+self._number+' '+self._devDir)
			os.system('mv -f /dev/snd/mixer'+self._number+' '+self._devDir)

	# device gone
	def remove(self):
		#todo signal stop
		os.system('rm -rf '+self._devDir)
		os.system('rm -f /dev/snd/controlC'+self._number)
		os.system('rm -f /dev/snd/pcmC'+self._number+'*')
		os.system('rm -f /dev/snd/hwC'+self._number+'*')
		os.system('rm -f /dev/snd/dsp'+self._numberi)
		os.system('rm -f /dev/snd/adsp'+self._number)
		os.system('rm -f /dev/snd/mixer'+self._number)

	def add(self):
		#which means our object still exist
		bypass


def check_param():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', action='store', dest='cardNum',
		help='toggle a card in systema and Container')
	parser.add_argument('-i', action='store_true', default=False, dest='info',
		help='show sound card in the database')
	arg=parser.parse_args()
	return arg


def showInfo():
	for dd in glob.glob(g_audTopDir+'/card*'):
		num=re.sub(r'.*card', '', dd)
		obj=cAudio(num)
		num, id=obj.getInfo()
		if os.path.exists('/dev/snd'+num):
			print 'Card '+num+': '+id+' (Container)'
		else:
			print 'Card '+num+': '+id+' (system)'



#main
arg=check_param()
if arg.info: showInfo()
elif arg.cardNum:
	if os.path.exists(g_audTopDir+'/card'+arg.cardNum):
		obj=cAudio(arg.cardNum)
		obj.toggle()

	
