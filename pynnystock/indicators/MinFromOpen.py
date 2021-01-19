# como calcular mínimo e máximo de algum elemento de dict de uma lista de dicts
# https://stackoverflow.com/questions/5320871/in-list-of-dicts-find-min-value-of-a-common-dict-field

class MinFromOpen:


	def __init__(self,intra):

		self.intra = intra

		self.minBar = min(self.intra._core,key=lambda x:x['low'])


	def getMinFromOpen(self):
		return self.minBar['low']


	def getMinFromOpenPercent(self):
		o = self.intra._core[0]['open'] # o: open
		m = self.minBar['low'] # m: ´min

		return m/o - 1

