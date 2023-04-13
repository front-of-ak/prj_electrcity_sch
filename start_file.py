import math
import random
import tkinter as t

# tk setup
from charges_class import Charge
from constants import ST_CHARGE, ST_RAD, W_X, W_Y, CANVAS_WIDTH, CANVAS_X, ST_LENGTH, ST_PTN, COLOR_LIST, \
    COEFF

root = t.Tk()
root.geometry(f'{W_X}x{W_Y}')
root.title('Главный экран')
canvas = t.Canvas(root, width=W_X, height=W_Y, bg='white')
canvas.pack()

charges = []
allowed_to_place = False
allowed_to_draw = False

cur_colors = COLOR_LIST.copy()


def motion_handler(event):
    """function for moving the charge with left click"""
    selected_charges = list(filter(lambda x: x.selected, charges))
    if selected_charges and CANVAS_X < event.x < W_X and 0 < event.y < W_Y:  # rework
        moving_charge = selected_charges[-1]
        moving_charge.change_coords(event.x, event.y)


def left_bt_rlsd(event):
    """function for moving charge to final position or to returning it to the start"""
    selected_charge = list(filter(lambda x: x.selected, charges)).pop()
    can_move = True
    for i in charges:
        if i.check_intersect(event.x, event.y) and id(i) != id(selected_charge) or \
                not (CANVAS_X < event.x < W_X and 0 < event.y < W_Y):
            can_move = False
    if not can_move:
        selected_charge.x, selected_charge.y = selected_charge.prev_x, selected_charge.prev_y
        selected_charge.change_coords(selected_charge.x, selected_charge.y)
    else:
        canvas.delete('lines')
        selected_charge.prev_x, selected_charge.prev_y = selected_charge.x, selected_charge.y
    root.bind('<ButtonPress-1>', left_bt_prsd)
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')
    charge_inp.focus()
    charge_inp.icursor(len(charge_inp.get()))


#         for i in charges:
#             i.select(cur_x, cur_y)
#         if list(filter(lambda x: x.selected, charges)):
#             disable_all()
#             root.unbind('<ButtonPress-1>')
#             root.bind('<B3-Motion>', motion_handler)
#             root.bind('<ButtonRelease-3>', right_bt_rlsd)
#             root.unbind('<ButtonPress-3>')


def save_data_from_inp():
    selected_charge = list(filter(lambda x: x.selected, charges))
    if selected_charge:
        selected_charge = selected_charge[-1]
        new_charge = charge_inp.get()
        selected_charge.charge = float(new_charge)


def deselection_process():
    next_click = False
    save_data_from_inp()
    for i in charges:
        if i.selected:
            next_click = True
        i.deselect()
    enable_all()
    return next_click


def left_bt_prsd(event):
    """function for placing charge and selecting it with rb"""
    cur_x, cur_y = event.x, event.y
    if CANVAS_X < cur_x < W_X:
        charge_selected = False
        for i in charges:
            if not list(filter(lambda x: x.selected, charges)):
                if i.in_the_charge(cur_x, cur_y):
                    charge_selected = True
                    if list(filter(lambda x: x.selected, charges)):
                        disable_all()
                        charge_inp["state"] = 'normal'
                        root.bind('<B1-Motion>', motion_handler)
                        root.bind('<ButtonRelease-1>', left_bt_rlsd)
                        root.unbind('<ButtonPress-1>')
            else:
                if i.selected and i.in_the_charge(cur_x, cur_y):
                    charge_selected = True
                    disable_all()
                    charge_inp["state"] = 'normal'
                    root.bind('<B1-Motion>', motion_handler)
                    root.bind('<ButtonRelease-1>', left_bt_rlsd)
                    root.unbind('<ButtonPress-1>')
                elif i.in_the_charge(cur_x, cur_y):
                    for j in charges:
                        j.deselect()
                    i.select(cur_x, cur_y)
                    charge_selected = True
                    disable_all()
                    charge_inp["state"] = 'normal'
                    root.bind('<B1-Motion>', motion_handler)
                    root.bind('<ButtonRelease-1>', left_bt_rlsd)
                    root.unbind('<ButtonPress-1>')

        next_click = False
        if not charge_selected:
            next_click = deselection_process()

        can_place = True
        if not next_click:
            for i in charges:
                if i.check_intersect(cur_x, cur_y):
                    can_place = False
            if can_place:
                try:
                    charges.append(Charge(canvas=canvas, x=cur_x, y=cur_y, rad=ST_RAD,
                                          ch=float(charge_inp.get())))
                except ValueError:
                    charges.append(Charge(canvas=canvas, x=cur_x, y=cur_y, rad=ST_RAD,
                                          ch=ST_CHARGE))
                    charge_inp.insert(0, ST_CHARGE)
    else:
        deselection_process()


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
    if CANVAS_X < cur_x < W_X and 0 < cur_y < W_Y:
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
    global cur_colors
    if not cur_colors:
        cur_colors = COLOR_LIST.copy()
    new_color = cur_colors[random.randint(0, len(cur_colors) - 1)]
    cur_colors.remove(new_color)
    disable_all()
    root.unbind('<ButtonPress-1>')
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')
    for i in ch_list:
        changed = False
        if i.charge < 0:
            for _ in ch_list:
                _.charge = -_.charge
            changed = True
        for j in range(0, 360, 30):
            angle_0 = j / 180 * math.pi
            cur_x, cur_y = i.x + i.radius * math.cos(angle_0), i.y + i.radius * math.sin(angle_0)
            counter = 1
            while is_in_borders(cur_x, cur_y) and is_outside_ch(cur_x, cur_y, ch_list, i):
                new_x, new_y = count_new_coords(ch_list, cur_x, cur_y)
                if counter % 50 == 0:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5, arrow=i.arrow,
                                       fill=new_color)
                else:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5, fill=new_color)
                counter += 1
                canvas.update()
                cur_x, cur_y = new_x, new_y
        if changed:
            for _ in ch_list:
                _.charge = -_.charge
    enable_all()
    root.bind('<ButtonPress-1>', left_bt_prsd)


