import flet as ft;

def exit_dialog_confirm(page: ft.Page):
    def yes_click(e):
        page.window.destroy()

    def no_click(e):
        page.close(confirm_dialog)
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    return confirm_dialog