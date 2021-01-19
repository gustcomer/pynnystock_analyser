import pandas as pd
import pickle

from .Ativo import Ativo
from .indicators.MinFromOpen import MinFromOpen
from .indicators.VolumeAfterTime import VolumeAfterTime
from .indicators.MinBeforeTime import MinBeforeTime
from .indicators.OHLCDay import OHLCDay

class DaysAnalyser:

	def __init__(self, fm, sg):

		self.sad = []
		self.selectedAtivosDiasDF = pd.DataFrame()

		self.fm = fm
		self.sg = sg
		self.names = []

		names_pennystocks = self.fm.getNames()
		names_free_float = self.fm.getFreeFloatNames()
		self.names = list(set(names_pennystocks) & set(names_free_float))
		self.names.sort()

		self.minPercentThreshold = -0.3


	def runAnalysis(self, 
					minPercentThreshold=-0.3,
					timeThreshold = 30,
					afterTimeThreshold = 45,
					minTime = 5
					):

		self.minPercentThreshold = minPercentThreshold

		self.sad = [] # Selected Ativo Dias (pra não confundir com adl nem com fad)
#		for n in self.names[0:50]:
		for n in self.names:
		    print(n, end='')
		    try:
		        a = Ativo(n, self.fm[n], self.sg)
		        freefloat = self.fm.getFreeFloat(n)
		        for intraday in a.intraDays:
		        	mfo = MinFromOpen(intraday) # indicador não parametrizável
		        	minFromOpenPercent = mfo.getMinFromOpenPercent()
		        	vat = VolumeAfterTime(intraday,
		        							timeThreshold=timeThreshold, 
		        							afterTimeThreshold=afterTimeThreshold
		        							)
		        	mbt = MinBeforeTime(intraday,
		        						minTime=minTime
		        						)
		        	ohlc = OHLCDay(intraday)
		        	if minFromOpenPercent <= self.minPercentThreshold:
			            d = {'name': a.name,
			                 'date': intraday.date,
			                 'minFromOpenPercent': minFromOpenPercent,
			                 'freefloat': freefloat,
			                 'price': intraday._core[0]['open'],
			                 '1stTrenchVolume': vat.volBefore,
			                 '2ndTrenchVolume': vat.volAfter,
			                 '1stTrenchPercent': vat.getVolumeRate(),
			                 '1stTrenchFloatRot': vat.volBefore/freefloat,
			                 '2ndTrenchFloatRot': vat.volAfter/freefloat,
			                 'minPctBeforeTime': mbt.getLowPercentBeforeMinutes(),
			                 'open_pre': ohlc.open_pre,
			                 'high_pre': ohlc.high_pre,
			                 'low_pre': ohlc.low_pre,
			                 'close_pre': ohlc.close_pre,
			                 'open_core': ohlc.open_core,
			                 'high_core': ohlc.high_core,
			                 'low_core': ohlc.low_core,
			                 'close_core': ohlc.close_core,
			                 'gap': intraday.stats['gap']
			                 }
			            self.sad.append( d )
		    except IndexError:
		        print(": Ativo sem nenhum dado ou dado inconsistente", end='')
		    print()
		self.setAnalysedDaysDF()


	def setParameters(self,
						minPercentThreshold = -0.3,
						timeThreshold = 30,
						afterTimeThreshold = 45,
						minTime = 5):

		self.minPercentThreshold = minPercentThreshold
		self.timeThreshold = timeThreshold
		self.afterTimeThreshold = afterTimeThreshold
		self.minTime = minTime


	def setAnalysedDaysDF(self):
		df = pd.DataFrame({ 'name':[],
		                    'date':[],
		                    'minFromOpenPercent':[],
		                    'freefloat':[],
		                    'price':[],
		                    '1stTrenchVolume':[],
		                    '2ndTrenchVolume':[],
		                    '1stTrenchPercent':[],
		                    '1stTrenchFloatRot':[],
		                    '2ndTrenchFloatRot':[],
		                    'minPctBeforeTime':[],
		                    'open_pre':[],
		                    'high_pre':[],
		                    'low_pre':[],
		                    'close_pre':[],
		                    'open_core':[],
		                    'high_core':[],
		                    'low_core':[],
		                    'close_core':[],
		                    'gap':[]
		                    })

		for d in self.sad: # para cada dia nos selected ativo-dias
		    df = df.append({ 'name':d['name'],
		                     'date':d['date'], #.strftime("%d/%m/%Y"), datetime é melhor que string
		                     'minFromOpenPercent': d['minFromOpenPercent'],
		                     'freefloat': d['freefloat'],
		                     'price': d['price'],
		                     '1stTrenchVolume': d['1stTrenchVolume'],
		                     '2ndTrenchVolume':d['2ndTrenchVolume'],
		                     '1stTrenchPercent':d['1stTrenchPercent'],
		                     '1stTrenchFloatRot':d['1stTrenchFloatRot'],
		                     '2ndTrenchFloatRot':d['2ndTrenchFloatRot'],
		                     'minPctBeforeTime':d['minPctBeforeTime'],
		                     'open_pre':d['open_pre'],
		                     'high_pre':d['high_pre'],
		                     'low_pre':d['low_pre'],
		                     'close_pre':d['close_pre'],
		                     'open_core':d['open_core'],
		                     'high_core':d['high_core'],
		                     'low_core':d['low_core'],
		                     'close_core':d['close_core'],
		                     'gap':d['gap']},
		                   ignore_index=True)
		    df = df.sort_values(by='date',ignore_index=True)

		self.selectedAtivosDiasDF = df

	def saveSelectedAD(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.sad,filehandle)

	def openSelectedAD(self,filename):
		with open(filename, 'rb') as filehandle: # w de read e b de binary
		    self.sad = pickle.load(filehandle)
		    self.setAnalysedDaysDF()

	def saveSelectedAtivoDiasDF(self,filename):
		with open(filename, 'wb') as filehandle: # w de write e b de binary
		    pickle.dump(self.selectedAtivosDiasDF,filehandle)

	def openSelectedAtivoDiasDF(self,filename):
		with open(filename, 'rb') as filehandle: # w de read e b de binary
		    self.selectedAtivosDiasDF = pickle.load(filehandle)