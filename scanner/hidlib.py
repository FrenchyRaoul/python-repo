import hid
import time
from collections import deque as dq


hid_dict = {0: None,
            1: "ErrorRollOver",
            2: "POSTFail",
            3: "ErrorUnidentified",
            4: 'a',
            5: 'b',
            6: 'c',
            7: 'd',
            8: 'e',
            9: 'f',
            10: 'g',
            11: 'h',
            12: 'i',
            13: 'j',
            14: 'k',
            15: 'l',
            16: 'm',
            17: 'n',
            18: 'o',
            19: 'p',
            20: 'q',
            21: 'r',
            22: 's',
            23: 't',
            24: 'u',
            25: 'v',
            26: 'w',
            27: 'x',
            28: 'y',
            29: 'z',
            30: 1,
            31: 2,
            32: 3,
            33: 4,
            34: 5,
            35: 6,
            36: 7,
            37: 8,
            38: 9,
            39: 0
            }


def decode_hid(code_list):
    return [hid_dict.get(code) for code in code_list]


class KeyboardBarcode(hid.device):

    CODE = ([0, 0, 31, 0, 0, 0, 0, 0],
            [0, 0, 38, 0, 0, 0, 0, 0],
            [0, 0, 37, 0, 0, 0, 0, 0],
            [0, 0, 38, 0, 0, 0, 0, 0],
            [0, 0, 39, 0, 0, 0, 0, 0],
            [0, 0, 36, 0, 0, 0, 0, 0],
            [0, 0, 34, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
           )

    def __init__(self):
        super().__init__()
        self.buffer = dq(self.CODE)
        self.iterator = self.iter_buffer()
        self.blocking = True

    def iter_buffer(self):
        while True:
            if self.buffer:
                yield self.buffer.popleft()
                yield [0, 0, 0, 0, 0, 0, 0, 0]
            else:
                if self.blocking:
                    self.poll_for_keypress()
                    time.sleep(0.5)
                else:
                    yield []

    def read(self, n):

        return next(self.iterator)[:n]

#     def open(self, *args, **kwargs):
#         super

    def poll_for_keypress(self):
        code = []
        while not any(code):
            code = super().read(8)
        while any(code):
            code = super().read(8)
        self.buffer.extend(self.CODE)

    def set_nonblocking(self, setting):
        self.blocking = not setting
