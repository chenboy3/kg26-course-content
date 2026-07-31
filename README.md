# KG26 course content

Shared lecture material, labs, dataset manifests, and OpenCode skills for the
KG26 AI and data science bootcamp.

## Start here

Use this repository if you are writing or testing student-visible lessons. It
does not contain competition answers, private scoring logic, platform secrets,
or a raw copy of the Mashina dataset.

| Repository | Owns |
|---|---|
| [`chenboy3/kg26-project`](https://github.com/chenboy3/kg26-project) | Cafe simulation data, project releases, the standalone course service, submissions, leaderboard, and private evaluation |
| This repository | Shared lessons, OpenCode skills, dataset manifests, student clients, and versioned bundles |
| [`jonathanzhang99/inklab`](https://github.com/jonathanzhang99/inklab) | Generic hosted OpenCode accounts, worker machines, persistent workspaces, and model access |

The current `kg26` manifest includes the Day 1 lesson, the
`/day-1-fetch-data` and `/submit-business-plan` skills, the dataset command,
and the course-service clients. The three-lab prompt-first template is an
author example; it is not yet part of the live `kg26` manifest.

### First local check

Requires Git and Python 3.12+. No Kaggle account or platform credentials are
needed for these checks:

```bash
git clone https://github.com/chenboy3/kg26-course-content.git
cd kg26-course-content

python3 -m unittest discover -s tests -v
bin/course-data list
bin/build-course-bundle \
  --ref HEAD \
  --output-dir /tmp/kg26-course-bundle-test
```

Success means the tests finish with `OK`, `course-data list` shows `mashina`,
and the bundle builder writes a `.tar.gz`, checksum, and manifest under
`/tmp/kg26-course-bundle-test`.

## Student workspace setup

Inklab does not install this course or need a KG26 database migration. From the
terminal in any persistent OpenCode workspace:

```bash
cd /data/workspace
git clone https://github.com/chenboy3/kg26-course-content.git kg26-course
cd kg26-course
python3 -m pip install -r requirements.txt
opencode
```

OpenCode discovers the checked-in `.opencode/skills` directory from this
workspace. The dataset and submission commands stay under `bin/`, so they do
not require system installation.

Before the first submission, configure the URL supplied by the mentor and enter
the team token at the hidden prompt:

```bash
bin/kg26-configure https://course.example
```

The command stores credentials in the gitignored `.kg26/config.json` with
owner-only permissions. `/submit-business-plan` reviews the team's artifact and
runs `bin/kg26-submit` only after the student confirms the file.

## Repository contract

`course-profile.json` is the versioned content manifest. Bundle builders and
local checks use it to:

1. identify `requirements.txt`;
2. list student commands under `bin/`;
3. list the OpenCode skills available in the workspace;
4. include the dataset manifest and released lesson directories.

The repository does not contain a raw copy of the Mashina dataset.

## Build an immutable course bundle

Build from a resolved commit so the artifact never includes uncommitted files:

```bash
git fetch origin main
bin/build-course-bundle \
  --ref "$(git rev-parse origin/main)" \
  --output-dir dist
```

The command validates `course-profile.json` and every referenced requirement,
command, skill, dataset manifest, and lesson before writing:

- a deterministic `.tar.gz` course bundle;
- a `.sha256` checksum file;
- a release manifest with the source commit and profile version.

After the bundle has a durable student-readable location, pass its HTTPS
directory URL to record the exact download location in the release metadata:

```bash
bin/build-course-bundle \
  --ref "$(git rev-parse origin/main)" \
  --output-dir dist \
  --base-url https://content.example/courses
```

Upload the bundle, checksum, manifest, and catalog file without renaming them.
They can be used for manual installation or archival verification. Inklab does
not read this catalog.

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

To exercise the real download, install the pinned CLI and authenticate it:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
source .venv/bin/activate
kaggle auth login

bin/course-data \
  --workspace ./workspace \
  fetch mashina \
  --accept-terms
```

The fetch command removes `License plate` and `VIN`, writes the cleaned CSV
under `workspace/data/mashina/`, and records source and output checksums. Keep
`workspace/` out of commits.

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

The unit tests do not download data or require secrets:

```bash
python3 -m unittest discover -s tests -v
```

After changing `course-profile.json`, a skill, lesson, command, requirement, or
dataset manifest, commit the candidate changes to a branch. The builder archives
the requested Git ref and intentionally ignores uncommitted files. Build that
commit twice and confirm the hashes match:

```bash
bin/build-course-bundle --ref HEAD --output-dir /tmp/kg26-bundle-a
bin/build-course-bundle --ref HEAD --output-dir /tmp/kg26-bundle-b
shasum -a 256 /tmp/kg26-bundle-a/*.tar.gz /tmp/kg26-bundle-b/*.tar.gz
```

## Current status

- [PR #1](https://github.com/chenboy3/kg26-course-content/pull/1) added the
  prompt-first Mashina lesson, fetch skill, dataset manifest, and reusable
  author template.
- [PR #2](https://github.com/chenboy3/kg26-course-content/pull/2) added the
  deterministic bundle builder and profile validation.
- The public
  [`course-bundle-d68f4ea`](https://github.com/chenboy3/kg26-course-content/releases/tag/course-bundle-d68f4ea)
  release contains `kg26` content version `2026.1` from merge commit
  `d68f4ea`.

The current candidate is content version `2026.2`. It adds self-service
workspace setup and the submission client but is not published yet. Before a
student rehearsal, attach the written Mashina redistribution permission and
publish a new immutable bundle. Never replace the `2026.1` release artifact in
place.
