
import enum
from collections import namedtuple


Pos = namedtuple("Pos", ["r", "c"])


def batch(it, sz):
    for i in range(0, len(it), sz):
        yield it[i:i+sz]



class Direction(enum.Enum):
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()

    @staticmethod
    def go(d, orig):
        if d == Direction.Up:
            p = Pos(orig.r - 1, orig.c)
        elif d == Direction.Down:
            p = Pos(orig.r + 1, orig.c)
        elif d == Direction.Left:
            p = Pos(orig.r, orig.c - 1)
        elif d == Direction.Right:
            p = Pos(orig.r, orig.c + 1)
        return p



class Tile(enum.Enum):
    Crate = enum.auto()
    Floor = enum.auto()
    Wall = enum.auto()



class State:
    def __init__(self):
        self.container = {}
        self.player = Pos(0, 0)
        self.targets = []
        self.moves = 0
        self.dim_r = 0
        self.dim_c = 0

    def check_bounds(self, pos):
        return pos.r < self.dim_r and pos.c < self.dim_c

    @staticmethod
    def new(raw, player, targets, dim_r, dim_c):
        s = State()
        s.container = raw
        s.player = player
        s.targets = targets
        s.dim_r = dim_r
        s.dim_c = dim_c
        return s

    def in_solution_state(self):
        return all([self.container.get(t) == Tile.Crate for t in self.targets])

    def move_player(self, direction):
        next_pos = Direction.go(direction, self.player)
        if not self.check_bounds(next_pos):
            return False  # InvalidMoveOOB

        t = self.container[next_pos]
        if t == Tile.Crate:
            cnext_pos = Direction.go(direction, next_pos)
            if not self.check_bounds(cnext_pos):
                return False  # InvalidMoveCrate
            if self.container.get(cnext_pos) != Tile.Floor:
                return False  # InvalidMoveCrate
            self.container[next_pos] = Tile.Floor
            self.container[cnext_pos] = Tile.Crate
        elif t == Tile.Wall:
            return False  # InvalidMoveCrate
        self.player = next_pos
        self.moves += 1
        return True

    def print(self):
        outp = "\n".join([i for i in batch(str(self), self.dim_c)])
        return outp

    @staticmethod
    def fromtext(text, r, c):
        container = {}
        player = Pos(0, 0)
        targets = []
        for i, s in enumerate(text):
            pos = Pos(i // c, i % c)
            if s in ["W", "w"]:
                newt = Tile.Wall
            elif s in ["E", "e"]:
                newt = Tile.Floor
                if s == "E":
                    targets.append(pos)
            elif s in ["M", "m"]:
                newt = Tile.Floor
                if s == "M":
                    targets.append(pos)
                player = pos
            elif s in ["O", "o"]:
                newt = Tile.Crate
                if s == "O":
                    targets.append(pos)
            container[pos] = newt
        return State.new(container, player, targets, r, c)

    def __str__(self):
        outp = ''
        for r in range(0, self.dim_r):
            for c in range(0, self.dim_c):
                pos = Pos(r, c)
                t = self.container.get(pos)
                if t is None:
                    outp += '?'
                elif pos == self.player:
                    if pos in self.targets:
                        outp += "M"
                    else:
                        outp += "m"
                elif t == Tile.Floor:
                    if pos in self.targets:
                        outp += "E"
                    else:
                        outp += "."
                elif t == Tile.Wall:
                    outp += "w"
                elif t == Tile.Crate:
                    if pos in self.targets:
                        outp += "O"
                    else:
                        outp += "o"
        return outp


