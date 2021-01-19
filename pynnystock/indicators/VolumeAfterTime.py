
from datetime import time

from ..Utilities import minutesDifference

class VolumeAfterTime:
	'''
	Esse indicador permite verificar o volume em duas tranches de tempo, a primeira sendo do inicío do core
	até o gatilho timeThreshold. A segunda tranche sendo depois de timeThreshold até mais afterTimeThreshold
	minutos.
	'''


	def __init__(self,intra, timeThreshold = 30, afterTimeThreshold = 45):

		self.intra = intra

		self.volBefore = 0
		self.volAfter = 0

		self.timeThreshold = timeThreshold # esse trigger divide o before. Primeira tranche seria 30 minutos depois de aberto
		self.afterTimeThreshold = afterTimeThreshold # esse trigger limita o after. Segunda tranche seria 45 minutos depois 
														# do primeiro gatilho

		for b in self.intra._core:
			elapsedTime = minutesDifference( b['time'].time() ,time(9,31))
			if elapsedTime <= self.timeThreshold:
				self.volBefore += b['volume']
			elif elapsedTime <= self.afterTimeThreshold:
				self.volAfter += b['volume']
			else:
				break


	def getVolumeRate(self):

		if self.volBefore+self.volAfter > 0:
			return self.volBefore/(self.volBefore+self.volAfter)
		else:
			return 0


	def setParameters(timeThreshold = 30, afterTimeThreshold = 45):
		self.timeThreshold = timeThreshold
		self.afterTimeThreshold = afterTimeThreshold


	def __repr__(self):
		s='Volume Fall After Time Rate\n'
		s = s + f"Volume before {self.timeThreshold} minutes threshold: {self.volBefore}\n"
		s = s + f"Volume after first trigger and before second trigger of {self.afterTimeThreshold} minutes: {self.volAfter}\n"

		return s