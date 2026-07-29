---
name: day-1-fetch-data
description: Fetch and verify the KG26 Mashina vehicle dataset, then guide an initial evidence-first inspection.
compatibility: opencode
metadata:
  audience: students
  course: kg26
  opencode/slash: "true"
---

# Day 1 data fetch

Use this skill when a student asks to load the shared Mashina vehicle dataset
or begin the Day 1 dashboard exercise.

## Fetch

1. Run `course-data list` to show the available course datasets.
2. Explain that the installer downloads the pinned Mashina version from Kaggle,
   verifies its checksum, and removes `License plate` and `VIN`.
3. Ask the student to confirm before downloading from the source.
4. After confirmation, run:

   ```bash
   course-data fetch mashina --accept-terms
   ```

5. Read `data/mashina/manifest.json` and report the source version, row count,
   removed columns, and output checksum.

Do not use `webfetch`, `curl`, or an unpinned Kaggle URL as a substitute.

## Initial inspection

Load `data/mashina/mashina.csv`, then help the student:

1. State the business question and intended dashboard audience.
2. Inspect columns, units, missingness, duplicates, and category frequencies.
3. Identify fields that need parsing, such as prices, mileage, engine size, and
   power.
4. Produce at least one table and one chart before suggesting a conclusion.
5. Separate observed evidence from interpretation and recommendation.

Do not provide a finished business conclusion before the student has reviewed
the supporting table or chart.
