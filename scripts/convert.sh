#!/bin/bash

for f in *.pdf
do
    pdf2txt.py -o "${$f%.*}.html" $f
done
