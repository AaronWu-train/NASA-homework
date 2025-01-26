TEXFILE = *.tex
PDF = $(TEXFILE:.tex=.pdf)

all: $(PDF)

$(PDF): $(TEXFILE)
	rm -f $(PDF)
	xelatex -shell-escape $(TEXFILE)
	xelatex -shell-escape $(TEXFILE)

clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out *.lof *.lot *fls *.fdb_latexmk *.synctex.gz
	rm -rf _minted

distclean: clean
	rm -f $(PDF)

.PHONY: all clean