.PHONY: test numbers paper

test:
	python3 -m unittest discover -s tests -t .

numbers:
	python3 -m analysis.paper_numbers

paper: numbers
	cd paper && pdflatex -interaction=nonstopmode pester.tex && pdflatex -interaction=nonstopmode pester.tex
