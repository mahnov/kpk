from tkinter import *
from random import choice, randint

screen_width = 400
screen_height = 300
timer_delay = 50
gravitational_acceleration = 9.8E-10
dt = 2 #квант физического времени


class MovingUnit:
    '''
    Абстрактный класс -- предок для шариков-мишеней и для снарядов.
    Имеет  атрибут x, y, Vx, Vy, R, avatar,
    а также метод fly -- абстрактый (т.е. его нельзя вызывать)
    '''
    def __init__ (self, x, y, Vx, Vy, R, avatar):
        self._R = R
        self._x = x
        self._y = y
        self._Vx = Vx
        self._Vy = Vy
        self._avatar = avatar
        self._deleted = False

    def fly(self):
        '''
        Абстрактный метод. Нельзя вызывать!
        Требуется реализовывать в классах-потомках.
        :return:
        '''
        raise RuntimeError()

    def delete(self):
        '''
        Удаляет объект с холста, если он еще не удален
        и помечает объект как удаленный
        :return:
        '''
        if not self._deleted:
            canvas.delete(self._avatar)
            self._deleted = True

    def deleted(self):
        '''
        :return: True, если объект уже удален
        '''
        return self._deleted

class Shell(MovingUnit):
    '''
    Снаряд, вылетающий из пушки.
    Не отражается от стенок, уничтожается, если вылетел за пределы поля.
    Двигается по гравитационной траектории
    '''
    radius = 5
    maximal_number = 3
    color = 'black'

    def __init__ (self, x, y, Vx, Vy, avatar):
        '''

        '''
        R = Shell.radius
        avatar = canvas.create_oval(x, y, x+2*R, y+2*R, width=1,
                                          fill=Shell.color,
                                          outline=Shell.color)
        super().__init__(x, y, Vx, Vy, R, avatar)

    def fly(self):
        ax = 0
        ay = gravitational_acceleration
        self._x += self._Vx*dt + ax*dt**2/2
        self._y += self._Vy*dt + ay*dt**2/2
        self._Vx += ax*dt
        self._Vx += ay*dt
        canvas.coords(self._avatar, self._x, self._y,
                      self._x + 2*self._R, self._y + 2*self._R)
        #FIXME: Пока никак не отслеживается вылет за пределы поля, когда надо уничтожить снаряд


class Ball(MovingUnit):
    initial_number = 20
    minimal_radius = 15
    maximal_radius = 40
    available_colors = ['green', 'blue', 'red']

    def __init__ (self):
        '''
        Создаю шарик в случайном положении на холсте canvas,
        при этом шарик не выходит за границы холста
        '''
        R = randint(Ball.minimal_radius, Ball.maximal_radius)
        x = randint(0, screen_width-2*R-1)
        y = randint(0, screen_height-2*R-1)
        Vx = randint(-2, 2)
        Vy = randint(-2, 2)
        fillcolor = choice(Ball.available_colors)
        avatar = canvas.create_oval(x, y, x+2*R, y+2*R, width=1,
                                          fill=fillcolor,
                                          outline=fillcolor)
        super().__init__(x, y, Vx, Vy, R, avatar)
        
    def fly(self):
        self._x += self._Vx
        self._y += self._Vy
        #отбиваемся от горизонтальных стенок
        if self._x < 0:
            self._x = 0
            self._Vx = -self._Vx
        elif self._x + 2*self._R >= screen_width:
            self._x = screen_width - 2*self._R - 1
            self._Vx = -self._Vx
        #отбиваемся от вертикальных стенок
        if self._y < 0:
            self._y = 0
            self._Vy = -self._Vy
        elif self._y + 2*self._R >= screen_height:
            self._y = screen_height - 2*self._R - 1
            self._Vy = -self._Vy
        canvas.coords(self._avatar, self._x, self._y, self._x + 2*self._R, self._y + 2*self._R)

class Gun:
    def __init__(self):
        self._x = 0
        self._y = screen_height - 1
        self._lx = 30
        self._ly = -30
        self._avatar = canvas.create_line(self._x, self._y,
                                          self._x + self._lx,
                                          self._y + self._ly)

    def shoot(self):
        '''
        :return: возвращает объект снаряда (класса Shall)
        '''
        shell = Shell(self._x + self._lx, self._y + self._ly,
                      self._lx/10, self._ly/10, self._avatar)
        return shell

def init_game():
    '''
    Создаем необходимое количество объектов-шариков,
    а также объект - пушку.
    :return:
    '''
    global balls, gun, shells_on_fly
    balls = [Ball() for i in range(Ball.initial_number)]
    shells_on_fly = []
    gun = Gun()


def init_main_window():
    global root, canvas, score_text, score_value
    root = Tk()
    root.title('Пушка')
    scores_value = IntVar()
    canvas = Canvas(root, width=screen_width, height=screen_height,
                    bg='white')
    score_text = Entry(root, textvariable=scores_value)
    canvas.pack()
    score_text.pack()
    canvas.bind('<Button-1>', click_event_handler)


def remove_deleted_from_units_from_list(units):
    delta = 0
    for i in range(len(units)):
        if units[i].deleted():
            delta += 1
        else:
            units[i-delta] = units[i]
    units[:] = units[:-delta]

def distance(unit1, unit2):
    '''

    :param unit1: шарик или снаряд
    :param unit2: шарик или снаряд
    :return: расстояние между поверхностями
    '''
    dx = unit1._x - unit2._x
    dy = unit1._y - unit2._y
    L = (dx**2 + dy**2)**0.5
    return L- unit1._R - unit2._R

def timer_event():
    #Все периодические расчеты, которые я хочу, выполняются здесь
    for ball in balls:
        ball.fly()
    for shell in shells_on_fly:
        shell.fly()
    for shell in shells_on_fly:
        for ball in balls:
            if distance(ball, shell) <= 0:
                # удалить данный шарик и данный снаряд
                shell.delete()
                ball.delete()
        remove_deleted_from_units_from_list(balls)
    remove_deleted_from_units_from_list(shells_on_fly)
    canvas.after(timer_delay, timer_event)


def click_event_handler(event):
    global shells_on_fly
    shell = gun.shoot()
    shells_on_fly.append(shell)

if __name__ == '__main__':
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()
