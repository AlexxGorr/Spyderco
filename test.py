from random import randint as rnd


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length: int = length
        self._tp: int = tp
        self._x: int = x
        self._y: int = y
        self._is_move = True
        self._cells = [1 for _ in range(length)]

    @staticmethod
    def set_start_coords(x, y):
        x = rnd(0, 9)
        y = rnd(0, 9)
        return x, y

    def get_start_coords(self):
        return self.set_start_coords(self._x, self._y)

    def dots(self):
        ship_dots = []
        for i in self._cells:
            coor_x = self.get_start_coords()[0]
            coor_y = self.get_start_coords()[1]
            if self._tp == 1:
                coor_x += i
            if self._tp == 2:
                coor_y += i
            ship_dots.append((coor_x, coor_y))
        return ship_dots

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
        if coord_collide != '0':
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
print(ship.get_start_coords())
print(ship.dots())



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
            print(*['0' for _ in range(self._size)])

    def get_pole(self):
        return [[x for x in range(self._size)] for y in range(self._size)]


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()

pole.move_ships()
print()
pole.show()















