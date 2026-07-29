---
name: lab-1-fetch-and-frame
description: Start a prompt-first data lab by fetching Mashina, inspecting its source and quality, and helping the student define an audience, decision, question, and hypothesis. Use whenever a student asks to load the course data, explore it, choose a project question, or begin the template course.
compatibility: opencode
metadata:
  audience: students
  course: prompt-first-template
  opencode/slash: "true"
---

# Lab 1: fetch and frame

Help the student choose what the analysis is for before producing results.

## Workflow

1. Ask who will use the analysis and what decision they need to make.
2. Ask what the student currently believes and what evidence might change that
   belief.
3. Run `course-data list`, then ask for confirmation before running:

   ```bash
   course-data fetch mashina --accept-terms
   ```

4. Read `data/mashina/manifest.json`. Report the source version, row count,
   columns, removed identifiers, and checksum.
5. Inspect schema, units, missingness, duplicates, category frequencies, and
   suspicious values.
6. Present a compact data-quality table. Ask the student what concerns them
   before suggesting a final question.
7. Help the student write `question-brief.md` with:
   - audience and decision;
   - question and hypothesis;
   - useful fields;
   - main limitation;
   - evidence that would change the hypothesis.

Use tools to perform checks without pasting code. Show and explain the code only
when the student asks to inspect, modify, or debug it.

Do not choose the business question or provide a final conclusion on the
student's behalf.
