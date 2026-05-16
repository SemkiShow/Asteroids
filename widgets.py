# Based on my GUI library: [RayUI](https://github.com/SemkiShow/RayUI)

from camera import camera, Colors
from input import is_key_pressed
from utils import *
from typing import Callable


def _clamp_axis(val: float, min_val: float, max_val: float) -> float:
    if min_val < 0:
        return val
    if max_val < 0:
        return max(min_val, val)
    if val < 0:
        return max_val
    return min(max_val, val)


def _clamp_bounds(bounds: Rec, min_size: Vec2, max_size: Vec2):
    return Rec(
        bounds.x,
        bounds.y,
        _clamp_axis(bounds.width, min_size.x, max_size.x),
        _clamp_axis(bounds.height, min_size.y, max_size.y),
    )


def _add_margin(bounds: Rec, margin: float):
    return Rec(
        bounds.x + margin, bounds.y + margin, bounds.width - margin * 2, bounds.height - margin * 2
    )


class Widget:
    # Negative axis value means that the widget can expand in that axis
    bounds: Rec = Rec(0, 0, -1, -1)
    min_size: Vec2 = Vec2(1, 1)
    max_size: Vec2 = Vec2(-1, -1)
    visible: bool = True
    disabled: bool = False
    highlighted: bool = False
    color: str = Colors.RESET

    _update_bounds: bool = True
    _is_clicked: bool = False

    def update_bounds(self):
        self._update_bounds = True

    def reset_events(self):
        self._is_clicked = False

    def poll_events(self) -> bool:
        if not self.highlighted:
            return False

        self._is_clicked = is_key_pressed("ENTER")
        return True

    def shrink(self):
        pass

    def update(self):
        if self._update_bounds:
            self._update_bounds = False
            self.bounds = _clamp_bounds(self.bounds, self.min_size, self.max_size)

    def draw(self):
        pass


class Label(Widget):
    _text: str

    def set_text(self, text: str):
        self._text = text
        self.update_bounds()

    def get_text(self):
        return self._text

    def __init__(self, text: str):
        super().__init__()
        self.set_text(text)

    def draw(self):
        camera.draw_text(self.bounds.get_pos(), self._text, self.color, world_pos=False)


class Layout(Widget):
    _margin: float = 0
    _padding: float = 1
    _widgets: list[Widget] = []

    def set_margin(self, margin: float):
        self._margin = margin
        self.update_bounds()

    def get_margin(self):
        return self._margin

    def set_padding(self, padding: float):
        self._padding = padding
        self.update_bounds()

    def get_padding(self):
        return self._padding

    def add_widget(self, widget: Widget):
        self._widgets.append(widget)

    def clear_widgets(self):
        self._widgets.clear()

    def reset_events(self):
        for widget in self._widgets:
            widget.reset_events()
        super().reset_events()

    def poll_events(self) -> bool:
        for widget in self._widgets:
            if widget.poll_events():
                return True
        return super().poll_events()

    def update(self):
        if self._update_bounds:
            self._update_bounds = False
            self.bounds = _clamp_bounds(self.bounds, self.min_size, self.max_size)

            for widget in self._widgets:
                widget.update_bounds()

        for widget in self._widgets:
            if widget.visible:
                widget.update()

    def draw(self):
        super().draw()
        for widget in self._widgets:
            if widget.visible:
                widget.draw()


class VBoxLayout(Layout):
    def shrink(self):
        # Not implemented yet
        return super().shrink()

    def update(self):
        if not self._update_bounds:
            for widget in self._widgets:
                widget.update()
            return

        fixed_height: float = 0
        visible_count: int = 0
        dynamic_count: int = 0
        for widget in self._widgets:
            if widget.visible:
                if widget.max_size.y < 0:
                    dynamic_count += 1
                else:
                    fixed_height += widget.max_size.y
                visible_count += 1

        if visible_count <= 0:
            return

        dynamic_height: float = (
            self.bounds.height
            - 2 * self._margin
            - (visible_count - 1) * self._padding
            - fixed_height
        )

        max_width: float = self.bounds.width - 2 * self._margin
        pos: Vec2 = _add_margin(self.bounds, self._margin).get_pos()
        for widget in self._widgets:
            widget.update_bounds()
            if not widget.visible:
                continue

            widget.bounds.x = pos.x
            widget.bounds.y = pos.y

            widget.bounds.width = round(max_width)

            if widget.max_size.y < 0:
                widget.bounds.height = round(dynamic_height / dynamic_count)
            else:
                widget.bounds.height = round(widget.max_size.y)

            widget.update()

            pos.y += widget.bounds.height + self._padding

            if widget.max_size.y < 0:
                dynamic_height -= widget.bounds.height
                dynamic_count -= 1

        self.shrink()


