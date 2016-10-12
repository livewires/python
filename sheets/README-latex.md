# Livewires Python Course #

Release 1.3


# INTRODUCTION #

This is the LaTeX source distribution of the LiveWires Python Course,
release 1.2. It consists of a number of worksheets which are intended to
help people who have not programmed before to learn the Python language.
The sheets are written in LaTeX in such a way that PDF and Postscript
versions of the sheets can be produced from them.

This source distribution is only intended for people who want to modify
the worksheets. If you just want to use them to learn Python, you should
get the PDF distribution.

Modification and distribution of the course:
--------------------------------------------

The worksheets are distributed under the LiveWires Documentation
Licence, which is a BSD-like licence for documentation. You can find the
licence in the COPYING.txt file, which should have come with this
distribution, and also in the LaTeX source files themselves.

REMEMBER that compliance with this licence is required if you wish to
modify and distribute the course. The mkcopying.py script will help with
this: see below for more information.

NOTE: If you modify the sheets and so produce a derived work of them,
note that the licence requires that you do not use the LiveWires name
to promote this work.


# USE #

What you will need to use the source:
-------------------------------------

- You will need a working LaTeX system, including pdflatex. Please don't
  ask us how to get LaTeX working, as we're not experts. Pre-packaged
  versions of LaTeX are available for most operating systems.

    [On OS X, you can try `brew install mactex`.]

- Your life will be easier if you have a working Unix "make" utility (we
  use GNU Make). If you're using Windows, try the Cygnus utilities.

- You will need the "rcs" LaTeX package to handle the version control
  information in the files. If it's not already installed, CTAN (the TeX
  archive network) has this package.

- You will need to put the LiveWires worksheet class file (wsheet.cls)
  on your system in a place where LaTeX will find it. Where this is
  varies from distribution to distribution.

- You will need a working knowledge of LaTeX to make alterations to the
  sheets, and of how to use "make".

How to build using make:
------------------------

Uncompress the archive, change directory into the sheets directory, and
type:

    make all

If all goes well, after a little while you will find PDF versions of all
the worksheets in the same directory as the source. If it doesn't,
ensure you have all the pre-requisites listed above.

If you add extra LaTeX files to the course, you'll need to alter the
makefile to ensure that they're included when doing a "make all". The
SOURCES and TARGETS settings both need to be changed. 

You can make individual sheets by typing

    make sheetname.pdf

Note that the makefile doesn't include the dependancies of the sheets on
the diagrams. If you want to all this, feel free.

pdflatex requires PDF versions of the diagrams, latex requires EPS
versions. In your documents, it's best to write \includegraphics{file}
without specifying the extension, so they will work with either pdflatex
or latex. If you've produced an EPS file, you can make the equivalent
PDF with epstopdf, which should have come with your pdflatex
distribution.

Life without make:
------------------

If you don't have make, you can type

    pdflatex sourcefile.ltx

to produce the relevant PDF file. You might need to run it twice to get
the table of contents right.

mkcopying.py:
-------------

The mkcopying.py script produces the copyright statement (which is
required by the licence when the PDF versions are distributed without
the source) for each worksheet, to go at the top of the COPYING.txt
file. It assumes that you've written

    \copyright{} J Random Hacker. All rights reserved.
    \copyright{} A N Modifier. All rights reserved.

somewhere in your worksheet source. 

The COPYING.txt target in the makefile produces a COPYING.txt file from
the output of the script and the standard licence file.

pdfrelease:
-----------

The pdfrelease target produces a release .zip file of the PDFs in the
release, along with the README.txt and COPYING.txt files.

srcrelease:
-----------

The srcrelease target produces a source .tar.gz file containing the
LaTeX source, along with the necessary diagram source files and other
files required to build the PDFs using LaTeX.

If you add extra files you'll need to alter the SOURCES or AUX (the
non-latex source files) to ensure they are included in the release.

Comments and corrections:
-------------------------

If you have comments on the course or you spot any typos, you can email
the maintainers at python@livewires.org.uk. We like context diffs
(diff -c oldversion newversion).

Note: we don't consider the use of British spellings (colour, grey and
so on) to be typos. :-)

Please don't email us with general Python or LaTeX queries as we don't
have time to answer them all. You could try posting a question to the
comp.lang.python newsgroup if you get stuck with Python.


# BACKGROUND #

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
