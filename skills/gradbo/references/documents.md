# Documents: build and check

## Tools

Run `command -v tectonic pdftotext pdftoppm pdfinfo` first.

- **Tectonic** (XeTeX; it fetches LaTeX packages on first use) compiles `.tex`.
- **Poppler** (`pdftotext`, `pdftoppm`, `pdfinfo`) extracts, renders and inspects PDFs.

If any are missing, tell the candidate what to install (`tectonic`, `poppler-utils`). Until then, send the candidate's own `profile/cv/main.pdf` unchanged, skip the cover letter unless the form requires one, and say in the receipt that documents were not tailored. Never send a PDF you could not check.

## Build

From the application folder:

```sh
<skill>/scripts/check_pdf.sh main.tex
<skill>/scripts/check_pdf.sh --one-page cover-letter.tex
```

`<skill>` is this skill's directory. The script compiles with Tectonic, extracts text with `pdftotext -layout`, renders every page to `render/` at 150 dpi, prints page count, page size, word count and the SHA-256, and fails when compilation fails, almost no text comes out, ligature characters appear in the text, or a `--one-page` document runs longer.

Without the script, the same steps by hand:

```sh
tectonic --keep-logs main.tex
pdftotext -layout main.pdf main.txt
mkdir -p render && pdftoppm -png -r 150 main.pdf render/main-page
pdfinfo main.pdf
```

## Pass criteria

Reject and fix a document when any of these fail:

1. It compiles.
2. `main.txt` reads correctly: names, dates, headings and bullet points in order, no ligature characters (ﬀ ﬁ ﬂ), no words split by stray spaces ("T eam", "A WS"), no garbage where icons sit.
3. Look at every rendered page image: nothing clipped at the margins, no overlapping text, nothing running off the page, no empty trailing page.
4. Content: everything in it is in the facts or CV, nothing important from the base CV was lost, and dates are right.

A CV can be any length; aim for one page when the content fits, and don't cut real content to get there. A cover letter is one A4 page.

## Fonts

Tectonic is XeTeX: use `fontspec` with OpenType fonts and `Ligatures={TeX,NoCommon},Kerning=Off`, as in [templates/cover-letter.tex](../templates/cover-letter.tex). Never use `\usepackage[T1]{fontenc}`; under XeTeX it prints "£" as "č". If the candidate's own CV template loads `fontenc`, compile it as it is (it is their document) and check the extracted text extra carefully.
