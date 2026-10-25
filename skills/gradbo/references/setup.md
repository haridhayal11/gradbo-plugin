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
  - Write `CLAUDE.md` with two lines, `@AGENTS.md` and `@AUTHORISATION.md`.
  - Write `GEMINI.md` with the same text as `AGENTS.md`.
  - If any of these files already exists, add a "Gradbo job-search workspace" section instead of replacing it.
  - **Already set up:** whenever you start in a Gradbo folder, compare its `AGENTS.md` (or its Gradbo section) with [templates/AGENTS.md](../templates/AGENTS.md). If the template has lines the folder's copy lacks, replace the Gradbo text with the template's and update `GEMINI.md` to match. Make sure `CLAUDE.md` has both lines. Tell the candidate in one line; it doesn't need their approval. Never rewrite `AUTHORISATION.md`: it is the candidate's.
- **The standing authorisation** ("Standing authorisation", below): if the folder has no `AUTHORISATION.md`, set it up now.
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

Check `mail_status()`. If their inbox isn't connected, suggest they connect it in Settings > Your data in the dashboard (an app password for Gmail, iCloud or Yahoo; you can't do it for them, and never ask for the password): then codes, confirmation links and replies work from any agent. If they'd rather not, or use Outlook or Microsoft 365, use a mail connector in this agent, or the IMAP script with an app password in their environment, or have them read codes out. See [email.md](email.md).

## 5. Search preferences

The server filters and keyword-scores adverts with these; they decide what reaches the digest.

1. `get_preferences()` returns the current values and the list of role families.
2. Propose values from the profile: up to six role families in the candidate's order of preference, seniority (`internship`, `graduate`, `junior`, …), `graduation_year` for graduate schemes, `available_from` (YYYY-MM), preferred locations, keywords, and employers to favour or hide. Keep `exclude_clearance` true. Set `needs_sponsorship` from the `work.uk.requires_sponsorship` fact (true if they need sponsorship now or in future), never from the default; with it false, adverts that refuse sponsorship are kept.
3. Show the proposal and save it with `set_preferences` once the candidate agrees. Only send fields they confirmed; these are search settings, not personal facts.

## Standing authorisation

Applying for the candidate means accepting the terms, the required consents and the "information is accurate" declaration on every form. Agents' safety checks (Claude Code's auto mode in particular) block that unless the candidate's authorisation names those exact actions, so record it once:

1. Show the candidate the text of [templates/AUTHORISATION.md](../templates/AUTHORISATION.md) with their full name and today's date, and ask once: "May I accept these for you on every application, as written?" It is their authorisation to give; never assume it.
2. On yes: write it to `AUTHORISATION.md` in the Gradbo folder exactly as shown, make sure `CLAUDE.md` has the line `@AUTHORISATION.md` (and `GEMINI.md` a line pointing to it), and `save_fact("authorization.standing", "granted <YYYY-MM-DD>", source="candidate", source_ref="told the agent on <date>")`. On no: leave it; you will ask them to tick these boxes themselves on each form.
3. **Claude Code only**: auto mode also needs a rule in the candidate's own settings, since it ignores rules in project files. With their yes, add this entry to `autoMode.allow` in `~/.claude/settings.json`, keeping `"$defaults"` first in the list (create the list as `["$defaults", <entry>]` if there is none, and leave every other setting alone):

   ```
   Gradbo job applications: while applying with the gradbo skill in the candidate's own browser, ticking or accepting an employer's privacy policy, terms and conditions or applicant terms, a consent the application requires, the declaration that the information given is true, accurate and complete, and submitting the application, are allowed: the candidate granted standing authorisation in their Gradbo folder's AUTHORISATION.md. Not covered: optional or marketing consents, and statements that the application is their own unaided work or that no AI was used.
   ```

   If you can't write that file, give them the entry to paste into `/permissions` › Auto mode › Allow, or into the file themselves. `claude auto-mode config` shows it in effect. Each computer they apply from needs it once.

## Moving an older folder in

Before 2026-10-24 the skill kept facts and answers in the folder. When a folder still has `profile/facts.md`, `answers/` or receipts:

1. Check the Gradbo connection first (install.md, step 1).
2. Gather the receipts. For each folder under `applications/` with a `receipt.json` or `receipt.md`:
   - its Gradbo job id: `gradbo_job_id` inside `receipt.json` (then leave `job_id` out), else the `Gradbo job id:` line of its `job.md`, else `export_tracker()`'s application-folder column or `search_jobs(<role title>)`;
   - send `{"path": ..., "json": <receipt.json's content>}`, or `{"path": ..., "text": <receipt.md>, "job_id": ...}` when there is only a `receipt.md`. Leave out a folder whose role you can't find, and say so.
3. Call `import_workspace(facts_md=<profile/facts.md as it is>, answers=[{"path": "answers/...md", "text": ...} for every answer file, employer files included], receipts=[...])`.
4. Check the result:
   - `stored`: the counts.
   - `kept`: what Gradbo held already and kept, as the master copy: a fact whose value there was checked at least as recently as the folder's, and any answer it already had under the same key and scope. Mention them in one line.
   - `skipped`: equal-opportunities answers wait for the candidate to allow Gradbo to keep them (Settings > Your data); after they do, call `import_workspace` again with the copy in `profile/imported-YYYY-MM-DD/facts.md` (nothing newer is overwritten). Fix or ask about anything else skipped.
5. Move `profile/facts.md` and `answers/` into `profile/imported-YYYY-MM-DD/` (don't delete them), and tell the candidate in one line that Gradbo now remembers these and they may delete the copy. Leave old application folders as they are.

A candidate with more than one older folder (a laptop and a desktop, say) moves each in the same way, from that computer; for facts Gradbo keeps whichever value was checked most recently, and answers it already holds stay as they are.

## 6. First roles

Call `get_digest(limit=5)` and tell the candidate setup is done: what is in their profile, what is still missing, and how many new roles are waiting. Offer to triage them now ([find.md](find.md)).
