# Submission notes: HackerRank Orchestrate, October 2026 ("Ghost Data Still Exists")

- Built overnight on 24-25 Oct 2026 with Claude Code as an AI pair programmer.
- Live leaderboard: total 35.8/100 (transcript 3.7, interview 8.7, output 8.7, code 14.7), rank ~1,339 of 2,612.
- **Lesson learned:** the submitted `output.csv` sorted `case_id` as text (`case_100` before `case_33`), while the input
  and the expected answers use numeric order. The answers were the same, but the order was not. That most likely
  explains the low output score despite 100% status accuracy on the labelled samples. This folder contains the fixed
  code (natural case order) and `output.csv` in input order; the answers are identical to the submission.
- The challenge dataset is not included; it is public at
  https://github.com/interviewstreet/hackerrank-orchestrate-october26 (place it in `dataset/` to run).
