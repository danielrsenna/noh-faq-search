import reflex as rx

from ..ui import footer
from .state import SearchState

def answer() -> rx.Component:
    return rx.cond(
        SearchState.is_loading,
        rx.flex(
            rx.spinner(size="3"),
            justify="center",
            align="center",
            padding="2em"
        ),
        rx.cond(
            SearchState.response,  
            rx.flex(
                rx.flex(
                    rx.button(
                        "Limpar Resultados",
                        size="1",
                        variant="soft",
                        color_scheme="red",
                        #on_click=SearchState.reset_state
                        on_click=[SearchState.reset_state,rx.set_value("input_user_question", "")]
                    ),
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                "Isso te ajudou?", 
                                size="1",
                                variant="soft",
                                color_scheme="blue",
                            ),
                        ),
                        rx.popover.content(
                            rx.flex(    
                                rx.flex(
                                    rx.button(
                                        rx.icon(tag="thumbs-up"),
                                        size="1",
                                        variant="ghost",
                                        color_scheme=rx.cond(SearchState.is_feedback_selected("up"), "green", "gray"),
                                        on_click=lambda: SearchState.set_feedback("up"),
                                    ),
                                    rx.button(
                                        rx.icon(tag="thumbs-down"),
                                        size="1",
                                        variant="ghost",
                                        color_scheme=rx.cond(SearchState.is_feedback_selected("down"), "red", "gray"),
                                        on_click=lambda: SearchState.set_feedback("down"),
                                    ),
                                    align="center",
                                    justify="between",
                                    spacing="4",
                                ), 
                                rx.flex(
                                    rx.button(
                                        "Enviar",
                                        size="2",
                                        width="5em",
                                        color_scheme="lime",
                                        on_click=SearchState.send_feedback,
                                    ),
                                    justify="between",
                                ),   
                                direction="column" ,
                                spacing="2",
                                width="5em",
                                align="center",
                                justify="between",
                            ),                           
                        ),
                    ),
                    padding_bottom="1em",
                    justify="between",
                    align="center",
                ),
                rx.box(
                    rx.text(
                        SearchState.response,
                        font_size="16px",
                        font_weight="normal",
                        color="#333333",
                        padding="1em",
                    ),
                    rx.text(
                        "Obs.: Essa resposta foi gerada por IA, então pode não ser 100% precisa. Se precisar de mais informações, clique em um dos links abaixo.",
                        font_size="12px",
                        font_weight="normal",
                        color="#333333",
                        padding="1em",
                    ),
                    background_color="#f5f5f5",
                    border_radius="10px",
                ),
                rx.foreach(
                    SearchState.search_results_metadata,
                    lambda artigo: rx.card(
                        rx.link(
                            rx.flex(
                                rx.text(
                                    artigo.titulo_artigo,
                                    font_size="18px",
                                    font_weight="bold",
                                    color="#222222",
                                ),
                                rx.text(
                                    f"Categoria: {artigo.titulo_categoria}",
                                    font_size="12px",
                                    font_weight="medium",
                                    color="gray",
                                ),
                                direction="column",
                                spacing="1",
                            ),
                            href=artigo.url_artigo,
                            is_external=True,
                            underline="none",
                        ),
                        width="100%",
                        height="auto",
                        padding="1em",
                        border_radius="5px",
                    ),
                ),
                direction="column",
                spacing="2",
                padding="1em",
            ),
            rx.box(),
        ),
    )

