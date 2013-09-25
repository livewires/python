# Livewires Python Package

Release 2.1-r2


**Download the package [here](https://github.com/livewires/python/releases)**


# INTRODUCTION #

This is the LiveWires package, release 2.1 revision 2. It consists of a
number of modules which are intended to be used in conjuction with the
LiveWires Python Course.

Overview of the package:
------------------------

The package contains 4 modules:

* beginners - The module for use with the lettered worksheets in the
              LiveWires Python Course. This was written before the other
              two modules and was originally the entire LiveWires package.
              That's why `from livewires import *` imports everything from
              the beginners module (and why the implementation of colours
              is inconsistent between the beginners and games modules).

* games     - The module for use with the games worksheets in the
              LiveWires Python Course.

* colour    - A module defining some colour names for use with the games
              module. Don't use this module when you're using the
              beginners worksheets.

* boards    - A module for producing board games with a regular grid. This
              is a new module for release 2.1 and effectively still under
              development.

The package has been used on versions of Python from 1.5.2 to 2.4, but
the games module now uses PyGame which requires at least version 2.1.
Release 2.1 experienced some compatibility problems with Python 2.3 and
later (or more specifically Tk8.4 which those include) which are hopefully
corrected by this revision.

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
  time, we recommend you use Python 2.2.3.

- You will need the Tkinter module and the Tk graphics libraries if you
  want to use the graphical parts of beginners module.  The Windows
  installer for Python comes with Tk, otherwise you'll need to install
  it yourself. See the documentation that comes with Python for details.

- If you want to use any of the games worksheets, you will need the
  pygame module to use our games module. Pygame can be found at
  <http://www.pygame.org/>. NOTE: Pygame is separate from the LiveWires
  package, so don't email the Pygame maintainer with questions about
  LiveWires as he won't know what you're talking about.

- You will also need the Distutils package to install the LiveWires
  package, unless you want to do it by hand. Distutils comes built into
  Python starting with version 1.6. For version 1.5.2, you can download
  it from <http://www.python.org/sigs/distutils-sig/download.html>
  You'll need to read the README file that comes with it to work out
  how to install it.

Python 1.6 and above: How to install the package using Distutils:
-----------------------------------------------------------------

In the top level directory of the LiveWires-2.1 package, there
is a Python script called setup.py. Run this script in Python.

Under Windows, if Python is associated with .py files (so that the icon
of the file is a snake), you can just double click on the setup.py file.

Under Unix, type `python setup.py` to run the script.

If you get an error message from Python about the distutils package,
you've forgotten to install it (see "What you will need" above). If you
get a message from your system saying that it cannot find python, you'll
need to make sure that the python executable is on your PATH, or provide
the path to it explicitly.

If the setup.py script runs successfully, you should find that Distutils
has installed the package in the right place.

Note for advanced users: the setup.py is a standard Distutils setup
script with the addition that, if no command line arguments are
supplied, the `install` command is assumed. This is a convenience to
save Windows users from having to get a command prompt to install.

Python 1.5.2: Installing without distutils:
-------------------------------------------

If you haven't got distutils, the following might help you to install
manually.

Make a directory called livewires wherever your Python distribution
keeps site-specific modules. Put the contents of the livewires directory
in the archive into that directory. Ensure that the directory is
readable by the people who you want to be able to use the package.

On my Debian Linux machine, I put the files into

    /usr/local/lib/python1.5/site-packages/livewires/

On Windows machines, I put the files into

    c:\program files\python\livewires

or

    c:\python21\livewires

Depending on how your machine is set up, these suggestions may or may
not work for you. That's what Distutils is there to sort out, of course.

Checking it works:
------------------

Run Python and, at the `>>>` prompt, type

    from livewires import beginners
    from livewires import games
    from livewires import colour

If none of these commands produce errors, you've successfully installed
the package. You can safely delete the directory where you unzipped the
.tar.gz file.

If you get an error about pygame when you try to import games, you've
probably forgotten to install pygame.

Note: You don't need to enter the commands above every time you run the
package. You should refer to the worksheets to see what you need to
type to use the package to learn Python.


# ADMIN #

Comments and corrections:
-------------------------

If you have comments on the course or you spot any typos, you can email
the maintainers at python@livewires.org.uk

Please don't email us with general Python programming queries as we
don't have time to answer them all. You could try posting a question to
the comp.lang.python newsgroup if you get stuck. Better yet, the
python-tutor email list exists to help people learn Python: you can
find details at <http://mail.python.org/mailman/listinfo/tutor>

Note: we don't consider the use of British spellings (licence, colour,
grey, centre and so on) to be typos. :-)

The main web site for the distribution of the package and worksheets is
at <http://www.livewires.org.uk/python/>

What is LiveWires?
-------------------

LiveWires is a Scripture Union holiday for 12 to 15 year olds, which
takes place in the UK every summer. The LiveWires Python Course was
written by the some of team of volunteers who run the holiday, to help
us to teach Python to some of the young people on the holiday.

The LiveWires web site is at <http://www.livewires.org.uk/>

What is Scripture Union?
------------------------

Scripture Union is an organisation whose aim is to make Jesus known to
children, young people and families. SU staff and volunteers work in
more than 130 countries; in the UK its work includes schools work,
missions, family ministry, helping Christians to read the Bible and
supporting the church through training and resources. Scripture Union
holidays have been happening for more than 100 years.

For more information on SU, see <http://www.scripture.org.uk/>
