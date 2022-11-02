from operator import itemgetter
import random


# все функции предназначены для выполнения доп задания

def get_area_and_value(all_stuff):  # запишем данные из словаря в список
    area = [all_stuff[i][0] for i in all_stuff]
    value = [all_stuff[i][1] for i in all_stuff]
    return area, value


def get_memtable(all_stuff, space):
    area, value = get_area_and_value(all_stuff)
    n = len(value)  # находим размеры таблицы

    table = [[0 for a in range(space + 1)] for i in range(n + 1)]  # создаём таблицу из нулевых значений

    for i in range(n + 1):
        for a in range(space + 1):
            if i == 0 or a == 0:  # нулевой столбец и нулевая строка остаются нулями
                table[i][a] = 0
            elif area[i - 1] <= a:
                table[i][a] = max(value[i - 1] + table[i - 1][a - area[i - 1]], table[i - 1][a])
            else:
                table[i][a] = table[i - 1][a]
    return table, area, value


def get_final_items(all_stuff, space):
    table, area, value = get_memtable(all_stuff, space)

    n = len(value)
    res = table[n][space]
    a = space
    items_list = []  # список ячеек и ценностей

    for i in range(n, 0, -1):  # если уже собрали рюкзак полностью
        if res <= 0:
            break
        if res == table[i - 1][a]:  # заберём на следующей строке
            continue
        else:
            items_list.append([area[i - 1], value[i - 1]])  # забрали предмет
            res -= value[i - 1]
            a -= area[i - 1]

    selected_stuff = []

    for search in items_list:  # находим названия предметов по значению
        for key, value in all_stuff.items():
            if (value == search) and (key not in selected_stuff):
                selected_stuff.append(key)
                break

    return selected_stuff


survival_points = 10  # очки выживания
space = 3 * 3  # количество доступных ячеек
final_bag = []  # итоговое наполнение рюкзака

all_stuff = {  # словарь вида 'ключ-обозначение вещи': [объём в ячейках, ценность]
    'в': [3, 25],
    'п': [2, 15],
    'б': [2, 15],
    'а': [2, 20],
    'и': [1, 5],
    'н': [1, 15],
    'т': [3, 20],
    'о': [1, 25],
    'ф': [1, 15],
    'д': [1, 10],
    'к': [2, 20],
    'р': [2, 20]
}

value = {}  # словарь удельных значений вещей (ценность/объём)
for i in all_stuff:
    p = all_stuff[i][1] / all_stuff[i][0]
    value[i] = p

staff_value = dict(sorted(value.items(), key=itemgetter(1), reverse=True))  # сортировка по удельному значению

for i in staff_value:  # заполняем рюкзак, пока не кончится место
    if space > 0:
        if all_stuff[i][0] <= space:
            for j in range(int(all_stuff[i][0])):
                final_bag.append(i)
            space -= all_stuff[i][0]
            survival_points += all_stuff[i][1]  # прибавляем очки выживания, если взяли вещь
        else:
            survival_points -= all_stuff[i][1]  # вычитаем очки выживания, если не взяли вещь
    else:
        break

print('Я советую Тому положить в рюкзак следующий набор вещей: ')

# вывод вещей двумерным массивом 3х3

for i in range(0, 9, 3):
    print('[' + final_bag[i] + ']', '[' + final_bag[i + 1] + ']', '[' + final_bag[i + 2] + ']')

print("Итоговые очки выживания: ", survival_points, '\n')

# конец основной части лабораторной работы, начало доп задания


# для выполнения доп задания (7 ячеек) воспользуемся динамическим программированием

print('Если бы у Тома было 7 ячеек в рюкзаке: ')

space = 7  # обновим количество доступных ячеек

stuff = get_final_items(all_stuff, space)  # работают все описанные в начале программы функции

survival_points = 10  # обновим очки выживания

for s in all_stuff:
    if s in stuff:
        survival_points += all_stuff[s][1]
    else:
        survival_points -= all_stuff[s][1]

final_bag = []  # опустошим рюкзак

for sub in stuff:
    n = all_stuff[sub][0]
    for i in range(n):
        final_bag.append(sub)

print(final_bag)  # двумерный массив для 7 ячеек невозможен

print("Итоговые очки выживания (максимально возможное значение): ", survival_points)

if survival_points <= 0:
    print('Количество очков выживания отрицательно -> не существует такого набора вещей')

# доп задание на вывод других возможных комбинаций вещей с положительным счётом

variants = 0
print('\n', 'Ещё варианты с положительным итоговым счётом:')

while variants < 5:  # здесь можно сменить количество результатов для вывода
    space = 9
    survival_points = 10
    taken = []  # положим в рюкзак
    not_taken = []  # не положим в рюкзак
    final_bag = []  # снова опустошим рюкзак

    while (space > 0) or (len(taken) + len(not_taken) != 12):  # переберём все вещи в рандомном порядке
        sub = random.choice(list(all_stuff))
        if (str(sub) not in taken) and (str(sub) not in not_taken):
            if space >= all_stuff[str(sub)][0]:
                taken.append(sub)  # берём вещь
                survival_points += all_stuff[str(sub)][1]
                space -= all_stuff[str(sub)][0]
            else:
                not_taken.append(sub)  # не берём вещь
                survival_points -= all_stuff[str(sub)][1]

    if survival_points > 0:  # выбираем ваврианты с положительным счётом
        variants += 1

        for sub in taken:
            n = all_stuff[sub][0]
            for i in range(n):
                final_bag.append(sub)

        print('\n', 'Вариант №', variants)  # выводим двумерным массивом
        for i in range(0, 9, 3):
            print('[' + final_bag[i] + ']', '[' + final_bag[i + 1] + ']', '[' + final_bag[i + 2] + ']')
        print('Итоговые очки выживания: ', survival_points)