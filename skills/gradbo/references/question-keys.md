# Canonical question keys

Each recurring application question has one canonical key. Name answer files `answers/<key>.md` and facts `<key>` in `profile/facts.md` with these keys, so a question asked in new wording is found under the key it was filed under before. Add a new key only when no listed one fits; use lowercase dotted names (`preferences.notice_period`).

Columns: **input** is the answer shape; **when** says whether the question is about today (`current`), a future start date (`future_start`), either (`any_time`) or neither; **stakes** `high` means a statement of fact answered only from a verified fact; **scope** `employer` means the answer belongs to one employer (`answers/employers/<slug>.md`).

## `work.uk.right_to_work`

Do you currently have the right to work in the UK?

- input: yes_no; when: current; stakes: high
- Known wordings:
  - Do you have the right to work in the UK?
  - Do you have the legal right to work in the UK?
  - Are you legally eligible to work in the UK?
  - Are you legally authorised to work in the UK?
  - Are you authorized to work in the country in which you are applying?
  - Are you legally eligible to work in the country in which you are applying?
  - Are you legally entitled to work in the UK?
  - Do you currently have the right to work in the United Kingdom?

## `work.uk.requires_sponsorship`

Will you now or in the future need visa sponsorship to work in the UK?

- input: yes_no; when: any_time; stakes: high
- Known wordings:
  - Will you now or in the future require visa sponsorship to work in the UK?
  - Will you now or in the future require sponsorship for employment visa status?
  - Will you require visa sponsorship at any time?
  - Will you now or in future need visa sponsorship?
  - Visa sponsorship now or in the future

## `work.uk.start_date_eligibility`

Will you be eligible to work in the UK at the start date without sponsorship?

- input: yes_no; when: future_start; stakes: high
- Known wordings:
  - Will you have the right to work in the UK on your start date?
  - Will you be eligible to work in the UK when the programme starts?

## `work.uk.visa_type`

What is your UK right to work status or visa type?

- input: text; when: current; stakes: high
- Known wordings:
  - Please select your right to work status
  - What is your right to work status?
  - Right to work status
  - Please can you confirm your right to work status in the UK?
  - What type of visa do you hold?
  - Visa type
  - Immigration status

## `work.uk.visa_expiry`

When does your permission to work in the UK end? Give the month and year, or "no end date".

- input: text; when: current; stakes: high
- Known wordings:
  - When does your visa expire?
  - Visa expiry date
  - When does your current permission to work in the UK end?

## `preferences.notice_period`

What is your notice period?

- input: text
- Known wordings:
  - Notice period
  - What is your current notice period?
  - How much notice do you need to give your current employer?

## `preferences.available_from`

When can you start?

- input: text
- Known wordings:
  - Earliest start date
  - When are you available to start?
  - What is your earliest available start date?
  - Available from
  - When could you start?

## `preferences.salary_expectation`

What salary do you expect?

- input: text
- Known wordings:
  - What are your salary expectations?
  - Salary expectations
  - Expected salary
  - Desired salary
  - What is your expected starting salary amount in annual terms?
  - What are your base salary expectations in GBP?

## `employment.current_salary`

What is your current salary?

- input: text
- Known wordings:
  - Current salary
  - What is your current salary?
  - Current base salary
  - Current compensation

## `preferences.willing_to_relocate`

Are you willing to relocate for work?

- input: yes_no
- Known wordings:
  - Are you willing to relocate?
  - Are you open to relocation?
  - Would you relocate for this role?
  - Are you local or willing to relocate?

## `preferences.relocation_locations`

Which locations are you open to relocating to?

- input: text
- Known wordings:
  - Which locations are you open to relocating to?
  - Location Preference - Please mark each location you are open to relocating to.

## `preferences.office_locations`

Which office locations do you prefer, in order?

- input: text
- Known wordings:
  - What is your preferred office location?
  - Preferred office location
  - Preferred location
  - Which office would you like to be based in?

## `preferences.willing_to_travel`

Are you willing to travel for work?

- input: yes_no
- Known wordings:
  - Are you willing to travel?
  - Are you able to travel for work?
  - Willingness to travel

## `preferences.working_pattern`

Which working pattern do you want (full time, part time)?

- input: text
- Known wordings:
  - Are you looking for full time or part time work?
  - Working pattern
  - Preferred working hours

## `driving.full_licence`

