import reflex as rx
import datetime
import uuid
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

import supabase
from supabase import create_client

def supabase_client():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não estão configuradas.")
    
    client = create_client(supabase_url, supabase_key)
    return client

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
    search_id = str
    result_helpful: bool = None
    feedback_given: str = None

    def reset_state(self):
        self.user_question = ""
        self.contexto_rag = ""
        self.response = ""
        self.search_results_metadata = []
        yield
        
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
        self.search_id = str(uuid.uuid4())  # Gera um search_id único
        search_start_time = datetime.datetime.utcnow()  # Horário de início da busca
        yield
        self.response = ""
        self.search_results_metadata = []

        try:
            self.query_pinecone()
            embeddings_results_time = datetime.datetime.utcnow()  # Após obter resultados dos embeddings
            print(f"[handle_search] Resultados da busca: {self.search_results_metadata}")
            self.generate_response()
            ia_response_time = datetime.datetime.utcnow()  # Após resposta da IA
            print(f"[handle_search] Resposta gerada: {self.response}")
            self.insert_log(search_start_time, embeddings_results_time, ia_response_time)
        finally:
            self.is_loading = False
    
    def set_feedback(self, value: str):
        """Define o feedback ('up' ou 'down') e altera o estado visual."""
        self.feedback_given = value
        print(f"Feedback recebido: {self.feedback_given}")
        yield  # Força a atualização visual.

    def is_feedback_selected(self, value: str) -> bool:
        """Verifica se o feedback atual corresponde ao valor passado ('up' ou 'down')."""
        return self.feedback_given == value
    
    def send_feedback(self):
        client = supabase_client()
        if self.search_id:
            try:
                response = client.table("search_log").update({"result_helpful": self.result_helpful}).eq("search_id", self.search_id).execute()
                print(f"Feedback enviado com sucesso! Response: {response.data}")
            except Exception as e:
                print(f"Erro ao enviar feedback: {e}")
        else:
            print("Nenhum search_id encontrado para enviar o feedback.")

    def insert_log(self, search_start_time, embeddings_results_time, ia_response_time):
        """Insere a busca e o resultado no Supabase."""
        client = supabase_client()
        log_data = {
            "search_id": self.search_id,
            "user_question": self.user_question,
            "embeddings_results": [  # Lista de dicionários com título e URL
                {#preciso adicionar o id do vetor e também o score da consulta <--------
                    "titulo_artigo": artigo.titulo_artigo,
                    "url_artigo": artigo.url_artigo
                }
                for artigo in self.search_results_metadata
            ],
            "ia_answer": self.response,
            "search_at": search_start_time,
            "embeddings_results_at": embeddings_results_time,
            "ia_response_at": ia_response_time,
            "model_used": "gpt-4o-mini"  # Ou outro modelo usado
        }
        try:
            response = client.table("search_log").insert(log_data).execute()
            print(f"Log inserido com sucesso! Response: {response.data}")
        except Exception as e:
            print(f"Erro ao inserir log no Supabase: {e}")

