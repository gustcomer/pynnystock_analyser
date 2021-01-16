import datetime
import pandas as pd

from ...OptimizerSimulator import OptimizerSimulator

class OptimizerSimulatorDSVW(OptimizerSimulator):
	
	def __init__(self, simulator, bs_simulator, sg):
		self.sim = simulator
		self.bs_sim = bs_simulator
		self.sg = sg


	def runSimulationGroup(self,
							prevol_threshold=[800000],
							open_dolar_threshold=[2],
							gap_threshold=[0.2],
							F_low_threshold=[0],
							F_high_threshold=[1],
							short_after = [0],
							exit_target = [0.3],
							exit_stop = [0.3],
							vwap_distance = [0.20], 
							vwap_timer_minutes = [10],
							vwap_pct = [0.5],
							exit_after_minutes = [60],
							start_money = [10000],
							allocation=[0.1],
							locate_fee=[0.02],
							commission=[2]):

		parametros = [ # 1) acho que aqui sai uma list of lists, 
			[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p]
			for a in prevol_threshold 
			for b in open_dolar_threshold
			for c in gap_threshold
			for d in F_low_threshold
			for e in F_high_threshold
			for f in short_after
			for g in exit_target
			for h in exit_stop
			for i in vwap_distance
			for j in vwap_timer_minutes
			for k in vwap_pct
			for l in exit_after_minutes
			for m in start_money
			for n in allocation
			for o in locate_fee
			for p in commission
		]

		parslist = []
		for di in parametros: # 2) mas preisamos de uma list of dictionaries
		    pars = {
		        'prevol_threshold':di[0],
		        'open_dolar_threshold':di[1],
		        'gap_threshold':di[2],
		        'F_low_threshold':di[3],
		        'F_high_threshold':di[4],

		        'short_after':di[5],
		        'exit_target':di[6],
		        'exit_stop':di[7],
		        'vwap_distance':di[8],
		        'vwap_timer_minutes':di[9],
		        'vwap_pct':di[10],
		        'exit_after_minutes':di[11],

		        'start_money':di[12],
		        'allocation':di[13],
		        'locate_fee':di[14],
		        'commission':di[15]
		    }
		    parslist.append(pars)
		# parslist

		print(f"Simulando {len(parslist)} combinações de parâmetros.")

		for p in parslist: # 3) para cada dictionary da list
			self.sim.parameters.setFilterParameters(prevol_threshold=p['prevol_threshold'],
									open_dolar_threshold=p['open_dolar_threshold'],
									gap_threshold=p['gap_threshold'],
									F_low_threshold=p['F_low_threshold'],
									F_high_threshold=p['F_high_threshold'])
			self.sim.runFiltering()
				
			self.sim.parameters.setAlgoParameters(short_after = p['short_after'],
									exit_target = p['exit_target'],
									exit_stop = p['exit_stop'],
									vwap_distance = p['vwap_distance'],
									vwap_timer_minutes = p['vwap_timer_minutes'],
									vwap_pct = p['vwap_pct'],
									exit_after_minutes = p['exit_after_minutes'])

			self.sim.parameters.setSimParameters(start_money = p['start_money'],
								allocation = p['allocation'],
								locate_fee=p['locate_fee'],
								commission=p['commission'])

			now = datetime.datetime.now()
			now_str = now.strftime("%d/%m/%Y %H:%M:%S")
			print("running another simulation.", now_str)
			self.sim.runSimulation()
			self.bs_sim.runBootstrap(n_iter=50, replace=False) # we will need data such as meanmax_drawdown, 
																# maxmax_drawdown, minmax_drawdown
			self.sg.appendSimResults()
			#self.bsresults = self.results.append(self.getSimResults(),ignore_index=True)