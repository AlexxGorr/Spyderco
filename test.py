from random import randint as rnd


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length: int = length
        self._tp: int = tp
        self._x: int = x
        self._y: int = y
        self._is_move = True
        # self._cells = [1 for _ in range(length)]
        self._cells = [1,2,3,4]

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        # if self._is_move:
        #     if self._tp == 1:
        #         self._x += go
        #     if self._tp == 2:
        #         self._y += go
        pass

    @staticmethod
    def is_collide(ship):
        contour = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        result = []
        for i, j in ship:
            for dx, dy in contour:
                cell_contour = i + dx, j + dy
                result.append(cell_contour)
        return result

    def is_out_pole(self, size):
        if self._tp == 1:
            return not self._x + self._length < size-1
        if self._tp == 2:
            return not self._y + self._length < size-1

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._busy_cells = []
        self._busy_contour = []
        self._contour = []
        self._pole = [['-' for _ in range(size)] for _ in range(size)]

    def init(self):
        ships = [
            Ship(4, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            Ship(1, tp=rnd(1, 2)),
            Ship(1, tp=rnd(1, 2)),
            Ship(1, tp=rnd(1, 2)),
            Ship(1, tp=rnd(1, 2)),
        ]
        for sh in ships:
            self._ships.append(sh)

        for ship in self._ships:
            ship_pos = False
            while not ship_pos and len(self._busy_cells) < 20:
                ship.set_start_coords(rnd(0, self._size-1), rnd(0, self._size-1))
                start_coord = ship.get_start_coords()

                print('get_start:', start_coord, '-', 'tp:', ship._tp, '-', 'ln:', ship._length)

                x = start_coord[0]
                y = start_coord[1]
                ship_pos = self.__check_pos(x, y, ship._tp, ship._length, ship.is_out_pole(self._size),
                                            ship._cells)
                self._contour.append(ship.is_collide(self._busy_cells))

            for i in self._contour:
                for j in i:
                    if j not in self._busy_contour:
                        self._busy_contour.append(j)

        # for x, y in self._busy_cells:
        #     self._pole[y][x] = "■"
        #
        # for cont in self._contour:
        #     for x, y in cont:
        #         if 0 <= x <= self._size-1 and 0 <= y <= self._size-1:
        #             if self._pole[y][x] != "■":
        #                 self._pole[y][x] = '*'

    def __check_pos(self, x, y, orient, ln, out, cells):
        if not out:
            if orient == 1 and (x, y) not in self._busy_cells:
                for i in range(x, x + ln):
                    for j in range(y, y + 1):
                        if (i, j) in self._busy_contour:
                            return False
                        else:
                            self._busy_cells.append((i, j))
                            for c in cells:
                                self._pole[i][j] = c
                return True
            if orient == 2 and (x, y) not in self._busy_cells:
                for i in range(x, x + 1):
                    for j in range(y, y + ln):
                        if (i, j) in self._busy_contour:
                            return False
                        else:
                            self._busy_cells.append((i, j))
                            for c in cells:
                                self._pole[i][j] = c
                return True
            return False

    def get_ships(self):
        return [x for x in self._ships]

    def move_ships(self):
        # for ship in self._ships:
        #     flag = any(map(lambda x: x == 2, ship._cells))
        #     print(flag)
        #     if flag:
        #         ship._is_move = False
        #     ship.move(1)
        pass

    def show(self):
        for line in self._pole:
            print(*line)

    def get_pole(self):
        return [[x for x in range(self._size)] for y in range(self._size)]


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()

pole.move_ships()
print()
pole.show()

print('-' * 30)
print(pole._busy_cells)
print(len(pole._busy_cells))
print('-' * 30)
print(len(pole._busy_contour))









