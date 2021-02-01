# algo Stop At High Pre


## 1. Descrição

O algoritmo é similar ao caso mais simples (Simpler Case) onde tínhamos uma entrada após spike de X% acima do open e saídas stop-loss e stop-target. A diferença principal está na saída que passa a ser baseada no high do pre-market.

Entrada do algoritmo

1. do tipo *short_after* (ENTRY) 

E possui as seguintes saídas
	
1. Saídas clássicas por 
	
	* Stop-Loss que vai ser calculado como um percentual acima do high das negociações do pre-market (SLHP - Stop Loss High Pre) 

	* Stop-Target definido como um valor fixo (TGT - Stop Target)

2. Saída ao fim do pregão. A posição ou o restante dela é completamente fechada no último ticker do dia. (STOP_END)

As an unknown data scientist said:

> If we have deira, let's look at deira.

## 2. Parâmetros envolvidos

#### 2.1 Filtragem

Nada muda na filtragem em relação à filtragem do algoritmo mais simples.

Parâmetro | Descrição 
----------|----------
prevol_threshold | Filtrar apenas ações que tenham volume de pre-market maior
open_dolar_threshold | Apenas ações que tenham cotação em $ maior que
gap_threshold | Apenas ações que tenham gap do open em relação ao close do dia anterior maior que
F_low_threshold | Apenas ações que tenham fator F maior que...
F_high_threshold | ...e menor que

#### 2.2 Parâmetros do Algoritmo

Parâmetro | Descrição 
----------|----------
short_after | Entrar no trade depois de % de subida em relação ao open...
exit_target | Stop-target clássico
**exit_stop_margin** | Margem de stop que vai ficar acima do high do pre market


#### 2.3 Parâmetros da Simulação

Parâmetro | Descrição 
----------|----------
start_money | Valor inicial de dinheiro, normalmente $10,000.00
allocation | Para cada trade, estaremos investindo valor nessa porcentagem do total do portfolio
locate_fee | Valor em % para alugar cada ação. É uma aproximação
commission | Corretagem. Paga metade na abertura da posição e metade no fechamento


#### 3 O que esperar no DataFrame of Filtered Days (dfd)?

Variável | Descrição 
----------|----------
name | nome do ativo
date | data do ativo-dia filtrado
freefloat | dados de freefloat do ativo (dia 28/11/2020 espelhado pra trás e pra frente)
volPre | volume do pre-market
gap | gap entre o open atual e o close do dia anterior
openToSpike% | variação percentual entre o open e a máxima do dia
minsToSpike | quanto tempo em minutos leva até alcançar a máxima do dia
volToSpike | qual o volume negociado até alcançar a máxima do dia
spikeToLow% | a variação percentual entre o high do core e a mínima do dia depois do high
minsToLowAfterSpike | quanto tempo leva desde o high até o low do dia depois do high
spikeToPreVolF | esse factor é a vol do core até o high do dia dividido pela vol do pre-market
factorF | (total volume of pre market)/(freefloat) 


#### 4 O que esperar no Dataframe of Trades (dft)?

Variável | Descrição 
----------|----------
name | nome do ativo
date | data em que houve trade (name+date é primary key)
entry_time | hora e minuto em que entrou o trade
mins_to_trade | entrou no trade depois de quantos minutos depois do open às 09:30
exit_time | hora e minuto em que saiu do trade
price | preço em que entrou no trade
stop | stop do trade
target | target do trade
profit | profit teórico do trade (sem commissions nem locate fee)
cum_profit | profit acumulado histórico (teórico, sem commissions nem locate fee) 
equity_real | total histórico de Equity em $ (real, com commissions e com locate fee)
profit_real | profit real de cada trade (com commissions e com locate fee)
cum_profit_real | profit acumulado histórico (real, com commissions e com locate fee)


#### 5 O que esperar no Dataframe of Extra Statistics (dfes)?

Variável | Descrição 
----------|----------
name | nome do ativo
date | data relativa aos dados extra (calculamos pros ativos-dias que tiveram trade)
open_pre | open do pre market
high_pre | high do pre market
low_pre | low do pre market
close_pre | close do pre market
open_core | open do core market
high_core | high do core market
low_core | low do core market
close_core | close do core market
