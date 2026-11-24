import unittest
from fastapi.testclient import TestClient
from jdss_app import app

client = TestClient(app)


class TestJDSSv1(unittest.TestCase):
    def test_health(self):
        r = client.get("/health")
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertEqual(d["cases_loaded"], 15)
        self.assertEqual(d["kg_edges_loaded"], 42)

    def test_search_by_regulation_and_keyword(self):
        r = client.get("/search", params={"q": "mediation", "regulation": "PERMA No. 1 Tahun 2016"})
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertGreaterEqual(d["count"], 1)
        self.assertEqual(d["results"][0]["doc_id"], "JPAIS-SYN-2026-000001")
        self.assertGreaterEqual(len(d["results"][0]["kg_relationships"]), 2)

    def test_case_lookup(self):
        r = client.get("/cases/JPAIS-SYN-2026-000015")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()["kg_relationships"]), 4)


if __name__ == "__main__":
    unittest.main()
