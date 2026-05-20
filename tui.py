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

    def dropdown(
        self, pos: Vec2, items: list[str], current_idx: int, active: bool
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
        camera.draw_text(pos, items[current_idx], color, world_pos=False)

        next_idx = current_idx
        next_active = active

        if selected:
            if is_key_pressed("ENTER"):
                next_active = not next_active

            if active:
                max_width = max(len(item) for item in items)
                pos.y += 1
                for i, item in enumerate(items):
                    text = item + " " * (max_width - len(item))
                    camera.draw_text(
                        pos,
                        text,
                        Colors.BG_WHITE + Colors.BLACK if i == current_idx else Colors.RESET,
                        world_pos=False,
                    )
                    pos.y += 1

                if is_key_pressed("UP"):
                    next_idx -= 1
                if is_key_pressed("DOWN"):
                    next_idx += 1
                if next_idx < 0:
                    next_idx = 0
                if next_idx >= len(items):
                    next_idx = len(items) - 1

        return (next_idx, next_active)

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
