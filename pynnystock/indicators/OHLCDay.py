
import numpy as np

class OHLCDay:

		def __init__(self,intra):

			self.intra = intra

			self.open_pre = intra._pre[0]['open'] if intra._pre else np.NaN
			self.high_pre = max(intra._pre, key=lambda x:x['high'])['high'] if intra._pre else np.NaN
			self.low_pre = min(intra._pre, key=lambda x:x['low'])['low'] if intra._pre else np.NaN
			self.close_pre = intra._pre[-1]['close'] if intra._pre else np.NaN
			self.open_core = intra._core[0]['open'] if intra._core else np.NaN
			self.high_core = max(intra._core, key=lambda x:x['high'])['high'] if intra._core else np.NaN
			self.low_core = min(intra._core, key=lambda x:x['low'])['low'] if intra._core else np.NaN
			self.close_core = intra._core[-1]['close'] if intra._core else np.NaN
			
			self.range_core = self.high_core-self.low_core

