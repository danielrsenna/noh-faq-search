import reflex as rx
import pandas as pd

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
        rx.text("Dashboard - Estatísticas de Busca", font_size="2em", padding="1em"),
        total_searches_component(),
        hourly_searches_chart(),
        #top_articles_table(),
        rx.text("Tempo Médio Embeddings"),
        rx.text("Tempo Médio Resposta IA"),  
        rx.text("Feedbacks Positivos x Negativos"), 
        justify="start", 
        direction="column",
        background_color="#ffffff",
        padding_top="2em",
        width="90%",
        height="80vh",
        padding_bottom="2em",
        align="start",
        spacing="2"
    )

def total_searches_component() -> rx.Component:
    """Componente para exibir o número total de pesquisas."""
    return rx.card(
        rx.text("Número Total de Pesquisas", font_size="1.5em"),
        rx.text(f"{DashboardState.total_searches}", font_size="2em", font_weight="bold"),
        padding="1em",
        background_color="#f5f5f5",
        border_radius="10px",
        width="30%",
    )

# def top_articles_table() -> rx.Component:
#     return rx.data_table(
#             data=DashboardState.top_articles_df,
#             pagination=False,
#             search=False,
#             sort=True,
#             width="100%",
#         )

def hourly_searches_chart() -> rx.Component:
    """Componente para exibir o gráfico de pesquisas por hora usando rx.cond."""
    return rx.recharts.line_chart(
            rx.recharts.line(data_key="pesquisas", name="Pesquisas", stroke="#8884d8"),
            rx.recharts.x_axis(data_key="hora", name="Hora"),
            rx.recharts.y_axis(name="Número de Pesquisas"),
            rx.recharts.graphing_tooltip(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=DashboardState.searches_by_hour_df,
            width="50%",
            height=300,
        )