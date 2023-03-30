import math
import tkinter as t

# tk setup
from charges_class import Charge
from constants import ST_CHARGE, ST_RAD, ST_LENGTH, W_X, W_Y

root = t.Tk()
root.geometry(f"{W_X}x{W_Y}")
canvas = t.Canvas(root, width=W_X, height=W_Y, bg="white")
canvas.pack()

charges = []


def motion_handler(event):
    selected_charges = list(filter(lambda x: x.selected, charges))
    if selected_charges:
        moving_charge = selected_charges[-1]
        moving_charge.change_coords(event.x, event.y)


def left_bt_rlsd(event):
    selected_charge = list(filter(lambda x: x.selected, charges))[-1]
    can_move = True
    for i in charges:
        if i.check_intersect(event.x, event.y) and id(i) != id(selected_charge):
            can_move = False
    if not can_move:
        selected_charge.x, selected_charge.y = selected_charge.prev_x, selected_charge.prev_y
        selected_charge.change_coords(selected_charge.x, selected_charge.y)
    else:
        selected_charge.prev_x, selected_charge.prev_y = selected_charge.x, selected_charge.y
    list(filter(lambda x: x.selected, charges))[-1].selected = False
    root.bind('<ButtonPress-1>', left_bt_prsd)
    root.unbind('<B1-Motion>')
    root.unbind('<ButtonRelease-1>')


def left_bt_prsd(event):
    cur_x, cur_y = event.x, event.y
    for i in charges:
        i.is_selected(cur_x, cur_y)
    if list(filter(lambda x: x.selected, charges)):
        root.unbind('<ButtonPress-1>')
        root.bind('<B1-Motion>', motion_handler)
        root.bind('<ButtonRelease-1>', left_bt_rlsd)
    else:
        can_place = True
        for i in charges:
            if i.check_intersect(cur_x, cur_y):
                can_place = False
        if can_place:
            charges.append(Charge(canvas=canvas, x=cur_x, y=cur_y, rad=ST_RAD, ch=ST_CHARGE))
            draw_line(charges)


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
    if 0 < cur_x < W_X and 0 < cur_y < W_Y:
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
    canvas.delete('s')  # redo
    for i in ch_list:
        changed = False
        # if ch_list[i].charge < 0:
        #     for _ in ch_list:
        #         _.charge = -_.charge
        #     changed = True
        # print(*charges)
        for j in range(0, 360, 72):
            angle_0 = j / 180 * math.pi
            cur_x, cur_y = i.x + ch_list[i].radius * math.cos(angle_0), \
                           ch_list[i].y + ch_list[i].radius * math.sin(angle_0)
            while is_in_borders(cur_x, cur_y) and is_outside_ch(cur_x, cur_y, ch_list, i):
                new_x, new_y = count_new_coords(ch_list, cur_x, cur_y)
                canvas.create_line(cur_x, cur_y, new_x, new_y, tags='s')
                canvas.update()
                cur_x, cur_y = new_x, new_y
        # if changed:
        #     for _ in ch_list:
        #         _.charge = -_.charge


root.bind('<ButtonPress-1>', left_bt_prsd)
root.mainloop()
