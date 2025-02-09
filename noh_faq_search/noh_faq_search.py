
import reflex as rx

from . import pages
from . import navigation
from .pages.state import SearchState

app = rx.App(
    theme=rx.theme(
        #appearance="light", 
        # has_background=True, 
        # panel_background="solid",
        scaling="90%",
        #radius="medium", 
        #accent_color="bronze",
    )
)

#Website Pages
app.add_page(pages.meajuda, navigation.routes.HOME_ROUTE, title="meajuda", on_load=SearchState.reset_state,)
# app.add_page(pages.sobre, route=navigation.routes.SOBRE_ROUTE, title="FAQ da Noh")
# app.add_page(pages.conta, route=navigation.routes.CONTA_ROUTE, title="FAQ da Noh")
# app.add_page(pages.cartao, route=navigation.routes.CARTAO_ROUTE, title="FAQ da Noh")
# app.add_page(pages.boletos, route=navigation.routes.BOLETOS_ROUTE, title="FAQ da Noh")
# app.add_page(pages.pix, route=navigation.routes.PIX_ROUTE, title="FAQ da Noh")
# app.add_page(pages.mensalidade, route=navigation.routes.MENSALIDADE_ROUTE, title="FAQ da Noh")






