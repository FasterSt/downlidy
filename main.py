import flet as ft;

# Components
from components.exit_dialog_confirm import exit_dialog_confirm
from components.tabs import list_tabs

def main(page: ft.Page):
    # Config window
    page.title = "Prototype to downlidy app"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 600
    page.window.width = 800
    page.theme_mode = ft.ThemeMode.LIGHT

    def progreso(d):
        if d['status'] == 'downloading':
            progress_text.value = f"Descargando... {d['_percent_str']} | Velocidad: {d['_speed_str']}"
            progress_bar.value = float(d['_percent_str'].replace('%','')) / 100
            page.update()
        elif d['status'] == 'finished':
            progress_text.value = "¡Descarga completa!"
            progress_bar.value = 1
            page.update()

    def window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)
            page.update()
        

            # Here you would add the logic to download the file from the URL
            # For now, we just simulate a download with a message

    # set components UI
    yt_url = ft.Text()
    info_txt = ft.Text()

    # Selectores dinámicos
    video_dropdown = ft.Dropdown(label="Calidad de video", width=300)
    audio_dropdown = ft.Dropdown(label="Calidad de audio", width=300)

    # Barra de progreso
    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text()
    
    # Exit confirm component
    confirm_dialog = exit_dialog_confirm(page)    

    page.window.prevent_close = True
    page.window.on_event = window_event
    container_tabs = list_tabs(page)

    page.add(
        ft.Container(
            expand=True,
            content=container_tabs,
        ),
    )

ft.app(target=main)