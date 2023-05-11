import math
import random
import tkinter as t
from tkinter import messagebox
from tkinter import filedialog as fd

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
stopped = False

cur_colors = COLOR_LIST.copy()
empty_menu = t.Menu(root)


def motion_handler(event):
    refresh_box()
    """function for moving the charge with left click"""
    selected_charges = list(filter(lambda x: x.selected, charges))
    if selected_charges and CANVAS_X < event.x < W_X and 0 < event.y < W_Y:  # rework
        moving_charge = selected_charges[-1]
        moving_charge.change_coords(event.x, event.y)
    refresh_box()


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
        # canvas.delete('lines')
        # canvas.delete('surface')
        selected_charge.prev_x, selected_charge.prev_y = selected_charge.x, selected_charge.y
    root.bind('<ButtonPress-1>', left_bt_prsd)
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')
    charge_inp.focus()
    charge_inp.icursor(len(charge_inp.get()))
    refresh_box()


#         for i in charges:
#             i.select(cur_x, cur_y)
#         if list(filter(lambda x: x.selected, charges)):
#             disable_all()
#             root.unbind('<ButtonPress-1>')
#             root.bind('<B3-Motion>', motion_handler)
#             root.bind('<ButtonRelease-3>', right_bt_rlsd)
#             root.unbind('<ButtonPress-3>')

def refresh_box():
    coordinates_box.delete(0, t.END)
    for i in charges:
        coordinates_box.insert(t.END, f'x={round((i.x - CANVAS_X))}, y={round(i.y)}, заряд {i.charge}')


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
                    i.select(cur_x, cur_y)
                    charge_selected = True
                    if list(filter(lambda x: x.selected, charges)):
                        disable_all()
                        charge_inp["state"] = 'normal'
                        root.bind('<B1-Motion>', motion_handler)
                        root.bind('<ButtonRelease-1>', left_bt_rlsd)
                        root.unbind('<ButtonPress-1>')
                    charge_inp.delete(0, t.END)
                    charge_inp.insert(0, i.charge)
            else:
                if i.selected and i.in_the_charge(cur_x, cur_y):
                    i.select(cur_x, cur_y)
                    charge_selected = True
                    disable_all()
                    charge_inp["state"] = 'normal'
                    root.bind('<B1-Motion>', motion_handler)
                    root.bind('<ButtonRelease-1>', left_bt_rlsd)
                    root.unbind('<ButtonPress-1>')
                    charge_inp.delete(0, t.END)
                    charge_inp.insert(0, i.charge)
                elif i.in_the_charge(cur_x, cur_y):
                    deselection_process()
                    for j in charges:
                        j.deselect()
                    i.select(cur_x, cur_y)
                    charge_inp.delete(0, t.END)
                    charge_inp.insert(0, i.charge)
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
                refresh_box()
    else:
        deselection_process()
    refresh_box()


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
    # print(cur_x + ST_LENGTH * (dx / ds), cur_y + ST_LENGTH * (dy / ds))
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
        for j in range(0, 360, 60):
            angle_0 = j / 180 * math.pi
            cur_x, cur_y = i.x + i.radius * math.cos(angle_0), i.y + i.radius * math.sin(angle_0)
            look_coords = set()
            look_coords.add((round(cur_x), round(cur_y)))
            counter = 1
            while is_in_borders(cur_x, cur_y) and is_outside_ch(cur_x, cur_y, ch_list, i):
                new_x, new_y = count_new_coords(ch_list, cur_x, cur_y)
                if counter % 50 == 5:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5, arrow=i.arrow,
                                       fill=new_color)
                else:
                    canvas.create_line(cur_x, cur_y, new_x, new_y, tags='lines', width=1.5, fill=new_color)
                counter += 1
                canvas.update()
                prev_coords = look_coords.copy()
                look_coords.add((round(new_x), round(new_y)))
                if prev_coords == look_coords:
                    break
                else:
                    cur_x, cur_y = new_x, new_y
        if changed:
            for _ in ch_list:
                _.charge = -_.charge
    enable_all()
    root.bind('<ButtonPress-1>', left_bt_prsd)


def count_pt_for_ch(charge, i, j):
    x, y = charge.x, charge.y
    distance = ((i - x) ** 2 + (j - y) ** 2) ** 0.5
    k = distance / 10
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


def key_fu(arg):
    return arg[0]


