# The Gradbo folder

One folder holds the candidate's documents for their job search: `~/Gradbo` by default (`%USERPROFILE%\Gradbo` on Windows), or the folder they chose. Always start the agent there. Everything else (their facts, reusable answers, each application's brief, progress and receipt) is kept by Gradbo and reached through the memory tools; it is never written to this folder.

```
Gradbo/
  AGENTS.md                     what this folder is, for any agent started here (templates/AGENTS.md)
  AUTHORISATION.md              the candidate's standing authorisation, in their words with their name and date (templates/AUTHORISATION.md); never rewritten
  CLAUDE.md, GEMINI.md          the same as AGENTS.md (CLAUDE.md imports AGENTS.md and AUTHORISATION.md), for Claude Code and Gemini CLI
  .agents/skills/ or .claude/   the gradbo and humanizer skills when installed for this folder only
  .mcp.json                     Claude Code's project-level tools (the browser), if added here
  profile/
    cv/
      main.tex | main.docx      the canonical CV source, LaTeX or Word (absent if they only have a PDF)
      main.pdf                  the compiled or original PDF
      main.txt                  its extracted text (docs.py check writes it)
      previous/YYYY-MM-DD/      an earlier CV, kept when a new one replaces it
    imported-YYYY-MM-DD/        an older folder's facts.md and answers/, after they were moved into Gradbo
  applications/
    YYYY-MM-DD_employer_role/   one folder per application (see below)
    mail-check.md               the date replies were last checked (email.md)
```

Create folders as you need them. Never edit the CV in `profile/cv/` for one application; tailor a copy in the application folder. Never put job-search files anywhere outside the Gradbo folder, and never move the candidate's other files into it without asking.

## Names

- Application folders are `YYYY-MM-DD_employer_role`, lowercase and hyphenated within each part, at the top of `applications/`, for example `applications/2026-09-18_edf_data-technology/`. The date is the day you start the application. Use Gradbo's employer slug when you have it.
- Fact and answer keys are lowercase dotted names (`work.uk.right_to_work`, `education.0.grade`, `motivation.why_employer`, `custom.non_compete_agreement`). `answer_questions` names the key for every question it recognises; use the same key for what you save.

## Application folder

```
applications/YYYY-MM-DD_employer_role/
  main.tex main.pdf | <Name>_CV.docx   the tailored CV (LaTeX or Word), with main.txt / render/ from its checks
  cover-letter.tex | cover-letter.txt + cover-letter.docx, and their PDF when built   when one is sent
  manual-handoff.md       only when a human has to take over (templates/manual-handoff.md)
```

The role's brief, the form's progress and the receipt are in Gradbo (`get_application(job_id)`). Older folders may hold `job.md`, `application-notes.md`, `receipt.md`, `receipt.json` or other files from before; leave them as they are once their receipt is in Gradbo.
