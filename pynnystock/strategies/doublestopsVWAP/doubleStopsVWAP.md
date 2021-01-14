# algo Double Stops VWAP


## 1. Descrição

Esse algoritmo possui uma entrada do tipo *short_after* e possui duas saídas sendo
	
1. Saída clássica por stop-loss e stop-target

2. Saída por distânciamento ao VWAP. Se o preço do ativo cair muito abaixo do VWAP, sai de parte da posição. Existe a possibilidade de acionar essa saída após um determinado número de minutos.

3. Saída ao fim do pregão. A posição é completamente fechada no último ticker do dia.

As Erich Ratzat said:

> O position sizing é onde está
> uma parte do edge também!

## 2. Parâmetros envolvidos

#### 2.1 Filtragem

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
exit_stop | Stop-loss clássico
**vwap_distance** | Sai da position se distância ao vwap ficar maior que
**vwap_timer_minutes** | Aciona a saída por distancia do vwap apos minutos


#### 2.3 Simulação

Parâmetro | Descrição 
----------|----------
start_money | Valor inicial de dinheiro, normalmente $10,000.00
allocation | Para cada trade, estaremos investindo valor nessa porcentagem do total do portfolio
locate_fee | Valor em % para alugar cada ação. É uma aproximação
commission | Corretagem. Paga metade na abertura da posição e metade no fechamento


#### 3 Extensões

* adicionar no algoritmo a rapidez com que a distância ao vwap é alcançada
* adicionar uma saída levando em conta um determinado tempo que o preço da ação ficar acima do VWAP