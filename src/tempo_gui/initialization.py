import os
import sys
import threading

import tempo_core
import tempo_core.initialization

from tempo_gui import settings
from tempo_gui import local_tempo as tempo_gui_tempo


has_completed_tempo_init = False


def run_tempo_init():
    global has_completed_tempo_init
    tempo_core.initialization.initialization()
    has_completed_tempo_init = True
    print("Tempo init completed.")


def check_presets_dir_exists():
    assets_dir = tempo_gui_tempo.get_tempo_gui_assets_directory()
    assets_dir_missing_error = "The assets directory next to the exe is missing."
    if not os.path.isdir(assets_dir):
        raise IsADirectoryError(assets_dir_missing_error)


def init():
    check_presets_dir_exists()
    settings.init_settings()
    settings.get_current_tempo_settings_file()

    sys.argv.append("--settings_json")
    sys.argv.append(str(settings.get_current_tempo_settings_file()))

    threading.Thread(target=run_tempo_init, daemon=True).start()
