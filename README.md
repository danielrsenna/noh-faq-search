# noh-faq-search

Contexto:

Descobri a Noh no Linkedin por acaso (tenho usado muito LinkedIn já que estou procurando emprego). Olhei o linkedin do CTO e ele me pareceu um cara peculiar, o que acho incrível, também vi que é uma empresa com mulheres na liderança, o que também acho muito positivo. Então resolvi checar se haviam vagas abertas.

Vi que o processo seletivo da Noh é "inverso" (você aponta um problema deles e diz como solucionaria e porque você é a pessoa certa para resolver). Como não conheço o produto, fui ao site para ganhar mais contexto e entendimento do negócio/produto.

Fuçando o site notei uma "dor" na parte de "Ajuda". A central de ajuda é dividida em 6 categorias, o usário clica na categoria desejada e isso o leva para outra página específica. Uma vez na outra página, haverá uma lista de artigos daquela categoria - são 78 artigos no total, divididos entre as 6 categorias. 

O usuário então clica no artigo e isso o direciona para a sua respectiva página contendo Título (a Pergunta), conteúdo (a Resposta) e links para artigos relacionados. Ou seja, o cliente precisa, sozinho, se direcionar até encontrar o artigo (ou os artigos) que vá sanar sua dúvida, precisa desbravar dentre os possíveis caminhos, por tentativa e erro, até achar a resposta. 

Em nenhum momento há um campo de busca digitável que, uma vez feita a busca, retorna os artigos mais relacionados ou, até mesmo, uma resposta gerada com IA. Resolvi então ajudar nisso, talvez não seja um problema crítico para a Noh, mas a estrutura por trás dessa solução pode ser aplicada em outros problemas que envolvam IA Generativa + RAG. 

1ª Etapa Web Scraping:
Obtenção dos dados:
Coletar, com web scraping, os artigos da área de Ajuda da Noh, esses servirão para a construção da nossa base de conhecimento (feita com embeddings em um Vector Database).

2ª Etapa Embeddings (RAG)
Obter os artigos mais relevantes com base em uma pesquisa:
Gerar os embeddings dos artigos coletados na etapa 1 e salvar os vetores em um database próprio para isso. Testar queries para retornar os vetores mais próximos. 

3ª Etapa Respostas com IA Generativa
Obter respostas "naturais" com IA.
Uma vez que temos os artigos mais relevantes para a pergunta (etapa 2), podemos fornecê-los como contexto para um modelo de IA que responderá a pergunta do usuário com base nos artigos. 

4ª Etapa Reflex
Desenvolver um web app simples que simule a página de ajuda da Noh (design similar), onde o usuário poderá digitar sua dúvida e obter os artigos mais relevantes, bem como uma resposta gerada por IA.

5ª Etapa Reflex Plus:
Quero conectar isso em uma base de dados para possibilitar informação de artigos mais acessados (uma FAQ de fato). Também, com isso, possibilitar testar versões diferentes de soluções para a busca (estilo experimentação, teste A/B), por exemplo testando modelos de embeddings diferentes.

Futuro:
Como essa solução é um protótipo, usei ferramentas mais conhecidas e fáceis de implementar. Porém poderíamos explorar algumas melhorias, como:
- Outras opções de Vector Database, além do Pinecone;
- Outros modelos de embeddings e de chat completion, além da OpenAI;
- Outras estratégias para rankear os artigos mais relevantes, adicionando modelos reranking ou usando diferentes métricas de similaridade (ao invés da cosine).
- Outros modelos e databases locais/open source, sem depender de APIs pagas;
- Melhorar o tempo de carregamento da busca;
- Conferir se as respostas geras por IA são confiáveis;
- Qual o custo atrelado ao uso de IA Generativa para essa busca, bem como num futuro com base em aumento de número de clientes (e consequentemente buscas no Ajuda)


