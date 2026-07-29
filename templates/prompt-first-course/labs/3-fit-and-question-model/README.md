# Lab 3: fit and question a model

## Learning goal

Use a basic regression as evidence, compare it with a simple baseline, and
explain when its predictions should not be trusted.

## Start with this prompt

> Help me turn my business question into a simple price-prediction exercise.
> Ask me to define the target and what a useful prediction means. Start with a
> baseline, keep code hidden, and make me interpret the errors.

## Student work

1. Choose a numeric price target after checking its units and missing values.
2. Decide which fields would be available at prediction time.
3. Set aside a validation group before fitting the model.
4. Compare a median prediction with one basic linear regression.
5. Review overall error and at least two meaningful segments.
6. Identify leakage risks, failure cases, and whether the model improves the
   original business decision.

## Evidence checkpoint

Explain:

- whether the regression beats the baseline enough to matter;
- where errors are largest and who is affected;
- one feature that may be misleading or unavailable in practice;
- whether you would use the model, revise it, or reject it.

## Deliverable

Create `model-card.md` with the target, available features, validation method,
baseline, model result, segment errors, limits, and recommendation.

## Optional deeper coding

Ask OpenCode to show the preprocessing and model-fitting code. Change one
feature or validation choice, rerun it, and explain why the result changed.
