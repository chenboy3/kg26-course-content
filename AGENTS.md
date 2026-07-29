# KG26 course-content instructions

This repository contains student-visible lecture material, labs, dataset
manifests, and OpenCode skills shared across KG26 projects.

- Do not add project simulation rules, hidden evaluation data, scoring code, or
  provider credentials.
- Do not commit raw source datasets. Fetch them from a version-pinned source and
  record checksums and transformations.
- Remove direct identifiers before a dataset reaches a student workspace.
- Keep the `course-profile.json` paths valid and covered by tests.
- Keep skills prompt-first. Students should form a question, inspect evidence,
  and explain conclusions instead of receiving a finished answer.
