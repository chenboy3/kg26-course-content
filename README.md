# KG26 course content

Shared lecture material, labs, dataset manifests, and OpenCode skills for the
KG26 AI and data science bootcamp.

## Start here

Use this repository if you are writing or testing student-visible lessons. It
does not contain competition answers, private scoring logic, platform secrets,
or a raw copy of the Mashina dataset.

| Repository | Owns |
|---|---|
| [`chenboy3/kg26-project`](https://github.com/chenboy3/kg26-project) | Cafe simulation data, project releases, submissions, and private evaluation |
| This repository | Shared lessons, OpenCode skills, dataset manifests, course profiles, and versioned bundles |
| [`jonathanzhang99/inklab`](https://github.com/jonathanzhang99/inklab) | Hosted OpenCode accounts, worker machines, and course-profile installation |

The current `kg26` profile installs the Day 1 lesson, the
`/day-1-fetch-data` skill, and the `course-data` command. The three-lab
prompt-first template is an author example; it is not yet installed by the
live `kg26` profile.

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

## Repository contract

`course-profile.json` is the installation contract for Inklab. A course-profile
installer should:

1. install `requirements.txt` in the student runtime;
2. expose `bin/course-data` as the `course-data` command;
3. install the listed OpenCode skills into the student workspace;
4. make the dataset manifest and lesson directories available read-only.

The repository does not contain a raw copy of the Mashina dataset.

## Build an Inklab course bundle

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
directory URL to produce the gateway catalog entry:

```bash
bin/build-course-bundle \
  --ref "$(git rev-parse origin/main)" \
  --output-dir dist \
  --base-url https://content.example/courses
```

The resulting `.catalog.json` file is the value for Inklab's
`COURSE_PROFILES_JSON`. Upload the matching bundle without renaming it, then
configure the gateway with that catalog and the desired
`DEFAULT_COURSE_PROFILE`.

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

Before a student rehearsal, add the remaining daily lessons and skills, attach
the written Mashina redistribution permission, and publish a new immutable
bundle when the profile changes. Never replace an existing release artifact in
place.
