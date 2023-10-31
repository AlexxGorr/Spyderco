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

    def move(self, go):
        go = 0
        if self._is_move:
            go += 1

    def is_collide(self, ship):
        contour = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        coord_collide = (0, 0)
        for i in ship:
            for dx, dy in contour:
                coord_collide = i._x + dx, i._y + dy
        if coord_collide == self.get_start_coords():
            return True

    def is_out_pole(self, size):
        if self._x not in range(size) or self._y not in range(size):
            return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


ship = Ship(5)
print(ship.__dict__)

val = ship[2]
print(val)

ship[2] = 4
print(ship._cells)


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

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

    def get_ships(self):
        return [x for x in self._ships]

    def move_ships(self):
        pass

    def show(self):
        for i in range(self._size):
            print(*[0 for _ in range(self._size)])

    def get_pole(self):
        return [[x for x in range(self._size)] for y in range(self._size)]


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()

pole.move_ships()
print()
pole.show()















