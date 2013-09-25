### Games support module for LiveWires using pygame.
###
### $Revision: 1.2 $ -- $Date: 2005/07/06 21:08:14 $
###############################################################################
# Copyright Richard Crook, Gareth McCaughan, Rhodri James, Neil Turton
# and Paul Wright.  All rights reserved.
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
###############################################################################

###############################################################################
#
# General introduction:
#
# A typical game will use a single Screen object (which represents a
# window on the user's screen, in which all the action takes place)
# and a number of instances of subclasses of Object, for the things
# that actually appear on the Screen.
#
# Some objects will have things happen to them regularly;
# their classes should subclass Timer as well as Object,
# and define a tick method.
#
# Some will, more specifically, move at regular intervals;
# their classes should subclass Mover (which < Timer) and
# define a moved method.
#
# All our object classes have methods with names like "init_circle"
# that take the same arguments as the constructor, for convenient use
# by subclasses. Be warned that sometimes when you inherit from more
# than one object class it may matter what order these are called in.

import math
import pygame, pygame.transform, pygame.draw

_have_image = _have_mixer = _have_font = 1

try:    import pygame.image
except: _have_image = 0

try:    import pygame.mixer
except: _have_mixer = 0

try:    import pygame.font
except: _have_font = 0

from pygame.locals import * # Richard's going to love this...

pygame.init ()


###############################################################################
## Error classes ##############################################################
###############################################################################

class GamesError (Exception): pass

###############################################################################
## Screen class ###############################################################
###############################################################################
##
## The Screen object represents the playing area. Since we can have
## only one screen under pygame, it's just a handy container for stuff
##
###############################################################################

