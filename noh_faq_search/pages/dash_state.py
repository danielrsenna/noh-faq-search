import reflex as rx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os
from dotenv import load_dotenv
from .supabase_client import supabase_client
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DashboardState(rx.State):
    is_loading: bool = False
    search_logs: list[dict] = []  
    total_searches: int = 0
    top_articles_df: pd.DataFrame = pd.DataFrame()
    searches_by_min_fig: go.Figure = go.Figure()
    ab_testing_bar_fig: go.Figure = go.Figure()
    ab_testing_line_fig: go.Figure = go.Figure()
    response_time_fig: go.Figure = go.Figure()
    

    def load_all_data(self):
        """Carrega todos os dados do Supabase e gera DataFrames necessários."""
        self.is_loading = True
        yield

        try:
            response = supabase_client().table("search_log").select("*").execute()
            if response.data:
                self.search_logs = response.data
                self.total_searches = len(self.search_logs)
                self.gen_searches_by_min()
                self.generate_top_articles()
                self.generate_response_time_fig()
                self.generate_ab_bar_fig()
                self.generate_ab_line_fig()
                logging.info(f"Dados carregados: {self.total_searches} registros.")
            else:
                self.search_logs = []
                logging.warning("Nenhum dado encontrado no Supabase.")
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            self.search_logs = []
        finally:
            self.is_loading = False

    def gen_searches_by_min(self):
        df = pd.DataFrame(self.search_logs)
        df["search_at"] = pd.to_datetime(df["search_at"])
        searches_by_hour = df.groupby(df["search_at"].dt.strftime("%Y-%m-%d %H:%M:00")).size().reset_index(name="pesquisas")
        searches_by_hour.rename(columns={"search_at": "minuto"}, inplace=True)
        fig = px.line(
            searches_by_hour, 
            x="minuto", 
            y="pesquisas",
            title="Buscas por Minuto",)
        self.searches_by_min_fig = fig
    
    def generate_top_articles(self):
        df = pd.DataFrame(self.search_logs)
        articles_df = pd.json_normalize(df["embeddings_results"].explode())
        top_articles = (
            articles_df.groupby(["titulo_artigo","url_artigo"])
            .size()
            .reset_index(name="Número de Ocorrências")
            .sort_values(by="Número de Ocorrências", ascending=False)
            .head(5)
        )
        self.top_articles_df = top_articles

    def generate_response_time_fig(self):
        df = pd.DataFrame(self.search_logs)
        df["search_at"] = pd.to_datetime(df["search_at"])
        df["ia_response_at"] = pd.to_datetime(df["ia_response_at"])
        df["tempo_resposta"] = (df["ia_response_at"] - df["search_at"]).dt.total_seconds()
        df["modelo"] = pd.json_normalize(df["model_used"])["embeddings"]
        response_time_df = df[["tempo_resposta", "modelo"]]
        fig = px.box(
            response_time_df,
            x="modelo",
            y="tempo_resposta",
            title="Tempo de Resposta por Modelo (s)",
        )
        self.response_time_fig = fig

    def generate_ab_bar_fig(self):
        df = pd.DataFrame(self.search_logs)
        df["modelo"] = pd.json_normalize(df["model_used"])["embeddings"]
        feedback_df = df[df["result_helpful"].notnull()]
        feedback_rate_df = feedback_df.groupby("modelo")["result_helpful"].mean().reset_index()
        feedback_rate_df["feedback_rate"] = feedback_rate_df["result_helpful"] * 100
        fig = px.bar(
            feedback_rate_df,
            x="modelo",
            y="feedback_rate",
            text="feedback_rate",
            title="Taxa de Feedback Positivo por Modelo (%)",
            labels={"feedback_rate": "Taxa de Feedback (%)", "modelo": "Modelo de Embeddings"},
            color="modelo",
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside')
        fig.update_layout(yaxis=dict(tickformat=".0f"), showlegend=False)
        self.ab_testing_bar_fig = fig

    def generate_ab_line_fig(self):
        df = pd.DataFrame(self.search_logs)
        df["modelo"] = pd.json_normalize(df["model_used"])["embeddings"]
        df["search_at"] = pd.to_datetime(df["search_at"])
        feedback_df = df[df["result_helpful"].notnull()]
        feedback_df["hour"] = feedback_df["search_at"].dt.floor("h")
        feedback_trend_df = feedback_df.groupby(["hour", "modelo"])["result_helpful"].mean().reset_index()
        feedback_trend_df["feedback_rate"] = feedback_trend_df["result_helpful"] * 100 
        fig = px.line(
            feedback_trend_df,
            x="hour",
            y="feedback_rate",
            color="modelo",
            title="Evolução da Taxa de Feedback Positivo por Hora (%)",
            labels={"feedback_rate": "Taxa de Feedback Positivo (%)", "hour": "Hora", "modelo": "Modelo de Embeddings"},
        )
        fig.update_layout(yaxis=dict(tickformat=".0f"), hovermode="x unified", xaxis_tickformat="%H:%M")
        self.ab_testing_line_fig = fig


    


    




