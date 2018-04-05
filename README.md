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

Produced PDFs end up in subdirectory output 

### Convenient latexmk replacement 

fswatch -o *.org figures/*.tex  | xargs  -n1 make slides
