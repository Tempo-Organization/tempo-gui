import os
import time
import threading

import tempo_core
import tempo_core.logger
import tempo_core.file_io
import logger


log_path = os.path.normpath(
    f"{tempo_core.file_io.SCRIPT_DIR}/logs/{tempo_core.logger.log_information.log_prefix}_latest.log"
)


def ensure_log_file_exists():
    log_dir = os.path.dirname(log_path)
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(log_path):
        open(log_path, "a", encoding="utf-8").close()


def monitor_log():
    ensure_log_file_exists()
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    logger.Logger.log_message(line.rstrip())
                else:
                    time.sleep(0.1)
    except Exception as e:
        logger.Logger.log_message(f"[Log Monitor] Error: {e}")


def init_log_thread():
    log_thread = threading.Thread(target=monitor_log, daemon=True)
    log_thread.start()
