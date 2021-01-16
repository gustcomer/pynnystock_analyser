# https://www.nelogica.com.br/conhecimento/artigos/indicadores-estudo/vwap
# Aldridge, Irene. “High-frequency trading: a practical guide to algorithmic strategies and trading systems”. 2010. John Wiley & Sons, Inc., Hoboken, New Jersey.
# Leshik, Edward A.; Cralle, Jane. “An introduction to algorithmic trading – basic to advanced strategies”. 2011. John Wiley & Sons Ltd, The Atrium, Southern Gate, Chichester, West Sussex, PO19 8SQ, United Kingdom.
# Berkowitz, Stephen A.; Logue, Dennis E.; Noser, Eugene A. J. “The Total Cost of Transactions on the NYSE”. Journal of Finance (American Finance Association). 1988.

# https://www.investopedia.com/terms/v/vwap.asp

# https://cmcapital.com.br/blog/vwap/
# explica um pouco sobre a questão dos pullbacks relacionados a VWAP

# VWAP = ∑ PxQx ÷ ∑ Qx
# PQt (Preço x Volume Total) = ∑ PxQx
# Vt (Volume Total) = ∑Qx

class VWAP:

	def __init__(self, intra):

		self.intra = intra

		self.PQt = 0
		self.Vt = 0
		self.VWAP = 0

		self.initPre()


	def initPre(self):

		for bar in self.intra._pre:
			self.getNextVWAP(bar)


	def getNextVWAP(self,bar):
		pm = (bar['high']+bar['low']+bar['close'])/3 # preço médio da barra atual
		v = bar['volume'] # volume da barra atual

		self.PQt = self.PQt + pm*v
		self.Vt = self.Vt + v

		self.VWAP = self.PQt/self.Vt

		return self.VWAP


	def __repr__(self):
		s='VWAP\n'
		s = s + f"VWAP barra atual: {self.VWAP}\n"
		s = s + f"∑ PxQx total atual: {self.PQt}\n"
		s = s + f"Volume total atual: {self.Vt}\n"

		return s
