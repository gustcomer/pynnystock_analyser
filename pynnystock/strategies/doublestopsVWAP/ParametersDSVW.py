from ...Parameters import Parameters

class ParametersDSVW(Parameters):


	def __init__(self):

		super().__init__()

		self.short_after = 0.1
		self.exit_target = 0.3
		self.exit_stop = 0.3

		self.vwap_distance = 0.20
		self.vwap_timer_minutes = 10
		self.vwap_pct = 0.5
		self.exit_after_minutes = 300


	def setAlgoParameters(	self, 
							short_after = 0.1, 
							exit_target = 0.3, 
							exit_stop = 0.3,
							vwap_distance = 0.20, 
							vwap_timer_minutes = 10,
							vwap_pct = 0.5,
							exit_after_minutes = 300):

		self.short_after = short_after
		self.exit_target = exit_target
		self.exit_stop = exit_stop
		self.vwap_distance = vwap_distance
		self.vwap_timer_minutes = vwap_timer_minutes
		self.vwap_pct = vwap_pct
		self.exit_after_minutes = exit_after_minutes


	def __repr__(self):
		s='PARÂMETROS PARA ALGORITMO DO TIPO DOUBLE STOP VWAP\n'
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
		s = s + f"vwap_distance: {self.vwap_distance}\n"
		s = s + f"vwap_timer_minutes: {self.vwap_timer_minutes}\n"
		s = s + f"vwap_pct: {self.vwap_pct}\n"
		s = s + f"exit_after_minutes: {self.exit_after_minutes}\n"
		s = s + f"\n"
		s = s + f'SIMULATION PARAMETERS\n'
		s = s + f"start_money: {self.start_money}\n"
		s = s + f"allocation: {self.allocation}\n"
		s = s + f"locate_fee: {self.locate_fee}\n"
		s = s + f"commission: {self.commission}\n"		

		return s