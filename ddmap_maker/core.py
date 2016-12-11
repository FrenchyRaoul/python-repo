from pygame import Rect
from random import randint


class Room(Rect):
    def __init__(self, left, top, width, height, floor):
        super().__init__((left, top), (width, height))
        self.floor = floor


class Passageway(Rect):
    def __init__(self, left, top, width, height):
        super().__init__((left, top), (width, height))


class Hallway(Passageway):
    def __init__(self, left, top, width, height, length):
        super().__init__(left, top, width, height)
        self.length = length


class Doorway(Passageway):
    def __init__(self, centerpoint: tuple=(0, 0), direction: str='east-west'):
        x, y = centerpoint
        width = 3
        depth = 1
        if direction == 'east-west':
            super().__init__(x - 0.5*depth, y + 0.5*width, depth, width)
        elif direction == 'north-south':
            super().__init__(x - 0.5*width, y + 0.5*depth, width, depth)


class Stairway(Passageway):
    def __init__(self, centerpoint: tuple=(0, 0), top_floor: int=1,
                 bottom_floor: int=0, length: int=6):
        super().__init__(1, 2, 3, 4)
        self.top_floor = top_floor
        self.bottom_floor = bottom_floor
        self.length = length
        self.width = 3

    @property
    def ave_slope(self):
        return 6 / self.length * (self.top_floor - self.bottom_floor)


def rand_room(minx=10, maxx=100, miny=10, maxy=100, floor=0):
    return Room(0, 0, randint(minx, maxx), randint(miny, maxy), floor=floor)


def layout_rooms(room_list, entrance='North'):
    entrance = Rect(room_list[0].left, -1000, room_list[0].width, 1000)
    for room in room_list:
        pass


class DDmap(object):
    def __init__(self, map_type: str, level: int=0):
        self.map_type = map_type
        self.level = level


class Cave(DDmap):
    def __init__(self, level: int=0):
        super().__init__(map_type='cave', level=level)


class Dungeon(DDmap):
    def __init__(self, level: int=0):
        super().__init__(map_type='dungeon', level=level)
