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

	def getFilteredDays(self):
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
		for ad in self.fad:
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
		return df

	def getTrades(self):
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'entry_time':[],
		                    'mins_to_trade':[],
		                    'exit_time':[],
		                    'price':[],
		                    'stop':[],
		                    'target':[],
		                    'profit':[]})
		for t in self.trades:
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
		return df

	def runSimulation(self):
		trades = []
		for ad in self.fad:
		    intra = at.Ativo.initIntradayFromDate(ad['name'],self.fm[ad['name']],ad['date'])
		    trades.append({'name': ad['name'],
		                   'date': ad['date'],
		                   'trade': intra.checkForTrade(self.parameters.short_after,
		                   								self.parameters.exit_target,
		                   								self.parameters.exit_stop)})
		self.trades = trades
		# vamos contar o número de non-None trades.
		self.n_trades = sum(x['trade'] is not None for x in self.trades)

	def runSimulationGroup(self,
							prevol_threshold=[800000],
							open_dolar_threshold=[2],
							gap_threshold=[0.2],
							F_low_threshold=[0],
							F_high_threshold=[1],
							short_after = [0.1],
							exit_target = [0.3],
							exit_stop = [0.3],
							start_money = [10000],
							allocation=[0.1],
							locate_fee=[0.02],
							commission=[2]):

		parametros = [
			[a,b,c,d,e,f,g,h,i,j,k,l]
			for a in prevol_threshold 
			for b in open_dolar_threshold
			for c in gap_threshold
			for d in F_low_threshold
			for e in F_high_threshold
			for f in short_after
			for g in exit_target
			for h in exit_stop
			for i in start_money
			for j in allocation
			for k in locate_fee
			for l in commission
		]

		parslist = []
		for l in parametros:
		    pars = {
		        'prevol_threshold':l[0],
		        'open_dolar_threshold':l[1],
		        'gap_threshold':l[2],
		        'F_low_threshold':l[3],
		        'F_high_threshold':l[4],
		        'short_after':l[5],
		        'exit_target':l[6],
		        'exit_stop':l[7],
		        'start_money':l[8],
		        'allocation':l[9],
		        'locate_fee':l[10],
		        'commission':l[11]
		    }
		    parslist.append(pars)
		parslist

		print(f"Simulando {len(parslist)} combinações de parâmetros.")

		for p in parslist:
			self.parameters.setFilterParameters(prevol_threshold=p['prevol_threshold'],
									open_dolar_threshold=p['open_dolar_threshold'],
									gap_threshold=p['gap_threshold'],
									F_low_threshold=p['F_low_threshold'],
									F_high_threshold=p['F_high_threshold'])
			self.runFiltering()
				
			self.parameters.setAlgoParameters(short_after = p['short_after'],
									exit_target = p['exit_target'],
									exit_stop = p['exit_stop'])
			self.parameters.setSimParameters(start_money = p['start_money'],
								allocation = p['allocation'],
								locate_fee=p['locate_fee'],
								commission=p['commission'])

			now = datetime.datetime.now()
			now_str = now.strftime("%d/%m/%Y %H:%M:%S")
			print("running another simulation.", now_str)
			self.runSimulation()

			self.results = self.results.append(self.getSimResults(),ignore_index=True)


	def saveTrades(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.trades,filehandle)

	def openTrades(self,filename):
		with open(filename, 'rb') as filehandle: # w de read e b de binary
		    self.trades = pickle.load(filehandle)
		    self.n_trades = sum(x['trade'] is not None for x in self.trades)

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

	def getSimResults(self):
		self.runBootstrap(n_iter=50, replace=False)
		bsr = self.getBootstrapResults()

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
		                    'end_money':self.getEndMoney(),
		                    'profit':(self.getEndMoney()-self.parameters.start_money)/self.parameters.start_money,
		                    'max_drawdown':self.getMaxDrawdown(),
		                    'meanmax_drawdown': bsr['max_drawdown'].mean(),
		                    'maxmax_drawdown':bsr['max_drawdown'].max(),
		                    'minmax_drawdown': bsr['max_drawdown'].min(),
		                    'n_trades':self.n_trades,
		                    'n_filtered_ativo_days':len(self.fad)},
		                    index=[0])
		return df

	def getEndMoney(self):
		dft = self.getTrades()
		return dft.iloc[-1]['equity_real']

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

	def getMaxDrawdown(self):
		s = self.getTrades() # pega todo o dataframe de trades, mas 
		s = s['cum_profit_real']

		return drawdown(s)

	def saveGroupResults(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.results,filehandle)

	def openGroupResults(self,filename):
		with open(filename, 'rb') as filehandle: # w de read e b de binary
			loaded = pickle.load(filehandle)
			self.results = self.results.append(loaded,ignore_index=True)

	def runBootstrap(self, n_iter=50, replace=False):
		self.bsl = []
		s = self.getTrades()

		self.bs_base = s[['profit_real', 'cum_profit_real']]

		prb = self.bs_base['profit_real'] # Profit Real do Base case (PRB)

		for i in range(0,n_iter):
			random_pr = prb.sample(n = prb.size, replace=replace).reset_index(drop=True)
			random_bs = pd.DataFrame({
										'profit_real':random_pr,
										'cum_profit_real':(1+random_pr).cumprod()
									})

			self.bsl.append(random_bs)

	def getBootstrapResults(self):

		dd_res = [] # DrawDown Results

		for bs in self.bsl: 
			cpr = bs['cum_profit_real']
			dd_res.append( drawdown(cpr) )

		# Results DataFrame
		bs_res = pd.DataFrame({
									'max_drawdown':dd_res,
								})

		return bs_res

	def printBootstrapResults(self):

		bsr = self.getBootstrapResults()

		print('base case maximum drawdown', self.getMaxDrawdown() )
		print('maximum maximum drawdown', bsr['max_drawdown'].max() )
		print('minimum maximum drawdown', bsr['max_drawdown'].min() )
		print('mean maximum drawdown', bsr['max_drawdown'].mean() )

	def __repr__(self):
		s='FILTERING PARAMETERS\n'
		s = s + f"prevol_threshold: {self.parameters.prevol_threshold}\n"
		s = s + f"open_dolar_threshold: {self.parameters.open_dolar_threshold}\n"
		s = s + f"gap_threshold: {self.parameters.gap_threshold}\n"
		s = s + f"F_low_threshold: {self.parameters.F_low_threshold}\n"
		s = s + f"F_high_threshold: {self.parameters.F_high_threshold}\n"
		s = s + f"\n"
		s = s + f'TRADING PARAMETERS\n'
		s = s + f"short_after: {self.parameters.short_after}\n"
		s = s + f"exit_target: {self.parameters.exit_target}\n"
		s = s + f"exit_stop: {self.parameters.exit_stop}\n"

		return s