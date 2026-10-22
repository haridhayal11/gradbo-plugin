#!/usr/bin/env sh
# Compile a LaTeX document and run the checks a document must pass before it is sent.
# Usage: check_pdf.sh [--one-page] path/to/main.tex
# Writes <name>.pdf, <name>.txt and render/<name>-page-<n>.png (every page) next to the source.
# Exits non-zero when compilation, text extraction or the page limit fails;
# the rendered pages still need looking at for clipping, overlap and overflow.
set -eu
one_page=0
if [ "${1:-}" = "--one-page" ]; then one_page=1; shift; fi
src="${1:?usage: check_pdf.sh [--one-page] file.tex}"
for tool in tectonic pdftotext pdftoppm pdfinfo; do
  command -v "$tool" >/dev/null 2>&1 || { echo "missing tool: $tool" >&2; exit 2; }
done
dir=$(dirname "$src"); name=$(basename "$src" .tex)
cd "$dir"
tectonic --keep-logs "$name.tex" >/dev/null 2>"$name.compile.err" || { echo "compile failed; see $dir/$name.log" >&2; tail -20 "$name.compile.err" >&2; exit 1; }
rm -f "$name.compile.err"
pdftotext -layout "$name.pdf" "$name.txt"
mkdir -p render
rm -f render/"$name"-page-*.png
pdftoppm -png -r 150 "$name.pdf" "render/$name-page"
pages=$(pdfinfo "$name.pdf" | awk '/^Pages:/ {print $2}')
size=$(pdfinfo "$name.pdf" | sed -n 's/^Page size: *//p')
words=$(wc -w < "$name.txt" | tr -d ' ')
echo "pdf: $dir/$name.pdf"
echo "pages: $pages"
echo "page size: $size"
echo "extracted words: $words"
echo "render: $(ls render/"$name"-page-*.png | sed "s|^|$dir/|" | tr '\n' ' ')"
echo "sha256: $(sha256sum "$name.pdf" | cut -d' ' -f1)"
status=0
[ "$words" -ge 30 ] || { echo "FAIL: almost no text extracted" >&2; status=1; }
if grep -q 'ﬀ\|ﬁ\|ﬂ\|ﬃ\|ﬄ' "$name.txt"; then echo "FAIL: ligature characters in the text (ﬀ ﬁ ﬂ); turn ligatures off" >&2; status=1; fi
case "$size" in *A4*) ;; *) echo "WARN: page size is not A4" >&2 ;; esac
if [ "$one_page" = 1 ] && [ "$pages" != 1 ]; then echo "FAIL: $pages pages; a cover letter must fit on one A4 page" >&2; status=1; fi
exit $status
