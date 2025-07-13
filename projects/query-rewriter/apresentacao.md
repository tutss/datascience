Text-to-SQL com Sistemas Multiagentes
Artur Magalh˜aes dos Santos∗, Daniel Ferreira Schulz∗,
Guilherme Narciso Lee∗, Pedro Rezende Mendonc¸a∗
∗Departamento de Ciˆencia da Computac¸ ˜ao do Instituto de Matem´atica e Estat´ıstica da Universidade de S˜ao Paulo, Brasil
{artur santos, danielschulz, narcisolee2002, pedro.rezende.mendonca}@usp.br
Abstract—Efficient access to large volumes of structured data
remains a challenge, especially for non-technical users. Text-to-
SQL approaches aim to translate natural language questions
into SQL queries, and recent advances in Large Language
Models (LLMs) have improved their performance. However, most
current solutions use single-agent architectures, which may limit
modularity and validation.
This paper investigates whether multi-agent architectures can
outperform single-agent systems in Text-to-SQL tasks. We de-
veloped Mimir, a system composed of four specialized agents
using the CrewAI framework, and compared it to a single-agent
baseline. Experiments were conducted on two databases with 27
natural language questions and gold-standard SQL queries.
The results indicate that the multi-agent architecture achieves
comparable accuracy to the single-agent model in manually
audited queries, although at a higher computational cost. We
observed that most discrepancies between expected and actual
outputs were due to lexical mismatches (e.g., singular/plural
forms and language translation), rather than logical errors
in query construction. Furthermore, automated LLM auditing
yielded a high false negative rate, highlighting the need for
execution-based evaluation metrics. These findings suggest that
while multi-agent systems offer modularity and extensibility, their
benefits are not evident for low-complexity queries. Future work
includes expanding the evaluation to more complex benchmarks,
refining prompt engineering strategies, and exploring alternative
agent topologies.
Index Terms—Text-to-SQL, Multi-agent Systems, LLM-as-a-
Judge
I. INTRODUC¸ ˜AO
O consumo eficiente a grandes volumes de dados estrutu-
rados ´e um desafio recorrente para aqueles que dependem da
tomada de decis˜ao orientada por dados. Embora a linguagem
de consulta SQL seja amplamente adotada, sua utilizac¸ ˜ao
depende de conhecimento t´ecnico especializado, restringindo o
acesso a dados por parte de usu´arios n˜ao t´ecnicos. Esse cen´ario
motivou o desenvolvimento de abordagens Text-to-SQL, que
visam traduzir perguntas em linguagem natural para consultas
SQL.
Com o avanc¸o dos modelos de aprendizado profundo e, mais
recentemente, de Grandes Modelos de Linguagem (LLMs),
Text-to-SQL tem obtido resultados melhores, inclusive em
cen´arios de m´ultiplos dom´ınios e esquemas complexos. No
entanto, a maioria das soluc¸ ˜oes atuais utiliza abordagens
com agentes ´unicos, generalizando a resoluc¸ ˜ao dos problemas
envolvidos na tarefa de traduc¸ ˜ao.
Diante disso, este trabalho busca responder `a seguinte
quest˜ao de pesquisa: abordagens baseadas em m´ultiplos
agentes podem superar arquiteturas com agente ´unico na tarefa
de gerac¸ ˜ao de consultas SQL a partir de linguagem natural?
Para investigar essa quest˜ao, este trabalho tem como ob-
jetivo comparar duas arquiteturas distintas para a tarefa de
Text-to-SQL: uma baseada em um ´unico agente, que centraliza
todas as decis˜oes, e outra composta por m´ultiplos agentes
especializados que interagem para propor, revisar e refinar a
consulta gerada. O estudo ´e conduzido por meio de um ex-
perimento controlado, considerando tanto a qualidade sint´atica
das consultas geradas quanto a correc¸ ˜ao dos resultados obtidos
ap´os sua execuc¸ ˜ao nos bancos de dados.
O restante deste artigo est´a organizado da seguinte forma:
a Sec¸ ˜ao II apresenta os conceitos te´oricos fundamentais
relacionados a LLMs, sistemas multiagentes e Text-to-SQL.
A sec¸ ˜ao III discute os trabalhos relacionados. A sec¸ ˜ao IV
descreve o estudo de caso desenvolvido. A sec¸ ˜ao V apresenta
os resultados e an´alise comparativa, e a sec¸ ˜ao VI conclui o
trabalho e apresenta trabalhos futuros.
II. FUNDAMENTAC¸ ˜AO TE ´ORICA
A. Large Language Models
Os Grandes Modelos de Linguagem (do inglˆes LLM -
Large Language Models) s˜ao modelos de Inteligˆencia Artificial
capazes de compreender e gerar linguagem natural [1]. De
modo geral, utilizam distribuic¸ ˜ao de probabilidade condicional
para prever a pr´oxima palavra em uma sequˆencia de texto
[2]. Esses c´alculos s˜ao realizados em redes neurais baseadas
na arquitetura Transformer, que se apoia no mecanismo de
atenc¸ ˜ao introduzido por Vaswani et al. [3]. Esse mecanismo
permite a paralelizac¸ ˜ao do treinamento e tratamento eficiente
de dependˆencias de longo alcance entre palavras.
Os avanc¸os introduzidos pelo mecanismo de atenc¸ ˜ao pos-
sibilitaram a criac¸ ˜ao de modelos com um n´umero significati-
vamente maior de parˆametros. Essa escalabilidade ´e uma das
principais caracter´ısticas que diferenciam as LLMs de modelos
de linguagem anteriores, permitindo que sejam treinadas com
bilh˜oes de parˆametros sobre vastas quantidades de dados
textuais [4]. Ao fornecer exemplos e instruc¸ ˜oes diretamente
na entrada, esses modelos passam a adaptar suas respostas a
tarefas espec´ıficas, demonstrando a capacidade de aprendizado
em contexto, conhecida como in-context learning [5].
Adicionalmente, t´ecnicas como Retrieval-Augmented Gen-
eration (RAG) [6] tˆem sido empregadas para ampliar o
escopo de atuac¸ ˜ao dos LLMs, ao permitir a recuperac¸ ˜ao
de informac¸ ˜oes externas e atualizadas que complementam
seu conhecimento treinado. Essa abordagem potencializa a
aplicac¸ ˜ao dos modelos em tarefas que demandam conheci-
mento factual e especializado [7]. Com isso, torna-se poss´ıvel
adaptar LLMs a diferentes dom´ınios da atividade humana,
como medicina, financ¸as, pesquisa acadˆemica, desenvolvi-
mento de software e traduc¸ ˜ao autom´atica, entre outros [8].
B. Sistemas Multiagentes
Para aprimorar o desempenho dos LLMs, diversas t´ecnicas
e arquiteturas tˆem sido exploradas. Entre elas, destacam-se a
cadeia de pensamento (chain-of-thought, [29]), engenharia de
prompts, auto-refinamento e ReAct (Reasoning and Acting,
[34]), que buscam fortalecer habilidades como racioc´ınio,
planejamento e uso de ferramentas externas pelos modelos.
Uma abordagem complementar que vem ganhando destaque
´e o uso de sistemas multiagentes, que tˆem se mostrado
promissores na melhoria da factualidade e da capacidade de
racioc´ınio dos modelos em comparac¸ ˜ao a estrat´egias baseadas
em modelos isolados. Em alguns cen´arios, essas configurac¸ ˜oes
multiagentes apresentam desempenho superior [9]. Nessa
configurac¸ ˜ao, m´ultiplas instˆancias do modelo interagem por
meio de propostas, cr´ıticas e refinamentos m´utuos ao longo de
v´arias rodadas, com o objetivo de convergir para uma resposta
mais confi´avel e precisa.
No contexto da Inteligˆencia Artificial, um agente ´e definido
como uma entidade computacional autˆonoma capaz de perce-
ber seu ambiente, tomar decis˜oes e executar ac¸ ˜oes de forma
orientada a objetivos [10]. J´a um sistema multiagente ´e com-
posto por um conjunto desses agentes, que cooperam (ou com-
petem) para resolver problemas complexos que ultrapassam a
capacidade de agentes individuais [11].
As interac¸ ˜oes entre m´ultiplos agentes podem ser classifi-
cadas em trˆes categorias principais: cooperativas, nas quais
os agentes colaboram para atingir um objetivo comum; ad-
vers´arias, em que cada agente busca maximizar seu pr´oprio
benef´ıcio; e mistas, que combinam elementos das duas abor-
dagens [12]. Essa flexibilidade torna os sistemas multiagentes
aplic´aveis a uma ampla gama de dom´ınios, como desenvolvi-
mento de software, automac¸ ˜ao industrial, pesquisa cient´ıfica,
jogos e simulac¸ ˜oes complexas.
C. Text-to-SQL
O consumo e a an´alise de dados tˆem crescido nos ´ultimos
anos devido `a valorizac¸ ˜ao desse ativo estrat´egico. Como
muitos desses dados est˜ao estruturados em grandes bancos,
dentro de uma estrutura relacional e frequentemente com-
postos por diversas tabelas, recuperar informac¸ ˜oes de forma
precisa pode representar um desafio. Nesse contexto, Text-to-
SQL dedica-se a democratizar o acesso a dados por meio de
consultas em sistemas gerenciadores de bancos de dados [13].
De forma simples, Text-to-SQL ´e o processo de traduc¸ ˜ao
de uma pergunta em linguagem natural humana para uma
consulta SQL. Para isso, a abordagem deve compreender
a intenc¸ ˜ao semˆantica da pergunta, identificar as tabelas e
colunas, al´em de realizar operac¸ ˜oes de agregac¸ ˜ao e filtragem
[14]. Por fim, o algoritmo pode ser avaliado sob diferentes
aspectos, como o resultado final da consulta no banco de dados
ou a similaridade da consulta em relac¸ ˜ao a sua correspondˆencia
com uma consulta de referˆencia anotada manualmente.
Essa abordagem ´e ´util em aplicac¸ ˜oes como sistemas con-
versacionais, ferramentas de an´alises de dados e em sistemas
gerenciadores de banco de dados. No entanto, alguns aspectos
ainda s˜ao desafios para essa ´area, como a ordenac¸ ˜ao dos
predicados na linguagem SQL, complexidade de m´ultiplos
dom´ınios de informac¸ ˜ao, ambiguidade semˆantica das consultas
entre outros [15]. Al´em disso, o desempenho dos modelos
pode variar dependendo do esquema, forma de anotac¸ ˜ao
das perguntas e da disponibilidade de dados de treinamento
diversificados.
III. TRABALHOS RELACIONADOS
A tarefa de Text-to-SQL tem sido amplamente explorada nas
´ultimas d´ecadas, impulsionada pela crescente necessidade de
tornar dados acess´ıveis a usu´arios sem conhecimento t´ecnico
em SQL. Diversas abordagens foram propostas ao longo
do tempo, desde modelos baseados em regras at´e os mais
modernos grandes modelos de linguagem. Nesta sec¸ ˜ao, s˜ao
apresentados trabalhos relevantes sobre o tema, com ˆenfase
nas suas contribuic¸ ˜oes, limitac¸ ˜oes e impacto no avanc¸o do
estado da arte.
A. Abordagens cl´assicas de Text-to-SQL
Os primeiros trabalhos de traduc¸ ˜ao entre linguagem natural
e bancos de dados relacionais foram inspirados por t´ecnicas da
´area de recuperac¸ ˜ao da informac¸ ˜ao (IR). Ferramentas como o
DISCOVER [27], IR-style [28] e SPARK [24] implementaram
mecanismos de busca por palavras-chave em bancos de dados
relacionais. Essas abordagens tentavam identificar os elemen-
tos mais relevantes das consultas com base na correspondˆencia
textual entre as palavras-chave da pergunta e os elementos
do esquema relacional, como nomes de tabelas e atributos.
Embora ´uteis, tais m´etodos eram limitados na sua capacidade
de representar intenc¸ ˜oes mais complexas, como agregac¸ ˜oes,
junc¸ ˜oes ou condic¸ ˜oes compostas.
Avanc¸os posteriores buscaram estruturar a interpretac¸ ˜ao da
linguagem natural por meio de t´ecnicas de parsing semˆantico.
Sistemas como SQLizer [22], que sintetiza consultas a partir
da linguagem natural, e o trabalho de Li e Jagadish [25],
que prop˜oe interfaces interativas para usu´arios, ilustram essa
linha de pesquisa. Tamb´em se destaca a proposta de Iyer
et al. [26], que utiliza retorno do usu´ario para refinar o
mapeamento semˆantico, antecipando t´ecnicas supervisionadas
mais modernas.
Modelos baseados em aprendizado de m´aquina iniciaram
um grande avanc¸o ao substituir heur´ısticas r´ıgidas por t´ecnicas
supervisionadas. O Seq2SQL [20] foi um dos primeiros a
explorar o uso de aprendizado por reforc¸o para gerar con-
sultas SQL a partir de linguagem natural, considerando a
correspondˆencia com os resultados esperados no banco de
dados. Posteriormente, Guo et al. [21] propuseram o uso
de representac¸ ˜oes intermedi´arias para lidar com consultas
mais complexas em ambientes multi-esquema. J´a o RAT-SQL
[23] introduziu um mecanismo de codificac¸ ˜ao relacional com
atenc¸ ˜ao contextualizada, permitindo ao modelo incorporar de
forma mais eficaz a estrutura do banco de dados durante o
processo de gerac¸ ˜ao.
A consolidac¸ ˜ao dessas abordagens foi impulsionada pelo
surgimento de benchmarks amplamente adotados na literatura.
O WikiSQL [20] ofereceu um dos primeiros conjuntos em
larga escala com pares pergunta-SQL, focando em consultas
simples sobre tabelas ´unicas. Em contrapartida, o Spider
[18] introduziu um benchmark de m´ultiplos dom´ınios com
consultas SQL complexas, m´ultiplas tabelas e diversos es-
quemas, estabelecendo um novo padr˜ao para avaliac¸ ˜ao de
generalizac¸ ˜ao e robustez dos modelos. Esses benchmarks n˜ao
apenas viabilizaram comparac¸ ˜oes consistentes entre trabalhos,
mas tamb´em incentivaram o desenvolvimento de arquiteturas
mais sofisticadas voltadas `a compreens˜ao semˆantica e `a estru-
tura relacional dos dados.
B. Avanc¸os com LLMs
A evoluc¸ ˜ao dos Language Models para Text-to-SQL acom-
panhou os avanc¸os gerais do processamento de linguagem
natural (PLN). Inicialmente, modelos baseados em arquite-
turas recorrentes (RNNs/LSTMs) e redes convolucionais
mostraram-se limitados para capturar dependˆencias de longo
prazo e estruturas sint´aticas complexas necess´arias para a
gerac¸ ˜ao de consultas SQL [20].
A arquitetura Transformer, introduzida por Vaswani et al.
[3], superou as limitac¸ ˜oes dos modelos precedentes ao adotar
uma abordagem centrada em mecanismos de atenc¸ ˜ao. Essa
inovac¸ ˜ao permitiu a captura de relac¸ ˜oes contextuais entre
tokens independentemente de sua distˆancia na sequˆencia,
grac¸as ao mecanismo de self-attention. Al´em disso, a ar-
quitetura possibilitou o processamento paralelo de sequˆencias
completas e a modelagem eficiente de hierarquias sint´aticas
complexas, caracter´ısticas anteriormente inating´ıveis com ar-
quiteturas recorrentes.
Essa revoluc¸ ˜ao introduzida com o desenvolvimento da ar-
quitetura Transformer impulsionou o desenvolvimento dos
Modelos de Linguagem modernos. Radford et al. [35] com
o GPT estabeleceu um novo paradigma ao demonstrar trˆes
princ´ıpios fundamentais: o pr´e-treinamento em corpus mas-
sivos (centenas de GB de texto) possibilita a aprendiza-
gem de padr˜oes lingu´ısticos profundos; o ajuste fino com
poucos exemplos adapta eficientemente o modelo a tarefas es-
pec´ıficas; e arquiteturas puramente auto-regressivas (decoder-
only) mostram-se altamente eficazes para gerac¸ ˜ao textual. Vale
destacar que esses modelos operam de forma generativa, pro-
duzindo sa´ıdas coerentes a partir de prompts de entrada, car-
acter´ıstica que se tornou fundamental para aplicac¸ ˜oes pr´aticas.
O sucesso dessa abordagem levou ao surgimento de sistemas
como o ChatGPT e modelos especializados como o SQLCoder.
Essas aplicac¸ ˜oes demonstram capacidade not´avel de gerar
consultas SQL funcionais a partir de prompts em linguagem
natural, seja incorporando informac¸ ˜oes do esquema do banco
diretamente no contexto do prompt, seja atrav´es de ferramentas
auxiliares que recuperam metadados da estrutura do banco de
dados.
Fig. 1: Benchmark BIRD comparando, o score de Execution
Accuracy de agentes humanos e sistemas envolvendo modelos
de linguagem
Assim, diversas abordagens utilizando LLMs como motor
de inferˆencia principal surgiram, cada uma com ferramentas
de extrac¸ ˜ao de dados de bancos, modelos espec´ıficos de
linguagem e arquiteturas diferentes umas das outras, o que
possibilitou a utilizac¸ ˜ao dessas abordagens em diversos casos
e variac¸ ˜oes de SQL diferentes.
Contudo, apesar desses avanc¸os, os resultados em bench-
marks como Spider [18] e BIRD [33] ainda revelam limitac¸ ˜oes
significativas, particularmente em consultas complexas envol-
vendo m´ultiplas tabelas ou operac¸ ˜oes de agregac¸ ˜ao aninhadas,
onde as taxas de acur´acia frequentemente permanecem abaixo
do patamar ideal para aplicac¸ ˜oes em produc¸ ˜ao.
C. Arquiteturas baseadas em Sistemas Multiagentes
Sistemas multiagentes podem ser constru´ıdos com difer-
entes topologias. Uma forma convencional ´e organizar os
agentes de forma sequencial. Ou seja, um agente realiza um
processamento, passando os resultados para o pr´oximo, assim
por diante.
Outra possibilidade ´e organizar os agentes em mesh (2). Na
arquitetura em mesh, os agentes trabalham em colaborac¸ ˜ao,
podendo ser todos conectados entre si. Um aspecto importante
´e que o controle n˜ao ´e delegado necessariamente a somente
um agente, os agentes interagem entre si, com um objetivo
comum .
A forma hier´arquica de organizac¸ ˜ao consiste um agente
atuando como orquestrador, enquanto delega e escolhe outros
agentes para realizar partes de uma tarefa principal. Aqui ´e
not´avel a separac¸ ˜ao de responsabilidades. Os agentes chama-
dos pelo orquestrador funcionam como func¸ ˜oes a tarefas
espec´ıficas, permitindo uma especializac¸ ˜ao detalhada de cada
agente.
D. Justificativa
Apesar dos avanc¸os descritos, grande parte dos trabalhos
recentes depende de arquiteturas centralizadas com agentes
Fig. 2: Exemplo de sistema multiagentes mesh. Fonte: Strands
SDK
Fig. 3: Exemplo de sistema multiagentes hier´arquica. Fonte:
Strands SDK
´unicos, o que pode limitar a capacidade de decomposic¸ ˜ao
semˆantica e validac¸ ˜ao das consultas geradas. Neste contexto,
abordagens multiagentes surgem como uma alternativa promis-
sora para superar essas limitac¸ ˜oes, promovendo maior modu-
laridade, especializac¸ ˜ao e robustez na gerac¸ ˜ao de consultas
SQL. Al´em disso, nenhum dos trabalhos citados realiza a
comparac¸ ˜ao dos resultados entre modelos de agentes ´unicos
com multiagentes, o que justifica a necessidade deste trabalho.
IV. ESTUDO DE CASO
Como estudo de caso para Text-to-SQL, implementamos
um sistema multi-agentes que tem como objetivo construir
uma query em SQL a partir de um texto fornecido pelo
usu´ario. Em muitos casos, usu´arios de sistemas de bancos
de dados n˜ao possuem familiaridade com a linguagem SQL.
Tamb´em, quando pensamos na elaborac¸ ˜ao de uma consulta,
muitas vezes ´e mais f´acil descrevˆe-la textualmente do que
escrever diretamente a consulta em SQL.
Nosso sistema, denominado Mimir, constr´oi e executa uma
consulta SQL fornecida pelo usu´ario, automaticamente sele-
cionando quais tabelas e quais informac¸ ˜oes deve resgatar para
que a consulta seja realizada com sucesso. Al´em do resultado
final, para fins did´aticos, ele tamb´em mostra qual foi a consulta
executada.
A. Arquitetura
A aplicac¸ ˜ao foi elaborada utilizando a biblioteca CrewAI.
Ela facilita a construc¸ ˜ao de sistemas multi-agentes (1) com
uma API padronizada para as interac¸ ˜oes entre agentes, (2)
facilidade de integrac¸ ˜ao com plataformas de LLMs como a
OpenAI e tamb´em (3) separa a especificac¸ ˜ao dos agentes -
e.g. objetivos e descric¸ ˜oes - do c´odigo de aplicac¸ ˜ao.
Nosso sistema ´e constitu´ıdo por 4 agentes sequenciais,
cada um com responsabilidades e objetivos diferentes. Na
nomenclatura padr˜ao do CrewAI, para definirmos um agente,
precisamos especificar: (1) role, o papel que o agente vai
desempenhar; (2) goal, o objetivo do agente; (3) backstory,
contexto adicional do papel que o agente deve desempenhar;
(4) llm, qual LLM o agente vai utilizar.
Um agente tamb´em ´e associado a uma task. Pela definic¸ ˜ao
do CrewAI, ”as Tasks fornecem todos os detalhes necess´arios
para a execuc¸ ˜ao, como uma descric¸ ˜ao, o agente respons´avel, as
ferramentas exigidas e mais, facilitando uma ampla variedade
de complexidades de ac¸ ˜ao”. Ou seja, representam a tarefa que
o agente vai desempenhar.
A figura 4 apresenta a arquitetura da aplicac¸ ˜ao Mimir e os
modelos LLM utilizados para cada agente.
Nossa aplicac¸ ˜ao possui os agentes (1) Rewriter, (2) SQL
Writer, (3) Optimizer e o Auditor. Cada agente ´e executado
sequencialmente, na ordem descrita. O primeiro deles, o
Rewriter, tem como objetivo reescrever a frase do usu´ario. O
usu´ario pode escrever uma frase errada ou at´e mesmo adicionar
um texto extra acidentalmente. A premissa do primeiro agente
´e corrigir isto. A ideia de um agente de rescrita tamb´em
adv´em de uma futura evoluc¸ ˜ao, deste agente permitir o uso de
guardrails de seguranc¸a para a aplicac¸ ˜ao, ou seja, que avalie
se a consulta ´e maliciosa ou perigosa antes de iniciar qualquer
processamento. O modelo utilizado para este agente foi o GPT
4o, da OpenAI.
A segunda etapa ´e escrever a consulta SQL, feita pelo agente
SQL Writer. Este agente utiliza uma LLM mais robusta, o
modelo o3-mini, da OpenAI, um dos mais capazes da gerac¸ ˜ao
atual das LLMs focadas em reasoning. A escolha do modelo
vem do fato de consultas possivelmente serem complexas e
necessitarem de maior capacidade de racioc´ınio. Este agente
possui 2 ferramentas: (1) ferramenta que lˆe quais s˜ao as tabelas
dispon´ıveis no banco e (2) uma ferramenta que acessa as
caracter´ısticas dos campos de uma tabela. Parte das decis˜oes
do agente envolve saber quais ferramentas utilizar para que
consiga concluir sua tarefa. Cada chamada ´e realizada em at´e
cinco tentativas, sendo a ´ultima a que corresponde `a consulta
SQL selecionada como melhor soluc¸ ˜ao.
Ap´os a gerac¸ ˜ao da consulta, o agente Optimizer ´e re-
spons´avel por garantir que a consulta gerada responda a per-
gunta inicial e re-ajusta a consulta gerada conforme necess´ario.
Ele foi pensado para permitir uma futura evoluc¸ ˜ao, de ser um
agente especializado em melhorar a qualidade de consultas
complexas que tenham maior sensibilidade a performance. Nos
nossos testes e exemplos, as consultas envolvem no m´aximo
4 tabelas, mas em um cen´ario real, esse valor pode ser muito
maior, envolver diferentes chaves, func¸ ˜oes, janelamento etc.
Por agora, seu papel ´e garantir uma consulta que seja de acordo
com o objetivo do usu´ario.
Por fim, ´e chamado o agente Auditor, que tem como
responsabilidade garantir que a consulta gerada ´e v´alida e
execut´avel. Ele checa o resultado da consulta do Optimizer
e garante que a consulta ´e execut´avel. Seu objetivo ´e remover
eventuais erros de identac¸ ˜ao, pontuac¸ ˜ao, entre outros. Um
exemplo de prompt pode ser encontrado no c´odigo 4.
Listing 1: Exemplo de prompt para SQL Writer
sql_writer:
role: >
SQL Data Analyst and Data Engineer
goal: >
Generate a SQL query for a given query written in
free text.
This is the user query: {query}
backstory: >
You are a skilled analyst with a background in
data manipulation
and data processing. You have a talent for
identifying patterns
and extracting meaningful insights from a free
form text and mapping
into a valid and executable SQL query.
You are aware that people need results that are
interpretable,
so you prefer to return textual results instead
of considering just ids for tables.
Fig. 4: Arquitetura da aplicac¸ ˜ao Mimir, desenvolvida para
estudo de caso
Para mais informac¸ ˜oes sobre os prompts, cheque o Apˆendice
VII-A
B. Testes
Os testes foram realizados com dois bancos de dados
pequenos, devido a limitac¸ ˜ao de recursos e ao n´umero alto
de chamadas de LLM causadas pela arquitetura multiagente.
O primeiro, Cooperagri, possui quatro tabelas relacionadas a
um circuito de produtores agr´ıcolas e restaurantes consumi-
dores de seus produtos (figura 5). O segundo, Alunos, possui
quatro tabelas relacionadas a matr´ıculas de alunos em cursos,
ministrados por professores (figura 6). Esses bancos foram
extra´ıdos de exemplos constru´ıdos para a disciplina MAC5861
– Modelagem de Banco de Dados (2025, 1º semestre). Foram
utilizadas 27 quest˜oes em linguagem natural extra´ıdas das
listas de exerc´ıcios da disciplina, e os gabaritos dos exerc´ıcios
em consultas SQL foram adotados como padr˜ao ouro (ground
truth).
Lei et al. [19] prop˜oem a mensurac¸ ˜ao da dificuldade de
uma tarefa text-to-SQL a partir do n´umero de espac¸os (tokens)
na consulta SQL do padr˜ao ouro. Utilizando essa m´etrica,
comparamos a dificuldade do padr˜ao ouro adotado neste artigo
`as dificuldades m´edias dos benchmarks Spider 1.0 e BIRD
(figura 7). Observa-se que o padr˜ao ouro adotado neste artigo
tem dificuldade baixa, pouco acima da m´edia do benchmark
Spider 1.0 e abaixo da dificuldade m´edia do benchmark BIRD.
O benchmark Spider 2.0 foi desenvolvido especificamente para
tarefas de alta dificuldade, adotando apenas consultas com
Fig. 5: Esquema do banco Cooperagri
Fig. 6: Esquema do banco Alunos
mais de 50 tokens. A m´edia de tokens na vers˜ao Spider 2.0-lite
´e 144,5, e 148,3 na vers˜ao completa.
Para avaliac¸ ˜ao dos resultados, formulamos m´etricas inspi-
radas nas metodologias do benchmark Spider 2.0-lite [19], e
de Katsogiannis-Meimarakis & Koutrika [13].
O benchmark Spider 2.0-lite possui c´odigos de avaliac¸ ˜ao
que consideram a acur´acia de execuc¸ ˜ao baseada na execuc¸ ˜ao,
ou seja, considera-se se todas as colunas das respostas do
padr˜ao ouro s˜ao preditas corretamente na resposta da consulta
formulada por LLM. Assim, reduz-se o n´umero de falsos
negativos sem incremento do n´umero de falsos positivos.
J´a Katsogiannis-Meimarakis & Koutrika apresentam
Fig. 7: Distribuic¸ ˜ao da dificuldade dos bancos Cooperagri e
Alunos por n´umero de tokens, em comparac¸ ˜ao `as m´edias dos
benchmarks BIRD e Spider 1.0
m´etricas para avaliac¸ ˜ao de aplicac¸ ˜oes text-to-SQL, que
podem ser agrupadas como avaliac¸ ˜ao da consulta SQL gerada
pela aplicac¸ ˜ao e avaliac¸ ˜ao dos resultados recuperados por
essa consulta.
A partir dessa literatura, constru´ımos duas m´etricas
sint´eticas:
1) Adequac¸ ˜ao da consulta SQL: valor booleano que avalia
se a consulta gerada corresponde ao padr˜ao ouro, ou
seja, se possui a estrutura l´ogica esperada e retorna todas
as colunas especificadas na cl´ausula SELECT do padr˜ao
ouro;
2) Adequac¸ ˜ao da resposta: valor booleano que avalia se
a resposta da consulta gerada corresponde `a resposta
gerada pela consulta de padr˜ao ouro, ou seja, se os
valores das colunas est˜ao corretos.
Al´em disso, a divis˜ao mais ampla do benchmark Spider 2.0
nas vers˜oes lite e completa cobre dois tipos de tarefa text-
to-SQL. A vers˜ao lite avalia o desempenho das LLMs para
gerac¸ ˜ao de consultas em SQL, tendo como dado de entrada
apenas o esquema do banco de dados. J´a a vers˜ao completa
avalia a gerac¸ ˜ao de uma resposta de texto complexa, que pode
conter o resultado de v´arias consultas. Para isso, permite-se
que a LLM acesse outros recursos para al´em do esquema,
como acesso ao pr´oprio banco de dados, a c´odigos auxiliares
e outros documentos (figura 8).
Fig. 8: Vers˜oes do Spider 2.0. Fonte: Lei et al. [19]
Partindo dessa divis˜ao, propomos quatro testes para cada
quest˜ao em linguagem natural:
1) Multiagente com acesso ao esquema e a ferramentas
adicionais
2) Multiagente com acesso apenas ao esquema
3) Agente simples com acesso ao esquema e a ferramentas
adicionais
4) Agente simples com acesso apenas ao esquema
Para calcular a pontuac¸ ˜ao de cada execuc¸ ˜ao a partir das
m´etricas propostas, realizamos uma avaliac¸ ˜ao por auditoria
manual e outra utilizando a abordagem “LLM-as-a-Judge”
[32], ou seja, a partir de uma nova chamada de LLM com
um prompt que compara as consultas em SQL e as respostas
ao padr˜ao ouro. Como modelo para LLM-as-a-Judge, foi uti-
lizado o GPT-3.5 Turbo, da OpenAI. As consultas e respostas
adequadas receberam a pontuac¸ ˜ao 1 e as incorretas receberam
a pontuac¸ ˜ao 0. Foram executadas 108 solicitac¸ ˜oes, com 486
chamadas a LLM, resultando em 16 pontuac¸ ˜oes. A figura 9
apresenta um diagrama simplificado da rotina de testes.
Fig. 9: Diagrama simplificado do fluxo de testes
V. RESULTADOS E DISCUSS ˜AO
As figuras 10, 11, 12 e 13 mostram a distribuic¸ ˜ao dos
resultados por dificuldade da tarefa e o percentual geral de
acertos (n´umero de quest˜oes com pontuac¸ ˜ao 1 em relac¸ ˜ao ao
total).
Fig. 10: Distribuic¸ ˜ao da avaliac¸ ˜ao das consultas em SQL por
auditoria manual, por dificuldade da tarefa
No geral, observamos que a arquitetura multiagentes possui
um desempenho pr´oximo `a arquitetura de agente simples
na auditoria manual. Dado que o custo de uma solicitac¸ ˜ao
em arquitetura multiagentes ´e multiplicado pelo n´umero de
agentes envolvidos, a arquitetura de agente simples mostra-
se mais vantajosa para a faixa de dificuldade analisada neste
artigo.
Fig. 11: Distribuic¸ ˜ao da avaliac¸ ˜ao das consultas em SQL por
auditor LLM, por dificuldade da tarefa
Fig. 12: Distribuic¸ ˜ao da avaliac¸ ˜ao das respostas por auditoria
manual, por dificuldade da tarefa
Fig. 13: Distribuic¸ ˜ao da avaliac¸ ˜ao das respostas por auditor
LLM, por dificuldade da tarefa
H´a uma diferenc¸a relevante entre a avaliac¸ ˜ao manual das
consultas SQL e das suas respostas. A partir da leitura das
consultas em SQL resultantes, identificamos que essa dis-
crepˆancia est´a relacionada majoritariamente ao uso de plural,
traduc¸ ˜ao do portuguˆes para o inglˆes e caracteres especiais.
Por exemplo, a quest˜ao “Liste os c´odigos dos agricultores que
j´a entregaram batatas, mas nunca entregaram cebolas” gera
consultas com cl´ausulas WHERE que filtram por entradas com
strings “cebolas” e “batatas” – palavras que s˜ao escritas no
singular nas entradas do banco de dados. Os demais casos
falharam ao traduzir cadeias de texto de filtros em portuguˆes
para inglˆes ou ao utilizar caracteres especiais nos r´otulos
das tabelas consultadas. Assim, a estrutura da consulta est´a
logicamente correta e retorna as colunas do padr˜ao ouro, mas
os valores da tabela da resposta n˜ao correspondem ao padr˜ao
ouro. Por conta disso, a m´etrica equivalente `a abordagem do
benchmark Spider 2.0 ´e a relativa `as respostas, por auditoria
manual.
Ao comparar os resultados da auditoria manual – adotada
como verdade base – ao auditor LLM, observamos que a
auditoria LLM gera um n´umero elevado de falsos negativos,
ou seja, aponta consultas e respostas corretas como incorretas.
O recall para a avaliac¸ ˜ao das consultas SQL ´e 56,8%, e
76,1% para as respostas, indicando que a comparac¸ ˜ao entre
consultas em SQL ´e uma tarefa mais dif´ıcil. Contudo, h´a uma
diferenc¸a relevante entre o desempenho do auditor LLM para
solicitac¸ ˜oes de multiagente contra as solicitac¸ ˜oes de agente
simples, com melhor desempenho para as consultas SQL
geradas por agente simples.
Por fim, observamos uma tendˆencia de gerac¸ ˜ao de consultas
em SQL mais longas (figura 14). Tamb´em observamos que
consultas geradas por LLM geram respostas com mais colunas
do que o necess´ario. Isso reforc¸a a abordagem de avaliac¸ ˜ao
baseada na execuc¸ ˜ao adotada pelo benchmark Spider 2.0 e
adaptada neste artigo como mais adequada, pois considera se
a resposta esperada est´a contida na resposta gerada e, com
isso, reduz o n´umero de falsos negativos.
Fig. 14: Distribuic¸ ˜ao do comprimento em n´umero de caracteres
das consultas SQL no padr˜ao ouro versus as consultas geradas
por LLM
VI. TRABALHOS FUTUROS
Uma avaliac¸ ˜ao mais definitiva sobre a vantagem da abor-
dagem multiagentes exigiria o emprego de quest˜oes mais
complexas e outros arranjos de pap´eis de agentes. Em trabal-
hos futuros, a aplicac¸ ˜ao implementada neste artigo deve ser
avaliada com benchmarks completos, como o Spider 2.0.
Al´em disso, a melhoria dos prompts, tanto das tasks quanto
dos agentes, utilizando t´ecnicas de prompt engineering [30],
[29], [31] potencialmente traria resultados melhores. Outro
melhoria direta seria uniformizar o uso dos modelos com
modelos de reasoning, como o o3-mini, j´a que estes possuem
maior capacidade de racioc´ınio e performam melhor nos
diferentes benchmarks de LLM. Outro caminho interessante
seria testar diferentes topologias para o sistema multiagentes,
como a topologia mesh, onde todos os agentes podem co-
municar entre si, ou a topologia hier´arquica, com um agente
coordenando os demais.
REFERENCES
[1] Y. Chang, X. Wang, J. Wang et al., “A survey on evaluation of large
language models,” ACM Trans. Intell. Syst. Technol., vol. 15, no. 3, pp.
1–45, 2024.
[2] M. Shanahan, K. McDonell, and L. Reynolds, “Role play with large
language models,” Nature, vol. 623, no. 7987, pp. 493–498, 2023.
[3] A. Vaswani, N. Shazeer, N. Parmar et al., “Attention is all you need,”
Adv. Neural Inf. Process. Syst., vol. 30, 2017.
[4] M. A. K. Raiaan, M. S. H. Mukta, K. Fatema et al., “A review on large
language models: Architectures, applications, taxonomies, open issues
and challenges,” IEEE Access, vol. 12, pp. 26839–26874, 2024.
[5] T. Kojima, S. S. Gu, M. Reid et al., “Large language models are zero-
shot reasoners,” in Adv. Neural Inf. Process. Syst., vol. 35, pp. 22199–
22213, 2022.
[6] P. Lewis, E. Perez, A. Piktus et al., “Retrieval-augmented generation for
knowledge-intensive NLP tasks,” in Adv. Neural Inf. Process. Syst., vol.
33, pp. 9459–9474, 2020.
[7] W. Fan, Y. Ding, L. Ning et al., “A survey on RAG meeting LLMs:
Towards retrieval-augmented large language models,” in Proc. 30th ACM
SIGKDD Conf. Knowl. Discov. Data Min., pp. 6491–6501, 2024.
[8] P. P. Ray, “ChatGPT: A comprehensive review on background, applica-
tions, key challenges, bias, ethics, limitations and future scope,” Internet
Things Cyber-Phys. Syst., vol. 3, pp. 121–154, 2023.
[9] Y. Du, S. Li, A. Torralba et al., “Improving factuality and reasoning in
language models through multiagent debate,” in Proc. 41st Int. Conf.
Mach. Learn. (ICML), 2023.
[10] Z. Xi, W. Chen, X. Guo et al., “The rise and potential of large language
model based agents: A survey,” Sci. China Inf. Sci., vol. 68, no. 2, pp.
121101, 2025.
[11] K. P. Sycara, “Multiagent systems,” AI Mag., vol. 19, no. 2, pp. 79,
1998.
[12] X. Li, S. Wang, S. Zeng et al., “A survey on LLM-based multi-agent
systems: Workflow, infrastructure, and challenges,” Vicinagearth, vol. 1,
no. 1, pp. 9, 2024.
[13] G. Katsogiannis-Meimarakis and G. Koutrika, “A survey on deep
learning approaches for text-to-SQL,” VLDB J., vol. 32, no. 4, pp. 905–
936, 2023.
[14] A. Wong, D. Joiner, C. Chiu et al., “A survey of natural language
processing implementation for data query systems,” in Proc. 2021 IEEE
Int. Conf. Recent Adv. Syst. Sci. Eng. (RASSE), pp. 1–8, 2021.
[15] A. B. Kanburo˘glu and F. B. Tek, “Text-to-SQL: A methodical review
of challenges and models,” Turk. J. Electr. Eng. Comput. Sci., vol. 32,
no. 3, pp. 403–419, 2024.
[16] G. Li, H. A. K. Hammoud, H. Itani et al., “CAMEL: Communicative
agents for ’mind’ exploration of large language model society,” in Proc.
37th Int. Conf. Neural Inf. Process. Syst. (NeurIPS), pp. 51991–52008,
2023.
[17] W. Chen, Y. Su, J. Zuo et al., “AgentVerse: Facilitating multi-agent
collaboration and exploring emergent behaviors,” in Proc. 12th Int. Conf.
Learn. Represent. (ICLR), 2024.
[18] T. Yu, R. Zhang, K. Yang et al., “Spider: A large-scale human-labeled
dataset for complex and cross-domain semantic parsing and text-to-SQL
task,” arXiv preprint arXiv:1809.08887, 2018.
[19] Lei, F., Chen, J., Ye, Y., Cao, R., Shin, D., Su, H.,et al., “Spider
2.0: Evaluating language models on real-world enterprise text-to-sql
workflows”, arXiv preprint arXiv:2411.07763, 2024.
[20] V. Zhong, C. Xiong, and R. Socher, “Seq2SQL: Generating structured
queries from natural language using reinforcement learning,” arXiv
preprint arXiv:1709.00103, 2017.
[21] J. Guo, Z. Zhan, Y. Gao et al., “Towards complex text-to-SQL in
cross-domain database with intermediate representation,” arXiv preprint
arXiv:1905.08205, 2019.
[22] N. Yaghmazadeh, Y. Wang, I. Dillig et al., “SQLizer: Query synthesis
from natural language,” Proc. ACM Program. Lang., vol. 1, no. OOP-
SLA, pp. 1–26, 2017.
[23] B. Wang, R. Shin, X. Liu et al., “RAT-SQL: Relation-aware schema
encoding and linking for text-to-SQL parsers,” in Proc. 58th Annu.
Meeting Assoc. Comput. Linguist. (ACL), pp. 7567–7578, 2020.
[24] Y. Luo, X. Lin, W. Wang, and X. Zhou, “SPARK: Top-k keyword query
in relational databases,” in Proc. 2007 ACM SIGMOD Int. Conf. Manag.
Data, pp. 115–126, 2007.
[25] F. Li and H. V. Jagadish, “Constructing an interactive natural language
interface for relational databases,” Proc. VLDB Endow., vol. 8, no. 1,
pp. 73–84, 2014.
[26] S. Iyer, I. Konstas, A. Cheung et al., “Learning a neural semantic parser
from user feedback,” arXiv preprint arXiv:1704.08760, 2017.
[27] V. Hristidis and Y. Papakonstantinou, “DISCOVER: Keyword search
in relational databases,” in Proc. 28th Int. Conf. Very Large Databases
(VLDB), pp. 670–681, 2002.
[28] V. Hristidis, Y. Papakonstantinou, and L. Gravano, “Efficient IR-style
keyword search over relational databases,” in Proc. 2003 Int. Conf. Very
Large Databases (VLDB), pp. 850–861, 2003.
[29] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian
Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. Chain-
of-thought prompting elicits reasoning in large language models. In
Proceedings of the 36th International Conference on Neural Information
Processing Systems (NeurIPS 2022), pages 1800–1813. Curran Asso-
ciates Inc., Red Hook, NY, USA, 2022.
[30] Tom B. Brown, Benjamin Mann, Nick Ryder, et al. Language models are
few-shot learners. In Proceedings of the 34th International Conference
on Neural Information Processing Systems (NeurIPS 2020), pages 159–
183. Curran Associates Inc., Red Hook, NY, USA, 2020.
[31] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan,
and Shunyu Yao. Reflexion: Language agents with verbal reinforcement
learning. In Proceedings of the 37th International Conference on Neural
Information Processing Systems (NeurIPS 2023), pages 377–395. Curran
Associates Inc., Red Hook, NY, USA, 2023.
[32] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, et al. Judging LLM-as-
a-judge with MT-bench and Chatbot Arena. In Proceedings of the 37th
International Conference on Neural Information Processing Systems
(NeurIPS 2023), pages 2020–2048. Curran Associates Inc., Red Hook,
NY, USA, 2023.
[33] Jinyang Li, Binyuan Hui, Ge Qu, et al. Can LLM already serve as
a database interface? A big bench for large-scale database grounded
text-to-SQLs. Advances in Neural Information Processing Systems, 36,
2024.
[34] Shunyu Yao, Jeffrey Zhao, Dian Yu, et al. ReAct: Synergiz-
ing Reasoning and Acting in Language Models. arXiv preprint
arXiv:2210.03629, 2023.
[35] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever. Im-
proving Language Understanding by Generative Pre-Training. OpenAI
Research, 2018. URL
VII. AP ˆENDICE
A. Prompts
Prompts utilizados nos agentes:
Listing 2: Exemplo de prompt para Rewriter
rewriter:
role: >
Rewrite and validate human user input text for {
query}
goal: >
Rewrite a human user input text into a meaningful
equivalent
text removing any non-essential information and
ensuring the
text is clear, concise and respectful.
backstory: >
You are an experienced analyzer and rewriter with
a talent for
rewriting text that maintains content but it is
more clear.
You excel at organizing information in a clear
and concise manner,
making a text more readable and appropriate.
Listing 3: Exemplo de prompt para Optimizer
optimizer:
role: >
SQL Data Analyst that verifies the quality of a
SQL query
goal: >
Verify if SQL query provided solves the problem
described in the provided
question. If not, correct the query.
backstory: >
You are a skilled analyst with a background in
data interpretation
and SQL queries. You are aware that people need
results that are interpretable,
so you prefer to return textual results instead
of considering just ids for tables.
You have a talent for identifying patterns and
making sure the SQL solves the problem
described in the provided question.
Listing 4: Exemplo de prompt para Auditor
auditor:
role: >
Audits SQL query
goal: >
Make sure a SQL query is valid and executable
backstory: >
You are a skilled analyst with a background in
data interpretation
and SQL. You are knowledgeable on SQL and
databases.
Os demais prompts utilizados podem ser encontrados na
URL: Github repo
B. Dados
Os dados utilizados para criac¸ ˜ao e testes se encontram na
URL: Github repo