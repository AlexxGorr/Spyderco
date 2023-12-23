from random import randint, choice
import sys
sys.setrecursionlimit(2000)


class GameException(Exception):
    pass


class InitialException(GameException):
    def __str__(self):
        return 'Generate error!'


class Ship:
    MARK_CELL = 1
    MARK_CELL_KILL = 'X'

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
        self._cells_move_iter = iter(self._cells)
        # self._is_move = False if any(map(lambda x: x == self.MARK_CELL_KILL, self._cells)) else True
        self._is_move = True

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                return self._x + go, self._y
            if self._tp == 2:
                return self._x, self._y + go
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
        ship_1 = self.build_ship_tuples(self)
        ship_2 = self.build_ship_tuples(ship)
        result = set(ship_1) & set(self.contour(ship_2))
        # if result:
        #     print(f'result &: {result}')
        return len(result) > 0

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

    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._ships_move = []
        self._busy_cells = []
        self._pole = [[self.MARK_WATER for _ in range(size)] for _ in range(size)]
        self._count = 0

    def init(self):
        self._count += 1
        ships_collection = [
            Ship(4, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
            Ship(1, tp=randint(1, 2)),
        ]
        for ship in ships_collection:
            if ship._length > 1:
                self._ships.append(ship)

        if self._count > 1000:
            print('GENERATE Failed')
            exit()

        print()
        print('COUNT TRY:', self._count)
        print('-' * 30)

        for ship in self._ships:
            self.__is_perimetr_ships(ship)

        if not self.__check_collision(self._ships):
            self.show()
            print()
            self._ships = []
            self._busy_cells = []
            self.reset_pole()
            self.init()

    @staticmethod
    def __check_collision(ships):
        count = 0
        if len(ships) < 2:
            return True
        for i in range(len(ships)):
            for j in range(len(ships)):
                if i != j:
                    # print(f'check: {i+1} - {j+1}')
                    if ships[i].is_collide(ships[j]):
                        print(f'is collide: '
                              f'{i + 1}: ({ships[i]._x}, '
                              f'{ships[i]._y}) ln:{ships[i]._length} | '
                              f'{j + 1}: ({ships[j]._x}, '
                              f'{ships[j]._y}) ln:{ships[j]._length}')
                        count += 1
                        print('-' * 30)
        ####################################################
        if count > 0:
            print()
            print('- count collisions:', count)
        else:
            print('- NO collision!')
        print('-' * 30)
        ####################################################
        return not count > 0

    def __is_perimetr_ships(self, ship):
        ship_position = False
        while not ship_position and len(self._busy_cells) < 20:
            if ship._tp == 1:
                ship.set_start_coords(
                    randint(0, self._size - 1 - ship._length),
                    randint(0, self._size - 1)
                )
            if ship._tp == 2:
                ship.set_start_coords(
                    randint(0, self._size - 1),
                    randint(0, self._size - 1 - ship._length)
                )
            start_coord = ship.get_start_coords()
            x = start_coord[0]
            y = start_coord[1]
            ship_position = self.__check_position(
                x,
                y,
                ship._tp,
                ship._length,
                ship.is_out_pole(self._size),
                ship._cells_iter
            )
            # REPR INITIAL SHIPS ###########################
            # if ship_position:
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
                            self.__fill_position(i, j, next(cells))
                return True
            if orient == 2 and (x, y) not in self._busy_cells:
                for i in range(x, x + 1):
                    for j in range(y, y + ln):
                        if (i, j) in self._busy_cells:
                            continue
                        if True:
                            self.__fill_position(i, j, next(cells))
                return True
            return False

    def __fill_position(self, i, j, cells):
        self._busy_cells.append((i, j))
        self._pole[j][i] = cells
        contour = Ship.contour([(i, j)])
        self.__fill_contour(contour)

    def __fill_contour(self, contour, verbose_contour=False):
        for b, a in contour:
            if a in range(0, self._size) and b in range(0, self._size):
                if self._pole[a][b] == self.MARK_WATER:
                    if verbose_contour:
                        self._pole[a][b] = self.MARK_CONTOUR
                    else:
                        self._pole[a][b] = self.MARK_WATER

    def get_ships(self):
        return [x for x in self._ships]

    def get_ships_move(self):
        return [x for x in self._ships_move]

    @staticmethod
    def __check_go_perimetr(go, coord, size, ln):
        return go + coord in range(0, size - ln)

    @staticmethod
    def __check_go_collision(ghost_ship, ships, ghost_ships):
        result = []
        cnt = 1
        if len(ghost_ships) == 0:
            for x in range(len(ships)):
                if ships[x]._length != ghost_ship._length:
                    # print(f'_check ghost_ship: '
                    #       f'{ghost_ship._length} - '
                    #       f'ship ln: {ships[x]._length} ({ships[x]._x}, {ships[x]._y})')
                    if ghost_ship.is_collide(ships[x]):
                        result.append(ships[x])
        else:
            for x in range(len(ghost_ships)):
                cnt += 1
                # print(f'_check ghost_ship: '
                #       f'{ghost_ship._length} - '
                #       f'ghost_ship ln: {ghost_ships[x]._length} '
                #       f'({ghost_ships[x]._x}, {ghost_ships[x]._y})')
                if ghost_ship.is_collide(ghost_ships[x]):
                    result.append(ghost_ships[x])
            for x in range(cnt, len(ships)):
                # print(f'_check ghost_ship: '
                #       f'{ghost_ship._length} - '
                #       f'ship ln: {ships[x]._length} '
                #       f'({ships[x]._x}, {ships[x]._y})')
                if ghost_ship.is_collide(ships[x]):
                    result.append(ships[x])

        # print(f'in result = {len(result)} | {[f"ln: {x._length}, tp: {x._tp}" for x in result]}')
        return not len(result) > 0

    def __is_collision_is_perimert(self, ship_ln, ship_tp, ship, go, ship_axis):
        collision = self.__check_go_collision(Ship(
            ship_ln,
            ship_tp,
            ship.move(go)[0],
            ship.move(go)[1]),
            self._ships,
            self._ships_move
        )
        perimetr = self.__check_go_perimetr(
            go,
            ship_axis,
            self._size,
            ship_ln
        )
        return collision, perimetr

    def __calculate_go(self, go, ship, ship_axis, ship_ln, ship_tp):
        print(f'IS_tp: {ship_tp} = {ship.build_ship_tuples(ship)}')

        collision, perimetr = self.__is_collision_is_perimert(
            ship_ln,
            ship_tp,
            ship,
            go,
            ship_axis
        )
        if not (collision and perimetr):
            go *= -1
        else: go

        # print(f'GO_check_collision: {collision}')
        # print(f'GO_check_perimetr: {perimetr}')

        collision, perimetr = self.__is_collision_is_perimert(
            ship_ln,
            ship_tp,
            ship,
            go,
            ship_axis
        )
        if not (collision and perimetr):
            go = 0

        # print(f'GO_check_collision: {collision}')
        # print(f'GO_check_perimetr: {perimetr}')

        self._ships_move.append(Ship(
            ship_ln,
            ship_tp,
            ship.move(go)[0],
            ship.move(go)[1],
        ))
        print(f'<<- GO_result: {go}')
        return go

    def move_ships(self):
        self.reset_pole()
        for ship in self._ships:
            positive = 1
            negative = -1
            go = choice([positive, negative])

            print('-' * 20)
            print(f'->> GO_generate: {go}')

            if ship._tp == 1:
                go_result = self.__calculate_go(
                    go,
                    ship,
                    ship._x,
                    ship._length,
                    ship._tp
                )
                for i in range(ship._length):
                    for y, x in [ship.move(go_result)]:
                        self._pole[x][y + i] = next(ship._cells_move_iter)
                        contour = Ship.contour([(y + i, x)])
                        self.__fill_contour(contour)
                        print(f'({y + i}, {x})')
                print('-' * 30)

            if ship._tp == 2:
                go_result = self.__calculate_go(
                    go,
                    ship,
                    ship._y,
                    ship._length,
                    ship._tp
                )
                for i in range(ship._length):
                    for y, x in [ship.move(go_result)]:
                        self._pole[x + i][y] = next(ship._cells_move_iter)
                        contour = Ship.contour([(y, x + i)])
                        self.__fill_contour(contour)
                        print(f'({y}, {x + i})')
                print('-' * 30)

    def show(self):
        print(' ', ' '.join([str(x) for x in range(10)]))
        for num, line in enumerate(self._pole):
            print(num, *line)

    def get_pole(self):
        return [[self.MARK_WATER if type(i) is str else i for i in line] for line in self._pole]

    def reset_pole(self):
        self._pole = [[self.MARK_WATER for _ in line] for line in self._pole]
        return self._pole


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()
pole.move_ships()
pole.show()

# print('-' * 30)
# print('busy cells: ', len(pole._busy_cells))
# print(pole._busy_cells)

print('-' * 30)
print('ships:')
for num, i in enumerate(pole.get_ships()):
    print(f'- {num+1} ln: {i._length} | tp: {i._tp} | ({i._x}, {i._y}) | '
          f'cells: {i._cells} | move: {i._is_move}')

print('-' * 30)
print('ships move:')
for num, i in enumerate(pole.get_ships_move()):
    print(f'- {num+1} ln: {i._length} | tp: {i._tp} | ({i._x}, {i._y}) | '
          f'cells: {i._cells} | move: {i._is_move}')












