import pandas as pd
import datetime
from Utilities import divideDays
import StatsGatherer

class IntraDay():
	'''
	Classe responsável por manter os dados dentro de um dia para algum ativo qualquer
	dataDay é uma list contendo os tickers de um dia qualquer de forma raw, sem nenhuma organização
	Essa classe organiza os dados em _pre, _core, _after e fornece alguns métodos interessantes
	'''
	def __init__(self,dataDay): # dataDay is one element of the list dataDays

		self.dataDay = dataDay
		self.date = dataDay[0]['time'].date()
		self._pre = []
		self._core = []
		self._pos = []

		self.stats = {} # empty curly cria empty dict e não empty set

		for dt in dataDay: # dt seria pra cada datetime (time com date), por isso extraímos dt.time()
			t1 = datetime.time(9,30)
			t2 = datetime.time(16,0)

			if dt['time'].time() <= t1: # se for horário de pre
			    self._pre.append(dt)
			elif t1 < dt['time'].time() <= t2: # se for horário de core
			    self._core.append(dt)
			else: # se for o que sobrou, horário de pós
			    self._pos.append(dt)

		if len(self._core)==0: # se tivermos core nulo mas pre ou pos não nulos, varemos alguns ajustes.
			if len(self._pre) > 0:
				print('caso core vazio mas com pre')
			if len(self._pos) > 0:
				print('caso core vazio mas com pos')

		# chama um static method da classe StatsGatherer do module StatsGatherer
		self.stats = StatsGatherer.StatsGatherer.calculateIntradayStats(self)

	def __repr__(self):

		s = ''
		s = s + f"{self.dataDay[0]['time'].date()}\n"
		s = s + f"{self.stats}\n"
		s = s + f"_pre\n"
		for b in self._pre:
			s = s + f"{b['time'].time()} open: {b['open']} high: {b['high']} low: {b['low']} close: {b['close']} volume: {b['volume']}\n"
		s = s + f"_core\n"
		for b in self._core:
			s = s + f"{b['time'].time()} open: {b['open']} high: {b['high']} low: {b['low']} close: {b['close']} volume: {b['volume']}\n"
		s = s + f"_pos\n"
		for b in self._pos:
			s = s + f"{b['time'].time()} open: {b['open']} high: {b['high']} low: {b['low']} close: {b['close']} volume: {b['volume']}\n"
		return s

class Ativo():
	'''
	Classe responsável por parsear os dados de uma ação específica
	'''
	def __init__(self, name, path):

		self.name = name
		self.path = path

		data = [] # list of bars, which are dicts containing tick information
		with open(path, 'r') as file:
		    line = file.readline() # le a primeira vez e descarta o header
		    line = file.readline() # le a primeira vez e tenta continuar a ler
		    while line:
		        tokens = line.split(',')
		        bar = { 'time':datetime.datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S'),
		                'open':float(tokens[1]),
		                'high':float(tokens[2]),
		                'low':float(tokens[3]),
		                'close':float(tokens[4]),
		                'volume':int(tokens[5])}
		        data.append(bar)
		        line = file.readline()
		data.reverse()
		self.data = data
		self._initDayData()
		self._initIntradayData()
		StatsGatherer.StatsGatherer.calculateOuterDayStats(self)

	@staticmethod # usamos @staticmethod e não @classmethod pois não precisaremos instanciar a classe com cls
					# na verdade nem usamos name
	def initIntradayFromDate(name, path, d): # d é a data em formato datetime.date
		data = []
		with open(path, 'r') as file:
			lines = [line for line in file if line.startswith(d.strftime("%Y-%m-%d"))]
		lines.reverse()
		for line in lines:
			tokens = line.split(',')
			bar = { 'time':datetime.datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S'),
					'open':float(tokens[1]),
					'high':float(tokens[2]),
					'low':float(tokens[3]),
					'close':float(tokens[4]),
					'volume':int(tokens[5])}
			data.append(bar)

		return IntraDay(data) # notar que iniciamos IntraDay() sem as outer stats, paciência.. por enquanto..

	# são os dados brutos divididos em dias, mas ainda não divididos em core, pre, pos e stats
	def _initDayData(self):
		self.dataDays = divideDays(self.data)

	# agora os dias divididos em core, pre, pos e stats, ou seja, dados intraday
	def _initIntradayData(self):
		self.intraDays = []
		for d in self.dataDays:
			self.intraDays.append( IntraDay(d) )

	# esse método filtra o dia de interesse e retorna um objeto da classe Intraday (aka ativo-dia)
	# daria pra fazer com filter mas no final das contas next() é a melhor opção
	def fromDay(self,d):
		return next(intra for intra in self.intraDays if intra.dataDay[0]['time'].date() == d )

	def __repr__(self):
		s=''
		s = s + f"{self.intraDays}"
		return s


	def show(self):
		print(self.dataDays)