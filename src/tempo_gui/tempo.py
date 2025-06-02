import os
import pathlib
import requests

from tempo_gui import file_io


def get_latest_tempo_version() -> str:
    api_url = "https://api.github.com/repos/Tempo-Organization/tempo/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    return ""


def get_latest_64_bit_windows_release_download_link() -> str:
    latest_tempo_version = get_latest_tempo_version()
    if latest_tempo_version == "":
        raise RuntimeError("Could not grab latest tempo tag")
    base_link = "https://github.com/Tempo-Organization/tempo/releases/latest/download"
    latest_download_link = (
        f"{base_link}/tempo-x86-64-pc-windows-msvc-{latest_tempo_version}.zip"
    )
    return latest_download_link


def get_tempo_gui_assets_directory() -> pathlib.Path:
    return pathlib.Path(os.path.normpath(f"{file_io.SCRIPT_DIR}/assets"))


def get_tempo_exe_path() -> pathlib.Path:
    return pathlib.Path(
        os.path.normpath(f"{get_tempo_gui_assets_directory()}/tempo/tempo.exe")
    )


def get_tempo_headless_exe_path() -> pathlib.Path:
    return pathlib.Path(
        os.path.normpath(f"{get_tempo_gui_assets_directory()}/tempo/tempo_headless.exe")
    )


def get_tempo_preset_template_dir() -> pathlib.Path:
    return pathlib.Path(
        os.path.normpath(f"{get_tempo_gui_assets_directory()}/preset_template")
    )


def get_default_preset_directory() -> pathlib.Path:
    return pathlib.Path(os.path.normpath(f"{file_io.SCRIPT_DIR}/presets/default"))