def draw_addit_lines(dots, color, pt):
    new_dots = dots.copy()
    itera = 400
    while new_dots:
        i = new_dots[0]
        distance = [[((i[0] - x[0]) ** 2 + (i[1] - x[1]) ** 2) ** 0.5, x[0], x[1]] for x in dots]
        distance = sorted(distance, key=key_fu)[0:int((itera // 100) * (abs(pt) // 10 + 1))]
        for m in distance:
            canvas.create_line(i[0], i[1], m[1], m[2], fill=color, width=3, tags='surface')
        canvas.update()
        new_dots = new_dots[1:]
        itera += 1
        if itera >= 570 * (len(dots) / 1.2) * (abs(pt) // 5 + 1):
            break
        if stopped:
            break


def draw_potentials(ch_list, st_pt):
    global cur_colors, stopped
    if not cur_colors:
        cur_colors = COLOR_LIST.copy()
    new_color = cur_colors[random.randint(0, len(cur_colors) - 1)]
    cur_colors.remove(new_color)
    disable_all()
    root.unbind('<ButtonPress-1>')
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')
    ofd_btn['state'] = 'normal'
    root.update()
    dots = list()
    if charges:
        for i in range(CANVAS_WIDTH):  # x
            for j in range(W_Y):  # y
                if stopped:
                    break
                x, y = CANVAS_X + i, j
                if is_outside_ch_pt(x, y, charges):
                    cur_pt = count_potential_in_spot(x, y, ch_list) * COEFF
                    if st_pt - 0.001 - 0.001 * cur_pt < cur_pt < st_pt + 0.001 + 0.001 * cur_pt:
                        dots.append([x, y, 0])
                        canvas.create_line(x - 1, y - 1,
                                           x + 1, y + 1, width=3, fill=new_color, tags='surface')
                        canvas.update()
    for i in range(1):
        if stopped:
            break
        draw_addit_lines(dots, new_color, st_pt)
    enable_all()
    ofd_btn['state'] = 'disabled'
    root.bind('<ButtonPress-1>', left_bt_prsd)
    stopped = False


def spawn_capacitor():
    global charges
    canvas.delete(t.ALL)
    create_grid()
    charges = []
    for i in [Charge(x=CANVAS_X + i, y=400, rad=ST_RAD, ch=ST_CHARGE, canvas=canvas) for i in range(600, 1000, 30)]:
        charges.append(i)
    for i in [Charge(x=CANVAS_X + i, y=500, rad=ST_RAD, ch=-ST_CHARGE, canvas=canvas) for i in range(600, 1000, 30)]:
        charges.append(i)
    charges[5].capacitored = True


def create_grid():
    # horizontal
    for i in range(26):
        canvas.create_line(CANVAS_X, 2 + i * 40, W_X, 2 + i * 40, fill='#c4c4c4')
        if i % 2 == 0:
            canvas.create_text(CANVAS_X + 3, 2 + i * 40, text=i * 40, anchor='nw', font='Calibri 14')
    # vertical
    for i in range(36):
        canvas.create_line(CANVAS_X + i * 40, 0, CANVAS_X + i * 40, W_Y - 60, fill='#c4c4c4')
        if i > 0 and i % 2 == 0:
            canvas.create_text(CANVAS_X + i * 40, 3, text=i * 40, anchor='nw', font='Calibri 14')
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
    capac_spawn_btn['state'] = 'disabled'
    menu.entryconfig('Файл', state="disabled")
    menu.entryconfig('Помощь', state="disabled")


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
    capac_spawn_btn['state'] = 'normal'
    menu.entryconfig('Файл', state="normal")
    menu.entryconfig('Помощь', state="normal")


def hide_all():
    start_btn.place_forget()
    task_btn.place_forget()
    charge_inp.place_forget()
    build_field_lines_btn.place_forget()
    clear_field_lines_btn.place_forget()
    potent_inp.place_forget()
    build_surface_btn.place_forget()
    clear_surface_btn.place_forget()
    clear_all_btn.place_forget()
    capac_spawn_btn.place_forget()
    charge_label.place_forget()
    potent_label.place_forget()
    coord_label.place_forget()
    coords_list.place_forget()
    coordinates_box.place_forget()
    ofd_btn.place_forget()
    root.config(menu=empty_menu)
    canvas.delete(t.ALL)
    root.unbind('<KeyPress>')
    root.unbind('<ButtonPress-1>')


def show_all(event):
    global charges
    canvas.delete(t.ALL)
    charges = list()
    start_btn.place(x=20, y=20)
    task_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=20, anchor='ne')
    charge_inp.place(x=20, y=120, height=48, width=195)
    build_field_lines_btn.place(x=20, y=190)
    clear_field_lines_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=190, anchor='ne')
    potent_inp.place(x=20, y=310, height=48, width=195)
    build_surface_btn.place(x=20, y=380)
    clear_surface_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=380, anchor='ne')
    clear_all_btn.place(x=20, y=480)
    capac_spawn_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=120, anchor='ne')
    charge_label.place(x=20, y=80)
    potent_label.place(x=20, y=270)
    coord_label.place(x=(W_X - CANVAS_WIDTH) // 2, y=580, anchor='center')
    coords_list.place(x=20, y=620, anchor='nw')
    coordinates_box.place(x=20, y=620, anchor='nw')
    ofd_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=480, anchor='ne')
    root.config(menu=menu)
    create_grid()
    root.unbind('<space>')
    root.bind('<KeyPress>', check_seq)
    create_grid()
    root.bind('<ButtonPress-1>', left_bt_prsd)


