
class Trade:


	def __init__(self, intra):

		self.intra = intra


	def isSuccessful(self):

		return True if self.intra._core[-1]['close'] < self.intra._core[0]['open'] else False