---
name: submit-business-plan
description: Review and submit the team's current Cafe Sim business plan to the KG26 course service.
compatibility: opencode
metadata:
  audience: students
  course: kg26
  opencode/slash: "true"
---

# Submit the business plan

Use this skill when a student wants to submit or revise a Cafe Sim strategy.
The course service records each changed artifact and freezes the latest accepted
revision at the cutoff.

## Before sending

1. Ask which JSON file the team intends to submit.
2. Read the file and show a short checklist:
   - team and day;
   - decisions that are active for the day;
   - predicted profit and 80% interval;
   - the evidence named in the rationale;
   - assumptions or risks the team wants to keep.
3. Point out missing or inconsistent fields, but do not replace the team's
   judgment with a finished strategy.
4. Ask the student to confirm the exact file.

## Send

After confirmation, run:

```bash
bin/kg26-submit path/to/submission.json
```

If the client says the workspace is not configured, ask the student to open the
terminal and run:

```bash
bin/kg26-configure https://course-url-given-by-your-mentor
```

The command prompts for the team token without echoing it and stores it in the
gitignored `.kg26/config.json` file with owner-only permissions. Never print the
token or put it into the artifact, chat, command arguments, or a committed file.
`KG26_COURSE_URL` and `KG26_TEAM_TOKEN` environment variables remain available
as temporary overrides.

The client derives a stable request key from the server release and canonical
artifact. Retrying the same artifact returns the original receipt. Changing the
artifact creates a new request key and a new revision.

## After sending

1. Report the submission ID, revision, receipt time, artifact hash, validation
   status, and any adjustment notes.
2. State clearly that the receipt contains no hidden score or profit.
3. Give the saved receipt path under `.kg26/receipts/`.
4. If the team changes its reasoning or decisions, repeat the review and submit
   the revised file. Do not overwrite prior receipts.
