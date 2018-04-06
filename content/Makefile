.PHONY: chapters chapter all slides slides169 handout clean book bookpdf cleanall figures

# on Holger's Mac: 
EMACS="/Applications/Aquamacs 2.app/Contents/MacOS/Aquamacs"

EMACSEXPORTPROG="(progn (add-to-list 'load-path (expand-file-name \"~/.emacs.d/org-mode/lisp\")) (require 'org)  (setq org-latex-listings 'minted) (setq org-latex-minted-options '((\"frame\" \"lines\") (\"linenos=true\") (\"mathescape\" \"true\"))) (org-beamer-export-to-latex))"

SOURCE := $(wildcard *-slides.org)
slidesTex := $(patsubst %.org,%.tex,$(SOURCE))
slidesPdf := $(patsubst %.org,%.pdf,$(SOURCE))
slides169Pdf := $(patsubst %.org,%169.pdf,$(SOURCE))
handoutPdf := $(patsubst %-slides.org,%-handout.pdf,$(SOURCE))
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
	${EMACS} -Q --batch $<  -eval ${EMACSEXPORTPROG}


book.pdf: book.tex
	pdflatex -shell-escape book
	# -bibtex book
	# pdflatex -shell-escape  book
	# pdflatex  -shell-escape book
	cp $@ ../../output 

#########################

chapter: slides slides169 handout 

slides: $(slidesPdf) 
	make -C figures
	make $<

handout: $(handoutPdf)
	make -C figures
	make $<

slides169: $(slides169Pdf) 
	make -C figures
	make $<

%-slides.tex: %-slides.org %.org ../slidehead.org 
	echo "building beamer tex file", $<, $@
	${EMACS} -Q --batch $<  -eval ${EMACSEXPORTPROG}


%-slides.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	pdflatex  -shell-escape "\\def\\OutputStyle{presentation}\\input{$<}"
	pdflatex  -shell-escape "\\def\\OutputStyle{presentation}\\input{$<}"
	bibtex $(basename $<)
	pdflatex  -shell-escape "\\def\\OutputStyle{presentation}\\input{$<}"
	cp $@ ../../output/slides/


%-handout.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	pdflatex  -jobname $(patsubst %-slides.tex,%-handout,$<) -shell-escape "\\def\\OutputStyle{handout}\\input{$<}"
	pdflatex  -jobname $(patsubst %-slides.tex,%-handout,$<) -shell-escape "\\def\\OutputStyle{handout}\\input{$<}"
	bibtex $(basename $<)
	pdflatex  -jobname $(patsubst %-slides.tex,%-handout,$<) -shell-escape "\\def\\OutputStyle{handout}\\input{$<}"
	cp $@ ../../output/handout/

%-slides169.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	pdflatex  -jobname $(patsubst %-slides.tex,%-slides169,$<) -shell-escape "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	pdflatex  -jobname $(patsubst %-slides.tex,%-slides169,$<) -shell-escape "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	bibtex $(basename $<)
	pdflatex  -jobname $(patsubst %-slides.tex,%-slides169,$<) -shell-escape "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	cp $@ ../../output/slides169/



##########################

clean:
	-rm *.tex *.tex~ tmp.org *.pdf *.bbl *.vrb
	-rm -rf _minted*
	-rm *.aux *.log *.nav *.out *.snm *.toc 

cleanall:
	-cd book ; rm *.pdf *.aux *.log *.bbl *.tex *.tex~ *.toc *.aux *.bbl *.log *.blg *.out *.vrb
	for d in ch*; do make -C $$d clean  ; done
