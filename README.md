# ResumeRoot

**A governed AI application operating system for truthful, job-specific applications.**

ResumeRoot turns a candidate's verified experience into role-specific application artifacts while preserving provenance, submission state, evidence, and exceptions. It is designed for candidates who want more than a resume generator: they need a durable operating layer for an active job search.

## Why it exists

Most application workflows collapse source facts, tailored claims, generated files, browser actions, and submission evidence into an untraceable sequence. ResumeRoot separates them.

It provides a repeatable workflow for:

- maintaining a private, evidence-backed master experience inventory;
- selecting supported claims for each target role;
- producing ATS-readable, job-specific resumes and optional letters;
- routing work across models with explicit cost and quality controls;
- recording every artifact, form answer, submission signal, and exception;
- requiring human resolution for missing facts, CAPTCHA, or unsupported claims; and
- preserving an auditable history of what was sent, where, and why.

## Core principles

1. **Evidence before optimization.** Tailoring strengthens a supported argument; it does not invent employment, credentials, results, or authorization.
2. **Private source of truth.** Master experience, contact information, and source documents remain local and are never committed.
3. **Artifact provenance.** Every submitted resume is retained with company, role, timestamp, source version, and submission status.
4. **Human authority at the edges.** CAPTCHAs, unknown screening answers, address gaps, and binding external actions are surfaced as exceptions rather than silently guessed.
5. **ATS without visual compromise.** Output uses an accessible, parsable single-column structure while maintaining deliberate one-page layout control.
6. **Observable execution.** Browser actions are verified with authoritative submission signals before an application is counted.

## Architecture

```text
Private experience inventory
        ↓
Evidence & claim registry ──→ Role fit / opportunity triage
        ↓                               ↓
Tailoring engine + ATS preflight ─→ Versioned resume artifacts
        ↓                               ↓
Application executor ────────→ Submission verification
        ↓                               ↓
Exception queue ←────────────── Application ledger / archive
```

## What this repository will contain

- a vendor-neutral application ledger and artifact schema;
- a claim/evidence registry for resume governance;
- ATS preflight rules and one-page document-output adapters;
- model-routing policies for quality, latency, and token economics;
- browser-execution contracts with explicit verification states;
- exception workflows for incomplete information and human-only checks; and
- import adapters for existing open-source tools.

## Relationship to ApplyPilot

ResumeRoot is being designed as a separate governance and artifact-preservation layer. It may integrate with [ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot) as an optional executor.

ApplyPilot is an AGPL-3.0 project created by Pickle-Pixel. Any future ResumeRoot code copied from, modified from, or distributed with ApplyPilot will preserve the required AGPL-3.0 licensing, copyright notices, and attribution. This repository will not present ApplyPilot's work as original ResumeRoot code.

## Status

Initial public architecture and interfaces are in development. The public repository will intentionally exclude resumes, application responses, API keys, personal contact details, company-specific submissions, private source documents, browser sessions, and any confidential materials.
