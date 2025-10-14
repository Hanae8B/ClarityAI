"""
explanation_engine.py – Core reasoning engine for ClarityAI
------------------------------------------------------------
Hybrid semantic similarity:
- SentenceTransformers embeddings (preferred)
- spaCy embeddings (fallback)
- Keyword overlap (fallback)
Generates top categories and causal explanations.
"""

import logging
from utils import load_demo_keywords

# Embedding setup
USE_EMBEDDINGS = False
EMBEDDING_MODEL = None

try:
    from sentence_transformers import SentenceTransformer, util
    EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    USE_EMBEDDINGS = True
except Exception:
    try:
        import spacy
        NLP = spacy.load("en_core_web_md")
        USE_EMBEDDINGS = True
        EMBEDDING_MODEL = None
    except Exception:
        USE_EMBEDDINGS = False
        EMBEDDING_MODEL = None

logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO
)
if USE_EMBEDDINGS:
    logging.info("Using embedding-based semantic similarity.")
else:
    logging.info("Using keyword overlap similarity (fallback).")

# Explanation Engine
class ExplanationEngine:
    def __init__(self, keyword_csv="../data/demo_keywords.csv", top_n=3, threshold=0.1):
        self.model_name = "ClarityAI_Model_v1"
        self.keywords = load_demo_keywords(keyword_csv)
        self.top_n = top_n
        self.threshold = threshold

        self.causal_map = {
    ("blockchain", "security"): "Blockchain transactions rely on cryptographic security; tampering can compromise integrity.",
    ("blockchain", "ethics"): "Blockchain voting errors may affect fairness and accountability.",
    ("security", "ethics"): "Security breaches can violate ethical principles of transparency and fairness.",
    ("health", "ethics"): "Medical AI errors may violate ethical responsibility to patients.",
    ("financial", "ethics"): "Financial irregularities may conflict with ethical governance and accountability.",
    ("industrial", "safety"): "Industrial hazards can compromise worker safety protocols.",
    ("robotics", "safety"): "Autonomous robotic actions may risk workplace safety.",
    ("media", "ethics"): "AI-generated misinformation in media raises ethical concerns.",
    ("communication", "ethics"): "Chatbot or assistant misbehavior can cause ethical or fairness implications.",
    ("transportation", "ethics"): "AI in transportation may face ethical dilemmas during emergencies.",
    ("environmental", "ethics"): "Neglecting environmental impact can violate ethical sustainability norms.",
    ("health", "safety"): "Medical errors can endanger patient safety.",
    ("financial", "security"): "Financial data breaches threaten transaction security.",
    ("industrial", "environmental"): "Industrial emissions contribute to environmental degradation.",
    ("robotics", "industrial"): "Robotics automation impacts industrial efficiency and safety.",
    ("transportation", "safety"): "Traffic AI or autonomous vehicles may risk public safety.",
    ("health", "ethics"): "Healthcare AI errors can breach patient privacy or violate ethical care standards.",
    ("media", "transportation"): "Incorrect media reporting on transportation incidents can affect public perception and safety.",
    ("media", "health"): "Misinformation in health-related media can endanger patient decisions.",
    ("communication", "safety"): "Misinterpreted commands can lead to safety hazards.",
    ("environmental", "safety"): "Environmental hazards may threaten human safety.",
    ("robotics", "transportation"): "Autonomous robotic systems can interfere with transportation safety.",
    ("financial", "ethics"): "AI financial recommendations may conflict with ethical and regulatory standards."
}

    # Semantic similarity functions
    def _semantic_similarity_basic(self, scenario: str, keywords: list[str]) -> float:
        if not scenario or not keywords:
            return 0.0
        scenario_lower = scenario.lower()
        matches = sum(1 for kw in keywords if kw.lower() in scenario_lower)
        return matches / len(keywords)

    def _semantic_similarity_embeddings(self, scenario: str, keywords: list[str]) -> float:
        if EMBEDDING_MODEL:  # SentenceTransformers
            scenario_emb = EMBEDDING_MODEL.encode(scenario, convert_to_tensor=True)
            keywords_text = ", ".join(keywords)
            keywords_emb = EMBEDDING_MODEL.encode(keywords_text, convert_to_tensor=True)
            score = float(util.cos_sim(scenario_emb, keywords_emb))
            return max(0.0, score)
        elif USE_EMBEDDINGS:  # spaCy fallback
            scenario_doc = NLP(scenario)
            keywords_doc = NLP(", ".join(keywords))
            return float(scenario_doc.similarity(keywords_doc))
        else:
            return self._semantic_similarity_basic(scenario, keywords)

    def semantic_similarity(self, scenario: str, keywords: list[str]) -> float:
        return self._semantic_similarity_embeddings(scenario, keywords) if USE_EMBEDDINGS else self._semantic_similarity_basic(scenario, keywords)

    # Main analysis
    def analyze_scenario(self, scenario: str) -> dict:
        if not scenario or not isinstance(scenario, str):
            return {"error": "Invalid scenario input."}

        scores = {}
        for category, words in self.keywords.items():
            sim = self.semantic_similarity(scenario, words)
            if sim >= self.threshold:
                scores[category] = sim

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.top_n]

        causal_explanations = []
        if len(sorted_scores) > 1:
            for i in range(len(sorted_scores)):
                for j in range(i + 1, len(sorted_scores)):
                    c1, c2 = sorted_scores[i][0], sorted_scores[j][0]
                    if (c1, c2) in self.causal_map:
                        causal_explanations.append(f"{c1} + {c2}: {self.causal_map[(c1, c2)]}")
                    elif (c2, c1) in self.causal_map:
                        causal_explanations.append(f"{c2} + {c1}: {self.causal_map[(c2, c1)]}")

        return {
            "scenario": scenario.strip(),
            "top_categories": sorted_scores,
            "causal_explanations": causal_explanations,
            "model": self.model_name,
        }
