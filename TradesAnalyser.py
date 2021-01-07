import FileManager as fman
import pandas as pd
import numpy as np
import datetime
import Ativo as at
import pickle
from Utilities import drawdown
import Parameters
from matplotlib import pyplot as plt



# Essa versão vai incluir position sizing em duas etapas. Provavelmente essa versão será descontinuada e só
# existirá enquanto o software não possuir módulos flexíveis.
class TradesAnalyser():
	'''
	Calcula os Trades e analisa eles
	'''
	def __init__(self, adl):
		self.fm = fman.FileManager()
		self.adl = adl # ADL: Ativos-Dias List
		self.fad = [] # FAD: Filtered Ativos-Dias
		self.trades = [] # trade results from last simulation
		self.n_trades = 0 # number of non-None trades

		self.parameters = Parameters.ParametersSimple()

		self.results = pd.DataFrame()

		self.bs_base = pd.DataFrame() # caso base do bootstrap
		self.bsl = [] # Boot Strap List: uma lista com varios dataframes. Cada df, uma combinação de trades.


	def printSimResults(self):

		print('prevol_threshold', self.parameters.prevol_threshold)
		print('open_dolar_threshold', self.parameters.open_dolar_threshold)
		print('gap_threshold', self.parameters.gap_threshold)
		print('F_low_threshold', self.parameters.F_low_threshold)
		print('F_high_threshold', self.parameters.F_high_threshold)

		print('')

		print('short_after', self.parameters.short_after)
		print('exit_target', self.parameters.exit_target)
		print('exit_stop', self.parameters.exit_stop)

		print('')

		print('start_money', self.parameters.start_money)
		print('allocation', self.parameters.allocation)
		print('locate_fee', self.parameters.locate_fee)
		print('commission', self.parameters.commission)

		print('')

		start = self.parameters.start_money
		print('Start Money:', '${:,.2f}'.format(start) )

		end_money = self.getEndMoney()
		print('End Money:', '${:,.2f}'.format(end_money) )
		print('Max Drawdown:', self.getMaxDrawdown() )
		print('Number of Trades:', self.n_trades)
		print('Number of filtered ativo-dias:', len(self.fad) )


	def plotHistMinsToTrade(self, bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]):
		dft = self.getTrades()

		plt.hist( np.clip( dft['mins_to_trade'], bins[0], bins[-1] ), bins=bins, edgecolor='black' )

		plt.title('Minutes to Trade')
		plt.xlabel('Minutes')
		plt.ylabel('Total Ativos-Dias')

		plt.show()

	def plotEquityCurve(self, logy=False):
		dft = self.getTrades()

		x = dft['equity_real']
		x.index = dft['date']
		x.plot(logy=logy)


	def printBootstrapResults(self):

		bsr = self.getBootstrapResults()

		print('base case maximum drawdown', self.getMaxDrawdown() )
		print('maximum maximum drawdown', bsr['max_drawdown'].max() )
		print('minimum maximum drawdown', bsr['max_drawdown'].min() )
		print('mean maximum drawdown', bsr['max_drawdown'].mean() )