def screen_saver():
    """create a screensaver with information about project"""
    hide_all()
    canvas.create_text(
        960, 512,
        text="Хубаев Артём 10Г\n\n\nМоделирование построения линий "
             "напряженности\n и эквипотенциальных поверхностей\n электростатического поля\n\nДля входа в меню нажмите "
             "пробел. "
             "\n\n\n\n\n\n\nШкола 67\n2023 год",
        font='Calibry 30',
        justify=t.CENTER)

    root.bind('<space>', show_all)


def open_start():
    hide_all()
    screen_saver()


def open_help():
    hide_all()

    def go_back():
        canvas.delete(t.ALL)
        go_back_btn.destroy()
        show_all(1)

    canvas.create_text(960, 35, text='Помощь', font='Calibri 50', justify=t.CENTER)
    canvas.create_text(
        50, 100,
        text="Левая кнопка мыши (ЛКМ) - поставить заряд;\n"
             "Delete - удалить заряд;\n"
             "Кликнуть ЛКМ по заряду - выбрать его, после чего можно изменить его величину\nили перетащить его;\n"
             "ЛКМ везде, кроме заряда - снять выбор;\n"
             "F3 - автозаполнение.\n"
             "Допустимые заряды - от -3 до 3, "
             "допустимые потенциалы - от -21 до 21 (всё невключительно).",
        font='Calibry 30',
        anchor='nw')

    go_back_btn = t.Button(text='Назад', width=13, height=1, command=go_back, font='Calibri 20')
    go_back_btn.pack()
    go_back_btn.place(x=20, y=15)


def open_task():
    def go_back():
        canvas.delete(t.ALL)
        go_back_btn.destroy()
        show_all(1)

    hide_all()
    canvas.create_text(960, 35, text='Задача', font='Calibri 50', justify=t.CENTER)
    canvas.create_text(
        50, 100,
        text="Составить программу, моделирующую построение линий напряженности и эквипотенциальных\nповерхностей "
             "электрос"
             "татического поля.\nЭлектростатическое поле создается неподвижными зарядами в "
             "количестве более 3-х.\nРазмещение зарядов произвольное, в частности может представлять регулярную "
             "структуру\nконденсатор.",
        font='Calibry 30',
        anchor='nw')
    go_back_btn = t.Button(text='Назад', width=13, height=1, command=go_back, font='Calibri 20')
    go_back_btn.pack()
    go_back_btn.place(x=20, y=15)


# def place_charge():
#     global allowed_to_place
#     place_charge_btn.config(background='aliceblue')
#     allowed_to_place = True


def clear_all_charges():
    global charges
    canvas.delete(t.ALL)
    create_grid()
    charges = []
    refresh_box()


def draw_field():
    draw_line(charges)


def clear_field():
    canvas.delete('lines')

def stop_surface():
    global stopped
    stopped = True


def draw_srfs():
    try:
        st_pt = float(potent_inp.get())
    except ValueError:
        st_pt = ST_PTN
        potent_inp.insert(0, ST_PTN)
    if len(charges) > 5:
        if charges[5].capacitored:
            if st_pt != 0:
                charges[5].y -= 5
                charges[5].deselect()
            else:
                charges[5].y += 5
                charges[5].deselect()
    draw_potentials(charges, st_pt)


def clear_srfs():
    canvas.delete('surface')


# def undo_charge():
#     list(filter(lambda x: x.selected, charges))[-1].deselect()
#     change_chr_btn["state"] = 'disabled'
#     enable_all()
#     root.bind('<ButtonPress-1>', left_bt_prsd)
#     place_charge_btn.config(text='Поставить заряд', command=place_charge)
#

# def change_spec_charge():
#     new_ch = float(inp_value_ch.get())
#     selected = list(filter(lambda x: x.selected, charges))
#     if selected:
#         sel_ch = selected.pop()
#         sel_ch.charge = new_ch
#         sel_ch.deselect()
#     # place_charge_btn.config(text='Поставить заряд', command=place_charge)
#     enable_all()
#     root.bind('<ButtonPress-1>', left_bt_prsd)
def all_coords():
    return [(round((-CANVAS_X + i.x), 3), round(i.y, 3), i.charge) for i in charges]


def save_coords():
    file = fd.asksaveasfile(initialfile='Координаты.txt',
                            defaultextension=".txt", filetypes=[("Text file", "*.txt")])
    coordinates = all_coords()
    for i in coordinates:
        file.write(f'{i[0]};{i[1]};{i[2]}\n')


