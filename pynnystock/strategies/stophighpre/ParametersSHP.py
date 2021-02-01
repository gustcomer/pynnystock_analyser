from ...Parameters import Parameters

class ParametersSHP(Parameters):

	def __init__(self):

		super().__init__() # inicializa tudo mas algumas variaveis da super vão ficar de fora. Bad software engineering practice

		# repetimos a declaração de alguns parâmetros só pra enfatizar. Bad practice.
		self.short_after = 0.1
		self.exit_target = 0.3

		self.exit_stop_margin = 0.1 # se high do pre for $5.00, stop vai ficar em $5.50


	def setAlgoParameters(	self, 
							short_after = 0.1, 
							exit_target = 0.3, 
							exit_stop_margin = 0.1):

		self.short_after = short_after
		self.exit_target = exit_target
		self.exit_stop_margin = exit_stop_margin


	def __repr__(self):
		s='PARÂMETROS PARA ALGORITMO DO TIPO STOP AT HIGH OF PRE-MARKET\n'
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
		s = s + f"exit_stop_margin: {self.exit_stop_margin}\n"
		s = s + f"\n"
		s = s + f'SIMULATION PARAMETERS\n'
		s = s + f"start_money: {self.start_money}\n"
		s = s + f"allocation: {self.allocation}\n"
		s = s + f"locate_fee: {self.locate_fee}\n"
		s = s + f"commission: {self.commission}\n"		

		return s