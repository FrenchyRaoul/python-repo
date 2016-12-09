from pygame import Rect
from random import randint


class Passageway(Rect):
    def __init__(self, left, top, width, height):
        super().__init__((left, top), (width, height))


class Doorway(Passageway):
    def __init__(self, centerpoint, direction='east-west'):
        x, y = centerpoint
        width = 3
        depth = 1
        if direction == 'east-west':
            super().__init__(x - 0.5*depth, y + 0.5*width, depth, width)
        elif direction == 'north-south':
            super().__init__(x - 0.5*width, y + 0.5*depth, width, depth)


class Room(Rect):
    def __init__(self, left, top, width, height):
        super().__init__((left, top), (width, height))


def rand_room(minx=10, maxx=100, miny=10, maxy=100):
    return Room(0, 0, randint(minx, maxx), randint(miny, maxy))


def layout_rooms(room_list, entrance='North'):
    entrance = Rect(room_list[0].left, -1000, room_list[0].width, 1000)
    for room in room_list:
        pass


class ddmap(object):
    def __init__(self, map_type):
        self.map_type = map_type


class Dungeon(ddmap):
    def __init__(self, *args, **kwargs):
        a = 1