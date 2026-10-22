# Setup: the candidate's profile

The goal is a `profile/` the rest of the skill can trust, plus search preferences on the server. Ask only for what the evidence cannot give.

## 1. The workspace

- Confirm the workspace folder with the candidate if you are not sure the current directory is meant for it.
- If they have a Gradbo export from the retired hosted applier, it already holds `profile/`, `answers/` and past `applications/`. Copy it in, read `profile/facts.md`, and continue from step 3 to fill gaps; don't redo what is verified.

## 2. The CV

- Put the canonical CV in `profile/cv/`: `main.tex` if the candidate has LaTeX source, otherwise their PDF as `main.pdf`.
- Produce `profile/cv/main.txt` with `pdftotext -layout main.pdf main.txt` (compile `main.tex` first; see [documents.md](documents.md)). If the text comes out empty or garbled, the PDF is a scan; ask for a text-based PDF or the source.
- A new CV replaces the old one: move the old files to `profile/cv/previous/YYYY-MM-DD/`, then re-check every fact whose source is the CV (step 3) and mark changed or vanished ones `stale`.

## 3. Facts

Read `main.txt` and write `profile/facts.md` in the format in [folder-layout.md](folder-layout.md). Use the keys in [question-keys.md](question-keys.md) where one fits.

- **From the CV** (status `verified`, source `cv: profile/cv/main.tex` with the quoted line): name, email, phone, links, education (institution, degree, grade or predicted grade, start and end months), experience (employer, role, dates, what they did), projects, skills.
- **From the candidate** (they are not in a CV; ask in one short batch, then record each with source `candidate: told the agent on <date>`):
  - `work.uk.right_to_work`, and when it ends (`valid until`)
  - `work.uk.requires_sponsorship`, now and in future
  - `preferences.available_from` (month and year they can start)
  - `address.city`, `address.country`, and a full address only if they want forms filled with it
  - `preferences.notice_period` if they are working
- An education end date of "Present" is not a graduation date: ask for the expected graduation month.
- Demographic and equal-opportunities answers (`demographics.*`) are optional. Ask once whether they want them answered or left as "Prefer not to say", and record whichever they choose.
- Never record passwords, codes, bank, passport or national insurance numbers.

## 4. Search preferences

The server filters and keyword-scores adverts with these; they decide what reaches the digest.

1. `get_preferences()` returns the current values and the list of role families.
2. Propose values from the profile: up to six role families in the candidate's order of preference, seniority (`internship`, `graduate`, `junior`, …), `graduation_year` for graduate schemes, `available_from` (YYYY-MM), preferred locations, `needs_sponsorship`, keywords, and employers to favour or hide. Keep `exclude_clearance` true.
3. Show the proposal and save it with `set_preferences` once the candidate agrees. Only send fields they confirmed; these are search settings, not personal facts.

## 5. Check the connection

Call `get_digest(limit=5)`. If it fails with an authentication error, the token is missing or read-only; see the end of SKILL.md.
