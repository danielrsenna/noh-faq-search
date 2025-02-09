import reflex as rx
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_large = pc.Index("noh-faq-index-3072")
embeddings_large = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store_large = PineconeVectorStore(index=index_large, embedding=embeddings_large)

class ArtigoMetadata(rx.Base):
    titulo_artigo: str
    titulo_categoria: str
    url_artigo: str

class SearchState(rx.State):
    user_question: str = ""
    contexto_rag: str = ""
    response: str = ""
    search_results_metadata: list[ArtigoMetadata] = []
    is_loading: bool = False

    def reset_state(self):
        self.user_question = ""
        self.contexto_rag = ""
        self.response = ""
        self.search_results_metadata = []
        
    def set_user_question(self, value: str):
        self.user_question = value

    def query_pinecone(self):
        #self.is_loading = True
        print(f"[query_pinecone] Iniciando busca para: {self.user_question}")
        results_large = vector_store_large.similarity_search_with_score(self.user_question, k=5)
        print(f"[query_pinecone] Resultados encontrados: {len(results_large)}")
        artigos_metadata = []

        if not results_large:
            self.contexto_rag = "Não foi possível encontrar artigos relacionados à sua pergunta."
            print("[query_pinecone] Nenhum resultado relevante.")
            return

        contexto = ""
        for i in results_large:
            titulo = i[0].metadata["titulo_artigo"]
            conteudo = i[0].metadata["conteudo_artigo"]
            url = i[0].metadata["url_artigo"]
            categoria = i[0].metadata["titulo_categoria"]

            contexto += f"Título do Artigo: {titulo}\nConteúdo: {conteudo}\n\n"
            artigos_metadata.append(ArtigoMetadata(titulo_artigo=titulo, titulo_categoria=categoria, url_artigo=url))
        
        self.contexto_rag = contexto
        self.search_results_metadata = artigos_metadata
        print(f"[query_pinecone] Metadados coletados: {self.search_results_metadata}")

    def generate_response(self):
        #self.is_loading = True
        if not self.contexto_rag or self.contexto_rag == "Não foi possível encontrar artigos relacionados à sua pergunta.":
            self.response = "Desculpe, não consegui encontrar informações suficientes para responder sua pergunta."
            return
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.6,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        system_template = """TAREFA:
            Você é um assistente para pergunta-resposta (Q&A), seu papel é responder dúvidas de visitantes no website da Noh. A Noh é um banco digital que oferece conta financeira para apenas para casais.
            Como contexto, serão fornecidos 3 artigos da central de ajuda da Noh obtidos via embeddings (RAG), ou seja, serão fornecidos os 3 artigos mais similares à pergunta do usuário. 
            INSTRUÇÕES:
            Responda EXCLUSIVAMENTE com base nos artigos fornecidos como contexto, NÃO invente informações sobre a conta Noh. Se você achar que os conteúdos dos artigos fornecidos não são suficientes para responder a pergunta do usuário, apenas diga que não é capaz de responder no momento. 
            Responda em língua portuguesa. 
            Responda com o mesmo tom de voz dos artigos fornecidos como contexto.
            Responda de forma concisa e termine com "para mais informações, consulte os artigos abaixo".

            Artigos da Central de Ajuda:\n{contexto}"""

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{user_question}")]
        )

        prompt = prompt_template.invoke({"contexto": self.contexto_rag, "user_question": self.user_question})
        response = llm.invoke(prompt)
        self.response = response.content
    
    def handle_search(self):
        print(f"[handle_search] Pergunta recebida: {self.user_question}")
        self.is_loading = True
        yield
        self.response = ""
        self.search_results_metadata = []
        try:
            self.query_pinecone()
            print(f"[handle_search] Resultados da busca: {self.search_results_metadata}")
            self.generate_response()
            print(f"[handle_search] Resposta gerada: {self.response}")
        finally:
            self.is_loading = False

