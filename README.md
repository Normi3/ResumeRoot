# ResumeRoot

**A governed AI application operating system, with a complete local executor.**

ResumeRoot combines a private application ledger with a vendored, runnable copy of [ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot). It separates supported candidate facts, tailored artifacts, application events, verification signals, and exceptions so a job search is inspectable rather than a pile of browser tabs and untraceable uploads.

## What is in this repository

| Component | Purpose |
| --- | --- |
| `src/resumeroot/` | Local-first application ledger and command-line interface. |
| `vendor/applypilot/` | Full upstream ApplyPilot executor: discovery, enrichment, scoring, tailoring, PDF generation, and browser-driven application workflow. |
| `scripts/bootstrap.sh` | One-command local environment setup. |
| `tests/` | Regression tests for the ResumeRoot ledger. |
| `ARCHITECTURE.md` | Domain model, state machine, and integration contract. |
| `THIRD_PARTY_NOTICES.md` | Upstream attribution, provenance, and license information. |

No candidate-specific content is committed: resumes, contact details, API keys, browser sessions, application responses, submission records, and source documents remain private and are ignored by Git.

## Quick start

Requirements for the full pipeline: Python 3.11+, Node.js 18+, Chrome/Chromium, a Gemini/OpenAI/local-model configuration for scoring and tailoring, and Codex CLI or Claude Code for browser execution. The executor checks dependencies before use.

```bash
git clone https://github.com/Normi3/ResumeRoot.git
cd ResumeRoot
make bootstrap
make init
make doctor
```

`make init` starts ApplyPilot's local setup wizard. Enter private information only into the local files it creates; never commit them.

Run the workflow in a safe preview mode first:

```bash
make run ARGS="--dry-run"
make apply ARGS="--dry-run --daily-limit 25"
```

For direct executor access:

```bash
.venv/bin/applypilot doctor
.venv/bin/applypilot run --dry-run
.venv/bin/applypilot apply --agent codex --dry-run --daily-limit 25
.venv/bin/applypilot apply --agent claude --dry-run --daily-limit 25
```

## Browser-agent support

The application executor supports two non-interactive browser agents:

- **Codex CLI** — `--agent codex` (the default); launches `codex exec` with an isolated Playwright MCP connection to the dedicated Chrome worker.
- **Claude Code** — `--agent claude`; launches Claude Code with the same isolated browser connection.

Both require Chrome/Chromium and Node.js (`npx`) for the Playwright MCP server. The `doctor` command reports whether each agent is available. Agent-specific models can be selected with `--model`; omit it to use the agent default.

For a human/browser handoff, generate the per-job prompt with `applypilot apply --gen --url <job-url>` and complete the site manually. Unsupported agent names fail before a browser workflow starts.

## ResumeRoot ledger

The ledger is deliberately small and local. It records opportunities, generated artifacts, execution events, and blocking exceptions in `.resumeroot/ledger.sqlite3` (which is ignored by Git).

```bash
.venv/bin/resumeroot init
.venv/bin/resumeroot record-opportunity --company "Example Co" --role "Analyst" --url "https://example.com/job"
.venv/bin/resumeroot status
```

Use it to preserve the evidence trail around the executor—not to store information in the public repository.

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

See [ARCHITECTURE.md](ARCHITECTURE.md) for the state model and adapter contract.

## Attribution and license

The executor in `vendor/applypilot/` is a clean vendored snapshot of ApplyPilot, created by Pickle-Pixel, and is licensed under the GNU Affero General Public License v3.0. Its source, license, notices, and attribution remain intact. To keep the complete runnable distribution unambiguous, ResumeRoot is also released under AGPL-3.0. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE](LICENSE).

If you modify, distribute, or deploy the vendored ApplyPilot component, follow its AGPL-3.0 obligations, including the corresponding-source and network-use provisions.
