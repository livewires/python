#------------------------------------------------------------------------------
# GameBoard and GameCell classes.
#
# $Revision: 1.2 $ -- $Date: 2005/07/06 21:08:14 $
#------------------------------------------------------------------------------
# Copyright Rhodri James.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither name of Scripture Union nor LiveWires nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SCRIPTURE UNION
# OR THE CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------


from livewires import games
from livewires import colour
from pygame.constants import *
from random import randint

DEFAULT_LINE_COLOUR   = colour.black
DEFAULT_FILL_COLOUR   = colour.light_grey
DEFAULT_CURSOR_COLOUR = colour.red

LEFT = 0
UP_LEFT = 1
UP = 2
UP_RIGHT = 3
RIGHT = 4
DOWN_RIGHT = 5
DOWN = 6
DOWN_LEFT = 7

def turn_45_clockwise(direction):
    return (direction + 1) % 8

def turn_45_anticlockwise(direction):
    return (direction - 1) % 8

def turn_90_clockwise(direction):
    return (direction + 2) % 8

def turn_90_anticlockwise(direction):
    return (direction - 2) % 8

def turn_180(direction):
    return (direction + 4) % 8

def random_direction(orthogonal_only = 0):
    if orthogonal_only:
        return 2 * randint(0, 3)
    return randint(0, 7)


class GameCell(games.Polygon):
    """
    A square cell on a square grid (i.e., a GameBoard).
    In typical applications this will be subclassed.
    """
    def __init__(self, board, i, j,
                 line_colour = DEFAULT_LINE_COLOUR, fill_colour = DEFAULT_FILL_COLOUR):
        self.init_gamecell(board, i, j, line_colour, fill_colour)

    def init_gamecell(self, board, i, j, line_colour = DEFAULT_LINE_COLOUR,
                                         fill_colour = DEFAULT_FILL_COLOUR):
        """
        Arguments:

        board -- The board this lives on.
        i -- Column number within the grid, starting at 0 at the left.
        j -- Row number within the grid, starting with 0 at the top.
        line_colour -- Colour of edges.
        fill_colour -- Colour of interior of cell.

        Creating grid cells is usually the job of the GridBoard
        object.
        """

        self.board = board

        (self.screen_x, self.screen_y) = board.cell_to_coords(i, j)
        box_size = board.box_size
        shape = ((0, 0), (0, box_size), (box_size, box_size), (box_size, 0))

        self.init_polygon(board.screen, self.screen_x, self.screen_y, shape,
                          fill_colour, filled=1, outline=line_colour, static=1)

        self.neighbours = []
        self.direction = [ None ] * 8
        self.grid_x = i
        self.grid_y = j

    def add_neighbour(self, neighbour):
        """
        What it says. Let this cell know that |neighbour| is one of
        its neighbours. This should be called for all pairs of cells
        when the grid is created. This establishes the connection
        only in one direction.
        """
        self.neighbours.append(neighbour)

    def add_direction(self, direction, cell):
        """
        Let this cell know that the |cell| given is in the direction
        |direction| from it.  This should be called for all appropriate
        pairs of cells when the grid is created, if the fast reference
        to neighbouring cells is needed.  It is most often of use if
        the board wraps at the edges, so a piece going off the top
        reenters at the bottom.  This establishes the connection in
        one direction only.
        """
        self.direction[direction] = cell


