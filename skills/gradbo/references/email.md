# Email: codes and replies

You read the candidate's email for two things: verification codes and links while applying, and employers' replies afterwards. Email is read only: never send, reply, archive, delete or mark anything, and never copy a message into a Gradbo tool.

## Which mail access to use

Use the first that works, and remember the choice with `save_fact("workspace.mail_access", "connector" | "imap" | "none")`:

1. **A mail tool in this agent**, such as a Gmail, Outlook or Microsoft 365 connector, or any MCP server that can search and read messages. Use its search with the sender's domain and a recent time window.
2. **The IMAP script**, `<skill>/scripts/mail.py`, when the candidate has set `GRADBO_IMAP_USER` and `GRADBO_IMAP_PASSWORD` in their environment. This needs an app password, which Gmail supports; Outlook.com and Microsoft 365 don't, so their users need a connector. Run it with `python <skill>/scripts/mail.py ...`; it uses the standard library only and opens the inbox read-only.
3. **The candidate.** Ask them to read out the code or open the link, and tell them which employer and roughly when it was sent.

During setup, ask once which they want. Never ask for or store their mail password yourself; the IMAP settings live in their shell environment.

## Verification codes and links while applying

1. Trigger the email (create the account, ask to resend), and note the time and the site's domain (`acme.myworkdayjobs.com`, `greenhouse.io`).
2. Wait about a minute, then look for it:
   - connector: search mail from that domain in the last 30 minutes;
   - IMAP: `python <skill>/scripts/mail.py codes --minutes 30 --from <domain>` prints each verification mail's codes and action links.
3. Use the newest code or link at once. Don't write it to any file, note or receipt, and don't reuse an old one.
4. Nothing after two or three minutes: check the spam folder if the tool can, resend once, then ask the candidate.

## Replies after applying

Run this when the candidate asks "any news?", and as part of [organise.md](organise.md).

1. Collect the roles with an application in flight: `list_jobs(status=...)` for `Submitted`, `Assessment completed` and `Interview`, with their employers, and the domains from each role's links (`get_job`, and the brief in `get_application`). Each call returns a page (`items`, `total`); if `total` is more than you got, call again with `offset`.
2. Look at mail since the last check (the date is in `applications/mail-check.md`; 14 days on the first run):
   - connector: search mail from those employers' domains and from applicant tracking systems;
   - IMAP: `python <skill>/scripts/mail.py scan --days <n> --domains <employer domains, comma-separated>`.
3. Match each message to its role by employer and job title, and read it to decide what it is. The script's label is a hint, not a decision:

| The message is | Do |
|---|---|
| A confirmation of an application | If the role isn't Submitted, follow "Applications the candidate sent themselves" in [organise.md](organise.md). Otherwise nothing. |
| A rejection | `update_status(job_id, "Rejected", reason="Rejection email <date>")` |
| An invitation to an online test or assessment | Tell the candidate, with the deadline or the link. Add a note: `add_note(job_id, "Assessment invite <date>")`. Once they have done it, `update_status(job_id, "Assessment completed")`. |
| An invitation to an interview or assessment centre | Tell the candidate, with the date or the booking link. `update_status(job_id, "Interview", reason="Interview invite <date>")`. |
| An offer | `update_status(job_id, "Offer", reason="Offer email <date>")`, and tell the candidate at once |
| "Under review", a newsletter, anything else | Nothing |

4. The status change and its reason are the record ("Rejection email 2026-11-02"); copy no more of the message than that.
5. Write today's date to `applications/mail-check.md`, then give the candidate the summary: offers first, then invitations with their deadlines, then rejections.

Notes and reasons sent to Gradbo name the kind of message and the date only (SKILL.md rule 6).
