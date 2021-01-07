import pandas as pd
import datetime
from Utilities import drawdown
import pickle

class StatsGatherer:

	def __init__(self, pars):
		self.filtereddf = pd.DataFrame()
		self.tradesdf = pd.DataFrame()
		self.parameters = pars
		self.endMoney = 0
		self.maxdrawdown = 0
		self.meanmax_drawdown = 0
		self.maxmax_drawdown = 0
		self.minmax_drawdown = 0

		self.bs_res = pd.DataFrame() # Bootstrap results

		self.groupResults = pd.DataFrame() # Optimization results


	def setFilteredDaysDF(self, fad):
		# vamos primeiramente criar um dataframe vazio, mas com as colunas bem definidas
		df = pd.DataFrame({'name':[],
		                   'date':[],
		                   'freefloat':[],
		                   'volPre':[],
		                   'gap':[],
		                   'openToSpike%':[],
		                   'minsToSpike':[],
		                   'volToSpike':[],
		                   'spikeToLow%':[],
		                   'minsToLowAfterSpike':[],
		                   'spikeToPreVolF':[],
		                   'factorF':[]})
		# agora popula esse dataframe com todos AtivosXDia que passaram nos critérios
		for ad in fad:
		    secondsToSpike = datetime.datetime.combine(datetime.date.today(), ad['stats']['highCoreTime']) - datetime.datetime.combine(datetime.date.today(), datetime.time(9,31))
		    minutesToLowAfterSpike = datetime.datetime.combine(datetime.date.today(), ad['stats']['lowAfterHighTime']) - datetime.datetime.combine(datetime.date.today(), ad['stats']['highCoreTime'])

		    df = df.append({'name':ad['name'],
		                       'date':ad['date'], #.strftime("%d/%m/%Y"),
		                       'freefloat':ad['freefloat'],
		                       'volPre':ad['stats']['volPre'],
		                       'gap':ad['stats']['gap'],
		                       'openToSpike%':ad['stats']['openToSpikePercent'],
		                       'minsToSpike':secondsToSpike.total_seconds()/60,
		                       'volToSpike':ad['stats']['volumeToSpike'],
		                       'spikeToLow%':ad['stats']['spikeToLowPercent'],
		                       'minsToLowAfterSpike':minutesToLowAfterSpike.total_seconds()/60,
		                       'spikeToPreVolF':ad['stats']['spikeToPreVolFactor'],
		                       'factorF':ad['stats']['moneyVolPre']/ad['freefloat']},
		                          ignore_index=True)
		df.date = pd.to_datetime(df.date)
		self.filtereddf = df


	def setTradesDF(self, trades):
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'entry_time':[],
		                    'mins_to_trade':[],
		                    'exit_time':[],
		                    'price':[],
		                    'stop':[],
		                    'target':[],
		                    'profit':[]})
		for t in trades:
		    if t['trade']:
		        secondsToTrade = t['trade']['entry']['time'] - datetime.datetime.combine( t['trade']['entry']['time'].date(), datetime.time(9,31) )
		        df = df.append({ 'name':t['name'],
		                         'date':t['date'], #.strftime("%d/%m/%Y"), datetime é melhor que string
		                         'entry_time':t['trade']['entry']['time'].strftime("%H:%M"),
		                         'mins_to_trade':secondsToTrade.total_seconds()/60,
		                         'exit_time':t['trade']['exit']['time'].strftime("%H:%M"),
		                         'price':t['trade']['price'],
		                         'stop':t['trade']['stop'],
		                         'target':t['trade']['target'],
		                         'profit':t['trade']['profit']},
		                       ignore_index=True)
		df = df.sort_values(by='date',ignore_index=True)
		df['cum_profit'] = (1+self.parameters.allocation*df['profit']).cumprod()
		df['equity_real'] = pd.Series(0, index=df.index, dtype='float64')
		df['profit_real'] = pd.Series(0, index=df.index, dtype='float64')

		value = self.parameters.start_money
		for index, row in df.iterrows():
			anterior = value # vamos armazenar anterior pra calcular 'profit_real'
			value = value + (value*self.parameters.allocation)*row['profit'] - value*self.parameters.allocation*self.parameters.locate_fee - self.parameters.commission
			df.at[index,'equity_real'] = value
			df.at[index,'profit_real'] = value/anterior-1 # curiosidade: a commission vai sendo diluida à medida dos trades

		df['cum_profit_real'] = df['equity_real']/self.parameters.start_money

		df.date = pd.to_datetime(df.date)
		self.tradesdf = df
		self.n_trades = len(self.tradesdf)
		self.endMoney = self.getEndMoney()
		self.maxdrawdown = self.getMaxDrawdown()


	def getEndMoney(self):
		dft = self.tradesdf
		return dft.iloc[-1]['equity_real']


	def getMaxDrawdown(self): # drawdown da Simulator, e não da BootstrapSimulator
		s = self.tradesdf # pega todo o dataframe de trades, mas 
		s = s['cum_profit_real']

		return drawdown(s)


	def setBootstrapResults(self, bsl):

		dd_res = [] # DrawDown Results. é um maximum drawdown pra cada iteração do bootstrap

		for bs in bsl: # for each boostrap reordering in the bootstrap list of reordering
			cpr = bs['cum_profit_real']
			dd_res.append( drawdown(cpr) )

		# Results DataFrame
		bs_res = pd.DataFrame({
									'max_drawdown':dd_res,
								})

		self.bs_res =  bs_res
		self.meanmax_drawdown = bs_res['max_drawdown'].mean()
		self.maxmax_drawdown = bs_res['max_drawdown'].max()
		self.minmax_drawdown = bs_res['max_drawdown'].min()


	def appendSimResults(self):

		df = pd.DataFrame({ 'prevol_threshold':self.parameters.prevol_threshold,
		                    'open_dolar_threshold':self.parameters.open_dolar_threshold,
		                    'gap_threshold':self.parameters.gap_threshold,
		                    'F_low_threshold':self.parameters.F_low_threshold,
		                    'F_high_threshold':self.parameters.F_high_threshold,
		                    'short_after':self.parameters.short_after,
		                    'exit_target':self.parameters.exit_target,
		                    'exit_stop':self.parameters.exit_stop,
		                    'start_money':self.parameters.start_money,
		                    'allocation':self.parameters.allocation,
		                    'locate_fee':self.parameters.locate_fee,
		                    'commission':self.parameters.commission,
		                    'end_money':self.endMoney,
		                    'profit':(self.endMoney-self.parameters.start_money)/self.parameters.start_money,
		                    'max_drawdown':self.maxdrawdown,
		                    'meanmax_drawdown':self.meanmax_drawdown,
		                    'maxmax_drawdown':self.maxmax_drawdown,
		                    'minmax_drawdown':self.minmax_drawdown,
		                    'n_trades':self.n_trades,
		                    'n_filtered_ativo_days':len(self.filtereddf)},
		                    index=[0])
		self.groupResults = self.groupResults.append(df, ignore_index=True)


	def saveGroupResults(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.groupResults,filehandle)


	def appendGroupResults(self,filename):
		with open(filename, 'rb') as filehandle: # r de read e b de binary
			loaded = pickle.load(filehandle)
			self.groupResults = self.groupResults.append(loaded,ignore_index=True)

	def openGroupResults(self,filename):
		with open(filename, 'rb') as filehandle: # r de read e b de binary
			self.groupResults = pickle.load(filehandle)