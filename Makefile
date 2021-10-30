all: gensty gendoc

gensty:
	python -m bin.gensty

gendoc:
	cd docs \
		&& latexmk -pdflatex -halt-on-error -interaction=batchmode -shell-escape -output-directory="../build" manual.tex \
		&& mv ../build/manual.pdf .. \
		&& latexmk -C manual.tex
