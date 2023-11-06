from random import randint as rnd


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length: int = length
        self._tp: int = tp
        self._x: int = x
        self._y: int = y
        self._is_move = True
        self._cells = [1 for _ in range(length)]

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    # def dots(self):
    #     ship_dots = []
    #     for i in self._cells:
    #         coor_x = self._x
    #         coor_y = self._y
    #         if self._tp == 1:
    #             coor_x += i
    #         if self._tp == 2:
    #             coor_y += i
    #         ship_dots.append((coor_x, coor_y))
    #     return ship_dots

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                self._x += go
            if self._tp == 2:
                self._y += go

    def is_collide(self, ship):
        contour = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for i in ship:
            for dx, dy in contour:
                cell_contour = i._x + dx, i._y + dy
                if cell_contour[self._x][self._y] == 1:
                    return True

    def is_out_pole(self, size):
        if self._x not in range(size) or self._y not in range(size):
            return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._busy_cells = []
        self._pole = [[0 for _ in range(size)] for _ in range(size)]

    def init(self):
        ships = [
            # Ship(4, tp=rnd(1, 2)),
            # Ship(3, tp=rnd(1, 2)),
            # Ship(3, tp=rnd(1, 2)),
            # Ship(2, tp=rnd(1, 2)),
            # Ship(2, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            Ship(1, tp=rnd(1, 2)),
        ]
        for sh in ships:
            self._ships.append(sh)

        for ship in self._ships:
            ship_position = False
            while not ship_position:
                ship._x = rnd(0, self._size-1)
                ship._y = rnd(0, self._size-1)
                print(ship._x, ship._y)
                ship_position = self.__check_position(ship._length, ship._tp, ship._x, ship._y)

        for x, y in self._busy_cells:
            if 0 <= x <= 9 and 0 <= y <= 9:
                self._pole[x][y] = 1

    def __check_position(self, ln, orient, x, y):
        if orient == 1 and (x + ln - 1) <= self._size-1 and (x, y) not in self._busy_cells:
            for i in range(x-1, x+ln+1):
                for j in range(y-1, y+2):
                    if (i, j) not in self._busy_cells:
                        self._busy_cells.append((i, j))
                    else:
                        continue
            return True
        elif orient == 2 and (y + ln - 1) <= self._size-1 and (x, y) not in self._busy_cells:
            for i in range(x-1, x+2):
                for j in range(y-1, y+ln+1):
                    if (i, j) not in self._busy_cells:
                        self._busy_cells.append((i, j))
                    else:
                        continue
            return True
        else:
            return False

    def get_ships(self):
        return [x for x in self._ships]

    def move_ships(self):
        pass

    def show(self):
        for line in self._pole:
            print(*list(map(lambda x: x, line)))

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
for i in pole._ships:
    print(i.__dict__)