def load_coords():
    clear_all_charges()
    file = fd.askopenfile(filetypes=[('Text files', '*.txt',)])
    data = file.read().split()
    try:
        for i in data:
            x, y, charge = tuple(map(float, i.split(';')))
            charges.append(Charge(canvas=canvas, x=x + CANVAS_X, y=y, ch=charge, rad=ST_RAD))
    except Exception as e:
        messagebox.showerror(title=None, message="Возникла ошибка\n" + str(e))


task_btn = t.Button(text='Задача', width=13, height=1, command=open_task, font='Calibri 20')
task_btn.pack()
task_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=20, anchor='ne')

start_btn = t.Button(text='Заставка', width=13, height=1, command=open_start, font='Calibri 20')
start_btn.pack()
start_btn.place(x=20, y=20)

capac_spawn_btn = t.Button(text='Конденсатор', width=17, height=1, command=spawn_capacitor, font='Calibri 16')
capac_spawn_btn.pack()
capac_spawn_btn.place(x=(W_X - CANVAS_WIDTH) - 20, y=120, anchor='ne')

charge_label = t.Label(text='Величина заряда:', font='Calibri 18', background='white')
charge_label.pack()
charge_label.place(x=20, y=80)

inp_value_ch = t.StringVar(value=ST_CHARGE)
charge_inp = t.Entry(textvariable=inp_value_ch, font='Calibri 17')
charge_inp.pack()
charge_inp.place(x=20, y=120, height=48, width=195)

build_field_lines_btn = t.Button(text='Нарисовать линии\n напряженности', width=17, height=2, command=draw_field,
                                 font='Calibri 16')
build_field_lines_btn.pack()
build_field_lines_btn.place(x=20, y=190)

clear_field_lines_btn = t.Button(text='Удалить линии\n напряженности', width=17, height=2, command=clear_field,
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


ofd_btn = t.Button(text='Прервать построение', width=17, height=2, command=stop_surface,
                         font='Calibri 16')
ofd_btn.pack()
ofd_btn.place(x=20, y=(W_X - CANVAS_WIDTH) - 20, anchor='ne')
ofd_btn['state'] = 'disabled'
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

coordinates_box = t.Listbox(root, font='Calibri 25', width=25, height=9)
coordinates_box.pack()
coordinates_box.place(x=20, y=620, anchor='nw')


# coordinates_box["state"] = "enabled "


def input_protection(inp_message, inp_field, min_val=-1, max_val=1, max_len=1):
    message = inp_message
    inp_field.delete(0, t.END)
    if not (message.isdigit()):
        inp_field.delete(0, t.END)
        redact_message = ""
        for i in range(len(message)):
            if message[i].isdigit() or (message[i] == "." and redact_message.count(".") == 0 and i > 0 and
                                        redact_message != '-') or \
                    (message[i] == "-" and len(redact_message) == 0):
                redact_message += message[i]
        message = redact_message
    try:
        if len(message) < max_len and message.count('-') == 1 and message.count('.') == 1 or \
                len(message) < max_len - 1 and message.count('-') == 0 and message.count('.') == 1 or \
                len(message) < max_len - 1 and message.count('-') == 1 and message.count('.') == 0 or \
                len(message) < max_len - 2 and message.count('-') == 0 and message.count('.') == 0:
            if min_val < float(message) < max_val:
                inp_field.insert(0, message)
            else:
                inp_field.insert(0, message[:-1])
        else:
            inp_field.insert(0, message[:-1])
    except ValueError:
        inp_field.insert(0, message)


def auto_fill():
    clear_all_charges()
    file = open('auto_fill.txt', 'r')
    data = file.read().split()
    file.close()
    try:
        for i in data:
            x, y, charge = tuple(map(float, i.split(';')))
            charges.append(Charge(canvas=canvas, x=x + CANVAS_X, y=y, ch=charge, rad=ST_RAD))
    except Exception as e:
        messagebox.showerror(title=None, message="Возникла ошибка\n" + str(e))
    refresh_box()


def check_seq(event):
    input_protection(inp_value_ch.get(), charge_inp, min_val=-3, max_val=3, max_len=5)
    input_protection(inp_value_pt.get(), potent_inp, min_val=-21, max_val=21, max_len=6)
    if event.keysym == 'Delete':
        selected_ch = list(filter(lambda x: x.selected, charges))
        if selected_ch:
            selected_ch = selected_ch[-1]
            selected_ch.deselect()
            canvas.delete(f'charge{id(selected_ch)}', f'sign{id(selected_ch)}')
            charges.remove(selected_ch)
            enable_all()
    elif event.keysym == 'F3':
        auto_fill()
    refresh_box()


root.bind('<KeyPress>', check_seq)
screen_saver()
root.mainloop()
