import reflex as rx
import asyncio
import logging
import os


class AuthState(rx.State):
    is_logged_in: bool = False
    username: str = ""
    password: str = ""
    error_message: str = ""
    is_loading: bool = False

    def _get_users(self) -> dict[str, str]:
        users_file = rx.get_upload_dir() / "users.txt"
        users = {}
        if not users_file.exists():
            logging.error("Users file not found!")
            return users
        with users_file.open("r") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    username, password = line.split(":", 1)
                    users[username] = password
        return users

    @rx.var
    def is_form_valid(self) -> bool:
        return (self.username != "") & (self.password != "")

    @rx.event
    async def login(self):
        self.is_loading = True
        self.error_message = ""
        yield
        await asyncio.sleep(0.5)
        try:
            users = self._get_users()
            user_password = users.get(self.username)
            if user_password and user_password == self.password:
                self.is_logged_in = True
                self.username = ""
                self.password = ""
                self.error_message = ""
            else:
                self.error_message = "Invalid credentials. Please try again."
        except Exception as e:
            logging.exception(f"Error during login: {e}")
            self.error_message = "A server error occurred. Please try again later."
        self.is_loading = False

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.username = ""
        self.password = ""

    @rx.event
    def clear_error(self):
        self.error_message = ""