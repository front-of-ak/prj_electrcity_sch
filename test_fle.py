import tkinter as t

# tk setup
root = t.Tk()
root.geometry("1200x1200")
canvas = t.Canvas(root, width=1200, height=1200, bg="white")
canvas.pack()

X, Y = 100, 100
RAD = 30
canvas.create_oval()
