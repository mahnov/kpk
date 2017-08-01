__author__ = 'Timofey Khirianov'

# GPLv3 license

from tkinter import *
from random import *
from math import *

frame_sleep_time = 5   # задержка между кадрами в милисекундах
dt = 0.1              # квант игрового времени между кадрами

brick_width = 40
brick_height = 15
bricks_horizontal_number = 10
bricks_vertical_number = 20
max_physical_x = bricks_horizontal_number
max_physical_y = bricks_vertical_number
screen_width = brick_width*bricks_horizontal_number    # ширина игрового экрана
screen_height = brick_height*bricks_vertical_number    # высота игрового экрана


def screen_x(_physical_x):
    return round(_physical_x*brick_width)


def screen_y(_physical_y):
    return screen_height - round(_physical_y*brick_height)


def physical_x(_screen_x):
    return _screen_x/brick_width


def physical_y(_screen_y):
    return (screen_height - _screen_y)/brick_height


def create_scores_text():
    global scores_text
    scores_text = canvas.create_text(60, 12, text="Scores: " + str(scores),
                                     font="Sans 18")


def change_scores_text():
    canvas.itemconfigure(scores_text, text="Scores: " + str(scores))


def brick_color(symbol):
    colors = {'r':'red', 'g':'green', 'b':'blue', 'y':'yellow', ' ':None}
    return colors[symbol]

class Bricks:
    def __init__(self, level_file, canvas):
        """загружает карту из файла"""
        self._canvas = canvas
        with open(level_file) as file:
            self.matrix = [None]*bricks_vertical_number
            self.avatars = [None]*bricks_vertical_number
            for yi in range(bricks_vertical_number):
                self.matrix[yi] = [None]*bricks_horizontal_number
                self.avatars[yi] = [None]*bricks_horizontal_number
                line = file.readline().rstrip()
                line = line + ' '*(bricks_horizontal_number - len(line))
                for xi in range(bricks_horizontal_number):
                    color = brick_color(line[xi])
                    if color != None:
                        self.matrix[yi][xi] = color
                        self.avatars[yi][xi] = canvas.create_rectangle(screen_x(xi), screen_y(yi),
                                                                       screen_x(xi+1), screen_y(yi+1), fill=color)

    def check_collision(self, ball):
        """ проверка, есть ли кирпич в левой, правой, верхней или нижней точке мячика """
        ball_beat_points = [(ball.x + ball.rx, ball.y), (ball.x + ball.rx, ball.y),
                            (ball.x, ball.y - ball.ry), (ball.x, ball.y - ball.ry)]
        for x, y in ball_beat_points:
            if self.matrix[floor(x)][floor(y)]:
                return True
        return False

    def delete_brick(self, xi, yi):
        """ удалить кирпич """
        self.matrix[yi][xi] = None
        self._canvas.delete(self.avatars[yi][xi])
        self.avatars[yi][xi] = None

class Ball:
    def __init__(self, x, y, vx, vy):
        self.r = 5  # отображаемый радиус при полёте
        self.rx = self.r/brick_width
        self.ry = self.r/brick_height
        self.x, self.y = x, y
        self.old_x, self.old_y = x, y
        self.vx, self.vy = vx, vy
        self.avatar = canvas.create_oval(screen_x(self.x) - self.r, screen_y(self.y) - self.r,
                                         screen_x(self.x) + self.r, screen_y(self.y) + self.r,
                                         fill="red")

    def move(self):
        new_x = self.x + self.vx*dt
        new_y = self.y + self.vy*dt
        if new_x - self.rx <= 0:
            self.vx = abs(self.vx)
        elif new_x + self.rx >= max_physical_x:
            self.vx = -abs(self.vx)
        if new_y + self.ry >= max_physical_y:
            self.vy = -abs(self.vy)

        self.x, self.y, self.old_x, self.old_y = new_x, new_y, self.x, self.y

        canvas.coords(self.avatar, screen_x(self.x) - self.r, screen_y(self.y) - self.r,
                      screen_x(self.x) + self.r, screen_y(self.y) + self.r)
        global game_over
        if new_y <= 0:
            game_over = True


class Racket:
    def __init__(self):
        self.lives = 3
        self.x = 0
        self.y = 0
        self.lx = 2  # ширина ракетки
        self.ly = 1  # высота ракетки
        self.avatar = canvas.create_rectangle(screen_x(self.x), screen_y(self.y),
                                              screen_x(self.x + self.lx),
                                              screen_y(self.y + self.ly),
                                              fill="brown")

    def move(self, x, y):
        """ Двигает ракетку в указанную точку
            x, y — координаты мышки в экранных координатах
            """
        self.x = physical_x(x)
        canvas.coords(self.avatar, screen_x(self.x), screen_y(self.y),
                      screen_x(self.x + self.lx), screen_y(self.y + self.ly))

    def check_collision(self, ball):
        """ Проверяет, попал ли мяч в ракетку.
            ball — мячик.
            возвращает True или False"""
        return ball.y - ball.ry <= self.y + self.ly and self.x <= ball.x <= self.x + self.lx


def time_event():
    global scores

    # если снаряд существует, то он летит
    if current_ball:
        current_ball.move()
        collision = racket.check_collision(current_ball)  # проверка, не столкнулся ли снаряд с землёй

        if collision:
            current_ball.vy = abs(current_ball.vy)
            scores += 1
            change_scores_text()
    if not game_over:
        canvas.after(frame_sleep_time, time_event)
    else:
        print("Game over!")


def mouse_move(event):
    # целимся ракеткой на курсор мышки
    racket.move(event.x, event.y)


def mouse_click(event):
    pass


if __name__ == "__main__":
    root = Tk()
    canvas = Canvas(root, width=screen_width, height=screen_height)
    canvas.pack()

    bricks = Bricks('map1.txt', canvas)
    scores = 0
    game_over = False
    racket = Racket()
    current_ball = Ball(racket.x+racket.lx/2, racket.y+racket.ly, 0.5, 1)

    create_scores_text()
    # canvas.bind('<Button-1>', mouse_click)  # FIXME: раскомментировать, когда будет сделано залипание мяча на ракетке
    canvas.bind('<Motion>', mouse_move)
    time_event()  # начинаю циклически запускать таймер
    root.mainloop()
