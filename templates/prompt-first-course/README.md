# Prompt-first course template

Use this directory as a working example when creating a short data lab. It
assumes the repository already provides the `course-data` command and a
version-pinned Mashina manifest.

The course has three labs:

1. Fetch and frame. Load the data, choose an audience, and turn curiosity into
   a decision-oriented question.
2. Analyze and explain. Inspect quality, build a small evidence set, and
   separate observation from interpretation.
3. Fit and question a model. Compare a basic regression with a baseline, inspect
   errors, and decide whether the model is useful.

## Student experience

Students should spend most of their time writing good prompts, choosing
questions, inspecting evidence, and explaining conclusions.

The OpenCode assistant may run calculations behind the scenes, but it should
not paste code by default. When a student asks to see or change the code, the
assistant can expose the relevant steps and explain them in plain language.

Every lab follows the same rhythm:

```text
student question
  -> clarify the intended decision
  -> ask for a hypothesis
  -> produce a small evidence set
  -> ask the student what they notice
  -> discuss limits and revise the claim
```

## Reusing the template

1. Copy the three lab and skill directories.
2. Rename the skill names and update their frontmatter descriptions.
3. Replace Mashina with a version-pinned dataset manifest.
4. Update `course-profile.json` using `course-profile.example.json`.
5. Adapt the rubric to the learning goal without making code volume a proxy for
   understanding.
6. Test the skills with the prompts in `evals/evals.json`, especially the
   prompts that ask the assistant to do all the thinking.

Use [author-checklist.md](author-checklist.md) before publishing and
[rubric.md](rubric.md) when reviewing student work.
