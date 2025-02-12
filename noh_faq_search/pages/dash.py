import reflex as rx

from ..ui import footer


def upper_area() -> rx.Component:
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

def center_area() -> rx.Component:
    return rx.flex(
        rx.text("Dashboard"), 
        rx.text("Gráfico #Pesquisas por dia"), 
        rx.text("Tabela de Artigos mais retornados nas pesquisas"),
        rx.text("Tempo Médio Embeddings"),
        rx.text("Tempo Médio Resposta IA"),  
        rx.text("Feedbacks Positivos x Negativos"), 
        justify="start", 
        direction="column",
        background_color="#ffffff",
        padding_top="2em",
        width="50%",
        height="80vh",
        padding_bottom="2em",
        align="center",
    )

def dash() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        upper_area(),
        center_area(),
        footer(),
        direction="column",
        #background_color="#ffffff",
        align="center",
    )