def count_pt_for_ch(charge, i, j):
    x, y = charge.x, charge.y
    distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
    return charge.charge / distance


def count_potential_in_spot(i, j, ch_list):
    cur_pt = sum([count_pt_for_ch(charge, i, j) for charge in ch_list])
    return cur_pt


def is_outside_ch_pt(cur_x, cur_y, ch_list):
    for i in ch_list:
        if (cur_x - i.x) ** 2 + (cur_y - i.y) ** 2 < i.radius ** 2:
            return False
        else:
            continue
    return True


def draw_potentials(ch_list, st_pt):
    global cur_colors
    if not cur_colors:
        cur_colors = COLOR_LIST.copy()
    new_color = cur_colors[random.randint(0, len(cur_colors) - 1)]
    cur_colors.remove(new_color)
    disable_all()
    root.unbind('<ButtonPress-1>')
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')
    root.update()
    if charges:
        for i in range(CANVAS_WIDTH):  # x
            for j in range(W_Y):  # y
                if is_outside_ch_pt(i, j, charges):
                    cur_pt = count_potential_in_spot(i, j, ch_list) * COEFF
                    print(cur_pt)
                    if st_pt - 0.07 < cur_pt < st_pt + 0.07:
                        canvas.create_line(i - 0.5 + CANVAS_WIDTH, j - 0.5,
                                           i + 0.5 + CANVAS_WIDTH, j + 0.5, width=3, fill=new_color)
                        canvas.update()
    enable_all()
    root.bind('<ButtonPress-1>', left_bt_prsd)


def create_grid():
    # horizontal
    for i in range(26):
        canvas.create_line(CANVAS_X, 2 + i * 40, W_X, 2 + i * 40, fill='#c4c4c4')
        canvas.create_text(CANVAS_X + 3, 2 + i * 40, text=i, anchor='nw', font='Calibri 10')
    # vertical
    for i in range(36):
        canvas.create_line(CANVAS_X + i * 40, 0, CANVAS_X + i * 40, W_Y - 60, fill='#c4c4c4')
        if i > 0:
            canvas.create_text(CANVAS_X + i * 40, 3, text=i, anchor='nw', font='Calibri 10')
    canvas.create_line(CANVAS_X, 2, W_X, 2, width=5, arrow=t.LAST)
    canvas.create_line(CANVAS_X, 0, CANVAS_X, W_Y - 58, width=5, arrow=t.LAST)
    canvas.create_line(CANVAS_X, 2, W_X, 2, width=5, arrow=t.LAST)
    canvas.create_line(CANVAS_X, 0, CANVAS_X, W_Y - 58, width=5, arrow=t.LAST)


def disable_all():
    start_btn['state'] = 'disabled'
    task_btn['state'] = 'disabled'
    charge_inp['state'] = 'disabled'
    # place_charge_btn['state'] = 'disabled'
    build_field_lines_btn['state'] = 'disabled'
    clear_field_lines_btn['state'] = 'disabled'
    potent_inp['state'] = 'disabled'
    build_surface_btn['state'] = 'disabled'
    clear_surface_btn['state'] = 'disabled'
    # clear_all_btn['state'] = 'disabled'
    clear_all_btn['state'] = 'disabled'


def enable_all():
    start_btn['state'] = 'normal'
    task_btn['state'] = 'normal'
    charge_inp['state'] = 'normal'
    # place_charge_btn['state'] = 'normal'
    build_field_lines_btn['state'] = 'normal'
    clear_field_lines_btn['state'] = 'normal'
    potent_inp['state'] = 'normal'
    build_surface_btn['state'] = 'normal'
    clear_surface_btn['state'] = 'normal'
    # clear_all_btn['state'] = 'normal'
    clear_all_btn['state'] = 'normal'


