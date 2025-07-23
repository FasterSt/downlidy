import threading
import flet as ft
from yt_dlp import YoutubeDL

def yt_downloader(
        page: ft.Page, 
        url: ft.TextField, 
        loading_ring: ft.ProgressRing,
        info_txt: ft.Text,
        result_row: ft.Row
):

    best_formats = {}
    best_audio_formats = {}
    selected_format = None

    def ok_click(e):
        page.close(warning_dialog)
        page.update()

    # def progreso(d):
    #     if d['status'] == 'downloading':
    #         # Limpiar códigos ANSI (por si acaso)
    #         percent_clean = re.sub(r'[^0-9.]', '', d['_percent_str'])
    #         try:
    #             progress_bar.value = float(percent_clean) / 100
    #         except ValueError:
    #             progress_bar.value = 0

    #         progress_text.value = f"Descargando... {d['_percent_str']} | Velocidad: {d['_speed_str']}"
    #         page.update()
    #     elif d['status'] == 'finished':
    #         progress_text.value = "¡Descarga completa!"
    #         progress_bar.value = 1
    #         page.update()

    # Handle format On_change
    def handle_format_change(e: ft.ControlEvent):
        nonlocal selected_format
        selected_format = e.control.value

        print(f"Selected format: {selected_format}")
        vquality_dropdown.options.clear()
        for (heigth, ext), video in best_formats.items():
            if selected_format == ext:
                vquality_dropdown.options.append(
                    ft.dropdown.Option(
                        key=f"({heigth}, '{ext}')",
                        text=f"{video['resolution']}p - {int(video.get('fps', '?'))}Fps ({video['audio_format']['tbr']}kbps) (~{video['video_size_approx']: .2f}Mb approx)",
                        content=ft.Row(
                            controls=[
                                ft.Text(f"{video['resolution']}p, {video.get('fps', '?')}fps.{ext}"),
                                ft.Row(
                                    controls=[
                                        ft.Text(f"({video['audio_format']['tbr']}kbps)", size=12, color=ft.Colors.GREY_400),
                                        ft.Text(f"(~{video['video_size_approx']: .2f}Mb approx)", size=12, color=ft.Colors.GREY)
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            expand=True
                        )
                    )
                )
        vquality_dropdown.menu_height = 200
        vquality_dropdown.menu_width = 400
        vquality_dropdown.value = vquality_dropdown.options[0].key if vquality_dropdown.options else None
        page.update()

    # Download video function
    def download_video(e):
        selected = vquality_dropdown.value
        if not selected:
            info_txt.value = "Seleccione una calidad de video."
            page.update()
            return

        selected = eval(selected)  # Convert string representation back to tuple
        video = best_formats[selected]
        v_format_id = video['format_id']
        a_format_id = video['audio_format']['format_id']
        print(f"Selected video format: {v_format_id}, audio format: {a_format_id}")
        info_txt.value = "Descargando video..."

        def download():
            ydl_opts = {
                'format': f"{v_format_id} + {a_format_id}",
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                # 'quiet': True,
                'noplaylist': True,
                'no_color': True
            }
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url.value])
                    info_txt.value = "Descarga completa."
                except Exception as ex:
                    info_txt.value = f"Error al descargar: {ex}"
            
            loading_ring.visible = False
            page.update()

        threading.Thread(target=download).start()        

    # fetch data video
    def fetch():
        if not url.value:
            page.open(warning_dialog)
            page.update()
        
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'no_color': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                video_info = ydl.extract_info(url.value, download=False)
                duration_str = video_info.get('duration_string', 0)
                duration = video_info.get('duration', 0)

                nonlocal best_formats, best_audio_formats, selected_format
                best_formats.clear()
                vquality_dropdown.options.clear()
                format_dropdown.options.clear()

                info_txt.value = ""
                loading_ring.visible = False
                thumbnail = ft.Image(
                    src=video_info.get('thumbnail', ""),
                    width=320,
                    height=128,
                    fit=ft.ImageFit.CONTAIN,
                )


                list_videos = [f for f in video_info['formats'] if f.get('vcodec') != 'none']
                list_audios = [f for f in video_info['formats'] if f.get('acodec') != 'none' and (not f.get('vcodec') or f.get('vcodec') == 'none')]

                filtered_videos = [
                    f for f in list_videos
                    if f.get('fps') in [30, 60]
                ]

                filtered_audios = [
                    f for f in list_audios 
                    if f.get('abr') is not None 
                    and f.get('abr') >= 128 and f.get('abr') <= 256
                ]

                print("ya pase el filtro de videos")
                for a in filtered_audios:
                    key = a['ext']
                    current_best = best_audio_formats.get(key)

                    if (not current_best 
                        or ((a.get('tbr', 0) >= current_best.get('tbr', 0)) 
                        and a['quality'] >= current_best['quality'])
                        and a['language'] == 'es'
                        ):
                        best_audio_formats[key] = a
                
                print("Ya pasé el filtro de audio")
                for f in filtered_videos:
                    key = (f['height'], f['ext'])
                    current_best = best_formats.get(key)

                    if not current_best or (f.get('tbr', 0) > current_best.get('tbr', 0)):
                        if f['ext'] == 'mp4':
                            f['audio_format'] = best_audio_formats['m4a'] if 'm4a' in best_audio_formats else None
                        elif f['ext'] == 'webm':
                            f['audio_format'] = best_audio_formats['webm'] if 'webm' in best_audio_formats else None
                                                        
                        f['video_size_approx'] = (
                            (a['tbr'] + f['tbr']) * duration / (8 * 1024) 
                            if a.get('tbr') is not None and f.get('tbr') is not None 
                            else 0
                        )
                        best_formats[key] = f
                
                print("Pass for best formats")
                # print(duration)
                # print(best_formats)

                list_formats = set({ext for (_, ext) in best_formats})
                print(f"#Selected: {selected_format}")

                vquality_dropdown.options.append(
                    ft.dropdown.Option(
                        key="None Selected",
                        content=ft.Row(
                            controls=[
                                ft.Text("---No video selected---", size=14, color=ft.Colors.GREY_400),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                        ),
                        disabled=True,
                    ),
                )
                
                for ext in list_formats:
                    format_dropdown.options.append(
                        ft.dropdown.Option(
                            key=ext,
                            text=f"{ext.upper()}",
                            content=ft.Text(ext.upper())
                        )
                    )
                result_row.controls.clear()
                result_row.controls.append(
                        ft.Row(
                            controls=[
                                thumbnail,
                                ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                format_dropdown,
                                                vquality_dropdown,
                                            ]
                                        ),
                                        ft.ElevatedButton(
                                            "Download",
                                            width=200,
                                            icon=ft.Icons.DOWNLOAD,
                                            on_click=download_video
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=5,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                        ),

                    )

                (selct_heigth, selct_ext), video = next(iter(best_formats.items()))
                # vquality_dropdown.value = f"{selct_heigth}p.{selct_ext}"
                print(f"{video['resolution']}p, {video.get('fps', '?')}fps.{ext} ({video['audio_format']['tbr']}kbps) (~{video['video_size_approx']: .2f}Mb approx")
                # page.update()
            except Exception as ex:
                print(f"Error fetching video info: {ex}")
                info_txt.value = f"Error: {ex}"

            page.update()


    # components
    vquality_dropdown = ft.Dropdown(label="Select Quality", width=200)
    aquality_dropdown = ft.Dropdown(label="Select Audio Quality", width=400)
    format_dropdown = ft.Dropdown(label="Select Format", width=200, on_change=handle_format_change)


    warning_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=28),
                ft.Text("You don't Provide a Correct URL Youtube Video"),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        content=ft.Text("Provide a correct url youtube video to proceed to downloaded"),
        actions=[
            ft.TextButton("Ok", on_click=ok_click)
        ],
    )

    # Execution fetch function
    threading.Thread(target=fetch).start()