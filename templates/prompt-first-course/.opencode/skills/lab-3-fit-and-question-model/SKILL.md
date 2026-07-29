---
name: lab-3-fit-and-question-model
description: Guide a prompt-first basic regression lab using Mashina, including target definition, a validation split, a median baseline, linear regression, segment errors, leakage checks, and student interpretation. Use whenever a student asks to predict price, fit a model, compare performance, inspect errors, or decide whether a model is useful.
compatibility: opencode
metadata:
  audience: students
  course: prompt-first-template
  opencode/slash: "true"
---

# Lab 3: fit and question a model

Treat the model as evidence for a decision, not as an answer generator.

## Workflow

1. Read `question-brief.md` and `analysis.md`.
2. Ask the student to choose a numeric price target and define what level of
   prediction error would still be useful.
3. Review which features are available at prediction time. Exclude identifiers,
   direct target derivatives, post-outcome fields, and obvious leakage.
4. Set aside validation data before preprocessing or feature selection.
5. Fit a median baseline and one basic linear regression. Keep the first model
   simple enough to explain.
6. Report the validation metric in the target's units, the improvement over the
   baseline, and errors for at least two meaningful segments.
7. Show several large errors and ask the student what might explain them.
8. Ask whether the model is useful, needs revision, or should be rejected.
9. Save `model-card.md` with:
   - target and intended use;
   - available features;
   - validation method;
   - baseline and model result;
   - segment errors;
   - leakage risks and limits;
   - the student's recommendation.

Do not paste preprocessing or model code unless the student asks to see,
modify, or debug it. When they do, explain one step at a time and connect every
technical choice to the business question.

Do not search for a more complicated model until the student can explain the
baseline, the regression errors, and the main limitation.
