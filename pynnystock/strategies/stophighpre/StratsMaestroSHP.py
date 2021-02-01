import numpy as np
from datetime import datetime, time

from ...StratsMaestro import StratsMaestro
from ...indicators.OHLCDay import OHLCDay

class StratsMaestroSHP(StratsMaestro):

	### parâmetros
	# short_after
	# exit_target
	# **exit_stop__margin**

	def checkForTrade(self, intra):

		p = self.pars

		trade = {
			'has_trade':False,
			'has_eod_exit':False, # has End Of Day exit
			'entry': None,
			'price': np.nan,
			'stop': np.nan,
			'target': np.nan,
			'exit': None,
			'profit': np.nan
		}

		s = 0 # s=0 NO POSITION | s=1 OPEN POSITION | s=2 CLOSED POSITION

		first = intra._core[0]

		ohlc = OHLCDay(intra)
		high_pre = ohlc.high_pre

		for bar in intra._core:
			if s == 0: # NO POSITION
				if bar != intra._core[-1]: # se não for última barra do dia..
					variation = (bar['high'] - first['open'])/first['open']
					if variation >= p.short_after: # ENTRY
						trade['has_trade'] = True
						trade['entry'] = bar
						trade['price'] = (1+p.short_after)*first['open']
						trade['stop'] = high_pre*(1+p.exit_stop_margin)
						trade['target'] = (1-p.exit_target)*trade['price']
						s = 1
			elif s == 1: # OPEN POSITION
				if bar['high'] >= trade['stop']: # STOP_LOSS
					trade['exit'] = bar
					trade['profit'] = -(trade['stop']-trade['price'])/trade['price'] # prejuízo
					s = 2
				elif bar['low'] <= trade['target']: # STOP_TARGET
					trade['exit'] = bar
					trade['profit'] = p.exit_target # lucro
					s = 2
				elif bar == intra._core[-1]: # STOP_END
					trade['exit'] = bar
					trade['has_eod_exit'] = True
					trade['profit'] = -(bar['close'] - trade['price'])/trade['price']
					s = 2 # nem precisaria pois esta é a última bar
			elif s == 2: # CLOSED POSITION
				break

		return trade