import math
import tkinter as t

# tk setup
from charges_class import Charge
from constants import ST_CHARGE, ST_RAD, W_X, W_Y, CANVAS_WIDTH, CANVAS_X, ST_LENGTH, ST_PTN

root = t.Tk()
root.geometry(f'{W_X}x{W_Y}')
root.title('Главный экран')
canvas = t.Canvas(root, width=CANVAS_WIDTH, height=W_Y, bg='white')
canvas.pack()
canvas.place(x=CANVAS_X)

charges = []
allowed_to_place = False
allowed_to_draw = False


def motion_handler(event):
    selected_charges = list(filter(lambda x: x.selected, charges))
    if selected_charges:
        moving_charge = selected_charges[-1]
        moving_charge.change_coords(event.x, event.y)


def left_bt_rlsd(event):
    selected_charge = list(filter(lambda x: x.selected, charges))[-1]
    can_move = True
    for i in charges:
        if i.check_intersect(event.x, event.y) and id(i) != id(selected_charge) or \
                not (0 < event.x < W_X and 0 < event.y < W_Y):
            can_move = False
    if not can_move:
        selected_charge.x, selected_charge.y = selected_charge.prev_x, selected_charge.prev_y
        selected_charge.change_coords(selected_charge.x, selected_charge.y)
    else:
        canvas.delete('lines')
        selected_charge.prev_x, selected_charge.prev_y = selected_charge.x, selected_charge.y
    list(filter(lambda x: x.selected, charges))[-1].deselect()
    draw_line(charges)
    root.bind('<ButtonPress-1>', left_bt_prsd)
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')


def left_bt_prsd(event):
    global allowed_to_place
    cur_x, cur_y = event.x, event.y
    if W_X - CANVAS_WIDTH < cur_x < W_X:
        for i in charges:
            i.select(cur_x, cur_y)
        if list(filter(lambda x: x.selected, charges)):
            root.unbind('<ButtonPress-1>')
            root.bind('<B1-Motion>', motion_handler)
            root.bind('<ButtonRelease-1>', left_bt_rlsd)
        else:
            can_place = True
            for i in charges:
                if i.check_intersect(cur_x, cur_y):
                    can_place = False
            if can_place and allowed_to_place:
                charges.append(Charge(canvas=canvas, x=cur_x, y=cur_y, rad=ST_RAD, ch=ST_CHARGE))
                draw_line(charges)
                place_charge_btn.config(background='SystemButtonFace')
                allowed_to_place = False
    else:
        place_charge_btn.config(background='SystemButtonFace')


def operation_func(ch, x_ch, y_ch, cur_x, cur_y):
    distance_sq = (x_ch - cur_x) ** 2 + (y_ch - cur_y) ** 2
    cosa = (-x_ch + cur_x) / distance_sq ** 0.5
    sina = (-y_ch + cur_y) / distance_sq ** 0.5
    e = ch / distance_sq
    return e * cosa, e * sina


def count_new_coords(ch_list, cur_x, cur_y):
    """Returns new coords"""
    cur_e = [operation_func(i.charge, i.x, i.y, cur_x, cur_y) for i in ch_list]
    dx, dy = sum(map(lambda x: x[0], cur_e)), sum(map(lambda x: x[1], cur_e))
    ds = (dx ** 2 + dy ** 2) ** 0.5
    return cur_x + ST_LENGTH * (dx / ds), cur_y + ST_LENGTH * (dy / ds)


def is_in_borders(cur_x, cur_y):
    if 0 < cur_x < CANVAS_WIDTH and 0 < cur_y < W_Y:
        return True
    return False


def is_outside_ch(cur_x, cur_y, ch_list, cur_ch):
    for i in ch_list:
        if i != cur_ch:
            if (cur_x - i.x) ** 2 + (cur_y - i.y) ** 2 < i.radius ** 2:
                return False
        else:
            continue
    return True


