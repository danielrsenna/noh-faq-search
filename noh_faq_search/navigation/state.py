import reflex as rx

from . import routes

class NavState(rx.State):
    def to_sobre(self):
        return rx.redirect(routes.SOBRE_ROUTE)
    def to_conta(self):
        return rx.redirect(routes.CONTA_ROUTE)
    def to_cartao(self):
        return rx.redirect(routes.CARTAO_ROUTE)
    def to_boletos(self):
        return rx.redirect(routes.BOLETOS_ROUTE)
    def to_pix(self):
        return rx.redirect(routes.PIX_ROUTE)
    def to_mensalidade(self):
        return rx.redirect(routes.MENSALIDADE_ROUTE)
    def to_home(self):
        return rx.redirect(routes.HOME_ROUTE)
