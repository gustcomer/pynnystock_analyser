import numpy as np
from datetime import datetime, time

from ...StratsMaestro import StratsMaestro
from ...Utilities import minutesDifference
from ...indicators.VWAP import VWAP

class StratsMaestroDSVW(StratsMaestro):

	### parâmetros
	# short_after
	# exit_target
	# exit_stop
	# vwap_distance
	# vwap_timer_minutes
	# vwap_pct
	# exit_after_minutes

	def checkForTrade(self, intra):

		p = self.pars # vamos dar um apelido para self.pars para facilitar

		trade = {
					'has_trade': False,
					'has_vwap_exit': False,
					'has_time_exit': False,
					'entry': None,
					'price': np.nan,
					'stop': np.nan,
					'target': np.nan,
					'exit': None,
					'profit': np.nan,
					'exit_vwap': None,
					'profit1_vwap': np.nan,
					'profit2_vwap': np.nan
		}

		s = 0 # s=0 SEM POSITION | s=1 FULL POSITION | s=2 HALF POSITION | s=3 NO POSITION

		first = intra._core[0]
		vwapCalc = VWAP(intra) # aqui ele faz umas inicializações com os dados do pre, e depois com getNextVWAP(bar)
							# vai atualizando barra a barra. vwapCalc: VWAP Calculator

		for bar in intra._core:
			
			vwap = vwapCalc.getNextVWAP(bar) # calculamos vwap externamente pois em todas barras temos que atualizar o objeto vwapCalc
			
			if s == 0: # SEM POSITION
				if bar != intra._core[-1]: # se não for última barra do dia..
					variation = (bar['high'] - first['open'])/first['open']
					if variation >= p.short_after: # ENTRY
						trade['has_trade'] = True
						trade['entry'] = bar
						trade['price'] = (1+p.short_after)*first['open']
						trade['stop'] = (1+p.exit_stop)*trade['price']
						trade['target'] = (1-p.exit_target)*trade['price']
						s = 1
			elif s == 1: # FULL POSITION
				elapsed_time = minutesDifference(bar['time'].time(), trade['entry']['time'].time()) # código duplicado, mas é mais legível
				if bar['high'] >= trade['stop']: # STOP_LOSS
					trade['exit'] = bar
					trade['profit'] = -p.exit_stop # prejuízo
					s = 3
				elif bar['low'] <= trade['target']: # STOP_TARGET
					trade['exit'] = bar
					trade['profit'] = p.exit_target # lucro
					s = 3
				elif elapsed_time >= p.exit_after_minutes: # STOP TIME
					trade['has_time_exit'] = True
					trade['exit'] = bar
					trade['profit'] = -(bar['close'] - trade['price'])/trade['price']
					s = 3
				elif bar == intra._core[-1]: # STOP_END
					trade['exit'] = bar
					trade['profit'] = -(bar['close'] - trade['price'])/trade['price']
					s = 3 # nem precisaria pois esta é a última bar
				elif (bar['low'] < (1-p.vwap_distance)*vwap) and (elapsed_time >= p.vwap_timer_minutes):
					trade['has_vwap_exit'] = True
					trade['exit_vwap'] = bar
					trade['profit1_vwap'] = -(bar['close'] - trade['price'])/trade['price']
					s = 2
			elif s == 2: # HALF POSITION
				elapsed_time = minutesDifference(bar['time'].time(), trade['entry']['time'].time()) # código duplicado, mas é mais legível
				if bar['high'] >= trade['stop']: # STOP_LOSS
					trade['exit'] = bar
					trade['profit2_vwap'] = -p.exit_stop # prejuízo
					trade['profit'] = p.vwap_pct*trade['profit1_vwap'] + (1-p.vwap_pct)*trade['profit2_vwap']
					s = 3
				elif bar['low'] <= trade['target']: # STOP_TARGET
					trade['exit'] = bar
					trade['profit2_vwap'] = p.exit_target # lucro
					trade['profit'] = p.vwap_pct*trade['profit1_vwap'] + (1-p.vwap_pct)*trade['profit2_vwap']
					s = 3
				elif elapsed_time >= p.exit_after_minutes: # STOP TIME
					trade['has_time_exit'] = True
					trade['exit'] = bar
					trade['profit2_vwap'] = -(bar['close'] - trade['price'])/trade['price']
					trade['profit'] = p.vwap_pct*trade['profit1_vwap'] + (1-p.vwap_pct)*trade['profit2_vwap']
					s = 3
				elif bar == intra._core[-1]: # STOP_END
					trade['exit'] = bar
					trade['profit2_vwap'] = -(bar['close'] - trade['price'])/trade['price']
					trade['profit'] = p.vwap_pct*trade['profit1_vwap'] + (1-p.vwap_pct)*trade['profit2_vwap']
					s = 3 # nem precisaria pois esta é a última bar
			elif s == 2:
				break

		return trade # se o dictionary não estiver vazio, vai retornar os dados em trade