def upper_area() -> rx.Component:
    return rx.flex( #parte superior como um todo -> vertical
        rx.flex( #linha superior com logo e Bloquear conta -> horizontal
            rx.flex( #logo
                rx.link( #logo
                    rx.image(
                        src="/logo.png",
                        width="5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    href="https://www.noh.com.br/",
                    underline="none",
                    is_external=True,
                ),
                #spacing="2",
            ),
            rx.flex( #logo
                rx.text(
                    "ATENÇÃO: ESSE NÃO É O SITE OFICIAL DA NOH!!!",
                    font_size="1em",
                    font_weight=400,
                    font_family= "sans-serif",
                    color="red",  
                ),
            ),
            rx.flex( #bloquear conta
                rx.link( #botão entrar
                    rx.text(
                        "Bloquear conta",
                        font_size="1em",
                        font_weight=400,
                        font_family= "sans-serif",
                        color="#222222",  
                    ),
                    href="https://cobrar.noh.com.br/#/conta",
                    is_external=True,
                ),
            ),
            #spacing="7",
            justify="between",
            align="center",
            padding_top="1em", 
            padding_left="20em", 
            padding_right="20em", 
        ),
        rx.flex( #titulozão
            rx.text(
                "Oi, veja como aproveitar melhor a Noh",
                font_size="2em",
                font_weight=150,
                font_family= "sans-serif",
                color="#222222",  
            ),
            justify="center",
        ),
        rx.flex( #campo de pesquisa
            rx.input(
                rx.input.slot(rx.icon(tag="search"),color_scheme="grass",),
                placeholder="Qual a sua dúvida?",
                width="40em",
                height="3em",
                radius="large",
                color_scheme="lime",
                on_change=SearchState.set_user_question,
                id="input_user_question",
            ),
            rx.button(
                "Pesquisar", 
                color_scheme="lime", 
                radius="large",
                size="2",
                variant="solid",
                height="3em",
                disabled=SearchState.user_question == "",
                on_click=SearchState.handle_search
            ),
            justify="center",
            padding_bottom="1em",
            spacing="1",
            align="center", 
        ),
        background_color="#ebeae9",
        direction="column",
        width="100%",
        height="19.5em",
        #align="center",
        justify="between",
    )

def center() -> rx.Component:
    return rx.flex(
        answer(),
        rx.callout(
            "⚠️ A Noh não oferece empréstimos nem limite de crédito. Nunca compartilhe seus dados ou senha com ninguém!",
            variant="soft",
            size="2",
            color_scheme="gray",
            justify="center",
            align="center",
        ),
        rx.flex(
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Sobre Nohs",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "Saiba mais sobre a Noh e a nossa segurança.",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",
                            padding="0.5em",  
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.SOBRE_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/sobre-nohs",
                    underline="none",
                    is_external=True,
                ),
                height="15em",
                width="32%",
            ),
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Conta",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "Tudo o que você precisa saber para usar a Noh.",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",  
                            padding="0.5em",  
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.CONTA_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/conta",
                    underline="none",
                    is_external=True,
                ),
                height="15em",
                width="32%",
            ),
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Cartão Noh",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "O cartão compartilhado para casais modernos do Brasil. Um passa, dois pagam!",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",
                            padding="0.5em",    
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.CARTAO_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/cartao-noh",
                    underline="none",
                    is_external=True,
                ),
                height="15em",
                width="32%",
            ),
            width="100%",
            spacing="1",
            justify="between",
        ),
        rx.flex(
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Boletos",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "Tire as suas dúvidas sobre os pagamentos no boleto.",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",
                            padding="0.5em",  
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.BOLETOS_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/boletos",
                    is_external=True,
                    underline="none",
                ),
                height="15em",
                width="32%",
            ),
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Pix",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "O que você precisa saber sobre o funcionamento do Pix na Noh.",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",  
                            padding="0.5em",  
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.PIX_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/pix",
                    is_external=True,
                    underline="none",
                ),
                height="15em",
                width="32%",
            ),
            rx.card(
                rx.link(
                    rx.flex(
                        rx.image(
                            src="/green_circle.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.text(
                            "Mensalidade",
                            font_size="25px",
                            font_weight=100,
                            font_family= "sans-serif",
                            color="#222222",  
                        ),
                        rx.text(
                            "Tudo o que você precisa saber sobre a mensalidade da Noh.",
                            font_size="12px",
                            font_weight="bold",
                            font_family= "sans-serif",
                            color="#222222",
                            padding="0.5em",    
                        ),
                        direction="column",
                        spacing="2",
                        justify="between",
                        align="center",
                    ),
                    #href=routes.MENSALIDADE_ROUTE,
                    href="https://www.noh.com.br/ajuda-categorias/mensalidade",
                    is_external=True,
                    underline="none",
                ),
                height="15em",
                width="32%",
            ),
            width="100%",
            spacing="1",
            justify="between",
        ),
        spacing="6",
        direction="column",
        background_color="#ffffff",
        padding_top="2em",
        width="50%",
        padding_bottom="2em",
        align="center",
    )

def meajuda() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        upper_area(),
        center(),
        footer(),
        direction="column",
        #background_color="#ffffff",
        align="center",
    )