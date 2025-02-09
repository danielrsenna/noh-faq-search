
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






