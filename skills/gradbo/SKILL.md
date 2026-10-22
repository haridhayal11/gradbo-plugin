---
name: gradbo
description: Job search and applications with Gradbo. Use before any gradbo MCP tool call, and whenever the candidate wants to set up their job-search profile, find or triage roles, tailor a CV or cover letter, fill in or submit an application, answer screening questions, record an application they sent or an outcome they heard back, or check what they have applied to. Keeps the local workspace (profile, answers, application folders and receipts) in step with the gradbo tracker.
---

# Gradbo

Gradbo has two halves:

- **The gradbo MCP server** finds roles and tracks them. It crawls UK employers' career pages, filters the adverts by the candidate's search preferences and keeps each role's status, fit score and notes. It holds nothing else about the candidate.
- **The workspace**, a local folder (the directory you were started in unless the candidate says otherwise), holds everything personal: verified facts, the CV, reusable answers, each application's documents and its receipt. You keep it organised. The layout is in [references/folder-layout.md](references/folder-layout.md); read it before writing any file.

You apply with whatever browser tool this harness gives you, for example Playwright MCP or a browser extension.

## Pick the task

| The candidate wants to | Read |
|---|---|
| Start, or bring their profile up to date (new CV, new facts, preferences) | [references/setup.md](references/setup.md) |
| See new roles, or triage what Gradbo found | [references/find.md](references/find.md) |
| Apply to a role (prepare, fill in, submit) | [references/apply.md](references/apply.md), then [questions.md](references/questions.md), [consents.md](references/consents.md) and [documents.md](references/documents.md) as the form needs them |
| Record an application they sent themselves, report an outcome, tidy the workspace, or check the tracker | [references/organise.md](references/organise.md) |

If `profile/facts.md` does not exist yet, run setup first, whatever was asked.

## Rules that always apply

1. **Facts come only from evidence.** Everything you state about the candidate must come from `profile/facts.md`, the CV, an answer file, the live advert, or something the candidate told you in this session, which you then record with its source. Never invent or embellish claims, metrics, tools, grades, responsibilities, motivation, personal qualities or examples. If a fact is missing, ask for that one fact; don't ask again for one that is already verified.
2. **Statements of fact are never guessed.** Right to work, sponsorship, convictions, age, disability and similar questions are answered only from a verified fact whose wording and time frame fit the question (now or at the start date). Otherwise ask.
3. **Read before you write.** Read `profile/facts.md` and the relevant `answers/` files before opening the CV. Read the live advert on the employer's own site before tailoring anything or applying. LinkedIn and Indeed are discovery sources only.
4. **Never state that the candidate wrote an answer unaided or that no AI was used.** Those are the candidate's own statements to make. Record the employer's AI guidance in the application's `job.md`, then write the answers from verified evidence anyway.
5. **Prose goes through a humanizer pass.** Run CV text, cover letters and free-text answers through the `humanizer` skill if this harness has it, otherwise through [references/prose-checks.md](references/prose-checks.md). The pass removes formulaic language; it never adds claims.
6. **Keep personal details off the server.** Anything sent to the gradbo tools must be impersonal:
   - Fit rationales (`override_fit`) describe the role's requirements and how well they are covered, not the candidate's details. Write "Needs SystemVerilog and UVM; covered", not the candidate's grades or employers.
   - Notes and confirmations (`add_note`, `record_submission`) carry dates, references and folder names, never answers, documents or personal facts.
   - Never send the CV, `facts.md`, answers or receipts through any tool.
7. **No credentials in the workspace.** Employer passwords live in the browser's own password manager, or the candidate types them in. Never write passwords, one-time codes, cookies or identity documents to any file, note or tool call.
8. **Exclude clearance and vetting roles.** If an advert requires security clearance or vetting, don't apply; set the role to Excluded with the reason. When sponsorship or eligibility is unclear, record what the advert says rather than guessing.
9. **Status changes go through the tools.** Use `update_status` and `record_submission`; an illegal transition is refused, so follow the legal path (Shortlisted → Materials prepared → Submitted) rather than forcing it.
10. **Every submission has a receipt.** Before calling `record_submission`, make sure the role has its folder under `applications/` with `job.md` and `receipt.md`, and pass that folder. This includes applications the candidate sent themselves ([references/organise.md](references/organise.md)).
11. **Stop at protections.** On a CAPTCHA, anti-bot block or an access check you cannot pass with direct page controls, stop retrying. Write `manual-handoff.md` and hand over to the candidate. Never try to defeat the protection.

## The gradbo tools

| Tool | Use |
|---|---|
| `get_digest(unjudged_only=True)` | New eligible roles not yet judged, best keyword match first |
| `get_job(job_id)` | One role: advert text, eligibility verdict and reasons, closing date, status, notes, links |
| `list_jobs(status=..., q=...)`, `search_jobs(q)` | Look roles up, e.g. everything Submitted |
| `override_fit(job_id, fit_score, fit_rationale)` | Record your 0-10 judgement; it replaces the keyword score |
| `update_status(job_id, status, reason)` | Move a role along the legal transitions |
| `add_note(job_id, note)` | Append a dated, impersonal note |
| `set_application_dir(job_id, application_dir)` | Link a role to its workspace folder |
| `record_submission(job_id, application_dir, confirmation, note)` | After the employer confirms receipt: moves the role to Submitted and notes the confirmation |
| `add_job_by_url(url, ...)` | Add a role the crawl has not found, from the employer's advert link |
| `get_preferences()`, `set_preferences(preferences)` | The coarse search filter the server applies |
| `get_criteria()` | The eligibility rules and legal status transitions |

If the tools are missing, the plugin's MCP connection is not set up. Ask the candidate to set `GRADBO_TOKEN` (and `GRADBO_URL` if they use their own server) to a token from Settings › Connect your agent, then restart the session.
