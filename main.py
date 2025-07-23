import flet as ft;
from yt_dlp import YoutubeDL;

# Components
from components.exit_dialog_confirm import exit_dialog_confirm
from components.yt_dlp_comp import yt_downloader

def main(page: ft.Page):
    # Config window
    page.title = "Prototype to downlidy app"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 600
    page.window.width = 800

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

    loading_ring = ft.ProgressRing(width=16, height=16, visible=False)


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

    def on_submit_url(e):
        yt_url.value = e.control.value
        info_txt.value = "Cargando ..."
        loading_ring.visible = True
        result_row.controls.clear()
        page.update()

        yt_downloader(page, yt_url, loading_ring, info_txt, result_row)
        

            # Here you would add the logic to download the file from the URL
            # For now, we just simulate a download with a message

    inpt_url = ft.TextField(
            label="Enter YouTube URL",
            width=400,
            autofocus=True,
            on_submit=on_submit_url,
        )
    btn_download = ft.ElevatedButton("Download", width=200, icon=ft.Icons.DOWNLOAD)

    page.window.prevent_close = True
    page.window.on_event = window_event
    result_row = ft.Row()

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[inpt_url,btn_download], alignment=ft.MainAxisAlignment.CENTER, spacing=20,),
                info_txt,
                loading_ring,
                result_row
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

ft.app(target=main)