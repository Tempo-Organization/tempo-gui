import os
import sys
import time
import shutil
import pathlib
import tomlkit
import platform
from screeninfo import get_monitors

from tempo_gui import file_io, tempo


has_inited_settings = False

SETTINGS_FILE = os.path.normpath(f"{file_io.SCRIPT_DIR}/settings.toml")


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


def is_exe():
    return getattr(sys, "frozen", False) and os.path.isfile(sys.executable)


def make_settings_file():
    settings = {"blender_path": "", "ide_path": ""}

    toml_str = tomlkit.dumps(settings)

    if os.path.isdir(str(tempo.get_default_preset_directory())):
        shutil.rmtree(str(tempo.get_default_preset_directory()))

    with open(SETTINGS_FILE, "w") as f:
        f.write(toml_str)
    # logger.Logger.log_message(f"Settings file created at {SETTINGS_FILE}")


def to_toml_value(value):
    if isinstance(value, dict):
        table = tomlkit.table()
        for k, v in value.items():
            table[k] = to_toml_value(v)
        return table
    elif isinstance(value, list):
        if all(isinstance(i, dict) for i in value):
            aot = tomlkit.aot()
            for item in value:
                aot.append(to_toml_value(item))
            return aot
        else:
            return value
    else:
        return value


def to_pretty_toml(data: dict):
    table = tomlkit.table()
    for key, value in data.items():
        table[key] = to_toml_value(value)
    return table


def save_settings(settings_dictionary: dict):
    pretty_data = to_pretty_toml(settings_dictionary)
    toml_str = tomlkit.dumps(pretty_data)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(toml_str)

    # logger.Logger.log_message(f"Settings saved to {SETTINGS_FILE}")


def init_settings():
    global has_inited_settings
    if not os.path.isfile(SETTINGS_FILE):
        make_settings_file()

    has_inited_settings = True
    # logger.Logger.log_message(f"Settings initialized from {SETTINGS_FILE}")


def get_settings() -> tomlkit.TOMLDocument:
    if not os.path.isfile(SETTINGS_FILE):
        # logger.Logger.log_message(f"Settings file {SETTINGS_FILE} does not exist!")
        raise FileNotFoundError("Missing settings file.")

    with open(SETTINGS_FILE, "r") as f:
        settings_data = tomlkit.load(f)

    return settings_data


def get_default_settings_path() -> pathlib.Path:
    return pathlib.Path(
        os.path.normpath(f"{tempo.get_default_preset_directory()}/settings.json")
    )


def set_current_tempo_settings_file(settings_path: pathlib.Path):
    local_settings = get_settings()
    local_settings["current_settings_file"] = str(settings_path)
    add_settings_files_to_list(local_settings, [pathlib.Path(settings_path)])
    save_settings(local_settings)


def create_initial_tempo_settings():
    if os.path.isdir(tempo.get_default_preset_directory()):
        shutil.rmtree(tempo.get_default_preset_directory())
    shutil.copytree(
        tempo.get_tempo_preset_template_dir(),
        tempo.get_default_preset_directory(),
    )
    set_current_tempo_settings_file(get_default_settings_path())


def get_current_tempo_settings_file() -> pathlib.Path:
    default_settings_file_path = str(get_default_settings_path())
    file_path = get_settings().get("current_settings_file", default_settings_file_path)
    if (
        file_path == default_settings_file_path
        and not os.path.isfile(default_settings_file_path)
    ) or (not os.path.isfile(file_path) and file_path != default_settings_file_path):
        create_initial_tempo_settings()

    return pathlib.Path(file_path)


def add_settings_files_to_list(
    settings: tomlkit.TOMLDocument, settings_paths: list[pathlib.Path]
) -> None:
    settings_files = settings.get("settings_files", [])

    for settings_path in settings_paths:
        path_str = str(settings_path)
        if path_str not in settings_files:
            settings_files.append(path_str)

    settings["settings_files"] = settings_files
    save_settings(settings)


def remove_settings_files_from_list(
    settings: tomlkit.TOMLDocument, settings_paths: list[pathlib.Path]
) -> None:
    settings_files = settings.get("settings_files", [])

    settings_files = [
        path for path in settings_files if path not in {str(p) for p in settings_paths}
    ]

    settings["settings_files"] = settings_files
    save_settings(settings)


def get_settings_files_list_from_tempo_gui_settings() -> list[pathlib.Path]:
    return [
        pathlib.Path(string_path)
        for string_path in get_settings().get("settings_files", [])
        if pathlib.Path(string_path).is_file()
    ]


def get_ide_path_from_settings() -> str:
    return get_settings().get("ide_path", "")


def get_blender_path_from_settings() -> str:
    return get_settings().get("blender_path", "")


def get_default_width() -> float:
    return 420.0


def get_default_height() -> float:
    return 600.0


def get_default_app_position(title: str) -> tuple[int, int]:
    time.sleep(0.01)
    try:
        win_width = 800
        win_height = 600

        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        screen_x = monitor.x
        screen_y = monitor.y

        x = screen_x + (screen_width - win_width) // 2
        y = screen_y + (screen_height - win_height) // 2

        return (x, y)
    except Exception:
        return (480, 240)


def save_preferred_app_position(x_position: float | None, y_position: float | None):
    settings = get_settings()
    settings.update({"app_x_position": x_position, "app_y_position": y_position})
    save_settings(settings)


def save_preferred_app_size(width: float | None, height: float | None):
    settings = get_settings()
    settings.update({"app_width": width, "app_height": height})
    save_settings(settings)


def get_app_title() -> str:
    return "Tempo GUI"


def get_preferred_app_position() -> tuple[float | None, float | None]:
    loaded_settings = get_settings()
    x_position = loaded_settings.get(
        "app_x_position", get_default_app_position(get_app_title())[0]
    )
    y_position = loaded_settings.get(
        "app_y_position", get_default_app_position(get_app_title())[1]
    )
    return (x_position, y_position)


def get_preferred_app_size() -> tuple[float | None, float | None]:
    loaded_settings = get_settings()
    width = loaded_settings.get("app_width", get_default_width())
    height = loaded_settings.get("app_height", get_default_height())
    return (width, height)
