import reflex as rx

from ..ui import footer

def dash() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        footer(),
        direction="column",
        #background_color="#ffffff",
        align="center",
    )