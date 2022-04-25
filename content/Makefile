.PHONY: chapters chapter all slides slides169 handout clean book cleanall dirfigures quick

# Use .SECONDARY with no argument is a little overkill, but using %.tex does not work
# because we need to refer to .tex files in subdirectories. make does not allow %/%.tex. 
.SECONDARY: 



EMACS=emacs
# typical alternatives can be something like:
# EMACS="/Applications/Emacs.app/Contents/MacOS/Emacs" 

EMACSEXPORTPARAMS= --batch -l ../templates/emacs_init.el -f org-beamer-export-to-latex

# pdflatex command
PDFLATEX=pdflatex -shell-escape -interaction=nonstopmode
BIBCOMMAND=biber


BookSources := $(shell find .. -name "ch*.org")
SOURCE := $(wildcard *-slides.org)
slidesTex := $(patsubst %.org,%.tex,$(SOURCE))
slidesPdf := $(patsubst %.org,%.pdf,$(SOURCE))
slides169Pdf := $(patsubst %.org,%169.pdf,$(SOURCE))
handoutPdf := $(patsubst %-slides.org,%-handout.pdf,$(SOURCE))
bookTex := $(patsubst %.org,%-chapter.tex,$(wildcard *.org))

# Setting environment for HPI slides right
.EXPORT_ALL_VARIABLES:
TEXINPUTS=".:../hpi-slides/src:./hpi-slides/src::"
TFMFONTS=".:../hpi-slides/src:./hpi-slides/src::"
TTFONTS=".:../hpi-slides/src:./hpi-slides/src::"



# build order for all is important; have to make sure that
# book.aux file exists for inter-chapter cross-references 
all: 
	-make chapterfigures
	-make book
	-make chapters

chapters:
	for d in ch*; do make -C $$d chapter  ; done

chapterfigures:
	for d in ch*; do make -C $$d/figures ; done 

#########################

book:
	make -C book book.pdf 

book.tex: book.org  $(BookSources)
	echo "making book.tex"
	echo "building beamer tex file", $<, $@
	${EMACS} -Q --batch $<  -eval ${EMACSEXPORTPROG}
	grep -v "begin{LaTeX}" $@ | grep -v "end{LaTeX}" | sponge $@


book.pdf: book.tex
	-${PDFLATEX} book
	-${BIBCOMMAND} book
	-${PDFLATEX} book
	-${PDFLATEX} book
	cp $@ ../../output 

#########################

chapter: slides handout slides169 

quick:
	quick=True make slides

slides: $(slidesPdf) 
	-make -C figures
	-make $<

handout: $(handoutPdf)
	-make -C figures
	-make $<

slides169: $(slides169Pdf) 
	-make -C figures
	-make $<

%-slides.tex: %-slides.org %.org ../slidehead.org  ../references.org ../acronyms.tex
	echo "building beamer tex file", $<, $@
	${EMACS} $<  ${EMACSEXPORTPARAMS}
	# grep -v "begin{LaTeX}" $@ | grep -v "end{LaTeX}" | sponge $@


%-slides.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib ../book/book.aux 
	-${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
ifndef quick
	-${BIBCOMMAND} $(basename $<)
	-${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
	-${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
	cp $@ ../../output/slides/
endif

%-handout.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib ../book/book.aux  
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	-${BIBCOMMAND} $(patsubst %-slides.tex,%-handout,$<)
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	cp $@ ../../output/handout/

%-slides169.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib  ../book/book.aux 
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
ifndef quick
	${BIBCOMMAND} $(patsubst %-slides.tex,%-slides169,$<)
	#cp $(basename $<).bbl  $(basename $<)169.bbl
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	-${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	cp $@ ../../output/slides169/
endif



##########################

clean:
	-rm *.tex *.tex~ tmp.org *.pdf *.bbl *.vrb
	-rm -rf _minted*
	-rm *.aux *.log *.nav *.out *.snm *.toc *.pyg  *.bcf *.blg *.synctex.gz  *.fls *.fdb_latexmk *.run.xml *.auxlock

cleanall:
	-cd book ; rm *.pdf *.aux *.log *.bbl *.tex *.tex~ *.toc *.aux *.bbl *.log *.blg *.out *.vrb
	for d in ch*; do make -C $$d clean  ; done


dirfigures:
	mkdir figures
	cd figures ; ln -s ../../ch_00/figures/Makefile

