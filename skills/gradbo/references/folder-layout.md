# The Gradbo folder

One folder holds everything for the candidate's job search: `~/Gradbo` by default (`%USERPROFILE%\Gradbo` on Windows), or the folder they chose. Always start the agent there.

```
Gradbo/
  AGENTS.md                     what this folder is, for any agent started here (templates/AGENTS.md)
  CLAUDE.md, GEMINI.md          the same, for Claude Code and Gemini CLI
  .agents/skills/ or .claude/   the gradbo and humanizer skills when installed for this folder only
  .mcp.json                     Claude Code's project-level tools (the browser), if added here
  profile/
    facts.md                    verified facts, one section per key
    cv/
      main.tex | main.docx      the canonical CV source, LaTeX or Word (absent if they only have a PDF)
      main.pdf                  the compiled or original PDF
      main.txt                  its extracted text (docs.py check writes it)
  answers/
    <question-key>.md           reusable answers to recurring questions
    employers/<employer-slug>.md  answers and dropdown choices that belong to one employer
  applications/
    YYYY-MM-DD_employer_role/   one folder per application (see below)
    mail-check.md               the date replies were last checked (email.md)
```

Create folders as you need them. Never edit the CV in `profile/cv/` for one application; tailor a copy in the application folder. Never put job-search files anywhere outside the Gradbo folder, and never move the candidate's other files into it without asking.

## Names

- Application folders are `YYYY-MM-DD_employer_role`, lowercase and hyphenated within each part, for example `applications/2026-09-18_edf_data-technology/`. The date is the day you start the application. Use Gradbo's employer slug when you have it.
- Answer files are named after the canonical key in [question-keys.md](question-keys.md) (`answers/motivation.why_employer.md`). When no key fits, use a short hyphenated slug of the question (`answers/how-did-you-hear-about-us.md`).
- Employer files use Gradbo's employer slug (`answers/employers/arm.md`).

## `profile/facts.md`

A heading line, then one section per fact, in this exact shape (the Gradbo export writes the same):

```markdown
# Candidate facts

## work.uk.right_to_work

Do you currently have the right to work in the UK?

Yes

- status: verified, checked 2026-10-22
- valid until: 2029-01-31
- source: candidate: told the agent on 2026-10-22
```

- `## <key>`: the canonical key from [question-keys.md](question-keys.md), or a new lowercase dotted key (`education.0.grade`, `skills.cad.revit`).
- The next paragraph is a plain label; the paragraph after it is the value, which may span several lines.
- `status` is `verified` (from the CV, the candidate or another source quoted below it), `needs_review` (found but not yet confirmed) or `stale` (out of date). Only `verified` facts may be used in an application. Add `checked YYYY-MM-DD` whenever you verify it.
- `valid until` (optional) is the date after which the fact is stale, such as a visa's expiry. `confirmed for start month: YYYY-MM` (optional) records which start month a future-eligibility answer was confirmed for.
- `source` is `cv`, `candidate` or `application`, a colon, and a reference: a file path, `told the agent on <date>`, or an application folder. A quote may follow on lines starting `  > `.

Never store passwords, one-time codes, bank details, national insurance or passport numbers, or identity-document scans as facts.

## `answers/<key>.md`

```markdown
## motivation.why_employer

**Question:** Why do you want to work for us?

<the answer text>

- status: draft, origin: assisted
- uses facts: education.0.degree, experience.1.role
- source: application: applications/2026-10-22_arm_graduate-engineer
```

- `status` is `candidate_approved` (written or confirmed by the candidate), `draft` (written by you from verified evidence) or `stale` (a fact it uses has changed).
- `origin` is `candidate` or `assisted`.
- An answer that only makes sense for one employer goes in `answers/employers/<slug>.md`, each block preceded by `<!-- scope: employer:<slug> -->`. Use `<!-- scope: job:<gradbo job id> -->` for one role.

## Application folder

```
applications/YYYY-MM-DD_employer_role/
  job.md                  the role: links, Gradbo job id, closing date, live-advert check, eligibility notes, AI guidance
  main.tex main.pdf | <Name>_CV.docx   the tailored CV (LaTeX or Word), with main.txt / render/ from its checks
  cover-letter.tex | cover-letter.txt + cover-letter.docx, and their PDF when built   when one is sent
  application-notes.md    the form as you work through it: fields, answers, open questions, where you stopped
  manual-handoff.md       only when a human has to take over (templates/manual-handoff.md)
  receipt.md receipt.json the exact submission (templates/receipt.md, templates/receipt.json)
```

Older folders may hold other files, such as `cover-letter.md`, `document-checks.json` or `page-1.png`; leave them as they are.
