# Passo a passo para criação de Estratégias


#### 1. Descrever a estratégia

O ideal nessa etapa é escrever a estratégia num papel ou num arquivo .txt


#### 2. Quais parâmetros novos surgirão?

Tendo descrito a estratégia, naturalmente irão surgir os parâmetros que fazem parte dela. É hora de criar uma classe **ParametersSOMETHING** que herda da classe **Parameters** e colocar lá os parâmetros que provavelmente serão utilizados.

Ir adicionando esses novos arquivos dentro de um package em */strategies/NOME_DA_SUA_ESTRATEGIA*.


#### 3. Vai afetar alguma coisa de filtragem?

Se a estratégia possui alguma maneira diferente de filtrar os ativos em relação à filtragem do caso simples, alterar o método *runFiltering()* dentro do objeto **Simulator**.

Lembrar que todas essas mudanças devem ser feitas por meio de uma nova classe **SimulatorSOMETHING** que herda da classe **Simulator** e colocada no package da sua estratégia.


#### 4. Escrever o código da estratégia.

A lógica da estratégia vai ser registrada no método *checkForTrade()* do objeto **StratsMaestro**.

Criar nova classe **StratsMaestroSOMETHING** e sobrescrever o método *checkForTrade()*, salvando a nova classe no package */strategies/NOME_DA_SUA_ESTRATEGIA*.

Dependendo da complexidade da estratégia, podemos ter variáveis temporárias, como por exemplo para descrever se a estratégia está posicionada ou não. Essas variáveis são incluidas dentro no preâmbulo do método *checkForTrade()* do objeto **StratsMaestro** e naturalmente possuem escopo local.


#### 5. O que muda no dictionary trades?

Lembrar que enquanto o *checkForTrades()* verifica se houve trades, precisamos armazenar informações sobre o trade num dictionary *trade* para que possamos depois verificar se houve lucro, prejuízo, calcular cumulative_profit, etc. É bom ir pensando em quais informações sobre o trade precisaremos armazenar, isso pode inclusive auxiliar no passo anterior de escrever o código da estratégia.


#### 6. Alterar código de coleta de estatísticas.

Primeiramente notar como não precisamos mexer na classe Simulator. Esse é o milagre do polimorfismo em ação.

Não precisaremos modificar o método que cria Dataframe com dados sobre os ativos-dias filtrados pois o que mudou no processo foi só da maneira de fazer os trades pra frente.

Basicamente temos que alterar os métodos que coletam estatísticas sobre os trades, modificando o método *setTradesDF()* e também o método static *calculateExtraStats()*, ambos na classe **StatsGatherer.**


#### 7. Reescrever código de *printSimResults()*

Esse método fica dentro da classe **StatsGatherer**. Na verdade, o método chama o *__repr()__* de pars, portanto atualiza essa dunder function na classe **Parameters**. 


#### 8. Adaptar código de inputs de **OptimizerSimulator**.

A classe **OptmizerSimulator** trabalha com uma série de parâmetros. Para cada parâmetro é passado um range de possíveis valores e então é feita uma combinação. Para cada combinação de parâmetros é feita a otimização. Como cada estratégia tem seu conjunto de parâmetros, é natural esperar que seja necessário também um Optimizer Simulator para cada nova estratégia.

Talvez seja possível passar os parâmetros de maneira dinâmica, futuramente vou estudar maneiras inteligentes de instanciar esse objeto tal que não precisemos criar um para cada estratégia.


#### 9. Adaptar código que junta resultados do optimizer.

Lembrar que o nosso *optimizer* na verdade é a classe **OptimizerSimulator**. O *optimizer* adaptado para nossa estratégia vai ser o **OptimizerSimulatorSOMETHING**. Mas o cálculo das resultados é feito via **StatsGathererSOMETHING** usando Visitor Pattern. E para escolher quais dados vão ser guardados a cada iteração basta modificar o método *appendSimResults()* na classe **StatsGathererSOMETHING**. 