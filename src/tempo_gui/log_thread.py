import os
import time
import threading

import tempo_core
import tempo_core.logger
import tempo_core.file_io
from tempo_gui import logger


log_path = os.path.normpath(
    f"{tempo_core.file_io.SCRIPT_DIR}/logs/{tempo_core.logger.log_information.log_prefix}_latest.log"
)


def monitor_log():
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    logger.Logger.log_message(line.rstrip())
                else:
                    time.sleep(0.1)
    except FileNotFoundError:
        logger.Logger.log_message(f"[Log Monitor] File not found: {log_path}")
    except Exception as e:
        logger.Logger.log_message(f"[Log Monitor] Error: {e}")


def init_log_thread():
    log_thread = threading.Thread(target=monitor_log, daemon=True)
    log_thread.start()
