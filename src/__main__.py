import os
import sys
import shutil
import pathlib
import webbrowser
from typing import Callable

import flet as ft

import tempo_core
import tempo_core.app_runner
import tempo_core.data_structures
import tempo_core.file_io
import tempo_core.main_logic
import tempo_core.programs
import tempo_core.programs.unreal_engine
import tempo_core.settings

import file_io
import settings
import logger
import initialization
import tempo


original_webbrowser_open = webbrowser.open


def get_settings_path_suffix_from_full_path(settings_path: pathlib.Path) -> str:
    base_directory = pathlib.Path(os.path.dirname(tempo.get_default_preset_directory()))
    path = os.path.normpath(str(settings_path.relative_to(base_directory)))
    return path


def get_should_be_resizable() -> bool:
    return True


def get_should_be_maximizable() -> bool:
    return True


def add_button_row(page: ft.Page, button_labels_to_callbacks: dict[str, Callable]):
    row = ft.Row(expand=True, spacing=10)

    for label, callback in button_labels_to_callbacks.items():
        button = ft.OutlinedButton(
            height=24,
            text=label,
            expand=True,
            on_click=lambda e, cb=callback: cb(e),
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=12)),
        )
        row.controls.append(button)

    container = ft.Container(content=row, padding=0, margin=0)

    page.add(container)


def add_google_and_youtube_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Google": lambda e: webbrowser.open("http://www.google.com"),
            "Youtube": lambda e: webbrowser.open("http://www.youtube.com"),
        },
    )


def add_github_and_unreal_docs_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Github": lambda e: webbrowser.open("http://www.github.com"),
            "Unreal Docs": lambda e: webbrowser.open(
                "https://dev.epicgames.com/documentation/en-us/unreal-engine"
            ),
        },
    )


def stove_button_was_clicked():
    tempo_core.main_logic.install_stove(
        output_directory=f"{tempo.get_tempo_gui_assets_directory()}/stove",
        run_after_install=True,
    )


def spaghetti_button_was_clicked():
    tempo_core.main_logic.install_spaghetti(
        output_directory=os.path.normpath(
            f"{tempo.get_tempo_gui_assets_directory()}/spaghetti"
        ),
        run_after_install=True,
    )


def add_stove_and_spaghetti_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Stove": lambda e: stove_button_was_clicked(),
            "Spaghetti": lambda e: spaghetti_button_was_clicked(),
        },
    )


def uasset_gui_button_was_clicked():
    tempo_core.main_logic.install_uasset_gui(
        output_directory=f"{tempo.get_tempo_gui_assets_directory()}/uasset_gui",
        run_after_install=True,
    )


def kismet_analyzer_button_was_clicked():
    tempo_core.main_logic.install_kismet_analyzer(
        output_directory=os.path.normpath(
            f"{tempo.get_tempo_gui_assets_directory()}/kismet_analyzer"
        ),
        run_after_install=True,
    )


def add_uasset_gui_and_kismet_analyzer_row(page: ft.Page):
    add_button_row(
        page,
        {
            "UAssetGUI": lambda e: uasset_gui_button_was_clicked(),
            "Kismet Analyzer": lambda e: kismet_analyzer_button_was_clicked(),
        },
    )


def fmodel_button_was_clicked():
    tempo_core.main_logic.install_fmodel(
        output_directory=f"{tempo.get_tempo_gui_assets_directory()}/fmodel",
        run_after_install=True,
    )


def umodel_button_was_clicked():
    tempo_core.main_logic.install_umodel(
        output_directory=f"{tempo.get_tempo_gui_assets_directory()}/umodel",
        run_after_install=True,
    )


def add_umodel_and_fmodel_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Umodel": lambda e: umodel_button_was_clicked(),
            "Fmodel": lambda e: fmodel_button_was_clicked(),
        },
    )


def open_blender():
    tempo_core.app_runner.run_app(
        settings.get_blender_path_from_settings(),
        tempo_core.data_structures.ExecutionMode.ASYNC,
    )


def open_ide():
    tempo_core.app_runner.run_app(
        settings.get_ide_path_from_settings(),
        tempo_core.data_structures.ExecutionMode.ASYNC,
    )


