# Third-Party Notices

## ApplyPilot

This repository contains `vendor/applypilot/`, a clean vendored snapshot of [Pickle-Pixel/ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot), retrieved from its public `main` branch on 2026-08-01.

- Copyright: Pickle-Pixel and ApplyPilot contributors.
- License: GNU Affero General Public License v3.0 only (AGPL-3.0-only).
- Original repository: <https://github.com/Pickle-Pixel/ApplyPilot>
- Upstream license text: [`vendor/applypilot/LICENSE`](vendor/applypilot/LICENSE)

The vendored directory is included so a clone of ResumeRoot contains the full application executor. ResumeRoot does not represent ApplyPilot's discovery, enrichment, scoring, tailoring, PDF, or browser-automation implementation as original work. Root-level ResumeRoot code is an independent local ledger and orchestration layer; it does not alter the vendored source.

ResumeRoot applies a documented local patch to the vendored executor so its `--agent codex` and `--agent claude` modes genuinely select the corresponding CLI, check the matching dependencies, use dedicated browser worker profiles, and write agent usage metadata. These are ResumeRoot modifications dated 2026-08-01; they are not represented as upstream ApplyPilot behavior.

To avoid ambiguity for a complete runnable distribution, the repository as a whole is released under AGPL-3.0. Any distribution, modification, or network deployment must comply with that license, including preserving notices and providing corresponding source where required.
