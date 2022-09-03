.PHONY: all dev package manual manual-dev

all: package manual

dev: package manual-dev

package:
	python -m bin package build

manual:
	python -m bin manual build --no-dev

manual-dev:
	python -m bin manual build --dev

clear:
	cd manual && latexmk -C manual.tex && rm -rf _minted_manual *.log