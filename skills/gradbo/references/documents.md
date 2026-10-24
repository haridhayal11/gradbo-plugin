# Documents: tailor, build and check

`<skill>` below is this skill's directory. Every command runs from the application folder.

## The script

`<skill>/scripts/docs.py` builds and checks documents on Windows, macOS and Linux. Run it in whichever of these ways works:

```sh
uv run <skill>/scripts/docs.py <command> ...      # installs its dependencies on first use
python <skill>/scripts/docs.py <command> ...      # after: python -m pip install python-docx pypdfium2 pillow
```

On Windows use `py` or `python`, whichever exists. If neither Python nor uv is installed, ask the candidate to install uv (https://docs.astral.sh/uv/); until then, send their CV unchanged.

| Command | Does |
|---|---|
| `check FILE [--one-page]` | `.tex` (compiled with Tectonic), `.pdf` or `.docx`. Extracts the text to `<name>.txt`, renders every page to `render/`, and prints pages, size, word count and SHA-256. Fails on almost no text, ligature characters, or a `--one-page` document that runs over |
| `compare BASE TAILORED [--allow FILE] [--allow-term TEXT]` | Lists names, numbers and terms the tailored CV has that the base never mentions, and base lines it dropped. Fails if anything was added. Terms in an `--allow` file and each `--allow-term` count as known |
| `text FILE` | Prints a document's text |
| `docx-dump FILE` | Lists a Word document's paragraphs as JSON, numbered |
| `docx-edit FILE EDITS.json OUT` | Applies `set`, `move` and `delete` edits to those numbered paragraphs, keeping the formatting |
| `letter TEXT OUT.docx` | A plain one-page A4 cover letter in Word format from a text file |

## Which CV the candidate has

`profile/cv/` holds one of three things:

- **`main.tex` (LaTeX).** Tailor a copy of the source; build and check it with Tectonic.
- **`main.docx` (Word).** Tailor a copy paragraph by paragraph with `docx-dump` and `docx-edit`; upload the `.docx`.
- **Only `main.pdf`.** It can't be edited reliably, so send it unchanged and say so in the receipt. Ask the candidate once whether they have the Word or LaTeX source; it lets you tailor future applications.

## Tailoring rules

The same for every format:

- Rewrite the profile, summary or "about" section for this role. Lead with what the advert asks for most, and the candidate's evidence for it: the degree, projects and experience that match, in the advert's terms where their own wording supports them. It may name the role and the employer. It claims nothing the rest of the CV and `profile/facts.md` don't already say. A CV without such a section doesn't gain one.
- Reorder sections, entries and bullet points so the advert's priorities come first. Experience stays in date order.
- Reword a point toward the advert's terms only where the candidate's own wording already supports it ("built test benches in SystemVerilog" may become "built SystemVerilog verification test benches"; it may not gain "UVM" unless the CV says UVM elsewhere).
- Add nothing that isn't in the CV or `profile/facts.md`: no skills, tools, numbers, employers, grades or outcomes.
- Cut only what is irrelevant to this role, never dates or employers.
- Run the reworded text through the `humanizer` skill.

### LaTeX

1. Copy `profile/cv/main.tex` to `main.tex` in the application folder and edit the copy.
2. `docs.py check main.tex`.
3. `docs.py compare ../../profile/cv/main.tex main.tex --allow ../../profile/facts.md --allow-term "<Employer>" --allow-term "<Role title>"`, with the employer and title as `job.md` gives them.

Tectonic must be installed (https://tectonic-typesetting.github.io). Without it, use `profile/cv/main.pdf` unchanged.

### Word

1. `docs.py docx-dump ../../profile/cv/main.docx > cv-paragraphs.json` and read it.
2. Write `cv-edits.json`, for example:

   ```json
   [{"op": "set", "i": 12, "text": "Built SystemVerilog verification test benches for an AXI interconnect."},
    {"op": "move", "i": 15, "before": 12},
    {"op": "delete", "i": 20}]
   ```

   The numbers are from the dump of the base file. `set` keeps the paragraph's formatting: leading runs whose text is unchanged (a bold "Label:") stay as they are, and the new text takes the next run's style. A `move` must stay within one section or table cell.
3. `docs.py docx-edit ../../profile/cv/main.docx cv-edits.json <Name>_CV.docx`
4. `docs.py check <Name>_CV.docx`. With LibreOffice or Word installed, the pages are rendered too; without them, say in the receipt that the layout was not checked by eye.
5. `docs.py compare ../../profile/cv/main.docx <Name>_CV.docx --allow ../../profile/facts.md --allow-term "<Employer>" --allow-term "<Role title>"`.

## Cover letters

Write the text first: the candidate's name, contact line, then 3-4 short paragraphs following [templates/cover-letter.tex](../templates/cover-letter.tex)'s outline. Every claim must come from the facts, the CV or the advert. Then run it through the `humanizer` skill.

The letter's job is to say why this role, at this employer:

- Open with the role and why it, not a summary of the CV. Name what the advert says the role does (the programme, the team, the products or the problems it works on) and connect it to the candidate's own interests and target areas in `profile/facts.md` (`motivation.*`), and to `answers/employers/<slug>.md` if they gave a reason for this employer.
- Be specific to this advert: a sentence that would fit any employer's letter is cut or rewritten with the advert's own details.
- Never invent a motivation, a visit, a conversation or a long-held interest. If `motivation.*` is empty, ask the candidate once what draws them to this kind of role and record the answer as a fact; until then, base the "why" on how the advert's work matches what they have done.

- **LaTeX candidates:** fill in `templates/cover-letter.tex` as `cover-letter.tex`, then `docs.py check --one-page cover-letter.tex`.
- **Everyone else:** save the text as `cover-letter.txt`, then run `docs.py letter cover-letter.txt cover-letter.docx` and `docs.py check --one-page cover-letter.docx`.

Upload the PDF when the form asks for PDF and you have one; otherwise the `.docx`.

## Pass criteria

Reject and fix a document when any of these fail:

1. `check` passes: it compiles, the text extracts, and the page count is right.
2. The extracted text reads correctly: names, dates and headings in order, no ligature characters (ﬀ ﬁ ﬂ), and no words split by stray spaces ("T eam").
3. Every rendered page is clean: nothing clipped, overlapping or running off the page, and no empty trailing page.
4. `compare` lists nothing added. Each added term must be removed, or traced to a fact in `profile/facts.md` (pass it with `--allow`). Only the employer's name and the role title may come from the advert (`--allow-term`); never allow the advert's text as a whole. Whatever was dropped was meant to be.

`compare` catches new names, numbers and tool names, not new plain words ("led", "coverage"). Reread the reworded bullets against the base yourself.

A CV can be any length; aim for one page when the content fits. A cover letter is one A4 page.

## LaTeX fonts

Tectonic is XeTeX: use `fontspec` with OpenType fonts and `Ligatures={TeX,NoCommon},Kerning=Off`, as the cover-letter template does. Never use `\usepackage[T1]{fontenc}`; under XeTeX it prints "£" as "č". If the candidate's own CV loads `fontenc`, compile it as it is and check the extracted text carefully.
