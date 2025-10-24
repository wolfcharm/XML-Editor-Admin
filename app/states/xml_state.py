import reflex as rx
import logging
import os
import xml.etree.ElementTree as ET


class XmlState(rx.State):
    """State for managing XML files."""

    xml_files: list[str] = []
    selected_file: str | None = None
    xml_data: dict[str, str] = {}
    is_loading_files: bool = True

    @rx.event
    def on_dashboard_load(self):
        """Load XML files from the server directory on page load."""
        self.is_loading_files = True
        try:
            xml_dir = rx.get_upload_dir() / "xml_files"
            if not xml_dir.exists():
                xml_dir.mkdir(parents=True, exist_ok=True)
            files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]
            self.xml_files = sorted(files)
        except Exception as e:
            logging.exception(f"Error loading XML files: {e}")
            yield rx.toast.error("Failed to load XML files.")
        self.is_loading_files = False

    @rx.event
    def select_file(self, filename: str):
        """Select an XML file and parse its content."""
        if self.selected_file == filename:
            self.selected_file = None
            self.xml_data = {}
            return
        self.selected_file = filename
        if not self._parse_xml(filename):
            yield rx.toast.error(f"Failed to parse {filename}.")

    def _parse_xml(self, filename: str) -> bool:
        try:
            file_path = rx.get_upload_dir() / "xml_files" / filename
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = {}
            for prop in root.findall("property"):
                name = prop.get("name")
                value = prop.get("value", "")
                if name:
                    data[name] = value
            self.xml_data = data
            return True
        except Exception as e:
            logging.exception(f"Error parsing XML file {filename}: {e}")
            self.xml_data = {}
            return False

    @rx.event
    def update_field_value(self, key: str, value: str):
        """Update the value of an XML field in the state."""
        self.xml_data[key] = value

    @rx.event
    def save_xml_file(self):
        """Save the updated XML data back to the file."""
        if not self.selected_file or not self.xml_data:
            yield rx.toast.warning("No file selected or no data to save.")
            return
        try:
            root = ET.Element("ServerSettings")
            for name, value in self.xml_data.items():
                ET.SubElement(root, "property", {"name": name, "value": str(value)})
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ", level=0)
            file_path = rx.get_upload_dir() / "xml_files" / self.selected_file
            with file_path.open("wb") as f:
                tree.write(f, encoding="utf-8", xml_declaration=True)
            yield rx.toast.success(f"Successfully saved {self.selected_file}.")
        except Exception as e:
            logging.exception(f"Error saving XML file: {e}")
            yield rx.toast.error(f"Failed to save {self.selected_file}.")