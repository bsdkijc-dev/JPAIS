import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import stage8_rag_eval
import stage9_reg_drafting
import stage10_security_audit


class TestJPAISStages8To10(unittest.TestCase):
    def test_stage8_offline_eval_no_critical_failures(self):
        # Ensure data dir points to jpais_stages_1_4
        res = stage8_rag_eval.run_evaluation(use_ollama=False)
        self.assertEqual(res["total_tests"], 10)
        self.assertEqual(res["critical_failures"], 0)
        self.assertEqual(res["passed"], 10)

    def test_stage9_conflict_and_human_review(self):
        clauses = [
            {"clause_id": "P1", "instrument_type": "PERMA", "text": "Valid", "supporting_doc_ids": ["JPAIS-SYN-2026-000001"], "overrides_higher_norm": None},
            {"clause_id": "P2", "instrument_type": "PERMA", "text": "Bad", "supporting_doc_ids": [], "overrides_higher_norm": "UU PDP"},
        ]
        pkg = stage9_reg_drafting.create_draft_package("Test Draft", "PERMA", clauses, HERE / "test_history.jsonl")
        self.assertTrue(pkg["human_review_required"])
        self.assertEqual(len(pkg["conflict_findings"]), 2)
        (HERE / "test_history.jsonl").unlink(missing_ok=True)

    def test_stage10_security_audit(self):
        rep = stage10_security_audit.run_security_audit()
        self.assertEqual(rep["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
