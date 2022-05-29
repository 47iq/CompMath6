import numpy as np
import matplotlib.pyplot as plt
from math import exp


def calculate_modified_euler(f, a, b, y0, h):
    points = list()
    points.append((a, y0))
    for i in range(1, int((b - a) / h) + 1):
        x = points[i - 1][0] + h
        y = points[i - 1][1] + h / 2 * (f(points[i - 1][0], points[i - 1][1]) + f(points[i - 1][0] + h, points[i - 1][1] + h * f(points[i - 1][0], points[i - 1][1])))
        points.append((x, y))
    return points


def calculate_adams(f, a, b, y0, h):
    points = list()
    points.append((a, y0))
    for i in range(1, int((b - a) / h) + 1):
        points.append((points[i - 1][0] + h,
                       points[i - 1][1] + h * f(points[i - 1][0], points[i - 1][1])))
    for i in range(4, int((b - a) / h) + 1):
        delta_f = f(points[i - 1][0], points[i - 1][1]) - f(points[i - 2][0], points[i - 2][1])
        delta_f2 = f(points[i - 1][0], points[i - 1][1]) - 2 * f(points[i - 2][0], points[i - 2][1]) + f(points[i - 3][0], points[i - 3][1])
        delta_f3 = f(points[i - 1][0], points[i - 1][1]) - 3 * f(points[i - 2][0], points[i - 2][1]) + 3 * f(points[i - 3][0], points[i - 3][1]) - f(points[i - 4][0], points[i - 4][1])
        x = points[i - 1][0] + h
        y = points[i - 1][1] + h * f(points[i - 1][0], points[i - 1][1]) + (h ** 2) * delta_f / 2 + 5 * (h ** 3) * delta_f2 / 12 + 3 * (h ** 4) * delta_f3 / 8
        points.append((x, y))
    return points


if __name__ == '__main__':
    functions = {
        1: lambda x, y: y + (1 + x) * (y ** 2),
        2: lambda x, y: (x ** 2) - 2 * y
    }
    solutions = {
        1: lambda x: -1 / x,
        2: lambda x: 0.75 * exp(-2 * x) + 0.5 * (x ** 2) - 0.5 * x + 0.25
    }
    func = 0
    print("Выберите функцию:\n1 — y' = y + (1 + x)y²\n2 - y' = x² - 2y")
    while True:
        try:
            func = int(input())
            if func not in [1, 2]:
                raise Exception
            break
        except Exception:
            print("Введенное число должно быть 1 или 2. Повторите ввод:")

    method = 0
    h = 0
    y_left = 0
    left, right = (0, 0)
    print("Введите метод рассчета:\n1 - Модифицированный метод Эйлера\n2 - Метод Адамса")
    while True:
        try:
            method = int(input())
            if method not in [1, 2]:
                raise Exception
            break
        except Exception:
            print("Введенное число должно быть 1 или 2. Повторите ввод:")
    print("Введите границы интервала в формате: a b")
    while True:
        try:
            left, right = map(float, input().split(" "))
            if left > right:
                t = left
                left = right
                right = t
            break
        except Exception:
            print("Некорректные границы. Повторите ввод:")
    print("Введите шаг:")
    while True:
        try:
            h = float(input())
            if h <= 0:
                raise Exception
            break
        except Exception:
            print("Некорректный шаг. Повторите ввод:")
    print("Введите значение функции в левой границе интервала:")
    while True:
        try:
            y_left = float(input())
            break
        except Exception:
            print("Некорректное значение. Повторите ввод:")
    eps = 0
    print("Введите значение необходимой точности:")
    while True:
        try:
            eps = float(input())
            break
        except Exception:
            print("Некорректное значение. Повторите ввод:")
    calculated_solution = None
    if method == 1:
        calculated_solution = calculate_modified_euler(functions[func], left, right, y_left, h)
    else:
        calculated_solution = calculate_adams(functions[func], left, right, y_left, h)
    current_eps = 1e18
    prev_eps = current_eps
    accuracy_type = 4
    iters = 0
    MAX_ITERS = 10
    if method == 1:
        accuracy_type = 2
    while current_eps > eps:
        iters += 1
        prev_eps = current_eps
        h = h / 2
        new_solution = None
        if method == 1:
            new_solution = calculate_modified_euler(functions[func], left, right, y_left, h)
        else:
            new_solution = calculate_adams(functions[func], left, right, y_left, h)
        current_eps = (abs(new_solution[2][1] - solutions[func](new_solution[2][0]))) / (pow(2, accuracy_type) - 1)
        if iters > MAX_ITERS or prev_eps < current_eps:
            print("Не удалось достигнуть необходимой точности")
            break
    print("Результат:")
    print("Достигнутая точность по правилу Рунге: " + str(current_eps))
    print("Итоговый шаг разбиения:" + str(h))
    print("%15s%15s%15s" % ("X ", "Рассчитанный Y ", "Точный Y"))
    for i in range(len(new_solution)):
        print("%15.5f%15.5f%15.5f" % (new_solution[i][0], new_solution[i][1], solutions[func](new_solution[i][0])))
    argument_values = [sol[0] for sol in calculated_solution]
    calculated_solution_values = [sol[1] for sol in calculated_solution]
    actual_solution_values = [solutions[func](i) for i in
                              np.linspace(np.min(argument_values), np.max(argument_values), 100)]
    ax = plt.gca()
    plt.plot(argument_values, calculated_solution_values, label="Рассчитанный y(x)")
    plt.plot(np.linspace(np.min(argument_values), np.max(argument_values), 100), actual_solution_values,
             label="Точный y(x)")
    plt.legend()
    plt.show()
