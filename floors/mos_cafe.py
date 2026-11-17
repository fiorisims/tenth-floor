"""Mo's Cafe: Nora Wentz's floor (claim #3), from a starter.

It shares the basement (floor B) with the Basement Library: the library is by the West elevator, and the
cafe carries on to the east. The East elevator doesn't come down to the basement, so the far end of the cafe
is a dead end; walk back through the library to leave. Whoever claims this floor makes it theirs: change
AUTHOR, then rebuild any room you like. Practise it alone with: python main.py --floor mos_cafe
"""
from engine import config as C
from engine.kit import (CeilingLight, Couch, Desk, FloorLaser, PatrolBot, Plant, Poster, Sign, VendingMachine,
                        Window)
from engine.room import Platform, Room

NAME = "Mo's Cafe"
AUTHOR = "Nora Wentz"


class Counter(Room):
    """The counter and the espresso shelf. The digit is in the vending machine up on the shelf."""

    title = "Mo's Cafe: the counter"

    def build(self):
        self.decor += [Sign(400, 46, "MO'S CAFE"), CeilingLight(260), CeilingLight(700),
                       Poster(120, 90, "COFFEE", (150, 100, 60)), Poster(820, 90, "OPEN", (80, 140, 90))]
        self.platforms.append(Platform(260, 420, 160))        # the counter top
        self.platforms.append(Platform(500, 330, 220))        # the shelf behind it
        self.furniture += [Desk(130, C.FLOOR_Y), Plant(450, C.FLOOR_Y), VendingMachine(600, 330, holds_piece=True),
                           Desk(780, C.FLOOR_Y)]
        self.hazards.append(PatrolBot(520, C.FLOOR_Y, left=440, right=860, speed=80))


class Seating(Room):
    """Tables, couches and a dead end: the East elevator doesn't come down to the basement."""

    title = "Mo's Cafe: seating"

    def build(self):
        self.decor += [Window(150, 70, seed=3), Window(620, 70, seed=4), CeilingLight(480), Sign(380, 46, "SEATING")]
        self.furniture += [Couch(140, C.FLOOR_Y), Desk(380, C.FLOOR_Y), Desk(560, C.FLOOR_Y), Couch(740, C.FLOOR_Y),
                           Plant(880, C.FLOOR_Y)]
        self.hazards.append(FloorLaser(320, 560, on_time=1.1, off_time=1.7))


ROOMS = [Counter, Seating]
