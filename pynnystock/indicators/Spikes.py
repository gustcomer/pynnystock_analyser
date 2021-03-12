
from datetime import time

from ..Utilities import minutesDifference

class Spikes:


	def __init__(self, intra):

		self.intra = intra

		highCoreValue = intra._core[0]['high']
		highCoreTime = intra._core[0]['time'].time()
		highCorePosition = 0

		for b in intra._core:
		    if highCoreValue < b['high']:
		        highCoreValue = b['high']
		        highCoreTime = b['time'].time()
		        highCorePosition = intra._core.index(b)

		self.spike = highCoreValue
		self.spike_minutes = minutesDifference( highCoreTime ,time(9,31))
		self.highCorePosition = highCorePosition

		# calcula o low depois do high
		lowAfterHighValue = intra._core[highCorePosition]['high'] # aqui achei melhor deixar high, se bem que não ia fazer diferença
		lowAfterHighTime = intra._core[highCorePosition]['time'].time()
		lowPositionAfterHigh = highCorePosition

		for b in intra._core[highCorePosition:]: # da high position pra frente
			if lowAfterHighValue > b['low']:
				lowAfterHighValue = b['low']
				lowAfterHighTime = b['time'].time()
				lowPositionAfterHigh = intra._core.index(b)

		self.low_after_high = lowAfterHighValue
		self.low_after_high_minutes = minutesDifference( lowAfterHighTime ,time(9,31))
		self.lowPositionAfterHigh = lowPositionAfterHigh

		self.after_pullback_pct = intra._core[-1]['close']/lowAfterHighValue-1


	def volumeAteMaxima(self):

		volMaxima = 0

		for b in self.intra._core[0 : self.highCorePosition]:
			volMaxima = volMaxima + b['volume']

		return volMaxima