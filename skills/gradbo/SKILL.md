---
name: gradbo
description: Job search and applications with Gradbo. Use before any gradbo MCP tool call, and whenever the candidate wants to set up their job-search profile, find or triage roles, tailor a CV or cover letter, fill in or submit an application, answer screening questions, record an application they sent or an outcome they heard back, or check what they have applied to. Gradbo remembers the candidate's facts, answers and applications, so no question is asked twice; the local folder keeps their CV and documents.
---

# Gradbo

Gradbo has two halves:

- **The gradbo MCP server** finds roles, tracks them, and remembers the candidate. It crawls UK employers' career pages, filters the adverts by the candidate's search preferences and keeps each role's status, fit score and notes. It also keeps the candidate's memory: their facts, reusable answers, and each application's brief, progress and receipt, encrypted. It answers a form's questions from that memory (`answer_questions`) and learns each new wording, so the candidate is never asked the same thing twice.
- **The Gradbo folder** is one project folder on the candidate's computer, `~/Gradbo` unless they chose another. It holds their documents: the CV in `profile/cv/` and, for each application, the tailored CV, cover letter and their checks. It also holds the skills and an `AGENTS.md` that tells any agent started there what the folder is. The layout is in [references/folder-layout.md](references/folder-layout.md); read it before writing any file.

You are the go-between: read the page, ask Gradbo, fill, ask the candidate only what Gradbo doesn't know, and save their answer to Gradbo the moment they give it. You apply with this agent's own browser tools, in the candidate's own browser wherever the agent supports it (Claude Code's Chrome integration, for example), so their logins and saved passwords are there. Playwright's browser extension is the fallback for agents without one.

## Pick the task

| The candidate wants to | Read |
|---|---|
| Start, or bring their profile up to date (new CV, new facts, preferences) | [references/setup.md](references/setup.md) |
| See new roles, or triage what Gradbo found | [references/find.md](references/find.md) |
| Apply to a role, or to their jobs in general ("apply to my jobs") | [references/apply.md](references/apply.md) (step 0 picks the roles when none is named), then [questions.md](references/questions.md), [consents.md](references/consents.md) and [documents.md](references/documents.md) as the form needs them |
| Check email for replies, record an application they sent themselves, report an outcome, or check the tracker | [references/organise.md](references/organise.md), [references/email.md](references/email.md) |

## First, in every session

Do these before the task, without asking; they are routine and take a moment.

1. **Be in the Gradbo folder.** If the current directory isn't it (no `AGENTS.md` naming it a Gradbo workspace and no `profile/`), check whether `~/Gradbo` exists. If it does, ask the candidate to restart you there (`cd ~/Gradbo`), so their files never scatter; if it doesn't, set the folder up as setup step 1 describes.
2. **Check the Gradbo connection**: call `get_profile()`. If the gradbo tools are missing or refuse the token, follow [references/install.md](references/install.md), step 1, before anything else.
3. **Refresh `AGENTS.md`** from the template when it lacks the template's lines ([references/setup.md](references/setup.md), step 1, "Already set up").
4. **Move an older folder in.** If the folder still has `profile/facts.md` or `answers/`, call `import_workspace` with them and move the files aside, as [references/setup.md](references/setup.md), "Moving an older folder in", describes. Then work from Gradbo, never from those files.
5. **Know whether setup is needed.** If `get_profile()` has no facts and there is no CV in `profile/cv/`, run setup first, whatever was asked. Setup starts with a preflight ([references/install.md](references/install.md)) that checks the Gradbo connection, this machine, the browser tool and mail.

## Rules that always apply

