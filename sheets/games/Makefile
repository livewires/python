# Yet another makefile
# $Id: Makefile,v 1.2 2000/10/03 21:58:04 paul Exp paul $

.SUFFIXES: .ltx .dvi .ps .pdf

.ltx.dvi:
	latex $(LATEX_OPTS) $<
.dvi.ps:
	dvips -o $@ $<
.ltx.pdf:
	pdflatex $(LATEX_OPTS) $<; pdflatex $(LATEX_OPTS) $<

# Note: if you add to these and want your LaTeX source to go in the
# source release archive, you'll need to add the filenames of the latex
# source to the AUX definition in makefile in the directory above.

TARGETS = asteroid.pdf spacewar.pdf pacman.pdf chain.pdf draughts.pdf \
fifteen.pdf minesweeper.pdf othello.pdf robots.pdf scramfender.pdf \
snake.pdf tetris.pdf

SOURCES = asteroid.ltx spacewar.ltx pacman.ltx chain.ltx draughts.ltx \
fifteen.ltx minesweeper.ltx othello.ltx robots.ltx scramfender.ltx \
snake.ltx tetris.ltx

all: $(TARGETS) COPYING.txt

clean: 
	rm -f $(TARGETS) *.aux *.log *.out

COPYING.txt: ../COPYING.txt.src $(SOURCES) ../mkcopying.py
	echo "THE LIVEWIRES DOCUMENTATION LICENCE" > COPYING.txt
	echo "" >> COPYING.txt
	echo "COPYRIGHT NOTICE:" >> COPYING.txt
	echo "" >> COPYING.txt
	python ../mkcopying.py $(SOURCES) >> COPYING.txt
	echo "The documents referred to above are each subject to the" >> COPYING.txt
	echo "conditions and disclaimer below." >> COPYING.txt

	cat ../COPYING.txt.src >> COPYING.txt


