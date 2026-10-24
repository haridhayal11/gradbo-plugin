---
name: gradbo
description: Job search and applications with Gradbo. Use before any gradbo MCP tool call, and whenever the candidate wants to set up their job-search profile, find or triage roles, tailor a CV or cover letter, fill in or submit an application, answer screening questions, record an application they sent or an outcome they heard back, or check what they have applied to. Keeps the local workspace (profile, answers, application folders and receipts) in step with the gradbo tracker.
---

# Gradbo

Gradbo has two halves:

- **The gradbo MCP server** finds roles and tracks them. It crawls UK employers' career pages, filters the adverts by the candidate's search preferences and keeps each role's status, fit score and notes. It holds nothing else about the candidate.
- **The Gradbo folder** is one project folder on the candidate's computer, `~/Gradbo` unless they chose another. It holds everything personal: the CV, verified facts, reusable answers, and each application's documents and receipt. It also holds the skills and an `AGENTS.md` that tells any agent started there what the folder is. You keep it organised; the layout is in [references/folder-layout.md](references/folder-layout.md), so read it before writing any file.

You apply with this agent's own browser tools, in the candidate's own browser wherever the agent supports it (Claude Code's Chrome integration, for example), so their logins and saved passwords are there. Playwright's browser extension is the fallback for agents without one.

## Pick the task

| The candidate wants to | Read |
|---|---|
| Start, or bring their profile up to date (new CV, new facts, preferences) | [references/setup.md](references/setup.md) |
| See new roles, or triage what Gradbo found | [references/find.md](references/find.md) |
| Apply to a role, or to their jobs in general ("apply to my jobs") | [references/apply.md](references/apply.md) (step 0 picks the roles when none is named), then [questions.md](references/questions.md), [consents.md](references/consents.md) and [documents.md](references/documents.md) as the form needs them |
| Check email for replies, record an application they sent themselves, report an outcome, tidy the workspace, or check the tracker | [references/organise.md](references/organise.md), [references/email.md](references/email.md) |

**Work only in the Gradbo folder, in its layout.** Read [references/folder-layout.md](references/folder-layout.md) before writing any file; each application is `applications/YYYY-MM-DD_employer_role/`. If the current directory isn't it (there is no `AGENTS.md` naming it a Gradbo workspace and no `profile/`), check whether `~/Gradbo` exists:
- If it does, ask the candidate to restart you there (`cd ~/Gradbo`), so their files never scatter.
- If it doesn't, set the folder up as setup step 1 describes.

When you start in an existing Gradbo folder, bring its `AGENTS.md` up to date with the template first ([references/setup.md](references/setup.md), step 1, "Already set up"). If `profile/facts.md` does not exist yet, run setup first, whatever was asked. Setup starts with a preflight ([references/install.md](references/install.md)) that checks the Gradbo connection, this machine, the browser tool and mail.

## Rules that always apply

1. **Facts come only from evidence.** Everything you state about the candidate must come from `profile/facts.md`, the CV, an answer file, the live advert, or something the candidate told you in this session, which you then record with its source. Never invent or embellish claims, metrics, tools, grades, responsibilities, motivation, personal qualities or examples. If a fact is missing, ask for that one fact; don't ask again for one that is already verified.
2. **Statements of fact are never guessed.** Right to work, sponsorship, convictions, age limits, disability adjustments and similar questions are answered only from a verified fact whose wording and time frame fit the question (now or at the start date). Otherwise ask. Equal-opportunities monitoring questions follow the candidate's standing choice instead ([references/questions.md](references/questions.md)) and are never asked about.
3. **Read before you write.** Read `profile/facts.md` and the relevant `answers/` files before opening the CV. Read the live advert on the employer's own site before tailoring anything or applying. LinkedIn and Indeed are discovery sources only.
4. **Never state that the candidate wrote an answer unaided or that no AI was used.** Those are the candidate's own statements to make. Record the employer's AI guidance in the application's `job.md`, then write the answers from verified evidence anyway.
5. **Prose goes through the humanizer skill.** Run CV text, cover letters and free-text answers through the `humanizer` skill before they are saved or sent. It is required. If it isn't installed, install it first ([references/install.md](references/install.md), step 3); if this agent can't invoke skills by name, read its `SKILL.md` and follow it. The pass removes formulaic language; it never adds claims.
6. **Keep personal details off the server.** Anything sent to the gradbo tools must be impersonal:
   - Fit rationales (`override_fit`) describe the role's requirements and how well they are covered, not the candidate's details. Write "Needs SystemVerilog and UVM; covered", not the candidate's grades or employers.
   - Notes and confirmations (`add_note`, `record_submission`) carry dates, references and folder names, never answers, documents or personal facts.
   - Never send the CV, `facts.md`, answers or receipts through any tool.
7. **Email is read only.** Read the candidate's mail only for verification codes and employers' replies ([references/email.md](references/email.md)); never send, delete or mark messages.
8. **No credentials in the workspace.** You apply in the candidate's own browser ([references/install.md](references/install.md), step 4). Employer passwords live in its password manager, and the candidate accepts or types them; you never read or type one. Never write passwords, one-time codes, cookies or identity documents to any file, note or tool call.
9. **Exclude clearance and vetting roles.** If an advert requires security clearance or vetting, don't apply; set the role to Excluded with the reason. When sponsorship or eligibility is unclear, record what the advert says rather than guessing.
10. **Submit without asking for approval.** The candidate asked you to apply: prepare, fill in, upload and submit. "Awaiting final review" or "awaiting approval" is never a stopping point. Stop only for a missing fact, a protection (rule 13), or a statement only the candidate can make (rule 4). If they asked you only to prepare, or to show them first, do that instead.
11. **Status changes go through the tools.** Use `update_status` and `record_submission`; an illegal transition is refused, so follow the legal path (Shortlisted → Materials prepared → Submitted) rather than forcing it. A role whose advert has gone is Closed; after submitting, a role moves to Assessment completed, Interview, Offer, Rejected or Withdrawn (`get_criteria()` lists every legal move).
12. **Every submission has a receipt.** Before calling `record_submission`, make sure the role has its folder under `applications/` with `job.md` and `receipt.md`, and pass that folder. This includes applications the candidate sent themselves ([references/organise.md](references/organise.md)).
13. **Stop at protections.** On a CAPTCHA, anti-bot block or an access check you cannot pass with direct page controls, stop retrying. Write `manual-handoff.md` and hand over to the candidate. Never try to defeat the protection.

## The gradbo tools

| Tool | Use |
|---|---|
| `get_digest(unjudged_only=True)` | New eligible roles on live adverts not yet judged, best keyword match first; `include_uncertain=True` adds the Researching roles the rules could not decide |
| `get_job(job_id)` | One role: advert text, eligibility verdict and reasons, closing date, status, notes, links |
| `list_jobs(status=..., state=..., q=..., closes_before=..., offset=...)`, `search_jobs(q)` | Look roles up, e.g. everything Submitted, or Shortlisted roles whose advert is still `open`. `list_jobs` returns a page: `items` and `total` |
| `override_fit(job_id, fit_score, fit_rationale)` | Record your 0-10 judgement; it replaces the keyword score |
| `update_status(job_id, status, reason)` | Move a role along the legal transitions |
| `bulk_update_status(job_ids, status, reason)` | Move up to 100 roles at once, e.g. after triage; reports which moves were refused |
| `get_job_history(job_id)` | When the role's status changed, by whom and why |
| `get_job_snapshots(job_id)` | How the advert has changed since the crawl first saw it (a moved deadline, new wording) |
| `add_note(job_id, note)` | Append a dated, impersonal note |
| `set_application_dir(job_id, application_dir)` | Link a role to its workspace folder |
| `record_submission(job_id, application_dir, confirmation, note)` | After the employer confirms receipt: moves the role to Submitted and notes the confirmation |
| `add_job_by_url(url, ...)` | Add a role the crawl has not found, from the employer's advert link |
| `get_preferences()`, `set_preferences(preferences)` | The coarse search filter the server applies |
| `get_criteria()` | The eligibility rules and legal status transitions |
| `export_tracker(statuses=None)` | The tracker as CSV for the candidate's own records: by default the roles shortlisted, watched or applied to |

If the gradbo tools are missing or refuse the token, follow [references/install.md](references/install.md), step 1.
