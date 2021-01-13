
import pandas as pd


class BootstrapSimulator:
	

	def __init__(self, sg):

		self.sg = sg
		self.bsl = [] # Bootstrap List armazena 50 dataframes de trades. Cada um sendo reordenamento do original.


	def runBootstrap(self, n_iter=50, replace=False):

		self.bsl = []

		s = self.sg.tradesdf

		bs_base = s[['profit_real', 'cum_profit_real']]

		prb = bs_base['profit_real'] # Profit Real do Base case (PRB)

		for i in range(0,n_iter):
			random_pr = prb.sample(n = prb.size, replace=replace).reset_index(drop=True)
			random_bs = pd.DataFrame({
										'profit_real':random_pr,
										'cum_profit_real':(1+random_pr).cumprod()
									})

			self.bsl.append(random_bs)

		self.sg.setBootstrapResults(self.bsl)