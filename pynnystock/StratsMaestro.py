
class StratsMaestro:

	def __init__(self, pars):
		self.pars = pars


	def checkForTrade(self, intra):
		trade = {
					'has_trade':False
		} # se não tiver trade nesse dia o dictionary fica vazio
		
		first = intra._core[0]

		for bar in intra._core: 
			# ENTRY POINT
			if trade['has_trade']==False: # se nenhum trade tiver sido encontrado, procura por trades
				if bar != intra._core[-1]:
					variation = (bar['high'] - first['open'])/first['open']
					if variation >= self.pars.short_after:
						trade['has_trade'] = True
						trade['entry'] = bar
						trade['price'] = (1+self.pars.short_after)*first['open']
						trade['stop'] = (1+self.pars.exit_stop)*trade['price']
						trade['target'] = (1-self.pars.exit_target)*trade['price'] # lembrar que pra short o target é menor
			# EXIT POINTS
			else: # se já tivermos encontrado algum trade, vamos procurar exits
				if bar['high'] >= trade['stop']:
					trade['exit'] = bar
					trade['profit'] = -self.pars.exit_stop
					break # só pararemos a execução do loop apos encontrar uma entry e um stop
				if bar['low'] <= trade['target']:
					trade['exit'] = bar
					trade['profit'] = self.pars.exit_target
					break
				if bar == intra._core[-1]: # se for a última barra, fecha o trade no close da ultima barra
					trade['exit'] = bar
					trade['profit'] = -(bar['close'] - trade['price'])/trade['price']

		return trade # se o dictionary não estiver vazio, vai retornar os dados em trade