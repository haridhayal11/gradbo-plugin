# Setup: the candidate's profile

The goal is the candidate's CV in `profile/cv/`, their facts in Gradbo (`save_fact`), and their search preferences. Ask only for what the evidence cannot give.

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
  - **Already set up:** whenever you start in a Gradbo folder, compare its `AGENTS.md` (or its Gradbo section) with [templates/AGENTS.md](../templates/AGENTS.md). If the template has lines the folder's copy lacks, replace the Gradbo text with the template's and update `GEMINI.md` to match. Tell the candidate in one line; it doesn't need their approval.
- **The CV they named lives elsewhere** (`~/Downloads/cv.pdf`): copy it in at step 2 and leave the original where it is.
- If they have an older Gradbo folder or an export from the retired hosted applier (it holds `profile/facts.md`, `answers/` and past `applications/`), copy it in and move it into Gradbo ("Moving an older folder in", below), then continue from step 3 to fill gaps; don't redo what is verified.

## 2. The CV

- Put the canonical CV in `profile/cv/`: `main.tex` for LaTeX source, `main.docx` for Word, and their PDF as `main.pdf` either way. Ask for the Word or LaTeX source if they only sent a PDF: without it, applications can't be tailored.
- Run `docs.py check` on the source (or the PDF) from `profile/cv/` ([documents.md](documents.md)); it writes `main.txt`. If the text comes out empty or garbled, the PDF is a scan; ask for a text-based PDF or the source.
- A new CV replaces the old one: move the old files to `profile/cv/previous/YYYY-MM-DD/`, then re-check every fact whose source is the CV (`get_profile`) against the new text: save changed ones again, and `save_fact(..., status="stale")` for vanished ones.

## 3. Facts

Read `main.txt`, `get_profile()` for what Gradbo already holds, and save each new fact with `save_fact`. Use dotted keys: `identity.first_name`, `identity.last_name`, `contact.email`, `contact.phone`, `links.linkedin`, `address.city`, `education.0.school` / `.qualification` / `.subject` / `.grade` / `.start` / `.end`, `employment.0.employer` / `.title` / `.start` / `.end` / `.summary`, `projects.0.name` / `.summary`, `skills.0`.

- **From the CV** (`source="cv"`, `source_ref="profile/cv/main.txt: <the quoted line>"`): name, email, phone, links, education (institution, degree, grade or predicted grade, start and end months), experience (employer, role, dates, what they did), projects, skills.
- **From the candidate** (they are not in a CV; ask in one short batch, then save each with `source="candidate"`, `source_ref="told the agent on <date>"`):
  - `work.uk.right_to_work`, and when it ends (`valid_until`)
  - `work.uk.requires_sponsorship`, now and in future
  - `preferences.available_from` (month and year they can start)
  - `address.city`, `address.country`, and a full address only if they want forms filled with it
  - `preferences.notice_period` if they are working
  - `motivation.target_areas` and `motivation.what_they_want`: the kinds of role they want and what they want from one, in their own words. Cover letters and "why this role" answers build on these; without them the letters can only say how the advert matches their record.
- An education end date of "Present" is not a graduation date: ask for the expected graduation month.
- Equal-opportunities answers: ask once whether they want them answered from their details or left as "Prefer not to say", and save it as `demographics.choice` (`answer from facts` or `prefer not to say`). If they choose to answer, Gradbo keeps those answers only with their consent: ask them to tick it in Settings > Your data in the dashboard (you can't), then save the `demographics.*` answers they give. Forms never ask them again ([questions.md](questions.md)).
- Never save passwords, codes, bank, passport or national insurance numbers.

## 4. Email

Ask how you may read their email for verification codes and employers' replies: a mail connector in this agent, the IMAP script with an app password they set in their environment, or not at all (they read codes out). Save it as the fact `workspace.mail_access`. See [email.md](email.md).

## 5. Search preferences

The server filters and keyword-scores adverts with these; they decide what reaches the digest.

1. `get_preferences()` returns the current values and the list of role families.
2. Propose values from the profile: up to six role families in the candidate's order of preference, seniority (`internship`, `graduate`, `junior`, …), `graduation_year` for graduate schemes, `available_from` (YYYY-MM), preferred locations, keywords, and employers to favour or hide. Keep `exclude_clearance` true. Set `needs_sponsorship` from the `work.uk.requires_sponsorship` fact (true if they need sponsorship now or in future), never from the default; with it false, adverts that refuse sponsorship are kept.
3. Show the proposal and save it with `set_preferences` once the candidate agrees. Only send fields they confirmed; these are search settings, not personal facts.

## Moving an older folder in

Before 2026-10-24 the skill kept facts and answers in the folder. When a folder still has `profile/facts.md`, `answers/` or receipts:

1. Read them and call `import_workspace(facts_md=<profile/facts.md as it is>, answers=[{"path": "answers/...md", "text": ...} for every answer file, employer files included], receipts=[{"path": ..., "json": <receipt.json>, "job_id": <its Gradbo job id>} for each application folder with a receipt.json])`.
2. Check the result: `stored` counts, and `skipped`. Equal-opportunities answers are skipped until the candidate allows Gradbo to keep them (Settings > Your data); import again afterwards. Fix or ask about anything else skipped.
3. Move `profile/facts.md` and `answers/` into `profile/imported-YYYY-MM-DD/` (don't delete them), and tell the candidate in one line that Gradbo now remembers these and they may delete the copy. Leave old application folders as they are.

## 6. First roles

Call `get_digest(limit=5)` and tell the candidate setup is done: what is in their profile, what is still missing, and how many new roles are waiting. Offer to triage them now ([find.md](find.md)).
