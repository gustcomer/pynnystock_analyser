import datetime
import pandas as pd

from ...OptimizerSimulator import OptimizerSimulator

class OptimizerSimulatorDEDS(OptimizerSimulator):
	
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
							short_after1 = [0],
							short_after2 = [0.1],
							firstEntryPct = [0.5],
							exit_target = [0.3], 
							exit_stop = [0.3],
							start_money = [10000],
							allocation=[0.1],
							locate_fee=[0.02],
							commission=[2]):

		parametros = [ # 1) acho que aqui sai uma list of lists, 
			[a,b,c,d,e,f,g,h,i,j,k,l,m,n]
			for a in prevol_threshold 
			for b in open_dolar_threshold
			for c in gap_threshold
			for d in F_low_threshold
			for e in F_high_threshold
			for f in short_after1
			for g in short_after2
			for h in firstEntryPct
			for i in exit_target
			for j in exit_stop
			for k in start_money
			for l in allocation
			for m in locate_fee
			for n in commission
		]

		parslist = []
		for di in parametros: # 2) mas preisamos de uma list of dictionaries
		    pars = {
		        'prevol_threshold':di[0],
		        'open_dolar_threshold':di[1],
		        'gap_threshold':di[2],
		        'F_low_threshold':di[3],
		        'F_high_threshold':di[4],
		        'short_after1':di[5],
		        'short_after2':di[6],
		        'firstEntryPct':di[7],
		        'exit_target':di[8],
		        'exit_stop':di[9],
		        'start_money':di[10],
		        'allocation':di[11],
		        'locate_fee':di[12],
		        'commission':di[13]
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
				
			self.sim.parameters.setAlgoParameters(short_after1 = p['short_after1'],
									short_after2 = p['short_after2'],
									firstEntryPct = p['firstEntryPct'],
									exit_target = p['exit_target'],
									exit_stop = p['exit_stop'])
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