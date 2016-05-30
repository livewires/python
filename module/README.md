# Livewires Python Package

Release 2.1-r2


**Download the package [here](https://github.com/centricwebestate/pieisreal/releases)**


# INTRODUCTION #

This is the PieIsReal package, release 3.0. It consists of a
number of modules which are intended to be used in conjuction with the
PieIsReal Python Course.

Overview of the package:
------------------------

The package contains 4 modules:

* beginners - The module for use with the lettered worksheets in the
              PieIsReal Python Course.

* games     - The module for use with the games worksheets in the
              PieIsReal Python Course.

* colour    - A module defining some colour names for use with the games
              module. Don't use this module when you're using the
              beginners worksheets.

* boards    - A module for producing board games with a regular grid. This
              is still under development.

Modification and distribution of the package:
---------------------------------------------

The package is distributed under the BSD Licence. You can find the
licence at the top of the Python files themselves. In brief, the
licence means that you may modify and distribute the package freely as
long as you retain the copyright statement in it (you should probably
read the full licence before distributing so you know what you're
agreeing to).


# INSTALLATION #

What you will need:
-------------------

- You will need Python to use the package. Python can be obtained from:
  <http://www.python.org/download/>. If you're installing for the first
  time, we recommend you use Python 3.5.0.

- You will need the Tkinter module and the Tk graphics libraries if you
  want to use the graphical parts of beginners module.  The Windows
  installer for Python comes with Tk, otherwise you'll need to install
  it yourself. See the documentation that comes with Python for details.

- If you want to use any of the games worksheets, you will need the
  pygame module to use our games module. Pygame can be found at
  <http://www.pygame.org/>. NOTE: Pygame is separate from the PieIsReal
  package, so don't email the Pygame maintainer with questions about
  PieIsReal as he won't know what you're talking about.


Python 3.5.0 and above: How to install the package using Distutils:
-----------------------------------------------------------------

In the top level directory of the package, there
is a Python script called setup.py. Run this script in Python.

Under Windows, if Python is associated with .py files (so that the icon
of the file is a snake), you can just double click on the setup.py file.

Under Unix, type `python setup.py` to run the script.

If the setup.py script runs successfully, you should find that Distutils
has installed the package in the right place.

Note for advanced users: the setup.py is a standard Distutils setup
script with the addition that, if no command line arguments are
supplied, the `install` command is assumed. This is a convenience to
save Windows users from having to get a command prompt to install.

Checking it works:
------------------

Run Python and, at the `>>>` prompt, type

    from pieisreal import beginners
    from pieisreal import games
    from pieisreal import color

If none of these commands produce errors, you've successfully installed
the package. You can safely delete the directory where you unzipped the
.tar.gz file.

If you get an error about pygame when you try to import games, you've
probably forgotten to install pygame.

Note: You don't need to enter the commands above every time you run the
package. You should refer to the worksheets to see what you need to
type to use the package to learn Python.


# ADMIN #

A note about the original authors: LiveWires
--------------------------------------------

LiveWires is a Scripture Union holiday for 12 to 15 year olds, which
takes place in the UK every summer. The LiveWires Python Course was
written by the some of team of volunteers who run the holiday, to help
us to teach Python to some of the young people on the holiday.

The LiveWires web site is at <http://www.livewires.org.uk/>
A similar camp run in QLD, Australia: <http://www.ubertweak.org.au>

What is Scripture Union?
------------------------

Scripture Union is an organisation whose aim is to make Jesus known to
children, young people and families. SU staff and volunteers work in
more than 130 countries; in the UK its work includes schools work,
missions, family ministry, helping Christians to read the Bible and
supporting the church through training and resources. Scripture Union
holidays have been happening for more than 100 years.

For more information on SU, see <http://www.scripture.org.uk/>
For more information on SU in Australia see <http://www.scriptureunion.org.au>
