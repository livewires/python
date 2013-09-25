###############################################################################
#
# LiveWires beginners' support library
#
# This library provides a simple graphics API to allow procedural
# programming using (in this instance) Tk to provide an output
# window. It is intended, however, to be graphics-subsystem
# independent.
#
###############################################################################
#
# $Revision: 1.6 $ -- $Date: 2002/08/17 14:24:45 $
#
###############################################################################
# Copyright Richard Crook and Gareth McCaughan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
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
### External dependencies #####################################################
###############################################################################

import sys
import math
import random
import string
import time
import types
import Tkinter

###############################################################################
### Module statics ############################################################
###############################################################################

_Windows     = sys.platform == 'win32'  # True if on Win95/98/NT

_root_window    = None                  # The root window for graphics output
_canvas         = None                  # The canvas which holds graphics
_canvas_xs      = None                  # Size of canvas object
_canvas_ys      = None
_canvas_x       = None                  # Current position on canvas
_canvas_y       = None
_canvas_col     = None                  # Current colour (set to black below)
_canvas_tsize   = 12
_canvas_tserifs = 0

if _Windows:
    _canvas_tfonts = ['times new roman', 'lucida console']
else:
    _canvas_tfonts = ['times','lucidasans-24']
    pass # XXX need defaults here

_mouse_enabled  = 0                     # mouse_begin called
_mouse_x        = None                  # Initial position assumed outside
_mouse_y        = None                  # the window

_returning      = 0                     # Return objects when created?

###############################################################################
### Exception classes #########################################################
###############################################################################

class LWException(Exception):           pass
class ExAlreadyStarted(LWException):    pass
class ExBadParameters(LWException):     pass
class ExUnimplemented(LWException):     pass

###############################################################################
### Class for canvas object encapsulation #####################################
###############################################################################

class Movable:

    def __init__(self, id, coord_list):
        self.id = id
        self.coord_list = coord_list

    def coords(self):
        return self.coord_list

class MovableCircle(Movable):

    def coords(self):
        cl = self.coord_list
        return [(cl[0]+cl[2])/2, (cl[1]+cl[3])/2]

###############################################################################
### Colour handling ###########################################################
###############################################################################

