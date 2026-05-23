"""Menus and game update"""

from input import Key, is_key_pressed
from game import FieldType, Player, Map, Field
from tui import *
from utils import *
import time, turtle, random, json, os


class ExitSuccess(KeyboardInterrupt): ...


class MainMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        pos = Vec2(0, 0)
        terminal_size = camera.get_terminal_size()

        title = R"""
    _        _                 _     _     
   / \   ___| |_ ___ _ __ ___ (_) __| |___ 
  / _ \ / __| __/ _ \ '__/ _ \| |/ _` / __|
 / ___ \\__ \ ||  __/ | | (_) | | (_| \__ \
/_/   \_\___/\__\___|_|  \___/|_|\__,_|___/"""
        title = title[1:]  # Remove the first newline

        self.label(pos, title, Colors.BOLD, align=Align.Center, parent_width=terminal_size.x)
        pos.y += measure_text(title).y + 2

        if self.button(pos, "Play", align=Align.Center, parent_width=terminal_size.x):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            game_menu.set_visible(True)
            self.set_visible(False)
        pos.y += 2

        if self.button(pos, "Settings", align=Align.Center, parent_width=terminal_size.x):
            settings_menu.set_visible(True)
            self.set_visible(False)
        pos.y += 2

        if self.button(pos, "Exit", align=Align.Center, parent_width=terminal_size.x):
            raise ExitSuccess
        pos.y += 2

        return super().draw()


class SettingsMenu(Window):
    def __init__(self):
        super().__init__()

        parent_vars = set(self.__dict__.keys())

        self.player_name: str = "Player"
        self.difficulty: int = 0
        self.map_size_x: int = 200
        self.map_size_y: int = 200

        self._settings_keys = [k for k in self.__dict__.keys() if k not in parent_vars]

        self.settings_path: str = "settings.json"
        self.difficulties: list[str] = ["Easy", "Medium", "Hard"]
        self.min_map_size: int = 50
        self.max_map_size: int = 500

        self.load()

    def load(self):
        if not os.path.exists(self.settings_path):
            self.save()
            return
        with open(self.settings_path, "r") as file:
            data = json.load(file)
            filtered_data = {k: v for k, v in data.items() if k in self._settings_keys}
            for key, value in filtered_data.items():
                setattr(self, key, value)

    def save(self):
        with open(self.settings_path, "w") as file:
            data = {k: self.__dict__[k] for k in self._settings_keys}
            json.dump(data, file, indent=4)

    def draw(self):
        pos: Vec2 = Vec2(0, 0)
        text_width = 15

        if self.button(pos, "Back"):
            main_menu.set_visible(True)
            self.set_visible(False)
        pos.y += 2

        self.label(pos, "Player name")
        pos.x += text_width
        self.player_name = self.input_field(pos, self.player_name)
        pos.x -= text_width
        pos.y += 2

        self.label(pos, "Difficulty")
        pos.x += text_width
        self.difficulty = self.dropdown(pos, self.difficulties, self.difficulty)
        pos.x -= text_width
        pos.y += 2

        self.label(pos, "Map size X")
        pos.x += text_width
        self.map_size_x = self.slider(pos, self.map_size_x, self.min_map_size, self.max_map_size)
        pos.x -= text_width
        pos.y += 2

        self.label(pos, "Map size Y")
        pos.x += text_width
        self.map_size_y = self.slider(pos, self.map_size_y, self.min_map_size, self.max_map_size)
        pos.x -= text_width
        pos.y += 2

        return super().draw()