def open_start():
    pass


def open_help():
    pass


# def place_charge():
#     global allowed_to_place
#     place_charge_btn.config(background='aliceblue')
#     allowed_to_place = True


def clear_all_charges():
    global charges
    canvas.delete(t.ALL)
    create_grid()
    charges = []


def draw_field():
    draw_line(charges)


def clear_field():
    canvas.delete('lines')


def draw_srfs():
    try:
        st_pt = float(potent_inp.get())
    except ValueError:
        st_pt = ST_PTN
        potent_inp.insert(0, ST_PTN)
    draw_potentials(charges, st_pt)


def clear_srfs():
    pass


# def undo_charge():
#     list(filter(lambda x: x.selected, charges))[-1].deselect()
#     change_chr_btn["state"] = 'disabled'
#     enable_all()
#     root.bind('<ButtonPress-1>', left_bt_prsd)
#     place_charge_btn.config(text='Поставить заряд', command=place_charge)
#

def change_spec_charge():
    new_ch = float(inp_value_ch.get())
    selected = list(filter(lambda x: x.selected, charges))
    if selected:
        sel_ch = selected.pop()
        sel_ch.charge = new_ch
        sel_ch.deselect()
    # place_charge_btn.config(text='Поставить заряд', command=place_charge)
    enable_all()
    root.bind('<ButtonPress-1>', left_bt_prsd)


def save_coords():
    pass


def load_coords():
    pass


task_btn = t.Button(text='Задача', width=13, height=1, command=open_help, font='Calibri 20')
task_btn.pack()
task_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=20, anchor='ne')

start_btn = t.Button(text='Заставка', width=13, height=1, command=open_start, font='Calibri 20')
start_btn.pack()
start_btn.place(x=20, y=20)

charge_label = t.Label(text='Величина заряда:', font='Calibri 18', background='white')
charge_label.pack()
charge_label.place(x=20, y=80)

inp_value_ch = t.StringVar(value=ST_CHARGE)
charge_inp = t.Entry(textvariable=inp_value_ch, font='Calibri 17')
charge_inp.pack()
charge_inp.place(x=20, y=120, height=48, width=195)

build_field_lines_btn = t.Button(text='Нарисовать линии\n поля', width=17, height=2, command=draw_field,
                                 font='Calibri 16')
build_field_lines_btn.pack()
build_field_lines_btn.place(x=20, y=190)

clear_field_lines_btn = t.Button(text='Удалить линии\n поля', width=17, height=2, command=clear_field,
                                 font='Calibri 16')
clear_field_lines_btn.pack()
clear_field_lines_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=190, anchor='ne')

potent_label = t.Label(text='Величина потенциала:', font='Calibri 18', background='white')
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

clear_all_btn = t.Button(text='Удалить всё', width=17, height=2, command=clear_all_charges,
                         font='Calibri 16')
clear_all_btn.pack()
clear_all_btn.place(x=20, y=480)

coord_label = t.Label(text='Координаты зарядов', font='Calibri 25', background='white')
coord_label.pack()
coord_label.place(x=(W_X - CANVAS_WIDTH) // 2, y=580, anchor='center')

coords_list = t.Label(text='', font='Calibri 25', width=25, height=9)
coords_list.pack()
coords_list.place(x=20, y=620, anchor='nw')

menu = t.Menu(root, tearoff=0)
root.config(menu=menu)

file_edit = t.Menu(menu, tearoff=0)

menu.add_cascade(label='Файл', menu=file_edit)
file_edit.add_command(label='Сохранить координаты в файл', command=save_coords)
file_edit.add_command(label='Загрузить координаты из файла', command=load_coords)

help_btn = t.Menu(menu, tearoff=0)
menu.add_cascade(label='Помощь', menu=help_btn)
help_btn.add_command(label='Помощь', command=open_help)


def input_protection(inp_message, inp_field):
    message = inp_message
    if not (message.isdigit()):
        inp_field.delete(0, t.END)
        redact_message = ""
        for i in range(len(message)):
            if message[i].isdigit() or (message[i] == "." and redact_message.count(".") == 0) or \
                    (message[i] == "-" and len(redact_message) == 0):
                redact_message += message[i]
        inp_field.insert(0, redact_message)


def check_seq(event):
    input_protection(inp_value_ch.get(), charge_inp)
    input_protection(inp_value_pt.get(), potent_inp)
    if event.keysym == 'Delete':
        selected_ch = list(filter(lambda x: x.selected, charges))
        if selected_ch:
            selected_ch = selected_ch[-1]
            selected_ch.deselect()
            canvas.delete(f'charge{id(selected_ch)}', f'sign{id(selected_ch)}')
            charges.remove(selected_ch)
            enable_all()


root.bind('<KeyPress>', check_seq)

create_grid()
root.bind('<ButtonPress-1>', left_bt_prsd)
root.mainloop()
