"""A simple immediate mode TUI library"""

from camera import camera, Colors
from input import Key, get_last_pressed_key, is_key_pressed
from utils import *
from enum import Enum, auto


class Align(Enum):
    Left = auto()
    Center = auto()
    Right = auto()


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
        self._active_idx = -1
        self._total_widgets = 0

    def set_visible(self, visible: bool):
        self._visible = visible
        self._selected_idx = 0
        self._active_idx = -1
        self.reset()

    def is_visible(self):
        return self._visible

    def reset(self):
        self.active = False
        self._total_widgets = 0

    def is_selected(self, idx: int):
        return idx == self._selected_idx

    def is_active(self, idx: int):
        return idx == self._active_idx

    def toggle_active(self, idx: int):
        if self._active_idx == idx:
            self._active_idx = -1
        else:
            self._active_idx = idx

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
        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, measure_text(text).x, align, parent_width)
        camera.draw_text(new_pos, text, color, world_pos=False)

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

        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, measure_text(text).x, align, parent_width)

        camera.draw_text(
            new_pos,
            text,
            selected_color if self.is_selected(idx) else idle_color,
            world_pos=False,
        )

        return self.active and self.is_selected(idx) and is_key_pressed(Key.Enter)

    def dropdown(
        self,
        pos: Vec2,
        items: list[str],
        item_idx: int,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        active_color: str = Colors.BG_BLUE,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> int:
        idx = self._total_widgets
        self._total_widgets += 1

        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, measure_text(items[item_idx]).x, align, parent_width)

        selected = self.is_selected(idx)
        active = self.is_active(idx)
        if active:
            self.active = False

        color = idle_color
        if selected:
            color = selected_color
        if active:
            color = active_color
        camera.draw_text(new_pos, items[item_idx], color, world_pos=False)

        if selected:
            if is_key_pressed(Key.Enter):
                self.toggle_active(idx)

            if active:
                if is_key_pressed(Key.Up):
                    item_idx -= 1
                if is_key_pressed(Key.Down):
                    item_idx += 1
                if item_idx < 0:
                    item_idx = 0
                if item_idx >= len(items):
                    item_idx = len(items) - 1

        return item_idx

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

        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, width, align, parent_width)

        selected = self.is_selected(idx)

        draw_text = text + " " * max(0, width - len(text))
        camera.draw_text(
            new_pos,
            draw_text[-width:],
            (selected_color if selected else idle_color) + Colors.UNDERLINE,
            world_pos=False,
        )

        if selected:
            key = get_last_pressed_key()
            if key:
                if len(key) == 1 and key.isprintable():
                    text += key
            if is_key_pressed(Key.Backspace):
                text = text[:-1]

        return text

    def slider(
        self,
        pos: Vec2,
        val: int,
        min_val: int,
        max_val: int,
        step_size: int = -1,
        width: int = 20,
        show_value: bool = True,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        active_color: str = Colors.BG_BLUE,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> int:
        idx = self._total_widgets
        self._total_widgets += 1

        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, width, align, parent_width)

        selected = self.is_selected(idx)
        active = self.is_active(idx)
        if active:
            self.active = False

        text = list("-" * width)
        handle_pos = round((val - min_val) / (max_val - min_val) * width)
        text[clamp(handle_pos, 0, width - 1)] = "+"
        text = "".join(text)

        color = idle_color
        if selected:
            color = selected_color
        if active:
            color = active_color
        camera.draw_text(new_pos, text, color, world_pos=False)

        if show_value:
            new_pos.x += width + 1
            camera.draw_text(new_pos, str(val), idle_color, world_pos=False)

        if selected:
            if is_key_pressed(Key.Enter):
                self.toggle_active(idx)

            if active:
                if step_size <= 0:
                    step_size = math.ceil((max_val - min_val) / width)
                if is_key_pressed(Key.Left):
                    val -= step_size
                if is_key_pressed(Key.Right):
                    val += step_size

        if val < min_val:
            val = min_val
        if val > max_val:
            val = max_val

        return val

    def checkbox(
        self,
        pos: Vec2,
        val: bool,
        idle_color: str = Colors.RESET,
        selected_color: str = Colors.INVERTED,
        align: Align = Align.Left,
        parent_width: float = 0,
    ) -> bool:
        idx = self._total_widgets
        self._total_widgets += 1

        text = "[" + ("X" if val else " ") + "]"
        new_pos = Vec2(pos.x, pos.y)
        apply_align(new_pos, len(text), align, parent_width)

        selected = self.is_selected(idx)

        color = idle_color
        if selected:
            color = selected_color
        camera.draw_text(new_pos, text, color, world_pos=False)

        if selected:
            if is_key_pressed(Key.Enter):
                val = not val

        return val

    def update(self):
        pass

    def poll_events(self):
        if not self.active:
            return

        if is_key_pressed(Key.Up):
            self._selected_idx -= 1
        if is_key_pressed(Key.Down):
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
