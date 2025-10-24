import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("shield-check", class_name="h-10 w-10 text-teal-600"),
                    rx.el.h1(
                        "Admin Panel", class_name="text-2xl font-bold text-gray-800"
                    ),
                    class_name="flex items-center justify-center gap-3 mb-8",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Sign In", class_name="text-xl font-semibold text-gray-700 mb-1"
                    ),
                    rx.el.p(
                        "Enter your credentials to access the dashboard.",
                        class_name="text-sm text-gray-500 mb-6",
                    ),
                    rx.el.form(
                        rx.el.div(
                            _input_field(
                                "username", "Username", "admin", AuthState.set_username
                            ),
                            _input_field(
                                "password",
                                "Password",
                                "••••••••",
                                AuthState.set_password,
                                type="password",
                            ),
                            rx.cond(
                                AuthState.error_message != "",
                                rx.el.div(
                                    rx.icon("badge_alert", class_name="h-4 w-4 mr-2"),
                                    rx.el.p(AuthState.error_message),
                                    class_name="flex items-center text-sm text-red-600 bg-red-50 p-3 rounded-lg mt-4",
                                ),
                                None,
                            ),
                            class_name="flex flex-col gap-4",
                        ),
                        _login_button(),
                        on_submit=AuthState.login,
                        reset_on_submit=False,
                        class_name="w-full",
                    ),
                    class_name="w-full",
                ),
                class_name="flex flex-col items-center p-8 bg-white rounded-2xl shadow-[0_1px_3px_rgba(0,0,0,0.12)] w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4",
        ),
        class_name="font-['Roboto']",
    )


def _input_field(
    name: str,
    label: str,
    placeholder: str,
    on_change: rx.event.EventSpec,
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="block text-sm font-medium text-gray-700 mb-2",
        ),
        rx.el.input(
            type=type,
            id=name,
            name=name,
            placeholder=placeholder,
            on_change=[on_change, AuthState.clear_error],
            class_name="w-full px-4 py-3 bg-gray-100 border-2 border-transparent rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors",
        ),
        class_name="w-full",
    )


def _login_button() -> rx.Component:
    return rx.el.button(
        rx.cond(
            AuthState.is_loading,
            rx.spinner(class_name="w-5 h-5 border-2 border-t-teal-500"),
            rx.el.span("Sign In"),
        ),
        type="submit",
        disabled=~AuthState.is_form_valid | AuthState.is_loading,
        class_name="w-full mt-8 py-3 px-4 bg-teal-600 text-white font-semibold rounded-lg shadow-[0_4px_8px_rgba(0,0,0,0.15)] hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center",
    )