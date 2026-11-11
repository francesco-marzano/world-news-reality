# eval

Hand-labelled samples used to measure the pipeline: duplicates, story clustering, story
location, the sport filter, translations and blind spots. The samples and their thresholds
are described in `docs/architecture.md`, section 16.

The folder is empty for now. The first sample (300 labelled pairs for duplicate
detection) arrives with milestone M3.

Rules:

- Labels are written by a person, with the instructions that will live in this folder.
- Assistants read these files and never edit them. A change here is a level 2 change.
- Results of evaluation runs go in `eval/results/` as new files, with date and commit.
