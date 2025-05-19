import flet as ft


class Logger:
    _log_view: ft.ListView

    @classmethod
    def init_logger(cls, logging_scroll_box: ft.ListView):
        cls._log_view = logging_scroll_box

    @classmethod
    def log_message(cls, message: str):
        if cls._log_view:
            cls._log_view.controls.append(ft.Text(value=message, size=12))
            cls._log_view.update()
        else:
            accessed_logger_early_error = (
                "You attempted to print to the scroll box log before it was initiated"
            )
            raise RuntimeError(accessed_logger_early_error)
