# DistributedSystems

## Content 

Lecture material (slides, script) for a distributed systems Bachelor
class. The intention is to update standard material with material on
new developments in cloud systems, big data processing,
etc. Concepts (like vector clocks, distributed algorithms, distributed
transactions) will be introduced using concrete use cases. Heavy
emphasis on case studies. 

The target audience is a third-year Computer Science Bachelor class,
with 6 LP/ECTS. Subsets shold be easily useable for a shorter (e.g., 4
ECTS class). 

## Material, preparation 

Material will be produced using emacs org mode, from which LaTeX
Beamer files will be generated. These can be turned into slides as
well as handout scripts. 

You need emacs and and org-mode v9 or better. Adapt path name for the
emacs executable in Makefile. 


### Files to touch 

- In each chXX subdirectory, you need to update the chapter title in
  chXX-slides.org. The actual content - without any header markup -
  goes into chXX.org. Slides are at level 3. 
  
- In book/book.org, include the various files, add \part and \chapter
  commands. 

- slidehead.org has formatting setup for the slide decks. Usually, no
  need to touch this file. 

- subdirectories need symbolic links to the main Makefile 

### Produced files 

Produced PDFs end up in subdirectory output. One version of the PDFs
is available in Dropbox:
https://www.dropbox.com/sh/ts47xz5vgiua4l6/AAC-8XZVs3xP0A5--sBslN9na?dl=0 

### Convenient latexmk replacement 

fswatch -o *.org figures/*.tex  | xargs  -n1 make slides


## TODO 

### Continuous intgration 

If somebody feels like setting up a continous integration toolchain on
TravisCI, I'd be oblighed. It would need a fairly new TexLive, emacs,
orgmode9 current version, and dropbox uploader. See here for
inspiration: https://github.com/harshjv/travis-ci-latex-pdf