class Screen:

    initialised = 0
    got_statics = 0

    def __init__ (self, width=640, height=480):

        self.init_screen (width, height)

    def init_screen (self, width=640, height=480):
        """
        width -- width of graphics window
        height -- height of graphics window
        """

        # Bomb if you try this more than once: pygame can only have one
        # window
        if Screen.initialised:
            raise GamesError, "Cannot have more than on Screen object"

        Screen.initialised = 1

        # Create the pygame display
        self._display = pygame.display.set_mode ((width, height), HWSURFACE)
        self._width = width
        self._height = height
        self._background = self._display.convert ()

        # Initialise a list of objects in play
        self._objects = []
        # Initialise list dirty rectangles to be repainted
        self._dirtyrects = []

        # Time when we should draw the next frame
        self._next_tick = 0

    def is_pressed (self, key):
        """
        Return true if the indicated key is pressed, false if not.
        The key should be specified using a pygame key identifier
        (defined in pygame.constants, and hence here, with a name
        beginning "K_").
        """
        return pygame.key.get_pressed () [key]

    def set_background (self, background):
        """
        Set the background to the surface provided. Note that the
        surface should not have transparency set, or weird things
        will happen.
        """

        self._background = pygame.Surface((self._width, self._height))
        for x in range(0, self._width, background.get_width()):
            for y in range (0, self._height, background.get_height()):
                self._background.blit(background, (x, y))

        self._display.blit (self._background, (0,0))
        pygame.display.update ()

    def set_background_colour (self, back_col):
        """
        Set the background to a surface consisting of the colour
        provided.  Strange things will happen should the colour
        have transparency!
        """

        self._background = pygame.Surface((self._width, self._height))
        self._background.fill(back_col)
        self._display.blit(self._background, (0, 0))
        pygame.display.update()

    def tick (self):
        """
        If you override the tick method in a subclass of the Screen
        class, you can specify actions which are carried out every
        tick.
        """
        pass

    def keypress(self, key):
        """
        If you override the keypress method, you will be able to
        handle individual keypresses instead of dealing with the
        keys held down as in the standard library.
        """

        pass

    def mouse_down(self, pos, button):
        """
        This method will be called when a mouse button becomes
        pressed. You can override it if you want to make use of
        the information. By default, it does nothing.

        It will be passed two arguments. The first is the
        position of the mouse when the button is pressed,
        as a tuple (x,y). The second is the button number,
        starting at 0.
        """

        pass

    def mouse_up(self, pos, button):
        """
        This method will be called when a mouse button becomes
        un-pressed. You can override it if you want to make use of
        the information. By default, it does nothing.

        It will be passed two arguments. The first is the
        position of the mouse when the button is released,
        as a tuple (x,y). The second is the button number,
        starting at 0.
        """

        pass

    def mouse_position(self):
        """
        Return the current position of the mouse as (x,y).
        """

        return pygame.mouse.get_pos()

    def mouse_buttons(self):
        """
        Return the current pressed-ness of up to three mouse buttons
        as a tuple (left,middle,right).
        """

        return pygame.mouse.get_pressed()

    def handle_events (self):
        """
        If you override this method in a subclass of the Screen
        class, you can specify how to handle different kinds of
        events.  However you must handle the quit condition!
        """
        events = pygame.event.get ()
        for event in events:
            if event.type == QUIT:
                self.quit ()
            elif event.type == KEYDOWN:
                self.keypress (event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up (event.pos, event.button-1)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down (event.pos, event.button-1)

    def quit (self):
        """
        Calling this method will stop the main loop from running and
        make the graphics window disappear.
        """

        self._exit = 1

    def clear (self):
        """
        Destroy all objects on this Screen.
        """
        for object in self._objects[:]:
            object.destroy ()
        self._objects = []

    def _update_display (self):
        """
        Get the actual display in sync with reality.
        """
        pygame.display.update (self._dirtyrects)
        self._dirtyrects = []

    def mainloop (self, fps = 50):
        """
        Run the pygame main loop. This will animate the objects on the
        screen and call their tick methods every tick.

        fps -- target frame rate
        """

        self._exit = 0

        while not self._exit:
            self._wait_frame (fps)

            for object in self._objects:
                if not object._static:
                    object._erase ()
                    object._dirty = 1

            # Take a copy of the _objects list as it may get changed in place.
            for object in self._objects [:]:
                if object._tickable: object._tick ()

            self.tick ()

            if Screen.got_statics:
                for object in self._objects:
                    if not object._static:
                        for o in object.overlapping_objects ():
                            if o._static and not o._dirty:
                                o._erase ()
                                o._dirty = 1

            for object in self._objects:
                if object._dirty:
                    object._draw ()
                    object._dirty = 0

            self._update_display()

            self.handle_events()

        # Throw away any pending events.
        pygame.event.get()

    def _wait_frame (self, fps):
        "Wait for the correct fps time to expire"
        this_tick = pygame.time.get_ticks()
        if this_tick < self._next_tick:
            pygame.time.delay(int(self._next_tick+0.5) - this_tick)
        self._next_tick = this_tick + (1000./fps)

    def overlapping_objects (self, rectangle):
        """
        Returns a list of all the objects which overlap the rectangle
        given.
        """

        rect = pygame.Rect (rectangle)

        rect_list = []
        for obj in self._objects:
            rect_list.append (obj._rect)

        indices = rect.collidelistall (rect_list)

        over_objects = []
        for index in indices:
            over_objects.append (self._objects [index])

        return over_objects

    ## Object list (all represented objects)

    def all_objects (self):
        """
        Returns a list of all the Objects on the Screen.
        """
        return self._objects [:]

    def _raise(self, it, above=None):
        """
        Raise an object to the top of the stack, or above the specified
        object.
        """
        # This makes sure we're always in a consistent state.
        objects = self._objects[:]
        # Remove the object from the list.
        objects.remove(it)
        if above == None:
            # Put it on top (the end).
            objects.append(it)
        else:
            # Put the object after <above>.
            idx = 1+objects.index(above)
            objects[idx:idx]=[it]
        # Install the new list.
        self._objects = objects
        # Force a redraw
        if it._static:
            it._erase()
            it._dirty = 1

    def _lower(self, object, below=None):
        """
        Lower an object to the bottom of the stack, or below the specified
        object.
        """
        # This makes sure we're always in a consistent state.
        objects = self._objects[:]
        objects.remove(it)
        if below == None:
            # Put the object on the beginning (bottom) of the list.
            self._objects = [it]+objects
        else:
            # Put the object before (below) the aboject.
            idx = objects.index(below)
            objects[idx:idx]=[it]
            self._objects = objects

    def _raise_list(self, objects, above=None):
        """
        Raise all the objects in a list to the top of the stack,
        or above the specified object (which must not be in the list).
        """
        d = {}
        for object in objects: d[object] = 1

        # Objects that aren't in the list.
        new_objects = []
        for object in self._objects:
            if not d.has_key(object): new_objects.append(object)

        # Put the list in the right place.
        if above: idx = new_objects.index(above)+1
        else:     idx = len(new_objects)
        new_objects[idx:idx] = objects

        # And install.
        self._objects = new_objects

    def _lower_list(self, objects, below=None):
        """
        Lower all the objects in a list to the top of the stack,
        or below the specified object (which must not be in the list).
        """
        d = {}
        for object in objects: d[object] = 1

        # Objects that aren't in the list.
        new_objects = []
        for object in self._objects:
            if not d.has_key(object): new_objects.append(object)

        # Put the list in the right place.
        if below: idx = new_objects.index(below)
        else:     idx = 0
        new_objects[idx:idx] = objects

        # And install.
        self._objects = new_objects

    def add_object (self, object):
        self._objects.append (object)

    def remove_object (self, object):
        try:
            self._objects.remove (object)
        except ValueError:
            # Already done it: happens in some games, not an error.
            pass

    def blit_and_dirty (self, source_surf, dest_pos):
        """
        You probably won't need to use this method in your own programs,
        as |Object| and its sub-classes know how to draw themselves on
        the screen. You'd need to use method if you wanted to draw an
        image on the screen which wasn't an |Object|.

        This method blits (draws, taking account of transparency) the
        given source surface |source_surf| to the screen at the position
        given by |dest_pos|.

        It then remembers the place where the surface was drawn as
        ``dirty''.  This means that when the display is updated on the
        next tick, this part of it will be redrawn.
        """

        rect = self._display.blit (source_surf, dest_pos)
        self._dirtyrects.append (rect)


    def blit_background (self, rect):
        """
        This method draws the background over the given rectangle, and
        marks that rectangle as ``dirty'' (see the |blit_and_dirty|
        method for what that means). It's used to erase an object before
        moving it. You shouldn't need to call it yourself.
        """

        rect = self._display.blit (self._background, rect, rect)
        self._dirtyrects.append (rect)

###########################################################################


###############################################################################
## Object class ###############################################################
###############################################################################
##                                                                           ##
## Object represents a graphical object on the screen. Objects can be moved, ##
## rotated, deleted, and maybe have other things done to them.               ##
## Every object has a "reference point". When you move the object to a       ##
## given point, it is moved so that its reference point ends up there.       ##
##                                                                           ##
###############################################################################

class Object:

    def __init__ (self, screen, x, y, surface, a=0, x_offset=0, y_offset=0,
                  static=0):
        """
        Initialise the object:

        screen -- screen object to put the object on.
        x -- x pos of object's reference point.
        y -- y pos of object's reference point.
        surface -- pygame.Surface object.
        a -- initial angle of rotation, in degrees.
        x_offset -- dx from reference point to BB top left at a=0.
        y_offset -- dy from reference point to BB top left at a=0.
        static -- flag, true if object usually doesn't need redrawing

        If you're using rather than writing the livewires.games
        module, then you almost certainly want to use one of the
        subclasses of Object rather than using Object itself.
        """

        self.screen = screen
        self._static = static
        if static:
            Screen.got_statics = 1
        self.screen.add_object (self)
        self._surface = surface
        self._orig_surface = surface # The surface before rotation
        self._orig_rect = surface.get_rect()

        # Offset from reference point to top left corner.
        self._x_offset_ = self._x_offset = x_offset
        self._y_offset_ = self._y_offset = y_offset

        self._rect = self._surface.get_rect ()
        self._x = 0
        self._y = 0
        self.move_to (x,y)

        self._a = a
        if self._a != 0:
            self._rotate ()

        self._tickable = 0

        self._gone = 0

        self._dirty = 1

    # When an object is GCed, it should disappear.
    def __del__(self):
        if not self._gone: self.destroy()

    def destroy(self):
        """
        Erase object from screen and remove it from the list of objects
        maintained by games module.
        """
        self._erase ()
        if Screen.got_statics:
            for o in self.overlapping_objects ():
                if o._static and not o._dirty:
                    o._erase ()
                    o._dirty = 1
        self.screen.remove_object (self)
        self._gone = 1

    def _erase (self):
        """
        Erase object from screen by blitting the background over where
        it was.
        """
        self.screen.blit_background (self._rect)

    def _draw (self):
        """
        Draw object on screen by blitting the image onto the screen.
        """
        self.screen.blit_and_dirty (self._surface, self._rect)

    def replace_image(self, surface):
        """
        Remove the current surface defining the object and replace
        it with a new one.
        """
        self._orig_surface = surface
        self._orig_rect    = surface.get_rect()

        if self._a != 0:
            self._rotate ()
        else:
            self._replace (surface)

    def _replace (self, surface):
        (x, y) = self.pos ()
        self._surface = surface
        self._rect = self._surface.get_rect()
        self.move_to (x, y)

    def pos(self):      return (self._x, self._y)
    def xpos(self):     return self._x
    def ypos(self):     return self._y
    def bbox(self):     return tuple(self._rect)
    def angle(self):    return self._a % 360

    def move_to(self, x, y=None):
        """
        Move the object so that its reference point is at the given position.
        """
        # Split a supplied coordinate pair, if required
        if y is None: x, y = x # assumed a 2-tuple
        if self._static:
            self._erase()
            self._dirty = 1
        self._x = x
        self._y = y
        self._rect.left = int (x + self._x_offset)
        self._rect.top  = int (y + self._y_offset)

    def move_by(self, x, y=None):
        if y is None: x, y = x
        x = self._x + x
        y = self._y + y
        self.move_to (x, y)

    def rotate_to(self, angle):
        self._a = angle % 360
        self._rotate()

    def rotate_by(self, angle):
        self.rotate_to(self._a+angle)

    def _rotate(self):
        self._replace (pygame.transform.rotate (self._orig_surface,
            -self._a))
        self._rect = self._surface.get_rect()
        self._fix_offsets()
        self.move_to(self._x, self._y)

    def _set_offsets(self, x,y):
        self._x_offset_ = x
        self._y_offset_ = y
        self._fix_offsets()

    def _fix_offsets(self):
        if self._a == 0:
            self._x_offset = self._x_offset_
            self._y_offset = self._y_offset_
        else:
            a = -math.pi/180 * self._a
            c,s = math.cos(a), math.sin(a)
            # Reference point to centre of original rectangle:
            dx = self._x_offset_ + (self._orig_rect.centerx-self._orig_rect.left)
            dy = self._y_offset_ + (self._orig_rect.centery-self._orig_rect.top)
            # Reference point to centre of new rectangle:
            dx,dy = c*dx + s*dy, -s*dx+c*dy
            # Reference point to top left of new rectangle:
            self._x_offset = dx - (self._rect.centerx-self._rect.left)
            self._y_offset = dy - (self._rect.centery-self._rect.top)

    ## Intersection testing

    def overlapping_objects(self):
        # Find approximate overlap list
        objects = self.screen.overlapping_objects (self._rect)
        if self in objects:
            objects.remove (self)

        # Use specialised checkers to get a better answer. This may be slow.
        result = filter(self.filter_overlaps, objects)
        return filter(lambda o,self=self: o.filter_overlaps(self), result)

    def filter_overlaps(self, object):
        """
        This is a utility method which allows you to have
        better control over whether two objects have collided
        than just checking whether the rectangles which enclose
        them are touching. It is called after having
        established that the rectangles touch so you can assume
        that in your checking.

        Some subclasses of object override it (eg the |Circle|
        class). You can also override it in your own subclasses
        of |Object| to get better collision detection.

        This function should return 1 if the your object really
        overlaps the other object and 0 otherwise. The standard
        |Object| class just returns 1.
        """
        return 1

    def overlaps(self, object):
        return (self._rect.colliderect (object._rect) and
            self.filter_overlaps (object) and object.filter_overlaps
            (self))

    def raise_object(self, above=None):
        """
        Raise an object to the top of the stack, or above the specified
        object.
        """
        self.screen._raise(self, above)

    def lower_object(self, below=None):
        """
        Lower an object to the bottom of the stack, or below the specified
        object.
        """
        self.screen._lower(self, below)

    def treat_as_dynamic(self):
        """
        Make the object not static.  This is intended for temporary use for
        static objects that otherwise won't get redrawn correctly, such as
        the cursor on a board.
        """
        self._static = 0

    def treat_as_static(self):
        """
        Make the object static.  This is intended for undoing a previous
        call to treat_as_dynamic(), not as a way of making objects static
        as an afterthought.  In particular, it won't help if no static
        objects have been made up to this point.
        """
        self._static = 1

#------------------------------------------------------------------------------

class Sprite (Object):
    """
    The class which lets you create sprites (that is, bitmaps).
    If you want a sprite that moves automatically, subclass from
    this and from Mover. If you want one that changes its image
    automatically, subclass from Animation instead of from Sprite.

    The reference point of a Sprite is the centre of its bounding box.
    """

    def __init__ (self,screen, x, y, image, a=0, static=0):
        self.init_sprite (screen, x, y, image, a, static)

    def init_sprite (self, screen, x, y, image, a=0, static=0):
        """
        Arguments:

        screen -- the screen on which the sprite should appear.
        x -- the x-coordinate of the centre of the image.
        y -- the y-coordinate of the centre of the image.
        image -- the image object, as returned from the load_image function.
        a -- the angle through which the image should be rotated.
        """
        Object.__init__ (self, screen, x, y, image, a, static=static,
                         x_offset=-image.get_width()/2, y_offset=-image.get_height()/2)

#------------------------------------------------------------------------------

class ColourMixin:
    """
    This is a mixin class which handles colour changes for geometric
    objects by redrawing them on a new surface using their
    _create_surface method.
    """

    def set_colour(self, colour):
        if colour != self._colour:
            self._colour = colour
            if self._static:
                self._erase()
                self._dirty = 1
            surface = self._create_surface ()
            self.replace_image(surface)

    def get_colour(self):
        return self._colour

#------------------------------------------------------------------------------

class OutlineMixin:
    """
    This is a mixin class which handles colour changes for the outlines
    of geometric objects by redrawing them on a new surface using their
    _create_surface method.
    """

    def set_outline(self, colour):
        if colour != self._outline:
            self._outline = colour
            if self._static:
                self._erase()
                self._dirty = 1
            surface = self._create_surface ()
            self.replace_image(surface)

    def get_outline(self):
        return self._outline

#------------------------------------------------------------------------------
class Text(Object, ColourMixin):
    """
    A class for representing text on the screen.

    The reference point of a Text object is the centre of its
    bounding box.
    """

    def __init__(self, screen, x, y, text, size, colour, static=0):

        self.init_text (screen, x, y, text, size, colour, static)

    def init_text (self, screen, x, y, text, size, colour, static=0):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of centre of bounding box.
        y -- y-coordinate of centre of bounding box.
        text -- the text to display.
        size -- nominal height of the text, in pixels.
        colour -- the colour the text should be.
        """
        if not _have_font:
            raise GameError, "We don't have pygame.font, so can't create text objects"
        self._size = size
        self._colour = colour
        self._text = text
        self._font = pygame.font.Font(None, self._size)
        self._a = 0
        surface = self._create_surface()
        Object.__init__(self, screen, x, y, surface, x_offset=self._x_offset,
                        y_offset=self._y_offset, static=static)
        self.move_to(x,y)

    def _create_surface (self):
        result = self._font.render(self._text, 1, self._colour)
        r = result.get_rect()
        self._set_offsets(-0.5*(r.right-r.left), -0.5*(r.bottom-r.top))
        return result

    def set_text(self, text):
        if text != self._text:
            self._erase()
            self._text = text
            surface = self._create_surface ()
            self.replace_image(surface)

    def get_text(self):
        return self._text

#------------------------------------------------------------------------------

class Polygon (Object, ColourMixin, OutlineMixin):
    """
    A polygon, either drawn in outline or filled in. Its shape
    is specified as a list of points relative to the polygon's
    reference point.
    """
    def __init__ (self, screen, x, y, shape, colour, filled = 1,
                  outline = None, static=0, thickness=1):
        self.init_polygon (screen, x, y, shape, colour, filled, outline, static, thickness)

    def init_polygon (self, screen, x, y, shape, colour, filled = 1,
                      outline = None, static = 0, thickness = 1):
        """
        Arguments:

        screen -- the screen the object is on.
        x -- x-coordinate of reference point.
        y -- y-coordinate of reference point.
        shape -- a list of vertices, each given as (dx,dy) from reference point.
        colour -- colour to draw either the boundary or the whole polygon.
        filled -- true iff the polygon is to be filled in.
        outline -- colour to draw the outline in (if different from whole polygon)
        static -- whether or not the polygon is ever expected to move
        """
        self._colour = colour
        self.screen = screen # Must do this here so surface convert works
        self._filled = filled
        self._shape = tuple(shape)
        self._outline = outline
        self._a = 0
        self._thickness = thickness

        surface = self._create_surface ()
        Object.__init__ (self, screen, x, y, surface, a = 0,
                         x_offset=self._x_offset_, y_offset=self._y_offset,
                         static=static)

    def __repr__(self):
        return "<Polygon at (%s,%s), %s, %s, colour %s, outline %s: %s>" \
               % (self.xpos(), self.ypos(), ["filled","unfilled"][not self._filled],
                  ["dynamic","static"][self._static], self._colour, self._outline, self._shape)

    def set_shape (self, shape):
        self._shape = tuple(shape)
        (old_x, old_y) = self.pos ()
        new_surf = self._create_surface ()
        # the new surface may set new offsets, so ensure we
        # are just where we were:
        self.move_to (old_x, old_y)
        self.replace_image (new_surf)

    def get_shape (self):
        return self._shape

    def _create_surface (self):

        shape = self._shape

        minx = maxx = shape[0][0]
        miny = maxy = shape[0][1]

        for (x,y) in shape:
            if x < minx: minx = x
            if x > maxx: maxx = x

            if y < miny: miny = y
            if y > maxy: maxy = y

        surface = pygame.Surface ((maxx-minx + 1, maxy-miny + 1)).convert ()

        # The part of the surface not occupied by the polygon should be
        # transparent. We choose a colour for it that isn't the same as the
        # one in which the polygon is to be drawn.
        key_colour = (0,0,0)
        if self._colour == key_colour or self._outline == key_colour:
            key_colour = (0,0,10)
            if self._colour == key_colour or self._outline == key_colour:
                key_colour = (0, 10, 10)
        surface.fill (key_colour)
        surface.set_colorkey (key_colour, RLEACCEL)

        nshape = []
        for (x,y) in shape:
            nshape.append ((x - minx, y - miny))
        nshape = tuple (nshape)

        # Offset from zero of user supplied co-ordinates to top left
        # of bounding box. These offsets are added to user-supplied coords
        # for move_to to give the new position of the top left of the surface.
        self._set_offsets(minx, miny)

        if self._filled:
            pygame.draw.polygon (surface, self._colour, nshape, 0)
            if self._outline != None:
                pygame.draw.polygon (surface, self._outline, nshape, self._thickness)
        elif self._outline != None:
            pygame.draw.polygon (surface, self._outline, nshape, self._thickness)
        else:
            pygame.draw.polygon (surface, self._colour, nshape, self._thickness)

        return surface

#------------------------------------------------------------------------------

class Circle (Object, ColourMixin, OutlineMixin):
    """
    A circle, filled or otherwise, on the screen.
    The reference point is the centre of the circle.
    """

    def __init__ (self, screen, x, y, radius, colour, filled = 1, outline = None, static = 0):
        self.init_circle (screen, x, y, radius, colour, filled, outline, static)

    def init_circle (self, screen, x, y, radius, colour, filled=1, outline=None, static=0):

        self._colour = colour
        self._outline = outline
        self.screen = screen # Must do this here so surface convert in _create_surface works
        self._filled = filled
        self._radius = radius

        self._a = 0

        Object.__init__ (self, screen, x, y, self._create_surface (),
                         a=0, x_offset=-radius, y_offset=-radius,
                         static=static)

    def _create_surface (self):

        surface = pygame.Surface ((2 * self._radius + 1, 2 * self._radius +1)).convert ()

        key_colour = (0,0,0)
        if self._colour == key_colour or self._outline == key_colour:
            key_colour = (0,0,10)
            if self._colour == key_colour or self._outline == key_colour:
                key_colour = (0,10,10)

        surface.fill (key_colour)
        surface.set_colorkey (key_colour, RLEACCEL)

        self._set_offsets(-self._radius, -self._radius)

        if self._filled:
            pygame.draw.ellipse (surface, self._colour, surface.get_rect (), 0)
            if self._outline != None:
                pygame.draw.ellipse (surface, self._outline, surface.get_rect (), 1)
        elif self._outline != None:
            pygame.draw.ellipse (surface, self._outline, surface.get_rect (), 1)
        else:
            pygame.draw.ellipse (surface, self._colour, surface.get_rect (), 1)

        return surface

    def get_radius (self):
        return self._radius

    def set_radius (self, radius):
        if self._radius != radius:
            self._radius = radius
            surface = self._create_surface ()
            self.replace_image (surface)

    def _rotate (self):
        pass

    def filter_overlaps(self, object):
        r = object._rect
        x0,y0, x1,y1 = r.left,r.top, r.right,r.bottom
        r = self._radius
        r2 = r*r
        x,y = self._x,self._y
        if x<x0-r or x>x1+r or y<y0-r or y>y1+r: return 0
        if x0<x<x1 or y0<y<y1: return 1
        if x<x0:
            if y<y0: return (x-x0)**2 + (y-y0)**2 <= r2
            else:    return (x-x0)**2 + (y-y1)**2 <= r2
        else:
            if y<y0: return (x-x1)**2 + (y-y0)**2 <= r2
            else:    return (x-x1)**2 + (y-y1)**2 <= r2

#------------------------------------------------------------------------------

class Timer:
    """
    This is a class which you can add to an Object to make a new class.
    In your new class, you must supply a |tick| method. This method will
    be called every |interval| ticks, where |interval| is the argument you
    give to |init_timer|.
    """

    def __init__ (self, interval = 1, running = 1):
        self.init_timer (interval)

    def init_timer (self, interval = 1, running = 1):
        """
        Call this function to start the timer. You must call it after
        the Object's init function.
        """
        self._interval = interval
        self._tickable = running
        self._next = 0

    def _tick (self):
        self._next = self._next + 1
        if self._next >= self._interval:
            self._next = 0
            self.tick ()

    def get_interval (self):
        return self._interval

    def set_interval (self, interval):
        self._interval = interval

    def stop (self):
        self._tickable = 0

    def start (self):
        self._tickable = 1
        self._next = 0

#------------------------------------------------------------------------------

class Mover (Timer):
    """
    This is a class which you can add to any Object or sub-class of
    Object to make a new class for something which moves itself around
    the screen. On each tick, your Object will be moved by the amount
    you specify.

    The moved method of your class will be called after each tick, even
    if the velocity of the object happens to be (0,0).
    """

    def init_mover (self, dx, dy, da=0):
        """
        Call this to set up the Mover's speed after you've created it.
        Its Object init method (init_circle or whatever) must already
        have been called.
        """
        self.set_velocity (dx, dy)
        self.set_angular_speed (da)
        self.init_timer (1)

    def set_velocity (self, dx, dy=None):
        if dy is None: dx, dy = dx
        self._dx = dx
        self._dy = dy

    def set_angular_speed (self, da):
        self._da = da

    def get_angular_speed (self):
        return self._da

    def get_velocity (self):
        return (self._dx, self._dy)

    def _tick (self):
        self.move_by (self._dx, self._dy)
        if self._da:
            self.rotate_by (self._da)
        self.moved ()

#------------------------------------------------------------------------------

class Message (Text, Timer):
    """
    A Text object that disappears from the screen after a while.
    More precisely, after a specified number of frames it will
    call the specified |after_death| function (if any) and then
    destroy itself.

    The reference point, as for a Text object, is the centre
    of the bounding box.
    """

    def __init__ (self, screen, x, y, text, size, colour, lifetime, after_death=None):
        self.init_message (screen, x, y, text, size, colour, lifetime,
        after_death)

    def init_message (self, screen, x, y, text, size, colour, lifetime, after_death=None):
        """
        Arguments:

        x -- x-coordinate of centre of bounding box.
        y -- y-coordinate of centre of bounding box.
        text -- the text to display.
        size -- the size of the text, in pixels nominal height.
        colour -- the colour of the text.
        lifetime -- the number of frames to wait before disappearing.
        after_death -- the function to call immediately before disappearing.
        """

        self._after_death = after_death
        self.init_text (screen, x, y, text, size, colour)
        self.init_timer (lifetime)

    def tick (self):
        if self._after_death:
            self._after_death ()
        self.stop ()
        self.destroy ()

#------------------------------------------------------------------------------

class Animation (Sprite, Timer):
    """
    An image that changes every N ticks.
    The init function expects (among other things) two lists of images.
    If the first list is [a,b,c,d] and the second is [x,y,z] then the
    sequence of images shown will be a,b,c,d, x,y,z, x,y,z, x,y,z, ... .
    The n_repeats parameter is the maximum number of images to show,
    or something <= 0 to keep showing for ever.
    You can give lists of filenames instead of lists of images,
    if you like.

    The reference point, as for a Sprite, is the centre of the
    bounding box.
    """

    def __init__(self, screen, x, y,
                 nonrepeating_images, repeating_images, n_repeats=0,
                 repeat_interval=1, a=0):
        self.init_animation(screen, x, y,
                            nonrepeating_images, repeating_images, n_repeats,
                            repeat_interval, a)

    def init_animation(self, screen, x, y,
                       nonrepeating_images, repeating_images, n_repeats,
                       repeat_interval, a):
        """
        Arguments:

        screen -- the screen to put the image on.
        x -- the x-coordinate of the centre of the image.
        y -- the y-coordinate of the centre of the image.
        nonrepeating_images -- list of images to show just once each.
        repeating_images -- list of images to show cyclicly
          once nonrepeating_images have finished.
        n_repeats -- maximum number of images to show in total,
          or something <=0 to continue for ever.
        repeat_interval -- number of frames between image changes.
        a -- angle to rotate through, in degrees.
        """
        if nonrepeating_images and type(nonrepeating_images[0]) is type(""):
            nonrepeating_images, repeating_images = \
                load_animation(nonrepeating_images, repeating_images)
        self.nonrepeating_images = nonrepeating_images
        self.repeating_images    = repeating_images
        self.n_repeats = n_repeats or -1
        first_image = self.next_image()
        if first_image is None:
            raise GamesError, "An animation with no images is illegal."
        Object.__init__(self, screen, x, y, self.next_image())
        self.init_timer(repeat_interval)

    def next_image(self):
        if self.n_repeats==0: return None
        if self.n_repeats>0: self.n_repeats -= 1
        if self.nonrepeating_images:
            return self.nonrepeating_images.pop(0)
        if not self.repeating_images: return None
        self.repeating_images = [self.repeating_images[-1]] \
                                + self.repeating_images[:-1]
        return self.repeating_images[0]

    def tick(self):
        new_image = self.next_image()
        if new_image is None: self.destroy()
        else: self.replace_image(new_image)

#------------------------------------------------------------------------------

###############################################################################
## Utility functions
###############################################################################
def load_image(file, transparent=1):
    """Loads an image, prepares it for play. Returns a pygame.Surface object
    which you can give as the "image" parameter to Object.

    file -- the filename of the image to load
    transparent -- whether the background of the image should be transparent.
                   Defaults to true.
                   The background colour is taken as the colour of the pixel
                   at (0,0) in the image.
    """
    if not _have_image:
        raise GamesError, "We don't have pygame.image, so can't load \"%s\"" % file
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise GamesError, 'Could not load image "%s" %s'%(file, pygame.get_error())
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()

def load_sound(file):
    """
    Load a sound file, returning a Sound object.
    """
    if not _have_mixer:
        raise GameError, "We don't have pygame.mixer, so can't load \"%s\"" % file
    try: return pygame.mixer.Sound(file)
    except pygame.error: return None

def load_animation(nonrepeating_files, repeating_files=[], transparent=1):
    """
    Loads a number of files. Returns the "nonrepeating images" and
    "repeating images" arguments needed for the Animation constructor.
    """
    def _(name, transparent=transparent):
        if not _have_image:
            raise GamesError, "We don't have pygame.image, so can't load animation \"%s\"" % name
        try: surface = pygame.image.load(name)
        except pygame.error:
            raise GamesError, 'Could not load animation frame "%s": %s' % (
                name, pygame.get_error())
        if transparent:
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        return surface.convert()
    nonrepeating = map(_, nonrepeating_files)
    repeating    = map(_, repeating_files)
    return nonrepeating, repeating

def scale_image(image, x_scale, y_scale=None):
    """
    Return a version of the image that's been scaled by a factor
    x_scale in the x direction and y_scale in the y direction.
    If y_scale is not given, scale uniformly.
    """
    if y_scale is None: y_scale = x_scale
    (x_size, y_size) = image.get_size()
    x_size = x_size * x_scale
    y_size = y_size * y_scale
    return pygame.transform.scale (image, (x_size, y_size))

###############################################################################
## Test code
###############################################################################
if __name__ == "__main__":

    import colour

    s = Screen (700, 500)
    try: stars = load_image ("starfield.bmp")
    except GamesError: stars = None
    try: chess = load_sound ("ngame.wav")
    except GamesError: chess = None
    if stars: s.set_background (stars)

    class StaticImage (Sprite):

        def __init__ (self):
            Sprite.__init__ (self, s, 200, 100, load_image ("alien.gif"))

    try: si = StaticImage ()
    except GamesError: si = None

    class SillyMessage (Text, Timer):
        def __init__ (self):
            Text.__init__ (self, s, 200, 200, "Hello", 100, colour.green)
            Timer.__init__ (self, 50)
            self.counter = 0

        def tick (self):
            if self.counter == 0:
                self.counter = 1
                self.set_text ("bye")
            else:
                if chess: chess.play ()
                self.destroy ()

    mess = SillyMessage ()

    class Square (Polygon, Mover):
        def __init__ (self):
            shape = ((0,0), (100,0), (100, 100), (0, 100))
            self.init_polygon (s, 200, 100, shape, colour.red, 1)
            self.init_mover (1, 0, 4)

        def moved (self):
            (x, y) = self.pos ()
            if x > s._width:
                s.quit ()


    sq = Square ()

    class MovingCircle (Circle, Mover):
        def __init__ (self):
            self.init_circle (s, 500, 100, 50, colour.purple, 0)
            self.init_mover (-1, 1, 0)

        def moved (self):
            for o in self.overlapping_objects ():
                if isinstance (o, Square):
                    self.destroy ()

    mc = MovingCircle ()

    class ExpandingBar (Polygon, Timer):
        def __init__ (self):
            self.length = 100
            shape = ((0,0), (self.length,0), (self.length, 10), (0, 10))
            self.init_polygon (s, 200, 400, shape, colour.red, 1)
            self.init_timer ()

        def tick (self):
            self.length = self.length + 2
            shape = ((0,0), (self.length,0), (self.length, 10), (0, 10))
            self.set_shape (shape)

    eb = ExpandingBar ()

    mess = Message (s, 500, 300, "WIBBLE", 50, colour.purple, 100)

    dummy = Polygon(s, 500,300, ((0,0),(50,0),(50,50),(0,50)), colour.white)

    s.mainloop ()


# vim:expandtab:sts=4:sw=4:showmatch:
