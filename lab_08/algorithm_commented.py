# Функция получения свободного вектора по 2 точкам (p1 - начало вектора, 
# p2 - конец вектора)
def get_vect(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]


# Функция расчета векторного произведения 2 векторов
def vect_mul(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

# Функция расчета скалярного произведения 2 векторов
def scalar_mul(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


# Функция проверки многоугольника (на выпуклость)
def check_polygon():
    # Не существует многоугольника, у которого меньше 3 вершин
    if len(verteces_list) < 3:
        return False
    # Знаки всех векторых произведений должны быть одинаковыми:
    # запомним знак первого векторного произведения
    sign = 1 if vect_mul(get_vect(verteces_list[1], verteces_list[2]),
                         get_vect(verteces_list[0], verteces_list[1])) > 0 else -1
    # В цикле проверяем совпадения знаков векторных произведений 
    # всех пар соседних ребер со знаком первого
    # векторного произведения
    for i in range(3, len(verteces_list)):
        if sign * vect_mul(get_vect(verteces_list[i - 1], verteces_list[i]),
                           get_vect(verteces_list[i - 2], verteces_list[i - 1])) < 0:
            # Возвращаем False при несовпадении знаков: прямоугольник невыпуклый
            return False

    if sign < 0:
        # если знак отрицательный, значит обход был по часовой стрелке. 
        # В дальнейших шагах мне нужно работать с обходом против часовой 
        # стрелке (при выяснении направления нормали, например), поэтому 
        # я переворчиваю список вершин (ну и соответственно при проходе 
        #в обратном порядке, будет обход против часовой стрелки)
        verteces_list.reverse()

    # CHECK: for verteces order
    # for i, c in enumerate(verteces_list):
        # canvas.create_oval(c[0] - i * 3, c[1] - i * 3, c[0] + i * 3, c[1] + i * 3, fill="green")

    return True


# Функция получения нормали для грани многоугольника между вершинами p1, p2
# cp = check point, следующая вершина в многоугольнике: нужна для проверки,
# направлена ли нормаль внутрь многоугольника или же из многоугольника
def get_normal(p1, p2, cp):
    vect = get_vect(p1, p2)
    # Если ищется нормаль к вертикальному вектору - то это нормаль [1, 0], 
    # иначе вектор нормали находится из условия равенства 0 скалярного произведения
    # исходного вектора и искомого вектора нормали
    norm = [1, 0] if vect[0] == 0 else [-vect[1] / vect[0], 1]
    # Если скалярное произведение найденного вектора нормали и вектора, совпадающего
    # со следующей стороной многоугольника меньше нуля - нормаль направлена из 
    # многоугольника, берем обратный вектор
    if scalar_mul(get_vect(p2, cp), norm) < 0:
        for i in range(len(norm)):
            norm[i] = -norm[i]

    # CHECK: for normal direction and side
    # center = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    # draw_section(center[0], center[1], center[0] + 10 * norm[0], center[1] + 10 * norm[1], cutter_color)

    return norm


# Функция, составляющая список векторов нормалей ко всем сторонам многоугольника
def get_normals_list(verteces):
    length = len(verteces_list)
    normal_list = list()
    for i in range(length):
        normal_list.append(get_normal(verteces[i], verteces[(i + 1) % length], verteces[(i + 2) % length]))

    return normal_list


# Функция, отсекающая отрезок и рисующая полученный новый отрезок
def cut(section, verteces_list, normals_list):
    # список параметров t рассматриваемого отрезка, при которых он пересекает ребро и
    # входит в многоугольник (не может быть меньше 0)
    t_start_list = [0]
    # аналогично списку выше, но выходит (не может быть больше 1)
    t_end_list = [1]
    # Вектор направления отрезка ( вектор = [P2 - P1] )
    d = get_vect(section[0], section[1])

    # Цикл по всем граням многоугольника и поиск параметров t точек пересечения
    # (а также получение информации о "входе-выходе", см. ниже)
    for i in range(len(verteces_list)):
        # В общем случае в качестве "точки многоугольника" берется начальная вершина
        # этой грани, однако если она совпадает с точкой начала отрезка, берется
        # конечная точка грани
        if verteces_list[i] != section[0]:
            wi = get_vect(verteces_list[i], section[0])
        else:
            wi = get_vect(verteces_list[(i + 1) % len(verteces_list)], section[0])

        # Скалярное произведение вектора нормали и вектора ориентации (если = 0, то вектор
        # параллелен стороне многоугольника)
        Dck = scalar_mul(d, normals_list[i])
        # Скалярное произведение вектора нормали и вектора от "точки многоугольника" до 
        # начала отрезка (если оно = 0, то начало отрезка лежит на рассматриваемой 
        # грани многоугольника)
        Wck = scalar_mul(wi, normals_list[i])

        # Если отрезок параллелен грани, и лежит вне многоугольника - выход
        if Dck == 0:
            if scalar_mul(wi, normals_list[i]) < 0:
                return
            else:
                continue

        # Параметр t, соответствующий точке пересечения рассматриваемого отрезка
        # с очередной гранью
        t = -Wck / Dck
        # Если Dck > 0 - точка входа в многоугольник
        if Dck > 0:
            t_start_list.append(t)
        else:
            t_end_list.append(t)
    
    # Видимый отрезок находится между "последним" входом и "первым" выходом
    t_start = max(t_start_list)
    t_end = min(t_end_list)

    # Если "входной" t < "выходной" t, то отрезок видимый - чертим его
    if t_start < t_end:
        p1 = [round(section[0][0] + d[0] * t_start), round(section[0][1] + d[1] * t_start)]
        p2 = [round(section[0][0] + d[0] * t_end), round(section[0][1] + d[1] * t_end)]
        draw_section(*p1, *p2, res_color)


def solve():
    # Проверка многоугольника на выпуклость
    if not check_polygon():
        mb.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека \
                     прямоугольник должен быть выпуклым")
        return

    # Получение нормалей для всех граней многоугольника
    normals_list = get_normals_list(verteces_list)
    # Отсечение всех отрезков из списка отрезков
    for section in sections:
        cut(section, verteces_list, normals_list)
