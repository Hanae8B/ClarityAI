# tests/test_explanation_engine.py
import unittest
import logging
from src.explanation_engine import ExplanationEngine

logging.basicConfig(level="WARNING")
logger = logging.getLogger(__name__)

class TestExplanationEngine(unittest.TestCase):
    def setUp(self):
        # Use the default CSV paths configured in src/config.py
        self.engine = ExplanationEngine()
        # Ensure the engine has at least some keywords; if not, tests will adapt
        if not self.engine.keywords:
            # inject a minimal keywords set for testing
            self.engine.keywords = {
                "ethics": ["ethics", "fairness", "bias"],
                "security": ["security", "breach", "encryption"],
                "health": ["health", "patient", "clinical"]
            }

    def test_empty_scenario(self):
        res = self.engine.analyze_scenario("")
        self.assertIn("top_categories", res)
        self.assertEqual(len(res["top_categories"]), 0)

    def test_simple_matching(self):
        scenario = "A hospital AI that misdiagnoses patients could be an ethical issue."
        res = self.engine.analyze_scenario(scenario)
        # should at least produce some score for 'health' or 'ethics'
        cats = [c for c, _ in res["top_categories"]]
        self.assertTrue(any(c in ("health", "ethics") for c in cats))

    def test_causal_pair_detection(self):
        # Create custom keywords and causal map to guarantee detection
        self.engine.keywords = {
            "health": ["medical", "patient", "hospital"],
            "ethics": ["ethic", "consent", "fairness"]
        }
        self.engine.causal_map = {
            frozenset(["health", "ethics"]): "health impacts raise ethical concerns"
        }
        scenario = "Medical AI in hospitals raises questions about patient consent and fairness."
        res = self.engine.analyze_scenario(scenario)
        self.assertTrue(len(res["causal_explanations"]) >= 1)
        self.assertEqual(res["causal_explanations"][0]["explanation"], "health impacts raise ethical concerns")

if __name__ == "__main__":
    unittest.main()
