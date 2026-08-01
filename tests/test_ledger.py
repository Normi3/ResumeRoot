from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from resumeroot.ledger import Ledger


class LedgerTests(unittest.TestCase):
    def test_records_provenance_without_artifact_contents(self) -> None:
        with TemporaryDirectory() as directory:
            ledger = Ledger(Path(directory) / "ledger.sqlite3")
            ledger.initialize()
            opportunity_id = ledger.record_opportunity("Example Co", "Analyst", "https://example.com/jobs/1")
            ledger.record_artifact(opportunity_id, "resume", "/private/resume.pdf", "v1")
            ledger.record_event(opportunity_id, "verified", "employer confirmation")
            ledger.record_exception("captcha", "Requires human completion", opportunity_id)
            self.assertEqual(
                ledger.counts(),
                {"opportunities": 1, "artifacts": 1, "application_events": 1, "exceptions": 1},
            )
