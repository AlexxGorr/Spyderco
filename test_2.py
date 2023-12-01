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
        ##########################################################
        self._cells = [i+1 for i in range(length)]
        self._cells_iter = iter(self._cells)
        # self._cells[1] = self.MARK_CELL_KILL
        ##########################################################
        self._is_move = False if any(map(lambda x: x == self.MARK_CELL_KILL, self._cells)) else True

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    @staticmethod
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
        # print('__contour:', result)
        return result

    @staticmethod
    def build_ship_tuples(ship):
        result = []
        if ship._tp == 1:
            for i in range(ship._length):
                for x, y in [(ship._x, ship._y)]:
                    result.append((x+i, y))
        if ship._tp == 2:
            for i in range(ship._length):
                for x, y in [(ship._x, ship._y)]:
                    result.append((x, y+i))
        return result

    def is_collide(self, ship):
        # if isinstance(ship, Ship):
        #     if not (self._x + self._length < ship._x,
        #             ship._x + ship._length < self._x,
        #             self._y + self._length < ship._y,
        #             ship._y + ship._length < self._y,
        #             self._x != ship._x,
        #             self._y != ship._y,
        #             ship._x != self._x,
        #             ship._y != self._y):
        #         return True
        #     return False
        #####################################################
        ship_1 = self.build_ship_tuples(self)
        ship_2 = self.build_ship_tuples(ship)
        result = set(ship_1) & set(self.contour(ship_2))
        if len(result) > 0:
            print()
            print(f'result &: {result}')
            return True
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
    MARK_CONTOUR = '+'
    NUM = 0

    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._busy_cells = []
        self._pole = [[self.MARK_WATER for _ in range(size)] for _ in range(size)]
        self.COUNT = self._count()

    def _count(self):
        while True:
            self.NUM += 1
            return self.NUM

    def init(self):
        ships = [
            Ship(4, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(3, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            Ship(2, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
            # Ship(1, tp=rnd(1, 2)),
        ]
        for sh in ships:
            self._ships.append(sh)

        for ship in self._ships:
            self.__is_perimetr_ships(ship)

        print()
        print('COUNT:', self.COUNT)
        print('-' * 30)

        if not self.__check_collision():
            self.show()
            print()
            self._ships = []
            self._busy_cells = []
            self.reset_pole()
            self.init()

    def __check_collision(self):
        count = 0
        for i in range(len(self._ships)):
            for j in range(len(self._ships)):
                if i != j:
                    print(f'check: {i+1} - {j+1}')
                    if self._ships[i].is_collide(self._ships[j]):
                        print(f'Collide! '
                              f'{i+1}: ({self._ships[i]._x}, '
                              f'{self._ships[i]._y}) ln:{self._ships[i]._length} | '
                              f'{j+1}: ({self._ships[j]._x}, '
                              f'{self._ships[j]._y}) ln:{self._ships[j]._length}')
                        count += 1
                        print('-' * 30)
        print()
        print('- count collisions:', count)
        print('-' * 30)
        if count > 0:
            return False
        return True

    def __is_perimetr_ships(self, ship):
        ship_position = False
        while not ship_position and len(self._busy_cells) < 20:
            ship.set_start_coords(rnd(0, self._size - 1), rnd(0, self._size - 1))
            start_coord = ship.get_start_coords()
            x = start_coord[0]
            y = start_coord[1]
            ship_position = self.__check_position(x, y, ship._tp, ship._length,
                                                  ship.is_out_pole(self._size), ship._cells_iter)

            # REPR INITIAL SHIPS ###########################
            if ship_position:
                print(f'start: {start_coord} | tp: {ship._tp} | ln: {ship._length} | '
                      f'position: {ship_position}')

    def __check_position(self, x, y, orient, ln, out, cells):
        if not out:
            if orient == 1 and (x, y) not in self._busy_cells:
                for i in range(x, x + ln):
                    for j in range(y, y + 1):
                        if (i, j) in self._busy_cells:
                            continue
                        if True:
                            self.__fill_position(i, j, cells, verbose_contour=False)
                return True
            if orient == 2 and (x, y) not in self._busy_cells:
                for i in range(x, x + 1):
                    for j in range(y, y + ln):
                        if (i, j) in self._busy_cells:
                            continue
                        if True:
                            self.__fill_position(i, j, cells, verbose_contour=False)
                return True
            return False

    def __fill_position(self, i, j, cells, verbose_contour):
        self._busy_cells.append((i, j))
        self._pole[j][i] = next(cells)
        contour = Ship.contour([(i, j)])
        for b, a in contour:
            if a in range(0, self._size) and b in range(0, self._size):
                if self._pole[a][b] == self.MARK_WATER:
                    if verbose_contour:
                        self._pole[a][b] = self.MARK_CONTOUR
                    else:
                        self._pole[a][b] = self.MARK_WATER

    def show(self):
        for line in self._pole:
            print(*line)

    def get_ships(self):
        return [x for x in self._ships]

    def get_pole(self):
        return [[self.MARK_WATER if type(i) is str else i for i in line] for line in self._pole]

    def reset_pole(self):
        self._pole = [[self.MARK_WATER for _ in line] for line in self._pole]
        return self._pole


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
# print()
pole.show()
# pole.move_ships()
print()
# pole.show()

print('-' * 30)
print('busy cells: ', len(pole._busy_cells))
print(pole._busy_cells)

print('-' * 30)
for num, i in enumerate(pole.get_ships()):
    print(f'- {num+1} ln: {i._length} | tp: {i._tp} | ({i._x}, {i._y}) | cells: {i._cells}')


















