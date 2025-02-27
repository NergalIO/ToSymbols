import os


def current_size() -> tuple[int, int]:
    return os.get_terminal_size().lines, os.get_terminal_size().columns


def resize(new_lines: int, new_columns: int) -> None:
    os.system(f"mode {new_lines},{new_columns}")