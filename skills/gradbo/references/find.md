# Find: triage new roles

Gradbo has already removed adverts that fail the hard rules (wrong level, clearance, closed, outside the UK, explicit no-sponsorship when the candidate needs it) and scored the rest by keyword. Your job is the judgement the server cannot make: how well the role fits this candidate's actual record.

## Loop

1. `get_digest(unjudged_only=True, limit=25)`. Each role has `id`, `title`, `employer`, `location`, `closes_at`, `fit_score` (keyword, 0-10), `verdict` and `fit_rationale`.
2. For each role, read `get_job(id)` for the advert text and the eligibility reasons, then judge it against `profile/facts.md` and `profile/cv/main.txt`:
   - **9-10:** one of the candidate's target areas, at a level they want, and the CV covers the core requirements.
   - **6-8:** a good match with gaps a graduate could close.
   - **3-5:** adjacent: a related field, or a stretch on level or core skills.
   - **0-2:** a different field or clearly the wrong level.
   Judge the substance of the role, not shared buzzwords: "Python" in a sales role is not a software match.
3. Record the judgement with `override_fit(id, score, rationale)`. The rationale names the role's requirements and how far they are covered, in one line, with no personal details ("Needs RTL design and UVM; both covered; no DSP required").
4. Move it on:
   - Score 7 or more: `update_status(id, "Shortlisted")`.
   - Score 2 or less: `update_status(id, "Excluded", reason="Not a match: <short reason>")`.
   - A role that needs security clearance or vetting, whatever the score: Excluded, with the advert's wording as the reason.
   - Anything else stays where it is. It is judged now, so it won't come back in the digest.
5. Repeat until the digest is empty or you have covered what the candidate asked for.

## Report

Give the candidate the shortlist: title, employer, closing date, your score and one line on why, best first. Flag closing dates within a week. Then ask which to apply to, unless they already told you to apply to everything you shortlist.

## Roles from elsewhere

When the candidate brings a role Gradbo hasn't found, call `add_job_by_url` with the employer's own advert link (job-board links are refused). If the result lists `missing` fields, read them from the page and call again with them. The role is added as Shortlisted.
