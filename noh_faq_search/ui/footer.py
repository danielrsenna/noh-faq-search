import reflex as rx

def footer_item(text: str, href: str) -> rx.Component:
    return rx.link(rx.text(text, size="3", color="#ffffff", font_family= "sans-serif"), href=href, is_external=True)


def footer_items_1() -> rx.Component:
    return rx.flex(
        footer_item("Termos & Condições", "https://www.noh.com.br/termos-de-uso"),
        footer_item("Tarifas e Taxas", "https://www.noh.com.br/tarifas"),
        footer_item("Política de Privacidade", "https://www.noh.com.br/politica-de-privacidade"),
        footer_item("Sobre Nohs", "https://www.noh.com.br/sobre-nohs"),
        footer_item("Sobre a Ana Zucato", "https://www.noh.com.br/ana-zucato-fundadora-ceo-noh"),
        footer_item("Sobre a Nath Finanças", "https://www.noh.com.br/nath-financas-socia-noh"),
        footer_item("Embaixadores Noh", "https://www.notion.so/fazumnoh/Embaixadores-Noh-05d7d80d964746c6a1add4dae8902625?pvs=4"),
        footer_item("Calculadora", "https://www.noh.com.br/calculadora"),
        footer_item("Preciso de ajuda!", "https://www.noh.com.br/meajuda"),
        footer_item("Bloquear conta", "https://cobrar.noh.com.br/#/conta"),
        spacing="3",
        text_align="start",
        flex_direction="column",
    )


def social_link(icon: str, href: str) -> rx.Component:
    return rx.link(rx.icon(icon, color="#ffffff", size=15), href=href, is_external=True)


def socials() -> rx.Component:
    return rx.flex(
        social_link("instagram", "https://www.instagram.com/fazumnoh/"),
        social_link("facebook", "https://www.facebook.com/fazumnoh/"),
        social_link("linkedin", "https://www.linkedin.com/company/nohpay/"),
        social_link("youtube", "https://www.youtube.com/channel/UCLFC8zqj_pTV9nokxIatrDA"),
        spacing="3",
        justify_content="center",
        width="100%",
    )


def footer() -> rx.Component:
    return rx.flex(
        rx.flex( #row no topo com logo à esquerda
            rx.image(
                src="/round_icon.png", 
                width="2em",
                height="auto",
                border_radius="25%",
            ),
            padding_top="5em",
            justify="between",
            align="start",
            direction="column",
            #width="50%",
        ),
        rx.flex(#row no meio com 3 colunas
            rx.flex(
                footer_items_1(),
                direction="column",
            ),
            rx.flex(
                rx.text("FALE COM NÓS", color="#ffffff", font_size="10px", font_family= "sans-serif"),
                rx.link(rx.text("meajuda@noh.com.br", color="#ffffff", font_family= "sans-serif"),href="mailto:meajuda@noh.com.br", is_external=True),
                spacing="2",
                justify="end",
                direction="column",
            ),
            rx.flex(
                rx.text("SIGA-NOHS",color="#ffffff", font_size="10px", font_family= "sans-serif"),
                socials(),
                spacing="2",
                justify="end",
                direction="column",
            ),
            justify="between",
        ),
        rx.divider(color_scheme="grass",size="4"),
        rx.flex(#row no fim
            rx.flex(
                rx.text("Noh Pay LTDA. 44.179.162/0001-04  /  Inscrição Estadual. 71230483" , color="#ffffff", font_size="10px", font_family= "sans-serif"),
                rx.text("Rua Cardeal Arcoverde, 2365 - Pinheiros, São Paulo, SP - 05407-003", color="#ffffff", font_size="10px", font_family= "sans-serif"),
                rx.text("SAC 0800 326 0965", color="#ffffff", font_size="10px", font_family= "sans-serif"),
                direction="column",
            ),
            rx.flex(
                rx.text("Feito com 💚", color="#ffffff", font_size="10px", font_family= "sans-serif"),
                rx.text("Desde Novembro 2021", color="#ffffff", font_size="10px", font_family= "sans-serif"),
                direction="column",
            ),
            justify="between",
        ),
        direction="column",
        height="90vh",
        width="100%",
        background_color="#222222",
        justify="between",
        padding_left="15em",
        padding_right="15em",
        padding_bottom="5em",
    )


















    return rx.el.footer(
        rx.vstack(
            rx.flex(
                footer_items_1(),
                justify="between",
                spacing="6",
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            rx.divider(),
            rx.flex(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.text(
                        "© 2024 Reflex, Inc",
                        size="3",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                    justify_content=[
                        "center",
                        "center",
                        "start",
                    ],
                    width="100%",
                ),
                socials(),
                spacing="4",
                flex_direction=["column", "column", "row"],
                width="100%",
            ),
            spacing="5",
            width="100%",
        ),

    )