def draw_line(ch_list):
    for i in ch_list:
        changed = False
        if i.charge < 0:
            for _ in ch_list:
                _.charge = -_.charge
            changed = True
        for j in range(0, 360, 72):
            angle_0 = j / 180 * math.pi
            cur_x, cur_y = i.x + i.radius * math.cos(angle_0), i.y + i.radius * math.sin(angle_0)
            counter = 1
            while is_in_borders(cur_x, cur_y) and is_outside_ch(cur_x, cur_y, ch_list, i):
                new_x, new_y = count_new_coords(ch_list, cur_x, cur_y)
                if counter % 200 == 0:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5, arrow=i.arrow)
                else:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5)
                counter += 1
                canvas.update()
                cur_x, cur_y = new_x, new_y
        if changed:
            for _ in ch_list:
                _.charge = -_.charge


def create_grid():
    # horizontal
    for i in range(26):
        canvas.create_line(0, 2 + i * 40, CANVAS_WIDTH, 2 + i * 40, fill='#c4c4c4')
    # vertical
    for i in range(36):
        canvas.create_line(4 + i * 40, 0, 4 + i * 40, W_Y - 60, fill='#c4c4c4')
    canvas.create_line(0, 2, CANVAS_WIDTH, 2, width=5, arrow=t.LAST)
    canvas.create_line(4, 0, 4, W_Y - 58, width=5, arrow=t.LAST)


def open_start():
    pass


def open_help():
    pass


def place_charge():
    global allowed_to_place
    place_charge_btn.config(background='aliceblue')
    allowed_to_place = True


def clear_all_charges():
    pass


def draw_field():
    pass


def clear_field():
    pass


def draw_srfs():
    pass


def clear_srfs():
    pass


def clear_all():
    pass


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

inp_value_ch = t.StringVar(value=ST_CHARGE)
charge_inp = t.Entry(textvariable=inp_value_ch, font='Calibri 17')
charge_inp.pack()
charge_inp.place(x=20, y=120, height=48, width=195)

place_charge_btn = t.Button(text='Поставить заряд', width=17, height=1, command=place_charge,
                            font='Calibri 16')
place_charge_btn.pack()
place_charge_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=120, anchor='ne')

build_field_lines_btn = t.Button(text='Нарисовать линии\n поля', width=17, height=2, command=draw_field,
                                 font='Calibri 16')
build_field_lines_btn.pack()
build_field_lines_btn.place(x=20, y=190)

clear_field_lines_btn = t.Button(text='Удалить линии\n поля', width=17, height=2, command=clear_field,
                                 font='Calibri 16')
clear_field_lines_btn.pack()
clear_field_lines_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=190, anchor='ne')

potent_label = t.Label(text='Величина потенциала:', font='Calibri 18')
potent_label.pack()
potent_label.place(x=20, y=270)

inp_value_pt = t.StringVar(value=ST_PTN)
potent_inp = t.Entry(textvariable=inp_value_pt, font='Calibri 17')
potent_inp.pack()
potent_inp.place(x=20, y=310, height=48, width=195)

build_surface_btn = t.Button(text='Нарисовать экв.\n поверхность', width=17, height=2, command=draw_srfs,
                             font='Calibri 16')
build_surface_btn.pack()
build_surface_btn.place(x=20, y=380)

clear_surface_btn = t.Button(text='Удалить экв.\n поверхности', width=17, height=2, command=clear_srfs,
                             font='Calibri 16')
clear_surface_btn.pack()
clear_surface_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=380, anchor='ne')

clear_all_btn = t.Button(text='Удалить всё', width=17, height=2, command=clear_all,
                         font='Calibri 16')
clear_all_btn.pack()
clear_all_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=480, anchor='ne')

clear_chr_btn = t.Button(text='Удалить все\n заряды', width=17, height=2, command=clear_all_charges,
                         font='Calibri 16')
clear_chr_btn.pack()
clear_chr_btn.place(x=20, y=480)

coord_label = t.Label(text='Координаты зарядов', font='Calibri 25')
coord_label.pack()
coord_label.place(x=(W_X - CANVAS_WIDTH) // 2, y=580, anchor='center')

create_grid()
root.bind('<ButtonPress-1>', left_bt_prsd)
root.mainloop()
