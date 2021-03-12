import pandas as pd
import pickle

from ..Ativo import Ativo
from ..indicators.Timely import Timely

from ..DaysAnalyser import DaysAnalyser

class DaysAnalyser_5m_A(DaysAnalyser):

	def runAnalysis(self):

		self.sad = []

#		for n in self.names[0:20]:
		for n in self.names:
		    print(n, end='')
		    try:
		        a = Ativo(n, self.fm, self.sg)

		        for intraday in a.intraDays:
		            tim = Timely(intraday)

		            d = {
		                 'name': a.name,
		                 'date': intraday.date,
		                 '0min':tim.times['0min'],
		                 '10min':tim.times['10min'],
		                 '20min':tim.times['20min'],
		                 '30min':tim.times['30min'],
		                 '40min':tim.times['40min'],
		                 '50min':tim.times['50min'],
		                 '1h':tim.times['1h'],
		                 '1h15':tim.times['1h15'],
		                 '1h30':tim.times['1h30'],
		                 '1h45':tim.times['1h45'],
		                 '2h':tim.times['2h'],
		                 '3h':tim.times['3h'],
		                 '4h':tim.times['4h'],
		                 '5h':tim.times['5h'],
		                 '6h':tim.times['6h'],
		                 '6h30':tim.times['6h30'],
		                 }

		            self.sad.append( d )

		    except IndexError:
		        print(": Ativo sem nenhum dado ou dado inconsistente", end='')
		    print()

		self.setAnalysedDaysDF()