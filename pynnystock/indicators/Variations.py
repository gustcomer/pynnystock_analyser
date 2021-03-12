
class Variations:

	def __init__(self, intra):

		self.intra = intra

	def openToClosePct(self):
		core = self.intra._core # botando um apelido em self.intra pra facilitar a vida do cabra
		op = core[0]['open'] # open
		cl = core[-1]['close']
		return cl/op-1
