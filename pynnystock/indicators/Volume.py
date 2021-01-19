
class Volume:


	def __init__(self, intra):

		self.intra = intra


	def volumePreMarket(self):

		# calcula volume pre market
		volPre = 0
		for b in self.intra._pre:
			volPre = volPre + b['volume']
		return volPre


	def volumeCoreMarket(self):

		# calcula volume core market
		volCore = 0
		for b in self.intra._core:
			volCore = volCore + b['volume']
		return volCore


	def volumePosMarket(self):

		# calcula volume pos market
		volPos = 0
		for b in self.intra._pos:
			volPos = volPos + b['volume']
		return volPos


	def __repr__(self):

		s='Volume\n'
		s = s + f"Volume Pre Market: {self.volumePreMarket()}\n"
		s = s + f"Volume Core Market: {self.volumeCoreMarket()}\n"
		s = s + f"Volume Pos Market: {self.volumePosMarket()}\n"

		return s