class GameBoard:
    """
    A square grid of cells, each an instance of the GameCell class.
    Typically, GameBoard and GameCell will both be subclassed,
    and the new_gamecell method overridden so that it creates
    cells of the correct class.
    """

    def __init__(self, screen, origin, n_cols, n_rows, box_size,
                 line_colour = DEFAULT_LINE_COLOUR,
                 fill_colour = DEFAULT_FILL_COLOUR,
                 cursor_colour = DEFAULT_CURSOR_COLOUR):
        self.init_gameboard(screen, origin, n_cols, n_rows,
                            line_colour, fill_colour, cursor_colour)

    def init_gameboard(self, screen, origin, n_cols, n_rows, box_size,
                       line_colour = DEFAULT_LINE_COLOUR,
                       fill_colour = DEFAULT_FILL_COLOUR,
                       cursor_colour = DEFAULT_CURSOR_COLOUR):
        """
        Arguments:
        screen -- The screen on which this board lives.
        origin -- A tuple (x,y) giving the coords of the top left corner.
        n_cols -- The number of columns in the grid.
        n_rows -- The number of rows in the grid.
        box_size -- The total width and height of each cell.
        line_colour -- The colour of the grid lines.
        fill_colour -- The colour of the interior of each cell.
        cursor_colour -- The colour in which the edges of a cell
                         should be highlighted when the "cursor"
                         is over it.

        Initially, there is no cursor.
        """

        self._origin = origin
        self._n_cols = n_cols
        self._n_rows = n_rows
        self.box_size = box_size
        self.grid = []
        self.cursor = None
        self.screen = screen

        self._line_colour = line_colour
        self._fill_colour = fill_colour
        self._cursor_colour = cursor_colour

        self.key_movements = {
            K_UP:    (0,-1),
            K_DOWN:  (0,1),
            K_LEFT:  (-1,0),
            K_RIGHT: (1,0)
        }

        for i in xrange(n_cols):
            self.grid.append([])
            for j in xrange(n_rows):
                if self.on_board(i,j):
                    self.grid[i].append(self.new_gamecell(i, j))
                else:
                    self.grid[i].append(None)

    def cell_to_coords(self, i,j):
        """
        Return the pixel coordinates of the top-left corner
        of the cell whose "board coordinates" are (i,j).
        """
        return (self._origin[0] + i*self.box_size,
                self._origin[1] + j*self.box_size)

    def coords_to_cell(self, x,y):
        """
        Return the "board coordinates" of the cell in which
        the point (x,y) in pixel coordinates lies.
        """
        # This is integer division below. Take care in future
        # versions of Python where dividing integers yields a float.
        return ((x-self._origin[0])/self.box_size,
                (y-self._origin[1])/self.box_size)

    def new_gamecell(self, i, j):
        """
        Create and return a new GameCell object at (i,j)
        in the grid. Subclass this if you need a proper subclass
        of GameCell instead.
        """
        return GameCell(self, i, j,
                        self._line_colour, self._fill_colour)

    def create_neighbours(self, orthogonal_only = 0):
        """
        Call the add_neighbour method for each pair of adjacent cells
        in the grid. If orthogonal_only is true, a cell has 4 neighbours;
        otherwise, 8 neighbours.
        """
        for i in xrange(self._n_cols):
            for j in xrange(self._n_rows):
                if not self.on_board(i,j):
                    continue
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        if k==l==0 or not self.on_board(i+k,j+l):
                            continue
                        if k <> l and k <> -l:
                            self.grid[i][j].add_neighbour(self.grid[i+k][j+l])
                        elif not orthogonal_only and k <> 0 and l <> 0:
                            self.grid[i][j].add_neighbour(self.grid[i+k][j+l])

    def create_directions(self, orthogonal_only = 0, wrap = 0):
        """
        Call the add_direction method for each pair of adjacent cells
        in the grid. If orthogonal_only is true, a cell has 4 neighbours;
        otherwise, 8 neighbours.  If wrap is true, a cell on the edge of
        the board has neighbours on the opposite edge, otherwise it has
        no neighbour in that direction.
        """
        for i in xrange(self._n_cols):
            for j in xrange(self._n_rows):
                if not self.on_board(i, j):
                    continue
                if i <> 0 or wrap:
                    k = (i-1) % self._n_cols
                    if self.on_board(k, j):
                        self.grid[i][j].add_direction(LEFT, self.grid[k][j])
                    if not orthogonal_only:
                        if j <> 0 or wrap:
                            l = (j-1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(UP_LEFT, self.grid[k][l])
                        if j <> self._n_rows-1 or wrap:
                            l = (j+1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(DOWN_LEFT, self.grid[k][l])
                if i <> self._n_cols-1 or wrap:
                    k = (i+1) % self._n_cols
                    if self.on_board(k, j):
                        self.grid[i][j].add_direction(RIGHT, self.grid[k][j])
                    if not orthogonal_only:
                        if j <> 0 or wrap:
                            l = (j-1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(UP_RIGHT, self.grid[k][l])
                        if j <> self._n_rows-1 or wrap:
                            l = (j+1) % self._n_rows
                            if self.on_board(k, l):
                                self.grid[i][j].add_direction(DOWN_RIGHT, self.grid[k][l])
                if j <> 0 or wrap:
                    l = (j-1) % self._n_rows
                    if self.on_board(i, l):
                        self.grid[i][j].add_direction(UP, self.grid[i][l])
                if j <> self._n_rows-1 or wrap:
                    l = (j+1) % self._n_rows
                    if self.on_board(i, l):
                        self.grid[i][j].add_direction(DOWN, self.grid[i][l])

    def map_grid(self, fn):
        """
        Call fn for each cell in the grid.
        """
        for i in xrange(self._n_cols):
            for j in xrange(self._n_rows):
                if self.on_board(i,j):
                    fn(self.grid[i][j])

    def keypress(self, key):
        """
        This should be called whenever a key is pressed.
        In any class that subclasses both GameBoard and Screen,
        this will happen automatically.

        In GameBoard itself, the behaviour is as follows.
        We look the key up in self.key_movements. If we don't
        find it (because it isn't in there, or because self.key_movements
        doesn't even exist), we call self.handle_keypress(key).
        Otherwise, we try to move the cursor by the (dx,dy) displacement
        associated with the key identifier in the dict; if that
        would take us off the board, we don't move.
        """
        try: (dx,dy) = self.key_movements[key]
        except:
            self.handle_keypress(key)
            return

        if self.cursor <> None:
            (x, y) = (self.cursor.grid_x+dx, self.cursor.grid_y+dy)
            if self.on_board(x,y):
                self.move_cursor(x,y)

    def on_board(self, i, j):
        """
        Return true if (i,j) is on the board, false otherwise.
        Override this to restrict which cells are created and
        are legal cursor positions.
        """
        return 0 <= i < self._n_cols and 0 <= j < self._n_rows

    def enable_cursor(self, i, j):
        """
        Make there be a cursor, at (i,j) in grid coordinates.
        If there is already a cursor, it is simply moved to (i,j).
        """
        if self.cursor is None:
            self.cursor = self.grid[i][j]
            self.cursor.raise_object()
            self.cursor.set_outline(self._cursor_colour)
            self.cursor.treat_as_dynamic()
            self.cursor_moved()
        else:
            self.move_cursor(i, j)

    def disable_cursor(self):
        """
        Make there be no cursor.
        """
        if self.cursor is not None:
            self.cursor.treat_as_static()
            self.cursor.raise_object()
            self.cursor.set_outline(self._line_colour)
            self.cursor_moved() # To reacquire visibility of contents
            self.cursor = None

    def move_cursor(self, i, j):
        """
        Make the cursor (which must already exist) be at (i,j)
        in grid coordinates.
        """
        self.cursor.treat_as_static()
        self.cursor.raise_object()
        self.cursor.set_outline(self._line_colour)
        self.cursor = self.grid[i][j]
        self.cursor.raise_object()
        self.cursor.set_outline(self._cursor_colour)
        self.cursor.treat_as_dynamic()
        self.cursor_moved()

    def cursor_moved(self):
        """
        Override this if you want to be notified if the cursor moves.
        """
        pass

    def handle_keypress(self, key):
        """
        Override this if you want to handle keys other than the
        cursor keys, which have already been filtered out.
        """
        pass

class SingleBoard(GameBoard, games.Screen):
    """
    An almost trivial subclass of GameBoard and Screen,
    suitable for use when there is just one board which is
    the main thing on the screen.
    """

    def __init__(self, margins, n_cols, n_rows, box_size,
                 line_colour = DEFAULT_LINE_COLOUR,
                 fill_colour = DEFAULT_FILL_COLOUR,
                 cursor_colour = DEFAULT_CURSOR_COLOUR):
        self.init_singleboard(margins, n_cols, n_rows, box_size,
                              line_colour, fill_colour, cursor_colour)

    def init_singleboard(self, margins, n_cols, n_rows, box_size,
                         line_colour = DEFAULT_LINE_COLOUR,
                         fill_colour = DEFAULT_FILL_COLOUR,
                         cursor_colour = DEFAULT_CURSOR_COLOUR):
        """
        Arguments:
        margins -- A tuple (x,y) giving the amount of space on each side:
                   x at left and right, y at top and bottom.
                   Or, a tuple (xL,yT,xR,yB) giving the amount on all four
                   sides separately: left, top, right, bottom.
                   Or, a single number that will be used for all margins.
        n_cols -- The number of columns in the grid.
        n_rows -- The number of rows in the grid.
        box_size -- The total width and height of each cell.
        line_colour -- The colour of the grid lines.
        fill_colour -- The colour of the interior of each cell.
        cursor_colour -- The colour in which the edges of a cell
                         should be highlighted when the "cursor"
                         is over it.

        Initially, there is no cursor.
        """
        try: left,top = margins[:2]
        except TypeError: left,top,margins = margins,margins,(margins,margins)
        if len(margins)==2: right,bottom = margins
        else:               right,bottom = margins[2:]
        self.init_screen(n_cols * box_size + left+right,
                         n_rows * box_size + top+bottom)
        self.init_gameboard(self, (left,top), n_cols, n_rows, box_size,
                            line_colour, fill_colour, cursor_colour)


class Container:
    def __init__(self, contents):
        self.init_container(contents)

    def init_container(self, contents):
        self._contents = contents
        self._bases = []
        for b in self.__class__.__bases__:
            if b.__name__ != 'Container':
                self._bases.append(b)
        for c in contents:
            self.__dict__[c] = None

    def raise_object(self):
        for b in self._bases:
            try:
                b.raise_object(self)
            except:
                pass
            else:
                break
        else:
            raise games.GamesError, "Unable to raise this object"
        for content in self._contents:
            object = self.__dict__[content]
            if object != None:
                object.raise_object()

    def destroy(self):
        for b in self._bases:
            try:
                b.destroy(self)
            except:
                pass
            else:
                break
        else:
            raise games.GamesError, "Unable to destroy this object"
        for content in self._contents:
            object = self.__dict__[content]
            if object != None:
                object.destroy()

    def move_to(self, x, y=None):
        (old_x, old_y) = self.pos()
        if y is None: (x, y) = x
        delta_x = x - old_x
        delta_y = y - old_y
        for b in self._bases:
            try:
                b.move_to(self, x, y)
            except:
                pass
            else:
                break
        else:
            raise games.GamesError, "Unable to move this object"
        for content in self._contents:
            object = self.__dict__[content]
            if object != None:
                object.move_by(delta_x, delta_y)
