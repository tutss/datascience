-- Exercícios 3 
﻿
-- a) Liste os nomes dos restaurantes que ficam em Santo André.

select NomeR from Restaurante where CidadeR = 'Santo André';

-- b) Liste todas as informações dos produtos cujo nome começa com a letra “c”  e cujo preço por quilo é inferior a R$3,00.
select * from Produto where (NomeP like 'c%' or NomeP like 'C%') and PrecoQuilo < 3;

-- c) Liste os códigos dos agricultores que já entregaram produtos para o restaurante RU-USP.
select CodA from Entrega natural join Restaurante where NomeR = 'RU-USP';

-- d) Liste os nomes dos produtos que já foram alguma vez entregues por um agricultor de Mogi das Cruzes.
select distinct NomeP from Entrega natural join Produto natural join Agricultor where CidadeA = 'Mogi das Cruzes';

-- e) Liste os códigos dos agricultores que já entregaram batatas e também já entregaram cebolas.

(select CodA from Entrega natural join Produto where NomeP = 'batata')
intersect
(select CodA from Entrega natural join Produto where NomeP = 'cebola');

-- f) Liste os códigos dos agricultores que já entregaram batatas, mas nunca entregaram cebolas.
(select CodA from Entrega natural join Produto where NomeP = 'batata')
except
(select CodA from Entrega natural join Produto where NomeP = 'cebola');

-- g) Liste todas as triplas (código do agricultor, código do produto, código do restaurante) extraídas de Entrega tais que o agricultor e o restaurante estejam na mesma cidade.

select CodA, CodP, codR from Entrega natural join Agricultor natural join Restaurante where CidadeA = CidadeR;

-- h) Obtenha o número total de restaurantes já supridos pelo agricultor de nome “Machado de Assis”.

select count(distinct CodR) from Entrega natural join Agricultor where NomeA = 'Machado de Assis';

-- i) Liste os nomes das cidades onde ao menos um agricultor ou um restaurante esteja localizado.

(select CidadeA from Agricultor)
union
(select CidadeR from Restaurante);

-- j) Obtenha o número de produtos que são fornecidos ou por um agricultor de São Paulo ou para um restaurante em São Paulo.

select count(distinct CodP) from Entrega where CodA in (select CodA from Agricultor where CidadeA = 'São Paulo') or CodR in (select codR from Restaurante where CidadeR = 'São Paulo');

-- k) Obtenha pares do tipo (código do agricultor, código do produto) tais que o agricultor indicado nunca tenha fornecido o produto indicado.

select distinct CodA, CodP from Agricultor as A, Produto where CodP not in (select CodP from Entrega where CodA = A.CodA);

-- l) Obtenha os códigos dos produtos e suas respectivas quantidades médias por entrega  para os produtos que são fornecidos em uma quantidade média por entrega superior a 30 quilos.

select codP from Entrega group by codP having avg(QtdeQuilos) > 30;

-- m) Obtenha o(s) nome(s) dos produtos mais fornecidos a restaurantes (ou seja, os produtos dos quais as somas das quantidades já entregues é a maior possível). 

select NomeP from Entrega natural join Produto group by NomeP having sum(QtdeQuilos) >= ALL (select sum(QtdeQuilos) from Entrega group by CodP);
-- ou
select NomeP from Entrega natural join Produto group by NomeP having sum(QtdeQuilos) = (select max(total) from (select sum(QtdeQuilos) as total from Entrega group by CodP) as T);

-- n) Obtenha o nome do(s) agricultor(es) que fez(fizeram) a entrega de produtos mais antiga registrada no BD.

select NomeA from Entrega natural join Agricultor where DataEntrega = (select min(DataEntrega) from Entrega);

-- o) Liste os nomes dos produtos que são oferecidos a todos os restaurantes do BD. Ou seja, um produto não deve aparecer na lista se houver um restaurante que nunca o tenha recebido.

select NomeP from Produto as P where not exists (
	(select CodR from Restaurante)
	except
	(select CodR from Entrega where CodP = P.CodP));

-- p) Liste todos os pares possíveis do tipo (i,j) tal que i é o nome de um agricultor, j é o nome de um restaurante e i já entregou um produto para j. Mas atenção: o nome de todos os agricultores cadastrados no BD deve aparecer no conjunto resposta. Se um agricultor nunca fez uma entrega, então o seu nome deve vir acompanhado de NULL no conjunto resposta. 

select NomeA, NomeR from (Entrega natural join Restaurante) natural right outer join Agricultor;

