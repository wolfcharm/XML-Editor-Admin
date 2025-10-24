import reflex as rx
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.states.auth_state import AuthState
from app.database import initialize_users


def index() -> rx.Component:
    return rx.cond(AuthState.is_logged_in, dashboard_page(), login_page())


initialize_users()
app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)