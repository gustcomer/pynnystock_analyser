

import pandas as pd


def drawdown(s): # retorna o máximo drawdown de uma série
	dd = pd.Series(dtype='float64') # drawdown (dd) will be used to calculate maximum drawdown (mdd)
	# especificamos explicitamente o dtype para evitar uma warning

	for i in s.index:
		_dd = s[i]/max(s[:i+1].max(),1)-1 # i+1 pois slicing não é inclusive do ultimo termo
		# como não queremos dar append de 1 em s, usamos max(X,1) onde
		# X = s[:i+1].max()
		dd = dd.append( pd.Series( _dd ), ignore_index=True ) 
	return abs( dd.min() ) # na verdade retornamos o maximo drawdown de uma série,


def equityCurve(inicial,ps,alloc):
	'''
	Calcula a curva de equity teórica, desconsiderando commissions e locates
	inicial: montante inicial
	ps: Profit Series. Série com valores de profit teóricos de cada trade
	alloc: percent of allocation
	'''
	ec = ps*0

	for i in ec.index:
		if i == ec.index.start:
			ec.at[i] = inicial*(1+alloc*ps[i])
		else:
			ec.at[i] = ec[i-1]*(1+alloc*ps[i])

	return ec

#def profitFactor(s):