
from .VolumeAfterTime import VolumeAfterTime

class FloatRotationAfterTime:

	def __init__(self,intra, freefloat):

		self.intra = intra

		v = VolumeAfterTime(self.intra)

		self.volBefore = v.volBefore
		self.volAfter = v.volAfter

