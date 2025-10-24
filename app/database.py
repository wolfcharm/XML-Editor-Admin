import os
import reflex as rx


def initialize_users():
    """Create an empty users file if it doesn't exist."""
    upload_dir = rx.get_upload_dir()
    users_file = upload_dir / "users.txt"
    if not users_file.exists():
        users_file.parent.mkdir(parents=True, exist_ok=True)
        with users_file.open("w") as f:
            pass
    xml_dir = upload_dir / "xml_files"
    if not xml_dir.exists():
        xml_dir.mkdir(parents=True, exist_ok=True)