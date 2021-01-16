import numpy as np

from ...StratsMaestro import StratsMaestro

class StratsMaestroDEDS(StratsMaestro):

	# lembrar que não precisa do método __init__ pois ele está sendo herdado (eu acho, glup)

	### parâmetros
	# short_after1
	# short_after2
	# firstEntryPct
	# exit_target
	# exit_stop

	def checkForTrade(self, intra):

		trade = {
					'has_trade': False,
					'entry1': None,
					'price1': np.nan,
					'stop1': np.nan,
					'target1': np.nan,
					'has_trade2': False,
					'entry2': None,
					'price2': np.nan,
					'stop2': np.nan,
					'target2': np.nan,
					'profit1': 0,
					'exit1': None,
					'profit2': 0,
					'exit2': None
		} # se não tiver trade nesse dia o dictionary fica vazio

		t = 0 # t = 0 SEM POSITION 1  t = 1 ABRIU POSITION 1  t = 2 POSITION 1 ENCERRADA
		v = 0 # v = 0 SEM POSITION 2  v = 1 ABRIU POSITION 1  v = 2 POSITION 2 ENCERRADA 

		first = intra._core[0]

		for bar in intra._core:
			if t == 0: # t = 0 STATE
				if bar != intra._core[-1]: # se não for última barra do dia..
					variation = (bar['high'] - first['open'])/first['open']
					if variation >= self.pars.short_after1: # ENTRY 1
						trade['has_trade'] = True
						trade['entry1'] = bar
						trade['price1'] = (1+self.pars.short_after1)*first['open']
						trade['stop1'] = (1+self.pars.exit_stop)*trade['price1']
						trade['target1'] = (1-self.pars.exit_target)*trade['price1']
						t = 1
			elif t == 1: # t = 1 STATE
				if bar['high'] >= trade['stop1']: # STOP 1
					trade['exit1'] = bar
					trade['profit1'] = -self.pars.exit_stop
					t = 2
				if bar['low'] <= trade['target1']: # TARGET 1
					trade['exit1'] = bar
					trade['profit1'] = self.pars.exit_target
					t = 2
				if bar == intra._core[-1]: # TIME STOP
					trade['exit1'] = bar
					trade['profit1'] = -(bar['close'] - trade['price1'])/trade['price1']
					t = 2 # nem precisaria pois esta é a última bar
			# t = 2 STATE nada a ser feito

			if v == 0: # v = 0 STATE
				if bar != intra._core[-1]: # se não for última barra do dia..
					variation = (bar['high'] - first['open'])/first['open']
					if variation >= self.pars.short_after2: # ENTRY 2
						trade['has_trade2'] = True
						trade['entry2'] = bar
						trade['price2'] = (1+self.pars.short_after2)*first['open']
						trade['stop2'] = (1+self.pars.exit_stop)*trade['price2']
						trade['target2'] = (1-self.pars.exit_target)*trade['price2']
						v = 1
			elif v == 1: # v = 1 STATE
				if bar['high'] >= trade['stop2']: # STOP 2
					trade['exit2'] = bar
					trade['profit2'] = -self.pars.exit_stop
					v = 2
				if bar['low'] <= trade['target2']: # TARGET 2
					trade['exit2'] = bar
					trade['profit2'] = self.pars.exit_target
					v = 2
				if bar == intra._core[-1]: # TIME STOP
					trade['exit2'] = bar
					trade['profit2'] = -(bar['close'] - trade['price2'])/trade['price2']
					v = 2
			# v = 2 STATE nada a ser feito

			if t == 2 and v == 2:
				break

			# não lidamos mais com trades do tipo None

		if t == 0 and v == 0: # verifica se não houve nenhum trade, nesse caso retorna None
			return None

		return trade # se o dictionary não estiver vazio, vai retornar os dados em trade