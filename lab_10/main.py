import tkinter as tk
from tkinter import colorchooser
import config as cfg
import tkinter.messagebox as mb

color = cfg.DEFAULT_COLOUR


def clear_all():
    clear_canvas()


def clear_canvas():
    canvas.delete('all')


def change_color():
    global color, color_btn
    color = colorchooser.askcolor(title="select color")[1]
    color_btn.configure(background=color)


def draw_section(xb, yb, xe, ye, color):
    canvas.create_line(xb, yb, xe, ye, fill=color)


def rotate_x():
    print("rotate x")


def rotate_y():
    print("rotate y")


def rotate_z():
    print("rotate z")


def set_meta():
    pass


def solve():
    pass


root = tk.Tk()
root.title("Computer graphics 10 lab.")
root["bg"] = cfg.MAIN_COLOUR

data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

color_label = tk.Label(data_frame, text="Цвет", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                       fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rotate_label = tk.Label(data_frame, text="Вращение", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
meta_label = tk.Label(data_frame, text="Пределы и шаг", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
x_label = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
y_label = tk.Label(data_frame, text="y", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
z_label = tk.Label(data_frame, text="z", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
from_label = tk.Label(data_frame, text="От", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
to_label = tk.Label(data_frame, text="До", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                    fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
step_label = tk.Label(data_frame, text="Шаг", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
z_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
from_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")
to_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                    fg=cfg.MAIN_COLOUR, justify="center")
step_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")


x_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_x,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
y_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_y,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
z_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_z,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
confirm_btn = tk.Button(data_frame, text="Применить", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=set_meta,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

res_btn = tk.Button(data_frame, text="Нарисовать", font=("Consolas", 14),
                    bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=solve,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
color_btn = tk.Button(data_frame, text="", font=("Consolas", 14), bg=color,
                      command=change_color, relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_all,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0

color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                  height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1

color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

meta_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

from_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
to_label.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
               height=cfg.SLOT_HEIGHT)
step_label.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
                 height=cfg.SLOT_HEIGHT)
offset += 1

from_entry.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
to_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
               height=cfg.SLOT_HEIGHT)
step_entry.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
                 height=cfg.SLOT_HEIGHT)
offset += 1

confirm_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                  width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

rotate_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                   width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

x_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
x_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
x_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)
offset += 1

y_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
y_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
y_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)
offset += 1

z_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
z_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
z_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)

offset = cfg.ROWS - 2

res_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
root.bind("<Return>", lambda x: solve())

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')

root.mainloop()
