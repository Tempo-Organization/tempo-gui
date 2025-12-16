from __future__ import annotations

import os
import subprocess

from tempo_gui import file_io
from tempo_core.data_structures import ExecutionMode
from tempo_gui import logger


def run_app(
    exe_path: str,
    exec_mode: ExecutionMode = ExecutionMode.SYNC,
    args: list[str] | None = None,
    temp_dir: str = os.path.normpath(f"{file_io.SCRIPT_DIR}/working_dir"),
):
    os.makedirs(temp_dir, exist_ok=True)

    if not args:
        args = []
    exe_path = file_io.ensure_path_quoted(exe_path)

    if exec_mode == ExecutionMode.SYNC:
        command = exe_path
        for arg in args:
            command = f"{command} {arg}"
        # logger.Logger.log_message("----------------------------------------------------")
        logger.Logger.log_message(f"Command: main executable: {exe_path}")
        for arg in args:
            logger.Logger.log_message(f"Command: arg: {arg}")
        # logger.Logger.log_message("----------------------------------------------------")
        logger.Logger.log_message(
            f"Command: {command} running with the {exec_mode} enum"
        )
        if temp_dir and os.path.isdir(temp_dir):
            os.chdir(temp_dir)

        process = subprocess.Popen(
            command,
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                logger.Logger.log_message(line.strip())

            process.stdout.close()

        process.wait()
        logger.Logger.log_message(f"Command: {command} finished")

    elif exec_mode == ExecutionMode.ASYNC:
        command = exe_path
        for arg in args:
            command = f"{command} {arg}"
        logger.Logger.log_message(
            f"Command: {command} started with the {exec_mode} enum"
        )
        subprocess.Popen(command, cwd=temp_dir, start_new_session=True)
