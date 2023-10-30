from random import randint as rnd


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length: int = length
        self._tp: int = tp
        self._x: int = x
        self._y: int = y
        self._is_move = True
        self._cells = [1 for _ in range(length)]

    def set_start_coords(x, y):
        pass

    def get_start_coords():
        pass

    def move(go):
        pass

    def is_collide(ship):
        pass

    def is_out_pole(size):
        pass

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
            Ship(4, rnd(1, 2)),
            Ship(3, rnd(1, 2)),
            Ship(3, rnd(1, 2)),
            Ship(2, rnd(1, 2)),
            Ship(2, rnd(1, 2)),
            Ship(2, rnd(1, 2)),
            Ship(1, rnd(1, 2)),
            Ship(1, rnd(1, 2)),
            Ship(1, rnd(1, 2)),
            Ship(1, rnd(1, 2)),
        ]
        for sh in ships:
            self._ships.append(sh)

    def get_ships(self):
        return [x for x in self._ships]

    def move_ships():
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









