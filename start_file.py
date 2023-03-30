import tkinter as t

# tk setup
from charges_class import Charge
from constants import ST_CHARGE, ST_RAD, W_X, W_Y, CANVAS_WIDTH, CANVAS_X

root = t.Tk()
root.geometry(f'{W_X}x{W_Y}')
root.title('Главный экран')
canvas = t.Canvas(root, width=CANVAS_WIDTH, height=W_Y, bg='white')
canvas.pack()
canvas.place(x=CANVAS_X)


# canvas_2 = t.Canvas(root, width=(W_X - CANVAS_WIDTH), height=W_Y, bg='white')
# canvas_2.pack()
# canvas_2.place(x=0)
# canvas_2.create_line((W_X - CANVAS_WIDTH), 0, (W_X - CANVAS_WIDTH), W_Y, width=2)


def open_start():
    pass


def open_help():
    pass


def create_grid():
    # horizontal
    for i in range(26):
        canvas.create_line(0, 2 + i * 40, CANVAS_WIDTH, 2 + i * 40, fill='#c4c4c4')
    # vertical
    for i in range(36):
        canvas.create_line(4 + i * 40, 0, 4 + i * 40, W_Y - 60, fill='#c4c4c4')
    canvas.create_line(0, 2, CANVAS_WIDTH, 2, width=5, arrow=t.LAST)
    canvas.create_line(4, 0, 4, W_Y - 58, width=5, arrow=t.LAST)


help_btn = t.Button(text='Помощь', width=13, height=1, command=open_help, font='Calibri 20')
help_btn.pack()
help_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=20, anchor='ne')

start_btn = t.Button(text='Заставка', width=13, height=1, command=open_start, font='Calibri 20')
start_btn.pack()
start_btn.place(x=20, y=20)

# first_brd_line = canvas_2.create_line(0, 80, (W_X - CANVAS_WIDTH), 80, width=1)

charge_label = t.Label(text='Величина заряда:', font='Calibri 18')
charge_label.pack()
charge_label.place(x=20, y=80)

place_charge_btn = t.Button(text='Поставить заряд', width=17, height=1, command=open_start, font='Calibri 16')
place_charge_btn.pack()
place_charge_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=120, anchor='ne')


build_field_lines_btn = t.Button(text='Нарисовать линии\n поля', width=17, height=2, command=open_start,
                                 font='Calibri 16')
build_field_lines_btn.pack()
build_field_lines_btn.place(x=20, y=190)

clear_field_lines_btn = t.Button(text='Удалить линии\n поля', width=17, height=2, command=open_start,
                                 font='Calibri 16')
clear_field_lines_btn.pack()
clear_field_lines_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=190, anchor='ne')


potent_label = t.Label(text='Величина потенциала:', font='Calibri 18')
potent_label.pack()
potent_label.place(x=20, y=270)

build_surface_btn = t.Button(text='Нарисовать экв.\n поверхность', width=17, height=2, command=open_start,
                             font='Calibri 16')
build_surface_btn.pack()
build_surface_btn.place(x=20, y=380)

clear_surface_btn = t.Button(text='Удалить экв.\n поверхность', width=17, height=2, command=open_start,
                             font='Calibri 16')
clear_surface_btn.pack()
clear_surface_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=380, anchor='ne')


coord_label = t.Label(text='Координаты зарядов', font='Calibri 25')
coord_label.pack()
coord_label.place(x=(W_X - CANVAS_WIDTH) // 2, y=500, anchor='center')
create_grid()
root.mainloop()
