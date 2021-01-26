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

		#names_pennystocks = self.fm.getNames()
		names_pennystocks = self.fm.getNamesDB() # se quiser lista de names vida do DB usa essa. Senão usa a de cima.
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
#		for n in self.names[0:20]:
		for n in self.names:
		    print(n, end='')
		    try:
		        a = Ativo(n, self.fm, self.sg)
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
#		        	if minFromOpenPercent > self.minPercentThreshold: # ESSA É A CONDIÇÃO INVERSA
		        	if minFromOpenPercent <= self.minPercentThreshold:	# ESSA É A CONDIÇÃO ORIGINAL
			            d = {'name': a.name,
			                 'date': intraday.date,
			                 'minFromOpenPercent': minFromOpenPercent,
			                 'freefloat': freefloat,
			                 'price': intraday._core[0]['open'],
			                 '1stTrancheVolume': vat.volBefore,
			                 '2ndTrancheVolume': vat.volAfter,
			                 '1stTranchePercent': vat.getVolumeRate(),
			                 '1stTrancheFloatRot': vat.volBefore/freefloat,
			                 '2ndTrancheFloatRot': vat.volAfter/freefloat,
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

		adkl = {key: [dic[key] for dic in self.sad] for key in self.sad[0]}

		self.selectedAtivosDiasDF = pd.DataFrame(adkl)


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