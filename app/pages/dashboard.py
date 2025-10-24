import reflex as rx
from app.states.auth_state import AuthState
from app.states.xml_state import XmlState


def dashboard_page() -> rx.Component:
    return rx.el.div(
        _header(),
        rx.el.div(_sidebar(), _editor_panel(), class_name="flex flex-1"),
        on_mount=XmlState.on_dashboard_load,
        class_name="font-['Roboto'] bg-gray-50 min-h-screen flex flex-col",
    )


def _header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1("XML File Editor", class_name="text-2xl font-bold text-gray-800"),
            rx.el.div(
                rx.el.button(
                    "Save Changes",
                    on_click=XmlState.save_xml_file,
                    disabled=~XmlState.selected_file.to(bool),
                    class_name="px-6 py-2 bg-teal-600 text-white font-semibold rounded-lg shadow-md hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
                ),
                rx.el.button(
                    "Logout",
                    on_click=AuthState.logout,
                    class_name="px-6 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300 transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center w-full",
        ),
        class_name="w-full p-4 border-b border-gray-200 bg-white shadow-sm shrink-0",
    )


def _sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.h2(
            "XML Files",
            class_name="text-lg font-semibold text-gray-700 p-4 border-b border-gray-200",
        ),
        rx.cond(
            XmlState.is_loading_files,
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-teal-600"),
                class_name="flex items-center justify-center p-8",
            ),
            rx.el.nav(
                rx.foreach(XmlState.xml_files, _file_menu_item),
                class_name="flex flex-col p-2 space-y-1 overflow-y-auto",
            ),
        ),
        class_name="w-64 bg-white border-r border-gray-200 flex flex-col",
    )


def _file_menu_item(filename: str) -> rx.Component:
    return rx.el.a(
        rx.icon("file-text", class_name="w-5 h-5 mr-3 shrink-0"),
        rx.el.span(filename, class_name="truncate"),
        on_click=lambda: XmlState.select_file(filename),
        href="#",
        class_name=rx.cond(
            XmlState.selected_file == filename,
            "flex items-center px-3 py-2 text-sm font-medium rounded-md bg-teal-50 text-teal-700 cursor-pointer",
            "flex items-center px-3 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-100 hover:text-gray-900 cursor-pointer",
        ),
    )


def _editor_panel() -> rx.Component:
    return rx.el.main(
        rx.cond(XmlState.selected_file.to(bool), _xml_editor(), _empty_state_editor()),
        class_name="flex-1 p-8 overflow-y-auto",
    )


def _empty_state_editor() -> rx.Component:
    return rx.el.div(
        rx.icon("file-search", class_name="w-16 h-16 text-gray-300 mb-4"),
        rx.el.h3("Select a file", class_name="text-xl font-semibold text-gray-700"),
        rx.el.p(
            "Choose an XML file from the left menu to begin editing.",
            class_name="text-gray-500 mt-2",
        ),
        class_name="flex flex-col items-center justify-center h-full text-center bg-white rounded-2xl border-2 border-dashed border-gray-200",
    )


def _xml_editor() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            rx.el.span("Editing: ", class_name="font-medium text-gray-600"),
            rx.el.span(XmlState.selected_file, class_name="font-bold text-teal-700"),
            class_name="text-xl mb-6 pb-4 border-b border-gray-200",
        ),
        rx.el.div(
            rx.foreach(XmlState.xml_data.keys(), _editor_field), class_name="space-y-5"
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def _editor_field(key: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            key, class_name="block text-sm font-semibold text-gray-600 mb-2 capitalize"
        ),
        rx.el.input(
            default_value=XmlState.xml_data[key],
            on_change=lambda val: XmlState.update_field_value(key, val),
            class_name="w-full px-4 py-3 bg-gray-100 border-2 border-transparent rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-colors",
        ),
        class_name="w-full",
    )