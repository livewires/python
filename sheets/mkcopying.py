#!/usr/bin/env python
# $Id: mkcopying.py,v 1.3 2000/10/04 20:35:25 paul Exp paul $
# Usage: give it the filenames of the LaTeX sheets.

import string
import re
import sys 
NOTFOUND = -1

TitleMatcher = re.compile (r"^\\sheet{(.*?)}{(.*?)}")
CopyrightMatcher = re.compile (r"^\s*\\copyright{}\s*(.*)$")

def gettitle (infile):
	while 1:
		line = infile.readline ()
		if line == "": break

		m = TitleMatcher.match (line)
		if m:
			rawtitle = m.groups ()
			title = string.join (rawtitle, ": ")
			return title

def getcopyrights (infile):
	rights = []
	while 1:
		line = infile.readline ()
		if line == "": break

		m = CopyrightMatcher.match (line)
		if m:
			rights.append(m.group (1))

	return rights

if __name__ == '__main__':
	
	copyrights={}
	
	for fname in sys.argv [1:]:
		file = open (fname, "r")
		title = gettitle (file)
		copyrights [title] = getcopyrights (file)
		file.close ()
	
	print "The copyright notices for each document in this distribution"
	print "are as follows:\n"
	
	keylist=copyrights.keys()
	keylist.sort ()
	for title in keylist:
	
		print title
		for copy in copyrights [title]:
			print "    Copyright " + copy
		print ""
	
	




