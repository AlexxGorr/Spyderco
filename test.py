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
        self._is_move = False if any(map(lambda x: x == self.MARK_CELL_KILL, self._cells)) else True

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

    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._ships_move = []
        self._busy_cells = []
        self._pole = [[self.MARK_WATER for _ in range(size)] for _ in range(size)]
        self._count = 0

    def init(self):
        self._count += 1
        ships = [
            Ship(4, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(3, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            Ship(2, tp=randint(1, 2)),
            # Ship(2, tp=randint(1, 2)),
            # Ship(1, tp=randint(1, 2)),
            # Ship(1, tp=randint(1, 2)),
            # Ship(1, tp=randint(1, 2)),
            # Ship(1, tp=randint(1, 2)),
        ]
        for sh in ships:
            self._ships.append(sh)

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
    def __check_collision(ships, ghost_ships=None, lst_ln=None):
        ships_1 = ships
        if ghost_ships is not None:
            ships_2 = ghost_ships
            lst_ln = ships_1
        else:
            ships_2 = ships
            lst_ln = ships
        count = 0
        if len(lst_ln) < 2:
            return True
        for i in range(len(ships_1)):
            for j in range(len(ships_2)):
                if i != j:
                    print(f'check: {i+1} - {j+1}')
                    if ships_1[i].is_collide(ships_2[j]):
                        print(f'is collide: '
                              f'{i + 1}: ({ships_1[i]._x}, '
                              f'{ships_1[i]._y}) ln:{ships_1[i]._length} | '
                              f'{j + 1}: ({ships_2[j]._x}, '
                              f'{ships_2[j]._y}) ln:{ships_2[j]._length}')
                        count += 1
                        print('-' * 30)
        if count > 0:
            print()
            print('- count collisions:', count)
        else:
            print('- NO collision!')
        print('-' * 30)
        if count > 0:
            return False
        return True

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
            ship_position = self.__check_position(x,
                                                  y,
                                                  ship._tp,
                                                  ship._length,
                                                  ship.is_out_pole(self._size),
                                                  ship._cells_iter)

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
        if not go + coord in range(0, size - ln):
            return False
        return True

    @staticmethod
    def __check_go_collision(ghost_ship, ships, ghost_ships):
        if len(ghost_ships) < 2:
            result = all(map(lambda ships: ghost_ship.is_collide(ships), ships))
        else:
            result = all(map(lambda ships: ghost_ship.is_collide(ships), ghost_ships))
        if result:
            return False
        return True

    def move_ships(self):
        self.reset_pole()
        for num, ship in enumerate(self._ships):
            positive = 1
            negative = -1
            go = choice([positive, negative])
            print('-' * 20)
            print(f'->> GO_generate: {go}')
            if ship._tp == 1:
                print(f'HAVE_tp: {ship._tp} = {ship.build_ship_tuples(ship)}')
                self._ships_move.append(Ship(
                    ship._length,
                    ship._tp,
                    ship.move(go)[0],
                    ship.move(go)[1],
                ))
                
                ###############################################################
                # for i in self._ships_move:
                #     print('_check_ship: ', i._length, 'tp:', i._tp)
                # print(f'GO_check_collision: {self.__check_collision(self._ships_move)}')
                # print(f'GO_check_perimetr: '
                #       f'{self.__check_go_perimetr(go, ship._x, self._size, ship._length)}')
                #
                # if ship._length == 4:
                #     if not self.__check_collision(self._ships_move, self._ships, self._ships) or \
                #             not self.__check_go_perimetr(go, ship._x, self._size, ship._length):
                #         go *= -1
                # else:
                #     if not self.__check_collision(self._ships_move) or \
                #             not self.__check_go_perimetr(go, ship._x, self._size, ship._length):
                #         go *= -1
                #     else:
                #         go
                # print(f'<<- GO_result: {go}')
                ###############################################################

                for i in range(ship._length):
                    for y, x in [ship.move(go)]:
                        self._pole[x][y + i] = next(ship._cells_move_iter)
                        contour = Ship.contour([(y + i, x)])
                        self.__fill_contour(contour)
                        print(f'({y + i}, {x})')
                print('-' * 30)

            if ship._tp == 2:
                print(f'HAVE_tp: {ship._tp} = {ship.build_ship_tuples(ship)}')
                self._ships_move.append(Ship(
                    ship._length,
                    ship._tp,
                    ship.move(go)[0],
                    ship.move(go)[1],
                ))
                ###############################################################
                # for i in self._ships_move:
                #     print('_check_ship: ', i._length, 'tp:', i._tp)
                # print(f'GO_check_collision: {self.__check_collision(self._ships_move)}')
                # print(f'GO_check_perimetr: '
                #       f'{self.__check_go_perimetr(go, ship._y, self._size, ship._length)}')
                #
                # if ship._length == 4:
                #     if not self.__check_collision(self._ships_move, self._ships, self._ships) or \
                #             not self.__check_go_perimetr(go, ship._y, self._size, ship._length):
                #         go *= -1
                # else:
                #     if not self.__check_collision(self._ships_move) or \
                #             not self.__check_go_perimetr(go, ship._y, self._size, ship._length):
                #         go *= -1
                #     else:
                #         go
                # print(f'<<- GO_result: {go}')
                ###############################################################

                for i in range(ship._length):
                    for y, x in [ship.move(go)]:
                        self._pole[x + i][y] = next(ship._cells_move_iter)
                        contour = Ship.contour([(y, x + i)])
                        self.__fill_contour(contour)
                        print(f'({y}, {x + i})')
                print('-' * 30)

    # def move_ships(self):
    #     self.reset_pole()
    #     for num, ship in enumerate(self._ships):
    #         positive = 1
    #         negative = -1
    #         go = choice([positive, negative])
    #         print(f'GO_gen: {go}')
    #         if ship._tp == 1:
    #             flag_x = self.__check_go_perimetr(go, ship._x, self._size, ship._length)
    #             if not flag_x:
    #                 go *= -1
    #             else: go
    #             print(f'_tp: {ship._tp} = {ship.build_ship_tuples(ship)}')
    #             print(f'GO_check_perimetr: {go} | {flag_x}')
    #
    #             self._ships_move.append(Ship(
    #                 ship._length,
    #                 ship._tp,
    #                 ship.move(go)[0],
    #                 ship.move(go)[1],
    #             ))
    #
    #             if not self.__check_collision(self._ships_move):
    #                 go *= -1
    #                 if self._ships_move[num].__dict__['_x'] + go \
    #                         in range(1, self._size - self._ships_move[num]._length):
    #                     self._ships_move[num].__dict__['_x'] += go
    #                 else: go = 0
    #             else: go
    #             print(f'GO_check_collision: {go} | {self.__check_collision(self._ships_move)}')
    #
    #             for i in range(ship._length):
    #                 for y, x in [ship.move(go)]:
    #                     self._pole[x][y + i] = next(ship._cells_move_iter)
    #                     contour = Ship.contour([(y + i, x)])
    #                     self.__fill_contour(contour)
    #                     print(f'({y + i}, {x})')
    #             print('-' * 20)
    #
    #         if ship._tp == 2:
    #             flag_y = self.__check_go_perimetr(go, ship._y, self._size, ship._length)
    #             if not flag_y:
    #                 go *= -1
    #             else: go
    #             print(f'_tp: {ship._tp} = {ship.build_ship_tuples(ship)}')
    #             print(f'GO_check_perimetr: {go} | {flag_y}')
    #
    #             self._ships_move.append(Ship(
    #                 ship._length,
    #                 ship._tp,
    #                 ship.move(go)[0],
    #                 ship.move(go)[1],
    #             ))
    #
    #             if not self.__check_collision(self._ships_move):
    #                 go *= -1
    #                 if self._ships_move[num].__dict__['_y'] + go \
    #                         in range(1, self._size - self._ships_move[num]._length):
    #                     self._ships_move[num].__dict__['_y'] += go
    #                 else: go = 0
    #             else: go
    #             print(f'GO_check_collision: {go} | {self.__check_collision(self._ships_move)}')
    #
    #             for i in range(ship._length):
    #                 for y, x in [ship.move(go)]:
    #                     self._pole[x + i][y] = next(ship._cells_move_iter)
    #                     contour = Ship.contour([(y, x + i)])
    #                     self.__fill_contour(contour)
    #                     print(f'({y}, {x + i})')
    #             print('-' * 20)

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