1. **Facts come only from evidence.** Everything you state about the candidate must come from their facts in Gradbo (`get_profile`, `answer_questions`), their stored answers, the CV, the live advert, or something the candidate told you in this session, which you save with `save_fact` and its source at once. Never invent or embellish claims, metrics, tools, grades, responsibilities, motivation, personal qualities or examples. If a fact is missing, ask for that one fact; never ask again for one Gradbo already has.
2. **Statements of fact are never guessed.** Right to work, sponsorship, convictions, age limits, disability adjustments and similar questions are answered only from a verified fact whose wording and time frame fit the question (now or at the start date). `answer_questions` reads work-rights wording for you; when it can't settle one, ask. Equal-opportunities monitoring questions follow the candidate's standing choice and consent instead ([references/questions.md](references/questions.md)) and are never asked about during a form.
3. **Read before you write.** Read the candidate's facts (`get_profile`) before opening the CV, and the live advert on the employer's own site before tailoring anything or applying. LinkedIn and Indeed are discovery sources only.
4. **Never state that the candidate wrote an answer unaided or that no AI was used.** Those are the candidate's own statements to make. Record the employer's AI guidance in the application's brief (`save_application`), then write the answers from verified evidence anyway.
5. **All prose goes through the humanizer skill, every time.** Everything you write or adapt for an employer is run through the `humanizer` skill before it is put in a document, typed into a form or saved: the CV's rewritten summary and reworded bullets, every cover letter, every free-text answer (new, or a stored one adapted for this employer), and any other sentence you compose ("anything else to add", a short motivation line). No exceptions for short text or time pressure. Then `docs.py tells` checks documents for what it missed, Gradbo refuses an answer you wrote unless it is saved with `humanized=true`, and the receipt marks each piece. Values (a name, a date, an option) and the candidate's own words, given as they said them, are not rewritten. It is required. If it isn't installed, install it first ([references/install.md](references/install.md), step 3); if this agent can't invoke skills by name, read its `SKILL.md` and follow it. The pass removes formulaic language; it never adds claims.
6. **What goes where.** The candidate's facts, answers, application briefs, progress and receipts go to Gradbo through the memory tools, which encrypt them. Everything else sent to Gradbo stays impersonal:
   - Fit rationales (`override_fit`) describe the role's requirements and how well they are covered ("Needs SystemVerilog and UVM; covered"), not the candidate's grades or employers.
   - Notes, status reasons and confirmations (`add_note`, `update_status`, `record_submission`'s `confirmation` and `note`) carry dates, references and folder names, never answers or personal facts.
   - `remember_question` gets the question's wording only, never the candidate's details in it.
   - The CV and documents stay in the folder; never send their files or text through a tool.
7. **Email is read only.** Read the candidate's mail (through Gradbo when their inbox is connected, otherwise your own mail tool) only for verification codes, confirmation links and employers' replies ([references/email.md](references/email.md)); never send, delete or mark messages. Open confirmation links in the candidate's own browser.
8. **No credentials anywhere.** You apply in the candidate's own browser ([references/install.md](references/install.md), step 4). Gradbo tracks their employer accounts (`find_account`, `record_account`), but passwords live in the browser's password manager, and the candidate accepts or types them; you never read or type one. Never write passwords, one-time codes, cookies or identity documents to any file, note or tool call, including `save_fact` and `record_account`. The candidate connects their inbox in the dashboard themselves; never ask for their mail password.
9. **Exclude clearance and vetting roles.** If an advert requires security clearance or vetting, don't apply; set the role to Excluded with the reason. When sponsorship or eligibility is unclear, record what the advert says rather than guessing.
10. **Submit without asking for approval.** The candidate asked you to apply: prepare, fill in, upload and submit. "Awaiting final review" or "awaiting approval" is never a stopping point. Stop only for a missing fact, a protection (rule 13), a statement only the candidate can make (rule 4), or a step only they can take in their browser (accepting a password, choosing a file when an upload fails). If they asked you only to prepare, or to show them first, do that instead.
11. **Status changes go through the tools.** Use `update_status` and `record_submission`; an illegal transition is refused with the reason, so follow the legal path (Shortlisted → Materials prepared → Submitted) rather than forcing it. A role whose advert has gone is Closed; after submitting, a role moves to Assessment completed, Interview, Offer, Rejected or Withdrawn (`get_criteria()` lists every legal move).
12. **Every submission has a receipt.** Pass the exact submission to `record_submission` as its `receipt` ([references/apply.md](references/apply.md), step 5). This includes applications the candidate sent themselves ([references/organise.md](references/organise.md)).
13. **Stop at protections.** On a CAPTCHA, anti-bot block or an access check you cannot pass with direct page controls, stop retrying. Write `manual-handoff.md` in the application folder and hand over to the candidate. Never try to defeat the protection.

## The gradbo tools

**Roles and the tracker**

| Tool | Use |
|---|---|
| `get_digest(unjudged_only=True)` | New eligible roles on live adverts not yet judged, best keyword match first; `include_uncertain=True` adds the Researching roles the rules could not decide |
| `get_job(job_id)` | One role: advert text, eligibility verdict and reasons, closing date, status, notes, links |
| `list_jobs(status=..., state=..., q=..., closes_before=..., offset=...)`, `search_jobs(q)` | Look roles up, e.g. everything Submitted, or Shortlisted roles whose advert is still `open`. `list_jobs` returns a page: `items` and `total` |
| `override_fit(job_id, fit_score, fit_rationale)` | Record your 0-10 judgement; it replaces the keyword score |
| `update_status(job_id, status, reason)`, `bulk_update_status(job_ids, status, reason)` | Move roles along the legal transitions (up to 100 at once) |
| `get_job_history(job_id)`, `get_job_snapshots(job_id)` | When the status changed and by whom; how the advert changed since the crawl first saw it |
| `add_note(job_id, note)` | Append a dated, impersonal note |
| `record_submission(job_id, application_dir, confirmation, note, receipt)` | After the employer confirms receipt: moves the role to Submitted and keeps the receipt |
| `add_job_by_url(url, ...)` | Add a role the crawl has not found, from the employer's advert link |
| `get_preferences()`, `set_preferences(preferences)` | The coarse search filter the server applies |
| `get_criteria()`, `export_tracker(statuses=None)` | The eligibility rules and legal transitions; the tracker as CSV |

**The candidate's memory**

| Tool | Use |
|---|---|
| `answer_questions(questions, job_id)` | Every question on a form page answered from the memory, or why not (ask for a fact, confirm a reading, show the options) |
| `remember_question(wording, key, polarity, employer, confirmed)` | Teach Gradbo which fact a wording asks for, once you have settled it |
| `save_fact(key, value, source, source_ref, ...)`, `forget_fact(key)` | Store a fact the moment you learn it; delete a wrong one |
| `get_profile(prefix, include_answers)` | The candidate's facts (and answers) for tailoring the CV and letters |
| `save_answer(key, question, answer, scope, humanized=true, ...)`, `find_answers(question, employer)`, `forget_answer(key, scope)` | Reusable free-text answers, by question, this employer's first |
| `save_application(job_id, brief, progress, receipt, application_dir)`, `get_application(job_id)` | An application's brief and form progress, so any agent can resume |
| `import_workspace(facts_md, answers, receipts)` | Move an older folder's `facts.md`, answers and receipts into Gradbo |

**Mail and employer accounts**

| Tool | Use |
|---|---|
| `mail_status()` | Whether the candidate has connected their inbox to Gradbo (they do it in Settings > Your data) |
| `find_verification_codes(minutes, from_domain)` | Recent verification and confirmation emails, with their codes and confirmation links; open links in the candidate's browser |
| `scan_replies(days, domains)` | Recent recruiting mail, each classified (confirmation, rejection, interview, offer, ...) |
| `find_account(portal_url)`, `record_account(portal_url, status, username, job_id, used)`, `list_accounts()` | The candidate's accounts on application portals, so you sign in rather than register twice; never a password |

If the gradbo tools are missing or refuse the token, follow [references/install.md](references/install.md), step 1. A refused call says why; act on the reason rather than retrying it unchanged.
