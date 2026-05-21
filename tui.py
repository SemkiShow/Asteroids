from os import sendfile
from camera import camera, Colors
from input import get_last_pressed_ley, is_key_pressed
from utils import *
from enum import Enum


def measure_text(text: str):
    size = Vec2(0, 0)
    for line in text.split("\n"):
        size.x = max(size.x, len(line))
    size.y = text.count("\n") + 1
    return size


class Align(Enum):
    Left = 0
    Center = 1
    Right = 2


def apply_align(pos: Vec2, width: float, align: Align, parent_width: float):
    match align:
        case Align.Left:
            pass
        case Align.Center:
            pos.x = max(pos.x, pos.x + (parent_width - width) / 2)
        case Align.Right:
            pos.x = max(pos.x, pos.x + (parent_width - width))


class Window:
    def __init__(self):
        self.active = False

        self._visible = False
        self._selected_idx = 0
        self._total_widgets = 0

    def set_visible(self, visible: bool):
        self._visible = visible
        self._selected_idx = 0

    def is_visible(self):
        return self._visible

    def reset(self):
        self.active = False
        self._total_widgets = 0

    def selected(self, idx: int):
        return idx == self._selected_idx

    def has_widgets(self):
        return self._total_widgets > 0

    def label(
        self,
        pos: Vec2,
        text: str,
        color: str = Colors.RESET,
        align: Align = Align.Left,
        parent_width: float = 0,
    ):
        apply_align(pos, measure_text(text).x, align, parent_width)
        camera.draw_text(pos, text, color, world_pos=False)

    def button(
        self,
        pos: Vec2,
        text: str,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> bool:
        idx = self._total_widgets
        self._total_widgets += 1

        apply_align(pos, measure_text(text).x, align, parent_width)

        camera.draw_text(
            pos,
            text,
            selected_color if self.selected(idx) else idle_color,
            world_pos=False,
        )

        return self.active and self.selected(idx) and is_key_pressed("ENTER")

    def dropdown(
        self,
        pos: Vec2,
        items: list[str],
        item_idx: int,
        active: bool,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        active_color: str = Colors.BG_CYAN,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> tuple[int, bool]:
        idx = self._total_widgets
        self._total_widgets += 1

        apply_align(pos, measure_text(items[item_idx]).x, align, parent_width)

        selected = self.selected(idx)
        if active:
            self.active = False

        color = idle_color
        if selected:
            color = selected_color
        if active:
            color = active_color
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

    def input_field(
        self,
        pos: Vec2,
        text: str,
        width: int = 20,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> str:
        idx = self._total_widgets
        self._total_widgets += 1

        apply_align(pos, width, align, parent_width)

        selected = self.selected(idx)

        draw_text = text + "_" * max(0, width - len(text))
        camera.draw_text(
            pos,
            draw_text[-width:],
            selected_color if selected else idle_color,
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

    def update(self):
        active_idx: int = -1
        for i, window in reversed(list(enumerate(self._windows))):
            if window.is_visible() and window.has_widgets():
                active_idx = i
                break
        if active_idx < 0:
            active_idx = len(self._windows) - 1

        for window in self._windows:
            window.reset()

        if active_idx >= 0:
            self._windows[active_idx].active = True

        for window in self._windows:
            if window.is_visible():
                window.update()

    def draw(self):
        for window in self._windows:
            if window.is_visible():
                window.draw()
