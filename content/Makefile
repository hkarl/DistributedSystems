.PHONY: chapters chapter all slides slides169 handout clean book bookpdf cleanall figures

# on Holger's Mac: 
EMACS="/Applications/Aquamacs 2.app/Contents/MacOS/Aquamacs"

EMACSEXPORTPROG="(progn (add-to-list 'load-path (expand-file-name \"~/.emacs.d/org-mode/lisp\")) (require 'org)  (setq org-latex-listings 'minted) (setq org-latex-minted-options '((\"frame\" \"lines\") (\"linenos=false\") (\"mathescape\" \"true\") (\"breaklines\") (\"autogobble\") (\"escapeinside\" \"??\") )) (org-beamer-export-to-latex))"

# pdflatex command
PDFLATEX=pdflatex -shell-escape -interaction=nonstopmode


SOURCE := $(wildcard *-slides.org)
slidesTex := $(patsubst %.org,%.tex,$(SOURCE))
slidesPdf := $(patsubst %.org,%.pdf,$(SOURCE))
slides169Pdf := $(patsubst %.org,%169.pdf,$(SOURCE))
handoutPdf := $(patsubst %-slides.org,%-handout.pdf,$(SOURCE))
bookTex := $(patsubst %.org,%-chapter.tex,$(wildcard *.org))

all: chapters book

chapters:
	for d in ch*; do make -C $$d chapter  ; done

#########################

book:
	make -C book clean
	make -C book book.pdf 

book.tex: book.org  
	echo "making book.tex"
	echo "building beamer tex file", $<, $@
	${EMACS} -Q --batch $<  -eval ${EMACSEXPORTPROG}
	grep -v "begin{LaTeX}" $@ | grep -v "end{LaTeX}" | sponge $@


book.pdf: book.tex
	${PDFLATEX} book
	-bibtex book
	${PDFLATEX} book
	${PDFLATEX} book
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
	grep -v "begin{LaTeX}" $@ | grep -v "end{LaTeX}" | sponge $@


%-slides.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
	# ${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
	# bibtex $(basename $<)
	# ${PDFLATEX} "\\def\\OutputStyle{presentation}\\input{$<}"
	# cp $@ ../../output/slides/

%-handout.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	bibtex $(basename $<)
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-handout,$<) "\\def\\OutputStyle{handout}\\input{$<}"
	cp $@ ../../output/handout/

%-slides169.pdf: %-slides.tex $(wildcard figures/*.pdf) ../bib.bib 
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	bibtex $(basename $<)
	${PDFLATEX}  -jobname $(patsubst %-slides.tex,%-slides169,$<) "\\def\\OutputStyle{presentation,aspectratio=169}\\input{$<}"
	cp $@ ../../output/slides169/



##########################

clean:
	-rm *.tex *.tex~ tmp.org *.pdf *.bbl *.vrb
	-rm -rf _minted*
	-rm *.aux *.log *.nav *.out *.snm *.toc 

cleanall:
	-cd book ; rm *.pdf *.aux *.log *.bbl *.tex *.tex~ *.toc *.aux *.bbl *.log *.blg *.out *.vrb
	for d in ch*; do make -C $$d clean  ; done
