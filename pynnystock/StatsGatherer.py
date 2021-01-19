import pandas as pd
import datetime
import pickle
from matplotlib import pyplot as plt
import numpy as np

from .Utilities import drawdown, minutesDifference


class StatsGatherer:

	def __init__(self, pars):

		self.filtereddf = pd.DataFrame() # dataframe with some information about fad
		self.tradesdf = pd.DataFrame() # dataframe with some information about trades
		self.extrastatsdf = pd.DataFrame() # dataframe with some more information about trades
		self.bs_res = pd.DataFrame() # Bootstrap results
		self.groupResults = pd.DataFrame() # Optimization results

		self.n_filtered = 0
		self.n_trades = 0

		self.pars = pars

		self.endMoney = 0
		
		self.maxdrawdown = 0
		self.meanmax_drawdown = 0
		self.maxmax_drawdown = 0
		self.minmax_drawdown = 0


	def setFilteredDaysDF(self, fad): # quem chama é o método Simulator.runFiltering()
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
			minsToSpike = minutesDifference(ad['stats']['highCoreTime'], datetime.time(9,31))
			minutesToLowAfterSpike = minutesDifference(ad['stats']['lowAfterHighTime'], ad['stats']['highCoreTime'])

			df = df.append({'name':ad['name'],
			                   'date':ad['date'], #.strftime("%d/%m/%Y"),
			                   'freefloat':ad['freefloat'],
			                   'volPre':ad['stats']['volPre'],
			                   'gap':ad['stats']['gap'],
			                   'openToSpike%':ad['stats']['openToSpikePercent'],
			                   'minsToSpike':minsToSpike,
			                   'volToSpike':ad['stats']['volumeToSpike'],
			                   'spikeToLow%':ad['stats']['spikeToLowPercent'],
			                   'minsToLowAfterSpike':minutesToLowAfterSpike,
			                   'spikeToPreVolF':ad['stats']['spikeToPreVolFactor'],
			                   'factorF':ad['stats']['moneyVolPre']/ad['freefloat']},
			                      ignore_index=True)
		df.date = pd.to_datetime(df.date)
		self.filtereddf = df
		self.n_filtered = len(self.filtereddf)


	def setTradesDF(self, trades): # quem chama é o método Simulator.runSimulation() ou Simulator.openTrades()
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
		    if t['trade']['has_trade']:
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
		df['cum_profit'] = (1+self.pars.allocation*df['profit']).cumprod()
		df['equity_real'] = pd.Series(0, index=df.index, dtype='float64')
		df['profit_real'] = pd.Series(0, index=df.index, dtype='float64')

		value = self.pars.start_money
		for index, row in df.iterrows():
			anterior = value # vamos armazenar anterior pra calcular 'profit_real'
			value = value + (value*self.pars.allocation)*row['profit'] - value*self.pars.allocation*self.pars.locate_fee - self.pars.commission
			df.at[index,'equity_real'] = value
			df.at[index,'profit_real'] = value/anterior-1 # curiosidade: a commission vai sendo diluida à medida dos trades

		df['cum_profit_real'] = df['equity_real']/self.pars.start_money

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

		df = pd.DataFrame({ 'prevol_threshold':self.pars.prevol_threshold,
		                    'open_dolar_threshold':self.pars.open_dolar_threshold,
		                    'gap_threshold':self.pars.gap_threshold,
		                    'F_low_threshold':self.pars.F_low_threshold,
		                    'F_high_threshold':self.pars.F_high_threshold,
		                    'short_after':self.pars.short_after,
		                    'exit_target':self.pars.exit_target,
		                    'exit_stop':self.pars.exit_stop,
		                    'start_money':self.pars.start_money,
		                    'allocation':self.pars.allocation,
		                    'locate_fee':self.pars.locate_fee,
		                    'commission':self.pars.commission,
		                    'end_money':self.endMoney,
		                    'profit':(self.endMoney-self.pars.start_money)/self.pars.start_money,
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


	def printSimResults(self):

		print('prevol_threshold', self.pars.prevol_threshold)
		print('open_dolar_threshold', self.pars.open_dolar_threshold)
		print('gap_threshold', self.pars.gap_threshold)
		print('F_low_threshold', self.pars.F_low_threshold)
		print('F_high_threshold', self.pars.F_high_threshold)

		print('')

		print('short_after', self.pars.short_after)
		print('exit_target', self.pars.exit_target)
		print('exit_stop', self.pars.exit_stop)

		print('')

		print('start_money', self.pars.start_money)
		print('allocation', self.pars.allocation)
		print('locate_fee', self.pars.locate_fee)
		print('commission', self.pars.commission)

		print('')

		print('Start Money:', '${:,.2f}'.format(self.pars.start_money) )

		print('End Money:', '${:,.2f}'.format(self.endMoney) )
		print('Number of Trades:', self.n_trades)
		print('Number of filtered ativo-dias:', self.n_filtered )
		print('Max Drawdown:', self.maxdrawdown )


	def printBootstrapResults(self):

		print('Max Drawdown:', self.maxdrawdown )
		print('Mean of max Drawdown:', self.meanmax_drawdown )
		print('Max of max Drawdown:', self.maxmax_drawdown )
		print('Min of max Drawdown:', self.minmax_drawdown )


	def plotHistMinsToTrade(self, bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]):

		plt.hist( np.clip( self.tradesdf['mins_to_trade'], bins[0], bins[-1] ), bins=bins, edgecolor='black' )

		plt.title('Minutes to Trade')
		plt.xlabel('Minutes')
		plt.ylabel('Total Ativos-Dias')

		plt.show()


	def plotEquityCurve(self, logy=False):

		x = self.tradesdf['equity_real']
		x.index = self.tradesdf['date']
		x.plot(logy=logy)


	def calculateIntradayStats(self, intraday):
		stats = {}

		# calcula volume pre market
		volPre = 0
		for b in intraday._pre:
			volPre = volPre + b['volume']
		stats['volPre'] = volPre

		# calcula money volume de pre market
		moneyVolPre = 0
		for b in intraday._pre:
			moneyVolPre += b['volume']*b['close']
		stats['moneyVolPre'] = moneyVolPre

		# calcula open value
		stats['openValue'] = intraday._core[0]['open']

		# calcula o valor mais alto do core, a hora na qual aconteceu e a position
		highCoreValue = intraday._core[0]['high']
		highCoreTime = intraday._core[0]['time'].time()
		highCorePosition = 0

		for b in intraday._core:
			if highCoreValue < b['high']:
				highCoreValue = b['high']
				highCoreTime = b['time'].time()
				highCorePosition = intraday._core.index(b)

		stats['highCoreValue'] = highCoreValue
		stats['highCoreTime'] = highCoreTime
		stats['highCorePosition'] = highCorePosition

		# calcula o low depois do high
		lowAfterHighValue = intraday._core[highCorePosition]['high']
		lowAfterHighTime = intraday._core[highCorePosition]['time'].time()
		lowPositionAfterHigh = highCorePosition

		for b in intraday._core[highCorePosition:]: # da high position pra frente
			if lowAfterHighValue > b['low']:
				lowAfterHighValue = b['low']
				lowAfterHighTime = b['time'].time()
				lowPositionAfterHigh = intraday._core.index(b)

		stats['lowAfterHighValue'] = lowAfterHighValue
		stats['lowAfterHighTime'] = lowAfterHighTime
		stats['lowPositionAfterHigh'] = lowPositionAfterHigh

		# calcula variação percentual do open até o spike

		highCoreValue = intraday._core[highCorePosition]['high'] # escrevendo denovo só pra não se perder
		openValue = intraday._core[0]['open']
		openToSpikePercent = (highCoreValue - openValue)/openValue
		stats['openToSpikePercent'] = openToSpikePercent

		# calcula variação percentual do spike até o low
		highCoreValue = intraday._core[highCorePosition]['high'] # escrevendo denovo só pra não se perder
		lowAfterHighValue = intraday._core[lowPositionAfterHigh]['low']
		spikeToLowPercent = (lowAfterHighValue - highCoreValue)/highCoreValue
		stats['spikeToLowPercent'] = spikeToLowPercent

		# calcula volume from start of core to spike
		volumeToSpike = 0
		for b in intraday._core[:(highCorePosition+1)]: # o mais 1 é pq em python o end é exclusive
			volumeToSpike += b['volume']
		stats['volumeToSpike'] = volumeToSpike

		# calcula fator (volume até o spike)/(volume pre)
		spikeToPreVolFactor = 0
		if volPre == 0:
			spikeToPreVolFactor = 0
		else:
			spikeToPreVolFactor = volumeToSpike/volPre
		stats['spikeToPreVolFactor'] = spikeToPreVolFactor

		return stats


	# vamos inicializar algumas stats que não são autocontidas em um dia
	def calculateOuterDayStats(self, ativo):

		gap = 0
		dayBefore = ativo.intraDays[0]
		for day in ativo.intraDays:
			if dayBefore == day: # caso seja o primeiro dia, seta gap como zero, pois não faz sentido o calculo
				day.stats['gap'] = 0 # notar que estamos alterando uma variável dentro do intradia.
				dayBefore = day
			else:
				firstOpen = day._core[0]['open']
				lastClose = dayBefore._core[-1]['close']
				day.stats['gap'] = (firstOpen - lastClose)/lastClose
				dayBefore = day


	def calculateExtraStats(self, intraday): # esses dados são chamados por runSimulation e armazenados em trades
		extraStats = {}
		extraStats['open_pre'] = intraday._pre[0]['open'] if intraday._pre else np.NaN
		extraStats['high_pre'] = max(intraday._pre, key=lambda x:x['high'])['high'] if intraday._pre else np.NaN
		extraStats['low_pre'] = min(intraday._pre, key=lambda x:x['low'])['low'] if intraday._pre else np.NaN
		extraStats['close_pre'] = intraday._pre[-1]['close'] if intraday._pre else np.NaN
		extraStats['open_core'] = intraday._core[0]['open'] if intraday._core else np.NaN
		extraStats['high_core'] = max(intraday._core, key=lambda x:x['high'])['high'] if intraday._core else np.NaN
		extraStats['low_core'] = min(intraday._core, key=lambda x:x['low'])['low'] if intraday._core else np.NaN
		extraStats['close_core'] = intraday._core[-1]['close'] if intraday._core else np.NaN
		# usar np.NaN ou None? com np.NaN ainda podemos executar algumas funções matemáticas

		return extraStats # vai acabar sendo armazenado em Simulator.trades, sendo cahamdo em runSimulation()


	def setExtraStatsDF(self, trades): # quem chama é o método Simulator.runSimulation() ou Simulator.openTrades()
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'open_pre':[],
		                    'high_pre':[],
		                    'low_pre':[],
		                    'close_pre':[],
		                    'open_core':[],
		                    'high_core':[],
		                    'low_core':[],
		                    'close_core':[]
		                    })
		for t in trades:
		    if t['trade']:
		        df = df.append({ 'name': t['name'],
		                         'date': t['date'], #.strftime("%d/%m/%Y"), datetime é melhor que string
		                         'open_pre': t['extraStats']['open_pre'],
		                         'high_pre': t['extraStats']['high_pre'],
		                         'low_pre': t['extraStats']['low_pre'],
		                         'close_pre': t['extraStats']['close_pre'],
		                         'open_core': t['extraStats']['open_core'],
		                         'high_core': t['extraStats']['high_core'],
		                         'low_core': t['extraStats']['low_core'],
		                         'close_core': t['extraStats']['close_core']
		                         }, ignore_index=True)
		df = df.sort_values(by='date',ignore_index=True)
		df.date = pd.to_datetime(df.date)

		self.extrastatsdf = df