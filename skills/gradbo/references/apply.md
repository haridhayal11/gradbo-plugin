# Apply to a role

When the candidate asks you to apply, prepare everything and submit; they don't need to review the package first unless they ask to. If they ask you only to *prepare*, stop before the final submit and tell them what is ready.

## 1. Check the role

1. `get_job(job_id)` (or `add_job_by_url` first for a role Gradbo doesn't have). Stop if the status is Submitted, Rejected, Offer or Closed, or the closing date has passed.
2. Open the official advert on the employer's own site (`apply_url` or `canonical_url`) and confirm it is live. If it has gone, `update_status(job_id, "Excluded", reason="Advert no longer live on <date>")` and tell the candidate.
3. Check eligibility yourself against the advert and `profile/facts.md`:
   - Clearance or vetting required: don't apply (SKILL.md rule 9).
   - Sponsorship: if the candidate needs it and the advert refuses it, don't apply. If the advert says nothing, apply and record that sponsorship support is unconfirmed.
   - Degree, grade, start date, location or driving licence requirements the candidate doesn't meet: tell them and ask whether to continue.
4. Find the employer's guidance on AI use in applications, if any (advert, application page, FAQ). Record it word for word in `job.md`. It does not change how you work (SKILL.md rule 4), but it belongs in the record.

## 2. The folder

Create `applications/YYYY-MM-DD_employer_role/` ([folder-layout.md](folder-layout.md)) and write `job.md` from [templates/job.md](../templates/job.md). Then call `set_application_dir(job_id, "applications/<folder>")`.

## 3. Documents

- **CV:** tailor a copy of the candidate's CV for the advert, as [documents.md](documents.md) describes for LaTeX, Word or PDF-only CVs. You may reorder, and reword a point toward the advert's terms only where the candidate's own wording already supports it; add nothing the CV and facts don't contain. `docs.py check` and `docs.py compare` must both pass.
- **Cover letter:** write one when the form asks for one or offers an upload for one ([documents.md](documents.md), "Cover letters"). Use one A4 page and the advert's own requirements. Every claim must come from the facts or CV. Run it through the `humanizer` skill, then check it.
- Once the documents pass, `update_status(job_id, "Materials prepared")` (from Shortlisted or Researching; skip it if the transition is refused).

## 4. The form

Work through the application in the browser, page by page. Keep `application-notes.md` up to date as you go: each field's label as shown, what you entered, where the value came from, and any open question. If the session ends, this is how you or the candidate resume.

- **Accounts:** create the employer account or sign in when the form needs one, with the candidate's email from the facts. Let the browser's password manager generate and store the password, or ask the candidate to type it. Never write it down. For a verification email or code, follow [email.md](email.md). Don't store the code.
- **Fields:** fill each from [questions.md](questions.md). Identity and contact fields come straight from the facts.
- **Uploads:** upload files by their path in the application folder (for example Playwright MCP's `browser_file_upload` with the absolute path). If this browser tool cannot set a file input, ask the candidate to choose the file, telling them its exact path, then carry on.
- **Consents and declarations:** follow [consents.md](consents.md).
- **Controls you can't operate** (custom widgets that ignore input, embedded assessments): write `manual-handoff.md` from [templates/manual-handoff.md](../templates/manual-handoff.md) and hand over.
- **CAPTCHA or anti-bot block:** stop, write `manual-handoff.md`, and ask the candidate to complete that step in their own browser. Resume once they say it is done.

Before the final submit, go back over every page: all required fields are filled, every statement of fact matches a verified fact, and the uploaded files are the checked ones.

## 5. Submit and record

1. Submit once. Wait for the employer's confirmation page or message and capture its text, any reference number and the URL.
2. If you can't tell whether it went through (an error after submitting, a timeout, a blank page), don't submit again. Check the employer's candidate portal, or ask the candidate to check their email. Retry only when it is clear nothing was received.
3. Write `receipt.md` from [templates/receipt.md](../templates/receipt.md), with every submitted answer exactly as entered, and `receipt.json` with the same content as data.
4. `record_submission(job_id, application_dir="applications/<folder>", confirmation="<reference or the confirmation's first line>")`. Keep the confirmation impersonal (SKILL.md rule 6).
5. File any new reusable answers under `answers/` ([organise.md](organise.md)).
6. Tell the candidate it is done: role, employer, confirmation and folder.
