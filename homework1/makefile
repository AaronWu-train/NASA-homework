TEXFILE = *.tex
PDF = $(TEXFILE:.tex=.pdf)

-include .env
STUDENT_ID ?= unknown
ARCHIVE_DIR = $(STUDENT_ID)
ARCHIVE = $(STUDENT_ID).zip
FILES_TO_ARCHIVE = report.pdf merkle-dir.sh
DIST_DIR = dist

all: $(PDF)

$(PDF): $(TEXFILE)
	rm -f $(PDF)
	xelatex -shell-escape $(TEXFILE)
	xelatex -shell-escape $(TEXFILE)

archive: prepare_dist
	cd $(DIST_DIR) && zip -r $(ARCHIVE) $(ARCHIVE_DIR)

prepare_dist:
	@mkdir -p $(DIST_DIR)/$(ARCHIVE_DIR)
	@for file in $(FILES_TO_ARCHIVE); do \
	    cp $$file $(DIST_DIR)/$(ARCHIVE_DIR); \
	done	

clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out *.lof *.lot *fls *.fdb_latexmk *.synctex.gz
	rm -rf _minted
	rm -rf $(DIST_DIR) $(ARCHIVE)

distclean: clean
	rm -f $(PDF)

.PHONY: all clean