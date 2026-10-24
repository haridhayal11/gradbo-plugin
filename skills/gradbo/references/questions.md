# Answering form questions

Gradbo answers the questions; you read the page, fill it in, and fill the gaps with the candidate.

## 1. Send the whole page

Read the page's structure, then call `answer_questions(job_id=..., questions=[...])` with every question on it at once:

```json
[{"id": "q1", "label": "Will you now or in the future require visa sponsorship?", "options": ["Yes", "No"], "type": "yes_no", "section": "Eligibility"},
 {"id": "q2", "label": "How did you hear about this role?", "options": ["Referral", "Company website", "Other"]},
 {"id": "q3", "label": "Why do you want to join Graphcore?", "type": "long_text", "help": "Max 250 words"}]
```

`id` is your own reference to the field. Give the label as shown, the visible options for choice fields (not "Select one"), the page section, and any hint text. Identity and contact fields (name, email, phone, address, links, education and experience entries) go in the same call; each has its fact key.

## 2. Act on each answer's status

| Status | Do |
|---|---|
| `answered` | Fill `option` for a choice field, otherwise `value`. Format to the field (a phone field with a separate country code, a month picker) without changing the substance. |
| `confirm` | A likely reading Gradbo hasn't settled (a yes/no question matched by similarity, or a high-stakes key). Check that the question asks what `key` means and that Yes reads the same way; then fill it and `remember_question(wording, key, polarity, confirmed=True)`. If it doesn't fit, treat it as `uncertain_match`. |
| `missing_fact` | Gradbo has no fact for it. Ask the candidate `question` (see "Asking", below). |
| `uncertain_match` | The wording might ask for one of `candidates`. Decide which, by meaning and time frame (now, at the start date, or ever). Then answer from that fact and `remember_question(wording, key, polarity)`. If you can't tell, ask the candidate, quoting the question. |
| `unknown_question` | Gradbo doesn't know this question. Choose the fact key it asks for: one of the usual keys (`get_profile` shows what is held), or a new lowercase dotted key (`custom.non_compete_agreement`). Then `remember_question` and answer, or ask if the candidate's answer isn't held. |
| `unmatched_option` | The stored `value` isn't among the options. Show the candidate the options and ask which one; save their choice with `save_answer(key, question, answer, scope="employer:<slug>")` if it only fits this employer. |
| `reuse` | A free-text question with stored `answers` close to it. Adapt the nearest to this employer and role (an employer-specific question always needs this employer's specifics), then `save_answer`. |
| `draft` | A free-text question with nothing stored. Draft it from verified evidence (the facts, the CV, the advert), within the limit, with real examples only. Run it through the `humanizer` skill, fill it, then `save_answer(..., status="draft", origin="assisted", uses_facts=[...])`, with `scope="employer:<slug>"` when it only fits this employer. If it needs an example the evidence doesn't have, ask the candidate for one rather than writing around the gap. |

Record every value with its `source` in the application's progress (`save_application(job_id, progress=...)`); the receipt needs it.

## 3. Asking

Work through the whole page or form first, then ask everything at once, so the candidate answers once (`ask_candidate` lists the missing facts). Save each answer with `save_fact(key, value, source="candidate", source_ref="told the agent on <date>")` as soon as the candidate gives it, before you carry on. The next form finds it and never asks again.

Keep the outcomes apart; each needs a different question:
- **Missing:** "What is your notice period?"
- **Uncertain match:** whether a fact applies, quoting the employer's question.
- **Unmatched option:** the options, and which one says their answer.

Never ask for a fact Gradbo already answered.

## Statements of fact

Right to work, sponsorship, criminal convictions, age as a condition ("Are you over 18?"), disability when it asks about adjustments, relatives at the company, and previous employment there are statements of fact. Answer them only from a verified fact whose time frame fits, and read the polarity: "Will you require sponsorship?" with a candidate who needs it is **Yes**, while "Are you eligible to work without sponsorship?" is then **No**. `answer_questions` reads UK work-rights wording by code; when it can't settle one, it says so. Then read the question twice, and ask the candidate if it is still unclear.

## Equal-opportunities and diversity questions

Gender, ethnicity, sexual orientation, religion, disability monitoring, age range, background and the like follow two things:
- the candidate's standing choice, the `demographics.choice` fact (`answer from facts` or `prefer not to say`);
- their consent in Settings > Your data. Without consent, Gradbo keeps none of these answers and the form gets "Prefer not to say".

`answer_questions` applies both, so fill what it returns and never ask about these during an application. If it notes that `demographics.choice` is missing, ask the candidate once after the application how they want these answered, and save the choice. If they want them answered, tell them to allow it in Settings > Your data; then save each answer they give with `save_fact`.

## Low-stakes administrative questions

How they heard about the role, preferred contact method and language: `answer_questions` answers these with the standing defaults (the employer's careers website, or a neutral online option; email; English). Fill them without asking, and list them as defaults in the receipt. Never invent a referral or a named person. Where the advert's location is fixed, "Where would you like to work" is that location.
