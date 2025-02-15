import reflex as rx
import pandas as pd

import plotly.express as px

from ..ui import footer
from .dash_state import DashboardState


def dash() -> rx.Component:
    return rx.flex(
        navbar(),
        main(),
        footer(),
        direction="column",
        align="center",
    )

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex( 
            rx.link( 
                rx.text(
                    "Ajuda",
                    font_size="1em",
                    font_weight=400,
                    font_family= "sans-serif",
                    color="#222222",  
                ),
                href="/",
                is_external=False,
            ),
        ),
        rx.flex( 
            rx.text(
                "ATENÇÃO: ESSE NÃO É O SITE OFICIAL DA NOH!!!",
                font_size="1em",
                font_weight=400,
                font_family= "sans-serif",
                color="red",  
            ),
        ),
        justify="between",
        align="center",
        padding_top="1em", 
        padding_bottom="1em",
        padding_left="20em", 
        padding_right="20em", 
        width="100%",
        height="3em",
        background_color="#ebeae9",
    )

def main() -> rx.Component:
    return rx.flex(
        rx.text("Dashboard - Estatísticas de Busca", font_size="16px", font_weight="bold"),
        rx.text("Bem toscão/simples, só pra ilustrar o que poderíamos fazer com os dados que estão sendo salvos no Supabase", font_size="10px", font_weight="semibold"),
        total_searches_component(),
        rx.flex(
            minutes_searches_chart(),
            response_time_boxplot(),
            direction="row",
            justify="between",
            width="100%",
        ),
        rx.flex(
            rx.text("Top 5 Artigos Mais Recorrentes", font_size="16px", font_weight="bold"),
            top_articles_table(),
            #width="100%",
            direction="column",
            justify="start",
            spacing="1",
        ),
        rx.flex(
            rx.text("Experimentação - Teste A/B", font_size="16px", font_weight="bold"),
            rx.text("Influência do uso de Modelos de Embeddings (Small x Large) na qualidade da Resposta ao Usuário", font_size="14px"),
            rx.flex(
                ab_testing_bar_chart(),
                ab_testing_line_chart(),
                justify="between",
                width="100%",
            ),
            width="100%",
            direction="column",
            justify="start",
            spacing="1",
        ),
        justify="start", 
        direction="column",
        background_color="#ffffff",
        padding_top="1em",
        width="90%",
        #height="80vh",
        padding_bottom="2em",
        align="start",
        spacing="1"
    )

def total_searches_component() -> rx.Component:
    """Componente para exibir o número total de pesquisas."""
    return rx.card(
        rx.text(f"Número Total de Pesquisas: {DashboardState.total_searches}", font_size="16px"),
        padding="1em",
        background_color="#f5f5f5",
        border_radius="5px",
        #width="30%",
    )

def top_articles_table() -> rx.Component:
    return rx.data_table(
            data=DashboardState.top_articles_df,
            pagination=False,
            search=False,
            sort=False,
        )

def minutes_searches_chart() -> rx.Component:
    return rx.center(
        rx.plotly(data=DashboardState.searches_by_min_fig),
    )

def response_time_boxplot() -> rx.Component:
    return rx.center(
        rx.plotly(data=DashboardState.response_time_fig),
    )

def ab_testing_bar_chart() -> rx.Component:
    return rx.center(
        rx.plotly(data=DashboardState.ab_testing_bar_fig),
    )

def ab_testing_line_chart() -> rx.Component:
    return rx.center(
        rx.plotly(data=DashboardState.ab_testing_line_fig),
    )