import flet as ft

# Views
from views.home import home_page

def list_tabs(page: ft.Page):
    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tab_alignment=ft.TabAlignment.CENTER,
        tabs=[
            ft.Tab(
                    text="Home", 
                    content=ft.Container(
                        content=home_page(page),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.LIGHT_BLUE_50,
                        border=ft.border.all(2, ft.Colors.BLUE_300),
                )
            ),
            ft.Tab(
                    text="Music", 
                    content=ft.Container(
                        content=ft.Text("Welcome to Audio Download Page 🔥!"),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.LIGHT_BLUE_50,
                        border=ft.border.all(2, ft.Colors.BLUE_300),
                )
            ),
        ]
    )