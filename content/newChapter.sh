#!/bin/bash

mkdir $1
touch $1/$1.org

echo "#+TITLE: $2" > $1/$1-slides.org
echo -e "#+include: \"../slidehead.org\"\n\n\\\\begin{frame}\n\\\\titlepage\n\\end{frame}\n\n" >> $1/$1-slides.org
echo "#+include: \"./$1.org\"" >> $1/$1-slides.org

ln -s ../Makefile $1/Makefile 

echo "** $2"
echo " "
echo "#+include: \"../$1/$1.org\"" 

aquamacs $1/$1.org

