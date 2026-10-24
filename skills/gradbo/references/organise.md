# Organise: the tracker, outcomes and the candidate's memory

Do this after each application, and whenever the candidate asks to tidy up or check where things stand.

## Answers and facts

Gradbo keeps them; you keep them right.

- After an application, save any reusable answer you haven't yet (`save_answer`): free-text answers, and choices that will recur (preferred locations, salary expectation). Use `scope="employer:<slug>"` when it only fits that employer. If one exists under the key, keep the better answer.
- `get_profile()` marks a fact whose `valid_until` has passed as `stale`; tell the candidate and ask for the current value.
- Two facts that disagree (two graduation dates, an answer that contradicts a fact): save the right one once the candidate says which, and `forget_fact` or mark the other `stale`.
- An answer written from a fact that changed is marked `stale` by Gradbo; rewrite it from the new fact when it is next needed.
- After a new CV, re-check every fact whose source is the CV against the new text (setup.md, step 2).

## Applications the candidate sent themselves

When the candidate tells you they applied on their own:

1. Find the role (`search_jobs`, `list_jobs`), or add it with `add_job_by_url`.
2. `save_application(job_id, brief={...})` with what `get_job` returns and the advert's links.
3. `record_submission(job_id, application_dir="applications/<folder or 'none'>", confirmation="<reference>", receipt={"schema": "gradbo-receipt/1", "submitted_by": "candidate", "submitted_at": "<date>", "confirmation": {...}, "documents": [<what they say they sent>], "answers": [], "notes": ["Submitted by the candidate; answers not seen"]})`. Leave out what you don't know (`null`, empty lists) rather than guessing.

## Applications from an earlier setup

When the candidate applied to roles before using Gradbo (another tool, a spreadsheet), those roles must be marked so you never apply again:

1. Ask them for the list as a CSV: one row per application with the employer, the role title, the advert link if they have it, the status (applied, interview, rejected, …) and the date. An export from their old setup is fine as it is; the columns don't need renaming.
2. They send that file to the Gradbo admin, who imports it into their account. Each role becomes Submitted (or its later outcome), with `imported/<date>` as its folder.
3. After the import, `list_jobs(status="Submitted")` shows them. They have no receipts and need none (Tracker, step 3).

An older Gradbo folder with `profile/facts.md`, `answers/` and receipts is moved in with `import_workspace` instead (setup.md, "Moving an older folder in").

## Withdrawing

When the candidate withdraws an application they have sent, `update_status(job_id, "Withdrawn", reason="Withdrawn by the candidate <date>")`. Withdrawing from the employer's portal is the candidate's step unless they ask you to do it. A role they decide against before applying is Excluded instead.

## Replies

Check the candidate's email for employers' replies ([email.md](email.md), "Replies after applying") and update the tracker from them.

## Tracker

1. `list_jobs(status="Submitted", limit=200)`, and the same for `Assessment completed`, `Interview`, `Offer`, `Rejected` and `Withdrawn`. Each call returns a page (`items`, `total`); if `total` is more than you got, call again with `offset`.
2. A role you submitted whose `get_application(job_id)` has no receipt: the submission wasn't recorded fully; add the receipt with `record_submission` (it changes nothing else when repeated).
3. A Submitted role with no receipt and an application folder starting `imported/`, or a history (`get_job_history`) showing it was set by `import`: an application from an earlier setup; leave it. Any other Submitted role without a receipt: tell the candidate; it was applied to elsewhere.
4. Outcomes the candidate reports or email shows (an assessment invite, a rejection, an offer): handle them as in the table in [email.md](email.md).

## Folder names

Application folders you or another agent made outside the layout (`applications/<employer>/<role>/`, a name without the date) move to `applications/YYYY-MM-DD_employer_role/`, with the date from their brief or receipt. Then `save_application(job_id, application_dir="applications/<new folder>")`. Leave folders the candidate made themselves where they are.

## Never

Don't delete application folders, and don't move files the candidate made themselves (renaming agent-made folders, above, is fine). Delete facts or answers only when they are wrong or the candidate asks; the candidate can delete everything themselves in Settings > Your data.
