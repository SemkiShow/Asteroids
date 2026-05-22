from input import Key, is_key_pressed
from game import FieldType, Player, Map, Field
from tui import *
from utils import *
import time, turtle, random


class ExitSuccess(KeyboardInterrupt): ...


class MainMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        pos = Vec2(0, 0)
        terminal_size = camera.get_terminal_size()

        title = r"""
    _        _                 _     _     
   / \   ___| |_ ___ _ __ ___ (_) __| |___ 
  / _ \ / __| __/ _ \ '__/ _ \| |/ _` / __|
 / ___ \\__ \ ||  __/ | | (_) | | (_| \__ \
/_/   \_\___/\__\___|_|  \___/|_|\__,_|___/"""
        title = title[1:]  # Remove the first newline

        self.label(pos, title, align=Align.Center, parent_width=terminal_size.x)
        pos.y += measure_text(title).y + 2

        if self.button(pos, "Play", align=Align.Center, parent_width=terminal_size.x):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            game_menu.set_visible(True)
            self.set_visible(False)
        pos.y += 2

        if self.button(pos, "Exit", align=Align.Center, parent_width=terminal_size.x):
            raise ExitSuccess
        pos.y += 2

        return super().draw()


class GameMenu(Window):
    def __init__(self):
        super().__init__()

        self.player: Player = Player()
        self.map: Map = Map()

        self.dropdown_idx = 0
        self.dropdown_active = False
        self.field_text = ""

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
        self.map.restart_game()
        self.player.restart_game()
        self.player.pos = Vec2(self.map.player_pos.x, self.map.player_pos.y)
        self.points: int = 0
        self.time: float = 0

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

    def game_over(self):
        self.player.speed = 0
        notification_menu.show("Game Over!")
        game_over_menu.set_visible(True)

    def victory(self):
        self.player.speed = 0
        notification_menu.show("You won!")
        victory_menu.set_visible(True)

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

        # Wall collision game over
        player_pos = self.player.get_draw_pos()
        if (
            player_pos.x < 0
            or player_pos.x >= self.map.size.x
            or player_pos.y < 0
            or player_pos.y >= self.map.size.y
        ):
            self.game_over()
            return

        # Asteroid collision game over
        player_pos = camera.get_draw_pos(self.player.get_draw_pos())
        for asteroid in self.map.asteroids:
            asteroid_pos = camera.get_draw_pos(asteroid.pos)
            if asteroid_pos == player_pos:
                self.game_over()
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
                case FieldType.Speed:
                    speed = random.randint(10, 30) / 10
                    self.player.speed += speed
                    notification_menu.show("Picked up debuff: +" + str(speed) + " speed")
                case FieldType.RemovePoints:
                    points = random.randint(10, 30)
                    self.points -= points
                    notification_menu.show("Picked up debuff: -" + str(points) + " points")
            self.map.fields.remove(field)

        # Target collision victory
        if player_pos == camera.get_draw_pos(self.map.end_pos):
            self.victory()
            return

    def draw(self):
        self.map.draw()
        self.player.draw()

        self.label(Vec2(0, 0), "Speed: " + str(round(self.player.speed, 1)), Colors.YELLOW)
        self.label(Vec2(0, 1), "Points: " + str(self.points), Colors.YELLOW)
        self.label(Vec2(0, 2), "Time: " + str(round(self.time, 1)) + "s", Colors.YELLOW)

        return super().draw()


class PauseMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 8)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, world_pos=False)
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

        if self.button(
            rec.get_pos(),
            "Restart",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.restart_game()
            self.set_visible(False)
        rec.y += 1

        if self.button(
            rec.get_pos(),
            "New game",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            self.set_visible(False)
        rec.y += 1

        if self.button(
            rec.get_pos(),
            "Return to main menu",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.set_visible(False)
            main_menu.set_visible(True)
            self.set_visible(False)
        rec.y += 1

        return super().draw()


class GameOverMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 7)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, world_pos=False)
        rec.y += 1

        self.label(
            rec.get_pos(), "Game Over!", Colors.INVERTED, align=Align.Center, parent_width=rec.width
        )
        rec.y += 2

        if self.button(
            rec.get_pos(),
            "Restart",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.restart_game()
            self.set_visible(False)
        rec.y += 1

        if self.button(
            rec.get_pos(),
            "New game",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            self.set_visible(False)
        rec.y += 1

        if self.button(
            rec.get_pos(),
            "Return to main menu",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.set_visible(False)
            main_menu.set_visible(True)
            self.set_visible(False)
        rec.y += 1

        return super().draw()


class VictoryMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()

        rec = Rec(terminal_size.x // 2, terminal_size.y // 2, 21, 6)
        rec.x -= rec.width // 2
        rec.y -= rec.height // 2

        camera.draw_rec(rec, world_pos=False)
        rec.y += 1

        self.label(
            rec.get_pos(), "You won!", Colors.INVERTED, align=Align.Center, parent_width=rec.width
        )
        rec.y += 2

        if self.button(
            rec.get_pos(),
            "New game",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            self.set_visible(False)
        rec.y += 1

        if self.button(
            rec.get_pos(),
            "Return to main menu",
            idle_color=Colors.INVERTED,
            selected_color=Colors.RESET,
            align=Align.Center,
            parent_width=rec.width,
        ):
            game_menu.set_visible(False)
            main_menu.set_visible(True)
            self.set_visible(False)
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
game_menu = GameMenu()
pause_menu = PauseMenu()
game_over_menu = GameOverMenu()
victory_menu = VictoryMenu()
notification_menu = NotificationMenu()
