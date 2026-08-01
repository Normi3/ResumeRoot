"""Command-line interface for ResumeRoot's private local ledger."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from resumeroot.ledger import Ledger


def _workspace(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _ledger(workspace: Path) -> Ledger:
    ledger = Ledger(workspace / "ledger.sqlite3")
    ledger.initialize()
    return ledger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ResumeRoot local application-provenance ledger")
    parser.add_argument("--workspace", default=".resumeroot", type=_workspace, help="Private local workspace")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("init", help="Create the private local ledger")
    subcommands.add_parser("status", help="Show local ledger counts")
    subcommands.add_parser("doctor", help="Check ResumeRoot and executor availability")

    opportunity = subcommands.add_parser("record-opportunity", help="Record a discovered opportunity")
    opportunity.add_argument("--company", required=True)
    opportunity.add_argument("--role", required=True)
    opportunity.add_argument("--url", required=True)

    event = subcommands.add_parser("record-event", help="Record an application event")
    event.add_argument("--opportunity-id", type=int, required=True)
    event.add_argument("--status", required=True)
    event.add_argument("--signal")

    exception = subcommands.add_parser("record-exception", help="Record a blocking exception")
    exception.add_argument("--kind", required=True)
    exception.add_argument("--message", required=True)
    exception.add_argument("--opportunity-id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace: Path = args.workspace
    ledger = _ledger(workspace)

    if args.command == "init":
        print(f"Initialized private ResumeRoot workspace: {workspace}")
        return 0
    if args.command == "status":
        for name, count in ledger.counts().items():
            print(f"{name}: {count}")
        return 0
    if args.command == "doctor":
        applypilot = shutil.which("applypilot")
        print(f"workspace: {workspace}")
        print(f"applypilot: {applypilot or 'not found; run make bootstrap'}")
        return 0 if applypilot else 1
    if args.command == "record-opportunity":
        identifier = ledger.record_opportunity(args.company, args.role, args.url)
        print(f"Recorded opportunity {identifier}")
        return 0
    if args.command == "record-event":
        identifier = ledger.record_event(args.opportunity_id, args.status, args.signal)
        print(f"Recorded event {identifier}")
        return 0
    if args.command == "record-exception":
        identifier = ledger.record_exception(args.kind, args.message, args.opportunity_id)
        print(f"Recorded exception {identifier}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
