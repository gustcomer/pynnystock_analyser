import pandas as pd
import pickle

from ..Ativo import Ativo
from ..indicators.MinFromOpen import MinFromOpen
from ..indicators.VolumeAfterTime import VolumeAfterTime
from ..indicators.MinBeforeTime import MinBeforeTime
from ..indicators.OHLCDay import OHLCDay
from ..indicators.Trade import Trade
from ..indicators.Variations import Variations
from ..indicators.Spikes import Spikes
from ..indicators.Volume import Volume

from ..DaysAnalyser import DaysAnalyser

class DaysAnalyser_S_A(DaysAnalyser):

	def runAnalysis(self):

		self.sad = [] # nesse caso todos os dias serao selecionados pelo filtro

#		for n in self.names[0:20]:
		for n in self.names:
		    print(n, end='')
		    try:
		        a = Ativo(n, self.fm, self.sg)
		        freefloat = self.fm.getFreeFloat(n)

		        for intraday in a.intraDays:
		            mfo = MinFromOpen(intraday) # indicador não parametrizável
		            minFromOpenPercent = mfo.getMinFromOpenPercent()
		            ohlc = OHLCDay(intraday)
		            trade = Trade(intraday)
		            vari = Variations(intraday)
		            spikes = Spikes(intraday)
		            volume = Volume(intraday)

		            d = {
		                 'name': a.name,
		                 'date': intraday.date,
		                 'gap': intraday.stats['gap'],
		                 'freefloat': freefloat,
		                 'price_open': intraday._core[0]['open'],
		                 'range_core': ohlc.range_core,
		                 'is_successful': trade.isSuccessful(),
		                 'open_to_close_pct': vari.openToClosePct(),
		                 'spike': spikes.spike,
		                 'spike_minutes': spikes.spike_minutes,
		                 'low_after_high': spikes.low_after_high,
		                 'low_after_high_minutes': spikes.low_after_high_minutes,
		                 'after_pullback_pct': spikes.after_pullback_pct,
		                 'volume_pre': volume.volumePreMarket(),
		                 'volume_core': volume.volumeCoreMarket(),
		                 'volume_maxima': spikes.volumeAteMaxima(),
		                 'open_pre': ohlc.open_pre,
		                 'high_pre': ohlc.high_pre,
		                 'low_pre': ohlc.low_pre,
		                 'close_pre': ohlc.close_pre,
		                 'open_core': ohlc.open_core,
		                 'high_core': ohlc.high_core,
		                 'low_core': ohlc.low_core,
		                 'close_core': ohlc.close_core,
		                 }

		            self.sad.append( d )

		    except IndexError:
		        print(": Ativo sem nenhum dado ou dado inconsistente", end='')
		    print()

		self.setAnalysedDaysDF()