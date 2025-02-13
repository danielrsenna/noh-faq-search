import reflex as rx
import datetime
import os
from dotenv import load_dotenv
from .supabase_client import supabase_client
import logging
import pandas as pd

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DashboardState(rx.State):
    total_searches: int = 0
    searches_by_hour: dict = {}
    top_articles_df: pd.DataFrame = pd.DataFrame(columns=["Título do Artigo", "Pontuação Ponderada"])
    is_loading: bool = False

    def load_all_data(self):
        """Método para carregar todas as métricas relevantes do dashboard."""
        self.is_loading = True
        yield  # Atualiza a interface enquanto carrega os dados

        # Chamando os métodos individuais para cada métrica
        self.load_total_searches()
        self.load_searches_by_hour()
        self.load_top_articles()
        # self.load_avg_response_time() -> Também depois

        self.is_loading = False

    def load_total_searches(self):
        """Consulta o número total de pesquisas no Supabase."""
        response = supabase_client().table("search_log").select("search_id", count="exact").execute()
        if response.count:
            self.total_searches = response.count
        else:
            self.total_searches = 0

    def load_searches_by_hour(self):
        """Agrupa o número de pesquisas por hora no Supabase."""
        response = supabase_client().table("search_log").select("search_at").execute()
        if response.data:
            hourly_count = {}
            for entry in response.data:
                search_time = datetime.datetime.fromisoformat(entry["search_at"].replace("Z", "+00:00"))
                hour = search_time.strftime("%Y-%m-%d %H:00")
                hourly_count[hour] = hourly_count.get(hour, 0) + 1
            self.searches_by_hour = hourly_count
        else:
            self.searches_by_hour = {}

    def load_top_articles(self):
        """Agrupa e calcula os top 5 artigos mais retornados de forma ponderada e cria um DataFrame."""
        response = supabase_client().table("search_log").select("embeddings_results").execute()
        if response.data:
            article_scores = {}
            for entry in response.data:
                embeddings = entry["embeddings_results"]
                for idx, artigo in enumerate(embeddings):
                    titulo = artigo["titulo_artigo"]
                    score = 5 - idx  # Peso decrescente (1º = 5 pontos, 2º = 4, ..., 5º = 1)
                    article_scores[titulo] = article_scores.get(titulo, 0) + score

            # Ordenar, pegar os 5 artigos com maior pontuação e criar o DataFrame
            sorted_articles = sorted(article_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            self.top_articles_df = pd.DataFrame(sorted_articles, columns=["Título do Artigo", "Pontuação Ponderada"])