class Colour:

    # Basic methods

    def __init__(self, red=0.0, green=0.0, blue=0.0):
        # XXX We might want to accept Colour(c), where c is a colour
        # XXX Still not sure about domains of [0.0, 1.0], rather than [0,255]
        # XXX Consider also what rounding (if any) is appropriate here
        constrain  = self.__constrain
        self.r = constrain(255*red)
        self.g = constrain(255*green)
        self.b = constrain(255*blue)

    def __repr__(self):
        return ('Colour(%.3f, %.3f, %.3f)' %
                (self.r/255., self.g/255., self.b/255.))

    def _toTk(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    # Colour arithmetic methods

    def __constrain(self, component):
        return max(0, min(255, int(component + 0.5)))

    def __mul__(self, other):           # colour * n
        # XXX It might be preferable to use [0.0,1.0] representation
        #     internally, to preserve precision here, but we probably
        #     don't care very much about it
        constrain = self.__constrain
        red   = constrain(self.r * other)
        green = constrain(self.g * other)
        blue  = constrain(self.b * other)
        return Colour(red/255., green/255., blue/255.)

    def __rmul__(self, other):          # n * colour
        return self.__mul__(other)

    def __add__(self, other):           # colour + colour
        constrain = self.__constrain
        red   = constrain(self.r + other.r)
        green = constrain(self.g + other.g)
        blue  = constrain(self.b + other.b)
        return Colour(red/255., green/255., blue/255.)

    # Accessors

    def red(self):   return self.r
    def green(self): return self.g
    def blue(self):  return self.b

Colour.red      = Colour(1, 0, 0)
Colour.green    = Colour(0, 1, 0)
Colour.blue     = Colour(0, 0, 1)
Colour.black    = Colour(0, 0, 0)
Colour.white    = Colour(1, 1, 1)

Colour.dark_red   = Colour(0.5, 0.0, 0.0)
Colour.dark_green = Colour(0.0, 0.4, 0.0)
Colour.dark_blue  = Colour(0.0, 0.0, 0.5)

Colour.dark_grey  = Colour(0.3, 0.3, 0.3)
Colour.grey       = Colour(0.5, 0.5, 0.5)
Colour.light_grey = Colour(0.7, 0.7, 0.7)

Colour.yellow     = Colour(0.9, 0.8, 0.0)

Colour.brown      = Colour(0.5, 0.35, 0.0)
Colour.pink       = Colour(1.0, 0.0,  0.8)
Colour.purple     = Colour(0.6, 0.0,  0.7)

_canvas_col     = Colour.black

### make_colour() #############################################################
#
# XXX We might just delete this, and use Colour() directly

make_colour = Colour

### set_colour() ##############################################################

def set_colour(c):
    global _canvas_col
    if not isinstance (c, Colour):
        raise ExBadParameters, "colour must be from Colour class"
    c, _canvas_col = _canvas_col, c
    return c

###############################################################################
### Time support ##############################################################
###############################################################################

def sleep(secs):
    if _root_window == None:
        time.sleep(secs)
    else:
        _root_window.update_idletasks()
        _root_window.after(int(1000*secs), _root_window.quit)
        _root_window.mainloop()

###############################################################################
### Initialisation ############################################################
###############################################################################

### begin_graphics() ##########################################################
#
# Create the window in which graphics will be output.

def begin_graphics(width=640, height=480, background=Colour.white, title=None):

    global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys

    # Check for duplicate call
    if _root_window is not None:
        # Lose the window.
        _root_window.destroy()
        # raise ExAlreadyStarted('begin_graphics() called twice')

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = width-1, height-1
    _canvas_x,  _canvas_y  = 0, _canvas_ys

    # Create the root window
    _root_window = Tkinter.Tk()
    _root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
    if _Windows:
        _root_window.bind('<Alt-F4>',         _destroy_window)
    _root_window.title(title or 'Graphics Window')
    _root_window.resizable(0, 0)
    # XXX Should we force the input focus into the window?

    # Create the canvas object
    try:
        _canvas = Tkinter.Canvas(_root_window,
                                width=width, height=height,
                                bg=background._toTk())
        _canvas.pack()
        _canvas.update()
    except:
        _root_window.destroy()
        _root_window = None
        raise

    # Bind to key-down and key-up events
    _root_window.bind("<KeyPress>", _keypress)
    _root_window.bind("<KeyRelease>", _keyrelease)
    _root_window.bind("<FocusIn>", _clear_keys)
    _root_window.bind("<FocusOut>", _clear_keys)
    _clear_keys()

def _destroy_window(event=None):
    global _root_window
    _root_window.destroy()
    _root_window = None

### end_graphics() ############################################################
#
# Program terminated. Wait for graphics window to be closed.

def end_graphics():
    global _root_window, _canvas, _mouse_enabled
    try:
        sleep(1)
        _root_window.destroy()
        #try:
        #    _root_window.mainloop()
        #except KeyboardInterrupt:
        #    _root_window.destroy()
    finally:
        _root_window   = None
        _canvas        = None
        _mouse_enabled = 0
        _clear_keys()

###############################################################################
### Basic line drawing ########################################################
###############################################################################

### clear_screen() ############################################################

def clear_screen(background=None):

    global _canvas_x, _canvas_y

    # Remove all drawn items
    _canvas.delete('all')

    # Change background colour if required
    if background is not None:
        _canvas.configure(bg=background._toTk())

    # Reset default coordinates
    # XXX Should any other state be reset?
    _canvas_x, _canvas_y = 0, _canvas_ys

### move() ####################################################################

def move(x, y=None):

    global _canvas_x, _canvas_y

    # Unpack a tuple argument
    if y is None:
        try:        x, y = x
        except:     raise ExBadParameters('not a coordinate')

    _canvas_x, _canvas_y = x, _canvas_ys-y
    _canvas.update()


### plot() ####################################################################

def plot(x, y=None, colour=None):

    global _canvas_x, _canvas_y

    # Unpack a tuple argument
    if y is None:
        try:        x, y = x
        except:     raise ExBadParameters('not a coordinate')

    # Provide a dynamic default colour
    if colour is None: colour = _canvas_col

    # Draw a very short line
    y = _canvas_ys - y
    _canvas.create_line(x, y, x+1, y, fill=colour._toTk())

    _canvas_x, _canvas_y = x, y
    _canvas.update()

### draw() ####################################################################

def draw(x, y=None, colour=None):

    global _canvas_x, _canvas_y

    # Unpack a tuple argument
    if y is None:
        try:        x, y = x
        except:     raise ExBadParameters('not a coordinate')

    # Provide a dynamic default colour
    if colour is None: colour = _canvas_col

    # Draw a line
    y = _canvas_ys - y
    _canvas.create_line(_canvas_x, _canvas_y, x, y, fill=colour._toTk())

    _canvas_x, _canvas_y = x, y
    _canvas.update()

### position() ################################################################

def position(): return (_canvas_x, _canvas_y)

###############################################################################
### Object drawing ############################################################
###############################################################################

### line() ####################################################################

def line(x0, y0, x1=None, y1=None, colour=None):

    global _canvas_x, _canvas_y

    # Unpack arguments. The specification that we should accept any of
    #   line((x0,y0), (x1,y1))
    #   line((x0,y0), x1, y1)
    #   line(x0, y0, (x1,y1))
    #   line(x0, y0, x1, y1)
    # complicates life somewhat...

    tt = types.TupleType

    try: # catches unpacking errors
        if type(x0) is tt:
            if y1 is not None:          # Check for too many parameters
                raise ExBadParameters('too many coordinates')
            x1, y1 = y0, x1             # Shift parameters right
            x0, y0 = x0                 # and unpack first coordinate pair
        if type(x1) is tt:
            if y1 is not None:
                raise ExBadParameters('too many coordinates')
            x1, y1 = x1                 # Unpack second coordinate pair

    except ExBadParameters:     raise
    except:                     raise ExBadParameters('not a coordinate')

    y0 = _canvas_ys - y0
    y1 = _canvas_ys - y1

    if colour is None: colour = _canvas_col

    _canvas_x, _canvas_y = x1, y1

    if _returning:
      lobj = Movable(_canvas.create_line(x0, y0, x1, y1, fill=colour._toTk()),
                     [x0,y0,x1,y1])
      _canvas.update()
      return lobj
    else:
      _canvas.create_line(x0, y0, x1, y1, fill=colour._toTk())
    _canvas.update()

### box() #####################################################################

def box(x0, y0, x1=None, y1=None, colour=None, filled=0):

    global _canvas_x, _canvas_y

    # Unpack arguments as for line() above

    tt = types.TupleType

    try: # catches unpacking errors
        if type(x0) is tt:
            if y1 is not None:          # Check for too many parameters
                raise ExBadParameters('too many coordinates')
            x1, y1 = y0, x1             # Shift parameters right
            x0, y0 = x0                 # and unpack first coordinate pair
        if type(x1) is tt:
            if y1 is not None:
                raise ExBadParameters('too many coordinates')
            x1, y1 = x1                 # Unpack second coordinate pair

    except ExBadParameters:     raise
    except:                     raise ExBadParameters('not a coordinate')

    y0 = _canvas_ys - y0
    y1 = _canvas_ys - y1

    if colour is None: colour = _canvas_col
    colour = colour._toTk()
    if filled: fill = colour
    else:      fill = '' # transparent

    if _returning:
      bobj = Movable(_canvas.create_rectangle(x0, y0, x1, y1,
                                               outline=colour, fill=fill),
                     [x0,y0,x1,y1])
      _canvas.update()
      return bobj
    else:
      _canvas.create_rectangle(x0, y0, x1, y1, outline=colour, fill=fill)
      _canvas.update()

### polygon() #################################################################

def polygon(coords, colour=None, closed=0, filled=0):

    global _canvas_x, _canvas_y

    tt = types.TupleType

    c, i, n = [], 0, len(coords)
    while i < n:
        x = coords[i]
        if type(x) is tt:
            c.append(x[0])
            c.append(_canvas_ys - x[1])
            i = i + 1
        elif i+1 < n:
            c.append(x)
            c.append(_canvas_ys - coords[i+1])
            i = i + 2
        else:
            raise ExBadParameters('not a coordinate')

    # c now contains a flattened, transformed coordinate list

    if closed: _canvas_x, _canvas_y = c[0], c[1]
    else:      _canvas_x, _canvas_y = c[-2], c[-1]

    if colour is None:  colour = _canvas_col

    if closed or filled:
        # Create a polygon
        if filled: fill = colour._toTk()
        else:      fill = '' # transparent
        if _returning:
          pobj = Movable(_canvas.create_polygon(c,
                                                outline=colour._toTk(),
                                                fill=fill),
                         c)
          _canvas.update()
          return pobj
        else:
          _canvas.create_polygon(c,
                                 outline=colour._toTk(),
                                 fill=fill)
    else:
        # Tk can't draw open polygons, so simulate it
        x, y, c = c[0], c[1], c[2:]
        while c:
            x1, y1, c = c[0], c[1], c[2:]
            _canvas.create_line(x, y, x1, y1, fill=colour._toTk())
            x, y = x1, y1
        # Alas, this doesn't work right if _returning
        if _returning:
            raise ExUnimplemented("can't make movable open polygon")
    _canvas.update()

### circle() ##################################################################

def circle(x, y, r=None, colour=None, filled=0, endpoints=None):

    global _canvas_x, _canvas_y

    # Unpack a tuple argument

    tt = types.TupleType

    if type(x) is tt:
        if r is not None: raise ExBadParameters('too many parameters')
        r = y                           # shift remaining argument
        x, y = x                        # and unpack tuple

    if colour is None: colour = _canvas_col
    colour = colour._toTk()
    if filled: fill = colour
    else:      fill = ''

    if r is not None and r < 0: raise ExBadParameters('negative radius')

    # If we have endpoints but no radius, work out the radius.
    # If the endpoints are given as angles or something, don't
    # try to set r from them.
    # WOMBAT: THIS DOESN'T WORK for some reason: wrong value of r, etc.
    # gjm, 2002-08-11: seems to work OK for me. Maybe it got fixed
    # since that comment was written?
    if r is None and endpoints is not None:
        try:
            if len(endpoints)==2:
                e=endpoints[0]
                if type(e) is tt:
                    r = math.sqrt((x-e[0])**2+(y-e[1])**2)
        except: pass

    if r is None: raise ExBadParameters('no radius supplied')

    y = _canvas_ys - y

    # We now have x,y = centre, r = radius, colour in Tk format
    # Tk wants the corners of an enclosing rectangle.

    x0, x1 = x - r, x + r + 1
    y0, y1 = y - r, y + r + 1

    if endpoints is None:
        # Entire circle requested: use create_oval
        _canvas_x, _canvas_y = x, y
        if _returning:
          cobj = MovableCircle(_canvas.create_oval(x0, y0, x1, y1,
                                                   outline=colour, fill=fill),
                               [x0,y0,x1,y1])
          _canvas.update()
          return cobj
        else:
          _canvas.create_oval(x0, y0, x1, y1, outline=colour, fill=fill)
          _canvas.update()

          return

    # An arc has been requested. If an endpoint is given as an angle,
    # life is easy, since this is what Tk wants. Otherwise, we have to do some
    # maths.

    if len(endpoints) != 2: raise ExBadParameters('wrong number of endpoints')

    e = []
    for i in endpoints:
        if type(i) is tt:
            # Check for an endpoint at the centre
            if i == (x, y): raise ExBadParameters('endpoint at centre')
            # Otherwise, calculate the angle represented
            e.append(math.atan2(i[1]-_canvas_ys+y,i[0]-x)*180/math.pi)
        else:
            e.append(i) # assumed numeric

    # Ensure the arc goes the right way. This is technically conformant
    # with the API specification, but slightly limiting, in that it won't
    # let one explicitly override direction using angle specifications.

    while e[0] > e[1]: e[1] = e[1] + 360

    if filled: style = 'pieslice'
    else:      style = 'arc'

    _canvas_x = x + r * math.cos(e[1] * math.pi/180)
    _canvas_y = y + r * math.sin(e[1] * math.pi/180)
    if _returning:
      cobj = MovableCircle(_canvas.create_arc(x0, y0, x1, y1,
                                              outline=colour, fill=fill,
                                              extent=e[1]-e[0], start=e[0],
                                              style=style),
                           [x0,y0,x1,y1])
      _canvas.update()
      return cobj
    else:
      _canvas.create_arc(x0, y0, x1, y1, outline=colour, fill=fill,
                         extent=e[1]-e[0], start=e[0], style=style)
      _canvas.update()

###############################################################################
### Text operations ###########################################################
###############################################################################

### text() ####################################################################

def text(t, colour=None, size=None, angle=0, serifs=None):

    if colour is None:  colour = _canvas_col
    if size is None:    size   = _canvas_tsize
    if serifs is None:  serifs = _canvas_tserifs

    # XXX Tk doesn't offer angle support, AFAICT
    # XXX We should probably update point

    temp = _canvas.create_text(_canvas_x, _canvas_y,
                               text=t,
                               anchor='sw',
                               fill=colour._toTk(),
                               font=(_canvas_tfonts[serifs == 0], size),
                               justify='left')
    _canvas.update()

    if _returning:
      return Movable(temp,[_canvas_x,_canvas_y])

### set_textsize() ############################################################

def set_textsize(s):
    global _canvas_tsize
    s, _canvas_tsize = _canvas_tsize, s
    return s

### set_textserifs() ##########################################################

def set_textserifs(flag):
    global _canvas_tserifs
    flag, _canvas_tserifs = _canvas_tserifs, flag
    return flag

###############################################################################
### Mouse support #############################################################
###############################################################################

# Polled mouse support requires us to register for mouse motion events,
# button presses, and entering/leaving the window. This could be rather
# expensive, particularly on slow machines, so we have a separate enabling
# routine.

### begin_mouse() #############################################################

def begin_mouse():
    global _mouse_enabled
    if _mouse_enabled: raise ExAlreadyStarted('begin_mouse() already called')
    _canvas.bind("<Motion>",            _mouse_move)
    _canvas.bind("<Leave>",             _mouse_leave)
    _canvas.bind("<Button-1>",          _mouse_button1down)
    _canvas.bind("<Button-2>",          _mouse_button2down)
    _canvas.bind("<Button-3>",          _mouse_button3down)
    _canvas.bind("<ButtonRelease-1>",   _mouse_button1up)
    _canvas.bind("<ButtonRelease-2>",   _mouse_button2up)
    _canvas.bind("<ButtonRelease-3>",   _mouse_button3up)
    _mouse_enabled = 1

### end_mouse() ###############################################################

def end_mouse():
    # XXX Need to think about interaction with end_graphics()
    global _mouse_enabled
    _canvas.bind("<Motion>")
    _canvas.bind("<Leave>")
    _canvas.bind("<Button-1>")
    _canvas.bind("<Button-2>")
    _canvas.bind("<Button-3>")
    _canvas.bind("<ButtonRelease-1>")
    _canvas.bind("<ButtonRelease-2>")
    _canvas.bind("<ButtonRelease-3>")
    _mouse_enabled = 0

### mouse_position() ##########################################################

def mouse_position():
    if _mouse_x is None: return None
    else:                return (_mouse_x, _mouse_y)

### mouse_buttons() ###########################################################

def mouse_buttons():
    return {'left':   _mouse_b & 1 != 0,
            'middle': _mouse_b & 2 != 0,
            'right':  _mouse_b & 4 != 0}

### mouse_wait() ##############################################################

# XXX What happens if the window closes? Exception?

def mouse_wait(how):
    if how == 'down':
        while _mouse_b == 0: _root_window.dooneevent()
    elif how == 'up':
        while _mouse_b != 0: _root_window.dooneevent()
    elif how == 'change':
        b = _mouse_b
        while _mouse_b == b: _root_window.dooneevent()
    elif how == 'click':
        b = _mouse_b
        while b & ~_mouse_b == 0:
            b = _mouse_b
            _root_window.dooneevent()
    elif how == 'move':
        x, y = _mouse_x, _mouse_y
        while x == _mouse_x and y == _mouse_y: _root_window.dooneevent()
    elif how == 'any':
        x, y, b = _mouse_x, _mouse_y, _mouse_b
        while x == _mouse_x and y == _mouse_y and b == _mouse_b:
            _root_window.dooneevent()
    else:
        raise ExBadParameters('bad mouse_wait() type')

### _mouse_move() #############################################################

def _mouse_move(e):
    global _mouse_x, _mouse_y
    _mouse_x, _mouse_y = e.x, e.y

### _mouse_leave() ############################################################

def _mouse_leave(e):
    global _mouse_x, _mouse_y
    _mouse_x, _mouse_y = None, None

### _mouse_buttonxdown() ######################################################

def _mouse_button1down(e): _mouse_buttondown(e, 0)
def _mouse_button2down(e): _mouse_buttondown(e, 1)
def _mouse_button3down(e): _mouse_buttondown(e, 2)

def _mouse_button1up(e): _mouse_buttonup(e, 0)
def _mouse_button2up(e): _mouse_buttonup(e, 1)
def _mouse_button3up(e): _mouse_buttonup(e, 2)

_mouse_b = 0

def _mouse_buttondown(e, n):
    global _mouse_b
    _mouse_b = _mouse_b | (1 << n)
def _mouse_buttonup(e, n):
    global _mouse_b
    _mouse_b = _mouse_b &~ (1 << n)

##############################################################################
### Keypress handling ########################################################
##############################################################################

# We bind to key-down and key-up events.

_keysdown = {}
# This holds an unprocessed key release.  We delay key releases by up-to
# one call to keys_pressed() to get round a problem with auto repeat.
_got_release = None

def _keypress(event):
    global _got_release
    _keysdown[event.char] = 1
    _got_release = None

def _keyrelease(event):
    global _got_release
    try: del _keysdown[event.char]
    except: pass
    _got_release = 1

def _clear_keys(event=None):
    global _keysdown, _got_release
    _keysdown = {}
    _got_release = None

def keys_pressed(d_o_e=Tkinter.tkinter.dooneevent,
                 d_w=Tkinter.tkinter.DONT_WAIT):
    d_o_e(d_w)
    if _got_release:
      d_o_e(d_w)
    return _keysdown.keys()

# Block for a list of keys...

def wait_for_keys():
    keys = []
    while keys==[]:
        keys = keys_pressed()
    thekeys = keys
    while keys != []:
        keys = keys_pressed()
    return thekeys


##############################################################################
### Random number things #####################################################
##############################################################################

# In order to avoid having to explain modules at an early stage,
# we provide some friendly synonyms for the random.blah functions.

random_choice = random.choice
random_between = random.randint

###############################################################################
### Slightly friendlier input #################################################
###############################################################################

# The name "raw_input" is a little forbidding, so we rename it.
# We also provide some other reading functions that do useful things.

read_string = raw_input

def read_number(prompt='Please enter a number: '):
    numeric_types = [types.ComplexType, types.FloatType,
                     types.IntType, types.LongType];
    if prompt<>'' and prompt[-1] not in string.whitespace:
        prompt = prompt + ' '
    while 1:
        result = input(prompt)
        if type(result) in numeric_types:
            return result
        print "But that wasn't a number!"

def read_yesorno(prompt='Yes or no? '):
    if prompt<>'' and prompt[-1] not in string.whitespace:
        prompt = prompt + ' '
    while 1:
        result = raw_input(prompt)
        try: result = string.lower(string.split(result)[0])
        except: result=''
        if result=='yes' or result=='y': return 1
        if result=='no' or result=='n': return 0
        print "Please answer yes or no."

###############################################################################
### Rudimentary movable-object support ########################################
###############################################################################

def allow_movables():
    global _returning
    _returning = 1

def forbid_movables():
    global _returning
    _returning = 0

allow_moveables  = allow_movables
forbid_moveables = forbid_movables

def remove_from_screen(x,
                       d_o_e=Tkinter.tkinter.dooneevent,
                       d_w=Tkinter.tkinter.DONT_WAIT):
    _canvas.delete(x.id)
    d_o_e(d_w)

def _adjust_coords(coord_list,x,y):
    for i in range(0,len(coord_list),2):
        coord_list[i]   = coord_list[i] + x
        coord_list[i+1] = coord_list[i+1] + y
    return coord_list

def move_by(object, x,y=None,
            d_o_e=Tkinter.tkinter.dooneevent,
            d_w=Tkinter.tkinter.DONT_WAIT):
    if y is None:
        try: x,y = x
        except: raise ExBadParameters('incomprehensible coordinates')
    y = -y;
    apply(_canvas.coords, (object.id,) + tuple(_adjust_coords(object.coord_list,x,y)))
    d_o_e(d_w)

def move_to(object, x,y=None,
            d_o_e=Tkinter.tkinter.dooneevent,
            d_w=Tkinter.tkinter.DONT_WAIT):
    if y is None:
        try: x,y = x
        except: raise ExBadParameters('incomprehensible coordinates')
    y = _canvas_ys - y
    ox,oy = object.coords()[:2]
    apply(_canvas.coords, (object.id,) + tuple(_adjust_coords(object.coord_list,x-ox,y-oy)))
    d_o_e(d_w)

###############################################################################
###############################################################################
###############################################################################

def test():
    begin_graphics()
    try:
        magenta = 0.75*Colour.red + 0.75*Colour.blue
        print 'Magenta is', magenta
        set_colour(Colour.red)
        move(0,0)
        draw(200,200)
        draw((400,200), colour=Colour.green)
        for y in xrange(200,99,-1):
            plot(402,y,colour=Colour.blue)
        line((400,200), 400,0, colour=Colour.red)
        polygon(((300,300),(350,400),(400,350)), colour=Colour.green, filled=1)
        polygon(((500,300),(550,400),(600,350)), colour=Colour.blue)
        polygon(((510,300),(560,400),(610,350)), colour=Colour.blue, closed=1)
        box((50,400),100,450, colour=Colour.red, filled=1)
        circle(200,200,40,colour=Colour.red, filled=1)
        circle(200,200,50,colour=Colour.green, endpoints=(10,45))
        circle(200,200,50,colour=Colour.blue,
               endpoints=((195,190), 200), filled=1)
        move(100,100)
        text('Hello world', serifs=1, size=14)
    # XXX Think about how to handle errors in programs that prevent
    #     end_graphics() being reached.
    finally:
        pass
    if 1:
        end_graphics()
        print 'Done'

if __name__ == '__main__': test()

###############################################################################
###############################################################################
###############################################################################
