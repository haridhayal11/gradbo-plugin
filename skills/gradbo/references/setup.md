# Setup: the candidate's profile

The goal is a `profile/` the rest of the skill can trust, plus search preferences on the server. Ask only for what the evidence cannot give.

## 0. Preflight

Run [install.md](install.md) first: check the Gradbo connection, this machine (`scripts/doctor.py`), the browser tool and mail, and give the candidate one checklist. A missing optional item never blocks setup; a missing Gradbo connection does.

## 1. The Gradbo folder

Everything lives in one folder ([folder-layout.md](folder-layout.md)).

- **Started in a folder named `Gradbo`, an empty folder, or one holding only agent configuration** (`.agents/`, `.claude/`, `.mcp.json`, `.git/` and the like, which the install commands create): that is the folder. Confirm it with the candidate in one line.
- **Started somewhere else** (their home directory, a code project, Downloads): don't set up there. If `~/Gradbo` exists, ask them to restart you in it. Otherwise offer to create `~/Gradbo`, then ask them to restart you there (`cd ~/Gradbo`, then start the agent). Agents usually can't write outside the folder they were started in, and the skills and instructions installed for that folder only load there.
- **Mark the folder:**
  - Write `AGENTS.md` from [templates/AGENTS.md](../templates/AGENTS.md).
  - Write `CLAUDE.md` with the single line `@AGENTS.md`.
  - Write `GEMINI.md` with the same text as `AGENTS.md`.
  - If any of these files already exists, add a "Gradbo job-search workspace" section instead of replacing it.
- **The CV they named lives elsewhere** (`~/Downloads/cv.pdf`): copy it in at step 2 and leave the original where it is.
- If they have a Gradbo export from the retired hosted applier, it already holds `profile/`, `answers/` and past `applications/`. Copy it in, read `profile/facts.md`, and continue from step 3 to fill gaps; don't redo what is verified.

## 2. The CV

- Put the canonical CV in `profile/cv/`: `main.tex` for LaTeX source, `main.docx` for Word, and their PDF as `main.pdf` either way. Ask for the Word or LaTeX source if they only sent a PDF: without it, applications can't be tailored.
- Run `docs.py check` on the source (or the PDF) from `profile/cv/` ([documents.md](documents.md)); it writes `main.txt`. If the text comes out empty or garbled, the PDF is a scan; ask for a text-based PDF or the source.
- A new CV replaces the old one: move the old files to `profile/cv/previous/YYYY-MM-DD/`, then re-check every fact whose source is the CV (step 3) and mark changed or vanished ones `stale`.

## 3. Facts

Read `main.txt` and write `profile/facts.md` in the format in [folder-layout.md](folder-layout.md). Use the keys in [question-keys.md](question-keys.md) where one fits.

- **From the CV** (status `verified`, source `cv: profile/cv/main.txt` with the quoted line): name, email, phone, links, education (institution, degree, grade or predicted grade, start and end months), experience (employer, role, dates, what they did), projects, skills.
- **From the candidate** (they are not in a CV; ask in one short batch, then record each with source `candidate: told the agent on <date>`):
  - `work.uk.right_to_work`, and when it ends (`valid until`)
  - `work.uk.requires_sponsorship`, now and in future
  - `preferences.available_from` (month and year they can start)
  - `address.city`, `address.country`, and a full address only if they want forms filled with it
  - `preferences.notice_period` if they are working
- An education end date of "Present" is not a graduation date: ask for the expected graduation month.
- Demographic and equal-opportunities answers (`demographics.*`) are optional. Ask once whether they want them answered or left as "Prefer not to say", and record whichever they choose.
- Never record passwords, codes, bank, passport or national insurance numbers.

## 4. Email

Ask how you may read their email for verification codes and employers' replies: a mail connector in this agent, the IMAP script with an app password they set in their environment, or not at all (they read codes out). Record it as `workspace.mail_access`. See [email.md](email.md).

## 5. Search preferences

The server filters and keyword-scores adverts with these; they decide what reaches the digest.

1. `get_preferences()` returns the current values and the list of role families.
2. Propose values from the profile: up to six role families in the candidate's order of preference, seniority (`internship`, `graduate`, `junior`, …), `graduation_year` for graduate schemes, `available_from` (YYYY-MM), preferred locations, `needs_sponsorship`, keywords, and employers to favour or hide. Keep `exclude_clearance` true.
3. Show the proposal and save it with `set_preferences` once the candidate agrees. Only send fields they confirmed; these are search settings, not personal facts.

## 6. First roles

Call `get_digest(limit=5)` and tell the candidate setup is done: what is in their profile, what is still missing, and how many new roles are waiting. Offer to triage them now ([find.md](find.md)).
