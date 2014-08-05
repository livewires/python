# Makefile for LW worksheets
# $Id: Makefile,v 1.12 2001/10/28 21:41:51 paul Exp paul $
# pdrelease is probably the target you want to produce a tar.gz file
# all target is all the worksheets in PDF format

.SUFFIXES: .ltx .dvi .ps .pdf

.ltx.dvi:
	latex $(LATEX_OPTS) $<
.dvi.ps:
	dvips -o $@ $<
.ltx.pdf:
	pdflatex $(LATEX_OPTS) $< $@; pdflatex $(LATEX_OPTS) $< $@

# If you add LaTeX source files, you'll need to change both SOURCES and
# TARGETS. Don't include things in the games directory in SOURCES or
# TARGETS as that directory has its own makefile. 
TARGETS = 1-intro.pdf 2-tables.pdf 3-pretty.pdf 4-highlow.pdf \
5-robots.pdf A-lists.pdf C-conds.pdf D-dicts.pdf E-errors.pdf \
F-functions.pdf G-graphics.pdf I-inout.pdf J-jargon.pdf L-loops.pdf \
M-modules.pdf O-objects.pdf R-running.pdf S-strings.pdf T-time.pdf \
U-usage.pdf V-overview.pdf W-livewires.pdf

SOURCES = 1-intro.ltx 2-tables.ltx 3-pretty.ltx 4-highlow.ltx \
5-robots.ltx A-lists.ltx C-conds.ltx D-dicts.ltx E-errors.ltx \
F-functions.ltx G-graphics.ltx I-inout.ltx J-jargon.ltx L-loops.ltx \
M-modules.ltx O-objects.ltx R-running.ltx S-strings.ltx T-time.ltx \
U-usage.ltx V-overview.ltx W-livewires.ltx

# Files which are not SOURCES in this makefile but should be included in
# the source release archive. Note that this includes the LaTeX source
# under games, as I've not worked out how to get recursive make to
# handle the production of the source archive.
AUX = COPYING.txt COPYING.txt.src Makefile README.md README-latex.txt \
TEMPLATE.ltx blurb.ltx figures/bullet.eps figures/bullet.pdf \
figures/compass.eps figures/compass.pdf figures/coords.eps \
figures/coords.pdf figures/face-grid.eps figures/face-grid.pdf \
figures/face.eps figures/face.pdf figures/grid.eps figures/grid.pdf \
figures/objectgraph.eps figures/objectgraph.pdf figures/robomove.eps \
figures/robomove.pdf figures/ship.eps figures/ship.pdf figures/stick.eps \
figures/stick.pdf figures/othello-capture.eps \
figures/othello-capture.pdf figures/othello-grid.eps \
figures/othello-grid.pdf figures/terrain.eps figures/terrain.pdf \
figures/terrain-params.eps figures/terrain-params.pdf \
figures/terrain-path.eps figures/terrain-path.pdf \
figures/tetris-line-rotate.eps figures/tetris-line-rotate.pdf \
figures/tetris-L-rotate.eps figures/tetris-L-rotate.pdf \
figures/tetris-T-rotate.eps figures/tetris-T-rotate.pdf \
figures/tetris-Z-rotate.eps figures/tetris-Z-rotate.pdf \
figures/ufo-shoot.eps figures/ufo-shoot.pdf \
games/COPYING.txt games/Makefile games/asteroid.ltx \
games/pacman.ltx games/spacewar.ltx wsheet.cls mkcopying.py \
CHANGES.txt games/asteroid.bmp games/stars.bmp games/chain.ltx \
games/draughts.ltx games/fifteen.ltx games/minesweeper.ltx \
games/othello.ltx games/robots.ltx games/scramfender.ltx \
games/snake.ltx games/tetris.ltx games/jen.bmp games/jen0.bmp \
games/jen1.bmp games/jen2.bmp games/jen3.bmp games/jen4.bmp \
games/jen5.bmp games/jen6.bmp games/jen7.bmp games/jen8.bmp \
games/jen9.bmp games/jen10.bmp games/jen11.bmp games/jen12.bmp \
games/jen13.bmp games/jen14.bmp

# Files which aren't PDF files but should go in the PDF release
PDFAUX=README.md COPYING.txt games/COPYING.txt CHANGES.txt\
games/asteroid.bmp games/stars.bmp

all: $(TARGETS) games

clean:	force_look
	cd games; $(MAKE) clean
	rm -f $(TARGETS) *.aux *.log *.out

games:	force_look
	cd games; $(MAKE) 

force_look:

COPYING.txt: COPYING.txt.src $(SOURCES) mkcopying.py
	echo "THE LIVEWIRES DOCUMENTATION LICENCE" > COPYING.txt
	echo "" >> COPYING.txt
	echo "COPYRIGHT NOTICE:" >> COPYING.txt
	echo "" >> COPYING.txt
	python mkcopying.py $(SOURCES) >> COPYING.txt
	echo "The documents referred to above are each subject to the" >> COPYING.txt
	echo "conditions and disclaimer below." >> COPYING.txt
	cat COPYING.txt.src >> COPYING.txt

../release:
	mkdir ../release

../release/livewires-pdfs.tar.gz: all README.md COPYING.txt CHANGES.txt ../release
	tar --dereference -cvf ../release/livewires-pdfs.tar ./*.pdf games/*.pdf \
	$(PDFAUX)
	gzip --force --best ../release/livewires-pdfs.tar

../release/livewires-ltx.tar.gz: $(SOURCES) $(AUX) ../release
	tar --dereference -cvf ../release/livewires-ltx.tar $(SOURCES) $(AUX)
	gzip --force --best ../release/livewires-ltx.tar

pdfrelease: ../release/livewires-pdfs.tar.gz

srcrelease: ../release/livewires-ltx.tar.gz

