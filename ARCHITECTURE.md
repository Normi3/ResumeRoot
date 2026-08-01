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
