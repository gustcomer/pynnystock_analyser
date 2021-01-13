from ...Parameters import Parameters

class ParametersDEDS(Parameters):


	def __init__(self):

		super().__init__()

		self.short_after1 = 0
		self.short_after2 = 0.1
		self.firstEntryPct = 0.5
		self.exit_target = 0.3
		self.exit_stop = 0.3


	def setAlgoParameters(	self, 
							short_after1 = 0, 
							short_after2 = 0.1,
							firstEntryPct = 0.5,
							exit_target = 0.3, 
							exit_stop = 0.3):

		self.short_after1 = short_after1
		self.short_after2 = short_after2
		self.firstEntryPct = firstEntryPct
		self.exit_target = exit_target
		self.exit_stop = exit_stop


	def __repr__(self):
		s='PARÂMETROS PARA ALGORITMO DO TIPO DOUBLE ENTRY DOUBLE STOP\n'
		s = s + 'FILTERING PARAMETERS\n'
		s = s + f"prevol_threshold: {self.prevol_threshold}\n"
		s = s + f"open_dolar_threshold: {self.open_dolar_threshold}\n"
		s = s + f"gap_threshold: {self.gap_threshold}\n"
		s = s + f"F_low_threshold: {self.F_low_threshold}\n"
		s = s + f"F_high_threshold: {self.F_high_threshold}\n"
		s = s + f"\n"
		s = s + f'TRADING PARAMETERS\n'
		s = s + f"short_after1: {self.short_after1}\n"
		s = s + f"short_after2: {self.short_after2}\n"
		s = s + f"firstEntryPct: {self.firstEntryPct}\n"
		s = s + f"exit_target: {self.exit_target}\n"
		s = s + f"exit_stop: {self.exit_stop}\n"
		s = s + f"\n"
		s = s + f'SIMULATION PARAMETERS\n'
		s = s + f"start_money: {self.start_money}\n"
		s = s + f"allocation: {self.allocation}\n"
		s = s + f"locate_fee: {self.locate_fee}\n"
		s = s + f"commission: {self.commission}\n"		

		return s