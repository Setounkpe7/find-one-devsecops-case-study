# find-one-devsecops-case-study

A case study of the DevSecOps controls I built around [Find-One](https://github.com/Setounkpe7/Find-One), a FastAPI + React job-application tracker.

## What's inside

- **`REPORT.md`** is the case study. It covers the threat model, tool selection and rationale, pipeline architecture, three deep-dives on the non-obvious decisions (authenticated DAST, per-tool blocking rules, secrets defense in depth), operational artifacts, and a what's-not-done-yet section.
- **`artifacts/`** contains the real files from the source project: the GitHub Actions workflow, pre-commit config, Dependabot config, the ZAP auth hook, a fresh SPDX 2.3 SBOM, the rollback runbook, and redacted JSON outputs from every scanner in the pipeline.
- **`screenshots/`** has seven captures from live pipeline runs on Find-One: the CI run overview, the security-scans job detail, ZAP output in context, the artifacts download panel, a Dependabot state, a local pre-commit block, and an SBOM excerpt.

## Context

Find-One is a personal project, public on GitHub. The DevSecOps side of it grew out of the [Practical DevSecOps Certified DevSecOps Professional](https://www.practical-devsecops.com/certified-devsecops-professional/) coursework I completed in early 2026. This repo documents what I built and why I made the choices I made.

