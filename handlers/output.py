import sys
import os


if sys.platform == "linux" or sys.platform == "linux2":
    clear = lambda: os.system("clear")
elif sys.platform == "win32":
    clear = lambda: os.system("cls")


def fast_rewrite(text: str, height: int) -> None:
    sys.stdout.write("\033[F" * height * 10 + text)
    sys.stdout.flush()