import FileManager
import pandas as pd
import datetime
import Ativo
import pickle
from Utilities import drawdown

class Simulator:


	def __init__(self, adl, pars, sg):
		self.fm = FileManager.FileManager()
		self.adl = adl # ADL: Ativos-Dias List
		self.fad = [] # FAD: Filtered Ativos-Dias
		self.trades = [] # trade results from last simulation
		self.n_trades = 0 # number of non-None trades

		self.parameters = pars

		self.sg = sg

		self.results = pd.DataFrame()


	def runFiltering(self):
		def make_filter_prevol(threshold):
		     return lambda ad: ad['stats']['volPre'] >= threshold

		def make_filter_open_dolar(threshold):
		     return lambda ad: ad['stats']['openValue'] >= threshold

		def make_filter_gap(threshold):
		    return lambda ad: ad['stats']['gap'] >= threshold

		def make_filter_F(low_threshold, high_threshold):
		    return lambda ad: low_threshold <= ad['stats']['volPre']/ad['freefloat'] <= high_threshold

		prevol_greater_than = make_filter_prevol(self.parameters.prevol_threshold)
		open_greater_than_dolar = make_filter_open_dolar(self.parameters.open_dolar_threshold)
		gap_greater_than = make_filter_gap(self.parameters.gap_threshold)
		F_between = make_filter_F(self.parameters.F_low_threshold,self.parameters.F_high_threshold)

		filtered_ativo_dias =  filter(prevol_greater_than, self.adl)
		filtered_ativo_dias =  filter(open_greater_than_dolar, filtered_ativo_dias)
		filtered_ativo_dias =  filter(gap_greater_than, filtered_ativo_dias)
		filtered_ativo_dias =  filter(F_between, filtered_ativo_dias)
		self.fad = list(filtered_ativo_dias)
		self.sg.setFilteredDaysDF(self.fad)


	def runSimulation(self):
		trades = []
		for ad in self.fad:
		    intra = Ativo.Ativo.initIntradayFromDate(ad['name'],self.fm[ad['name']],ad['date'])
		    trades.append({'name': ad['name'],
		                   'date': ad['date'],
		                   'trade': intra.checkForTrade(self.parameters.short_after,
		                   								self.parameters.exit_target,
		                   								self.parameters.exit_stop)})
		self.trades = trades
		# vamos contar o número de non-None trades.
		self.n_trades = sum(x['trade'] is not None for x in self.trades)
		self.sg.setTradesDF(self.trades)


	def saveTrades(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.trades,filehandle)


	def openTrades(self,filename):
		with open(filename, 'rb') as filehandle: # w de read e b de binary
		    self.trades = pickle.load(filehandle)
		    self.n_trades = sum(x['trade'] is not None for x in self.trades)
		    self.sg.setTradesDF(self.trades)