def add_ide_and_blender_row(page: ft.Page):
    if (
        settings.get_blender_path_from_settings() == ""
        and settings.get_ide_path_from_settings() == ""
    ):
        return
    elif (
        not settings.get_blender_path_from_settings() == ""
        and not settings.get_ide_path_from_settings() == ""
    ):
        add_button_row(
            page, {"IDE": lambda e: open_ide(), "Blender": lambda e: open_blender()}
        )
        return
    elif settings.get_blender_path_from_settings() == "":
        add_button_row(
            page,
            {
                "IDE": lambda e: open_ide(),
            },
        )
        return
    else:
        add_button_row(
            page,
            {
                "Blender": lambda e: open_blender(),
            },
        )


def open_game_paks_folder(event):
    game_win_64_exe_path = str(tempo_core.settings.get_game_exe_path())
    game_paks_dir = str(
        tempo_core.programs.unreal_engine.get_game_paks_dir(
            uproject_file_path=tempo_core.settings.get_uproject_file(),
            game_dir=tempo_core.programs.unreal_engine.get_game_dir(
                game_win_64_exe_path
            ),
        )
    )
    tempo_core.file_io.open_dir_in_file_browser(game_paks_dir)


def open_game_exe_folder(event):
    game_win_64_exe_path = str(tempo_core.settings.get_game_exe_path())
    tempo_core.file_io.open_dir_in_file_browser(os.path.dirname(game_win_64_exe_path))


def add_game_paks_dir_and_game_exe_dir_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Game Paks Folder": open_game_paks_folder,
            "Game Exe Folder": open_game_exe_folder,
        },
    )


def add_tempo_dir_and_persistent_mods_dir_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Tempo Folder": lambda e: tempo_core.file_io.open_dir_in_file_browser(
                str(file_io.SCRIPT_DIR)
            ),
            "Persistent Mods Folder": lambda e: tempo_core.file_io.open_dir_in_file_browser(
                f"{os.path.dirname(str(settings.get_current_tempo_settings_file()))}/mod_packaging/persistent_files"
            ),
        },
    )


def test():
    tempo_core.main_logic.run_game(toggle_engine=False)


def add_test_mods_all_and_run_game_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Test Mods All": lambda e: tempo_core.main_logic.test_mods_all(
                toggle_engine=False, use_symlinks=False
            ),
            "Run Game": lambda e: test(),
        },
    )


def get_current_settings_path() -> str:
    return str(settings.get_current_tempo_settings_file())


settings_path_label_text = ft.TextField()


def add_settings_path_row(page: ft.Page):
    global settings_path_label_text
    settings_label_text = ft.Text(
        value="Settings Path: ", size=12, style=ft.TextStyle(weight=ft.FontWeight.BOLD)
    )
    settings_path_label_text = ft.TextField(
        value=get_settings_path_suffix_from_full_path(
            pathlib.Path(get_current_settings_path())
        ),
        text_size=12,
        multiline=True,
        content_padding=8,
        scroll_padding=4,
    )
    sub_row = ft.Row(expand=True, controls=[settings_path_label_text], wrap=True)
    row = ft.Row(expand=True, controls=[settings_label_text, sub_row])
    settings_label_container = ft.Container(
        border=ft.border.all(1, ft.Colors.BLUE_GREY),
        content=row,
        padding=ft.Padding(10, 0, 0, 0),
        border_radius=3,
    )
    page.add(settings_label_container)


def set_settings_input_box_value(value: str):
    global settings_path_label_text
    settings_path_label_text.value = get_settings_path_suffix_from_full_path(
        pathlib.Path(value)
    )
    settings_path_label_text.update()


def drop_down_selection_changed(event: ft.ControlEvent):
    selected_settings_path = os.path.normpath(
        f"{os.path.dirname(os.path.dirname(get_current_settings_path()))}/{event.data}"
    )
    settings.set_current_tempo_settings_file(pathlib.Path(selected_settings_path))
    set_settings_input_box_value(selected_settings_path)


