from camera import camera
import sys, os

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


def get_key():
    char = get_char()

    if char is None:
        return char

    if ord(char) in (10, 13):
        return "ENTER"

    if os.name == "nt":
        if ord(char) == 27:
            return "ESC"
        if ord(char) == 72:
            return "UP"
        if ord(char) == 75:
            return "LEFT"
        if ord(char) == 77:
            return "RIGHT"
        if ord(char) == 80:
            return "DOWN"
    else:
        if ord(char) == 27:
            char = get_char()
            if char is None:
                return "ESC"
            if ord(char) == 91:
                char = get_char()
                if char == "A":
                    return "UP"
                if char == "B":
                    return "DOWN"
                if char == "C":
                    return "RIGHT"
                if char == "D":
                    return "LEFT"
                return None
            return None

    return char


_keys: list[str] = []


def poll_events():
    key = get_key()
    while key:
        _keys.append(key)
        key = get_key()


def reset_events():
    _keys.clear()


def is_key_pressed(key: str):
    return key in _keys
