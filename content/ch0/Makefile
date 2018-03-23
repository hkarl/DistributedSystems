.PHONY: chapters all slides clean book bookpdf cleanall

# on Holger's Mac: 
EMACS="/Applications/Aquamacs 2.app/Contents/MacOS/Aquamacs"



SOURCE := $(wildcard *-slides.org)
slidesTex := $(patsubst %.org,%.tex,$(SOURCE))
slidesPdf := $(patsubst %.org,%.pdf,$(SOURCE))
bookTex := $(patsubst %.org,%-chapter.tex,$(wildcard *.org))

all: chapters book

chapters:
	for d in ch*; do make -C $$d slides  ; done

#########################

book: 
	make -C book book.pdf 

book.tex: book.org  
	echo "making book.tex"
	echo "building beamer tex file", $<, $@
	${EMACS} -Q --batch $<  -eval "(progn (add-to-list 'load-path (expand-file-name \"~/.emacs.d/org-mode/lisp\")) (require 'org) (org-beamer-export-to-latex))"


book.pdf: book.tex
	pdflatex book
	# -bibtex book
	# pdflatex book
	# pdflatex book
	cp $@ ../output 

#########################

slides: $(slidesPdf)
	make $<

%-slides.tex: %-slides.org %.org ../slidehead.org 
	echo "building beamer tex file", $<, $@
	${EMACS} -Q --batch $<  -eval "(progn (add-to-list 'load-path (expand-file-name \"~/.emacs.d/org-mode/lisp\")) (require 'org) (org-beamer-export-to-latex))"


%-slides.pdf: %-slides.tex
	pdflatex $< 
	pdflatex $< 
	cp $@ ../output 

##########################

clean:
	-rm *.tex *.tex~ tmp.org *.pdf *.bbl
	-rm -rf _minted*
	-rm *.aux *.log *.nav *.out *.snm *.toc 

cleanall:
	-cd book ; rm *.pdf *.aux *.log *.bbl *.tex *.tex~ *.toc *.aux *.bbl *.log *.blg *.out
	for d in ch*; do make -C $$d clean  ; done