def refresh_dropdown():
    global main_dropdown
    main_dropdown.value = get_settings_path_suffix_from_full_path(
        pathlib.Path(get_current_settings_path())
    )
    main_dropdown.options = [
        ft.dropdown.Option(get_settings_path_suffix_from_full_path(string_path))
        for string_path in settings.get_settings_files_list_from_tempo_gui_settings()
    ]
    main_dropdown.update()


def refresh_input_box():
    set_settings_input_box_value(str(settings.get_current_tempo_settings_file()))


def minus_button_clicked(event: ft.ControlEvent):
    settings_dir = os.path.dirname(get_current_settings_path())

    if len(settings.get_settings_files_list_from_tempo_gui_settings()) == 1:
        return

    mod_packaging_dir = os.path.normpath(
        f"{os.path.dirname(get_current_settings_path())}/mod_packaging"
    )

    if os.path.isdir(mod_packaging_dir):
        shutil.rmtree(mod_packaging_dir)

    if os.path.isfile(get_current_settings_path()):
        os.remove(get_current_settings_path())
    if os.path.isdir(settings_dir) and not os.listdir(settings_dir):
        shutil.rmtree(settings_dir)

    settings.remove_settings_files_from_list(
        settings.get_settings(), [pathlib.Path(get_current_settings_path())]
    )
    settings.set_current_tempo_settings_file(
        settings.get_settings_files_list_from_tempo_gui_settings()[0]
    )

    refresh_input_box()
    refresh_dropdown()


def add_button_clicked(event: ft.ControlEvent):
    global settings_path_label_text
    full_path = os.path.normpath(
        f"{os.path.dirname(os.path.dirname(settings.get_current_tempo_settings_file()))}/{settings_path_label_text.value}"
    )
    if (
        pathlib.Path(os.path.normpath(full_path))
        in settings.get_settings_files_list_from_tempo_gui_settings()
    ):
        return
    if not settings_path_label_text.value:
        return
    if len(full_path.strip()) == 0:
        return

    raw_value = settings_path_label_text.value.strip("'\"").strip()

    normalized_path = pathlib.Path(raw_value)

    parts = [part for part in normalized_path.parts if part.strip()]

    if len(parts) != 2 or parts[-1].lower() != "settings.json":
        return []

    if os.path.isfile(full_path):
        return
    if (
        os.path.normpath(settings_path_label_text.value).lower()
        == os.path.normpath("default/settings.json").lower()
    ):
        return
    settings.set_current_tempo_settings_file(pathlib.Path(full_path))
    settings.add_settings_files_to_list(
        settings.get_settings(), [pathlib.Path(full_path)]
    )
    dir_to_copy_from = str(tempo.get_tempo_preset_template_dir())
    dir_to_copy_to = os.path.normpath(
        f"{os.path.dirname(str(tempo.get_tempo_gui_assets_directory()))}/presets/{settings_path_label_text.value.split(os.sep)[0]}"
    )
    if os.path.isdir(dir_to_copy_to):
        shutil.rmtree(dir_to_copy_to)
    shutil.copytree(dir_to_copy_from, dir_to_copy_to)
    refresh_dropdown()
    refresh_input_box()


main_dropdown = ft.Dropdown()


def add_settings_management_row(page: ft.Page):
    global main_dropdown
    options = [
        ft.dropdown.Option(get_settings_path_suffix_from_full_path(string_path))
        for string_path in settings.get_settings_files_list_from_tempo_gui_settings()
    ]
    dropdown = ft.Dropdown(
        options=options,
        border_color=ft.Colors.BLUE_GREY_500,
        text_size=12,
        value=get_settings_path_suffix_from_full_path(
            pathlib.Path(get_current_settings_path())
        ),
        expand=True,
        on_change=drop_down_selection_changed,
        border_width=1,
        border_radius=3,
    )

    main_dropdown = dropdown

    minus_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.REMOVE, on_click=minus_button_clicked, icon_color="red"
        ),
        border=ft.border.all(1, "red"),
        border_radius=3,
        padding=3,
    )

    plus_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ADD, on_click=add_button_clicked, icon_color="green"
        ),
        border=ft.border.all(1, "green"),
        border_radius=3,
        padding=3,
    )

    row = ft.Row(
        controls=[dropdown, minus_button, plus_button],
        alignment=ft.MainAxisAlignment.START,
        spacing=4,
    )

    page.add(row)


