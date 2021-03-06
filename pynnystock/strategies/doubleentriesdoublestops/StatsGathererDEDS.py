import pandas as pd
import datetime
import pickle
from matplotlib import pyplot as plt
import numpy as np

from ...StatsGatherer import StatsGatherer
from ...Utilities import drawdown


class StatsGathererDEDS(StatsGatherer):


	def setTradesDF(self, trades): # quem chama é o método Simulator.runSimulation() ou Simulator.openTrades()
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'entry1_time':[],
		                    'exit1_time':[],
		                    'price1':[],
		                    'stop1':[],
		                    'target1':[],
		                    'profit1':[],
		                    'entry2_time':[],
		                    'exit2_time':[],
		                    'price2':[],
		                    'stop2':[],
		                    'target2':[],
		                    'profit2':[],
		                    })
		for t in trades:
		    if t['trade']: # se não for None
		        # os casos onde temos primeira entry mas não temos segunda entry podem ser chatinhos
		        entry1_time = t['trade']['entry1']['time'].strftime("%H:%M") if t['trade']['has_trade'] else np.nan
		        exit1_time = t['trade']['exit1']['time'].strftime("%H:%M") if t['trade']['has_trade'] else np.nan
		        entry2_time = t['trade']['entry2']['time'].strftime("%H:%M") if t['trade']['has_trade2'] else np.nan
		        exit2_time =  t['trade']['exit2']['time'].strftime("%H:%M") if t['trade']['has_trade2'] else np.nan
		        df = df.append({ 'name':t['name'],
		                         'date':t['date'], #.strftime("%d/%m/%Y"), datetime é melhor que string
		                         'entry1_time':entry1_time,
		                         'exit1_time':exit1_time,
		                         'price1':t['trade']['price1'],
		                         'stop1':t['trade']['stop1'],
		                         'target1':t['trade']['target1'],
		                         'profit1':t['trade']['profit1'],
		                         'entry2_time':entry2_time,
		                         'exit2_time':exit2_time,
		                         'price2':t['trade']['price2'],
		                         'stop2':t['trade']['stop2'],
		                         'target2':t['trade']['target2'],
		                         'profit2':t['trade']['profit2']
		                         },
		                       ignore_index=True)
		df = df.sort_values(by='date',ignore_index=True)
		#df['cum_profit'] = (1+self.pars.allocation*self.pars.firstEntryPct*df['profit1'])*(1+self.pars.allocation*(1-self.pars.firstEntryPct)*df['profit2']).cumprod()
		
		df['profit'] = (1+self.pars.firstEntryPct*df['profit1'])*(1+(1-self.pars.firstEntryPct)*df['profit2'])-1

		df['equity_real'] = pd.Series(0, index=df.index, dtype='float64')
		df['profit_real'] = pd.Series(0, index=df.index, dtype='float64')

		equity = self.pars.start_money
		for index, row in df.iterrows(): # Iterate over DataFrame rows as (index, Series) pairs.
			anterior = equity # vamos armazenar anterior pra calcular 'profit_real'
			equity = equity + (equity*self.pars.allocation*self.pars.firstEntryPct)*row['profit1'] + \
							(equity*self.pars.allocation*(1-self.pars.firstEntryPct))*row['profit2'] - \
							equity*self.pars.allocation*self.pars.locate_fee - \
							self.pars.commission
			df.at[index,'equity_real'] = equity
			df.at[index,'profit_real'] = equity/anterior-1 # curiosidade: a commission vai sendo diluida à medida dos trades

		df['cum_profit_real'] = df['equity_real']/self.pars.start_money

		df.date = pd.to_datetime(df.date)
		self.tradesdf = df
		self.n_trades = len(self.tradesdf)
		self.endMoney = self.getEndMoney()
		self.maxdrawdown = self.getMaxDrawdown()


	def appendSimResults(self): # precisa ainda mudar. Work to be done.

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


	def printSimResults(self):

		print()

		print(self.pars)

		print('Start Money:', '${:,.2f}'.format(self.pars.start_money) )

		print('End Money:', '${:,.2f}'.format(self.endMoney) )
		print('Number of Trades:', self.n_trades)
		print('Number of filtered ativo-dias:', self.n_filtered )
		print('Max Drawdown:', self.maxdrawdown )
