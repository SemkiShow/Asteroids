from os import sendfile
from camera import camera, Colors
from input import get_last_pressed_ley, is_key_pressed
from utils import *


def measure_text(text: str):
    size = Vec2(0, 0)
    for line in text.split("\n"):
        size.x = max(size.x, len(line))
    size.y = text.count("\n") + 1
    return size


class Window:
    def __init__(self):
        self.visible = False
        self.active = False

        self._selected_idx = 0
        self._total_widgets = 0

    def reset(self):
        self.active = False
        self._total_widgets = 0

    def selected(self, idx: int):
        return idx == self._selected_idx

    def label(self, pos: Vec2, text: str, color: str = Colors.RESET):
        camera.draw_text(pos, text, color, world_pos=False)

    def button(self, pos: Vec2, text: str) -> bool:
        idx = self._total_widgets
        self._total_widgets += 1

        camera.draw_text(
            pos,
            text,
            Colors.BG_WHITE + Colors.BLACK if self.selected(idx) else Colors.RESET,
            world_pos=False,
        )

        return self.active and self.selected(idx) and is_key_pressed("ENTER")

    def dropdown(
        self, pos: Vec2, items: list[str], item_idx: int, active: bool
    ) -> tuple[int, bool]:
        idx = self._total_widgets
        self._total_widgets += 1

        selected = self.selected(idx)
        if active:
            self.active = False

        color = Colors.RESET
        if selected:
            color = Colors.BG_WHITE + Colors.BLACK
        if active:
            color = Colors.BG_CYAN
        camera.draw_text(pos, items[item_idx], color, world_pos=False)

        if selected:
            if is_key_pressed("ENTER"):
                active = not active

            if active:
                if is_key_pressed("UP"):
                    item_idx -= 1
                if is_key_pressed("DOWN"):
                    item_idx += 1
                if item_idx < 0:
                    item_idx = 0
                if item_idx >= len(items):
                    item_idx = len(items) - 1

        return (item_idx, active)

    def input_field(self, pos: Vec2, text: str) -> str:
        idx = self._total_widgets
        self._total_widgets += 1

        selected = self.selected(idx)

        MAX_WIDTH = 20
        draw_text = text + "_" * max(0, MAX_WIDTH - len(text))
        camera.draw_text(
            pos,
            draw_text,
            Colors.BG_WHITE + Colors.BLACK if selected else Colors.RESET,
            world_pos=False,
        )

        if selected:
            key = get_last_pressed_ley()
            if key:
                if len(key) == 1 and key.isalnum():
                    text += key
                elif key == "BACKSPACE":
                    text = text[:-1]

        return text

    def update(self):
        pass

    def poll_events(self):
        if not self.active:
            return

        if is_key_pressed("UP"):
            self._selected_idx -= 1
        if is_key_pressed("DOWN"):
            self._selected_idx += 1
        if self._selected_idx < 0:
            self._selected_idx = 0
        if self._selected_idx >= self._total_widgets:
            self._selected_idx = self._total_widgets - 1

    def draw(self):
        self.poll_events()


class Application:
    def __init__(self):
        self._windows: list[Window] = []

    def add_window(self, window: Window):
        self._windows.append(window)

    def frame(self):
        for window in self._windows:
            window.reset()

        for window in self._windows[::-1]:
            if window.visible:
                window.active = True
                break

        for window in self._windows:
            if window.visible:
                window.update()
                window.draw()
