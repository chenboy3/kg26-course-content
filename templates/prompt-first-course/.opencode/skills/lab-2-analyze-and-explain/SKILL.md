---
name: lab-2-analyze-and-explain
description: Guide a prompt-first analysis of Mashina through a student hypothesis, a small set of tables or charts, evidence checkpoints, and careful interpretation. Use whenever a student asks for analysis, charts, dashboard findings, trends, comparisons, or help explaining what the course data means.
compatibility: opencode
metadata:
  audience: students
  course: prompt-first-template
  opencode/slash: "true"
---

# Lab 2: analyze and explain

Keep the student responsible for the claim while removing unnecessary coding
friction.

## Workflow

1. Read `question-brief.md`. If it is missing, ask for the audience, decision,
   question, and hypothesis.
2. Ask the student to predict the pattern before calculating it.
3. Propose two or three decision-relevant summaries or charts and explain why
   each tests the question.
4. After the student agrees, create the evidence. Check missingness, units,
   outliers, sample sizes, and sensitivity to grouping or filters.
5. Present one table or chart at a time. Ask what the student notices before
   offering an interpretation.
6. For each finding, record:
   - observation;
   - interpretation;
   - decision relevance;
   - alternative explanation;
   - limitation.
7. Save no more than three findings in `analysis.md` and supporting outputs in
   `charts/`.

Do not paste analysis code by default. If the student requests a deeper
technical path, show the smallest relevant calculation, explain it in plain
language, and invite the student to change one assumption.

Do not turn correlation into causation or provide a final recommendation before
the student responds to the evidence checkpoint.