def add_open_settings_and_open_latest_log_row(page: ft.Page):
    add_button_row(
        page,
        {
            "Open Settings": lambda e: os.startfile(get_current_settings_path()),
            "Open Latest Log": lambda e: tempo_core.main_logic.open_latest_log(),
        },
    )


def add_log_section(page: ft.Page):
    log_text = ft.Text(
        value="Log:",
        text_align=ft.TextAlign.CENTER,
        size=14,
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
    )

    log_text_scroll_box = ft.ListView(expand=True, auto_scroll=True)
    logger.Logger.init_logger(logging_scroll_box=log_text_scroll_box)
    import log_thread

    log_thread.init_log_thread()

    main_log_row = ft.Row(controls=[log_text], alignment=ft.MainAxisAlignment.START)
    divider = ft.Divider(thickness=1, color=ft.Colors.BLUE_GREY_500, height=0)
    column = ft.Column(
        controls=[main_log_row, divider, log_text_scroll_box],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        spacing=4,
    )

    log_container = ft.Container(
        bgcolor=ft.Colors.BLUE_GREY_900,
        content=column,
        border=ft.border.all(1, ft.Colors.BLUE_GREY),
        border_radius=3,
        expand=True,
        margin=0,
        padding=8,
        alignment=ft.alignment.top_left,
    )

    page.add(log_container)


def add_header(page: ft.Page):
    global is_web

    header_text = settings.get_app_title()

    if is_web:
        header = ft.Text(
            header_text,
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        row = ft.Row(
            controls=[header], alignment=ft.MainAxisAlignment.CENTER, height=32
        )
        page.add(row)


def main(page: ft.Page):
    initialization.init()
    page.window.resizable = get_should_be_resizable()
    page.window.maximizable = get_should_be_maximizable()
    page.window.width = settings.get_preferred_app_size()[0]
    page.window.height = settings.get_preferred_app_size()[1]
    page.window.left = settings.get_preferred_app_position()[0]
    page.window.top = settings.get_preferred_app_position()[1]
    page.title = settings.get_app_title()
    page.expand = True
    page.spacing = 6

    def on_resize(e):
        settings.save_preferred_app_position(
            x_position=page.window.left, y_position=page.window.top
        )
        settings.save_preferred_app_size(
            width=page.window.width, height=page.window.height
        )

    page.window.on_event = on_resize

    page.on_resized = on_resize

    page.update()

    global original_webbrowser_open
    webbrowser.open = original_webbrowser_open

    add_header(page)
    add_google_and_youtube_row(page)
    add_github_and_unreal_docs_row(page)
    add_stove_and_spaghetti_row(page)
    add_uasset_gui_and_kismet_analyzer_row(page)
    add_umodel_and_fmodel_row(page)
    add_ide_and_blender_row(page)
    add_game_paks_dir_and_game_exe_dir_row(page)
    add_tempo_dir_and_persistent_mods_dir_row(page)
    add_test_mods_all_and_run_game_row(page)
    add_open_settings_and_open_latest_log_row(page)
    add_settings_path_row(page)
    add_settings_management_row(page)
    add_log_section(page)


assets_dir = os.path.normpath(f"{file_io.SCRIPT_DIR}/assets")

is_web = True

if "--use_browser" in sys.argv:
    if "--browser_port" in sys.argv:
        index = sys.argv.index("--browser_port")
        browser_port = int(sys.argv[index + 1])
        if "--skip_opening_in_browser" in sys.argv:
            webbrowser.open = lambda url, *args, **kwargs: print()
        ft.app(
            main, view=ft.AppView.WEB_BROWSER, port=browser_port, assets_dir=assets_dir
        )
    else:
        ft.app(main, view=ft.AppView.WEB_BROWSER, assets_dir=assets_dir)
else:
    is_web = False
    ft.app(main, assets_dir=assets_dir)
