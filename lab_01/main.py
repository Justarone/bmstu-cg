from math import pi, atan
import tkinter as tk
import config as cfg
import tkinter.messagebox as mb

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке (применяется при наведении на окно root)
# entry.get()
# label['text'] = ''


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x:6g}".strip() + "; " + f"{self.y:6g}".strip()


class Line:
    def __init__(self, A=1, B=1, C=0):
        self.A = A
        self.B = B
        self.C = C

    def __str__(self):
        return f"{self.A:g}x + {self.B:g}y + {self.C:g} = 0"

    def find_intersection(self, line):
        # Чтобы пересечение было, слау должна иметь решения (ранг матрицы = ранг расш. матрицы = 2)
        print("lines got: ", self, line, sep='\n')
        if not (self.A * line.B - line.A * self.B != 0 and self.B * -line.C - line.B * -self.C != 0):
            return None

        ip = Point()

        if line.A != 0:
            line1, line2 = self, line
        else:
            line1, line2 = line, self

        a = line1.B - line1.A * line2.B / line2.A
        b = -line1.C - line1.A * -line2.C / line2.B
        ip.x = (line2.C - b / a * line2.B) / line2.A
        ip.y = b / a

        return ip


def get_limits(points):
    limits = [Point(points[0].x, points[0].y), Point(points[0].x, points[0].y)]

    # print("points:")
    # for i in range(len(points)):
        # print(points[i])

    # print("first limits:")

    # for i in range(2):
        # print(limits[i])
    # print()

    for point in points:

        if point.x < limits[0].x:
            limits[0].x = point.x

        if point.x > limits[1].x:
            limits[1].x = point.x

        if point.y < limits[0].y:
            limits[0].y = point.y

        if point.y > limits[1].y:
            limits[1].y = point.y

    # print("limits before additions:")
    # for i in range(2):
        # print(limits[i])

    for i in range(2):
        limits[i].x -= (limits[(i + 1) % 2].x - limits[i].x) * cfg.FIELD_BORDER_PART
        limits[i].y -= (limits[(i + 1) % 2].y - limits[i].y) * cfg.FIELD_BORDER_PART

    # print("limits after additions:")
    # for i in range(2):
        # print(limits[i])

    return limits


def create_line(p1, p2):
    line = Line()
    line.A = (p1.y - p2.y)
    line.B = -(p1.x - p2.x)
    line.C = (p1.x - p2.x) * p1.y - (p1.y - p2.y) * p1.x
    return line



# this function finds perpendicular to line, which has points p2 and p3, and perpendicular 
# has point p1
def find_perpendicular(p1, p2, p3):
    line = create_line(p2, p3)
    print("line got:", line)
    print("point is: ", p1)

    # Find coefficients for perpendicular:
    perpendicular = Line()
    if line.A == 0:
        perpendicular.B = 0
        perpendicular.A = 1
        perpendicular.C = -p1.x

    elif line.B == 0:
        perpendicular.A = 0
        perpendicular.B = 1
        perpendicular.C = -p1.y

    else:
        perpendicular.B = 1
        perpendicular.A = -(line.B / line.A)
        perpendicular.C = -perpendicular.A * p1.x - perpendicular.B * p1.y

    print("perpendicular is: ", perpendicular)
    return perpendicular


def find_angle(p1, p2, p3):
    # mediana second point (first point for mediana and height is p1).
    pm = Point((p2.x + p3.x) / 2, (p2.y + p3.y) / 2)
    # Coefficients for mediana.
    mediana = Line()
    mediana.A = (p1.y - pm.y)
    mediana.B = -(p1.x - pm.x)
    mediana.C = p1.y * (p1.x - pm.x) - p1.x * (p1.y - pm.y)

    # Coefficients for height perpendicular (only Bp and Ap 
    # (don't need C, cause we only need angle))
    height = find_perpendicular(p1, p2, p3)

    # Find angle.
    if height.B == 0 and mediana.B == 0:
        return 0

    elif mediana.B == 0:
        return abs(pi / 2 - abs(atan(-height.A / height.B)))

    elif height.B == 0:
        return abs(pi / 2 - abs(atan(-mediana.A / mediana.B)))

    else:
        angle = abs(abs(atan(-height.A / height.B)) - abs(atan(-mediana.A / mediana.B)))
        angle = pi - angle if angle > pi / 2 else angle
        return angle


def find_solution():
    print("Start of looking for solution.\n")
    only_ol = True
    for i in range(2, len(points_list)):
        if not one_line_check(points_list[0], points_list[1], points_list[i]):
            only_ol = False
            break

    if only_ol:
        print("Can't find solution (one line points)")
        return

    best_angle = find_angle(points_list[0], points_list[1], points_list[2])
    best_trio = [0, 1, 2]
    # limits = get_limits()
    print("start of cycle")

    for i in range(len(points_list)):
        for j in range(len(points_list)):
            if i == j:
                continue
            for k in range(j + 1, len(points_list)):
                if k == i:
                    continue
                angle = find_angle(points_list[i], points_list[j], points_list[k])
                if angle < best_angle:
                    print("new best angle", angle, "and trio is", i, j, k)
                    best_angle = angle
                    best_trio = [i, j, k]

    print("best trio is:", best_trio)

    print("creating lines")
    line1 = create_line(points_list[best_trio[1]], points_list[best_trio[2]])
    line2 = find_perpendicular(points_list[best_trio[0]], points_list[best_trio[1]], points_list[best_trio[2]])

    print("trying to draw (look logs of draw_solution function)")
    draw_solution([points_list[best_trio[0]], points_list[best_trio[1]], points_list[best_trio[2]],
                  line1.find_intersection(line2)])


