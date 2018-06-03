

.PHONY: build clean

SOURCE := $(wildcard *.tex)
PICS := $(patsubst %.tex,%.pdf,$(wildcard *.tex))

build: $(PICS)

$(PICS): %.pdf: %.tex
	pdflatex -shell-escape $< 

clean:
	-rm *aux *log