class GameMenu(Window):
    def __init__(self):
        super().__init__()

        self.player: Player = Player()
        self.map: Map = Map()

    def set_visible(self, visible: bool):
        if not visible:
            turtle.clearscreen()
        return super().set_visible(visible)

    def map_to_turtle(self, pos: Vec2) -> Vec2:
        return Vec2(
            (pos.x - self.map.size.x / 2),
            (self.map.size.y / 2 - pos.y) / camera.ratio,
        )

    def restart_game(self):
        # Configure map
        asteroids_fill: float = 0.1
        fields_fill: float = 0.025
        match settings_menu.difficulty:
            case 0:
                asteroids_fill = 0.1
                fields_fill = 0.025
            case 1:
                asteroids_fill = 0.5
                fields_fill = 0.05
            case 2:
                asteroids_fill = 1.25
                fields_fill = 0.1
            case _:
                notification_menu.show("Error: invalid diffuculty selected")
                pass
        self.map.restart_game(
            width=settings_menu.map_size_x,
            height=settings_menu.map_size_y,
            asteroids_fill=asteroids_fill,
            fields_fill=fields_fill,
            min_distance=min(settings_menu.map_size_x, settings_menu.map_size_y) / 2,
        )

        self.player.restart_game()
        self.player.pos = Vec2(self.map.player_pos.x, self.map.player_pos.y)
        self.points: int = 0
        self.time: float = 0
        self.frame: int = 0
        self.fields: int = 0

        # Set up the screen
        turtle.tracer(False)
        turtle.speed("fastest")
        turtle.Screen().setup(self.map.size.x * 1.25, self.map.size.y / camera.ratio * 1.25)
        turtle.title("Minimap")
        turtle.clearscreen()

        # Draw goal
        turtle_end_pos = self.map_to_turtle(self.map.end_pos)
        end_pos_size = 10
        turtle.color("green")
        turtle.width(3)
        turtle.penup()
        turtle.goto(turtle_end_pos.x - end_pos_size / 2, turtle_end_pos.y + end_pos_size / 2)
        turtle.pendown()
        turtle.goto(turtle_end_pos.x + end_pos_size / 2, turtle_end_pos.y - end_pos_size / 2)
        turtle.penup()
        turtle.goto(turtle_end_pos.x + end_pos_size / 2, turtle_end_pos.y + end_pos_size / 2)
        turtle.pendown()
        turtle.goto(turtle_end_pos.x - end_pos_size / 2, turtle_end_pos.y - end_pos_size / 2)
        turtle.color("black")
        turtle.width(1)

        # Move to the player position
        turtle.penup()
        self.move_turtle()
        turtle.pendown()

    def move_turtle(self):
        pos = self.map_to_turtle(self.player.pos)
        turtle.goto(pos.x, pos.y)
        turtle.settiltangle(90 - self.player.angle)
        turtle.update()

    def update(self):
        super().update()

        # Don't run game update if some specific menus are open
        if pause_menu.is_visible() or game_over_menu.is_visible() or victory_menu.is_visible():
            return

        if is_key_pressed("a") or is_key_pressed(Key.Left):
            self.player.angle -= 45
        if is_key_pressed("d") or is_key_pressed(Key.Right):
            self.player.angle += 45
        if is_key_pressed(" "):
            self.player.speed += 0.5
        if is_key_pressed(Key.Escape):
            pause_menu.set_visible(True)

        self.player.update()
        self.move_turtle()

        self.time += camera.get_delta_time()
        self.frame += 1

        # Wall collision game over
        player_pos = self.player.get_draw_pos()
        if (
            player_pos.x < 0
            or player_pos.x >= self.map.size.x
            or player_pos.y < 0
            or player_pos.y >= self.map.size.y
        ):
            notification_menu.show("You went out of bounds!")
            game_over_menu.set_visible(True)
            return

        # Asteroid collision game over
        player_pos = camera.get_draw_pos(self.player.get_draw_pos())
        for asteroid in self.map.asteroids:
            asteroid_pos = camera.get_draw_pos(asteroid.pos)
            if asteroid_pos == player_pos:
                notification_menu.show("You hit an asteroid!")
                game_over_menu.set_visible(True)
                return

        # Fuel game over
        if self.player.fuel <= 0:
            notification_menu.show("You ran out of fuel!")
            game_over_menu.set_visible(True)
            return

        # Field collision handling
        collected_fields: list[Field] = []
        for field in self.map.fields:
            field_pos = camera.get_draw_pos(field.pos)
            if field_pos == player_pos:
                collected_fields.append(field)
        for field in collected_fields[::-1]:
            match field.type:
                case FieldType.AddPoints:
                    points = random.randint(10, 50)
                    self.points += points
                    notification_menu.show("Picked up bonus: +" + str(points) + " points")
                case FieldType.Time:
                    seconds = random.randint(10, 30) / 10
                    self.time -= seconds
                    notification_menu.show("Picked up bonus: -" + str(seconds) + "s")
                case FieldType.Fuel:
                    fuel = random.randint(100, 500)
                    self.player.fuel += fuel
                    notification_menu.show("Picked up bonus: +" + str(fuel) + " fuel")
                case FieldType.Speed:
                    speed = random.randint(10, 30) / 10
                    self.player.speed += speed
                    notification_menu.show("Picked up debuff: +" + str(speed) + " speed")
                case FieldType.RemovePoints:
                    points = random.randint(10, 30)
                    self.points -= points
                    notification_menu.show("Picked up debuff: -" + str(points) + " points")
            self.fields += 1
            self.map.fields.remove(field)

        # Target collision victory
        if player_pos == camera.get_draw_pos(self.map.end_pos):
            notification_menu.show("You won!")
            victory_menu.set_visible(True)
            return

    def draw(self):
        self.map.draw()
        self.player.draw()

        pos_text = str(round(self.player.pos.x, 1)) + " " + str(round(self.player.pos.y, 1))

        self.label(Vec2(0, 0), "Player: " + settings_menu.player_name, Colors.YELLOW)
        self.label(Vec2(0, 1), "Position: " + pos_text, Colors.YELLOW)
        self.label(Vec2(0, 2), "Speed: " + str(round(self.player.speed, 1)), Colors.YELLOW)
        self.label(Vec2(0, 3), "Fuel: " + str(round(self.player.fuel, 1)), Colors.YELLOW)
        self.label(Vec2(0, 4), "Points: " + str(self.points), Colors.YELLOW)
        self.label(Vec2(0, 5), "Time: " + str(round(self.time, 1)) + "s", Colors.YELLOW)
        self.label(Vec2(0, 6), "Frame: " + str(self.frame), Colors.YELLOW)

        return super().draw()


