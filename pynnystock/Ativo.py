import pandas as pd
import datetime
import mysql.connector

from .Utilities import divideDays
from .StatsGatherer import StatsGatherer
from .settings import db

class IntraDay():
	'''
	Classe responsável por manter os dados dentro de um dia para algum ativo qualquer
	dataDay é uma list contendo os tickers de um dia qualquer de forma raw, sem nenhuma organização
	Essa classe organiza os dados em _pre, _core, _after e fornece alguns métodos interessantes
	'''
	def __init__(self,dataDay, sg): # dataDay is one element of the list dataDays

		self.sg = sg

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

		self.stats = self.sg.calculateIntradayStats(self)

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
	def __init__(self, name, path, sg):

		self.name = name
		self.path = path
		self.sg = sg

		# SE QUISER USAR CSVS AO INVÉS DE DATABASE MYSQL, DESCOMENTAR ESSA LINHA
		#self.data = self.openDataWithCSVs() # raw data, tem dados do ano inteiro

		self.data = self.openDataWithDB() # SE NÃO QUISER USAR MAIS DATABASE, COMENTAR ESSA LINHA
		self.dataDays = divideDays(self.data) # tem informação sobre os dias 

		# agora os dias divididos em core, pre, pos e stats, ou seja, dados intraday
		self.intraDays = []
		for d in self.dataDays:
			self.intraDays.append( IntraDay(d, self.sg) )

		self.sg.calculateOuterDayStats(self)

	def openDataWithCSVs(self):
		data = [] # list of bars, which are dicts containing tick information
		with open(self.path, 'r') as file:
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
		return data


	def openDataWithDB(self):
		data = []

		mydb = mysql.connector.connect(
		  host=db['host'],
		  user=db['user'],
		  password=db['password'],
		  database=db['database']
		)

		mycursor = mydb.cursor(dictionary=True)
		mycursor.execute(f"SELECT * FROM trades WHERE symbol='{self.name}'")
		result = mycursor.fetchall()

		for r in result:
			bar = {
			    'time': r['trade_timestamp'],
			    'open': float(r['open']),
			    'high': float(r['high']),
			    'low': float(r['low']),
			    'close': float(r['close']),
			    'volume': int(r['volume'])
			}
			data.append(bar)

		mydb.close()

		return data


	@staticmethod # usamos @staticmethod e não @classmethod pois não precisaremos instanciar a classe com cls
					# na verdade nem usamos name
	def initIntradayFromDate(name, path, d, sg): # d é a data em formato datetime.date

		# data = Ativo.openIntraDataWithCSV(path,d) # SE QUISER LER DE CSV USA ESSE LINHA, SENÃO USA A DEBAIXO
		data = Ativo.openIntraDataWithDB(name,d) # SE NÃO QUISER USAR DB, COMENTA ESSA LINHA E DESCOMENTA A DE CIMA

		return IntraDay(data, sg) # notar que iniciamos IntraDay() sem as outer stats, paciência.. por enquanto..


	@staticmethod
	def openIntraDataWithCSV(path, d):
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

		return data


	@staticmethod
	def openIntraDataWithDB(name,d):

		data = [] # data for an intraday

		date_str = d.strftime("%Y-%m-%d")

		mydb = mysql.connector.connect(
		  host=db['host'],
		  user=db['user'],
		  password=db['password'],
		  database=db['database']
		)

		mycursor = mydb.cursor(dictionary=True)
		mycursor.execute(f"SELECT * FROM trades WHERE symbol='{name}' AND DATE(trade_timestamp) = '{date_str}'")
		result = mycursor.fetchall()

		for r in result:
			bar = {
			    'time': r['trade_timestamp'],
			    'open': float(r['open']),
			    'high': float(r['high']),
			    'low': float(r['low']),
			    'close': float(r['close']),
			    'volume': int(r['volume'])
			}
			data.append(bar)

		mydb.close()

		return data


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