"""The ground floor, built with the engine: the security desk where you start, and the Flatiron Gallery's
hallway out to the West elevator. Students don't edit this; it shows the controls before anyone's floor."""
import pygame

from . import config as C
from .bots import PatrolBot
from .room import Furniture, Platform, Room

NAME = "Lobby / Flatiron Gallery"
AUTHOR = "the class"


class Artwork(Furniture):
    """A framed piece on a plinth. Searching it finds nothing; it's the gallery."""

    def __init__(self, x, y, w, h, name, colors):
        super().__init__(x, y, w, h, name)
        self.colors = colors

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, (225, 222, 214), r)                      # plinth
        pygame.draw.rect(surf, C.INK, r, 2)
        art = pygame.Rect(r.left + 6, r.top - 60, r.width - 12, 60)     # the piece, standing on top
        pygame.draw.rect(surf, self.colors[0], art)
        pygame.draw.circle(surf, self.colors[1], (art.centerx, art.centery), min(art.w, art.h) // 3)
        pygame.draw.rect(surf, (30, 30, 30), art, 3)


class GalleryHall(Room):
    """Left of the lobby: the gallery hallway. The West elevator is through its left wall."""

    title = "Flatiron Gallery"

    def build(self):
        self.furniture.append(Artwork(150, C.FLOOR_Y, 70, 50, "plinth 1", ((200, 90, 70), (240, 210, 120))))
        self.furniture.append(Artwork(420, C.FLOOR_Y, 70, 50, "plinth 2", ((60, 110, 170), (230, 230, 230))))
        self.platforms.append(Platform(600, 400, 170))                  # the mezzanine bench
        self.furniture.append(Artwork(640, 400, 70, 40, "plinth 3", ((90, 150, 100), (30, 40, 30))))
        self.furniture.append(Furniture(820, C.FLOOR_Y, 70, 30, "visitor bench"))
        # A slow guard bot that doesn't chase: jump over it (run and jump to flip).
        self.hazards.append(PatrolBot(300, C.FLOOR_Y, left=260, right=560, speed=55, sees=False))
        f = pygame.font.Font(None, 30)
        self.sign = f.render("SVA FLATIRON GALLERY", True, (40, 40, 44))
        self.hint = pygame.font.Font(None, 22).render(
            "WEST ELEVATOR  <--   run + SPACE to flip over a bot", True, (70, 70, 76))

    def draw_background(self, surf):
        surf.fill((236, 233, 226))                                       # white-cube walls
        for x in range(90, C.W, 210):                                    # track lights
            pygame.draw.line(surf, (190, 186, 178), (x, 36), (x + 40, 60), 3)
        for i, x in enumerate((110, 330, 760)):                          # works on the wall
            col = [(170, 60, 60), (40, 90, 140), (200, 160, 60)][i]
            pygame.draw.rect(surf, col, (x, 120, 110, 140))
            pygame.draw.rect(surf, (30, 30, 30), (x, 120, 110, 140), 3)
        surf.blit(self.sign, (C.W // 2 - self.sign.get_width() // 2, 46))
        surf.blit(self.hint, (20, 300))


class SecurityDesk(Room):
    """Right of the lobby: where the game starts. The East elevator is through its right edge."""

    title = "Security Desk"

    def build(self):
        self.furniture.append(Furniture(560, C.FLOOR_Y, 160, 60, "security desk"))
        self.furniture.append(Furniture(360, C.FLOOR_Y, 40, 70, "turnstile"))
        self.furniture.append(Furniture(160, C.FLOOR_Y, 60, 90, "coat rack"))
        self.platforms.append(Platform(760, 400, 150))
        self.furniture.append(Furniture(790, 400, 60, 40, "monitor bank"))
        f = pygame.font.Font(None, 30)
        self.sign = f.render("SVA  -  133/141 WEST 21ST STREET", True, (220, 220, 228))
        small = pygame.font.Font(None, 24)
        self.lines = [small.render(t, True, (200, 204, 214)) for t in (
            "After hours. MFA Computer Arts is on floor 10, and its door takes a code.",
            "Every floor hides one digit. Hold UP at furniture to search it.",
            "West elevator: the basement up to 9. East elevator, to the right: here to the top.",
            "Walk across a floor to switch elevators.   <-- West      East -->")]

    def draw_background(self, surf):
        surf.fill((44, 48, 60))
        pygame.draw.rect(surf, (58, 62, 78), (0, 300, C.W, 200))         # marble wainscot
        surf.blit(self.sign, (C.W // 2 - self.sign.get_width() // 2, 46))
        for i, img in enumerate(self.lines):
            surf.blit(img, (40, 110 + i * 30))


LEFT = GalleryHall
RIGHT = SecurityDesk
