from camera import camera, Colors
from input import is_key_pressed
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

    def update(self):
        pass

    def poll_events(self):
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
        self._update_bounds: bool = True
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
