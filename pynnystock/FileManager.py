import pandas as pd
import mysql.connector

from .settings import db


class FileManager():
	'''
	Organiza os nomes e os paths de cada arquivo.
	Permite descobrir o path de um arquivo usando o seu ticker
	Como tarefa adicional, organiza arquivos auxiliares como o arquivo com free_floats
	Como outra tarefa: acessa o banco de dados e pega os nomes dos tickers
	------------------------------------------------------------------------------------------
	Exemplo: fm = fman.FileManager()
			 fm['AAMC']
	------------------------------------------------------------------------------------------
	'''
	def __init__(self):

		self.ticker = dict()
		root = '..\\..\\..\\Data\\data_dist\\'

		# names.txt contem os pares nome_do_ticker endereço_do_csv
		# names é para que ele não use a primeira row como nomes das colunas
		# index_col=0 é para usar a primeira coluna como index, senão ele vai usar index numérico de 0 em diante
		df = pd.read_csv('names.txt', names=['name','path'], index_col=0)
		df['path'] = root + df['path']
		
		# temos que fazer essa jogada com ['path'] pois não tem solução de to_dict para apenas 1 coluna.
		self.ticker = df.to_dict()['path']
		# list(di.keys())[2] # se quisesse indexar um dictionary numericamente
		self.size = len(self.ticker)
		self._initFreeFloatFile()


	def __getitem__(self,i): # é o operador de quando for chamado com []
		return self.ticker[i]


	def getNames(self):
		return list(self.ticker.keys())


	def getNamesDB(self):
		data = []

		mydb = mysql.connector.connect(
		  host=db['host'],
		  user=db['user'],
		  password=db['password'],
		  database=db['database']
		)

		mycursor = mydb.cursor()
		mycursor.execute(f"SELECT DISTINCT symbol from trades")
		result = mycursor.fetchall()

		data = [item for t in result for item in t]

		return data


	def show(self):
		print(self.ticker)


	def _initFreeFloatFile(self):
		filename = 'america_2020-11-28.csv'
		df = pd.read_csv(filename)
		df = df[['Ticker', 'Shares Float']] # apenas colunas que interessam, transformaremos essas duas cols em dictionary
		df = df.dropna()
		df = df[ df['Shares Float']>=1 ]
		df['Shares Float'] = df['Shares Float'].astype('int64')
		self.freeFloat = dict(zip(df['Ticker'],df['Shares Float']))

	def getFreeFloatNames(self):
		return list( self.freeFloat.keys() )

	def getFreeFloat(self,tick):
		return self.freeFloat[tick]