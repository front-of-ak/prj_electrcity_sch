import tkinter

from constants import ST_RAD, ST_CHARGE


class Charge:
    selected = False
    radius = ST_RAD
    charge = ST_CHARGE

    def __init__(self, *args, **kwargs):
        self.canvas = kwargs['canvas']
        self.x = kwargs['x']  # x, y - center
        self.y = kwargs['y']
        self.radius = kwargs['rad']
        self.charge = kwargs['ch']
        self.prev_x, self.prev_y = self.x, self.y
        self.img = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                           self.x + self.radius, self.y + self.radius, width=2, tags='charge')
        self.arrow = tkinter.LAST
        if self.charge < 0:
            self.sign = (self.canvas.create_line(self.x - self.radius, self.y, self.x + self.radius, self.y,
                                                 tags=f'sign{id(self)}'),
                         None)
            self.arrow = tkinter.FIRST
        else:
            self.sign = (self.canvas.create_line(self.x - self.radius, self.y, self.x + self.radius, self.y,
                                                 tags=f'sign{id(self)}'),
                         self.canvas.create_line(self.x, self.y - self.radius, self.x, self.y + self.radius,
                                                 tags=f'sign{id(self)}'))

    def select(self, mouse_x, mouse_y, color='black'):
        if self.radius ** 2 > (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2:
            self.selected = True
            self.canvas.delete(self.img)
            self.img = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                               self.x + self.radius, self.y + self.radius, width=5,
                                               tags='charge',
                                               outline=color)

    def in_the_charge(self, mouse_x, mouse_y):
        if self.radius ** 2 > (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2:
            self.select(mouse_x, mouse_y)
            return True
        return False

    def deselect(self):
        self.selected = False
        self.canvas.delete(self.img)
        self.img = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                           self.x + self.radius, self.y + self.radius, width=2, tags='charge')
        self.canvas.delete(f'sign{id(self)}')
        if self.charge < 0:

            self.sign = (self.canvas.create_line(self.x - self.radius, self.y, self.x + self.radius, self.y,
                                                 tags=f'sign{id(self)}'),
                         None)
            self.arrow = tkinter.FIRST
        else:
            self.sign = (self.canvas.create_line(self.x - self.radius, self.y, self.x + self.radius, self.y,
                                                 tags=f'sign{id(self)}'),
                         self.canvas.create_line(self.x, self.y - self.radius, self.x, self.y + self.radius,
                                                 tags=f'sign{id(self)}'))
            self.arrow = tkinter.LAST

    def change_coords(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self.canvas.coords(self.img, new_x - self.radius, new_y - self.radius,
                           new_x + self.radius, new_y + self.radius)
        self.canvas.coords(self.sign[0], new_x - self.radius, new_y, new_x + self.radius, new_y)
        if self.sign[1] is not None:
            self.canvas.coords(self.sign[1], new_x, new_y - self.radius, new_x, new_y + self.radius)

    def check_intersect(self, ch_x, ch_y):
        if 4 * self.radius ** 2 > (ch_x - self.x) ** 2 + (ch_y - self.y) ** 2:
            return True  # has intersection
        return False

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, radius: {self.radius}, is_selected: {self.selected}, " \
               f"charge: {self.charge} {id(self)}"


if __name__ == '__main__':
    pass