Do you hold a full UK driving licence?

- input: yes_no
- Known wordings:
  - Do you have a full UK driving licence?
  - Do you hold a valid driving licence?
  - Full driving licence
  - Do you have a valid driver's license?

## `driving.vehicle_access`

Do you have access to a vehicle?

- input: yes_no
- Known wordings:
  - Do you have access to your own vehicle?
  - Do you have use of a car?
  - Do you have access to a car?

## `employer.previous_employment`

Have you worked for this employer before?

- input: yes_no; scope: employer
- Known wordings:
  - Have you previously worked for {employer}?
  - Have you worked with us before?
  - Have you ever been employed by {employer}?
  - Have you previously been employed by {employer}?
  - Are you a current or former employee of {employer}?

## `employer.relationship`

Are you related to, or in a close relationship with, anyone who works for this employer?

- input: yes_no; scope: employer
- Known wordings:
  - Do you have any relatives currently employed at {employer}?
  - Are you related to anyone who works for {employer}?
  - Relationship to a {employer} employee
  - Do you have a family member working at {employer}?

## `custom.employee_referral`

Were you referred by someone who works for this employer?

- input: yes_no; scope: employer
- Known wordings:
  - Were you referred by a current employee?
  - Employee referral
  - Were you referred to this position?

## `custom.non_compete_agreement`

Are you bound by a non-compete agreement or other restriction on your employment?

- input: yes_no
- Known wordings:
  - Are you subject to a non-compete agreement?
  - Have you signed or are you otherwise bound by any non-compete agreement?
  - Do you have any restrictive covenants?

## `custom.other_recruitment_processes`

Are you in other recruitment processes or holding other offers?

- input: text
- Known wordings:
  - Other processes/offers/timelines
  - Are you currently interviewing elsewhere?
  - Do you have any other offers?

## `application.source`

How did you hear about this role?

- input: text; administrative default: source
- Known wordings:
  - How did you hear about us?
  - How did you hear about this role?
  - Where did you first see this vacancy?
  - Please can you confirm the source that persuaded you to apply to {employer}?
  - Source type
  - Discovery source
  - Which platform did you use to find this job?
  - Recruitment source

## `preferences.communication_language`

Which language should employers write to you in?

- input: text; administrative default: language
- Known wordings:
  - Preferred language
  - Communication language
  - Preferred language of correspondence

## `preferences.contact_channel`

How should employers contact you?

- input: text; administrative default: contact_channel
- Known wordings:
  - Preferred contact method
  - Preferred method of contact
  - How would you like us to contact you?

## `demographics.sexual_orientation`

What is your sexual orientation?

- input: text
- Known wordings:
  - What is your sexual orientation?

## `demographics.transgender`

Is your gender identity the same as the sex you were registered at birth?

- input: text
- Known wordings:
  - Is your gender identity the same as the sex you were registered at birth?

## `demographics.gender`

What is your gender?

- input: text
- Known wordings:
  - What is your gender?

## `demographics.ethnicity`

What is your ethnicity?

- input: text
- Known wordings:
  - What is your ethnicity?

## `demographics.religion`

What is your religion or belief?

- input: text
- Known wordings:
  - What is your religion or belief?

## `demographics.disability`

Do you consider yourself to have a disability?

- input: text
- Known wordings:
  - Do you consider yourself to have a disability?

## `demographics.age_range`

Which age group are you in?

- input: text
- Known wordings:
  - Which age group are you in?

## `demographics.marital_status`

What is your marital status?

- input: text
- Known wordings:
  - What is your marital status?

## `demographics.veteran`

Have you served in the armed forces?

- input: text
- Known wordings:
  - Have you served in the armed forces?

## `demographics.caring_responsibilities`

Do you have caring responsibilities?

- input: text
- Known wordings:
  - Do you have caring responsibilities?

## `demographics.free_school_meals`

Were you eligible for free school meals?

- input: text
- Known wordings:
  - Were you eligible for free school meals?

## `demographics.first_generation_university`

Are you the first generation in your family to go to university?

- input: text
- Known wordings:
  - Are you the first generation in your family to go to university?

## `demographics.community_background`

What is your community background?

- input: text
- Known wordings:
  - What is your community background?

The `demographics.*` keys each hold one canonical fact, so the candidate's first answer serves every later employer's wording and option list. Answer them only from the stored fact.
