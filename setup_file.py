import tkinter as t
from constants import W_X, W_Y, CANVAS_WIDTH, CANVAS_X

# tk setup

root = t.Tk()
root.geometry(f'{W_X}x{W_Y}')
root.title('Главный экран')
canvas = t.Canvas(root, width=CANVAS_WIDTH, height=W_Y, bg='white')
canvas.pack()
canvas.place(x=CANVAS_X)

root.mainloop()