# points = [p1, p2, p3, height_intersection]
# p1 - vertex where median and height start
def draw_solution(points):

    limits = get_limits(points)
    print("\nPoints of the comp!:")
    for i in range(4):
        print(points[i], i)
        points[i] = translate_to_comp(points[i], limits)
        print(points[i])
    print("END OF TRANSLATE!")

    for i in range(3):
        field.create_line(points[i].x, points[i].y, points[(i + 1) % 3].x, points[(i + 1) % 3].y,
                          width=cfg.LINE_WIDTH, fill="green")
    field.create_line(points[0].x, points[0].y, points[3].x, points[3].y,
                      width=cfg.LINE_WIDTH, fill="blue")
    field.create_line(points[0].x, points[0].y, (points[1].x + points[2].x) / 2,
                      (points[1].y + points[2].y) / 2, width=cfg.LINE_WIDTH, fill="red")
    # Создание дуги (start - угол начала (в компьютерных координатах (по
    # часовой, 0 - справа)), extent - прирост)
    # c.create_arc(10, 10, 190, 190, start=160, extent=-70, style=ARC, outline='darkblue', width=5)


# def translate_to_normal(point: Point, limits: tuple): WROOONG!!!!
    # y = (1 - point.y / cfg.FIELD_HEIGHT) * \
        # (limits[1].y - limits[1].x) + limits[1][0]
    # x = point[0] / cfg.FIELD_WIDTH * \
        # (limits[0][1] - limits[0][0]) + limits[0][0]
    # return (x, y)


def one_line_check(p1, p2, p3):
    if p1.x == p2.x == p3.x:
        return True

    elif p1.x == p2.x or p1.x == p3.x or p3.x == p2.x:
        return False

    a = (p1.y - p2.y) / (p1.x - p2.x)
    b = (p2.y - p3.y) / (p2.x - p3.x)
    c = (p3.y - p1.y) / (p3.x - p1.x)

    return a == b == c


# limits = ((Xmin, Ymin), (Xmax, Ymax)).
def translate_to_comp(point: Point, limits):
    print("==============\n in translate_to_comp:")
    print(point)
    for i in range(len(limits)):
        print(limits[i])
    print("====================")
    x = int((point.x - limits[0].x) / (limits[1].x - limits[0].x) * cfg.FIELD_WIDTH)
    y = int((1 - (point.y - limits[0].y) /
         (limits[1].y - limits[0].y)) * cfg.FIELD_HEIGHT)
    return Point(x, y)


def add_point(entry1, entry2):
    try:
        x = float(entry1.get())
        y = float(entry2.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
    else:
        if Point(x, y) not in points_list:
            points_list.append(Point(x, y))
            points_listbox.insert(tk.END, str(points_list[-1]))

    add_x_entry.delete(0, tk.END)
    add_y_entry.delete(0, tk.END)


def remove_point():
    indeces = list(points_listbox.curselection())
    indeces.reverse()
    for i in indeces:
        points_list.pop(i)
        points_listbox.delete(i)
    return len(indeces)


def sub_point():
    try:
        float(sub_x_entry.get())
        float(sub_y_entry.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
    else:
        number = remove_point()
        if number:
            add_point(sub_x_entry, sub_y_entry)
        else:
            mb.showinfo("Не выбрана точка.",
                        "Если вы хотите просто добавить точку, добавьте через пункт \"Добавить\"")
    sub_x_entry.delete(0, tk.END)
    sub_y_entry.delete(0, tk.END)

    find_solution()


points_list = [Point(11, 1), Point(1, 11), Point(1, 1)]

root = tk.Tk()
root.title("Computer graphics 1 lab")
root["bg"] = cfg.MAIN_COLOUR
root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)


input_frame = tk.Frame(root)
input_frame["bg"] = cfg.MAIN_COLOUR

add_button = tk.Button(input_frame, text="Добавить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR,
                       command=lambda: add_point(add_x_entry, add_y_entry),
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

add_x_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")

add_y_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")


sub_button = tk.Button(input_frame, text="Заменить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=sub_point,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

sub_x_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")

sub_y_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")


del_button = tk.Button(input_frame, text="Удалить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=remove_point,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

add_x_entry.place(x=0, y=0, width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5)
                  )

add_y_entry.place(x=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2), y=0,
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5)
                  )

add_button.place(x=0, y=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_x_entry.place(x=0, y=int(2 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_y_entry.place(x=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  y=int(2 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_button.place(x=0, y=int(3 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

del_button.place(x=0, y=int(4 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

input_frame.place(x=int(cfg.BORDERS_PART * cfg.WINDOW_WIDTH),
                  y=int(cfg.BORDERS_PART * cfg.WINDOW_HEIGHT),
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
                 y=int((cfg.BORDERS_PART * 2 + cfg.INPUT_PART_HEIGHT)
                       * cfg.WINDOW_HEIGHT),
                 width=int(cfg.WINDOW_WIDTH * cfg.DATA_PART_WIDTH),
                 height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

points_listbox.place(x=0, y=0, width=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
                     height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))
for i in range(len(points_list)):
    points_listbox.insert(tk.END, str(points_list[i]))

scroll.place(x=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             y=0, width=int(0.1 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))


field_frame = tk.Frame(root, bg=cfg.ADD_COLOUR)
field = tk.Canvas(field_frame, bg=cfg.ADD_COLOUR)

field_frame.place(x=int((3 * cfg.BORDERS_PART + cfg.INPUT_PART_WIDTH) * cfg.WINDOW_WIDTH),
                  y=int(cfg.BORDERS_PART * cfg.WINDOW_HEIGHT),
                  width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

field.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

root.mainloop()
