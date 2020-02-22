from math import pi, atan
import tkinter as tk
import config as cfg
import tkinter.messagebox as mb

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке (применяется при наведении на окно root)
# entry.get()
# label['text'] = ''

def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x:g}".strip() + "; " + f"{self.y:g}".strip()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def find_solution():
    pass

# points = [p1, p2, p3, height_intersection]
# p1 - vertex where median and height start
def draw_solution(points, best_angle):
    pass
        # field.create_line(p1.x, p1.y, p2.x, p2.y, width=cfg.LINE_WIDTH * 2, fill="black")
    # field.create_text((p1.x + p2.x) / 2, -20 + (p1.y + p2.y) / 2, text=f"{best_angle:g}°", justify=tk.CENTER, font="Ubuntu 12")


def translate_to_comp(point: Point, limits):
    x = int((point.x - cfg.MIN_LIMIT_X) / (cfg.MAX_LIMIT_X - cfg.MIN_LIMIT_X) * cfg.FIELD_WIDTH)
    y = int((1 - (point.y - cfg.MIN_LIMIT_Y) /
         (cfg.MAX_LIMIT_Y - cfg.MIN_LIMIT_Y)) * cfg.FIELD_HEIGHT)
    return Point(x, y)


root = tk.Tk()
root.title("Computer graphics 2 lab.")
root["bg"] = cfg.MAIN_COLOUR
root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)
# root.bind("<Return>", lambda x: find_solution())


data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT)
                  )


data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

points_listbox = tk.Listbox(data_frame, selectmode=tk.EXTENDED, bg=cfg.ADD_COLOUR,
                            fg=cfg.MAIN_COLOUR, font=("Ubuntu", 14))

scroll = tk.Scrollbar(
    data_frame, command=points_listbox.yview, bg=cfg.MAIN_COLOUR)
points_listbox.config(yscrollcommand=scroll.set)

data_frame.place(x=int(cfg.BORDERS_PART * cfg.WINDOW_WIDTH),
                 y=int((cfg.BORDERS_PART * 1.5 + cfg.INPUT_PART_HEIGHT)
                       * cfg.WINDOW_HEIGHT),
                 width=int(cfg.WINDOW_WIDTH * cfg.DATA_PART_WIDTH),
                 height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

points_listbox.place(x=0, y=0, width=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
                     height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

# for i in range(len(points_list)):
    # points_listbox.insert(tk.END, str(points_list[i]))

scroll.place(x=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             y=0, width=int(0.1 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

label_frame = tk.Frame(root)
label_frame["bg"] = cfg.MAIN_COLOUR

label_frame.place(x=int(cfg.BORDERS_PART * cfg.WINDOW_WIDTH),
                 y=int((cfg.BORDERS_PART * 2 + cfg.INPUT_PART_HEIGHT + cfg.DATA_PART_HEIGHT)
                       * cfg.WINDOW_HEIGHT),
                 width=int(cfg.WINDOW_WIDTH * cfg.DATA_PART_WIDTH),
                 height=int(cfg.WINDOW_HEIGHT * 0.1))

result_label = tk.Label(label_frame, text="Здесь будут\nответы на ваши\nзапросы!", font=("Ubuntu", 11),
                       fg=cfg.MAIN_COLOUR, bg=cfg.ADD_COLOUR)

result_label.place(x=0, y=0, width=int(cfg.WINDOW_WIDTH * cfg.DATA_PART_WIDTH),
                 height=int(cfg.WINDOW_HEIGHT * 0.1))


field_frame = tk.Frame(root, bg=cfg.ADD_COLOUR)
field = tk.Canvas(field_frame, bg=cfg.ADD_COLOUR)

field_frame.place(x=int((3 * cfg.BORDERS_PART + cfg.INPUT_PART_WIDTH) * cfg.WINDOW_WIDTH),
                  y=int(cfg.BORDERS_PART * cfg.WINDOW_HEIGHT),
                  width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

field.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

info_button = tk.Button(root, text="i", font=("Ubuntu", 27),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

info_button.place(x=(cfg.BORDERS_PART * 1.5 + cfg.INPUT_PART_WIDTH) * cfg.WINDOW_WIDTH,
                  y=cfg.BORDERS_PART * cfg.WINDOW_HEIGHT, width=cfg.BORDERS_PART * cfg.WINDOW_HEIGHT,
                  height=cfg.WINDOW_HEIGHT * cfg.BORDERS_PART)

root.mainloop()
