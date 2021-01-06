class ParametersBase:
	def __init__(self):
		self.prevol_threshold = 800000
		self.open_dolar_threshold = 2
		self.gap_threshold = 0.20
		self.F_low_threshold = 0
		self.F_high_threshold = 1

		self.start_money = 10000
		self.allocation = 0.1
		self.locate_fee = 0.02
		self.commission = 2

	def setFilterParameters(self,prevol_threshold=800000,open_dolar_threshold=2,gap_threshold=0.2,
							F_low_threshold=0,F_high_threshold=1):
		self.prevol_threshold = prevol_threshold
		self.open_dolar_threshold = open_dolar_threshold
		self.gap_threshold = gap_threshold
		self.F_low_threshold = F_low_threshold
		self.F_high_threshold = F_high_threshold

	def setAlgoParameters():
		pass

	def setSimParameters(self, start_money = 10000, allocation=0.1, locate_fee=0.02, commission=2):
		self.start_money = start_money
		self.allocation = allocation
		self.locate_fee = locate_fee
		self.commission = commission

class ParametersSimple(ParametersBase):

	def __init__(self):
		super().__init__()

		self.short_after = 0.1
		self.exit_target = 0.3
		self.exit_stop = 0.3

	def setAlgoParameters(self,short_after = 0.1, exit_target = 0.3, exit_stop = 0.3):
		self.short_after = short_after
		self.exit_target = exit_target
		self.exit_stop = exit_stop

	def __repr__(self):
		s='PARÂMETROS PARA ALGORITMO DO TIPO SIMPLE\n'
		s = s + 'FILTERING PARAMETERS\n'
		s = s + f"prevol_threshold: {self.prevol_threshold}\n"
		s = s + f"open_dolar_threshold: {self.open_dolar_threshold}\n"
		s = s + f"gap_threshold: {self.gap_threshold}\n"
		s = s + f"F_low_threshold: {self.F_low_threshold}\n"
		s = s + f"F_high_threshold: {self.F_high_threshold}\n"
		s = s + f"\n"
		s = s + f'TRADING PARAMETERS\n'
		s = s + f"short_after: {self.short_after}\n"
		s = s + f"exit_target: {self.exit_target}\n"
		s = s + f"exit_stop: {self.exit_stop}\n"
		s = s + f"\n"
		s = s + f'SIMULATION PARAMETERS\n'
		s = s + f"start_money: {self.start_money}\n"
		s = s + f"allocation: {self.allocation}\n"
		s = s + f"locate_fee: {self.locate_fee}\n"
		s = s + f"commission: {self.commission}\n"		

		return s