# Organise the workspace

Do this after each application, and whenever the candidate asks to tidy up or check where things stand.

## Answers

- After an application, look at `application-notes.md` for answers worth reusing: free-text answers, and choices that will recur (notice period, preferred locations, salary expectation).
- File each under its canonical key ([question-keys.md](question-keys.md)) in `answers/`, or under `answers/employers/<slug>.md` when it only fits that employer. If a file exists, keep the better answer and add the new wording to the **Question** line as an alternative only when it differs in meaning.
- Facts the candidate gave you during the application go into `profile/facts.md` with source `candidate: told the agent on <date>`.

## Facts

- A fact whose `valid until` has passed: change its status to `stale` and tell the candidate.
- Two facts that disagree (two graduation dates, an answer that contradicts a fact): keep both, mark the older one `stale`, and ask the candidate which is right next time you talk.
- An answer whose `uses facts` include a fact that changed: mark it `stale`.
- After a new CV, re-check every fact with a `cv:` source against the new text.

## Applications the candidate sent themselves

When the candidate tells you they applied on their own:

1. Find the role (`search_jobs`, `list_jobs`), or add it with `add_job_by_url`.
2. Create its folder as usual ([folder-layout.md](folder-layout.md)), with `job.md` from what `get_job` returns.
3. Write `receipt.md` from [templates/receipt.md](../templates/receipt.md) and `receipt.json` from [templates/receipt.json](../templates/receipt.json) with what they tell you: the date, the confirmation, which CV or cover letter they sent if they know. Leave out what you don't know rather than guessing (`null` or an empty list in the JSON), set `"submitted_by": "candidate"`, and note "Submitted by the candidate; answers not seen".
4. `record_submission(job_id, application_dir="applications/<folder>", confirmation="<reference>")`.

## Withdrawing

When the candidate withdraws an application they have sent, `update_status(job_id, "Withdrawn", reason="Withdrawn by the candidate <date>")` and add a dated line under **Afterwards** in its `receipt.md` (and to `afterwards` in `receipt.json`). Withdrawing from the employer's portal is the candidate's step unless they ask you to do it. A role they decide against before applying is Excluded instead.

## Replies

Check the candidate's email for employers' replies ([email.md](email.md), "Replies after applying") and update the tracker from them.

## Tracker

Check that the server and the workspace agree:

1. `list_jobs(status="Submitted", limit=200)`, and the same for `Assessment completed`, `Interview`, `Offer`, `Rejected` and `Withdrawn`. Each call returns a page (`items`, `total`); if `total` is more than you got, call again with `offset`.
2. List `applications/*/receipt.md`.
3. A receipt whose role is not Submitted on the server: `record_submission` with that folder and its confirmation.
4. A role Submitted on the server with no receipt: tell the candidate; it was applied to elsewhere or the receipt was lost. `get_job_history(job_id)` shows when it was marked Submitted and by whom.
5. Outcomes the candidate reports or email shows (an assessment invite, a rejection, an offer): handle them as in the table in [email.md](email.md).

## Never

Don't delete application folders or receipts, and don't move files the candidate made themselves. Ask first.
