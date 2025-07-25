import flet as ft
import threading

# Components
from components.yt_dlp_comp import yt_downloader
from components.search_yt import get_trending_videos


def home_page(page: ft.Page):
    items = []

    def on_submit_url(e):
        yt_url.value = e.control.value
        info_txt.value = "Cargando ..."
        loading_ring.visible = True
        result_row.controls.clear()
        page.update()

        yt_downloader(page, yt_url, loading_ring, info_txt, result_row)

    def handle_click_video(e):
        print("Clicked!!!")

    def fetch_trending_videos():
        info_txt.value = "Cargando ..."
        loading_ring.visible = True
        trending_videos = get_trending_videos()
        info_txt.value = ""
        loading_ring.visible = False
        print("Ya pase el fetching de videos")
        print(trending_videos)
        for video in trending_videos:
            thumbnail_url = video['thumbnails'][-1]['url']
            video_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(src=thumbnail_url or '', width=300, height=200),
                            ft.Text(video['title'], size=16, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Text(f"Channel: {video['channel']}", size=12),
                                    ft.Text(f"Views: {video['view_count']}", size=12),
                                    ]),
                            ft.Text(f"Duration: {video['duration']} seconds", size=12),
                        ]
                    ),
                    alignment=ft.alignment.top_left,
                    bgcolor=ft.Colors.CYAN_100,
                    on_click=handle_click_video
                ),
            )
            container_videos.controls.append(video_card)
        for i in range(20):
            items.append(
                ft.Container(
                    content=ft.Text(f"Item {i}", size=20),
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.AMBER_100,
                    padding=10,
                    border_radius=10,
                )
            )
        print("Ya agregue los video a la grid")
        page.update()

    yt_url = ft.Text()
    info_txt = ft.Text()
    btn_download = ft.IconButton(
                tooltip="Buscar", 
                icon_size=40, 
                icon=ft.Icons.SEARCH,
                icon_color=ft.Colors.BLUE,
                on_click=on_submit_url,
            )
    loading_ring = ft.ProgressRing(width=16, height=16, visible=False)
    inpt_url = ft.TextField(
                label="Enter YouTube URL",
                width=400,
                autofocus=True,
                on_submit=on_submit_url,
                disabled=True, # To test the player video
            )
    result_row = ft.Row()

    container_videos = ft.GridView(
        runs_count=4,
        run_spacing=10,
        spacing=10,
        controls=[],
        max_extent=300,
        expand=True,
        height=300,
    )
    
    threading.Thread(target=fetch_trending_videos).start()
    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    inpt_url,
                    btn_download,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            info_txt,
            loading_ring,
            ft.Row(
                controls=[
                    container_videos,
                    # result_row,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
