class Vertex:
    # ID_POINT = 0

    def __init__(self):
        self._links = []
        # Vertex.ID_POINT += 1
        # self._id = Vertex.ID_POINT

    @property
    def links(self):
        return self._links

    # @links.setter
    # def links(self, link):
    #     self._links = link


# class Descripter_link:
#     def __set_name__(self, owner, name):
#         self.name = '_' + name
#         # self.keyname = name
#
#     def __get__(self, instance, owner):
#         if instance is not None:
#             return property()
#         return getattr(instance, self.name)
#
#     # def __set__(self, instance, value):
#     #     if self.keyname in ('v1', 'v2') and not isinstance(value, Vertex) or \
#     #             self.keyname == 'dist' and value < 1:
#     #         raise ValueError('Link attr error!')
#     #     setattr(instance, self.name, value)


class Link:
    # v1 = Descripter_link()
    # v2 = Descripter_link()
    # dist = Descripter_link()

    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        # res1 = tuple(filter(lambda x: Link(x.v1, x.v2) in self._links, self._links))
        # res2 = tuple(filter(lambda x: Link(x.v2, x.v1) in self._links, self._links))
        # # res1 = tuple(filter(lambda x: id(x.v1) == id(link.v1) and id(x.v2) == id(link.v2), self._links))
        # # res2 = tuple(filter(lambda x: id(x.v1) == id(link.v2) and id(x.v2) == id(link.v1), self._links))
        # if len(res1) == 0 or len(res2) == 0:
        #     self._links.append(link)
        #     self.add_vertex(link.v1)
        #     self.add_vertex(link.v2)
        #     link.v1.links.append(link)
        #     link.v1.links.append(link)

        ##############################################################

        res = tuple(filter(lambda x: id(x.v1) == id(link.v1) and id(x.v2) == id(link.v2) or \
                           id(x.v2) == id(link.v1) and id(x.v1) == id(link.v2), self._links))
        if len(res) == 0:
            self._links.append(link)
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)
            link.v1.links.append(link)
            link.v1.links.append(link)

    def find_path(self, start_v, stop_v):
        self._start = start_v
        self._stop = stop_v
        return self.step_next(self._start, None, [], [])

    def distant(self, links):
        return sum([x.dist for x in links if x is not None])

    def step_next(self, current, prev, cur_path, cur_link):
        cur_path += [current]
        if prev:
            cur_link += [prev]
        if current == self._stop:
            return cur_path, cur_link
        best_path = []
        best_link = []
        len_path = -1
        for link in current.links:
            temp_path = []
            temp_link = []
            if link.v1 not in cur_path:
                temp_path, temp_link = self.step_next(link.v1, link, cur_path.copy(), cur_link.copy())
            elif link.v2 not in cur_path:
                temp_path, temp_link = self.step_next(link.v2, link, cur_path.copy(), cur_link.copy())
            if self._stop in temp_path and (len_path > self.distant(temp_link) or len_path == -1):
                len_path = self.distant(temp_link)
                best_path = temp_path.copy()
                best_link = temp_link.copy()
        return best_path, best_link


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def __repr__(self):
        # return f'{self._id} - {self._name}'
        return self._name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist


# map_graph = LinkedGraph()
#
# v1 = Vertex()
# v2 = Vertex()
# v3 = Vertex()
# v4 = Vertex()
# v5 = Vertex()
# v6 = Vertex()
# v7 = Vertex()
#
# map_graph.add_link(Link(v1, v2))
# map_graph.add_link(Link(v2, v3))
# map_graph.add_link(Link(v1, v3))
#
# map_graph.add_link(Link(v4, v5))
# map_graph.add_link(Link(v6, v7))
#
# map_graph.add_link(Link(v2, v7))
# map_graph.add_link(Link(v3, v4))
# map_graph.add_link(Link(v5, v6))
#
#
# print(len(map_graph._links))   # 8 связей
# print(len(map_graph._vertex))  # 7 вершин
# path = map_graph.find_path(v1, v6)
#
# for i in map_graph.__dict__:
#     print(i)
#
# for i in v1.links:
#     print(id(i))

################################################################

map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7

print('-' * 30)
for i in v1.links:
    print(i.__dict__)

print('-' * 30)
for i in v2.links:
    print(i.__dict__)

print('-' * 30)
for i in v3.links:
    print(i.__dict__)














