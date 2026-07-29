# KG26 course content

Shared lecture material, labs, dataset manifests, and OpenCode skills for the
KG26 AI and data science bootcamp.

This repository is separate from:

- `chenboy3/kg26-project`, which owns the competition simulation, project
  releases, submissions, and evaluation;
- `jonathanzhang99/inklab`, which owns generic OpenCode provisioning and the
  course-profile installer.

## Repository contract

`course-profile.json` is the installation contract for Inklab. A course-profile
installer should:

1. install `requirements.txt` in the student runtime;
2. expose `bin/course-data` as the `course-data` command;
3. install the listed OpenCode skills into the student workspace;
4. make the dataset manifest and lesson directories available read-only.

The repository does not contain a raw copy of the Mashina dataset.

## Mashina dataset

The Day 1 lab uses version 1 of
`vinnyg110g/mashina-kyrgyzstan-dataset`. The manifest pins the source file
checksum. `course-data` removes `License plate` and `VIN` before writing the
student CSV and records the source, transformation, row count, columns, and
output checksum in a release manifest.

Course organizers believe they have permission for course use. Link the written
permission and confirm that it covers redistribution to student instances
before serving a centrally hosted snapshot. Until then, use the pinned Kaggle
download path and do not commit or bake the raw CSV into an image.

## Prompt-first template course

[`templates/prompt-first-course`](templates/prompt-first-course) is a small
example for instructors creating new labs. It uses Mashina across three steps:

1. fetch the dataset and frame a business question;
2. analyze evidence and explain what it supports;
3. fit a basic regression model and question its errors.

Each lab has a matching OpenCode skill. The default path keeps students at the
prompt and interpretation level. Students can ask for the calculations or code
when they want a deeper technical path.

The template includes an example course profile, author checklist, rubric, and
evaluation prompts. Copy the structure, then replace the learning goal,
dataset, expected artifacts, and decision context.

## Local verification

Create a virtual environment, install the pinned dependency, and run the tests:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests
```

List the available datasets:

```bash
bin/course-data list
```

Fetch Mashina into a test workspace after reviewing the source terms:

```bash
bin/course-data \
  --workspace ./workspace \
  fetch mashina \
  --accept-terms
```
