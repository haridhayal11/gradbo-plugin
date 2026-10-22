# Answering form questions

Decide each field with the cheapest source that settles it, in this order. Note the source of every value in `application-notes.md`; the receipt needs it.

## 1. Facts the field asks for directly

Name, email, phone, address, links, education and experience entries: take them from `profile/facts.md`. Format to the field (a phone field with a separate country code, a month picker, a dropdown of universities), but don't change the substance.

## 2. Questions you have seen before

Match the question to a canonical key in [question-keys.md](question-keys.md) by meaning, not by exact words; the known wordings there show the range. Then use, in order:

1. `answers/employers/<slug>.md` for this employer (and any `job:<id>` block for this role)
2. `answers/<key>.md`
3. the fact with that key in `profile/facts.md`

A dropdown or radio group: choose the option that says the same thing as the stored answer.

## 3. Statements of fact

Right to work, sponsorship, criminal convictions, age, disability, relatives at the company, previous employment there, and every key marked `stakes: high` are statements of fact.

- Answer only from a `verified` fact whose time frame matches. "Do you **currently** have the right to work" is about today; "will you have it **at the start date**" is about `preferences.available_from`; "now **or in the future**" covers both. A fact with a passed `valid until` is stale; don't use it.
- Read the polarity. "Will you require sponsorship?" with a candidate who needs it is **Yes**; "Are you eligible to work without sponsorship?" is then **No**. Read the question twice before choosing.
- If no fact fits, ask the candidate (see "Outcomes" below).

## 4. Low-stakes administrative questions

Answer these with sensible defaults without asking, and list them separately in the receipt as defaults:

- **How did you hear about us / source:** the employer's careers website if offered; otherwise a neutral online option ("Job board", "Online", "Other"). Never invent a referral or a named person.
- **Preferred contact method or language:** email; English.
- **Where would you like to work** (when the advert's location is fixed): the advert's location.

## 5. Free-text questions

Motivation, competency and "tell us about a time" questions:

1. Check `answers/` for one you can reuse or adapt; an employer-specific question ("Why us?") always needs this employer's specifics.
2. Otherwise draft one from verified evidence: the facts, the CV, and the advert for the employer and role. Use real examples only, with no invented situations, numbers or outcomes. Keep within the word or character limit.
3. Run the writing pass ([humanizer.md](humanizer.md), or the `humanizer` skill if installed).
4. Save it to `answers/` as `status: draft, origin: assisted`, or in the employer file if it only fits this employer.

If the question needs an example the evidence doesn't have, ask the candidate for one rather than writing around the gap.

## Outcomes when you can't answer

Keep these apart; each needs a different question to the candidate:

- **Missing:** no fact covers it ("What is your notice period?"). Ask for the fact, record it in `facts.md` with its source, then answer.
- **Uncertain match:** a fact might cover it but the wording or time frame doesn't clearly fit. Ask whether the fact applies, quoting the question.
- **Unmatched option:** the fact is known but no option clearly presents it (the options don't include the candidate's degree subject). Show the candidate the options and ask which one.

Batch your questions: work through the whole page or form first, then ask everything at once, so the candidate answers once. Never ask again for a fact that is already verified.
