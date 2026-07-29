# Lab author checklist

## Learning design

- Name one audience and one decision the lab supports.
- Write the learning goal in terms of what the student can question, explain,
  or decide.
- Give students a starting prompt, not a sequence of code cells to copy.
- Ask for a hypothesis before showing analysis or model output.
- Add at least one point where the student must interpret evidence before the
  assistant continues.
- Make the deeper coding path optional and clearly labeled.

## Data

- Pin the source version and checksum.
- Record license or permission evidence.
- Remove direct identifiers and review linkable free-text fields.
- Describe units, missingness, and known selection effects.
- Keep private evaluation data and answer keys out of student skills.

## Assistant behavior

- Ask what decision the analysis will support.
- Use a small baseline before a more complicated model.
- Show the evidence used for every material claim.
- Distinguish observation, interpretation, and recommendation.
- Discuss errors, limitations, and what would change the conclusion.
- Do not provide a finished recommendation before the student responds to the
  evidence checkpoint.
- Do not paste code unless the student asks to see, modify, or debug it.

## Release checks

- Confirm every profile path exists.
- Run the repository tests.
- Try the evaluation prompts in `evals/evals.json`.
- Review the lab as a student who has never written Python.
- Review the optional path as a student who wants to inspect the code.
