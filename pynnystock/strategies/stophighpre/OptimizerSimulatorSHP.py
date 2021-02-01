import datetime
import pandas as pd

from ...OptimizerSimulator import OptimizerSimulator


class OptimizerSimulatorSHP(OptimizerSimulator):

	def runSimulationGroup(self,
							prevol_threshold=[800000],
							open_dolar_threshold=[2],
							gap_threshold=[0.2],
							F_low_threshold=[0],
							F_high_threshold=[1],
							short_after = [0.1],
							exit_target = [0.3],
							exit_stop_margin = [0.1],
							start_money = [10000],
							allocation=[0.1],
							locate_fee=[0.02],
							commission=[2]):

		parametros = [
			[a,b,c,d,e,f,g,h,i,j,k,l]
			for a in prevol_threshold 
			for b in open_dolar_threshold
			for c in gap_threshold
			for d in F_low_threshold
			for e in F_high_threshold
			for f in short_after
			for g in exit_target
			for h in exit_stop_margin
			for i in start_money
			for j in allocation
			for k in locate_fee
			for l in commission
		]

		parslist = []
		for l in parametros:
		    pars = {
		        'prevol_threshold':l[0],
		        'open_dolar_threshold':l[1],
		        'gap_threshold':l[2],
		        'F_low_threshold':l[3],
		        'F_high_threshold':l[4],

		        'short_after':l[5],
		        'exit_target':l[6],
		        'exit_stop_margin':l[7],
		        
		        'start_money':l[8],
		        'allocation':l[9],
		        'locate_fee':l[10],
		        'commission':l[11]
		    }
		    parslist.append(pars)
		parslist

		print(f"Simulando {len(parslist)} combinações de parâmetros.")

		for p in parslist:
			self.sim.parameters.setFilterParameters(prevol_threshold=p['prevol_threshold'],
									open_dolar_threshold=p['open_dolar_threshold'],
									gap_threshold=p['gap_threshold'],
									F_low_threshold=p['F_low_threshold'],
									F_high_threshold=p['F_high_threshold'])
			self.sim.runFiltering()
				
			self.sim.parameters.setAlgoParameters(short_after = p['short_after'],
									exit_target = p['exit_target'],
									exit_stop_margin = p['exit_stop_margin'])
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