all: gensty gendoc

gensty:
	python -m bin.gensty

gendoc:
	cd docs \
		&& latexmk -pdflatex -halt-on-error -interaction=batchmode -shell-escape manual.tex \
		&& mv manual.pdf .. \
		&& latexmk -C manual.tex
