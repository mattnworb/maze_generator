from enum import Enum
import random


class Direction(Enum):
    north = 1
    south = 2
    west = 3
    east = 4

    def opposite(self):
        if self.value % 2 == 0:
            return Direction(self.value - 1)
        return Direction(self.value + 1)


def next_pos(pos, direction):
    """Determines next position after moving in direction from position.
    Positions are represented as a tuple of (x, y)"""
    if direction == Direction.north:
        return (pos[0], pos[1] - 1)
    if direction == Direction.south:
        return (pos[0], pos[1] + 1)
    if direction == Direction.west:
        return (pos[0] - 1, pos[1])
    if direction == Direction.east:
        return (pos[0] + 1, pos[1])


class MazeUnit(object):
    """A single unit in a Maze. Has four walls which can either exist or not exist"""
    def __init__(self):
        self.north, self.south, self.west, self.east = True, True, True, True


class Maze(object):
    """A maze is an X by Y grid of MazeUnits"""
    def __init__(self, x_size, y_size):
        self.size = (x_size, y_size)
        self.units = {}
        for x in range(x_size):
            for y in range(y_size):
                self.units[(x, y)] = MazeUnit()

    def knockdown_wall(self, pos, direction):
        """Knocks down the wall in direction from position pos"""
        if pos not in self.units:
            raise IndexError('Position {0} is out of bounds for {1}'.format(pos, repr(self)))

        pos2 = next_pos(pos, direction)
        if pos2 not in self.units:
            raise IndexError("Cannot move {0} from {1}".format(direction, pos))

        # we knock down two "walls", the one in direction and the wall in the next MazeUnit on the opposite side
        # (this is a place where this type of representation is not great)
        unit = self.units[pos]
        unit2 = self.units[pos2]

        if direction == Direction.west:
            unit.west = False
            unit2.east = False

        if direction == Direction.east:
            unit.east = False
            unit2.west = False

        if direction == Direction.north:
            unit.north = False
            unit2.south = False

        if direction == Direction.south:
            unit.south = False
            unit2.north = False

    def __str__(self):
        s = ''
        # top border
        for x in range(self.size[0]):
            if self.units[(x, 0)].north:
                s += ' _'
            else:
                s += '  '
        s += '\n'

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                unit = self.units[(x, y)]
                if unit.west:
                    s += '|'
                else:
                    s += ' '
                if unit.south:
                    s += '_'
                else:
                    s += ' '
                # add right wall only on last pos
                if x == self.size[0] - 1 and unit.east:
                    s += '|'
            s += '\n'

        return s


class MazeWalker(object):
    def __init__(self, maze, starting_position=(0, 0)):
        self.maze = maze
        self.pos = starting_position
        self.pos_history = []
        self.visited_positions = set()

    def allowed_move(self, pos, direction):
        """Tests if moving in direction from pos is allowed based on maze bounds. Doesn't care about walls"""
        if pos not in self.maze.units:
            raise IndexError('Position (%d, %d) is out of bounds for %s' % (pos[0], pos[1], repr(self)))

        np = next_pos(pos, direction)
        return np in self.maze.units and np not in self.visited_positions

    def all_visited(self):
        remaining = set(self.maze.units.keys()) - self.visited_positions
        return len(remaining) == 0

    def solve(self, verbose=False):
        ## from current position, figure out what moves are possible
        ## if there are moves, pick one at random
        ## if there are no moves, go backwards one step in history

        #counter = 0
        #while not self.all_visited() and counter < 1000000:
        #    if verbose:
        #        print 'Round', counter
        #    counter += 1

        #    choices = set(Direction)
        #    for d in Direction:
        #        if not self.allowed_move(self.pos, d):
        #            choices.remove(d)

        #    if verbose:
        #        print 'Possible moves from {0}: {1}'.format(self.pos, choices)

        #    if len(choices) > 0:
        #        direction = random.choice(list(choices))
        #        if verbose:
        #            print 'Moving {0} from {1}'.format(direction, self.pos)

        #        self.maze.knockdown_wall(self.pos, direction)
        #        self.pos_history.append(self.pos)
        #        self.visited_positions.add(self.pos)

        #        self.pos = next_pos(self.pos, direction)
        #    else:
        #        if verbose:
        #            print 'No moves valid from {0}, backtracking to {1}'.format(self.pos, self.pos_history[-1])
        #        self.visited_positions.add(self.pos)
        #        self.pos = self.pos_history[-1]
        #        self.pos_history = self.pos_history[:-1]
        #    if verbose:
        #        print self.maze

        ## are we all done after the loop?
        #return (self.all_visited(), counter)
        try:
            self.step((0, 0))
        except RuntimeError as e:
            print self.maze
            print e

    def step(self, pos):
        self.visited_positions.add(pos)

        choices = list(Direction)
        random.shuffle(choices)

        for direction in choices:
            if self.allowed_move(pos, direction):
                print 'From {0}, moving {1}'.format(pos, direction)

                self.maze.knockdown_wall(pos, direction)
                #self.pos_history.append(self.pos)

                self.step(next_pos(pos, direction))

         

if __name__ == '__main__':
    mw = MazeWalker(Maze(60, 50))
    solved = mw.solve()
    print 'Solved?', solved
    print mw.maze
