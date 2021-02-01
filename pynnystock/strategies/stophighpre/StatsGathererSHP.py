import pandas as pd
import datetime
import pickle
from matplotlib import pyplot as plt
import numpy as np

from ...StatsGatherer import StatsGatherer
from ...Utilities import drawdown, minutesDifference


class StatsGathererSHP(StatsGatherer):


	def setTradesDF(self, trades): # quem chama é o método Simulator.runSimulation() ou Simulator.openTrades()
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'has_trade':[],
		                    'has_eod_exit':[],
		                    'entry_time':[],
		                    'minutes_to_trade':[],
		                    'price':[],
		                    'stop':[],
		                    'target':[],
		                    'exit_time':[],
		                    'minutes_in_trade':[],
		                    'profit':[]
		                    })

		for t in trades:
		    if t['trade']['has_trade']: # se houver algum trade. Caso contrario não contabiliza pois esse DF é só de trades efetivados
		        entry_time = t['trade']['entry']['time'].strftime("%H:%M") if t['trade']['has_trade'] else np.nan
		        exit_time = t['trade']['exit']['time'].strftime("%H:%M") if t['trade']['has_trade'] else np.nan
		        minutes_to_trade = minutesDifference(t['trade']['entry']['time'].time(), datetime.time(9,31))
		        minutes_in_trade = minutesDifference(t['trade']['exit']['time'].time(), t['trade']['entry']['time'].time())
		        df = df.append({ 'name':t['name'],
		                         'date':t['date'], #.strftime("%d/%m/%Y"), datetime é melhor que string
		                         'has_trade':t['trade']['has_trade'],
		                         'has_eod_exit':t['trade']['has_eod_exit'],
		                         'entry_time':entry_time,
		                         'minutes_to_trade': minutes_to_trade,
		                         'price':t['trade']['price'],
		                         'stop':t['trade']['stop'],
		                         'target':t['trade']['target'],
		                         'exit_time':exit_time,
		                         'profit':t['trade']['profit'],
		                         'minutes_in_trade':minutes_in_trade,
		                         },
		                       ignore_index=True)
		df = df.sort_values(by='date',ignore_index=True)

		df['equity_real'] = pd.Series(0, index=df.index, dtype='float64')
		df['profit_real'] = pd.Series(0, index=df.index, dtype='float64')

		equity = self.pars.start_money
		for index, row in df.iterrows(): # Iterate over DataFrame rows as (index, Series) pairs.
			anterior = equity # vamos armazenar anterior pra calcular 'profit_real'

			equity = equity + equity*self.pars.allocation*row['profit'] - \
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


	def appendSimResults(self):

		df = pd.DataFrame({ 'prevol_threshold':self.pars.prevol_threshold,
		                    'open_dolar_threshold':self.pars.open_dolar_threshold,
		                    'gap_threshold':self.pars.gap_threshold,
		                    'F_low_threshold':self.pars.F_low_threshold,
		                    'F_high_threshold':self.pars.F_high_threshold,
		                    'short_after':self.pars.short_after,
		                    'exit_target':self.pars.exit_target,
		                    'exit_stop_margin':self.pars.exit_stop_margin,
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