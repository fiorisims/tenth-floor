"""The building: which floor is whose, and where the two elevators stop.

Every floor runs between two elevators: the WEST elevator at its left end and the EAST elevator at its
right end. You get off one, walk the floor's rooms west to east (two or more), and get on the other.
The West elevator stops at the lobby (and the basement) through floor 9; the East elevator stops at the
lobby through the top, including 10. The door on 10 still needs the code, and the code is on the floors.

Floors are found by file: every floors/<name>.py with its ROOMS (or LEFT and RIGHT) is in the game. Nobody edits
this file to add a floor, so a whole class can add floors at once without a merge conflict here.
The building has 12 floors (TOP_FLOOR) and a basement: the lobby on 1, MFA Computer Arts on 10, and 2 to 9,
11 and 12 for floors. The basement (B) holds the floors pinned to it in ASSIGN (two can share it), reached only by
the West elevator; the East elevator doesn't go down there, so its last room is a dead end. Floors listed in ASSIGN go where they're told. The rest fill 2 to 9, then 11 and 12, in
alphabetical order of file name. The example floors only take a floor nobody else has, so they leave the
building as it fills (they still run with main.py --floor). A student's floor is never left out: if there
are more of them than floors, the building grows past 12 to fit them.
"""
import importlib
import os
import pkgutil

GOAL = 10                # the floor you're trying to reach: MFA Computer Arts
TOP_FLOOR = 12           # SVA, 133/141 West 21st Street, has 12 floors (Isaac 11-17)
BASEMENT = 0             # below the lobby; only the West elevator goes down to it. Shown as "B".
PIECES_NEEDED = 8        # keycard pieces that unlock it (capped at the number of floors)

# Floor names on the elevator panel: SVA, 133/141 West 21st Street. Known (Isaac 11-14; sva.edu listings):
# the ground floor is the SVA Flatiron Gallery and the 10th floor is MFA Computer Arts. A student's floor
# shows its own NAME.
FLOOR_NAMES = {1: "Lobby / Flatiron Gallery", GOAL: "MFA Computer Arts"}

# Pin a floor file to a floor number: "file_name": 4. Everyone else is placed in order.
# The basement (0) is only used by floors pinned here. Two files pinned to the same number share that
# floor, west to east in the order listed: the library by the West elevator, then Mo's Cafe.
ASSIGN = {"fayth_elisa_navarro": BASEMENT, "mos_cafe": BASEMENT,
          "elise": 4, "brent_shultz": 6, "elle": 7, "yifan_wang": 11, "jerry_xu": 12}


class Floor:
    """One student's floor, read from floors/<name>.py."""

    def __init__(self, name, mod):
        self.file = name
        self.name = mod.NAME
        self.author = mod.AUTHOR
        # Rooms, west to east: ROOMS = [A, B, C, ...], or the two-room form LEFT = A and RIGHT = B.
        self.room_classes = list(mod.ROOMS) if hasattr(mod, "ROOMS") else [mod.LEFT, mod.RIGHT]


def load_floors(only=None):
    """Returns {file_name: Floor} for every floor file that imports. Broken files are skipped with a
    message so one bad floor can't stop the class's game; check.py is where they get caught."""
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "floors")
    found = {}
    for info in sorted(pkgutil.iter_modules([here]), key=lambda i: i.name):
        if info.name.startswith("_") or (only and info.name != only):
            continue
        try:
            mod = importlib.import_module("floors." + info.name)
            found[info.name] = Floor(info.name, mod)
        except Exception as e:  # noqa: BLE001 - a student's floor must not take the game down
            print(f"[skipped floor {info.name}: {type(e).__name__}: {e}]")
    return join_shared(found)


def join_shared(found):
    """Files pinned to the same floor number become one floor: their rooms west to east in ASSIGN order,
    both names on the panel, both authors. Each file still hides its own digit, and each one counts."""
    by_number = {}
    for f, n in ASSIGN.items():
        if f in found:
            by_number.setdefault(n, []).append(f)
    for n, files in by_number.items():
        if len(files) < 2:
            continue
        parts = [found.pop(f) for f in files]
        shared = parts[0]
        shared.file = "+".join(files)
        shared.name = " + ".join(p.name for p in parts)
        shared.author = " & ".join(p.author for p in parts)
        shared.room_classes = [c for p in parts for c in p.room_classes]
        shared.pin = n
        found[shared.file] = shared
    return found


def open_floors():
    """Floor numbers a student can have, in the order they fill: 2..9, then 11, 12, ..."""
    n = 2
    while True:
        if n != GOAL:
            yield n
        n += 1


def place(floors):
    """Returns {floor_number: file_name}."""
    where = {}
    pins = dict(ASSIGN)
    pins.update({name: fl.pin for name, fl in floors.items() if getattr(fl, "pin", None) is not None})
    for name, number in pins.items():
        if name in floors and number not in (1, GOAL):
            where[number] = name
    left = [n for n in floors if n not in where.values()]
    students = sorted(n for n in left if not n.startswith("example"))
    examples = sorted(n for n in left if n.startswith("example"))
    numbers = (n for n in open_floors() if n not in where)
    for name in students:
        where[next(numbers)] = name
    free = sum(1 for n in range(2, TOP_FLOOR + 1) if n != GOAL and n not in where)
    for name in examples[:free]:
        where[next(numbers)] = name
    return where


def basement_in_use():
    """True when a floor file pinned to the basement in ASSIGN is in floors/."""
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "floors")
    return any(n == BASEMENT and os.path.exists(os.path.join(here, f + ".py")) for f, n in ASSIGN.items())


def west_stops(top_floor):
    """The lobby to 9, and the basement too when a floor is down there."""
    return list(range(BASEMENT if basement_in_use() else 1, GOAL))


def east_stops(top_floor):
    """The lobby to the top, including 10: walk right through the gallery to board it."""
    return list(range(1, top_floor + 1))


def top(where):
    """The highest floor in the building: 12, or higher if more floors than that are built."""
    return max([TOP_FLOOR] + list(where))


def label(number):
    """What the elevator panel shows for a floor number: B for the basement."""
    return "B" if number == BASEMENT else str(number)


def floor_name(number, where, floors):
    if number in where:
        return floors[where[number]].name
    return FLOOR_NAMES.get(number, f"Floor {number}")
