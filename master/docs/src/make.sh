/usr/texbin/pdflatex -synctex=1 -interaction=nonstopmode document.tex
/usr/texbin/pdflatex -synctex=1 -interaction=nonstopmode document.tex
/usr/texbin/bibtex bibliography
makeindex document.nlo -s nomencl.ist -o document.nls
/usr/texbin/pdflatex -synctex=1 -interaction=nonstopmode document.tex
/usr/texbin/pdflatex -synctex=1 -interaction=nonstopmode document.tex
/usr/texbin/pdflatex -synctex=1 -interaction=nonstopmode document.tex
