
from datetime import time

from ..Utilities import minutesDifference

class MinBeforeTime:


	def __init__(self,intra, minTime = 5):
		
		self.intra = intra

		self.minTime = minTime

		self.minBar = {}

		self.runCalculation()


	def runCalculation(self):

		self.minBar = self.intra._core[0]

		for b in self.intra._core:
			elapsedTime = minutesDifference( b['time'].time() ,time(9,31) )
			if elapsedTime <= self.minTime:
				if b['low'] < self.minBar['low']:
					self.minBar = b
			else:
				break


	def getLowBeforeMinutes(self):

		return self.minBar['low']


	def getLowPercentBeforeMinutes(self):

		o = self.intra._core[0]['open'] # open
		m = self.getLowBeforeMinutes()

		return m/o - 1


	def setParameters(minTime = 5):

		self.minTime = minTime

		self.runCalculation()


	def __repr__(self):

		s='Minimum Before Time\n'
		s = s + f"Minimum Value Before {self.minTime} minutes: {self.getLowBeforeMinutes()}\n"
		s = s + f"Minimum % Value Before {self.minTime} minutes: {self.getLowPercentBeforeMinutes()}\n"
		s = s + f"Time threshold: {self.minTime}\n"

		return s