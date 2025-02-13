import reflex as rx
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from .supabase_client import supabase_client
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DashboardState(rx.State):
    search_logs: list[dict] = []  # Dados brutos de busca
    total_searches: int = 0
    top_articles_df: pd.DataFrame = pd.DataFrame()  # DataFrame para top artigos
    searches_by_hour_df: list[dict] = []  # DataFrame para pesquisas por hora
    is_loading: bool = False

    def load_all_data(self):
        """Carrega todos os dados do Supabase e gera DataFrames necessários."""
        self.is_loading = True
        yield

        try:
            response = supabase_client().table("search_log").select("*").execute()
            if response.data:
                self.search_logs = response.data
                self.total_searches = len(self.search_logs)
                self.gen_searches_by_hour_df()
                logging.info(f"Dados carregados: {self.total_searches} registros.")
            else:
                self.search_logs = []
                logging.warning("Nenhum dado encontrado no Supabase.")
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            self.search_logs = []
        finally:
            self.is_loading = False

    def gen_searches_by_hour_df(self):
        df = pd.DataFrame(self.search_logs)
        df["search_at"] = pd.to_datetime(df["search_at"])
        searches_by_hour = df.groupby(df["search_at"].dt.strftime("%Y-%m-%d %H:00")).size().reset_index(name="pesquisas")
        searches_by_hour.rename(columns={"search_at": "hora"}, inplace=True)
        self.searches_by_hour_df = searches_by_hour.to_dict('records')
        
