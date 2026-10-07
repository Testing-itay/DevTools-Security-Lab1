---
name: ci-failure-triage
description: Triage a failing CI job. Use when a pipeline run fails and you need to tell a real regression from a flaky test or an infra problem.
---

# CI failure triage

1. Open the failing job log and find the first error, not the last one.
2. Re-run only the failing job once. If it passes, mark the test as flaky and
   link the two run IDs in the PR.
3. If it fails again, check whether `main` fails the same way. If it does, the
   break is not from this PR.
4. Otherwise, bisect the PR's commits and name the commit that breaks the job.