def draw_info(window: Window, rec: Rec):
    def draw_label(text: str):
        window.label(
            rec.get_pos(),
            text[: rec.width - 2],
            Colors.INVERTED,
            align=Align.Center,
            parent_width=rec.width,
        )
        rec.y += 1

    start_pos_text = (
        str(int(game_menu.map.player_pos.x)) + " " + str(int(game_menu.map.player_pos.y))
    )
    end_pos_text = str(int(game_menu.player.pos.x)) + " " + str(int(game_menu.player.pos.y))

    draw_label("Player: " + settings_menu.player_name)
    draw_label("Map size: " + str(settings_menu.map_size_x) + " " + str(settings_menu.map_size_y))
    draw_label("Start pos: " + start_pos_text)
    draw_label("End pos: " + end_pos_text)
    draw_label("Time: " + str(round(game_menu.time, 1)) + "s")
    draw_label("Frames: " + str(game_menu.frame))
    draw_label("End speed: " + str(round(game_menu.player.speed, 1)))
    draw_label("Fuel: " + str(round(game_menu.player.fuel, 1)))
    draw_label("Points: " + str(game_menu.points))
    draw_label("Fields: " + str(game_menu.fields) + "/" + str(len(game_menu.map.fields)))
    draw_label("Difficulty: " + settings_menu.difficulties[settings_menu.difficulty])


def draw_buttons(window: Window, rec: Rec, show_restart: bool = True):
    def draw_button(text: str) -> bool:
        clicked = window.button(
            rec.get_pos(),
            text,
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        )
        rec.y += 1
        return clicked

    if show_restart and draw_button("Restart"):
        game_menu.restart_game()
        window.set_visible(False)

    if draw_button("New game"):
        game_menu.map.set_random_seed()
        game_menu.restart_game()
        window.set_visible(False)

    if draw_button("Return to main menu"):
        game_menu.set_visible(False)
        main_menu.set_visible(True)
        window.set_visible(False)


class PauseMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 8)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, Colors.INVERTED, world_pos=False)
        rec.y += 1

        self.label(
            rec.get_pos(), "Paused", Colors.INVERTED, align=Align.Center, parent_width=rec.width
        )
        rec.y += 2

        if self.button(
            rec.get_pos(),
            "Back to game",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            self.set_visible(False)
        rec.y += 1

        draw_buttons(self, rec)

        return super().draw()


class GameOverMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 19)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, world_pos=False)
        rec.y += 1

        self.label(
            rec.get_pos(), "Game Over!", Colors.INVERTED, align=Align.Center, parent_width=rec.width
        )
        rec.y += 2

        draw_info(self, rec)
        rec.y += 1

        draw_buttons(self, rec)
        rec.y += 1

        return super().draw()


class VictoryMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 18)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, world_pos=False)
        rec.y += 1

        self.label(
            rec.get_pos(), "You won!", Colors.INVERTED, align=Align.Center, parent_width=rec.width
        )
        rec.y += 2

        draw_info(self, rec)
        rec.y += 1

        draw_buttons(self, rec, show_restart=False)
        rec.y += 1

        return super().draw()


class NotificationMenu(Window):
    def __init__(self):
        super().__init__()

        self.message = ""
        self.open_time: float = 2
        self.timer: float = time.time()

    def show(self, message: str, open_time: float = 2):
        if len(self.message) > 0:
            self.message += "\n"
        self.message += message

        self.open_time = open_time
        self.timer = time.time()
        self.set_visible(True)

    def update(self):
        if time.time() - self.timer >= self.open_time:
            self.message = ""
            self.set_visible(False)

        return super().update()

    def draw(self):
        pos: Vec2 = Vec2(camera.get_terminal_size().x - measure_text(self.message).x, 0)
        self.label(pos, self.message)

        return super().draw()


main_menu = MainMenu()
settings_menu = SettingsMenu()
game_menu = GameMenu()
pause_menu = PauseMenu()
game_over_menu = GameOverMenu()
victory_menu = VictoryMenu()
notification_menu = NotificationMenu()
