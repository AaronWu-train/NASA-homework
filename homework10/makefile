TEXFILE = hw10.tex
PDF = hw10.pdf

-include ../.env
STUDENT_ID ?= unknown
ARCHIVE_DIR = $(STUDENT_ID)
ARCHIVE = $(STUDENT_ID).zip
FILES_TO_ARCHIVE = $(PDF)
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
	cp $(FILES_TO_ARCHIVE) $(DIST_DIR)/$(ARCHIVE_DIR)/$(STUDENT_ID).pdf
	cp hostapd.conf $(DIST_DIR)/$(ARCHIVE_DIR)/$(STUDENT_ID).conf
	cp images/c-5.png $(DIST_DIR)/$(ARCHIVE_DIR)/$(STUDENT_ID).png
	

clean:
	rm -f ./*.aux ./*.log ./*.bbl ./*.blg ./*.toc ./*.out ./*.lof ./*.lot ./*fls ./*.fdb_latexmk ./*.synctex.gz
	rm -rf _minted

distclean: clean
	rm -f $(PDF)
	rm -rf $(DIST_DIR) $(ARCHIVE)

.PHONY: all clean