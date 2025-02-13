
import reflex as rx

from . import pages
from . import navigation
from .pages.state import SearchState
from .pages.dash_state import DashboardState

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
app.add_page(pages.meajuda, navigation.routes.HOME_ROUTE, title="meajuda", on_load=SearchState.reset_state)
app.add_page(pages.dash, navigation.routes.DASH_ROUTE, title="dashboard",on_load=DashboardState.load_all_data)


