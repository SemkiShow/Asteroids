from camera import camera
import sys, os
from enum import Enum

if os.name != "nt":
    import tty, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)


def prepare_terminal():
    camera.hide_cursor()
    if os.name == "nt":
        os.system("")
    else:
        tty.setcbreak(fd)


def restore_terminal():
    if os.name != "nt":
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    camera.show_cursor()


def get_char():
    if os.name == "nt":
        import msvcrt

        if msvcrt.kbhit():
            char = msvcrt.getch().decode("utf-8", errors="ignore")
            return char if char else None
        return None
    else:
        import select

        if select.select([fd], [], [], 0)[0]:
            return os.read(fd, 1).decode("utf-8", errors="ignore")
        return None


class Key(Enum):
    Enter = 0
    Backspace = 1
    Escape = 2
    Up = 3
    Down = 4
    Right = 5
    Left = 6


def get_key():
    char = get_char()

    if char is None:
        return char

    if ord(char) in (10, 13):
        return Key.Enter

    if os.name == "nt":
        if ord(char) == 8:
            return Key.Backspace
        if ord(char) == 27:
            return Key.Escape
        if ord(char) == 72:
            return Key.Up
        if ord(char) == 75:
            return Key.Left
        if ord(char) == 77:
            return Key.Right
        if ord(char) == 80:
            return Key.Down
    else:
        if ord(char) == 27:
            char = get_char()
            if char is None:
                return Key.Escape
            if ord(char) == 91:
                char = get_char()
                if char == "A":
                    return Key.Up
                if char == "B":
                    return Key.Down
                if char == "C":
                    return Key.Right
                if char == "D":
                    return Key.Left
                return None
            return None
        if ord(char) == 127:
            return Key.Backspace

    return char


_keys: list[str] = []


def poll_events():
    key = get_key()
    while key:
        _keys.append(str(key))
        key = get_key()


def reset_events():
    _keys.clear()


def is_key_pressed(key: str | Key):
    return str(key) in _keys


def get_last_pressed_ley() -> str | None:
    return None if len(_keys) == 0 else _keys[-1]
