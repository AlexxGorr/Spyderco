def contour(cell):
    contour = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    result = []
    for i, j in cell:
        for dx, dy in contour:
            cell_contour = i + dx, j + dy
            result.append(cell_contour)
    return result


def is_collide(ship_1, ship_2):
    for i in ship_1:
        for j in ship_2:
            if contour(i) in contour(j):
                return True
            else:
                return False


ships = {
    0: [(3, 5), (4, 5), (5, 5), (6, 5)],
    1: [(8, 2), (8, 3), (8, 4)],
    2: [(7, 3), (7, 4), (7, 5)],
    3: [(1, 3), (2, 3)]
}

flag = []
res = []
for i in range(len(ships.values())):
    flag.append(contour(ships[i]))
    for el in flag:
        for e in el:
            if e not in res:
                res.append(e)

print(res)


















