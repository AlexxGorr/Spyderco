from random import randint as rnd


class Ship:
    MARK_CELL = 1
    MARK_CELL_KILL = 2

    def __init__(self, length, tp=1, x=None, y=None):
        self._length: int = length
        self._tp: int = tp
        self._x: int = x
        self._y: int = y
        # self._cells = [self.MARK_CELL for _ in range(length)]
        # self._cells_iter = iter(self._cells)
        self._cells = [i+1 for i in range(length)]
        self._cells_iter = iter(self._cells)
        # self._cells[1] = self.MARK_CELL_KILL
        self._is_move = False if any(map(lambda x: x == self.MARK_CELL_KILL, self._cells)) else True

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def contour(self, cell):
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

    def is_collide(self, ship):
        # if not (self._x + self._length > ship._x,
        #         ship._x + ship._length > self._x,
        #         self._y + self._length > ship._y,
        #         ship._y + ship._length > self._y):
        #     return True
        # else:
        #     return False
        for i in self:
            for j in ship:
                if self.contour(i) in self.contour(j):
                    return True
                else:
                    return False

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
    MARK_WATER = '-'

    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._busy_cells = []
        self._gen_ships = []
        self._pole = [[self.MARK_WATER for _ in range(size)] for _ in range(size)]

    def init(self):
        ships = [
            Ship(4, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            # Ship(2, tp=rnd(1, 2)),
            # Ship(2, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(4, tp=1),
            # Ship(3, tp=2),
        ]
        for sh in ships:
            self._ships.append(sh)

        # for i in range(len(self._ships)):
        #     if True:
        #         a = self.__gen_ships(self._ships[i])
        #     for j in range(len(self._ships)):
        #         if True:
        #             b = self.__gen_ships(self._ships[j])

        for ship in self._ships:
            if True:
                self.__gen_ships(ship)

    def __gen_ships(self, ship):
        ship_position = False
        while not ship_position and len(self._busy_cells) < 20:
            ship.set_start_coords(rnd(0, self._size - 1), rnd(0, self._size - 1))
            start_coord = ship.get_start_coords()
            x = start_coord[0]
            y = start_coord[1]
            ship_position = self.__check_position(x, y, ship._tp, ship._length,
                                                  ship.is_out_pole(self._size), ship._cells_iter)
            if ship not in self._gen_ships:
                self._gen_ships.append(ship)

            # REPR INITIAL SHIPS ###########################
            print(f'get_start: {start_coord} | tp: {ship._tp} | ln: {ship._length} | '
                  f'pos: {ship_position}')

    # def check_collision(self):
    #     for i in range(len(self._gen_ships)):
    #         for j in range(len(self._gen_ships)):
    #             return self._gen_ships[i].is_collide(self._gen_ships[j])

    def check_collision(self):
        ships = {}
        for num in range(len(self._gen_ships)):
            if self._gen_ships[num]._tp == 1:
                for i in range(self._gen_ships[num]._x, self._gen_ships[num]._x + self._gen_ships[num]._length):
                    ships.setdefault(num, []).append((self._gen_ships[num]._x, self._gen_ships[num]._y))
                    self._gen_ships[num]._x += 1
            if self._gen_ships[num]._tp == 2:
                for i in range(self._gen_ships[num]._y, self._gen_ships[num]._y + self._gen_ships[num]._length):
                    ships.setdefault(num, []).append((self._gen_ships[num]._x, self._gen_ships[num]._y))
                    self._gen_ships[num]._y += 1
        for ship in ships.values():
            pass
        return ships

    def __check_position(self, x, y, orient, ln, out, cells):
        if not out:
            if orient == 1 and (x, y) not in self._busy_cells:
                for i in range(x, x + ln):
                    for j in range(y, y + 1):
                        if (i, j) in self._busy_cells:
                            continue
                        if True:
                            self._busy_cells.append((i, j))
                            self._pole[j][i] = next(cells)
                return True
            if orient == 2 and (x, y) not in self._busy_cells:
                for i in range(x, x + 1):
                    for j in range(y, y + ln):
                        if (i, j) in self._busy_cells:
                            continue
                        if True:
                            self._busy_cells.append((i, j))
                            self._pole[j][i] = next(cells)
                return True
            return False

    def show(self):
        for line in self._pole:
            print(*line)

    def get_ships(self):
        return [x for x in self._gen_ships]

    def get_pole(self):
        return [[self.MARK_WATER if type(i) is str else i for i in line] for line in self._pole]


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
print()
pole.show()
# pole.move_ships()
print()
pole.show()

print('-' * 50)
print('ship cells: ', len(pole._busy_cells))
print(pole._busy_cells)

print('-' * 50)
for i in pole.get_ships():
    print(f'ln: {i._length} | tp: {i._tp} | ({i._x}, {i._y}) | cells: {i._cells}')

print('-' * 50)
print('check_collision:', pole.check_collision())















