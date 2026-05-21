from input import is_key_pressed
from game import Player, Map, Bonus
from tui import *
from utils import *
import time, turtle


class GameMenu(Window):
    def __init__(self):
        super().__init__()

        self.player: Player = Player()
        self.map: Map = Map()

        self.dropdown_idx = 0
        self.dropdown_active = False
        self.field_text = ""

        turtle.speed(0)
        turtle.tracer(False)
        self.map.set_random_seed()
        self.restart_game()

    def map_to_turtle(self, pos: Vec2) -> Vec2:
        return Vec2(
            (pos.x - self.map.size.x / 2) * 2,
            (self.map.size.y / 2 - pos.y) / camera.ratio * 2,
        )

    def restart_game(self):
        self.map.reload_game()
        self.player.pos = Vec2(self.map.player_pos.x, self.map.player_pos.y)
        self.player.angle = 0

        # Set up the screen
        turtle.Screen().setup(self.map.size.x * 2, self.map.size.y / camera.ratio * 2)
        turtle.clearscreen()

        # Draw goal
        turtle_end_pos = self.map_to_turtle(self.map.end_pos)
        end_pos_size = 10
        turtle.color("green")
        turtle.width(3)
        turtle.penup()
        turtle.goto(turtle_end_pos.x, turtle_end_pos.y)
        turtle.pendown()
        turtle.goto(turtle_end_pos.x + end_pos_size, turtle_end_pos.y - end_pos_size)
        turtle.penup()
        turtle.goto(turtle_end_pos.x + end_pos_size, turtle_end_pos.y)
        turtle.pendown()
        turtle.goto(turtle_end_pos.x, turtle_end_pos.y - end_pos_size)
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
        game_over_menu.visible = True

    def victory(self):
        self.player.speed = 0
        notification_menu.show("You won!")
        victory_menu.visible = True

    def update(self):
        super().update()

        # Don't run game update if the game is over
        if game_over_menu.visible or victory_menu.visible:
            return

        if is_key_pressed("a") or is_key_pressed("LEFT"):
            self.player.angle -= 45
        if is_key_pressed("d") or is_key_pressed("RIGHT"):
            self.player.angle += 45
        if is_key_pressed(" "):
            self.player.speed += 0.5

        self.player.update()
        self.move_turtle()

        player_pos = self.player.get_draw_pos()
        if (
            player_pos.x < 0
            or player_pos.x >= self.map.size.x
            or player_pos.y < 0
            or player_pos.y >= self.map.size.y
        ):
            self.game_over()
            return

        player_pos = camera.get_draw_pos(self.player.get_draw_pos())
        for asteroid in self.map.asteroids:
            asteroid_pos = camera.get_draw_pos(asteroid.pos)
            if asteroid_pos == player_pos:
                self.game_over()
                return

        collected_bonuses: list[Bonus] = []
        for bonus in self.map.bonuses:
            bonus_pos = camera.get_draw_pos(bonus.pos)
            if bonus_pos == player_pos:
                collected_bonuses.append(bonus)
        for bonus in collected_bonuses[::-1]:
            self.map.bonuses.remove(bonus)

        if player_pos == camera.get_draw_pos(self.map.end_pos):
            self.victory()
            return

    def draw(self):
        self.map.draw()
        self.player.draw()

        self.label(
            Vec2(0, 0),
            "Position: "
            + str(round(self.player.pos.x, 1))
            + " "
            + str(round(self.player.pos.y, 1)),
            Colors.YELLOW,
        )

        self.label(Vec2(0, 1), "Speed: " + str(round(self.player.speed, 1)), Colors.YELLOW)

        return super().draw()


class GameOverMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()
        pos = Vec2(terminal_size.x / 2 - 5, terminal_size.y / 2)

        camera.draw_rec(Rec(pos.x - 1, pos.y - 1, 12, 5), Colors.BG_BLACK, world_pos=False)

        self.label(pos, "Game Over!", Colors.BG_BLACK)
        pos.y += 2

        if self.button(Vec2(pos.x + 1, pos.y), "Restart"):
            game_menu.restart_game()
            self.visible = False
        pos.y += 2

        return super().draw()


class VictoryMenu(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        terminal_size = camera.get_terminal_size()
        pos = Vec2(terminal_size.x / 2 - 5, terminal_size.y / 2)

        camera.draw_rec(Rec(pos.x - 1, pos.y - 1, 12, 5), Colors.BG_BLACK, world_pos=False)

        self.label(pos, "You won!", Colors.BG_BLACK)
        pos.y += 2

        if self.button(Vec2(pos.x + 1, pos.y), "Restart"):
            game_menu.map.set_random_seed()
            game_menu.restart_game()
            self.visible = False
        pos.y += 2

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
        self.visible = True

    def update(self):
        if time.time() - self.timer >= self.open_time:
            self.message = ""
            self.visible = False

        return super().update()

    def draw(self):
        pos: Vec2 = Vec2(camera.get_terminal_size().x - measure_text(self.message).x, 0)
        self.label(pos, self.message)

        return super().draw()


game_menu = GameMenu()
game_over_menu = GameOverMenu()
victory_menu = VictoryMenu()
notification_menu = NotificationMenu()
