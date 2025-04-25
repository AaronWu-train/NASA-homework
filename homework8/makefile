TEXFILE = hw8.tex
PDF = hw8.pdf

-include ../.env
STUDENT_ID ?= unknown
ARCHIVE_DIR = $(STUDENT_ID)
ARCHIVE = $(STUDENT_ID).zip
FILE_TO_ARCHIVE = $(PDF)
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
	cp $(FILE_TO_ARCHIVE) $(DIST_DIR)/$(ARCHIVE_DIR)/report.pdf
	cp -r ldif/ $(DIST_DIR)/$(ARCHIVE_DIR)/ldif/

clean:
	rm -f ./*.aux ./*.log ./*.bbl ./*.blg ./*.toc ./*.out ./*.lof ./*.lot ./*fls ./*.fdb_latexmk ./*.synctex.gz
	rm -rf _minted

distclean: clean
	rm -f $(PDF)
	rm -rf $(DIST_DIR) $(ARCHIVE)

.PHONY: all clean