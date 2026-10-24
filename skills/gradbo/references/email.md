# Email: codes and replies

You read the candidate's email for two things: verification codes and confirmation links while applying, and employers' replies afterwards. Email is read only: never send, reply, archive, delete or mark anything, and never copy a message into a Gradbo tool beyond what the steps below record.

## Which mail access to use

Use the first that works:

1. **Gradbo's connection to their inbox.** `mail_status()` says whether the candidate has connected it (Settings > Your data in the dashboard). If it has, use `find_verification_codes` and `scan_replies`: they work the same from any agent or computer, and Gradbo reads the inbox read only. If `status` is `failing`, tell the candidate the reason (`last_error`) and that they can reconnect in the dashboard; use the next route meanwhile.
2. **A mail tool in this agent**, such as a Gmail, Outlook or Microsoft 365 connector, or any MCP server that can search and read messages. Use its search with the sender's domain and a recent time window.
3. **The IMAP script**, `<skill>/scripts/mail.py`, when the candidate has set `GRADBO_IMAP_USER` and `GRADBO_IMAP_PASSWORD` in their environment. Run it with `python <skill>/scripts/mail.py ...`; it uses the standard library only and opens the inbox read-only.
4. **The candidate.** Ask them to read out the code or open the link, and tell them which employer and roughly when it was sent.

When none of 1-3 is set up, suggest once, during setup, that they connect their inbox in Settings > Your data (a Gmail, iCloud or Yahoo app password; Outlook and Microsoft 365 users need route 2). Only the candidate can connect it: never ask for, type or store their mail password yourself.

## Verification codes and links while applying

1. Trigger the email (create the account, ask to resend), and note the time. Verification emails come from the system's mail domain, not the portal's address: Workday sends from `myworkday.com`, Greenhouse from `greenhouse-mail.io`, SmartRecruiters from `smartrecruiters.com`, others from the employer's or the system's base domain.
2. Wait about a minute, then look for it:
   - Gradbo: `find_verification_codes(minutes=30, from_domain="<sender's mail domain>")` returns each verification or confirmation email's `codes` and `links`, newest first. If it returns nothing, call it again without `from_domain` and take the newest message whose subject and time fit;
   - connector: search mail from that domain in the last 30 minutes;
   - IMAP: `python <skill>/scripts/mail.py codes --minutes 30 --from <domain>` prints each verification mail's codes and action links.
3. Use the newest at once:
   - **A code:** type it into the page.
   - **A confirmation link** ("confirm your email", "activate your account"): Gradbo gives links only from senders it trusts (an applicant tracking system, or the `from_domain` you asked for); a message with `sender_trusted: false` comes without links, since a sender can be forged. Ask for it again with the employer's or system's domain as `from_domain`. Open the link in a new tab of the candidate's own browser, check the page says the account or email is confirmed, then return to the application tab. Gradbo never opens links itself: many work only once, and some need that browser's session.
   Don't write a code or link to any file, note or receipt, and don't reuse an old one.
4. Nothing after two or three minutes (with and without the domain filter): check the spam folder if the tool can, resend once, then ask the candidate.

## Replies after applying

Run this when the candidate asks "any news?", and as part of [organise.md](organise.md).

1. Collect the roles with an application in flight: `list_jobs(status=...)` for `Submitted`, `Assessment completed` and `Interview`, with their employers, and the domains from each role's links (`get_job`, and the brief in `get_application`). Each call returns a page (`items`, `total`); if `total` is more than you got, call again with `offset`.
2. Look at mail since the last check (the date is in `applications/mail-check.md`; 14 days on the first run):
   - Gradbo: `scan_replies(days=<n>, domains=[<employer domains>])`;
   - connector: search mail from those employers' domains and from applicant tracking systems;
   - IMAP: `python <skill>/scripts/mail.py scan --days <n> --domains <employer domains, comma-separated>`.
3. Match each message to its role by employer and job title, and read it to decide what it is. The `kind` Gradbo or the script gives is a hint, not a decision:

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