class HBoxLayout(Layout):
    def shrink(self):
        # Not implemented yet
        return super().shrink()

    def update(self):
        if not self._update_bounds:
            for widget in self._widgets:
                widget.update()
            return

        fixed_width: float = 0
        visible_count: int = 0
        dynamic_count: int = 0
        for widget in self._widgets:
            if widget.visible:
                if widget.max_size.x < 0:
                    dynamic_count += 1
                else:
                    fixed_width += widget.max_size.x
                visible_count += 1

        if visible_count <= 0:
            return

        dynamic_width: float = (
            self.bounds.width - 2 * self._margin - (visible_count - 1) * self._padding - fixed_width
        )

        max_height: float = self.bounds.height - 2 * self._margin
        pos: Vec2 = _add_margin(self.bounds, self._margin).get_pos()
        for widget in self._widgets:
            widget.update_bounds()
            if not widget.visible:
                continue

            widget.bounds.x = pos.x
            widget.bounds.y = pos.y

            if widget.max_size.x < 0:
                widget.bounds.width = round(dynamic_width / dynamic_count)
            else:
                widget.bounds.width = round(widget.max_size.x)

            widget.bounds.height = round(max_height)

            widget.update()

            pos.x += widget.bounds.width + self._padding

            if widget.max_size.x < 0:
                dynamic_width -= widget.bounds.width
                dynamic_count -= 1

        self.shrink()


class Container(Widget):
    _margin: float = 0
    _widget: Widget | None = None

    def set_margin(self, margin: float):
        self._margin = margin
        self.update_bounds()

    def get_margin(self):
        return self._margin

    def set_widget(self, widget: Widget):
        self._widget = widget
        self.update_bounds()

    def unset_widget(self):
        self._widget = None
        self.update_bounds()

    def reset_events(self):
        if self._widget:
            self._widget.reset_events()
        return super().reset_events()

    def poll_events(self) -> bool:
        if self._widget and self._widget.visible:
            if self._widget.poll_events():
                return True
        return super().poll_events()

    def update(self):
        if self._update_bounds:
            self._update_bounds = False
            self.bounds = _clamp_bounds(self.bounds, self.min_size, self.max_size)

            if self._widget:
                self._widget.bounds = _add_margin(self.bounds, self._margin)
                self._widget.update_bounds()

        if self._widget and self._widget.visible:
            self._widget.update()

    def draw(self):
        super().draw()
        if self._widget and self._widget.visible:
            self._widget.draw()


class Event:
    event: Callable[[], bool]
    func: Callable[[], None]

    def __init__(self, event: Callable[[], bool], func: Callable[[], None]):
        self.event = event
        self.func = func


class Window(Container):
    _events: list[Event] = []

    def __init__(self):
        super().__init__()
        self.visible = False

    def connect(self, event: Callable[[], bool], func: Callable[[], None]):
        self._events.append(Event(event, func))

    def update(self):
        super().update()

        for event in self._events:
            if event.event():
                event.func()


class Application:
    _update_bounds: bool = True
    _windows: list[Window] = []

    def update_bounds(self):
        self._update_bounds = False
        for window in self._windows:
            window.update_bounds()

    def add_window(self, window: Window):
        self._windows.append(window)
        self.update_bounds()

    def update(self):
        if self._update_bounds:
            self._update_bounds = False
            terminal_size = camera.get_terminal_size()
            for window in self._windows:
                if window.max_size.x < 0:
                    window.bounds.width = terminal_size.x
                if window.max_size.y < 0:
                    window.bounds.height = terminal_size.y
                window.update_bounds()

        for window in self._windows:
            window.reset_events()
        for window in self._windows[::-1]:
            if window.poll_events():
                break

        for window in self._windows:
            if window.visible:
                window.update()

    def draw(self):
        for window in self._windows:
            if window.visible:
                window.draw()
