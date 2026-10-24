# Apply to a role

When the candidate asks you to apply, prepare everything and submit; they don't need to review the package first unless they ask to. Don't stop to wait for a final review or approval (SKILL.md rule 10). If they ask you only to *prepare*, stop before the final submit and tell them what is ready.

## 0. Choose the roles (when they don't name one)

"Apply to my jobs", "apply to the shortlist": pick the roles yourself, and never one they have already applied to.

1. Take the candidates from `list_jobs(status="Shortlisted", state="open")` and `list_jobs(status="Materials prepared", state="open")`, best fit first.
2. Skip a role when:
   - `get_application(job_id)` already has a receipt;
   - `search_jobs("<role title>")` shows the same employer and title already at Submitted or later (the same advert can be listed twice under different ids);
   - a folder under `applications/` (at any depth) is for the same employer and role and holds a receipt from before Gradbo kept them.
3. Apply to one role per employer at a time. If the employer already has an application in progress or submitted this cycle, skip its other roles unless the candidate named them, since some employers allow only one application.
4. Tell the candidate in one line which roles you will apply to and which you skipped and why, then work through them one at a time, each from step 1. This is a note, not a question; carry on unless they stop you.

## 1. Check the role

1. `get_job(job_id)` (or `add_job_by_url` first for a role Gradbo doesn't have). Stop if the role is already applied to or finished (Submitted, Assessment completed, Interview, Offer, Rejected, Withdrawn or Closed), or the closing date has passed. Stop too if step 0's checks find an application for the same employer and role title under another id or folder. If it was shortlisted a while ago, `get_job_snapshots(job_id)` shows whether the advert has changed since.
2. Open the official advert on the employer's own site (`apply_url` or `canonical_url`) and confirm it is live. If it has gone, `update_status(job_id, "Closed", reason="Advert no longer live on <date>")` and tell the candidate.
3. Check eligibility yourself against the advert and the candidate's facts (`get_profile`):
   - Clearance or vetting required: don't apply (SKILL.md rule 9).
   - Sponsorship: if the candidate needs it and the advert refuses it, don't apply. If the advert says nothing, apply and record that sponsorship support is unconfirmed.
   - Degree, grade, start date, location or driving licence requirements the candidate clearly doesn't meet: don't apply; `update_status(job_id, "Excluded", reason="Requirement not met: <which>")` and tell them in one line. Where their facts don't settle it (no grade stated, a start date that might fit), apply and record the unknown in the brief.
4. Find the employer's guidance on AI use in applications, if any (advert, application page, FAQ). It does not change how you work (SKILL.md rule 4), but it belongs in the record.

## 2. The folder and the brief

Create `applications/YYYY-MM-DD_employer_role/` for the documents, one folder at the top of `applications/`, never `applications/<employer>/<role>/` ([folder-layout.md](folder-layout.md)). Then record the brief:

```
save_application(job_id, application_dir="applications/<folder>", brief={
  "official_advert": "<employer's own URL>", "application_form": "<URL, once known>", "requisition": "<reference or null>",
  "location": "...", "start": "...", "closing_date": "<date or 'not stated'>", "live_advert_checked": "<YYYY-MM-DD>",
  "requirements": "<what the advert requires>", "eligibility": "<how the candidate's verified facts meet it; unknowns as unknown>",
  "employer_ai_guidance": "<their exact words and where, or 'None found (checked <date>)'>"})
```

## 3. Documents

- **CV:** tailor a copy of the candidate's CV for the advert in the application folder, as [documents.md](documents.md) describes for LaTeX, Word or PDF-only CVs. Rewrite the profile or summary section for this role, then reorder, and reword a point toward the advert's terms only where the candidate's own wording already supports it; add nothing the CV and their facts don't contain. `docs.py check` and `docs.py compare` must both pass.
- **Cover letter:** write one when the form asks for one or offers an upload for one ([documents.md](documents.md), "Cover letters"). Use one A4 page. Open with why this role, from the advert's specifics, then meet its main requirements with evidence. Every claim must come from the facts or CV. Run it through the `humanizer` skill, then check it.
- Once the documents pass, `update_status(job_id, "Materials prepared")` (from Shortlisted or Researching; skip it if the transition is refused).

## 4. The form

Work through the application in the candidate's browser, page by page, with this agent's own browser tools ([install.md](install.md), step 4). Read the page's structure (fields, labels, options) before acting rather than guessing from a screenshot, and answer the page with `answer_questions` ([questions.md](questions.md)). Act on one field at a time, and read the page again after each change, since forms often reveal new fields; send new ones to `answer_questions` too. After each page, save the progress: `save_application(job_id, progress={"page": ..., "fields": [{"label", "entered", "source", "open_question"}], "stopped_at": ...})`. If the session ends, this is how you, another agent or the candidate resume (`get_application`).

- **Accounts:** many portals (Workday, SuccessFactors, Taleo, SmartRecruiters) need an account. Gradbo keeps track of them; the candidate's browser password manager keeps the passwords.
  1. **Look it up:** `find_account(portal_url=<the portal page>)`. One account serves every role on the same portal.
  2. **Signing in** (an account exists, or the candidate is already signed in): use the sign-in name it gives. If the browser autofills the password, sign in; if not, ask the candidate to sign in in that tab, then carry on. Then `record_account(portal_url, status="active", used=True)`.
  3. **Creating one** (none exists): fill in everything but the password from `answer_questions` (the email, the name). Ask the candidate to click the password field and accept the browser's suggested strong password (or type their own), so their password manager saves it; it is usually one click. Submit the registration, then at once `record_account(portal_url, status="pending_verification", username=<the sign-in email>, job_id=job_id)`.
  4. **Confirming it:** most portals send a code or a confirmation link. Get it as [email.md](email.md) describes (`find_verification_codes(from_domain=<the sender's mail domain, such as myworkday.com>)` when the inbox is connected, then without the filter if nothing comes), type the code or open the link in the candidate's browser, then `record_account(portal_url, status="active")`.
  5. **Locked out or a forgotten password:** use the portal's reset link; the reset email comes the same way. Have the candidate accept the new suggested password, then carry on. `record_account(..., status="locked")` if it stays locked.
  - Never read out, type, copy or record a password, in a tool call, a file or anywhere else; `record_account` refuses anything that looks like one. Don't store a code or link.
- **Fields:** fill each from `answer_questions` ([questions.md](questions.md)), identity and contact fields included.
- **Facts the candidate gives you:** when you ask for a missing fact, `save_fact` it as soon as they answer, before you carry on with the form, with `source="candidate"` and `source_ref="told the agent on <date>"`. The next form finds it and never asks again.
- **Uploads:** attach files by their absolute path in the application folder, using your browser tool's file-upload action. If it has none, or the upload is refused, ask the candidate to choose the file in the page's file dialog, telling them its exact path, then carry on.
- **Consents and declarations:** follow [consents.md](consents.md).
- **Controls you can't operate** (custom widgets that ignore input, embedded assessments): write `manual-handoff.md` from [templates/manual-handoff.md](../templates/manual-handoff.md) and hand over.
- **CAPTCHA or anti-bot block:** stop, write `manual-handoff.md`, and ask the candidate to complete that step in the same tab (it is their browser). Resume once they say it is done.

Before the final submit, go back over every page yourself: all required fields are filled, every statement of fact matches a verified fact, and the uploaded files are the checked ones. Then submit; this check is yours, not a review for the candidate.

## 5. Submit and record

1. Submit once. Wait for the employer's confirmation page or message and capture its text, any reference number and the URL.
2. If you can't tell whether it went through (an error after submitting, a timeout, a blank page), don't submit again. Check the employer's candidate portal, or ask the candidate to check their email. Retry only when it is clear nothing was received.
3. `record_submission(job_id, application_dir="applications/<folder>", confirmation="<reference or the confirmation's first line>", receipt={...})`, with the receipt:

   ```json
   {"schema": "gradbo-receipt/1", "submitted_at": "<YYYY-MM-DDTHH:MM:SSZ>", "submitted_by": "agent",
    "official_advert": "<URL>", "application_form": "<URL>",
    "confirmation": {"text": "...", "reference": "<or null>", "url": "<or null>", "received_at": "<or null>"},
    "documents": [{"file": "main.pdf", "sha256": "...", "notes": "<how it was tailored>"}],
    "answers": [{"question": "<label as shown>", "answer": "<exactly as entered>", "source": "<fact:<key> | answer:<scope> | candidate (<date>) | drafted>"}],
    "administrative_defaults": [{"question": "...", "answer": "..."}],
    "accepted_statements": [{"wording": "<exact text>", "accepted": "<ticked | signed as <name>>"}],
    "left_unticked": ["<optional consent or marketing wording>"],
    "employer_ai_guidance": "<summary or null>", "notes": ["<a handoff, an unfilled field, an uncertain point>"]}
   ```

   Every submitted answer goes in exactly as entered; use `null` for anything unknown. Keep `confirmation` and `note` impersonal (SKILL.md rule 6). Check that the role it returns has status `Submitted`; if the call failed, fix the cause and call it again before moving on, or the role will be offered again.
4. Save any new reusable answers with `save_answer` (questions.md, `draft`); facts were saved as you went.
5. Tell the candidate it is done: role, employer, confirmation and folder.
