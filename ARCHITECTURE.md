# ResumeRoot Architecture Notes

## Domain model

| Entity | Purpose |
| --- | --- |
| `experience_source` | Private source material and factual experience records. |
| `claim` | A concise, externally usable statement tied to evidence and a confidence level. |
| `opportunity` | A job posting, role requirements, fit assessment, and execution status. |
| `artifact` | A versioned resume, letter, or supporting document generated for an opportunity. |
| `application_event` | A timestamped action or authoritative verification signal. |
| `exception` | A blocking unknown, human-only check, or conflict requiring resolution. |
| `policy` | Rules for claim support, model routing, cost ceilings, output format, and submission criteria. |

## Application state machine

```text
discovered → enriched → evaluated → tailored → ready
                                      ↓
                              exception_required
ready → form_in_progress → submitted → verified
                         ↘ failed / abandoned
```

`submitted` is not sufficient for reporting. A role becomes `verified` only when an authoritative employer or platform signal confirms that the application was received.

## Public-safe boundary

The public project contains schemas, policies, adapters, tests, and synthetic fixtures only. It excludes all candidate-specific data and any artifacts generated from real applications.

## Integration contract

Execution adapters should return structured outcomes rather than prose:

```json
{
  "status": "verified | submitted | exception_required | failed",
  "verification_signal": "string or null",
  "artifact_ids": ["..."],
  "exception": {"kind": "...", "message": "..."}
}
```

This makes a third-party executor replaceable and prevents a workflow from claiming success based on an unverified click.

## Browser-agent execution contract

ResumeRoot's vendored executor supports the following modes:

| Mode | Invocation | Browser boundary |
| --- | --- | --- |
| Codex CLI | `applypilot apply --agent codex` | `codex exec` receives only an isolated Playwright MCP server connected to a dedicated Chrome worker. |
| Claude Code | `applypilot apply --agent claude` | Claude Code receives the same isolated Playwright MCP configuration. |
| Human handoff | `applypilot apply --gen --url <job-url>` | A job-specific prompt is generated for manual completion; it is not reported as submitted. |

An executor must be selected explicitly from `codex` or `claude`; unsupported names fail before browser work begins. Both automated modes require a locally installed Chrome/Chromium, Node.js (`npx`) for the Playwright MCP server, and the matching CLI on `PATH`. The worker profile is dedicated to the job-search system; it is never cloned from a user's ordinary browser profile.

Executor output is parsed into an `application_event`. A successful click alone is insufficient: the system should record `verified` only after an authoritative employer or platform confirmation signal is available. CAPTCHA, login, missing-fact, and unsupported-flow outcomes become exceptions for human resolution.
