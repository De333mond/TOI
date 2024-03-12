import time

from lab5.ui.config import UIConfig


def forced_ups(ups):
    def _forced_ups(func):
        def wrapped(*args, **kwargs):
            if ups == 0:
                return func(*args, **kwargs)

            start = time.time()
            res = func(*args, **kwargs)
            delay = 1/ups - (time.time() - start)

            time.sleep(delay if delay > 0 else 0)
            return res

        return wrapped

    return _forced_ups


def coords_from_num(num: int):
    num_to_coords = {
        0: (-1, -1),
        1: (0, -1),
        2: (1, -1),
        3: (0, 1),
        4: (1, 1),
        5: (0, 1),
        6: (-1, 1),
        7: (-1, 0),
    }

    return num_to_coords[num]